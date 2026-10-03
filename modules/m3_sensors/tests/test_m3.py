"""Module 3 acceptance tests (Python side): Allan variance, deskew of a real scan, time offset."""

import importlib.util
import sys

import numpy as np
import pytest

from slampipe import allan


def load(repo_root, name):
    starter = repo_root / "modules/m3_sensors/starter"
    sys.path.insert(0, str(starter))
    spec = importlib.util.spec_from_file_location(name, starter / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_allan_white_noise_slope():
    fs = 100.0
    x = allan.simulate_rate_noise(200_000, fs, white_noise=0.01, random_walk=0.0, seed=1)
    taus, adev = allan.allan_deviation(x, fs)
    assert taus.ndim == 1 and taus.shape == adev.shape
    slope = np.polyfit(np.log10(taus[:30]), np.log10(adev[:30]), 1)[0]
    assert slope == pytest.approx(-0.5, abs=0.05)
    i = np.argmin(np.abs(taus - 1.0))
    assert adev[i] == pytest.approx(0.01, rel=0.1), "at tau = 1 s the white-noise line reads N"


def test_allan_recovers_parameters():
    fs = 100.0
    n_true, k_true = 2e-3, 5e-5
    x = allan.simulate_rate_noise(int(3 * 3600 * fs), fs, n_true, k_true, seed=7)
    taus, adev = allan.allan_deviation(x, fs)
    params = allan.fit_noise_parameters(taus, adev)
    assert params.white_noise == pytest.approx(n_true, rel=0.1)
    assert params.random_walk == pytest.approx(k_true, rel=0.35)


def test_deskew_real_scan(app, skewed_sample, repo_root, tmp_path):
    tools = load(repo_root, "skew_tools")
    sample = tools.load_skewed(skewed_sample)
    pts, traj = tools.write_inputs(sample, tmp_path)
    fixed = tools.run_deskew(app("deskew_scan"), pts, traj, tmp_path / "out.csv")
    before = np.sqrt(np.mean(np.sum((sample["points"] - sample["reference"]) ** 2, axis=1)))
    after = np.sqrt(np.mean(np.sum((fixed - sample["reference"]) ** 2, axis=1)))
    assert before > 0.3
    assert after < 0.01 * before


def test_time_offset_sweep(app, skewed_sample, repo_root, tmp_path):
    exp = load(repo_root, "time_offset")
    offsets = np.array([-0.01, -0.005, 0.0, 0.005, 0.01])
    rms = exp.offset_sweep(skewed_sample, app("deskew_scan"), offsets, tmp_path)
    assert rms.shape == offsets.shape
    assert np.argmin(rms) == 2
    assert rms[0] > rms[1] > rms[2] < rms[3] < rms[4]
