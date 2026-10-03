"""Module 3: effect of an IMU–LiDAR time offset on deskewing.

python modules/m3_sensors/starter/time_offset.py data/samples/skewed --build-dir build --plot offset.png
"""

import argparse
from pathlib import Path

import numpy as np
from skew_tools import load_skewed, run_deskew, write_inputs  # noqa: F401  (provided helpers)


def offset_sweep(sample_dir: Path, binary: Path, offsets: np.ndarray, work_dir: Path) -> np.ndarray:
    """RMS distance [m] between the deskewed scan and the reference scan, for each time offset [s]."""
    # TODO(m3): write the inputs once, run the deskew for each offset, compare with sample["reference"].
    del sample_dir, binary, offsets, work_dir
    raise NotImplementedError("offset_sweep")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sample_dir", type=Path)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()  # noqa: F841
    # TODO(m3): sweep offsets from -20 ms to +20 ms, plot RMS error vs offset, also report the
    # error of the uncorrected (skewed) scan for reference.


if __name__ == "__main__":
    main()
