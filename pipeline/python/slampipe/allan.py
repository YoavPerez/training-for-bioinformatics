"""Module 3: Allan variance analysis of IMU data."""

from dataclasses import dataclass

import numpy as np


@dataclass
class NoiseParameters:
    white_noise: float  # N: noise density, e.g. [rad/s/sqrt(Hz)] for a gyro
    random_walk: float  # K: bias random walk, e.g. [rad/s^2/sqrt(Hz)] for a gyro


def simulate_rate_noise(n: int, fs: float, white_noise: float, random_walk: float, seed: int = 0) -> np.ndarray:
    """Provided: synthetic static sensor output (white noise + bias random walk) at rate fs [Hz]."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / fs
    white = rng.normal(0.0, white_noise / np.sqrt(dt), n)
    bias = np.cumsum(rng.normal(0.0, random_walk * np.sqrt(dt), n))
    return white + bias


def allan_deviation(rate: np.ndarray, fs: float, taus: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Overlapping Allan deviation of rate samples recorded at fs [Hz].

    taus: averaging times [s]; default is ~100 log-spaced values up to 1/10 of the record length.
    Returns (taus actually used, deviations).
    """
    # TODO(m3): implement.
    raise NotImplementedError("allan_deviation")


def fit_noise_parameters(taus: np.ndarray, adev: np.ndarray) -> NoiseParameters:
    """Estimates N and K from an Allan deviation curve."""
    # TODO(m3): implement.
    raise NotImplementedError("fit_noise_parameters")
