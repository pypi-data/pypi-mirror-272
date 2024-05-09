"""Tests for nix integration."""
import os

import pytest
from plumbum import local

from mrchef import lib

from .conftest import PROJECT_ROOT


@pytest.mark.impure
@pytest.mark.xfail(
    os.environ.get("CI_PIPELINE_SOURCE") == "merge_request_event",
    reason="running in a merge request pipeline, without a GitHub ssh key",
)
def test_nix_flake_check():
    """Run `nix flake check` and hope it works."""
    local["nix"](
        "--extra-experimental-features",
        "nix-command flakes parse-toml-timestamps",
        "--no-allow-import-from-derivation",
        "flake",
        "check",
        PROJECT_ROOT,
    )


@pytest.mark.impure
def test_nix_flake_run():
    """Basic run of mrchef from flake."""
    cli_version = local["nix"](
        "--extra-experimental-features",
        "nix-command flakes parse-toml-timestamps",
        "--no-allow-import-from-derivation",
        "run",
        PROJECT_ROOT,
        "--",
        "--version",
    )
    assert cli_version.startswith("mrchef ")


@pytest.mark.impure
def test_nar_hash(tmp_path):
    """NAR hashing is consistent across runs."""
    # Init a new kitchen; NAR hashing is enabled by default
    worker = lib.Worker.init(tmp_path)
    assert worker.config_user["require_nar_hash"] is True
    # Add a meal; hash is correct
    worker.meal_add(
        tmp_path / "kitchen" / "autopretty1",
        "https://github.com/copier-org/autopretty.git",
        "main",
    )
    worker.meal_add(
        tmp_path / "kitchen" / "autopretty2",
        "https://github.com/copier-org/autopretty.git",
        "main",
        "d46b05b4cff321425e97cc4a04bd1950332a898b",
    )
    worker.warmup()
    worker.freeze()
    assert worker.config_frozen["meals"] == {
        "autopretty1": {
            "last_update": lib.now(),
            "nar_hash": "sha256-ShLqCb6WpRrvydooh5YundVx7IC1nYle1ebxoQd+aXY=",
            "rev": "f185a0467f7745e6730f01f58d9cba06224b34f8",
        },
        "autopretty2": {
            "last_update": lib.now(),
            "nar_hash": "sha256-ATlPLBDpJgNJHHdhkX0VdiQuskHOXCA2lkzdU0gXCZI=",
            "rev": "d46b05b4cff321425e97cc4a04bd1950332a898b",
        },
    }
