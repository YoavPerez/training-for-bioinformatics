# Module 0 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M0-R01.** Left (x forward, y left, z up). See: kitti_raw — devkit readme, "Coordinate Systems"
**M0-R02.** The odometry frame drifts but is continuous; the map frame can jump. See: stachniss_slam_intro — whole lecture
**M0-R03.** `T_world_imu = T_world_lidar * T_lidar_imu`. See: modern_robotics — Ch. 3.3 (composition of homogeneous transforms)
**M0-R04.** z axis, 90°. See: sola_eskf — Section 1 (quaternion definition) and Section 3
**M0-R05.** Handedness of the quaternion product (i·j = k vs i·j = −k); also the frame direction of the rotation it represents. See: sola_eskf — Section 3, comparison table
**M0-R06.** x, y, z, w. See: eigen_geometry_module — Quaternion class reference, `coeffs()`
**M0-R07.** Degrees for lat/lon; radians for roll/pitch/yaw. See: kitti_raw — devkit readme, OXTS field list
**M0-R08.** `git blame <file>`. See: missing_semester — lecture 6 "Version Control (Git)"

## Self-check 2 — Apply
**M0-A01.** 77 scans; about 7.8 s. See: kitti_raw — devkit readme, velodyne_points/timestamps.txt
**M0-A02.** ≈ 10–30 ms per frame (mean ≈ 17 ms on the sample; it varies); compare oxts/timestamps.txt with velodyne_points/timestamps.txt. See: kitti_raw — devkit readme, "timestamps"
**M0-A03.** Neither: forward velocity, heading-aligned and parallel to the earth surface (not body, not world); integrate speed × dt for distance, no frame transform needed. See: kitti_raw — devkit readme, OXTS field list
**M0-A04.** `T_velo_imu` (maps IMU-frame points into the velodyne frame), if your convention is `T_to_from`. See: kitti_raw — devkit readme, calibration section
**M0-A05.** `infra/docker/requirements.txt` with exact `==` pins (plus pinned build args in the Dockerfile). See: missing_semester — lecture 8 "Metaprogramming" (dependency management)
