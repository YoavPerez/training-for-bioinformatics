"""Smoke tests for provided (non-assignment) Python code. These pass on the starter code."""

import numpy as np

from slampipe import allan, kitti


def test_read_calib_and_matrix(tmp_path):
    f = tmp_path / "calib_imu_to_velo.txt"
    f.write_text("calib_time: 25-Sep-2011 13:20:02\nR: 1 0 0 0 1 0 0 0 1\nT: 1 2 3\n")
    m = kitti.calib_to_matrix(kitti.read_calib(f))
    assert np.allclose(m[:3, 3], [1, 2, 3])
    assert np.allclose(m[:3, :3], np.eye(3))


def test_read_timestamps(tmp_path):
    f = tmp_path / "timestamps.txt"
    f.write_text("2011-09-26 13:02:25.964389445\n2011-09-26 13:02:26.068877445\n")
    t = kitti.read_timestamps(f)
    assert np.isclose(t[1] - t[0], 0.104488, atol=1e-6)


def test_simulated_noise_shape():
    x = allan.simulate_rate_noise(1000, 100.0, 0.01, 0.001)
    assert x.shape == (1000,)
