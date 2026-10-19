"""Module 4b stretch: metric depth from the KITTI stereo pair, checked against the LiDAR.

    python modules/m4b_vision/starter/stereo_depth.py <drive_dir> --frames 0 20 40 60 --out outputs/m4b

Cameras 0 and 1 are rectified to a common orientation, so a match lies on the same image row in both. Matches are
triangulated with the two projection matrices (your `triangulate_dlt`), which gives depth in metres, unlike
monocular VO. Each stereo depth is compared with the LiDAR depth projected to the same pixel.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from scipy.spatial import cKDTree

from slampipe import kitti
from slampipe.vision import projection_matrix, triangulate_dlt  # noqa: F401 (needed by the TODO in stereo_depth)


def stereo_matches(img0: np.ndarray, img1: np.ndarray, max_dy: float = 1.5, ratio: float = 0.75):
    """ORB matches between the left (0) and right (1) image, ratio test, then the rectified-stereo check:
    the same row (|v0 - v1| <= max_dy) and positive disparity (u0 > u1). Returns (x0, x1) as (N, 2) arrays."""
    # TODO(m4b): ORB (3000 features) + ratio test as in mono_vo, then keep only same-row matches with u0 > u1.
    del img0, img1, max_dy, ratio
    raise NotImplementedError("stereo_matches")


def stereo_depth(x0: np.ndarray, x1: np.ndarray, cam0: kitti.Camera, cam1: kitti.Camera) -> np.ndarray:
    """Depth (z in the camera 0 frame, metres) of each match, by DLT triangulation with P0 and P1."""
    # TODO(m4b): T_cam1_cam0 from the two T_cam_velo, P0 = K0 [I | 0], P1 = K1 [T_cam1_cam0], then triangulate_dlt.
    del x0, x1, cam0, cam1
    raise NotImplementedError("stereo_depth")


def lidar_depth_at(uv: np.ndarray, scan: np.ndarray, cam0: kitti.Camera, radius: float = 2.0) -> np.ndarray:
    """Provided: LiDAR depth at each pixel (median of the projected LiDAR points within `radius` px; NaN if none)."""
    p = np.column_stack([scan[:, :3], np.ones(len(scan))]) @ cam0.T_cam_velo[:3].T
    p = p[p[:, 2] > 0.5]
    h = p @ cam0.K.T
    tree = cKDTree(h[:, :2] / h[:, 2:3])
    out = np.full(len(uv), np.nan)
    for i, idx in enumerate(tree.query_ball_point(uv, radius)):
        if idx:
            out[i] = np.median(p[idx, 2])
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("--frames", type=int, nargs="+", default=[0, 20, 40, 60])
    parser.add_argument("--out", type=Path, default=Path("outputs/m4b"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    drive = kitti.Drive(args.drive_dir)
    cam0, cam1 = drive.camera(0), drive.camera(1)
    rows = []
    for k in args.frames:
        img0, img1 = (cv2.imread(str(drive.image_paths(c)[k]), cv2.IMREAD_GRAYSCALE) for c in (0, 1))
        x0, x1 = stereo_matches(img0, img1)
        z = stereo_depth(x0, x1, cam0, cam1)
        z_lidar = lidar_depth_at(x0, drive.scan(k), cam0)
        ok = np.isfinite(z_lidar)
        rows.append(np.column_stack([np.full(ok.sum(), k), z[ok], z_lidar[ok]]))
        rel = np.abs(z[ok] - z_lidar[ok]) / z_lidar[ok]
        print(
            f"frame {k}: {len(x0)} stereo matches, {ok.sum()} with LiDAR depth, "
            f"median |dz| {np.median(np.abs(z[ok] - z_lidar[ok])):.2f} m, median relative error {np.median(rel):.1%}"
        )
    np.savetxt(
        args.out / "stereo_vs_lidar.csv",
        np.vstack(rows),
        delimiter=",",
        header="frame,z_stereo,z_lidar",
        comments="",
        fmt=["%d", "%.3f", "%.3f"],
    )


if __name__ == "__main__":
    main()
