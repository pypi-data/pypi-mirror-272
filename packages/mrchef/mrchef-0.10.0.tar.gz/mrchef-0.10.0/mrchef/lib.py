"""Mr. Chef's core functionality."""

import json
import os
import re
import sys
import warnings
from collections.abc import Generator
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import lru_cache
from logging import DEBUG, ERROR, captureWarnings, getLogger
from pathlib import Path
from shutil import rmtree
from textwrap import dedent
from typing import NamedTuple
from urllib.parse import ParseResult, urlparse

import coloredlogs
import requests
import rtoml
import tomlkit
from git_find_repos import find_repos
from plumbum import local
from plumbum.commands.processes import ProcessExecutionError
from requests.exceptions import HTTPError

CONFIG_FILE = "mrchef.toml"
CONFIG_VERSION = 1
FREEZER_FILE = ".mrchef.freezer.toml"
FREEZER_VERSION = 2


def now():
    """Return tz-aware current datetime.

    If an environment variable `MRCHEF_MOCK_DATE` is set, return that instead.
    It is helpful for testing, or for generating reproducible freezes.
    """
    try:
        return datetime.fromisoformat(os.environ["MRCHEF_MOCK_DATE"])
    except KeyError:
        return datetime.now(tz=UTC)


logger = getLogger("mrchef")
coloredlogs.install(logger=logger, level=0)

# Combine with warnings
warnings_logger = getLogger("py.warnings")
coloredlogs.install(logger=warnings_logger, level=0)
captureWarnings(True)


class MrChefError(Exception):
    """Core MrChef exception.

    It will be handled and pretty-printed when raised to CLI.
    """

    def __init__(self, msg: str, trace_level=DEBUG):
        """Initialize the exception.

        Args:
            msg: The message to present to the user.
            trace_level: Level used to log the exception traceback.
        """
        self.msg = msg
        self.trace_level = trace_level


@dataclass
class Meal:
    """Store warm and frozen configurations for meals (sub-repositories)."""

    # From a human
    path: Path
    url: str
    branch: str

    # From the freezer
    last_update: datetime = field(default_factory=now)
    rev: str | None = None
    spices: list[str] = field(default_factory=list)


class BiMeal(NamedTuple):
    """An item that contains 2 meals: the frozen one and the hot one.

    One of them could be `None`, if not found.
    """

    cold: Meal | None
    hot: Meal | None


class Worker:
    """Get meta-repo status and do stuff with it."""

    def __init__(self, starting_folder: Path | None = None):
        """Load configuration from starting path upwards.

        Starts traversing directories upwards, looking for a `mrchef.toml` file,
        and loads it.
        """
        if starting_folder is None:
            starting_folder = Path()
        assert starting_folder.is_dir()
        current = starting_folder.absolute()
        top = Path(current.root)
        while current > top:
            current_file = current / CONFIG_FILE
            try:
                fd = current_file.open("r")
            except FileNotFoundError:
                current = current.parent
                continue
            self.path = current
            self.config_file = current_file
            self.config_user = tomlkit.load(fd)
            break
        else:
            raise MrChefError(f"No {CONFIG_FILE} file found here or in parent folders.")
        # Attempt to merge normal config with frozen one
        self.freezer_file = self.path / FREEZER_FILE
        try:
            # Style in the freezer isn't preserved, so we use rtoml it to be faster
            self.config_frozen = rtoml.load(self.freezer_file)
        except FileNotFoundError:
            warnings.warn("Freezer file not found.", stacklevel=2)
            self.config_frozen = {}
        # Setup self and do some checks
        if self.config_user["version"] != CONFIG_VERSION:
            logger.warning(
                "%s has version %s instead of %s; update it or bad things could happen",
                self.config_file,
                self.config_user["version"],
                CONFIG_VERSION,
            )
        self.kitchen = self.path / self.config_user["kitchen"]
        self.config_frozen.setdefault("meals", {})
        self.config_frozen.setdefault("patch2spice", {})
        self.config_frozen.setdefault("spices", {})
        if self.config_frozen.get("version", FREEZER_VERSION) != FREEZER_VERSION:
            logger.warning(
                "%s has version %s instead of %s; re-freeze or bad things could happen",
                self.freezer_file,
                self.config_frozen.get("version"),
                FREEZER_VERSION,
            )
        self.config_frozen.setdefault("version", FREEZER_VERSION)
        self._cached_hot_spices = {}

    def _cache_spices(self):
        """Make sure all spices cache is updated."""
        for meal_value in self.config_user.get("meals", {}).values():
            for spice_url in meal_value.get("spices", []):
                self._get_spice_content(spice_url)

    def _get_meal_key_by_path(self, meal_path: Path) -> str:
        """Get the meal key by its path."""
        meal_abs = meal_path.absolute().resolve()
        kitchen_abs = self.kitchen.absolute().resolve()
        if not meal_abs.is_relative_to(kitchen_abs):
            raise MrChefError(
                f"The meal {meal_path} is not inside the kitchen {self.kitchen}"
            )
        return str(meal_abs.relative_to(kitchen_abs))

    def _get_spice_content(self, spice_url: str, force_update=False) -> str:
        """Get spice content.

        Return the raw text of the patch.

        If the spice wasn't in the freezer, download it automatically and cache it.

        Args:
            meal_key: Key of the meal in the config file.
            spice_url: Patch URL.
            force_update: Ignore cached contents in the freezer.
        """
        if force_update:
            # Locate local patch
            local_patch = Path(spice_url)
            if not local_patch.is_absolute():
                local_patch = self.path / local_patch
            # Get content from local cache, local file or from the Internet
            try:
                content = self._cached_hot_spices[spice_url]
            except KeyError:
                content = (
                    local_patch.read_text()
                    if local_patch.is_file()
                    else download_spice(spice_url)
                )
            self.config_frozen["spices"][spice_url] = content
            for patch_id in git_get_patch_ids_map(self.path, content):
                self.config_frozen["patch2spice"][patch_id] = spice_url
        try:
            # Get cached content
            return self._cached_hot_spices.get(
                spice_url, self.config_frozen["spices"][spice_url]
            )
        except KeyError:
            # Cached content not found, get it from the Internet
            logger.info(f"Spice was not frozen, downloading: {spice_url}")
            return self._get_spice_content(spice_url, True)

    def _patches_generator(self) -> Generator[Path, None, None]:
        """A generator that creates new patch file names in the kitchen."""
        num = 0
        while True:
            patch_path = self.kitchen / f"mrchef-{num:03d}.patch"
            if not patch_path.exists():
                yield patch_path
            num += 1

    def _new_patch(self) -> Path:
        """Generate a new patch file name in the kitchen."""
        try:
            generator = self._cached_patch_generator
        except AttributeError:
            self._cached_patch_generator = self._patches_generator()
            generator = self._cached_patch_generator
        return next(generator)

    def _nar_hash(self, meal: Meal) -> str:
        """Get Nix hash for a meal.

        This will take longer to freeze, but it will make Nix expressions
        faster to evaluate later.

        TODO: Possibly not needed when [Nix's RFC 133 is implemented][1].

        [1]: https://github.com/NixOS/nix/issues/8919
        """
        assert meal.rev
        # Get cached hash if possible
        with suppress(MrChefError, KeyError):
            key = self._get_meal_key_by_path(meal.path)
            cold_config = self.config_frozen["meals"][key]
            if cold_config["rev"] == meal.rev:
                return cold_config["nar_hash"]
        # Get hash from Nix
        logger.info("Getting NAR hash for %s @ %s", meal.url, meal.branch)
        fetcher = Path(__file__).parent / "nix" / "fetchMeal.nix"
        json_hash = local["nix-instantiate"](
            "--extra-experimental-features",
            "flakes",
            "--json",
            "--eval",
            fetcher,
            "--argstr",
            "returnAttr",
            "narHash",
            "--argstr",
            "url",
            meal.url,
            "--argstr",
            "branch",
            meal.branch,
            "--argstr",
            "rev",
            meal.rev,
        )
        return json.loads(json_hash)

    def _is_auto_patch(self, patch_path: Path) -> bool:
        """Check if the patch was generated by MrChef."""
        return (
            patch_path.name.startswith("mrchef-")
            and patch_path.suffix == ".patch"
            and patch_path.parent == self.kitchen
        )

    @classmethod
    def init(cls, where: Path) -> "Worker":
        """Initialize a new kitchen."""
        where.joinpath(CONFIG_FILE).write_text(
            dedent(
                f"""\
                version = {CONFIG_VERSION}
                kitchen = "kitchen"

                # Remove if you don't need Nix integration
                require_nar_hash = true

                # Add meals like this:
                # [meals.starter]
                # url = "https://gitlab.example.com/menu/starter.git"
                # branch = "delicacy"

                # You can add special spices to your version of this meal:
                # spices = [
                #     # Special shared spices for this metarepo
                #     "https://gitlab.example.com/menu/starter/-/merge_requests/1.patch",
                #     "https://gitlab.example.com/menu/starter/-/commit/14ebafa278a28a08b9660e6ccab33fc72bbccd17.patch",
                #     "https://github.com/menu/starter/pull/45.patch",
                #     "https://github.com/menu/starter/commit/430e53b9de9cf986d8236061eeb77ae35fd03f55",
                #     # This special spice is only for us
                #     "./local-extra-spicy.patch",
                # ]

                # Add more meals:
                # [meals.dessert]
                # url = "git@github.com/menu/dessert.git"
                # branch = "pudding"

                # After you're done adding meals, get them:
                # $ mrchef warmup

                # After you're done cooking, put them in the freezer, for reproducibility:
                # $ mrchef freeze
                """
            )
        )
        where.joinpath(FREEZER_FILE).touch()
        return cls(where)

    def cold_meals(self) -> dict[str, Meal]:
        """Get meals info from the freezer."""
        return {
            key: Meal(
                path=self.kitchen / key,
                url=value["url"],
                branch=value["branch"],
                rev=value.get(
                    "rev", self.config_frozen["meals"].get(key, {}).get("rev")
                ),
                spices=value.get("spices", []),
            )
            for key, value in self.config_user.get("meals", {}).items()
        }

    def hot_meals(self, *meal_keys: str) -> dict[str, Meal]:
        """Get info from the hot meals found in the kitchen."""
        result = {}
        if not self.kitchen.is_dir():
            return result
        self._cache_spices()
        for meal_path in map(Path, find_repos(self.kitchen)):
            key = self._get_meal_key_by_path(meal_path)
            if meal_keys and key not in meal_keys:
                continue
            branch = git_branch(meal_path)
            url = self.config_user.get(key, {}).get("url") or git_origin(meal_path)
            remote_head = git_remote_head(meal_path, url, branch)
            meal = Meal(
                path=meal_path,
                url=url,
                branch=branch,
                # Revision is not the current commit; it's the closest common
                # parent between local and remote commits
                rev=git_merge_base(meal_path, remote_head, "HEAD"),
            )
            # Get last update date from freezer if possible
            with suppress(KeyError):
                meal.last_update = self.config_frozen["meals"][key]["last_update"]
            # Build spices from local changes
            for hot_commit in git_commits_diff(meal_path, meal.rev, "HEAD"):
                hot_patch_id = git_commit_patch_id(meal_path, hot_commit)
                try:
                    # Get patch URL from freezer
                    hot_spice_url = self.config_frozen["patch2spice"][hot_patch_id]
                except KeyError:
                    # The patch is local; cache it locally
                    local_path = self._new_patch()
                    local_contents = git_get_commit_patch(meal_path, hot_commit)
                    hot_spice_url = str(local_path.relative_to(self.path))
                    self._cached_hot_spices[hot_spice_url] = local_contents
                # A spice can contain various commits, so it could exist already
                if hot_spice_url not in meal.spices:
                    meal.spices.append(hot_spice_url)
            result[key] = meal
        return result

    def all_meals(self, *meal_paths: Path) -> dict[str, BiMeal]:
        """Obtain all meals, both warmed up and frozen.

        Useful to compare meals in both states.

        Args:
            meal_paths: Filter only meals related to these paths.

        Returns:
            Dict with all meals and their states.

            The dict key will be the meal name (relative path to kitchen root).

            The dict value will be another dict with keys "hot" and "cold".
            Each of those keys will contain `None` if the meal is not found in
            that state, or a [Meal][] object if found.

            !!! example

                ```python
                {
                    "sashimi": {
                        "hot": None,
                        "cold": Meal(...),
                    },
                    "pizza/pepperoni": {
                        "hot": Meal(...),
                        "cold": Meal(...),
                    },
                }
                ```
        """
        cold = self.cold_meals()
        meal_keys = {self._get_meal_key_by_path(meal_path) for meal_path in meal_paths}
        invented_meals = meal_keys - set(cold)
        if invented_meals:
            raise MrChefError(
                f"Couldn't find meal(s) in freezer: {', '.join(sorted(invented_meals))}"
            )
        hot = self.hot_meals(*meal_keys)
        all_keys = set(cold) | set(hot)
        if meal_paths:
            all_keys &= set(meal_keys)
        all_keys = sorted(all_keys)
        return {key: BiMeal(cold.get(key), hot.get(key)) for key in all_keys}

    def update_user_config(self):
        """Update user config."""
        tomlkit.dump(self.config_user, self.config_file.open("w"))

    def check(self):
        """Check freezer and oven are in sync."""
        errors = []
        for key, (cold, hot) in self.all_meals().items():
            if cold is None:
                errors.append(f"Meal {key} is hot but not frozen")
                continue
            if hot is None:
                errors.append(f"Meal {key} is frozen but not hot")
                continue
            if hot.url != cold.url:
                errors.append(
                    f"Meal {key} is frozen with origin {cold.url}, but hot with origin {hot.url}"
                )
            if hot.rev != cold.rev:
                errors.append(
                    f"Meal {key} is frozen with rev {cold.rev}, but hot with rev {hot.rev}"
                )
            if hot.spices != cold.spices:
                errors.append(
                    f"Meal {key} spices are different. frozen={cold.spices} warm={hot.spices}"
                )
        try:
            if self.config_frozen != rtoml.load(self.freezer_file):
                errors.append("Freezer is outdated.")
        except FileNotFoundError:
            errors.append("Freezer not found.")
        if errors:
            raise MrChefError("🔪 Found errors:\n" + "\n".join(errors))
        logger.info("All frozen and hot meals are ready! 👨‍🍳")

    def warmup(self, *meal_paths: Path, force: bool = False):
        """Get meals out from freezer, warm them up in the kitchen.

        Args:
            *meal_paths: Meals to warm up. Skip to select all.
            force: Continue warming up meal if it is dirty.
        """
        for key, (cold, hot) in self.all_meals(*meal_paths).items():
            # Nothing to do if something is not in the freezer
            if not cold:
                continue
            if hot == cold:
                logger.info("Matches frozen status, skipping meal: %s", key)
                continue
            # Clone if meal is not in the kitchen
            if not hot:
                logger.info("Cloning %s", key)
                local["git-autoshare-clone"](
                    "--recursive",
                    "--filter",
                    "blob:none",
                    "--branch",
                    cold.branch,
                    cold.url,
                    cold.path,
                )
            _git = git(cold.path)
            was_dirty = git_is_dirty(cold.path)
            if was_dirty:
                if not force:
                    raise MrChefError(f"Meal {key} is dirty.")
                logger.info("Stashing dirty changes at %s", key)
                _git(
                    "stash",
                    "push",
                    "--all",
                    "--message",
                    f"MrChef dirty meal - {hot.branch} - {datetime.now()}",
                )
                # Discard other dirty operations
                _git("am", "--abort", retcode=None)
                _git("cherry-pick", "--abort", retcode=None)
                _git("merge", "--abort", retcode=None)
                _git("rebase", "--abort", retcode=None)
            logger.info(
                "Updating %s: remote=%s branch=%s rev=%s",
                key,
                cold.url,
                cold.branch,
                cold.rev,
            )
            remote_head = git_remote_head(
                cold.path, cold.url, cold.rev or cold.branch, not cold.rev
            )
            _git("switch", "--force-create", cold.branch, cold.rev or remote_head)
            for spice in cold.spices:
                logger.info("Applying spice to %s: %s", key, spice)
                content = self._get_spice_content(spice)
                self.spice_apply(cold.path, content)
        # Some hot meals may have been modified
        git_remote_head.cache_clear()

    def freeze(self):
        """Get meals from the kitchen and put them in the freezer."""
        logger.info("Freezing...")
        new_freezer = {
            "version": FREEZER_VERSION,
            "meals": {},
            "spices": {},
            "patch2spice": {},
        }
        for name, meal in sorted(self.hot_meals().items()):
            assert meal.rev
            new_freezer["meals"][name] = {
                "last_update": meal.last_update,
                "rev": meal.rev,
            }
            if self.config_user.get("require_nar_hash"):
                new_freezer["meals"][name]["nar_hash"] = self._nar_hash(meal)
            # Force cast to str for compatibility with rtoml.dump
            for spice_url in map(str, meal.spices):
                spice_content = self._get_spice_content(spice_url)
                new_freezer["spices"][spice_url] = spice_content
                for patch_id in git_get_patch_ids_map(meal.path, spice_content):
                    new_freezer["patch2spice"][patch_id] = spice_url
                local_patch = self.path / spice_url
                if self._is_auto_patch(local_patch) and not local_patch.exists():
                    local_patch.write_text(spice_content)
                # Store spice in user config
                if spice_url not in self.config_user["meals"][name].get("spices", []):
                    self.config_user["meals"][name].setdefault("spices", []).append(
                        spice_url
                    )
        with self.freezer_file.open("w") as fd:
            fd.write("# MrChef's freezer. MANUAL CHANGES WILL BE OVERRIDDEN.\n")
            rtoml.dump(new_freezer, fd, pretty=True)
        self.config_frozen = new_freezer
        # Because maybe we detected hot patches in the mean time
        self.update_user_config()

    def meal_add(self, meal_path: Path, url: str, branch: str, rev: str | None = None):
        """Add a new meal to the kitchen and the freezer."""
        meal_path = meal_path.absolute()
        kitchen = self.kitchen.absolute()
        if not meal_path.is_relative_to(kitchen):
            raise MrChefError(
                f"The meal path must be inside the configured kitchen {kitchen}"
            )
        key = str(meal_path.relative_to(kitchen))
        self.config_user.setdefault("meals", {})
        logger.info(
            "Adding meal %s: remote=%s branch=%s rev=%s",
            key,
            url,
            branch,
            rev,
        )
        self.config_user["meals"][key] = {"url": url, "branch": branch}
        if rev:
            self.config_user["meals"][key]["rev"] = rev
        self.warmup(meal_path)
        self.freeze()

    def meal_rm(self, meal_path: Path):
        """Remove a meal from the kitchen."""
        meals = self.cold_meals()
        key = self._get_meal_key_by_path(meal_path)
        del self.config_user["meals"][key]
        logger.info("Removing meal %s", key)
        with suppress(FileNotFoundError):
            rmtree(meals[key].path)
        self.freeze()

    def spice_add(self, meal_path: Path, url: str):
        """Download a patch and spice up meal with it."""
        if git_is_dirty(meal_path):
            raise MrChefError("Cannot add spice to dirty meal {meal_path}")
        key = self._get_meal_key_by_path(meal_path)
        meal = self.hot_meals(key)[key]
        content = self._get_spice_content(url, True)
        if self.spice_is_applied(meal, content):
            raise MrChefError(f"Spice already exists: {url}")
        self.spice_apply(meal_path, content)
        self.config_user["meals"][key].setdefault("spices", [])
        self.config_user["meals"][key]["spices"].append(url)
        self.freeze()

    def spice_rm(self, meal_path: Path, url: str):
        """Remove a patch from a meal.

        After successfully removing it, the meal will be re-warmed up and the
        config and freezer files will be updated.

        Args:
            meal_path: Where to find the meal.
            url: Spice URL to remove.
        """
        if git_is_dirty(meal_path):
            raise MrChefError("Cannot remove spice from dirty meal {meal_path}")
        key = self._get_meal_key_by_path(meal_path)
        logger.info("Removing spice from %s: %s", key, url)
        try:
            self.config_user["meals"][key]["spices"].remove(url)
        except ValueError as error:
            raise MrChefError(
                f"Cannot remove spice, not found in meal {key}: {url}"
            ) from error
        # If it was an autogenerated patch file, remove it
        patch_file = self.path / url
        if self._is_auto_patch(patch_file):
            patch_file.unlink(missing_ok=True)
        # Clean the kitchen
        self.warmup(meal_path)
        self.freeze()

    def spice_export(self, url: str) -> str:
        """Export spice contents from the freezer.

        Args:
            url: The url that was frozen.
        """
        return self.config_frozen["spices"][url]

    def spice_is_applied(self, meal: Meal, spice_content: str) -> bool:
        """Check if a spice is already appled."""
        # See https://stackoverflow.com/a/66755317/1468388
        check = git(meal.path)["apply", "--reverse", "--check"] << spice_content
        try:
            check()
        except ProcessExecutionError:
            # Patch cannot be reversed, so it was never applied
            return False
        return True

    def spice_apply(self, meal_path: Path, spice_content: str):
        """Spice up a meal."""
        _git = git(meal_path)
        apply = _git["am", "--keep-non-patch", "--3way"] << spice_content
        try:
            apply()
        except ProcessExecutionError as error:
            _git("am", "--abort")
            raise MrChefError("Failed to apply spice.", ERROR) from error

    def update(
        self,
        *meal_paths: Path,
        force: bool = False,
        oldest: int = 0,
        autocommit: bool = False,
    ):
        """Update hot meals, store changes in the freezer.

        Args:
            *meal_paths: Meals to update. Skip to select all.
            force: Continue warming up meal if it is dirty.
            oldest: Update this many oldest ones among found meals. If 0, update all.
            autocommit: Commit changes to the meal after updating.
        """
        if autocommit and git_is_dirty(self.path):
            logger.warning(
                "Repo is dirty; autocommit could contain non-mrchef changes."
            )
        meal_keys = (
            {self._get_meal_key_by_path(meal_path) for meal_path in meal_paths}
            if meal_paths
            else list(self.config_frozen.get("meals", {}).keys())
        )
        sorted_keys = sorted(
            meal_keys,
            key=lambda key: self.config_frozen["meals"]
            .get(key, {})
            .get("last_update", datetime.min),
        )
        old_meals = {}
        for num, key in enumerate(sorted_keys):
            if oldest and num >= oldest:
                break
            # Clear meal cache
            old_meals[key] = self.config_frozen["meals"].pop(key, {}).get("rev")
            for spice in self.config_user["meals"].get(key, {}).get("spices", []):
                self.config_frozen["spices"].pop(spice, None)
        # Warm up again without some caches
        self.warmup(*meal_paths, force=force)
        # Write changes to freezer
        self.freeze()
        if autocommit:
            self._autocommit(old_meals)

    def _autocommit(self, old_meals: dict[str, str | None]) -> None:
        """Get commit message for an update.

        The message respects [Conventional
        Commits](https://www.conventionalcommits.org/).

        Args:
            old_meals:
                Dict indicating a meal name and its previous revision. If the
                revision is `None`, it means the meal was not previously frozen.
        """
        if not git_is_dirty(self.path):
            logger.info("Nothing to commit.")
            return
        lines = ["build(mrchef): update kitchen", ""]
        for key, old_long in old_meals.items():
            repo_url = self.config_user["meals"][key]["url"]
            new_long = self.config_frozen["meals"][key]["rev"]
            new_short = new_long[:8]
            if old_long is None:
                try:
                    lines.append(
                        f"- {key}: Frozen at [{new_short}]({commit_url(repo_url, new_long)})"
                    )
                except NotImplementedError:
                    lines.append(f"- {key}: Frozen at {new_long}")
                continue
            old_short = old_long[:8]
            if old_long == new_long:
                continue
            try:
                lines.append(
                    f"- {key}: [{old_short}..{new_short}]({commit_range_url(repo_url, old_long, new_long)})"
                )
            except NotImplementedError:
                lines.append(f"- {key}: {old_long}..{new_long}")
        logger.info("Committing changes")
        _git = git(self.path)
        _git("add", self.config_file, self.freezer_file)
        _commit = _git["commit", "-am", "\n".join(lines)]
        if sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty():
            _commit = _commit["--edit"]
        # Pre-commit can fail; attempt to commit twice
        try:
            _commit()
        except ProcessExecutionError:
            _commit()


def commit_url(repo_url: str, commit_sha: str) -> str:
    """Get the URL to a commit in a repository."""
    with suppress(TypeError):
        return github_url(repo_url) + f"/commit/{commit_sha}"
    with suppress(TypeError):
        return gitlab_url(repo_url) + f"/-/commit/{commit_sha}"
    raise NotImplementedError(f"Unknown repository URL: {repo_url}")


def commit_range_url(repo_url: str, commit_from: str, commit_to: str) -> str:
    """Get the URL to a commit range in a repository."""
    with suppress(TypeError):
        return github_url(repo_url) + f"/compare/{commit_from}...{commit_to}"
    with suppress(TypeError):
        return gitlab_url(repo_url) + f"/-/compare/{commit_from}...{commit_to}"
    raise NotImplementedError(f"Unknown repository URL: {repo_url}")


def parse_git_url(url: str) -> ParseResult:
    """Normalize a Git URL and return it parsed."""
    parsed = urlparse(url)
    if not parsed.scheme and not parsed.netloc:
        # SSH URL
        url = "ssh://" + url.replace(":", ":22/", 1)
        return urlparse(url)
    return parsed


def github_url(url: str) -> str | None:
    """Get browsable URL for a repo, if it is from Github.

    Args:
        url: The URL to check.
    """
    parsed = parse_git_url(url)
    if parsed.hostname != "github.com":
        return
    owner, repo, *_rest = parsed.path.split("/")[1:]
    repo = repo.removesuffix(".git")
    return f"https://github.com/{owner}/{repo}"


def gitlab_url(url: str) -> str | None:
    """Get browsable URL for a repo, if it is from Gitlab.

    Since Gitlab can be self-hosted, to be sure it is Gitlab, the host name
    must contain the word "gitlab" somewhere.

    Sample URLs supported:
    - https://gitlab.com/owner/repo
    - https://gitlab.example.com/group/subgroup/repo.git
    - https://gitlab.example.com/owner/repo
    - https://gitlab.example.com/owner/repo/-/merge_requests/1
    - https://gitlab.example.com/group/subgroup/repo/-/merge_requests/1
    - git@gitlab.com:group/subgroup/repo.git
    - ssh://git@gitlab.example.com:2222/group/subgroup/repo.git

    Args:
        url: The URL to check.
    """
    url = url.split("/-/")[0].removesuffix(".git")
    parsed = parse_git_url(url)
    if "gitlab" not in parsed.hostname:
        return
    if parsed.scheme == "ssh":
        return f"https://{parsed.hostname}{parsed.path}"
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


def download_spice(spice_url: str) -> str:
    """Download spice from URL.

    Supports these URL formats:

    - Gitlab merge request, like https://gitlab.com/moduon/mrchef/-/merge_requests/1
    - Gitlab commit, like https://gitlab.com/moduon/mrchef/-/commit/4699372d84f7f67b52fc7548f606e9a42559b5c2
    - Github pull request, like https://github.com/octocat/Hello-World/pull/1
    - Github commit, like https://github.com/octocat/Hello-World/commit/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d
    - Any other URL, downloaded without modifications.
    """
    request_params = {}
    parsed_url = urlparse(spice_url)
    transformed_url = spice_url
    # Get Github spices from API
    if github_url(spice_url):
        mime = "diff" if parsed_url.path.endswith(".diff") else "patch"
        request_params["headers"] = {
            "Accept": f"application/vnd.github.v3.{mime}",
        }
        if "GITHUB_TOKEN" in os.environ:
            # Authenticate with Github API
            request_params["headers"][
                "Authorization"
            ] = f"Bearer {os.environ['GITHUB_TOKEN']}"
        else:
            logger.warning(
                f"Downloading spice from Github without authentication: {spice_url}"
            )
        # Alter spice URL to use API
        match (
            parsed_url.path.strip("/")
            .removesuffix(".diff")
            .removesuffix(".patch")
            .split("/")
        ):
            case [org, repo, "pull", pr_number] if pr_number.isdecimal():
                transformed_url = (
                    f"https://api.github.com/repos/{org}/{repo}/pulls/{pr_number}"
                )
            case [org, repo, "commit", commit_sha]:
                transformed_url = (
                    f"https://api.github.com/repos/{org}/{repo}/commits/{commit_sha}"
                )
            case [org, repo, "files", *_]:
                pass  # Download files directly
            case _:
                transformed_url = spice_url.rstrip("/") + f".{mime}"
    elif gitlab_url(spice_url) and not parsed_url.path.endswith(".patch"):
        # TODO Handle Gitlab authentication
        transformed_url = spice_url.rstrip("/") + ".patch"
    # Report transformation
    if transformed_url != spice_url:
        logger.debug(
            "Attempting to download transformed spice URL: %s ➡️ %s",
            spice_url,
            transformed_url,
        )
    try:
        response = requests.get(transformed_url, **request_params)
        response.raise_for_status()
    except HTTPError:
        if transformed_url == spice_url:
            raise
        # Fallback to original URL
        logger.debug("Attempting to download spice from %s", spice_url)
        response = requests.get(spice_url, **request_params)
        response.raise_for_status()
    return response.text


def git(folder: Path | None = None) -> str:
    """Get a git executable ready to operate in `folder`."""
    _git = local["git"]
    if folder:
        _git = _git["-C", folder]
    return _git


def git_branch(folder: Path) -> str:
    """Get current branch name in that git folder."""
    return git(folder)("rev-parse", "--abbrev-ref", "HEAD").strip()


def git_commit_patch_id(folder: Path, commit_id: str) -> str:
    """Get the patch ID from a commit ID.

    And what is a patch ID? See https://git-scm.com/docs/git-patch-id
    """
    commit_patch = git_get_commit_patch(folder, commit_id)
    patch_id_map = git_get_patch_ids_map(folder, commit_patch)
    assert len(patch_id_map) == 1
    return list(patch_id_map)[0]


def git_commits_diff(folder: Path, rev1: str, rev2: str) -> list[str]:
    """Get differential commits between rev1 and rev2."""
    return git(folder)(
        "log", "--topo-order", "--reverse", "--format=%H", f"{rev1}...{rev2}"
    ).splitlines()


def git_get_commit_patch(folder: Path, commit: str) -> str:
    """Get patch text contents from a git commit."""
    return git(folder)("format-patch", "-1", "--stdout", "--binary", commit)


def git_get_patch_ids_map(folder: Path, patch_text: str) -> dict:
    """Get patch ids from patch text."""
    patch_id_map = git(folder)["patch-id", "--stable"] << patch_text
    return {
        patch_id: commit_id
        for patch_id, commit_id in (
            line.split() for line in patch_id_map().splitlines()
        )
    }


def git_is_dirty(folder: Path) -> bool:
    """Know if the folder is a dirty git repository."""
    _git = git(folder)
    if _git("status", "--porcelain"):
        return True
    if _git("am", "--show-current-patch", retcode=None):
        return True
    return False


def git_origin(folder: Path) -> str:
    """Know the git origin URL for Mr. Chef's default origin."""
    _git = git(folder)
    # See https://stackoverflow.com/a/60297250/1468388
    status = _git("status", "--branch", "--porcelain=v2")
    if not (match := re.search(r"^# branch.upstream (.*)/.*$", status, re.MULTILINE)):
        raise MrChefError(
            f"Couldn't guess remote origin for {folder}. "
            "Please make sure it's checked out in a branch with a remote."
        )
    origin = match[1]
    return _git("remote", "get-url", origin).strip()


def git_merge_base(folder: Path, rev1: str, rev2: str) -> str:
    """Know the closest common ancestor commit of 2 git revisions.

    Args:
        folder: Path to git repo.
        rev1: First commit to compare.
        rev2: Second commit to compare.
    """
    return git(folder)("merge-base", rev1, rev2).strip()


@lru_cache
def git_remote_head(
    folder: Path, remote_url: str, remote_ref: str, force_fetch: bool = False
) -> str:
    """Get latest commit sha from remote url and ref combination.

    Args:
        folder: Path to git repo.
        remote_url: Absolute URL to remote.
        remote_ref: Branch or revision to query from remote.
        force_fetch: Do not use a locally cached remote head.
    """
    _git = git(folder)
    remote_alias = git_remote_alias(folder, remote_url)
    if not force_fetch and remote_alias:
        try:
            return _git(
                "rev-parse", f"refs/remotes/{remote_alias}/{remote_ref}"
            ).strip()
        except ProcessExecutionError:
            # Remote ref not found locally, fetch it
            pass
    # By attempting to fetch using the alias instead of the URL, we force Git
    # to cache the result, so next calls with force_fetch=False will be faster
    _git("fetch", "--write-fetch-head", remote_alias or remote_url, remote_ref)
    return _git("rev-parse", "FETCH_HEAD").strip()


def git_remote_alias(folder: Path, remote_url: str) -> str | None:
    """Get local alias of a remote URL.

    Args:
        folder: Path to git repo.
        remote_url: Absolute URL to remote.

    Returns:
        Local alias of the remote, or None if not found.
    """
    _git = git(folder)
    # Output is like:
    #   origin  https://gitlab.com/moduon/mrchef (fetch) [blob:none]
    for remote in _git("remote", "-v").splitlines():
        alias, url, mode = remote.split()[:3]
        if url == remote_url and mode == "(fetch)":
            return alias


def git_rev(folder: Path) -> str:
    """Know the commit where a git repository is currently checked out."""
    return git(folder)("rev-parse", "--verify", "HEAD").strip()


def git_root(folder: Path) -> Path:
    """Know the root of the git repository that owns a folder."""
    return Path(git(folder)("rev-parse", "--show-toplevel").strip())
