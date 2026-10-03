"""Module 2: GNSS outage experiment with the 3-D ESKF.

    python -m slampipe.prepare <drive_dir> outputs/prep
    python modules/m2_estimation/starter/outage_experiment.py outputs/prep --build-dir build \
        --outage 60 100 --plot outage.png

Runs `eskf_run` twice (with and without an outage), compares both to gt.tum and plots the
position error together with the filter's 3-sigma bound.
"""

import argparse
import subprocess
from pathlib import Path

import numpy as np


def run_eskf(build_dir: Path, prep_dir: Path, out_csv: Path, outage: tuple[float, float] | None = None) -> np.ndarray:
    """Provided: runs the C++ filter and returns its CSV as an array (t, x, y, z, sx, sy, sz)."""
    cmd = [str(build_dir / "pipeline" / "apps" / "eskf_run"), str(prep_dir), str(out_csv)]
    if outage:
        cmd += ["--outage", str(outage[0]), str(outage[1])]
    subprocess.run(cmd, check=True)
    return np.loadtxt(out_csv, delimiter=",", skiprows=1)


def position_errors(estimate: np.ndarray, gt_tum: Path) -> np.ndarray:
    """(N, 3) position error of `estimate` rows against ground truth interpolated at their times."""
    # TODO(m2): load gt.tum, interpolate ground-truth positions at the estimate times, subtract.
    del estimate, gt_tum
    raise NotImplementedError("position_errors")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prep_dir", type=Path)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--outage", type=float, nargs=2, required=True)
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()  # noqa: F841
    # TODO(m2): run with and without the outage, plot horizontal error and its 3-sigma bound vs time,
    # shade the outage window, and print the error growth over the outage.


if __name__ == "__main__":
    main()
