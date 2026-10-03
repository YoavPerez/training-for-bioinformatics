"""Module 2: planar error-state EKF (warm-up before the 3-D C++ filter).

Nominal state: position p (2), velocity v (2), heading theta (1), all in the world frame.
Error state (fixed order): [dp_x, dp_y, dv_x, dv_y, dtheta].
IMU: body-frame acceleration (2) [m/s^2] and yaw rate [rad/s]; no biases in this warm-up.
Noise parameters are continuous-time densities.
"""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Eskf2D:
    p: np.ndarray
    v: np.ndarray
    theta: float
    P: np.ndarray  # 5x5 error-state covariance
    acc_noise: float  # [m/s^2/sqrt(Hz)]
    gyro_noise: float  # [rad/s/sqrt(Hz)]
    history: list = field(default_factory=list)

    def predict(self, acc_body: np.ndarray, yaw_rate: float, dt: float) -> None:
        """Propagates nominal state and error covariance with one IMU sample held over dt."""
        # TODO(m2): implement.
        raise NotImplementedError("Eskf2D.predict")

    def update_position(self, z: np.ndarray, R: np.ndarray) -> None:
        """Fuses a 2-D position measurement with covariance R (2x2)."""
        # TODO(m2): implement (update, inject, reset).
        raise NotImplementedError("Eskf2D.update_position")
