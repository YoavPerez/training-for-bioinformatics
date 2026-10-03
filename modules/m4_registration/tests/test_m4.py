"""Module 4 acceptance tests (Python side): ICP on real KITTI scan pairs and the benchmark harness."""

import importlib.util

import numpy as np
import pytest


def load(repo_root):
    spec = importlib.util.spec_from_file_location(
        "benchmark", repo_root / "modules/m4_registration/starter/benchmark.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _scan(sample_drive, k):
    return sample_drive / "velodyne_points" / "data" / f"{k:010d}.bin"


def test_gt_relative_is_about_one_metre_forward(prepared_sample, repo_root):
    T = load(repo_root).gt_relative(prepared_sample, 10, 11)
    assert T.shape == (4, 4)
    assert T[0, 3] == pytest.approx(0.95, abs=0.15), "the car drives ~1 m per frame along the lidar x axis"
    assert abs(T[1, 3]) < 0.1


@pytest.mark.parametrize("k", [5, 30, 60])
def test_icp_matches_ground_truth_on_real_pairs(app, sample_drive, prepared_sample, repo_root, k):
    bench = load(repo_root)
    T_true = bench.gt_relative(prepared_sample, k, k + 1)
    est = bench.register_ours(app("icp_register"), _scan(sample_drive, k + 1), _scan(sample_drive, k), np.eye(4))
    t_err, r_err = bench.pose_error(est["T"], T_true)
    assert t_err < 0.10, f"translation error {t_err:.3f} m"
    assert r_err < 0.3, f"rotation error {r_err:.3f} deg"
    assert est["runtime_ms"] < 2000, "runtime regression (generous budget)"


def test_initial_error_sweep(app, sample_drive, prepared_sample, repo_root):
    bench = load(repo_root)
    T_true = bench.gt_relative(prepared_sample, 20, 21)
    binary = app("icp_register")

    def register(init):
        return bench.register_ours(binary, _scan(sample_drive, 21), _scan(sample_drive, 20), init)["T"]

    rates = bench.initial_error_sweep(register, T_true, [0.0, 0.5], trials=3)
    assert set(rates) == {0.0, 0.5}
    assert rates[0.0] == 1.0
    assert all(0.0 <= v <= 1.0 for v in rates.values())
