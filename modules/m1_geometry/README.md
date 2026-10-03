# Module 1: 3D geometry, frames, geodesy
**Tentative effort:** ~1 week · **Phase:** A — Foundations

## Goal
Become fluent with rotations, rigid transforms and Earth-referenced coordinates, and put the first verified layer of the pipeline in place: the transform library and the GNSS → ENU conversion.

---

## Segment 1 — Learn

### Learn from
- [Modern Robotics (Lynch & Park)](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) — book + videos — Chapter 3 "Rigid-Body Motions", sections 3.1–3.3, with the Chapter 3 videos on the same page
- [Solà et al. — A micro Lie theory for state estimation in robotics](https://arxiv.org/abs/1812.01537) — paper — Sections II-A to II-E; Appendix B (SO(3)); Appendix D (SE(3))
- [Eigen — Space transformations tutorial](https://eigen.tuxfamily.org/dox/group__TutorialGeometry.html) — docs — "Transformation types"; Isometry vs Affine
- [Eigen — Geometry module](https://eigen.tuxfamily.org/dox/group__Geometry__Module.html) — docs — Quaternion class reference (storage order)
- [ROS 2 — About tf2](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Tf2.html) — docs — transform trees (concepts only; no ROS dependency in this program)
- [ESA Navipedia — Reference Frames in GNSS](https://gssc.esa.int/navipedia/index.php/Reference_Frames_in_GNSS) — docs — whole page
- [ESA Navipedia — Ellipsoidal and Cartesian Coordinates Conversion](https://gssc.esa.int/navipedia/index.php/Ellipsoidal_and_Cartesian_Coordinates_Conversion) — docs — "From Ellipsoidal to Cartesian coordinates"
- [ESA Navipedia — Transformations between ECEF and ENU](https://gssc.esa.int/navipedia/index.php/Transformations_between_ECEF_and_ENU_coordinates) — docs — whole page

Optional: [Modern Robotics PDF](https://hades.mech.northwestern.edu/images/7/7f/MR.pdf) Appendix B "Other Representations of Rotations"; [tf2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html).

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Transform library (C++).** Implement every `TODO(m1)` in [`pipeline/src/geometry/transform.cpp`](../../pipeline/src/geometry/transform.cpp) against the API in `pipeline/include/slam/geometry/transform.hpp`. Respect the "do not call" notes in the TODOs: the point is to implement them yourself.
2. **Geodesy (Python).** Implement `wgs84_to_ecef` and `ecef_to_enu` in [`pipeline/python/slampipe/geodesy.py`](../../pipeline/python/slampipe/geodesy.py).
3. **GNSS track.** Complete [`starter/gnss_to_enu.py`](starter/gnss_to_enu.py): convert the drive's OXTS fixes to ENU and plot east vs north.
4. **Scan in the world.** Complete [`starter/world_scan.py`](starter/world_scan.py): put one velodyne scan into the world frame using the OXTS pose and the IMU–velodyne calibration, and plot it top-down together with the GNSS track. Name every transform according to `CONVENTIONS.md`.
5. Run both scripts on a full drive (e.g. `2011_09_30_drive_0027`, see `data/README.md`) as well as on the sample.

### C++ focus: unit testing and passing Eigen types
- [GoogleTest Primer](https://google.github.io/googletest/primer.html) — docs — then "Advanced GoogleTest Topics" → value-parameterized tests (linked from the primer)
- [Eigen — Writing functions taking Eigen types as parameters](https://eigen.tuxfamily.org/dox/TopicFunctionTakingEigenTypes.html) and [Common pitfalls](https://eigen.tuxfamily.org/dox/TopicPitfalls.html) — docs — "Pass-by-value"

Task: add a value-parameterized test (`TEST_P`) to `tests/test_transform.cpp` that runs `so3Log`/`so3Exp` round trips near π about at least five different axes. No Eigen object may be passed by value in code you write.

### Deliverables
- [ ] Transform library and geodesy merged through PR review
- [ ] ENU trajectory plot (sample + one full drive)
- [ ] One rendered world-frame scan overlaid on the trajectory

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m1`): C++ `ctest -L m1` and pytest.
- Every transform variable in your scripts follows the `T_<to>_<from>` naming from `CONVENTIONS.md`.
- Plots have units and equal axis scaling.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your plots, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR (keep it small: library first, scripts in a second PR) and request review.

## Where to look if stuck
- Exp/log formulas and their small-angle behaviour: micro Lie theory, Appendix B-A.
- Behaviour of the log near π: Modern Robotics, Section 3.2.3.3 (matrix logarithm of rotations), special cases.
- SLERP and the sign of quaternions: [Solà — Quaternion kinematics for the ESKF](https://arxiv.org/abs/1711.02508), Sections 2.4 and 2.7.
- ECEF and ENU: the two Navipedia pages above. Check your result against points whose ECEF coordinates you can derive by hand (equator, poles).
- OXTS roll/pitch/yaw definitions and the calibration file format: the KITTI raw devkit readme ([KITTI raw page](https://www.cvlibs.net/datasets/kitti/raw_data.php)).
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
