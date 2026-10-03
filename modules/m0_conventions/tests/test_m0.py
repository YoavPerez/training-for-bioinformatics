"""Module 0 acceptance tests."""

import importlib.util
import re

import numpy as np
import pytest


def load_replay(repo_root):
    spec = importlib.util.spec_from_file_location("replay", repo_root / "modules/m0_conventions/starter/replay.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_conventions_has_no_blanks(repo_root):
    text = (repo_root / "CONVENTIONS.md").read_text(encoding="utf-8")
    blanks = [line for line in text.splitlines() if "______" in line]
    assert not blanks, f"{len(blanks)} lines still have blanks, e.g.: {blanks[0]!r}"


def test_conventions_reviewed(repo_root):
    text = (repo_root / "CONVENTIONS.md").read_text(encoding="utf-8")
    assert re.search(r"\[x\]\s*reviewed|☑\s*reviewed|✅\s*reviewed", text, re.IGNORECASE), (
        "mark the status line as reviewed (e.g. '☑ reviewed by mentor')"
    )


def _value(text: str, label: str) -> str:
    """The text after the colon on the line starting with `- <label>`."""
    for line in text.splitlines():
        if line.strip().lower().startswith(f"- {label.lower()}"):
            return line.split(":", 1)[1].lower() if ":" in line else ""
    return ""


def test_conventions_quaternion_decided(repo_root):
    text = (repo_root / "CONVENTIONS.md").read_text(encoding="utf-8")
    convention = _value(text, "Convention (Hamilton / JPL)")
    storage = _value(text, "Storage order")
    assert "hamilton" in convention or "jpl" in convention, "state the quaternion convention"
    assert "wxyz" in storage or "xyzw" in storage, "state the storage order"


def test_sample_sequence_loads(sample_drive):
    from slampipe import kitti

    drive = kitti.Drive(sample_drive)
    scan = drive.scan(0)
    assert scan.shape[1] == 4 and scan.shape[0] > 10000
    assert len(drive.oxts()) == len(drive.oxts_times())


def test_replay_summary(sample_drive, repo_root):
    summary = load_replay(repo_root).summarize(sample_drive)
    assert summary["n_scans"] == 77
    assert summary["duration_s"] == pytest.approx(7.8, abs=0.2)
    assert summary["distance_m"] == pytest.approx(81.0, rel=0.05)
    assert np.isfinite(summary["distance_m"])
