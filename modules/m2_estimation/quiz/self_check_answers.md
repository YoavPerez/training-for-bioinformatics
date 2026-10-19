# Module 2 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M2-R01.** (JᵀJ) Δx = −Jᵀ r. See: barfoot_ser — "Nonlinear Non-Gaussian Estimation" → "Batch Discrete-Time Estimation" → "Maximum A Posteriori" (Gauss-Newton Method, PDF p. 164)
**M2-R02.** A damping term (JᵀJ + λD)Δx = −Jᵀr; matters far from the optimum or when JᵀJ is ill-conditioned. See: scipy_least_squares — `method='lm'` notes
**M2-R03.** Prediction (motion model) and correction/update (measurement model). See: coursera_state_estimation — Module 2
**M2-R04.** Both recursively propagate p(state | observations so far); hidden state = pose, emissions = measurements. See: labbe_kalman — 02-Discrete-Bayes
**M2-R05.** The error lives in a minimal 3-D tangent space and stays small/near-linear; a quaternion has a unit-norm constraint. See: sola_eskf — Section 5.1 "Motivation"
**M2-R06.** σ_d = σ_c · √200 ≈ 14.1 σ_c. See: kalibr_imu_noise — "Additive White Noise"
**M2-R07.** The estimated error must be added to the nominal state and the error state set back to zero with its covariance adjusted. See: sola_eskf — Sections 6.2–6.3
**M2-R08.** About 3 (the dimension). See: labbe_kalman — 08-Designing-Kalman-Filters, NEES section
**M2-R09.** Bird's-eye pass, content pass, re-implementation pass; after pass 1 decide whether to read further (the five Cs). See: keshav_read_paper — Section 2.1

## Self-check 2 — Apply
**M2-A01.** About 10 from the good start. From [0.1, −5, 0] plain GN diverges (NaN) while LM converges; from [5, 1, −2] GN converges and LM can stall in a flat region (damping is no guarantee). See: scipy_least_squares — `method` parameter
**M2-A02.** Linear at first (velocity error at the outage start), then faster (quadratic/cubic) as attitude and bias errors integrate. See: sola_eskf — Section 5.3 (error kinematics)
**M2-A03.** Typically a few fixes; depends on GNSS rate and noise. See: coursera_state_estimation — Module 3
**M2-A04.** For example: noise units/scaling in Q, wrong Jacobian sign, time alignment of GNSS vs IMU, a GNSS bias the filter does not model (`prepare --gnss-bias-rw`). See: kalibr_imu_noise — "Additive White Noise"
**M2-A05.** The OXTS solution is the ground truth; fusing it is circular and gives near-zero error. See: kitti_raw — devkit readme (OXTS is a GNSS/INS solution)
