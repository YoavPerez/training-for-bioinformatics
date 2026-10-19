"""Module 5 acceptance tests (Python side): ATE and bootstrap CI on fixture trajectories, design doc, end-to-end
pipeline on the sample drive."""

import re
import subprocess

import numpy as np
import pytest
from evo.core.trajectory import PoseTrajectory3D

from slampipe import evaluation
from slampipe.evaluation import evaluate_ate

DESIGN_DOC = "modules/m5_factor_graphs/design_doc.md"

# Thresholds set from the reference implementation on the CI sample (2011_09_26_drive_0002,
# default prepare options): odometry ATE RMSE 0.091 m, odometry + GNSS 0.128 m. Limits allow ~1.5x.
ODOMETRY_ATE_RMSE_MAX = 0.14
GRAPH_ATE_RMSE_MAX = 0.19
# Unaligned ATE (absolute ENU frame, `evaluate_ate(..., align=False)`) of the same reference runs: odometry + GNSS
# 0.657 m, odometry + GNSS + IMU 0.492 m. Limits allow ~1.5x; they catch GNSS fused in the wrong frame or offset.
GRAPH_UNALIGNED_ATE_RMSE_MAX = 1.0
GRAPH_IMU_UNALIGNED_ATE_RMSE_MAX = 0.75


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


def test_bootstrap_ci_contains_mean_and_shrinks():
    rng = np.random.default_rng(1)
    small, large = rng.normal(1.0, 0.5, 30), rng.normal(1.0, 0.5, 3000)
    lo_s, hi_s = evaluation.bootstrap_ci(small)
    lo_l, hi_l = evaluation.bootstrap_ci(large)
    assert lo_s < small.mean() < hi_s
    assert lo_l < large.mean() < hi_l
    assert (hi_l - lo_l) < 0.3 * (hi_s - lo_s)
    assert evaluation.bootstrap_ci(small, seed=3) == evaluation.bootstrap_ci(small, seed=3)


# Template placeholders look like <component> or <What exists today ...>. Code spans and common HTML tags
# (<br>, <img ...>, <sub>, ...) and autolinks (<https://...>) are not placeholders.
_HTML_OR_LINK = r"(?!(?:br|img|sub|sup|details|summary|a|p|b|i|em|strong|code|kbd|div|span)\b|https?:)"
_PLACEHOLDER = re.compile(r"<" + _HTML_OR_LINK + r"[A-Za-z][^<>\n]*>")


def _placeholders(text):
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    return _PLACEHOLDER.findall(prose)


def test_design_doc_completed_and_approved(repo_root):
    path = repo_root / DESIGN_DOC
    assert path.exists(), f"write {DESIGN_DOC} from templates/design_doc.md before coding"
    text = path.read_text(encoding="utf-8")
    for heading in [
        "## Context",
        "## Goals",
        "## Non-goals",
        "## State and factors",
        "## Data flow",
        "## Failure modes",
        "## Evaluation plan",
    ]:
        assert heading in text, f"missing section {heading}"
    assert not _placeholders(text), f"template placeholders are still present: {_placeholders(text)}"
    assert re.search(r"\*\*Status:\*\*\s*approved", text, re.IGNORECASE), "status must be 'approved' by a reviewer"


@pytest.fixture(scope="module")
def pipeline_run(app, sample_drive, prepared_sample, tmp_path_factory):
    out = tmp_path_factory.mktemp("m5")
    r = subprocess.run(
        [str(app("run_pipeline")), str(sample_drive), str(prepared_sample), str(out)], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stderr[-2000:]
    return out


def test_odometry_ate(pipeline_run, prepared_sample):
    ate = evaluate_ate(pipeline_run / "odometry.tum", prepared_sample / "gt.tum")
    assert ate["n"] == 77
    assert ate["rmse"] < ODOMETRY_ATE_RMSE_MAX, f"odometry ATE RMSE {ate['rmse']:.3f} m"


def test_graph_with_gnss_ate(pipeline_run, prepared_sample):
    ate = evaluate_ate(pipeline_run / "optimized.tum", prepared_sample / "gt.tum")
    assert ate["rmse"] < GRAPH_ATE_RMSE_MAX, f"graph ATE RMSE {ate['rmse']:.3f} m"
    absolute = evaluate_ate(pipeline_run / "optimized.tum", prepared_sample / "gt.tum", align=False)
    assert absolute["rmse"] < GRAPH_UNALIGNED_ATE_RMSE_MAX, f"graph unaligned ATE RMSE {absolute['rmse']:.3f} m"


def test_graph_with_imu_builds_and_optimizes(app, sample_drive, prepared_sample, tmp_path):
    r = subprocess.run(
        [str(app("run_pipeline")), str(sample_drive), str(prepared_sample), str(tmp_path), "--imu"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr[-2000:]
    factors = int(re.search(r"factors (\d+)", r.stderr).group(1))
    assert factors > 200, "IMU factors (plus bias factors) should have been added between all keyframes"
    ate = evaluate_ate(tmp_path / "optimized.tum", prepared_sample / "gt.tum")
    assert ate["rmse"] < GRAPH_ATE_RMSE_MAX
    absolute = evaluate_ate(tmp_path / "optimized.tum", prepared_sample / "gt.tum", align=False)
    assert absolute["rmse"] < GRAPH_IMU_UNALIGNED_ATE_RMSE_MAX, f"unaligned ATE RMSE {absolute['rmse']:.3f} m"
