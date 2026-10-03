"""Provided: converts a KITTI raw drive into the files the C++ tools read.

    python -m slampipe.prepare <drive_dir> <out_dir>

Writes (times in seconds since the first OXTS packet):
    imu.csv          t,ax,ay,az,wx,wy,wz        body (OXTS) frame
    gnss.csv         t,x,y,z,sx,sy,sz           simulated GNSS in local ENU, origin at the first fix
    gt.tum           OXTS INS poses T_enu_imu   (TUM format)
    lidar_times.csv  one time per scan
    T_imu_lidar.txt  4x4 extrinsic

Needs your module 1 geodesy functions.

Why the GNSS is simulated: in KITTI raw, the OXTS RTK GNSS/INS solution is also the ground truth,
so fusing it directly would be circular. gnss.csv is therefore the OXTS position, subsampled to
--gnss-rate and degraded with white noise plus a slowly drifting bias (consumer-grade receiver).
The seed makes it reproducible; record the options you used in every report.
"""

import argparse
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

from slampipe import geodesy, kitti


def simulate_gnss(
    t: np.ndarray, enu: np.ndarray, rate_hz: float, sigma_h: float, sigma_v: float, bias_rw: float, seed: int
) -> np.ndarray:
    """Rows t,x,y,z,sx,sy,sz of a degraded GNSS track."""
    rng = np.random.default_rng(seed)
    keep = [0]
    for k in range(1, t.size):
        if t[k] - t[keep[-1]] >= 1.0 / rate_hz - 1e-3:
            keep.append(k)
    keep = np.array(keep)
    sig = np.array([sigma_h, sigma_h, sigma_v])
    dt = np.diff(t[keep], prepend=t[keep[0]])
    bias = np.cumsum(rng.normal(0.0, 1.0, (keep.size, 3)) * bias_rw * np.sqrt(dt)[:, None], axis=0)
    noisy = enu[keep] + bias + rng.normal(0.0, 1.0, (keep.size, 3)) * sig
    return np.column_stack([t[keep], noisy, np.tile(sig, (keep.size, 1))])


def prepare(
    drive_dir: Path,
    out_dir: Path,
    gnss_rate: float = 1.0,
    gnss_sigma_h: float = 1.5,
    gnss_sigma_v: float = 3.0,
    gnss_bias_rw: float = 0.05,
    seed: int = 0,
) -> None:
    drive = kitti.Drive(Path(drive_dir))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ox = drive.oxts()
    t_ox = drive.oxts_times()
    t0 = t_ox[0]
    t = t_ox - t0

    enu = geodesy.wgs84_to_enu(ox.lat, ox.lon, ox.alt, ox.lat[0], ox.lon[0], ox.alt[0])
    quats = Rotation.from_euler("xyz", np.stack([ox.roll, ox.pitch, ox.yaw], axis=1)).as_quat()

    imu = np.column_stack([t, ox.ax, ox.ay, ox.az, ox.wx, ox.wy, ox.wz])
    np.savetxt(out / "imu.csv", imu, delimiter=",", header="t,ax,ay,az,wx,wy,wz", comments="", fmt="%.9f")

    gnss = simulate_gnss(t, enu, gnss_rate, gnss_sigma_h, gnss_sigma_v, gnss_bias_rw, seed)
    np.savetxt(out / "gnss.csv", gnss, delimiter=",", header="t,x,y,z,sx,sy,sz", comments="", fmt="%.9f")

    np.savetxt(out / "gt.tum", np.column_stack([t, enu, quats]), fmt="%.9f")
    np.savetxt(out / "lidar_times.csv", drive.lidar_times() - t0, fmt="%.9f")

    t_velo_imu = kitti.calib_to_matrix(drive.calib("imu_to_velo"))
    np.savetxt(out / "T_imu_lidar.txt", np.linalg.inv(t_velo_imu), fmt="%.12f")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drive_dir", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--gnss-rate", type=float, default=1.0, help="[Hz]")
    parser.add_argument("--gnss-sigma-h", type=float, default=1.5, help="horizontal noise [m]")
    parser.add_argument("--gnss-sigma-v", type=float, default=3.0, help="vertical noise [m]")
    parser.add_argument("--gnss-bias-rw", type=float, default=0.05, help="bias random walk [m/sqrt(s)]")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    prepare(
        args.drive_dir, args.out_dir, args.gnss_rate, args.gnss_sigma_h, args.gnss_sigma_v, args.gnss_bias_rw, args.seed
    )


if __name__ == "__main__":
    main()
