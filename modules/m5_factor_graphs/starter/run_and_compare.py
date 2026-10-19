"""Module 5: run the pipeline and compare it with the module 2 ESKF.

    python modules/m5_factor_graphs/starter/run_and_compare.py <drive_dir> <prep_dir> --build-dir build --out outputs/m5

Runs run_pipeline (odometry only, + GNSS, + GNSS + IMU) and eskf_run on the same prepared drive,
evaluates all of them against gt.tum and writes a comparison table and plot.
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np  # noqa: F401


def run_pipeline(build_dir: Path, drive_dir: Path, prep_dir: Path, out_dir: Path, *options: str) -> Path:
    """Provided: runs the C++ pipeline and returns the directory with odometry.tum and optimized.tum."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [str(build_dir / "pipeline/apps/run_pipeline"), str(drive_dir), str(prep_dir), str(out_dir), *options]
    subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    return out_dir


def eskf_as_tum(eskf_csv: Path, out_tum: Path) -> Path:
    """Converts eskf_run output (positions only) to TUM with identity orientation, for evo."""
    # TODO(m5): implement (evo's ATE translation part only needs positions).
    del eskf_csv, out_tum
    raise NotImplementedError("eskf_as_tum")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("prep_dir", type=Path)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("outputs/m5"))
    args = parser.parse_args()  # noqa: F841
    # TODO(m5): run the variants, evaluate each with slampipe.evaluation.evaluate_ate (RPE comes in module 6),
    # and write a table (ATE RMSE, median, p95, CI) plus an overlay plot of the trajectories.


if __name__ == "__main__":
    main()
