"""Module 0: replay one KITTI drive and summarize it.

    python modules/m0_conventions/starter/replay.py data/samples/kitti/2011_09_26/2011_09_26_drive_0002_sync

Uses the provided reader in pipeline/python/slampipe/kitti.py.
"""

import argparse
from pathlib import Path

from slampipe import kitti


def summarize(drive_dir: Path) -> dict[str, float]:
    """Returns {"n_scans": int, "duration_s": float, "distance_m": float}.

    duration_s: from the first to the last velodyne timestamp.
    distance_m: distance travelled, from the OXTS forward velocity and OXTS timestamps.
    """
    drive = kitti.Drive(Path(drive_dir))
    # TODO(m0): implement.
    del drive
    raise NotImplementedError("summarize")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("--plot", type=Path, help="save a speed-over-time plot here")
    args = parser.parse_args()
    print(summarize(args.drive_dir))
    # TODO(m0): if --plot is given, plot OXTS forward speed over time and save it.


if __name__ == "__main__":
    main()
