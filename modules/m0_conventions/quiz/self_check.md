# Module 0 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M0-R01.** In REP-103, which direction does the y axis of a body frame point (forward/left/up convention)?

**M0-R02.** Which REP-105 frame is continuous (no jumps) but drifts over time: `map`, `odom` or `base_link`?

**M0-R03.** In this program `T_a_b` maps points from frame b to frame a. Given `T_world_lidar` and `T_lidar_imu`, write the expression for `T_world_imu`.

**M0-R04.** A quaternion is written (w, x, y, z) = (0.7071, 0, 0, 0.7071) in Hamilton convention. About which axis does it rotate, and by how many degrees?

**M0-R05.** Name one difference between the Hamilton and the JPL quaternion conventions.

**M0-R06.** Eigen's `Quaterniond(w, x, y, z)` constructor takes the scalar first. In what order does `coeffs()` store the four values in memory?

**M0-R07.** REP-103: what is the base unit for angles, and what is it for time?

**M0-R08.** Which git command shows you which lines of a file were last changed by which commit?

## Self-check 2 — Apply

**M0-A01.** In the sample drive, how many velodyne scans are there, and roughly how long does the drive last (in seconds)?

**M0-A02.** The OXTS timestamps and the velodyne timestamps of the same frame index are not identical. Roughly how large is the offset in the sample? Which file did you read to find out?

**M0-A03.** Is the OXTS field `vf` expressed in the vehicle frame or in a world frame? What does that imply for computing distance travelled?

**M0-A04.** KITTI's calibration file `calib_imu_to_velo.txt` contains R and T. Using the convention in your `CONVENTIONS.md`, what is the name of the transform it describes?

**M0-A05.** You built the image twice a week apart and got different numpy versions. Which file in this repo prevents that, and what mechanism does it use?

## Explain to your mentor
- Walk through `T_world_lidar` vs `T_lidar_world`: which one do you use to put a LiDAR point on the map, and why?
- Why do we write the timestamp source and epoch into a conventions document instead of "just using the timestamps in the data"?
