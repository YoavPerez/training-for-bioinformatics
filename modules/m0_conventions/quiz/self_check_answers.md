# Module 0 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M0-R01.** Left. See: rep103 — "Axis Orientation"
**M0-R02.** `odom`. See: rep105 — "odom"
**M0-R03.** `T_world_imu = T_world_lidar * T_lidar_imu`. See: modern_robotics — Ch. 3.3 (composition of homogeneous transforms)
**M0-R04.** z axis, 90°. See: sola_eskf — Section 1 (quaternion definition) and Section 3
**M0-R05.** Handedness of the quaternion product (i·j = k vs i·j = −k); also the frame direction of the rotation it represents. See: sola_eskf — Section 3, comparison table
**M0-R06.** x, y, z, w. See: eigen_geometry_module — Quaternion class reference, `coeffs()`
**M0-R07.** Radian; second. See: rep103 — "Base Units"
**M0-R08.** `git blame <file>`. See: missing_semester — lecture 6 "Version Control (Git)"

## Self-check 2 — Apply
**M0-A01.** 77 scans; about 7.8 s. See: kitti_raw — devkit readme, velodyne_points/timestamps.txt
**M0-A02.** A few milliseconds per frame (it varies); compare oxts/timestamps.txt with velodyne_points/timestamps.txt. See: kitti_raw — devkit readme, "timestamps"
**M0-A03.** Vehicle frame (forward velocity); integrate speed × dt over time, no frame transform needed for distance. See: kitti_raw — devkit readme, OXTS field list
**M0-A04.** `T_velo_imu` (maps IMU-frame points into the velodyne frame), if your convention is `T_to_from`. See: kitti_raw — devkit readme, calibration section
**M0-A05.** `infra/docker/requirements.txt` with exact `==` pins (plus pinned build args in the Dockerfile). See: missing_semester — lecture 8 "Metaprogramming" (dependency management)
