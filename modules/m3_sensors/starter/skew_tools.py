"""Provided helpers for the module 3 deskew experiments (no TODOs here)."""

import subprocess
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation


def load_skewed(sample_dir: Path) -> dict[str, np.ndarray]:
    """Arrays from data/samples/skewed/scan.npz: points, times, reference, traj_t, traj_T."""
    with np.load(Path(sample_dir) / "scan.npz") as z:
        return {k: z[k] for k in z.files}


def write_inputs(sample: dict[str, np.ndarray], out_dir: Path) -> tuple[Path, Path]:
    """Writes points.csv (x,y,z,t) and trajectory.tum for the deskew_scan tool."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pts = out_dir / "points.csv"
    np.savetxt(pts, np.column_stack([sample["points"], sample["times"]]), delimiter=",", fmt="%.9f")
    q = Rotation.from_matrix(sample["traj_T"][:, :3, :3]).as_quat()
    tum = out_dir / "trajectory.tum"
    np.savetxt(tum, np.column_stack([sample["traj_t"], sample["traj_T"][:, :3, 3], q]), fmt="%.9f")
    return pts, tum


def run_deskew(
    binary: Path, points: Path, traj: Path, out: Path, t_ref: float = 0.0, offset: float = 0.0
) -> np.ndarray:
    """Runs your C++ deskew via the deskew_scan tool and returns the (N, 3) result."""
    subprocess.run([str(binary), str(points), str(traj), str(out), str(t_ref), str(offset)], check=True)
    return np.loadtxt(out, delimiter=",")
