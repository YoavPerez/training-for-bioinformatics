"""Provided: converts a KITTI raw drive into the files the C++ tools read.

    python -m slampipe.prepare <drive_dir> <out_dir> [--imu-oxts <extract_drive_dir>]

Writes (times in seconds since the first OXTS packet of the sync drive):
    imu.csv          t,ax,ay,az,wx,wy,wz        body (OXTS) frame; 10 Hz (synced OXTS, one packet per scan)
                                                by default, 100 Hz with --imu-oxts
    gnss.csv         t,x,y,z,sx,sy,sz           simulated GNSS in local ENU (see the origin note below)
    gt.tum           OXTS INS poses T_enu_imu   (TUM format, quaternion with w >= 0)
    lidar_times.csv  one time per scan
    T_imu_lidar.txt  4x4 extrinsic

Needs your module 1 geodesy functions.

ENU origin: the first OXTS (ground-truth) position of the drive. The simulated fixes are noisy, so the
first fix is not at the origin.

--imu-oxts: the unsynced 100 Hz OXTS of the same drive (`data/download.py --extract-oxts`, directory
<root>/<date>/<drive>_extract). Its times use the same t0 as the sync drive; samples before t0 are dropped,
samples after the last sync packet are kept. gnss.csv and gt.tum always come from the sync drive.

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
    imu_oxts: Path | None = None,
) -> None:
    drive = kitti.Drive(Path(drive_dir))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ox = drive.oxts()
    t_ox = drive.oxts_times()
    t0 = t_ox[0]
    t = t_ox - t0

    enu = geodesy.wgs84_to_enu(ox.lat, ox.lon, ox.alt, ox.lat[0], ox.lon[0], ox.alt[0])
    quats = Rotation.from_euler("xyz", np.stack([ox.roll, ox.pitch, ox.yaw], axis=1)).as_quat(canonical=True)

    if imu_oxts is None:
        imu = np.column_stack([t, ox.ax, ox.ay, ox.az, ox.wx, ox.wy, ox.wz])
    else:
        fast = kitti.Drive(Path(imu_oxts))
        fo, ft = fast.oxts(), fast.oxts_times() - t0
        keep = ft >= 0.0
        imu = np.column_stack([ft, fo.ax, fo.ay, fo.az, fo.wx, fo.wy, fo.wz])[keep]
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
    parser.add_argument("--imu-oxts", type=Path, default=None, help="extract drive dir with 100 Hz OXTS for imu.csv")
    args = parser.parse_args()
    prepare(
        args.drive_dir,
        args.out_dir,
        args.gnss_rate,
        args.gnss_sigma_h,
        args.gnss_sigma_v,
        args.gnss_bias_rw,
        args.seed,
        args.imu_oxts,
    )


if __name__ == "__main__":
    main()
