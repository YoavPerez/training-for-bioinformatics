# Module 3 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M3-R01.** −½ for white noise, +½ for random walk. See: kalibr_imu_noise — "From the Allan standard deviation (AD)"
**M3-R02.** N at τ = 1 s; K at τ = 3 s. See: kalibr_imu_noise — "From the Allan standard deviation (AD)"
**M3-R03.** rad/s/√Hz and rad/s²/√Hz. See: kalibr_imu_noise — "The Noise Model Parameters in Kalibr"
**M3-R04.** E.g. ionosphere, troposphere, clocks/orbits, multipath; multipath (and blockage) dominates in canyons and forests. See: navipedia_multipath — whole page
**M3-R05.** Corrections from a nearby base station (carrier phase); centimetre level. See: navipedia_rtk — whole page
**M3-R06.** PPP uses global precise orbit/clock products, no local base station; RTK needs a base nearby. See: navipedia_ppp — whole page
**M3-R07.** 3° ≈ 0.052 rad → about 2 m at 40 m. See: stachniss_lidar_odometry_5min — motion distortion
**M3-R08.** `T_ref_i = inverse(T_world_sensor(t_ref)) * T_world_sensor(t_i)`, then `p_ref = T_ref_i * p_i`. See: modern_robotics — Ch. 3.3.1
**M3-R09.** Long averaging times are needed to see the random-walk region; motion would add signal. See: kalibr_imu_noise — "How to Obtain the Parameters for your IMU"
**M3-R10.** Raw: no. Odometry benchmark: yes (motion-corrected with the GPS/IMU trajectory). See: ct_icp_paper — Section V

## Self-check 2 — Apply
**M3-A01.** Depends on the unit; compare in the same units (rad/s/√Hz, not °/h). See: kalibr_imu_noise — "From the Datasheet of the IMU"
**M3-A02.** It grows with time from the reference time and with range. With t_ref at the sweep start (the skewed sample): at the end of the sweep, next to the seam. See: kiss_icp_paper — Step 1 "Motion Prediction and Scan Deskewing"
**M3-A03.** Depends on your sweep; roughly symmetric for constant motion. See: kiss_icp_paper — Step 1
**M3-A04.** Larger, typically by one to two orders of magnitude. See: kalibr_imu_noise — "Kalibr IMU Noise Parameters in Practice"
**M3-A05.** Hardware time sync (e.g. PPS from GNSS or PTP) rather than host receive time. See: esa_gnss_book — Ch. 3.1 "Time and Reference Frames"
**M3-A06.** No: gyro z is almost flat from 0.1 s to 10 s (not slope −½), so an (N, K) fit is misleading there; read N only where the slope is −½ or add terms. See: kalibr_imu_noise — "From the Allan standard deviation (AD)"
