"""Module 5 acceptance tests (Python side): design doc, end-to-end pipeline on the sample drive."""

import re
import subprocess

import pytest

from slampipe.evaluation import evaluate

DESIGN_DOC = "modules/m5_factor_graphs/design_doc.md"

# Thresholds set from the reference implementation on the CI sample (2011_09_26_drive_0002,
# default prepare options): odometry ATE RMSE 0.091 m, odometry + GNSS 0.128 m. Limits allow ~1.5x.
ODOMETRY_ATE_RMSE_MAX = 0.14
GRAPH_ATE_RMSE_MAX = 0.19


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
    assert not re.search(r"<[A-Z][^>]*>", text), "template placeholders (<...>) are still present"
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
    ate = evaluate(pipeline_run / "odometry.tum", prepared_sample / "gt.tum")["ate"]
    assert ate["n"] == 77
    assert ate["rmse"] < ODOMETRY_ATE_RMSE_MAX, f"odometry ATE RMSE {ate['rmse']:.3f} m"


def test_graph_with_gnss_ate(pipeline_run, prepared_sample):
    ate = evaluate(pipeline_run / "optimized.tum", prepared_sample / "gt.tum")["ate"]
    assert ate["rmse"] < GRAPH_ATE_RMSE_MAX, f"graph ATE RMSE {ate['rmse']:.3f} m"


def test_graph_with_imu_builds_and_optimizes(app, sample_drive, prepared_sample, tmp_path):
    r = subprocess.run(
        [str(app("run_pipeline")), str(sample_drive), str(prepared_sample), str(tmp_path), "--imu"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr[-2000:]
    factors = int(re.search(r"factors (\d+)", r.stderr).group(1))
    assert factors > 200, "IMU factors (plus bias factors) should have been added between all keyframes"
    ate = evaluate(tmp_path / "optimized.tum", prepared_sample / "gt.tum")["ate"]
    assert ate["rmse"] < GRAPH_ATE_RMSE_MAX
