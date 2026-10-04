# Phase gate A — answers

**PA-01.** `T_world_lidar = T_world_imu * inverse(T_lidar_imu)`. See: modern_robotics — Ch. 3.3.1
**PA-02.** (10, 2, 0). See: modern_robotics — Ch. 3.3.1
**PA-03.** A global map frame (e.g. local ENU); the odometry frame drifts but is continuous. See: stachniss_slam_intro — whole lecture
**PA-04.** (1, 0, 0, 0) and (−1, 0, 0, 0) in (w, x, y, z). See: sola_eskf — Section 2.4
**PA-05.** The stored x (≈0) is read as the scalar and the scalar is read as z: a small z rotation turns into ≈ 180° about (almost) z. See: sola_eskf — Section 3
**PA-06.** (π, 0, 0); not unique: (−π, 0, 0) is equally valid. See: micro_lie — Appendix B-A
**PA-07.** q and −q are the same rotation; without the flip SLERP takes the long way round. See: sola_eskf — Section 2.7
**PA-08.** 3×3 identity (the right Jacobian at zero). See: micro_lie — Appendix B-C
**PA-09.** WGS84 ellipsoid; ECEF, then local ENU (plus the geodetic lat/lon/h input). See: navipedia_ecef_enu — whole page
**PA-10.** About 111 km × cos 60° ≈ 56 km. See: navipedia_geodetic_ecef — "From Ellipsoidal to Cartesian coordinates"
**PA-11.** `git reset --soft HEAD~1` (or `--mixed`). See: missing_semester — lecture 6 "Version Control (Git)"
**PA-12.** The world/map frame and its origin; positions from different origins cannot be compared or fused. See: navipedia_ecef_enu — whole page
**PA-13.** A temporary Matrix3Xd copy of the block is made for every call; take `Eigen::Ref<const Eigen::Matrix3Xd>` instead. See: eigen_function_params — "Ref"
**PA-14.** None (rule of zero); copying does not compile because the unique_ptr member makes the class move-only. See: cppref_rule_of_three — rule of zero
