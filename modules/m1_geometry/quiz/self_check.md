# Module 1 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M1-R01.** What are the two defining properties of a rotation matrix R? What is R⁻¹?

**M1-R02.** Given T_a_b = (R, t), write the rotation and translation parts of T_b_a.

**M1-R03.** How many degrees of freedom does SE(3) have? How many numbers does a 4×4 homogeneous transform store?

**M1-R04.** A rotation vector φ = (0, 0, π/2). What is exp(φ^) applied to the point (1, 0, 0)?

**M1-R05.** Why is the logarithm map of SO(3) numerically delicate near an angle of π, and also near 0?

**M1-R06.** Quaternions q and −q: do they represent the same rotation? What goes wrong in a naive SLERP between q₀ and q₁ when q₀·q₁ < 0?

**M1-R07.** Name the three steps to convert a WGS84 fix (lat, lon, h) into a local ENU position relative to a reference fix.

**M1-R08.** Does the ECEF → ENU rotation matrix depend on the reference latitude, the longitude, the height, or which of these?

**M1-R09.** True or false: composing T_a_b * T_b_c is commutative for rigid transforms.

## Self-check 2 — Apply

**M1-A01.** In your ENU plot of the sample drive, roughly in which compass direction does the car drive?

**M1-A02.** Over the sample drive, how much does the ENU "up" coordinate change? Is that plausible for the street, and what limits its accuracy?

**M1-A03.** In your world-frame scan, how far below the OXTS (IMU) position is the road surface? Which calibration or setup fact explains the value?

**M1-A04.** If you accidentally used `T_imu_velo` where `T_velo_imu` was needed, what would the world-frame scan look like?

**M1-A05.** Your `so3Log` passes the near-π test only after a fix. Which test input caught the problem and what did you change?

## Explain to your mentor
- Walk through the chain of transforms from a velodyne point to the world frame, naming every transform.
- Why does the world (ENU) frame need a reference point, and what happens to your ENU coordinates if a colleague picks a different one?
- Show one edge case your tests cover that the library would have got wrong on the first try.
