# Module 2 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M2-R01.** Write the normal equations of one Gauss-Newton step for minimizing ½‖r(x)‖², in terms of the Jacobian J and residual r.

**M2-R02.** What does Levenberg-Marquardt add to Gauss-Newton, and when does it matter?

**M2-R03.** The Bayes filter alternates two steps. Name them and say which one uses the motion model.

**M2-R04.** In which sense is the Bayes filter the same algorithm as the HMM forward algorithm you know from bioinformatics? What plays the role of the hidden state and of the emissions?

**M2-R05.** Why does an *error-state* EKF estimate the attitude error as a 3-vector instead of filtering the quaternion directly?

**M2-R06.** A gyro's noise density is given in rad/s/√Hz. You sample at 200 Hz. What is the standard deviation of the noise on a single sample?

**M2-R07.** After the Kalman update, why are the "injection" and "reset" steps needed in an ESKF?

**M2-R08.** For a 3-D position error with a consistent filter, what value should the NEES average to?

**M2-R09.** Name the three passes of Keshav's reading method and what you decide at the end of the first pass.

## Self-check 2 — Apply

**M2-A01.** In your notebook, how many iterations did plain Gauss-Newton need from the good start? What happened from the poor start?

**M2-A02.** In your outage experiment, how did the horizontal error grow during the outage (roughly linear, quadratic, other)? Which error source dominates that growth for a car-grade/RTK-grade INS?

**M2-A03.** After GNSS returns, how many fixes did it take for the error to fall back inside its pre-outage range?

**M2-A04.** Your filter's error left the 3σ bound in some segment. List two candidate causes you checked, in the order you checked them.

**M2-A05.** The prepared `gnss.csv` is simulated from the OXTS solution. Why, and what would happen to your result if you fused the OXTS position directly?

## Explain to your mentor
- Walk through one predict + update cycle of your 3-D ESKF on a whiteboard, with the dimensions of every matrix.
- How did you decide that your filter is consistent, and what would an overconfident filter look like in your plots?
- Present your paper summary in 3 minutes.
