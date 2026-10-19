"""Module 4b: overlay a LiDAR scan on the camera image it was taken with.

    python modules/m4b_vision/starter/lidar_on_image.py <drive_dir> --frame 0 --build-dir build --out outputs/m4b

Runs the provided `project_lidar` tool (your C++ camera model) and draws the projected points on camera 0's
rectified image, coloured by depth. A correct extrinsic puts depth edges on object edges (poles, cars, kerbs).
"""

import argparse
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from slampipe import kitti  # noqa: E402


def project(build_dir: Path, drive: Path, frame: int, out_csv: Path) -> np.ndarray:
    """Provided: runs project_lidar and returns an (N, 4) array u, v, depth, index."""
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    tool = build_dir / "pipeline/apps/project_lidar"
    subprocess.run([str(tool), str(drive), str(frame), str(out_csv)], check=True)
    return np.loadtxt(out_csv, delimiter=",", skiprows=1, ndmin=2)


def overlay(image: np.ndarray, uvd: np.ndarray, out_png: Path, max_depth: float = 40.0) -> None:
    """Draws the image in grey and the points (u, v) on top, coloured by depth (clipped at max_depth), with a
    colour bar in metres; saves to out_png."""
    # TODO(m4b): image in grey, scatter of (u, v) coloured by min(depth, max_depth), colour bar in metres,
    # axes limited to the image; save to out_png.
    del image, uvd, out_png, max_depth
    raise NotImplementedError("overlay")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("--frame", type=int, default=0)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("outputs/m4b"))
    args = parser.parse_args()

    uvd = project(args.build_dir, args.drive_dir, args.frame, args.out / f"projected_{args.frame:04d}.csv")
    image = plt.imread(kitti.Drive(args.drive_dir).image_paths(0)[args.frame])
    out_png = args.out / f"lidar_on_image_{args.frame:04d}.png"
    overlay(image, uvd, out_png)
    print(f"{len(uvd)} points, depth {uvd[:, 2].min():.1f}-{uvd[:, 2].max():.1f} m -> {out_png}")


if __name__ == "__main__":
    main()
