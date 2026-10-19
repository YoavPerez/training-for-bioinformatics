"""Module 4b: two-view geometry in numpy (no OpenCV here; module scripts compare against OpenCV).

Conventions: pixel coordinates are (N, 2) arrays; a projection matrix is P = K [R | t] with [R | t] = T_cam_world,
so x ~ P X for a world point X. Fundamental matrix F satisfies x2ᵀ F x1 = 0 for homogeneous pixels x1, x2.
"""

import numpy as np


def projection_matrix(K: np.ndarray, T_cam_world: np.ndarray) -> np.ndarray:
    """Provided: 3x4 P = K [R | t] from a 4x4 T_cam_world."""
    return K @ T_cam_world[:3, :]


def rotation_angle_deg(R: np.ndarray) -> float:
    """Provided: angle of a rotation matrix [deg]."""
    return float(np.degrees(np.arccos(np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0))))


def normalize_points(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Hartley normalization: returns (x_n, T) with centroid 0 and mean distance √2, where [x_n, 1]ᵀ = T [x, 1]ᵀ."""
    # TODO(m4b): implement.
    del x
    raise NotImplementedError("normalize_points")


def eight_point(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    """Normalized eight-point algorithm: F (rank 2, unit Frobenius norm) from N ≥ 8 correspondences.
    Raise ValueError for fewer than 8 correspondences or arrays of different length."""
    # TODO(m4b): normalize both point sets, solve A f = 0 by SVD, enforce rank 2, undo the normalization.
    del x1, x2
    raise NotImplementedError("eight_point")


def essential_from_fundamental(F: np.ndarray, K1: np.ndarray, K2: np.ndarray) -> np.ndarray:
    """E = K2ᵀ F K1, projected onto the essential manifold (singular values 1, 1, 0)."""
    # TODO(m4b): implement.
    del F, K1, K2
    raise NotImplementedError("essential_from_fundamental")


def triangulate_dlt(P1: np.ndarray, P2: np.ndarray, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    """Linear (DLT) triangulation of N correspondences; returns (N, 3) world points."""
    # TODO(m4b): two rows per view from x × (P X) = 0, solve by SVD, dehomogenize.
    del P1, P2, x1, x2
    raise NotImplementedError("triangulate_dlt")


def reprojection_errors(P: np.ndarray, X: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Pixel distance between the projections of world points X (N, 3) and the observations x (N, 2)."""
    # TODO(m4b): implement (vectorized, no Python loop).
    del P, X, x
    raise NotImplementedError("reprojection_errors")
