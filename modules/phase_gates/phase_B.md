# Phase gate B — Estimation & sensors (modules 2–3)

Closed-book, 45 minutes. Score yourself with `phase_B_answers.md`.

**PB-01.** Write the Kalman gain for a linear measurement z = Hx + v, v ~ N(0, R).

**PB-02.** Why is the Joseph form of the covariance update preferred in practice?

**PB-03.** Your ESKF's NEES averages 12 for 3-D position. What does that say and what do you check first?

**PB-04.** An accelerometer noise density is 0.002 m/s²/√Hz at 100 Hz. What variance do you add to the velocity per step in the discrete filter?

**PB-05.** During a GNSS outage, why does a small roll error make the position error grow quickly?

**PB-06.** What does Gauss-Newton approximate in Newton's method, and when is that approximation good?

**PB-07.** On an Allan deviation plot, a curve keeps falling with slope −½ until τ = 1000 s, the end of the plot. What does that tell you about the recording?

**PB-08.** List the error sources that make GNSS worse in a forest than in an open field.

**PB-09.** A 64-beam LiDAR on a car turning at 45°/s: why is the motion distortion of an uncorrected sweep most visible at the seam?

**PB-10.** A 10 ms clock offset between IMU and LiDAR at 20 m/s and 30°/s. Estimate the position error at 30 m range.

**PB-11.** Why can't you validate a GNSS/INS fusion on KITTI by fusing the OXTS positions and comparing to the OXTS ground truth?

**PB-12.** Bridge: the Bayes filter and the HMM forward algorithm. Map each of these to the filter: hidden state, transition matrix, emission probability, forward variable.
