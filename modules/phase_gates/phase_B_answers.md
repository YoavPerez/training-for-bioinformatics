# Phase gate B — answers

**PB-01.** K = P Hᵀ (H P Hᵀ + R)⁻¹. See: labbe_kalman — 06-Multivariate-Kalman-Filters
**PB-02.** It stays symmetric positive semi-definite under round-off and suboptimal gains. See: labbe_kalman — 07-Kalman-Filter-Math
**PB-03.** Overconfident (expected ≈ 3); check Q scaling/units and measurement R first. See: labbe_kalman — 08-Designing-Kalman-Filters
**PB-04.** σ² Δt = 0.002² × 0.01 = 4 × 10⁻⁸ (m/s)² per axis. See: kalibr_imu_noise — "Additive White Noise"
**PB-05.** A tilt error projects gravity into the horizontal acceleration, which is integrated twice. See: sola_eskf — Section 5.3
**PB-06.** It drops the second-order residual terms of the Hessian (H ≈ JᵀJ); good when residuals are small or nearly linear. See: barfoot_ser — "Nonlinear Non-Gaussian Estimation"
**PB-07.** White noise dominates and the recording is too short (or the IMU too good) to see bias instability/random walk. See: kalibr_imu_noise — "From the Allan standard deviation (AD)"
**PB-08.** Signal blockage/attenuation by foliage, multipath, fewer satellites (poor geometry). See: navipedia_multipath — whole page
**PB-09.** Start and end points are measured 0.1 s apart (4.5° of rotation) but are neighbours in space. See: stachniss_lidar_odometry_5min — whole video
**PB-10.** 0.2 m from translation plus 30 m × 0.0052 rad ≈ 0.16 m from rotation, so about 0.2–0.35 m. See: ct_icp_paper — Section V
**PB-11.** The OXTS solution is both the measurement and the ground truth: the test is circular. See: kitti_raw — devkit readme
**PB-12.** Hidden state ↔ pose; transition matrix ↔ motion model; emission ↔ measurement likelihood; forward variable ↔ the filter's belief (posterior). See: labbe_kalman — 02-Discrete-Bayes
