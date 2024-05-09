"""Builder for nix's mrchef.combinedSource derivation."""

import json
import os
import sys
from pathlib import Path
from shutil import rmtree

from plumbum import local
from plumbum.cmd import git

from mrchef.lib import Worker


def json_load(env_var: str):
    """Load json from file pointed by environment variable."""
    with open(os.environ[env_var]) as fd:
        return json.load(fd)


# Helpers
PURE_MEALS = json_load("pureMealsJSON")
UNCOMPRESSED_SRC = Path(os.environ["unpackedSrcDir"])

# Disable git garbage collection
# DOC http://git-scm.com/docs/git-config#Documentation/git-config.txt---global
local.env["XDG_CONFIG_HOME"] = Path().absolute()
Path("git").mkdir()
git("config", "--file=git/config", "gc.auto", "0")

# Get destination worker
worker = Worker(UNCOMPRESSED_SRC)

# Know which meals to warmup
try:
    MEALS_TO_WARMUP = json.loads(os.environ["mealsToWarmup"])
    if not MEALS_TO_WARMUP:
        raise KeyError
    WARMUP_ALL_MEALS = False
except KeyError:
    MEALS_TO_WARMUP = worker.cold_meals().keys()
    WARMUP_ALL_MEALS = True

# Generate fake git repos for build time
Path("build-kitchen").mkdir()
for key, value in worker.cold_meals().items():
    if key not in MEALS_TO_WARMUP:
        print(f"not mocking {key}: skipping")
        continue
    fake_repo = Path("build-kitchen", key)
    fake_repo.mkdir(parents=True)
    src = Path(PURE_MEALS[key])
    # Create a fake git repo that tracks source
    _git = git["--git-dir", fake_repo, "--work-tree", src]
    _git("init")
    _git("checkout", "-b", value.branch)
    _git("add", "-A")
    # Add possibly ignored but added files
    for line in _git("status", "--ignored", "--porcelain").strip().splitlines():
        status, name = line.split(maxsplit=1)
        if status == "??":
            _git("add", "--force", name)
    _git("commit", "-m", "init files")
    # Patch destination user configuration
    mocked_url = str(fake_repo.absolute())
    mocked_rev = _git("rev-parse", "HEAD").strip()
    print(
        f"mocking {key}: original_url={value.url} mocked_url={mocked_url} "
        f"original_rev={value.rev} mocked_rev={mocked_rev}",
        file=sys.stderr,
    )
    worker.config_user["meals"][key].update({"url": mocked_url, "rev": mocked_rev})

print("warming up kitchen", file=sys.stderr)
worker.warmup(*map(worker.kitchen.joinpath, MEALS_TO_WARMUP))

if WARMUP_ALL_MEALS:
    print("checking kitchen", file=sys.stderr)
    worker.check()
else:
    # TODO Implement check by meal and use it here
    print("not checking kitchen because some meals were not warmed up")

# Remove .git subfolders, to keep outputHash reproducible
print("cleaning up kitchen", file=sys.stderr)
for meal in MEALS_TO_WARMUP:
    rmtree(worker.kitchen / meal / ".git")
