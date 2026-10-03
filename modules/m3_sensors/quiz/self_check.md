# Module 3 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M3-R01.** On a log-log Allan deviation plot, what slope does white noise have, and what slope does a bias random walk have?

**M3-R02.** At which averaging time τ do you read the white-noise density N directly off its fitted line? At which τ do you read K off its line?

**M3-R03.** What are the units of a gyroscope's white-noise density and of its bias random walk?

**M3-R04.** Name three GNSS error sources and say which one typically dominates in an urban canyon or a forest.

**M3-R05.** What does RTK need that standalone GNSS does not, and roughly what accuracy does it reach once ambiguities are fixed?

**M3-R06.** What is the difference between PPP and RTK in terms of infrastructure?

**M3-R07.** A spinning LiDAR takes 0.1 s per revolution and the vehicle turns at 30°/s. How far is a point 40 m away displaced by the rotation between the start and end of the sweep (order of magnitude)?

**M3-R08.** To deskew a point measured at time tᵢ into the frame at t_ref, which two poses do you need and how do you combine them (in `T_<to>_<from>` notation)?

**M3-R09.** Why is a long, *static* recording needed for Allan variance analysis?

**M3-R10.** Are the velodyne scans in the KITTI *raw* dataset motion-compensated? And the ones in the KITTI odometry benchmark?

## Self-check 2 — Apply

**M3-A01.** What values of N and K did you obtain for the gyro z-axis, and how do they compare with the datasheet?

**M3-A02.** In your before/after deskew figure, where in the scan is the distortion largest, and why there?

**M3-A03.** From your time-offset sweep, what is the deskew error for a 10 ms offset? Is the curve symmetric around zero?

**M3-A04.** The OXTS IMU on KITTI is a high-grade unit. Would you expect a consumer MEMS IMU's N to be larger or smaller, and by roughly how much?

**M3-A06.** On the MILUV recording, is every gyro axis white-noise dominated around τ = 1 s? How can you tell from the plot, and what does that mean for a two-parameter (N, K) fit?

**M3-A05.** Your sweep implies a maximum tolerable clock offset for your error budget. What synchronization mechanism would you ask the hardware team for, to stay below it?

## Explain to your mentor
- Show your Allan plot and explain each region of the curve.
- Explain where in the pipeline (module 4 onwards) a residual time offset would show up first, and how you would detect it from data alone.
