"""Module 4b acceptance tests: two-view geometry, bundle adjustment, LiDAR projection and visual odometry."""

import importlib.util
import subprocess
import sys

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from slampipe import kitti, vision

K = np.array([[721.5377, 0.0, 609.5593], [0.0, 721.5377, 172.854], [0.0, 0.0, 1.0]])


def _load(repo_root, name):
    starter = repo_root / "modules/m4b_vision/starter"
    sys.path.insert(0, str(starter))  # two_view_ba imports mono_vo from the same folder
    spec = importlib.util.spec_from_file_location(name, starter / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _scene(n=60, seed=0):
    """Points 5-30 m in front of camera 1; camera 2 moved ~1 m forward with a small rotation (T_cam2_cam1)."""
    rng = np.random.default_rng(seed)
    X = np.column_stack([rng.uniform(-8, 8, n), rng.uniform(-3, 2, n), rng.uniform(5, 30, n)])
    T21 = np.eye(4)
    T21[:3, :3] = Rotation.from_euler("xyz", [0.01, -0.03, 0.005]).as_matrix()
    T21[:3, 3] = [0.1, -0.02, -1.0]
    P1, P2 = vision.projection_matrix(K, np.eye(4)), vision.projection_matrix(K, T21)

    def proj(P):
        h = np.column_stack([X, np.ones(n)]) @ P.T
        return h[:, :2] / h[:, 2:3]

    return X, T21, P1, P2, proj(P1), proj(P2)


def _skew(v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])


def _hom(x):
    return np.column_stack([x, np.ones(len(x))])


def test_normalize_points():
    x = np.random.default_rng(1).uniform([0, 0], [1242, 375], (40, 2))
    xn, T = vision.normalize_points(x)
    assert np.allclose(xn.mean(axis=0), 0.0, atol=1e-9)
    assert np.isclose(np.linalg.norm(xn, axis=1).mean(), np.sqrt(2.0))
    assert np.allclose((_hom(x) @ T.T)[:, :2], xn)


def test_eight_point_noise_free():
    _, T21, _, _, x1, x2 = _scene()
    F = vision.eight_point(x1, x2)
    assert np.isclose(np.linalg.norm(F), 1.0)
    assert np.linalg.svd(F, compute_uv=False)[2] < 1e-10, "F must have rank 2"
    residual = np.abs(np.sum(_hom(x2) * (_hom(x1) @ F.T), axis=1))
    assert residual.max() < 1e-8
    Kinv = np.linalg.inv(K)
    F_true = Kinv.T @ _skew(T21[:3, 3]) @ T21[:3, :3] @ Kinv
    F_true /= np.linalg.norm(F_true)
    assert min(np.abs(F - F_true).max(), np.abs(F + F_true).max()) < 1e-6


def test_eight_point_with_pixel_noise_is_well_conditioned():
    _, _, _, _, x1, x2 = _scene(n=200, seed=2)
    rng = np.random.default_rng(3)
    x1n, x2n = x1 + rng.normal(0, 0.5, x1.shape), x2 + rng.normal(0, 0.5, x2.shape)
    F = vision.eight_point(x1n, x2n)
    lines = _hom(x1) @ F.T  # epipolar lines in image 2 of the noise-free points
    dist = np.abs(np.sum(_hom(x2) * lines, axis=1)) / np.linalg.norm(lines[:, :2], axis=1)
    assert np.median(dist) < 1.0, f"median epipolar distance {np.median(dist):.2f} px: did you normalize?"


def test_eight_point_rejects_bad_input():
    x = np.zeros((7, 2))
    with pytest.raises(ValueError):
        vision.eight_point(x, x)
    with pytest.raises(ValueError):
        vision.eight_point(np.zeros((9, 2)), np.zeros((8, 2)))


def test_essential_from_fundamental():
    _, T21, _, _, x1, x2 = _scene()
    E = vision.essential_from_fundamental(vision.eight_point(x1, x2), K, K)
    assert np.allclose(np.linalg.svd(E, compute_uv=False), [1.0, 1.0, 0.0], atol=1e-9)
    E_true = _skew(T21[:3, 3]) @ T21[:3, :3]
    E_true *= np.sqrt(2.0) / np.linalg.norm(E_true)
    assert min(np.abs(E - E_true).max(), np.abs(E + E_true).max()) < 1e-6


def test_triangulate_and_reprojection_errors():
    X, _, P1, P2, x1, x2 = _scene()
    Xt = vision.triangulate_dlt(P1, P2, x1, x2)
    assert Xt.shape == X.shape
    assert np.abs(Xt - X).max() < 1e-6
    assert np.abs(vision.reprojection_errors(P1, X, x1)).max() < 1e-9
    e = vision.reprojection_errors(P2, X, x2 + np.array([3.0, 4.0]))
    assert np.allclose(e, 5.0)


def test_bundle_adjustment_on_synthetic_pair(repo_root):
    ba = _load(repo_root, "two_view_ba")
    X, T21, _, _, x1, x2 = _scene(n=80, seed=4)
    t_unit = T21[:3, 3] / np.linalg.norm(T21[:3, 3])
    X_unit = X / np.linalg.norm(T21[:3, 3])  # |t| = 1 gauge
    params = np.concatenate([Rotation.from_matrix(T21[:3, :3]).as_rotvec(), t_unit, X_unit.ravel()])
    r = ba.ba_residuals(params, K, x1, x2)
    assert r.shape == (4 * len(X),)
    assert np.abs(r).max() < 1e-8

    rng = np.random.default_rng(5)
    x1n, x2n = x1 + rng.normal(0, 0.5, x1.shape), x2 + rng.normal(0, 0.5, x2.shape)
    R0 = Rotation.from_rotvec(Rotation.from_matrix(T21[:3, :3]).as_rotvec() + 0.01).as_matrix()
    X0 = X_unit * rng.uniform(0.9, 1.1, (len(X), 1))
    before = ba.rms(K, R0, t_unit + 0.05, X0, x1n, x2n)
    R, t, Xr = ba.refine(K, x1n, x2n, R0, t_unit + 0.05, X0)
    after = ba.rms(K, R, t, Xr, x1n, x2n)
    assert after < 0.6 < before, f"reprojection RMS {before:.2f} -> {after:.2f} px (noise 0.5 px)"
    assert vision.rotation_angle_deg(R.T @ T21[:3, :3]) < 0.1


def test_lidar_projection_on_sample(app, sample_drive, tmp_path):
    out = tmp_path / "proj.csv"
    subprocess.run([str(app("project_lidar")), str(sample_drive), "0", str(out)], check=True)
    uvd = np.loadtxt(out, delimiter=",", skiprows=1)
    cam = kitti.Drive(sample_drive).camera(0)
    w, h = cam.size
    assert 10_000 < len(uvd) < 40_000, f"{len(uvd)} points in the image"
    assert (uvd[:, 0] >= -0.5).all() and (uvd[:, 0] < w - 0.5).all()
    assert (uvd[:, 1] >= -0.5).all() and (uvd[:, 1] < h - 0.5).all()
    assert (uvd[:, 2] >= 0.1).all()
    # Same projection in numpy for the reported indices.
    pts = kitti.Drive(sample_drive).scan(0)[uvd[:, 3].astype(int), :3].astype(float)
    p_cam = _hom(pts) @ cam.T_cam_velo[:3].T
    uv = p_cam @ cam.K.T
    assert np.abs(uv[:, :2] / uv[:, 2:3] - uvd[:, :2]).max() < 1e-2
    assert np.abs(p_cam[:, 2] - uvd[:, 2]).max() < 1e-3


def test_overlay_writes_a_figure(repo_root, tmp_path):
    lidar_on_image = _load(repo_root, "lidar_on_image")
    image = np.zeros((375, 1242))
    uvd = np.array([[10.0, 20.0, 5.0, 0], [600.0, 170.0, 60.0, 1]])
    out = tmp_path / "overlay.png"
    lidar_on_image.overlay(image, uvd, out)
    assert out.is_file() and out.stat().st_size > 1000


def test_two_frame_vo_on_sample(repo_root, sample_images, prepared_sample):
    import cv2

    vo = _load(repo_root, "mono_vo")
    drive = kitti.Drive(sample_images)
    cam = drive.camera(0)
    T_cam_imu = cam.T_cam_velo @ kitti.calib_to_matrix(drive.calib("imu_to_velo"))
    T_world_cam = vo.read_tum(prepared_sample / "gt.tum") @ np.linalg.inv(T_cam_imu)
    paths = drive.image_paths(0)
    rot, ang = [], []
    for k in range(0, len(paths) - 1, 4):
        img1, img2 = (cv2.imread(str(paths[i]), cv2.IMREAD_GRAYSCALE) for i in (k, k + 1))
        x1, x2 = vo.match_features(img1, img2)
        assert len(x1) >= 300, f"only {len(x1)} matches for frames {k}, {k + 1}"
        R, t, inliers = vo.relative_pose(x1, x2, cam.K)
        assert inliers.dtype == bool and inliers.shape == (len(x1),)
        assert np.isclose(np.linalg.norm(t), 1.0)
        T_gt = np.linalg.inv(T_world_cam[k + 1]) @ T_world_cam[k]
        rot.append(vision.rotation_angle_deg(R.T @ T_gt[:3, :3]))
        cosang = t @ T_gt[:3, 3] / np.linalg.norm(T_gt[:3, 3])
        ang.append(np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0))))
    assert np.median(rot) < 0.3, f"median rotation error {np.median(rot):.3f} deg"
    assert np.median(ang) < 6.0, f"median translation direction error {np.median(ang):.2f} deg"


def test_stereo_depth_matches_lidar_on_sample(repo_root, sample_images):
    import cv2

    stereo = _load(repo_root, "stereo_depth")
    drive = kitti.Drive(sample_images)
    cam0, cam1 = drive.camera(0), drive.camera(1)
    rel = []
    for k in (0, 20, 40, 60):
        img0, img1 = (cv2.imread(str(drive.image_paths(c)[k]), cv2.IMREAD_GRAYSCALE) for c in (0, 1))
        x0, x1 = stereo.stereo_matches(img0, img1)
        assert len(x0) >= 300, f"only {len(x0)} stereo matches in frame {k}"
        assert np.abs(x0[:, 1] - x1[:, 1]).max() <= 1.5 and (x0[:, 0] > x1[:, 0]).all(), "rectified-stereo check"
        z = stereo.stereo_depth(x0, x1, cam0, cam1)
        assert z.shape == (len(x0),)
        z_lidar = stereo.lidar_depth_at(x0, drive.scan(k), cam0)
        ok = np.isfinite(z_lidar)
        assert ok.sum() >= 150, f"only {ok.sum()} stereo points with LiDAR depth in frame {k}"
        rel.extend(np.abs(z[ok] - z_lidar[ok]) / z_lidar[ok])
    assert np.median(rel) < 0.05, f"median relative depth error {np.median(rel):.1%} against the LiDAR"
