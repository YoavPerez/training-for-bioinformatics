"""Shared pytest fixtures.

Environment variables:
    SLAM_BUILD_DIR     C++ build directory (default: build)
    SLAM_DATA_DIR      data directory (default: data)
    SLAM_REQUIRE_DATA  if "1", missing data/build artifacts fail tests instead of skipping them (CI)
"""

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "pipeline" / "python"))  # import slampipe from this checkout
SAMPLE_DRIVE = "2011_09_26/2011_09_26_drive_0002_sync"


def _missing(what: str):
    if os.environ.get("SLAM_REQUIRE_DATA") == "1":
        pytest.fail(f"{what} is missing (SLAM_REQUIRE_DATA=1)")
    pytest.skip(f"{what} is missing")


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO


@pytest.fixture(scope="session")
def build_dir() -> Path:
    path = Path(os.environ.get("SLAM_BUILD_DIR", REPO / "build")).resolve()
    if not path.is_dir():
        _missing(f"build directory {path}")
    return path


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return Path(os.environ.get("SLAM_DATA_DIR", REPO / "data")).resolve()


@pytest.fixture(scope="session")
def sample_drive(data_dir) -> Path:
    path = data_dir / "samples" / "kitti" / SAMPLE_DRIVE
    if not (path / "oxts").is_dir():
        _missing("KITTI sample (python data/download.py --sample)")
    return path


@pytest.fixture(scope="session")
def sample_images(sample_drive) -> Path:
    """The sample drive, checked to contain camera 0 images (module 4b)."""
    if not any((sample_drive / "image_00" / "data").glob("*.png")):
        _missing("camera 0 images of the sample (re-run python data/download.py --sample)")
    return sample_drive


@pytest.fixture(scope="session")
def skewed_sample(data_dir) -> Path:
    path = data_dir / "samples" / "skewed"
    if not (path / "scan.npz").is_file():
        _missing("skewed sample (python data/download.py --sample)")
    return path


@pytest.fixture(scope="session")
def app(build_dir):
    """app("run_pipeline") -> path of a built C++ tool."""

    def find(name: str) -> Path:
        path = build_dir / "pipeline" / "apps" / name
        if not path.is_file():
            _missing(f"binary {path}")
        return path

    return find


@pytest.fixture(scope="session")
def prepared_sample(sample_drive, tmp_path_factory) -> Path:
    """The sample drive converted by `slampipe.prepare` (needs your module 1 geodesy)."""
    from slampipe import prepare

    out = tmp_path_factory.mktemp("prep")
    prepare.prepare(sample_drive, out)
    return out
