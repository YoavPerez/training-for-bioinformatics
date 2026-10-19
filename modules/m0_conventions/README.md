# Module 0: Diagnostic and team conventions
**Tentative effort:** a few days · **Phase:** A — Foundations

## Goal
Calibrate where you start, and agree on the conventions (frames, rotations, units, time) that prevent most frame and timestamp bugs later.

**Builds on:** nothing. **Used by:** every module; `CONVENTIONS.md` names every frame, transform and timestamp from module 1 on.

---

## Segment 1 — Learn

### Learn from
- [`GLOSSARY.md`](../../GLOSSARY.md) — the "Coming from bioinformatics" table: which SLAM tools you already know under another name. Come back to it in every module.
- [MIT Missing Semester (2020)](https://missing.csail.mit.edu/2020/) — course — lectures 1 "Course Overview + The Shell", 6 "Version Control (Git)", 7 "Debugging and Profiling"
- [3Blue1Brown — Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) — video — chapters 3–6, 13, 14 (after the diagnostic quiz, which calibrates what you already know)
- [KITTI raw data](https://www.cvlibs.net/datasets/kitti/raw_data.php) — dataset docs — the devkit readme's "Coordinate Systems" section (axes of the IMU, velodyne and cameras) and the OXTS field list (units)
- [ESA Navipedia — Transformations between ECEF and ENU coordinates](https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates) — docs — what a local ENU frame is
- [Introduction to SLAM (Cyrill Stachniss)](https://www.youtube.com/watch?v=0I30M6yTklo) — video — the difference between drifting odometry and a globally consistent map
- [Solà — Quaternion kinematics for the ESKF](https://arxiv.org/abs/1711.02508) — paper — Section 3 "Quaternion conventions" only
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "R: Resource management", "F.call: Parameter passing" (reference for code review)
- [Eigen quick reference](https://eigen.tuxfamily.org/dox/group__QuickRefPage.html) — docs — matrix types, coefficient access, geometry

## Segment 2 — Self-check 1: Readiness
1. Take the **diagnostic quiz** [`quiz.md`](quiz.md) on your own, time-boxed to 90 minutes, without searching. Hand your answers to your mentor; this one is for calibration and is graded by the mentor.
2. Then answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) and grade yourself with [`quiz/self_check_answers.md`](quiz/self_check_answers.md).

## Segment 3 — Build

### Assignment
1. **Conventions.** Complete [`CONVENTIONS.md`](../../CONVENTIONS.md) together with your mentor: frame names, `T_a_b` meaning and composition rule, quaternion convention (Hamilton/JPL) and storage order, units, timestamp source and epoch, geodesy choices. Every blank (`______`) must be filled, and the status must be marked as reviewed.
2. **Environment.** Build the dev container (`infra/docker/Dockerfile`, or *Reopen in Container*), fetch the sample (`python data/download.py --sample`) and build the pipeline (see the top-level README).
3. **Replay.** Complete `summarize()` and `main()` in [`starter/replay.py`](starter/replay.py): replay the sample drive and report the number of scans, the duration, and the distance travelled (from the OXTS forward velocity). Plot speed over time.
4. Run `bash modules/m0_conventions/tests/check_container.sh` once on your machine to check the image builds and loads the sample.

### Deliverables
- [ ] Diagnostic quiz handed to mentor
- [ ] `CONVENTIONS.md` completed and reviewed (PR)
- [ ] `starter/replay.py` completed, with the speed plot attached to the PR

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m0`).
- `CONVENTIONS.md` has no blanks left, and the mentor has ticked "reviewed".
- You can explain `T_world_lidar` vs `T_lidar_world` without hesitation.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) against your own replay output, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review.

## Where to look if stuck
- Frame names and axes: the KITTI devkit readme, "Coordinate Systems" (mounting heights: Geiger et al. 2013, Fig. 3 "Sensor Setup") and Navipedia's ENU page.
- Quaternion conventions: Solà, Section 3 (the comparison table).
- OXTS fields (`vf`, timestamps): the KITTI raw devkit readme, linked from the [KITTI raw page](https://www.cvlibs.net/datasets/kitti/raw_data.php).
- Docker or shell trouble: Missing Semester lecture 1.
- `docker build` stalls on downloads (apt "Connection failed", hanging `pip`): common on WSL or behind a VPN, where the network MTU is below Docker's 1500. Build with `docker build --network host …` (and run containers with `--network host`).
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
