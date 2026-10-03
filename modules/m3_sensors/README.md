# Module 3: Sensors in depth
**Tentative effort:** ~1 week · **Phase:** B — Estimation & sensors

## Goal
Know how each sensor lies and how to correct for it: characterize IMU noise, understand GNSS error sources, deskew LiDAR scans, and measure what a clock offset between sensors does.

---

## Segment 1 — Learn

### Learn from
- [Kalibr wiki — IMU Noise Model](https://github.com/ethz-asl/kalibr/wiki/IMU-Noise-Model) — docs — "Additive White Noise", "Bias", "How to Obtain the Parameters for your IMU" → "From the Allan standard deviation (AD)"
- [ESA — GNSS Data Processing, Vol. I](https://gssc.esa.int/navipedia/GNSS_Book/ESA_GNSS-Book_TM-23_Vol_I.pdf) — book (free PDF) — Ch. 1.1 "An Intuitive Approach to GNSS Positioning"; Ch. 4.2 "Measurement Features and Noise"; Ch. 5.4 "Atmospheric Effects Modelling"
- [ESA Navipedia — GNSS Measurements Modelling](https://gssc.esa.int/navipedia/index.php/GNSS_Measurements_Modelling) — docs — error budget
- [ESA Navipedia — Multipath](https://gssc.esa.int/navipedia/index.php/Multipath) — docs — whole page
- [ESA Navipedia — RTK Fundamentals](https://gssc.esa.int/navipedia/index.php/RTK_Fundamentals) and [Precise Point Positioning](https://gssc.esa.int/navipedia/index.php/Precise_Point_Positioning) — docs — whole pages
- [Coursera — State Estimation and Localization for Self-Driving Cars](https://www.coursera.org/learn/state-estimation-localization-self-driving-cars) — course — Module 3 "GNSS/INS Sensing for Pose Estimation" and Module 4 "LIDAR Sensing"
- [LiDAR Odometry — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=9FhKgAEQTOg) — video — whole video (scanning model, motion distortion)
- [Dellenbach et al. — CT-ICP](https://arxiv.org/abs/2109.12979) — paper — Section V "Experiments", the paragraph on KITTI-corrected vs KITTI-raw (only that part)

Note: the Stanford "GPS: An Introduction to Satellite Navigation" course from the original curriculum is no longer offered on Coursera; the ESA book replaces it.

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Allan variance.** Implement `allan_deviation` and `fit_noise_parameters` in [`pipeline/python/slampipe/allan.py`](../../pipeline/python/slampipe/allan.py). Complete [`starter/allan_static.py`](starter/allan_static.py) and run it on a **static** IMU recording of at least 2 hours: the public 16-hour [MILUV](https://doi.org/10.25452/figshare.plus.28386041.v1) recording (`python data/download.py --static-imu`, ~1.7 GB download, ~11 GB temporary disk), or one from the team's hardware if your mentor provides it. Compare your parameters with the datasheet and, for MILUV, with the authors' own results (downloaded next to the data); only open those after you have your numbers.
2. **Deskew.** Implement `poseAt`, `propagateImu` and `deskew` in [`pipeline/src/sensors/deskew.cpp`](../../pipeline/src/sensors/deskew.cpp).
3. **Before/after.** `data/samples/skewed/scan.npz` holds a KITTI raw scan with strong synthetic distortion added (a 45°/s turn), so the effect is easy to see and to check against a reference. Deskew it with the `deskew_scan` tool (helpers in [`starter/skew_tools.py`](starter/skew_tools.py)) and plot before/after top-down views. Then repeat on a real turning segment of a full drive: KITTI raw scans are *not* motion-compensated (the odometry-benchmark copies are), the per-point times must be derived from the azimuth, and the motion comes from your IMU propagation. Find out how the CT-ICP paper derives the per-point times.
4. **Time offset.** Complete [`starter/time_offset.py`](starter/time_offset.py): sweep an IMU–LiDAR clock offset from −20 ms to +20 ms and plot the deskew error against it.

### C++ focus: generic code and sanitizers on your own code
- [Back to Basics: Templates, part 1](https://www.youtube.com/watch?v=XN319NYEOcE) and [part 2](https://www.youtube.com/watch?v=2Y9XbltAfXs) — video
- [cppreference: std::lower_bound](https://en.cppreference.com/w/cpp/algorithm/lower_bound) — docs
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) — docs — "Usage"

Task: make `poseAt` O(log n) with a standard algorithm. Build the module 3 tests once with `-DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"` in a separate build directory, run them, and fix anything reported (module 0b explains the `setarch -R` workaround if ASan hangs).

### Deliverables
- [ ] `allan.py` and `deskew.cpp` merged through PR review
- [ ] Noise-parameter report: Allan plots, a table of N and K per axis, and the datasheet comparison
- [ ] Before/after deskew figure
- [ ] Short write-up of the time-offset experiment (error vs offset, and what offset you can tolerate for a given error budget)

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m3`).
- The noise report states the recording length and rate, and gives units for every parameter.
- The time-offset write-up gives a number (ms) for the tolerable offset and says how you derived it.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your plots, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review.

## Where to look if stuck
- Overlapping Allan deviation and how N and K appear on the log-log plot: Kalibr wiki, "From the Allan standard deviation (AD)".
- Before trusting any fit on the MILUV recording: derive the sample rate from the timestamps (not from a config file), check the units of every reference number you compare with, and look at the slope of each axis's curve before fitting a model to it.
- Which pose to interpolate and in which direction to apply it: the transform chain in your `CONVENTIONS.md` and module 1's `interpolate`.
- Per-point time in a spinning LiDAR: the "LiDAR Odometry — 5 Minutes" video; KISS-ICP paper, Step 1 "Motion Prediction and Scan Deskewing".
- GNSS error magnitudes: ESA book Ch. 4.2 and Navipedia "GNSS Measurements Modelling".
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
