# Data

## License

| Dataset | License | Commercial use |
|---|---|---|
| KITTI raw | CC BY-NC-SA 3.0 | **No**: training and research only |
| MILUV (static IMU, module 3) | CC BY 4.0 | Yes, with attribution |

Cite: A. Geiger, P. Lenz, C. Stiller, R. Urtasun, "Vision meets Robotics: The KITTI Dataset", IJRR 2013. Applied-project datasets have their own licenses, listed in `applied_project/README.md`.

## Getting data

```bash
python data/download.py --sample                         # CI subset: drive 2011_09_26_0002, LiDAR + OXTS only
python data/download.py --drive 2011_09_30_drive_0027    # full drive into data/kitti/
python data/download.py --drive 2011_09_30_drive_0027 --extract-oxts   # + unsynced 100 Hz OXTS
```

`python data/download.py --static-imu` fetches one 16-hour static IMU recording from MILUV (Shalaby et al., figshare DOI 10.25452/figshare.plus.28386041.v1) into `data/static_imu/` as an `.npz`, together with the dataset authors' Allan-variance results. It needs ~11 GB of temporary disk space and the `rosbags` package (in the dev image).

Full drives go to `data/kitti/`, which is gitignored. Never commit data.

## Suggested drives

| Use | Drive | Notes |
|---|---|---|
| CI sample, quick checks | `2011_09_26_drive_0002` | 77 frames, short |
| Modules 2–5 main development | `2011_09_30_drive_0027` | ~1100 frames, contains a loop (KITTI odometry sequence 07) |
| Second sequence for comparisons | `2011_09_30_drive_0018` | ~2760 frames, several loops (odometry sequence 05) |
| Large-scale test | `2011_10_03_drive_0027` | ~4500 frames, many loops (odometry sequence 00) |

Check the KITTI raw devkit readme for the mapping between raw drives and odometry sequences, and for the meaning of every OXTS field.

## Preparing a drive for the C++ tools

```bash
python -m slampipe.prepare data/kitti/2011_09_30/2011_09_30_drive_0027_sync outputs/prep_0027
```

`gnss.csv` is **simulated**: the OXTS RTK solution is also the ground truth, so `prepare` subsamples it to 1 Hz and adds noise plus a drifting bias. Record the `prepare` options and seed in every experiment.

## Module 3 skewed sample

`data/samples/skewed/scan.npz` holds one KITTI raw scan (taken as the reference) with strong synthetic motion distortion added: a 45°/s yaw plus the recorded forward speed, with per-point times taken from azimuth. `download.py --sample` creates it. Note that KITTI *raw* scans are not motion-compensated; only the odometry-benchmark copies are.
