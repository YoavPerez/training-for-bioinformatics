"""Module 4: registration benchmark harness.

    python modules/m4_registration/starter/benchmark.py <drive_dir> <prep_dir> --build-dir build --out outputs/m4

Compares your ICP (through the icp_register tool) with Open3D and small_gicp on consecutive scan
pairs: accuracy against the OXTS ground truth, runtime, and convergence basin.
Open3D and small_gicp are optional imports; methods that are not installed are skipped.
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np


# ---------------------------------------------------------------- provided: running the methods
def register_ours(binary: Path, source_bin: Path, target_bin: Path, init: np.ndarray, voxel: float = 0.5) -> dict:
    """Runs icp_register. init is a 4x4 initial guess (only x, y, z and yaw are passed on)."""
    yaw = np.degrees(np.arctan2(init[1, 0], init[0, 0]))
    cmd = [str(binary), str(source_bin), str(target_bin), str(voxel), *map(str, init[:3, 3]), str(yaw)]
    out = json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)
    return {"T": np.array(out["T_target_source"]).reshape(4, 4), "runtime_ms": out["runtime_ms"]}


def _load_xyz(path: Path) -> np.ndarray:
    return np.fromfile(path, dtype=np.float32).reshape(-1, 4)[:, :3].astype(np.float64)


def register_open3d(source_bin: Path, target_bin: Path, init: np.ndarray, voxel: float = 0.5) -> dict | None:
    try:
        import open3d as o3d
    except ImportError:
        return None
    src = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(_load_xyz(source_bin))).voxel_down_sample(voxel)
    tgt = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(_load_xyz(target_bin))).voxel_down_sample(voxel)
    t0 = time.perf_counter()
    tgt.estimate_normals(o3d.geometry.KDTreeSearchParamKNN(10))
    res = o3d.pipelines.registration.registration_icp(
        src, tgt, 1.0, init, o3d.pipelines.registration.TransformationEstimationPointToPlane()
    )
    return {"T": np.asarray(res.transformation), "runtime_ms": 1e3 * (time.perf_counter() - t0)}


def register_small_gicp(source_bin: Path, target_bin: Path, init: np.ndarray, voxel: float = 0.5) -> dict | None:
    try:
        import small_gicp
    except ImportError:
        return None
    t0 = time.perf_counter()
    res = small_gicp.align(
        _load_xyz(target_bin), _load_xyz(source_bin), init_T_target_source=init, downsampling_resolution=voxel
    )
    return {"T": np.asarray(res.T_target_source), "runtime_ms": 1e3 * (time.perf_counter() - t0)}


def pose_error(T_est: np.ndarray, T_ref: np.ndarray) -> tuple[float, float]:
    """(translation error [m], rotation error [deg]) between two 4x4 transforms."""
    D = np.linalg.inv(T_ref) @ T_est
    angle = np.degrees(np.arccos(np.clip((np.trace(D[:3, :3]) - 1.0) / 2.0, -1.0, 1.0)))
    return float(np.linalg.norm(D[:3, 3])), float(angle)


def _tum_to_matrices(path: Path) -> tuple[np.ndarray, np.ndarray]:
    from scipy.spatial.transform import Rotation

    d = np.loadtxt(path)
    T = np.repeat(np.eye(4)[None], len(d), axis=0)
    T[:, :3, :3] = Rotation.from_quat(d[:, 4:8]).as_matrix()
    T[:, :3, 3] = d[:, 1:4]
    return d[:, 0], T


# ---------------------------------------------------------------- your part
def gt_relative(prep_dir: Path, i: int, j: int) -> np.ndarray:
    """Ground-truth T_lidar_i_lidar_j (4x4) between velodyne frames i and j.

    Use gt.tum (T_world_imu per OXTS packet; the sync data has one packet per frame) and
    T_imu_lidar.txt from the prepared directory. Name every transform per CONVENTIONS.md.
    """
    # TODO(m4): implement.
    del prep_dir, i, j
    raise NotImplementedError("gt_relative")


def initial_error_sweep(
    register, T_true: np.ndarray, magnitudes_m: list[float], trials: int = 8, success_m: float = 0.1, seed: int = 0
) -> dict[float, float]:
    """Success rate per initial-error magnitude.

    For each magnitude, perturb T_true by a random horizontal translation of that length and a random
    yaw of (magnitude * 5) degrees, call register(init) -> 4x4 estimate, and count a success when the
    translation error is below success_m.
    """
    # TODO(m4): implement.
    del register, T_true, magnitudes_m, trials, success_m, seed
    raise NotImplementedError("initial_error_sweep")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("prep_dir", type=Path)
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--out", type=Path, default=Path("outputs/m4"))
    args = parser.parse_args()  # noqa: F841
    # TODO(m4): for a set of consecutive pairs, run all available methods, tabulate translation and
    # rotation errors (distributions, not single numbers) and runtimes; run the initial-error sweep
    # on a few pairs and plot success rate vs initial error for each method. Save figures to --out.


if __name__ == "__main__":
    main()
