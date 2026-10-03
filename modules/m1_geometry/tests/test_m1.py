"""Module 1 acceptance tests (Python side): geodesy and the world-frame scan."""

import importlib.util

import numpy as np
import pytest

from slampipe import geodesy

A = 6378137.0
B = 6356752.314245  # WGS84 semi-minor axis


def load(repo_root, name):
    spec = importlib.util.spec_from_file_location(name, repo_root / f"modules/m1_geometry/starter/{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "lat, lon, h, expected",
    [
        (0.0, 0.0, 0.0, (A, 0.0, 0.0)),
        (0.0, 90.0, 0.0, (0.0, A, 0.0)),
        (0.0, 180.0, 100.0, (-(A + 100.0), 0.0, 0.0)),
        (90.0, 0.0, 0.0, (0.0, 0.0, B)),
        (-90.0, 0.0, 10.0, (0.0, 0.0, -(B + 10.0))),
        # Reference values computed with PROJ (EPSG:4979 -> EPSG:4978):
        (49.0, 8.4, 100.0, (4147524.794, 612453.177, 4790634.218)),
        (32.8, 35.0, 0.0, (4395998.025, 3078110.955, 3435335.432)),
    ],
)
def test_wgs84_to_ecef_reference_points(lat, lon, h, expected):
    np.testing.assert_allclose(geodesy.wgs84_to_ecef(lat, lon, h), expected, atol=1e-3)


def test_wgs84_to_ecef_vectorized():
    out = geodesy.wgs84_to_ecef(np.array([0.0, 90.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]))
    assert out.shape == (2, 3)


def test_enu_origin_is_zero():
    np.testing.assert_allclose(geodesy.wgs84_to_enu(49.0, 8.4, 100.0, 49.0, 8.4, 100.0), 0.0, atol=1e-6)


def test_enu_axes():
    lat0, lon0, h0 = 49.0, 8.4, 100.0
    north = geodesy.wgs84_to_enu(lat0 + 1e-4, lon0, h0, lat0, lon0, h0)
    east = geodesy.wgs84_to_enu(lat0, lon0 + 1e-4, h0, lat0, lon0, h0)
    up = geodesy.wgs84_to_enu(lat0, lon0, h0 + 10.0, lat0, lon0, h0)
    assert north[1] == pytest.approx(11.12, abs=0.05) and abs(north[0]) < 1e-3
    assert east[0] == pytest.approx(7.32, abs=0.05) and abs(east[1]) < 1e-3
    np.testing.assert_allclose(up, [0.0, 0.0, 10.0], atol=1e-6)


def test_ecef_to_enu_preserves_distances():
    rng = np.random.default_rng(0)
    lat0, lon0, h0 = 32.8, 35.0, 0.0
    origin = geodesy.wgs84_to_ecef(lat0, lon0, h0)
    pts = origin + rng.normal(0, 500.0, (20, 3))
    enu = geodesy.ecef_to_enu(pts, lat0, lon0, h0)
    np.testing.assert_allclose(np.linalg.norm(enu, axis=1), np.linalg.norm(pts - origin, axis=1), rtol=1e-12)


def test_drive_enu_track(sample_drive, repo_root):
    enu = load(repo_root, "gnss_to_enu").drive_enu(sample_drive)
    assert enu.shape == (77, 3)
    np.testing.assert_allclose(enu[0], 0.0, atol=1e-6)
    path = np.sum(np.linalg.norm(np.diff(enu[:, :2], axis=0), axis=1))
    assert path == pytest.approx(81.0, rel=0.05)


def test_scan_in_world_is_around_the_vehicle(sample_drive, repo_root):
    world_scan = load(repo_root, "world_scan")
    enu = load(repo_root, "gnss_to_enu").drive_enu(sample_drive)
    pts = world_scan.scan_in_world(sample_drive, 40)
    near = pts[np.linalg.norm(pts[:, :2] - enu[40, :2], axis=1) < 15.0]
    assert len(near) > 0.3 * len(pts), "most points should lie within 15 m of the vehicle position"
    ground = near[:, 2]
    # KITTI setup: the OXTS unit is mounted ~0.93 m above the road (the velodyne ~1.73 m).
    assert np.percentile(ground, 10) == pytest.approx(enu[40, 2] - 0.93, abs=0.4), "ground ~0.9 m below the IMU"
