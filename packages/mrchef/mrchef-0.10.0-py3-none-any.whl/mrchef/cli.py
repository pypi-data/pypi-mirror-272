"""Tools for command-line usage."""
import os
from importlib.metadata import PackageNotFoundError, version
from logging import INFO
from pathlib import Path

import rtoml
from decorator import decorator
from plumbum import cli

from . import lib

AUTOCOMMIT = cli.Flag(
    ["a", "autocommit"],
    help="Commit changes automatically after updating successfully",
)


def _get_version():
    """Get version from metadata or from local development environment."""
    try:
        return version("mrchef")
    except PackageNotFoundError:
        # You're developing locally using direnv
        return rtoml.load(Path(__file__).parent.parent.joinpath("pyproject.toml"))[
            "project"
        ]["version"]


@decorator
def handle_error(function, *args, **kwargs):
    """Do not print error traces for expected errors."""
    try:
        return function(*args, **kwargs)
    except lib.MrChefError as error:
        lib.logger.log(error.trace_level, "Error trace", exc_info=True)
        lib.logger.critical(error.msg)
        if os.environ.get("MRCHEF_ERROR_SLURP", "1") == "1":
            return 1
        raise


class MrChef(cli.Application):
    """Meta-repo Chef 👨‍🍳.

    Culinary helper to cook in metarepo source code kitchens.

    Note: in case you didn't notice, all that cooking stuff is just a metaphore:

    - "Meals" are remote repositories of source code.
    - "Cooking" is developing.
    - The "kitchen" is where all "meals" will be "cooked".
    - "Warming" means setting up those "meals" to be "cooked".
    - "Freezing" means locking the code that was "cooked", for reproducibility.
    - "Spices" are extra patches for the source code.
    - I am just another secondary "Chef" in the "kitchen". You are the master chef!
      I will just "freeze" or "warm up" meals for you, but you will "cook" them.

    Yay, I'm hungry now! 🥘
    """

    PROGNAME = "mrchef"  # Just in case it's being called as a module
    VERSION = _get_version()

    starting_folder = cli.SwitchAttr(
        ["s", "starting-folder"],
        cli.ExistingDirectory,
        ".",
        help=f"Search for {lib.CONFIG_FILE} from this directory upwards",
    )
    log_level = cli.SwitchAttr(
        ["-l", "--log-level"],
        int,
        INFO,
        envname="MRCHEF_LOG_LEVEL",
        help="Set numeric log level (see https://docs.python.org/3/library/logging.html#logging-levels)",
    )

    def worker(self) -> lib.Worker:
        """Get a worker in the proper path."""
        # Set log level
        lib.logger.setLevel(self.log_level)
        lib.warnings_logger.setLevel(self.log_level)
        lib.logger.debug("Log level set to %d", self.log_level)
        # Return desired worker
        return lib.Worker(Path(self.starting_folder))


@MrChef.subcommand("check")
class MrChefCheck(cli.Application):  # noqa: D415
    """Check if hot meals are the same as the ones in the freezer"""

    @handle_error
    def main(self):
        self.parent.worker().check()


@MrChef.subcommand("freeze")
class MrChefFreeze(cli.Application):  # noqa: D415
    """Put hot meals in the freezer"""

    @handle_error
    def main(self):
        self.parent.worker().freeze()


@MrChef.subcommand("init")
class MrChefInit(cli.Application):  # noqa: D415
    """Set up a new kitchen"""

    @handle_error
    def main(self):
        lib.Worker.init(Path(self.parent.starting_folder))


@MrChef.subcommand("meal-add")
class MrChefMealAdd(cli.Application):  # noqa: D415
    """Start cooking a new meal"""

    @handle_error
    def main(
        self, meal_path: cli.NonexistentPath, url: str, branch: str, rev: str = ""
    ):
        self.parent.worker().meal_add(Path(meal_path), url, branch, rev or None)


@MrChef.subcommand("meal-ls")
class MrChefMealLs(cli.Application):  # noqa: D415
    """List meals"""

    print0 = cli.Flag(["0", "print0"], help="Separate items with null character")

    @handle_error
    def main(self):
        worker = self.parent.worker()
        for meal in worker.all_meals():
            print(worker.kitchen / meal, end="\0" if self.print0 else os.linesep)


@MrChef.subcommand("meal-rm")
class MrChefMealRm(cli.Application):  # noqa: D415
    """Remove a meal from the kitchen"""

    @handle_error
    def main(self, meal_path: cli.ExistingDirectory):
        self.parent.worker().meal_rm(Path(meal_path))


@MrChef.subcommand("spice-add")
class MrChefSpiceAdd(cli.Application):  # noqa: D415
    """Add a new spice to a meal"""

    @handle_error
    def main(self, meal_path: cli.ExistingDirectory, url: str):
        self.parent.worker().spice_add(Path(meal_path), url)


@MrChef.subcommand("spice-export")
class MrChefSpiceExport(cli.Application):  # noqa: D415
    """Export spice contents from the freezer"""

    @handle_error
    def main(self, url: str):
        print(self.parent.worker().spice_export(url))


@MrChef.subcommand("spice-rm")
class MrChefSpiceRm(cli.Application):  # noqa: D415
    """Remove a spice from a meal"""

    @handle_error
    def main(self, meal_path: cli.ExistingDirectory, url: str):
        self.parent.worker().spice_rm(Path(meal_path), url)


@MrChef.subcommand("update")
class MrChefUpdate(cli.Application):  # noqa: D415
    """Update meal(s), ignoring what's in the freezer"""

    autocommit = AUTOCOMMIT
    force = cli.Flag(
        ["f", "force"], help="Override dirty changes (they will be stashed)"
    )
    oldest = cli.SwitchAttr(
        ["o", "oldest"],
        int,
        0,
        help="Update only the N oldest meals (0 means all)",
    )

    @handle_error
    def main(self, *meal_paths: cli.ExistingDirectory):
        self.parent.worker().update(
            *map(Path, meal_paths),
            autocommit=self.autocommit,
            force=self.force,
            oldest=self.oldest,
        )


@MrChef.subcommand("warmup")
class MrChefWarm(cli.Application):  # noqa: D415
    """Warm up meals from the freezer into the kitchen"""

    force = cli.Flag(
        ["f", "force"], help="Override dirty changes (they will be stashed)"
    )

    @handle_error
    def main(self, *meal_paths: Path):
        self.parent.worker().warmup(*meal_paths, force=self.force)
