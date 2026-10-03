"""Provided: readers for the KITTI raw dataset layout.

A drive directory looks like <root>/2011_09_26/2011_09_26_drive_0002_sync/ with
oxts/, velodyne_points/ and image_*/ inside; calibration files sit in <root>/2011_09_26/.
See the KITTI raw devkit readme for the meaning of each OXTS field.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

OXTS_FIELDS = (
    "lat lon alt roll pitch yaw vn ve vf vl vu ax ay az af al au wx wy wz wf wl wu "
    "pos_accuracy vel_accuracy navstat numsats posmode velmode orimode"
).split()


@dataclass
class Drive:
    path: Path

    @property
    def date_dir(self) -> Path:
        return self.path.parent

    def oxts(self) -> np.ndarray:
        """Structured array with one row per OXTS packet; field names as in OXTS_FIELDS."""
        files = sorted((self.path / "oxts" / "data").glob("*.txt"))
        rows = [np.loadtxt(f) for f in files]
        return np.rec.fromarrays(np.array(rows).T, names=OXTS_FIELDS)

    def oxts_times(self) -> np.ndarray:
        return read_timestamps(self.path / "oxts" / "timestamps.txt")

    def lidar_times(self) -> np.ndarray:
        return read_timestamps(self.path / "velodyne_points" / "timestamps.txt")

    def scan_paths(self) -> list[Path]:
        return sorted((self.path / "velodyne_points" / "data").glob("*.bin"))

    def scan(self, index: int) -> np.ndarray:
        """(N, 4) float32 array: x, y, z, reflectance in the velodyne frame."""
        return read_velodyne_bin(self.scan_paths()[index])

    def calib(self, name: str) -> dict[str, np.ndarray]:
        """Reads e.g. calib('imu_to_velo') from calib_imu_to_velo.txt."""
        return read_calib(self.date_dir / f"calib_{name}.txt")


def read_timestamps(path: Path) -> np.ndarray:
    """Absolute UNIX times [s] (float64) from a KITTI timestamps.txt."""
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        day, frac = line.split(".")
        t = datetime.strptime(day, "%Y-%m-%d %H:%M:%S").timestamp()
        out.append(t + float("0." + frac))
    return np.array(out)


def read_velodyne_bin(path: Path) -> np.ndarray:
    return np.fromfile(path, dtype=np.float32).reshape(-1, 4)


def read_calib(path: Path) -> dict[str, np.ndarray]:
    out = {}
    for line in Path(path).read_text().splitlines():
        key, _, value = line.partition(":")
        try:
            out[key.strip()] = np.array([float(v) for v in value.split()])
        except ValueError:
            continue  # e.g. calib_time
    return out


def calib_to_matrix(calib: dict[str, np.ndarray]) -> np.ndarray:
    """4x4 transform from a calib dict containing R (row-major 3x3) and T."""
    m = np.eye(4)
    m[:3, :3] = calib["R"].reshape(3, 3)
    m[:3, 3] = calib["T"]
    return m
