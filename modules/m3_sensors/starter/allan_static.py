"""Module 3: Allan deviation of a static IMU recording.

    python data/download.py --static-imu        # public 16 h recording (MILUV), once
    python modules/m3_sensors/starter/allan_static.py data/static_imu/ifo001_mavros_imu.npz --rate 200 --plot allan.png

Input: either the .npz written by `download.py --static-imu` (arrays t, acc, gyro), or a CSV with columns
t,ax,ay,az,wx,wy,wz (one header line) from your own IMU. Pass --simulate for synthetic data with known
parameters (a method check only). The MILUV authors' own results are in data/static_imu/mavros_imu.yaml:
compare with them only after you have your own numbers.
"""

import argparse
from pathlib import Path

import numpy as np

from slampipe import allan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("imu_csv", type=Path, nargs="?")
    parser.add_argument("--rate", type=float, required=True)
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--plot", type=Path, required=True)
    args = parser.parse_args()
    if args.simulate:
        gyro = np.column_stack(
            [allan.simulate_rate_noise(int(4 * 3600 * args.rate), args.rate, 1e-3, 2e-5, s) for s in range(3)]
        )
    elif args.imu_csv.suffix == ".npz":
        gyro = np.load(args.imu_csv)["gyro"]
    else:
        gyro = np.loadtxt(args.imu_csv, delimiter=",", skiprows=1)[:, 4:7]
    # TODO(m3): for each gyro axis (and then each accelerometer axis): compute the Allan deviation,
    # fit N and K, plot the curves on log-log axes with the fitted lines, print a table next to
    # the datasheet values.
    del gyro


if __name__ == "__main__":
    main()
