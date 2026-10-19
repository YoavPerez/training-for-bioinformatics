"""Module 2 acceptance tests (Python side): Gauss-Newton, 2-D ESKF, ESKF on the sample drive."""

import importlib.util
import subprocess

import numpy as np
from scipy.optimize import least_squares

from slampipe.optim import gauss_newton


def load(repo_root, name):
    spec = importlib.util.spec_from_file_location(name, repo_root / f"modules/m2_estimation/starter/{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------- Gauss-Newton
def test_gauss_newton_solves_linear_problem_in_one_step():
    rng = np.random.default_rng(0)
    A = rng.normal(size=(30, 3))
    b = rng.normal(size=30)
    res = gauss_newton(lambda x: A @ x - b, lambda x: A, np.zeros(3))
    np.testing.assert_allclose(res.x, np.linalg.lstsq(A, b, rcond=None)[0], atol=1e-9)
    assert res.converged and res.iterations <= 2


def test_gauss_newton_matches_scipy_on_curve_fit():
    rng = np.random.default_rng(1)
    t = np.linspace(0.0, 4.0, 60)
    y = 2.5 * np.exp(-1.3 * t) + 0.4 + rng.normal(0.0, 0.02, t.size)

    def residual(x):
        return x[0] * np.exp(x[1] * t) + x[2] - y

    def jacobian(x):
        e = np.exp(x[1] * t)
        return np.column_stack([e, x[0] * t * e, np.ones_like(t)])

    x0 = np.array([1.0, -0.5, 0.0])
    res = gauss_newton(residual, jacobian, x0)
    ref = least_squares(residual, x0, jac=jacobian, method="lm")
    np.testing.assert_allclose(res.x, ref.x, rtol=1e-6)
    assert res.converged
    assert res.cost_history[-1] < res.cost_history[0]  # undamped GN need not decrease at every step
    assert len(res.cost_history) == res.iterations + 1


# ---------------------------------------------------------------- 2-D ESKF
def _simulate_2d(seed, duration=120.0, rate=100.0, gnss_sigma=1.0):
    rng = np.random.default_rng(seed)
    radius, speed = 40.0, 8.0
    w = speed / radius
    acc_noise, gyro_noise = 0.02, 0.002
    dt = 1.0 / rate
    steps = int(duration * rate)
    imu, gnss, truth = [], [], []
    for k in range(steps):
        t = k * dt
        acc = np.array([0.0, speed * w]) + rng.normal(0.0, acc_noise * np.sqrt(rate), 2)
        gyro = w + rng.normal(0.0, gyro_noise * np.sqrt(rate))
        imu.append((acc, gyro))
        t1 = t + dt
        p = np.array([radius * np.sin(w * t1), radius * (1.0 - np.cos(w * t1))])
        truth.append(p)
        gnss.append(p + rng.normal(0.0, gnss_sigma, 2) if (k + 1) % int(rate) == 0 else None)
    return imu, gnss, np.array(truth), dt, (acc_noise, gyro_noise, speed)


def _run_2d(module, seed):
    imu, gnss, truth, dt, (acc_noise, gyro_noise, speed) = _simulate_2d(seed)
    f = module.Eskf2D(
        p=np.zeros(2),
        v=np.array([speed, 0.0]),
        theta=0.0,
        P=np.diag([0.25, 0.25, 0.01, 0.01, 1e-4]),
        acc_noise=acc_noise,
        gyro_noise=gyro_noise,
    )
    errs, nees, raw = [], [], []
    for k, (acc, gyro) in enumerate(imu):
        f.predict(acc, gyro, dt)
        if gnss[k] is not None:
            f.update_position(gnss[k], np.eye(2))
            e = f.p - truth[k]
            errs.append(e)
            nees.append(e @ np.linalg.solve(f.P[:2, :2], e))
            raw.append(gnss[k] - truth[k])
    rmse = np.sqrt(np.mean(np.sum(np.array(errs) ** 2, axis=1)))
    raw_rmse = np.sqrt(np.mean(np.sum(np.array(raw) ** 2, axis=1)))
    return rmse, raw_rmse, float(np.mean(nees))


def test_eskf_2d_beats_raw_gnss(repo_root):
    rmse, raw_rmse, _ = _run_2d(load(repo_root, "eskf_2d"), seed=3)
    assert rmse < 0.6 * raw_rmse


def test_eskf_2d_is_consistent(repo_root):
    module = load(repo_root, "eskf_2d")
    anees = np.mean([_run_2d(module, seed)[2] for seed in range(10, 20)])
    assert 1.0 < anees < 4.0, f"average NEES {anees:.2f}, expected about 2"


def test_eskf_2d_covariance_growth_is_rate_independent(repo_root):
    module = load(repo_root, "eskf_2d")
    diagonals = []
    for rate in (100.0, 400.0):
        f = module.Eskf2D(
            p=np.zeros(2), v=np.array([8.0, 0.0]), theta=0.0, P=np.zeros((5, 5)), acc_noise=0.02, gyro_noise=0.002
        )
        for _ in range(int(rate)):  # the same 1 s of motion at two IMU rates
            f.predict(np.array([0.0, 1.6]), 0.2, 1.0 / rate)
        diagonals.append(np.diag(f.P).copy())
    assert np.all(diagonals[0] > 0.0)
    np.testing.assert_allclose(diagonals[1] / diagonals[0], 1.0, atol=0.05, err_msg="P diagonal, 400 Hz / 100 Hz")


# ---------------------------------------------------------------- 3-D ESKF on the sample drive
def test_eskf_on_sample_drive(app, prepared_sample, repo_root, tmp_path):
    exp = load(repo_root, "outage_experiment")
    est = exp.run_eskf(app("eskf_run").parents[2], prepared_sample, tmp_path / "eskf.csv")
    assert np.all(np.isfinite(est))
    err = exp.position_errors(est, prepared_sample / "gt.tum")
    horizontal_rmse = np.sqrt(np.mean(np.sum(err[:, :2] ** 2, axis=1)))
    assert horizontal_rmse < 3.0, f"horizontal RMSE {horizontal_rmse:.2f} m against the OXTS solution"


def test_eskf_binary_rejects_missing_input(app, tmp_path):
    r = subprocess.run([str(app("eskf_run")), str(tmp_path), str(tmp_path / "x.csv")], capture_output=True)
    assert r.returncode != 0
