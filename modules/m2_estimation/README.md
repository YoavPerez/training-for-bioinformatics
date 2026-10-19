# Module 2: State estimation fundamentals
**Tentative effort:** ~1 week · **Phase:** B — Estimation & sensors

## Goal
Understand estimation as probabilistic inference, implement nonlinear least squares and a loosely coupled GNSS + IMU error-state EKF, and characterize its behaviour during a GNSS outage. Start the paper-summary habit.

---

## Segment 1 — Learn

### Learn from
- [Coursera — State Estimation and Localization for Self-Driving Cars](https://www.coursera.org/learn/state-estimation-localization-self-driving-cars) — course (free to audit) — Module 1 "Least Squares"; Module 2 "State Estimation - Linear and Nonlinear Kalman Filters"; Module 3 "GNSS/INS Sensing for Pose Estimation". Closest match to this module.
- [Labbe — Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python) — book (notebooks) — 02-Discrete-Bayes, 06-Multivariate-Kalman-Filters, 07-Kalman-Filter-Math, 08-Designing-Kalman-Filters (NEES), 11-Extended-Kalman-Filters
- [Barfoot — State Estimation for Robotics, 2nd ed.](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser24.pdf) — book (free PDF) — "Linear-Gaussian Estimation" (PDF p. 63) and "Nonlinear Non-Gaussian Estimation" (PDF p. 125): batch vs recursive, Gauss-Newton, EKF
- [Solà — Quaternion kinematics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508) — paper — Sections 5 "Error-state kinematics for IMU-driven systems" and 6 "Fusing IMU with complementary sensory data"
- [Kalibr wiki — IMU Noise Model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model) — docs — "Additive White Noise", "Bias" (units of the noise parameters)
- [SciPy — least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html) — docs — parameters `jac`, `method`, `loss`
- [Ceres Solver tutorial](http://ceres-solver.org/nnls_tutorial.html) — docs — "Hello World!", "Curve Fitting", "Robust Curve Fitting" (to compare the C++ API with what you build)
- [Keshav — How to Read a Paper](http://ccr.sigcomm.org/online/files/p83-keshavA.pdf) — paper — Section 2 "The three-pass approach"

Optional: [Kalman Filter — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=o_HW6GnLqvg), [Bayes Filter — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=oUq0a8jHSQg), [Least Squares — An Informal Introduction](https://www.youtube.com/watch?v=r2cyMQ5NB1o).

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Gauss-Newton.** Implement `gauss_newton` in [`pipeline/python/slampipe/optim.py`](../../pipeline/python/slampipe/optim.py). Complete the notebook [`starter/gauss_newton.ipynb`](starter/gauss_newton.ipynb): fit the model by hand, compare with SciPy (and optionally Ceres), and try a poor initial guess.
2. **2-D ES-EKF.** Implement `predict` and `update_position` in [`starter/eskf_2d.py`](starter/eskf_2d.py).
3. **3-D ES-EKF.** Implement `Eskf::predict` and `Eskf::updatePosition` in [`pipeline/src/estimation/eskf.cpp`](../../pipeline/src/estimation/eskf.cpp). The error-state ordering and the noise units are fixed in the header.
4. **Real data.** Prepare a full drive (`python -m slampipe.prepare …`, see `data/README.md`) and run `eskf_run` on it.
5. **Outage experiment.** Complete [`starter/outage_experiment.py`](starter/outage_experiment.py). Drop GNSS for 30–60 s on a full drive, and plot the horizontal error and the 3σ bound over time, with and without the outage.
6. **Paper summary.** Write your first one-page summary with [`templates/paper_summary.md`](../../templates/paper_summary.md). Use one of the module's papers or one your mentor suggests, and present it at paper club.

### C++ focus: class design and numerical hygiene
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "C: Classes and class hierarchies" (C.2 invariants), "Con: Constants and immutability"
- [Back to Basics: Cpp Value Semantics — Klaus Iglberger](https://www.youtube.com/watch?v=G9MxNwUoSt0) — video

Task: write the invariants of `Eskf` in its header (covariance symmetric positive semi-definite, quaternion unit norm) and check them with `assert` after every `predict` and `updatePosition`. Replace every explicit matrix inverse in your code with a decomposition-based solve, or justify the ones you keep.

### Deliverables
- [ ] `optim.py`, `eskf_2d.py`, `eskf.cpp` merged through PR review
- [ ] Executed notebook with the comparison and the poor-start experiment
- [ ] Outage plot (error + 3σ) and a one-page note explaining the behaviour during and after the outage
- [ ] One paper summary

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m2`).
- The outage note states the error growth over the outage with numbers, and says whether the error stays inside the 3σ bound.
- Every number is tied to a commit, the `prepare` options and the drive id.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your plots, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review. Present your paper summary at paper club.

## Where to look if stuck
- Error-state Jacobians F and noise matrix Q: Solà, Section 5.4 "System kinematics in discrete time".
- Update, injection and reset: Solà, Sections 6.1–6.3.
- Units of the noise parameters and how they scale with the sample rate: Kalibr wiki "Additive White Noise".
- Real-data runs: check the IMU rate in `imu.csv`. The synced OXTS is 10 Hz; see `--extract-oxts` and `prepare --imu-oxts` in [`data/README.md`](../../data/README.md).
- What NEES is and how to read it: Labbe notebook 08-Designing-Kalman-Filters.
- Gauss-Newton derivation: Barfoot, "Nonlinear Non-Gaussian Estimation", batch estimation section.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
