"""Module 2: nonlinear least squares by Gauss-Newton."""

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np


@dataclass
class GaussNewtonResult:
    x: np.ndarray
    converged: bool
    iterations: int
    cost_history: list[float] = field(default_factory=list)  # 0.5 * ||r||^2 per iteration, incl. start


def gauss_newton(
    residual: Callable[[np.ndarray], np.ndarray],
    jacobian: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    max_iterations: int = 50,
    tol: float = 1e-10,
) -> GaussNewtonResult:
    """Minimizes 0.5 * ||residual(x)||^2. Converged when the step norm drops below tol."""
    # TODO(m2): implement.
    raise NotImplementedError("gauss_newton")
