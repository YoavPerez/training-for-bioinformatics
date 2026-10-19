"""Module 4b: two-frame monocular visual odometry on KITTI camera 0 (grayscale, rectified).

    python modules/m4b_vision/starter/mono_vo.py <drive_dir> <prep_dir> --out outputs/m4b

For each pair of consecutive frames: ORB features, ratio-test matching, essential matrix with RANSAC, relative
pose. Monocular VO has no metric scale, so each step is scaled with the ground-truth step length (the prep dir's
gt.tum). Writes vo.tum (IMU poses in the ENU world frame, comparable with gt.tum) and per-step errors.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from slampipe import kitti
from slampipe.vision import rotation_angle_deg  # noqa: F401 (needed by the TODO in main)


def match_features(img1: np.ndarray, img2: np.ndarray, n_features: int = 2000, ratio: float = 0.75):
    """ORB keypoints in both images, brute-force Hamming matching with Lowe's ratio test.
    Returns (x1, x2): (N, 2) float arrays of matched pixel coordinates."""
    # TODO(m4b): cv2.ORB_create, detectAndCompute, cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(k=2), ratio test.
    del img1, img2, n_features, ratio
    raise NotImplementedError("match_features")


def relative_pose(x1: np.ndarray, x2: np.ndarray, K: np.ndarray):
    """Essential matrix with RANSAC (prob 0.999, 1 px threshold) and cheirality check.
    Returns (R, t, inliers): T_cam2_cam1 = [R | t] with |t| = 1, and a boolean inlier mask over the matches."""
    # TODO(m4b): cv2.findEssentialMat (RANSAC) and cv2.recoverPose; return the recoverPose inlier mask.
    del x1, x2, K
    raise NotImplementedError("relative_pose")


def read_tum(path: Path) -> np.ndarray:
    """Provided: (N, 4, 4) poses from a TUM file."""
    rows = np.loadtxt(path)
    T = np.tile(np.eye(4), (len(rows), 1, 1))
    T[:, :3, :3] = Rotation.from_quat(rows[:, 4:8]).as_matrix()
    T[:, :3, 3] = rows[:, 1:4]
    return T


def write_tum(path: Path, times: np.ndarray, poses: np.ndarray) -> None:
    """Provided: writes (N, 4, 4) poses as TUM."""
    q = Rotation.from_matrix(poses[:, :3, :3]).as_quat(canonical=True)
    np.savetxt(path, np.column_stack([times, poses[:, :3, 3], q]), fmt="%.9f")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("prep_dir", type=Path, help="output of slampipe.prepare for the same drive (gt.tum)")
    parser.add_argument("--out", type=Path, default=Path("outputs/m4b"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    drive = kitti.Drive(args.drive_dir)
    cam = drive.camera(0)
    T_cam_imu = cam.T_cam_velo @ kitti.calib_to_matrix(drive.calib("imu_to_velo"))
    gt = np.loadtxt(args.prep_dir / "gt.tum")
    T_world_imu_gt = read_tum(args.prep_dir / "gt.tum")
    T_world_cam_gt = T_world_imu_gt @ np.linalg.inv(T_cam_imu)  # frame k <-> OXTS packet k
    images = [cv2.imread(str(p), cv2.IMREAD_GRAYSCALE) for p in drive.image_paths(0)]
    n = min(len(images), len(gt))

    # TODO(m4b): for each consecutive pair (k, k+1) of the first n frames:
    #   - match_features, relative_pose -> T_cam2_cam1 with |t| = 1;
    #   - the ground-truth T_cam2_cam1 from T_world_cam_gt; rotation error (rotation_angle_deg of R_estᵀ R_gt) and
    #     translation direction error (angle between t_est and t_gt) [deg];
    #   - scale t with the ground-truth step length and chain: T_world_cam[k+1] = T_world_cam[k] @ inv(T_cam2_cam1).
    # Write steps.csv (k, matches, inliers, rot_err_deg, dir_err_deg) and vo.tum (IMU poses: T_world_cam @ T_cam_imu,
    # times from gt.tum) to args.out, and print the median errors.
    del images, n, T_world_cam_gt, T_cam_imu, cam, gt
    raise NotImplementedError("mono_vo main")


if __name__ == "__main__":
    main()
