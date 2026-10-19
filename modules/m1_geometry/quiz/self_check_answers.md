# Module 1 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M1-R01.** RᵀR = I and det R = +1; R⁻¹ = Rᵀ. See: modern_robotics — Ch. 3.2.1
**M1-R02.** R_b_a = Rᵀ, t_b_a = −Rᵀ t. See: modern_robotics — Ch. 3.3.1 (inverse of a transformation matrix)
**M1-R03.** 6; 16 numbers (12 meaningful). See: micro_lie — Appendix D
**M1-R04.** (0, 1, 0). See: micro_lie — Section II-D and Appendix B-A
**M1-R05.** Near 0: division by sin θ → 0; near π: the antisymmetric part vanishes so the axis must come from the symmetric part. See: modern_robotics — Ch. 3.2.3.3 (matrix logarithm of rotations)
**M1-R06.** Yes, same rotation; naive SLERP takes the long way (> 180°). See: sola_eskf — Sections 2.4 and 2.7 (SLERP)
**M1-R07.** Geodetic → ECEF; subtract the reference ECEF; rotate into ENU at the reference lat/lon. See: navipedia_ecef_enu — whole page
**M1-R08.** Latitude and longitude only (not height). See: navipedia_ecef_enu — rotation matrix
**M1-R09.** False. See: modern_robotics — Ch. 3.3.1 (properties of transformation matrices)

## Self-check 2 — Apply
**M1-A01.** Roughly west (heading ≈ 180° from east; ENU x decreasing). See: kitti_raw — devkit readme, OXTS yaw definition
**M1-A02.** Well under a metre; plausible for a flat street, limited by the vertical accuracy of the GNSS/INS solution. See: navipedia_measurements — error budget (vertical vs horizontal)
**M1-A03.** About 0.9–1.1 m: the OXTS unit is mounted ~0.93 m above the road (velodyne ~1.73 m). See: kitti_raw — devkit readme, sensor setup figure
**M1-A04.** Shifted by about twice the 1.2 m IMU–LiDAR offset (≈ 2.4 m) and slightly mis-rotated; the road no longer lies ~1 m below the IMU. See: modern_robotics — Ch. 3.3.1
**M1-A05.** The near-π case (angle π − ε, small ε) or the exact-π case. See: micro_lie — Appendix B-A
