# Module 5 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M5-R01.** What are the two kinds of nodes in a factor graph, and what does a factor represent?

**M5-R02.** What is the difference between a SLAM front-end and back-end?

**M5-R03.** Why does a pose graph need at least one prior (or equivalent) factor?

**M5-R04.** What problem does IMU preintegration solve when keyframes are re-linearized?

**M5-R05.** Which extra variables does an IMU factor connect besides the two poses?

**M5-R06.** Filtering (EKF) vs smoothing (factor graph): name one advantage of each.

**M5-R07.** Scan-to-scan vs scan-to-map odometry: what does the local map buy you?

**M5-R08.** Why does the information matrix of a SLAM problem stay sparse, and why does that matter?

**M5-R09.** A fixed-lag smoother marginalizes out the poses that fall out of its window. What does that do to the sparsity of the remaining problem, and why?

**M5-R10.** Why does a sliding-window smoother usually beat an EKF on the same data, and what does it give up compared with full batch smoothing?

## Self-check 2 — Apply

**M5-A01.** On your two full drives, how did odometry-only, +GNSS, +GNSS+IMU and the ESKF rank by ATE RMSE? Were the differences larger than the confidence intervals?

**M5-A02.** On the short CI sample, adding GNSS can make the result worse than odometry alone, especially without alignment. Why?

**M5-A03.** Which noise values did you choose for the odometry factor, and how did you justify them?

**M5-A04.** How long does `optimize()` take on your longest drive, and how does it scale with the number of keyframes?

**M5-A05.** Which design-doc failure mode did you actually hit, and how did you detect it?

## Explain to your mentor
- Draw your factor graph for three keyframes with every factor type, and say which variables each one touches.
- Walk through the frame conversion from LiDAR odometry to the body-frame graph state.
