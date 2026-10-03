"""Module 1: transform one LiDAR scan into the world (ENU) frame using the OXTS poses.

python modules/m1_geometry/starter/world_scan.py <drive_dir> --frame 40 --plot scan_world.png
"""

import argparse
from pathlib import Path

import numpy as np

from slampipe import geodesy, kitti  # noqa: F401  (geodesy: your module 1 code)


def pose_world_imu(drive: kitti.Drive, frame: int) -> np.ndarray:
    """4x4 T_world_imu at an OXTS frame; world = ENU at the first fix. Use roll/pitch/yaw from OXTS."""
    # TODO(m1): implement. Check the devkit readme for the angle definitions.
    del drive, frame
    raise NotImplementedError("pose_world_imu")


def scan_in_world(drive_dir: Path, frame: int) -> np.ndarray:
    """(N, 3) points of velodyne scan `frame` expressed in the world frame."""
    drive = kitti.Drive(Path(drive_dir))
    # TODO(m1): chain the calibration and the OXTS pose. Name every transform per CONVENTIONS.md.
    del drive, frame
    raise NotImplementedError("scan_in_world")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("--frame", type=int, default=0)
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()
    points = scan_in_world(args.drive_dir, args.frame)
    # TODO(m1): top-down scatter plot (east, north) coloured by height, together with the GNSS track.
    del points


if __name__ == "__main__":
    main()
