"""Module 6 acceptance tests (Python side): evaluation on fixture trajectories, false loop on the sample."""

import importlib.util
import subprocess

import numpy as np
import pytest
from evo.core.trajectory import PoseTrajectory3D

from slampipe import evaluation


def _traj(xyz: np.ndarray, t: np.ndarray | None = None) -> PoseTrajectory3D:
    t = np.arange(len(xyz), dtype=float) * 0.1 if t is None else t
    quat_wxyz = np.tile([1.0, 0.0, 0.0, 0.0], (len(xyz), 1))
    return PoseTrajectory3D(positions_xyz=xyz, orientations_quat_wxyz=quat_wxyz, timestamps=t)


@pytest.fixture
def reference():
    s = np.linspace(0, 200, 400)
    return np.column_stack([s, 20 * np.sin(s / 30.0), np.zeros_like(s)])


def test_ate_is_zero_after_alignment_for_rigid_offset(reference):
    est = reference + np.array([5.0, -3.0, 1.0])
    errs = evaluation.ate_errors(_traj(est), _traj(reference), align=True)
    assert errs.shape == (len(reference),)
    assert np.max(errs) < 1e-6


def test_ate_without_alignment_sees_the_offset(reference):
    errs = evaluation.ate_errors(_traj(reference + np.array([3.0, 4.0, 0.0])), _traj(reference), align=False)
    np.testing.assert_allclose(errs, 5.0, atol=1e-9)


def test_ate_matches_known_noise(reference):
    rng = np.random.default_rng(0)
    errs = evaluation.ate_errors(_traj(reference + rng.normal(0, 0.1, reference.shape)), _traj(reference))
    assert np.sqrt(np.mean(errs**2)) == pytest.approx(0.1 * np.sqrt(3), rel=0.15)


def test_ate_does_not_modify_inputs(reference):
    est, ref = _traj(reference + 1.0), _traj(reference)
    before = est.positions_xyz.copy()
    evaluation.ate_errors(est, ref)
    np.testing.assert_array_equal(est.positions_xyz, before)


def test_rpe_of_constant_offset_is_zero(reference):
    errs = evaluation.rpe_errors(_traj(reference + 2.0), _traj(reference), delta_m=10.0)
    assert len(errs) > 10
    assert np.max(errs) < 1e-6


def test_bootstrap_ci_contains_mean_and_shrinks():
    rng = np.random.default_rng(1)
    small, large = rng.normal(1.0, 0.5, 30), rng.normal(1.0, 0.5, 3000)
    lo_s, hi_s = evaluation.bootstrap_ci(small)
    lo_l, hi_l = evaluation.bootstrap_ci(large)
    assert lo_s < small.mean() < hi_s
    assert lo_l < large.mean() < hi_l
    assert (hi_l - lo_l) < 0.3 * (hi_s - lo_s)
    assert evaluation.bootstrap_ci(small, seed=3) == evaluation.bootstrap_ci(small, seed=3)


def test_false_loop_on_sample_is_rejected_by_the_robust_kernel(app, sample_drive, prepared_sample, tmp_path):
    def ate(*flags):
        out = tmp_path / ("_".join(flags) or "clean")
        out.mkdir()
        subprocess.run(
            [str(app("run_pipeline")), str(sample_drive), str(prepared_sample), str(out), *flags],
            check=True,
            capture_output=True,
        )
        return evaluation.evaluate(out / "optimized.tum", prepared_sample / "gt.tum")["ate"]["rmse"]

    clean, corrupted = ate(), ate("--false-loop", "5", "70")
    assert corrupted < 1.2 * clean + 0.02, f"clean {clean:.3f} m, with false loop {corrupted:.3f} m"


def _load_ablation(repo_root):
    spec = importlib.util.spec_from_file_location(
        "ablation", repo_root / "modules/m6_loop_closure_eval/starter/ablation.py"
    )
    ablation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ablation)
    return ablation


def test_ablation_table(repo_root):
    ablation = _load_ablation(repo_root)
    ate = {"rmse": 1.0, "median": 0.9, "p95": 2.0, "mean_ci95": [0.8, 1.1]}
    results = {
        (g, lo, d): {"ate": dict(ate, rmse=1.0 + 0.1 * (not g))}
        for g in (True, False)
        for lo in (True, False)
        for d in (True, False)
    }
    table = ablation.summarize_ablation(results)
    assert table.count("\n") >= 9, "header, separator and 8 rows"
    assert "+0.100" in table


def test_seed_spread_table(repo_root):
    ablation = _load_ablation(repo_root)
    table = ablation.summarize_seeds({(True, True, True): [0.1, 0.4, 0.3], (True, False, False): [0.5, 0.7]})
    assert table.count("\n") >= 3, "header, separator and 2 rows"
    assert "0.267" in table and "0.153" in table, "mean and sample std (ddof=1) of 0.1, 0.4, 0.3"
    assert "0.600" in table and "0.141" in table, "mean and sample std of 0.5, 0.7"
