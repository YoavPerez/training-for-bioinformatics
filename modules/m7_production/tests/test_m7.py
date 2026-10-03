"""Module 7 acceptance tests: regression gate, Argo workflow template, CI workflow, runtime image."""

import json
import os
import shutil
import subprocess
import sys

import pytest
import yaml

from slampipe import gate

FIXTURES = "modules/m7_production/tests/fixtures"
BASELINE = "modules/m7_production/baseline.json"
WORKFLOW = "infra/argo/pipeline-workflow.yaml"


def _json(repo_root, rel):
    return json.loads((repo_root / rel).read_text())


def test_gate_passes_on_good_metrics(repo_root):
    assert gate.check(_json(repo_root, f"{FIXTURES}/good_metrics.json"), _json(repo_root, BASELINE), 0.15) == []


def test_gate_fails_on_degraded_metrics(repo_root):
    failures = gate.check(_json(repo_root, f"{FIXTURES}/degraded_metrics.json"), _json(repo_root, BASELINE), 0.15)
    assert len(failures) == 2 and all(isinstance(f, str) for f in failures)


def test_gate_fails_when_metric_missing(repo_root):
    assert gate.check({"ate": {"rmse": 0.1}}, _json(repo_root, BASELINE), 0.15) != []


def test_gate_cli_exit_codes(repo_root):
    env = dict(os.environ, PYTHONPATH=str(repo_root / "pipeline" / "python"))

    def run(metrics):
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "slampipe.gate",
                str(repo_root / FIXTURES / metrics),
                str(repo_root / BASELINE),
                "--tolerance",
                "0.15",
            ],
            env=env,
            capture_output=True,
        ).returncode

    assert run("good_metrics.json") == 0
    assert run("degraded_metrics.json") == 1


def test_workflow_template_structure(repo_root):
    text = (repo_root / WORKFLOW).read_text()
    assert "TODO" not in text, "complete every TODO in the workflow template"
    doc = yaml.safe_load(text)
    assert doc["kind"] in {"Workflow", "WorkflowTemplate"}
    templates = {t["name"]: t for t in doc["spec"]["templates"]}
    steps = [s for group in templates[doc["spec"]["entrypoint"]]["steps"] for s in group]
    assert any("withParam" in s or "withItems" in s for s in steps), "fan out over sequences"
    assert len(steps) >= 2, "a fan-out step followed by a summary step"
    images = [t["container"]["image"] for t in templates.values() if "container" in t]
    params = {p["name"]: p.get("value", "") for p in doc["spec"]["arguments"]["parameters"]}
    for image in images:
        resolved = params.get("image", "") if "workflow.parameters.image" in image else image
        assert resolved and not resolved.endswith(":latest") and ":" in resolved, "pin the image tag"
    assert any("resources" in t.get("container", {}) for t in templates.values()), "set resource requests"


def test_workflow_template_lints(repo_root):
    argo = shutil.which("argo") or (repo_root / ".cache" / "argo" if (repo_root / ".cache" / "argo").exists() else None)
    if argo is None:
        if os.environ.get("SLAM_REQUIRE_DATA") == "1":
            pytest.fail("argo CLI not found")
        pytest.skip("argo CLI not installed (it is in the dev image)")
    r = subprocess.run([str(argo), "lint", "--offline", str(repo_root / WORKFLOW)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_regression_ci_workflow(repo_root):
    path = repo_root / "modules/m7_production/starter/regression.yml"
    text = path.read_text()
    assert "TODO" not in text
    doc = yaml.safe_load(text)
    commands = " ".join(step.get("run", "") for job in doc["jobs"].values() for step in job["steps"])
    assert "slampipe.gate" in commands and "slampipe.evaluation" in commands and "run_pipeline" in commands


def test_runtime_dockerfile_is_pinned(repo_root):
    text = (repo_root / "infra/docker/pipeline.Dockerfile").read_text()
    assert "TODO" not in text
    froms = [line.split()[1] for line in text.splitlines() if line.startswith("FROM ")]
    assert froms and all(not f.endswith(":latest") for f in froms)
    assert "USER" in text, "do not run as root"
