"""Module 4b: two-view bundle adjustment with scipy.optimize.least_squares.

    python modules/m4b_vision/starter/two_view_ba.py <drive_dir> <prep_dir> --frame 30

Initializes from mono_vo (essential matrix + DLT triangulation of the inliers), then jointly refines the second
camera's pose and the 3-D points by minimizing the reprojection error in both images (robust loss). Camera 1 is
fixed at the origin and |t| = 1 fixes the scale (the gauge). Prints the reprojection RMS and the pose errors
against ground truth before and after.
"""

import argparse
from pathlib import Path

import cv2
import numpy as np
from mono_vo import match_features, read_tum, relative_pose
from scipy.optimize import least_squares  # noqa: F401 (needed by the TODO in refine)
from scipy.spatial.transform import Rotation

from slampipe import kitti
from slampipe.vision import projection_matrix, reprojection_errors, rotation_angle_deg, triangulate_dlt


def unpack(params: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Provided: params = [rotation vector (3), translation (3), points (3N)] -> (R, t with |t| = 1, X (N, 3))."""
    R = Rotation.from_rotvec(params[:3]).as_matrix()
    t = params[3:6] / np.linalg.norm(params[3:6])
    return R, t, params[6:].reshape(-1, 3)


def ba_residuals(params: np.ndarray, K: np.ndarray, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    """Reprojection residuals (4N,) of all points in both images: camera 1 at the origin, camera 2 at
    T_cam2_cam1 = [R | t] from `unpack`. Order: all x/y residuals of image 1, then those of image 2."""
    # TODO(m4b): project X with P1 = K [I | 0] and P2 = K [R | t]; return the stacked pixel differences.
    del params, K, x1, x2
    raise NotImplementedError("ba_residuals")


def refine(K, x1, x2, R0, t0, X0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bundle adjustment from an initial guess; returns refined (R, t, X)."""
    # TODO(m4b): pack the initial guess, call least_squares on ba_residuals with a robust loss, unpack the result.
    del K, x1, x2, R0, t0, X0
    raise NotImplementedError("refine")


def rms(K, R, t, X, x1, x2) -> float:
    """Provided: reprojection RMS over both images [px]."""
    T2 = np.eye(4)
    T2[:3, :3], T2[:3, 3] = R, t
    e = np.concatenate(
        [
            reprojection_errors(projection_matrix(K, np.eye(4)), X, x1),
            reprojection_errors(projection_matrix(K, T2), X, x2),
        ]
    )
    return float(np.sqrt(np.mean(e**2)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("prep_dir", type=Path)
    parser.add_argument("--frame", type=int, default=30, help="refines the pair (frame, frame + 1)")
    args = parser.parse_args()

    drive = kitti.Drive(args.drive_dir)
    cam = drive.camera(0)
    T_cam_imu = cam.T_cam_velo @ kitti.calib_to_matrix(drive.calib("imu_to_velo"))
    T_world_cam = read_tum(args.prep_dir / "gt.tum") @ np.linalg.inv(T_cam_imu)
    T_gt = np.linalg.inv(T_world_cam[args.frame + 1]) @ T_world_cam[args.frame]
    paths = drive.image_paths(0)
    img1, img2 = (cv2.imread(str(paths[i]), cv2.IMREAD_GRAYSCALE) for i in (args.frame, args.frame + 1))

    x1, x2 = match_features(img1, img2)
    R0, t0, inliers = relative_pose(x1, x2, cam.K)
    x1, x2 = x1[inliers], x2[inliers]
    P2 = projection_matrix(cam.K, np.vstack([np.column_stack([R0, t0]), [0, 0, 0, 1]]))
    X0 = triangulate_dlt(projection_matrix(cam.K, np.eye(4)), P2, x1, x2)
    R, t, X = refine(cam.K, x1, x2, R0, t0, X0)

    def pose_errors(Re, te):
        rot = rotation_angle_deg(Re.T @ T_gt[:3, :3])
        cosang = te @ T_gt[:3, 3] / np.linalg.norm(te) / np.linalg.norm(T_gt[:3, 3])
        return rot, float(np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0))))

    for name, (Re, te, Xe) in {"initial": (R0, t0, X0), "refined": (R, t, X)}.items():
        rot, ang = pose_errors(Re, te)
        print(
            f"{name:8s} {len(x1)} points: reprojection RMS {rms(cam.K, Re, te, Xe, x1, x2):.3f} px, "
            f"rotation error {rot:.4f} deg, translation direction error {ang:.3f} deg"
        )


if __name__ == "__main__":
    main()
