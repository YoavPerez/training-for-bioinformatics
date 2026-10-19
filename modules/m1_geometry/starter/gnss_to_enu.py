"""Module 1: convert a drive's GNSS fixes to local ENU and plot the trajectory.

python modules/m1_geometry/starter/gnss_to_enu.py <drive_dir> --plot enu.png
"""

import argparse
from pathlib import Path

import numpy as np

from slampipe import geodesy, kitti  # noqa: F401  (geodesy: your module 1 code)


def drive_enu(drive_dir: Path) -> np.ndarray:
    """(N, 3) ENU positions of the OXTS fixes, origin at the first OXTS packet."""
    drive = kitti.Drive(Path(drive_dir))
    # TODO(m1): use your geodesy functions.
    del drive
    raise NotImplementedError("drive_enu")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()
    enu = drive_enu(args.drive_dir)
    # TODO(m1): plot east vs north with equal axis scaling, mark the start, label axes with units.
    del enu


if __name__ == "__main__":
    main()
