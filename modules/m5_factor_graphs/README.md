# Module 5: Odometry to SLAM with factor graphs
**Tentative effort:** ~1 week · **Phase:** C — Mapping core

## Goal
Build a back-end that fuses LiDAR odometry, IMU and GNSS in a factor graph, starting from an approved design doc, and compare it with the module 2 filter.

---

## Segment 1 — Learn

### Learn from
- [GTSAM — Factor Graphs and GTSAM: A Hands-on Introduction](https://gtsam.org/tutorials/intro.html) — docs — sections 1 "Factor Graphs", 2 "Modeling Robot Motion", 3 "Robot Localization", 4 "PoseSLAM"
- [Dellaert & Kaess — Factor Graphs for Robot Perception](https://www.cs.cmu.edu/~kaess/pub/Dellaert17fnt.pdf) — book (free PDF) — Ch. 1 "Introduction", Ch. 2 "Smoothing and Mapping", Ch. 6 "Optimization on Manifolds"
- [Graph-based SLAM using Pose Graphs (Cyrill Stachniss)](https://www.youtube.com/watch?v=uHbRKvD8TWg) — video — whole lecture
- [Forster et al. — On-Manifold Preintegration](https://arxiv.org/abs/1512.02363) — paper — Section V "IMU Model and Motion Integration", Section VI "IMU Preintegration on Manifold"
- [GTSAM — ImuFactor documentation](https://borglab.github.io/gtsam/imufactor/) — docs — whole page
- [GTSAM — ImuFactorsExample.cpp](https://github.com/borglab/gtsam/blob/develop/examples/ImuFactorsExample.cpp) — repo — parameter setup, preintegration loop
- [LiDAR Odometry — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=9FhKgAEQTOg) — video — scan-to-map odometry
- [KISS-ICP paper](https://arxiv.org/abs/2209.15397) — paper — Step 3 "Local Map and Correspondence Estimation"
- Code to read, not copy: [LIO-SAM](https://github.com/TixiaoShan/LIO-SAM) (`src/imuPreintegration.cpp`, `src/mapOptmization.cpp`) and [FAST-LIO](https://github.com/hku-mars/FAST_LIO) (`src/laserMapping.cpp`)

Optional: [Factor Graph — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=uuiaqGLFYa4); [Barfoot](http://asrl.utias.utoronto.ca/~tdb/bib/barfoot_ser24.pdf) "Matrix Lie Groups" (PDF p. 299).

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before writing the design doc, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Design doc first.** Copy [`templates/design_doc.md`](../../templates/design_doc.md) to `modules/m5_factor_graphs/design_doc.md` and fill it in: state, factors and noise models, keyframe policy, data flow, failure modes, evaluation plan. Get it reviewed by a senior; set **Status: approved** only after that review. No back-end code before approval.
2. **Odometry.** Implement `LidarOdometry::registerScan` in [`pipeline/src/odometry/lidar_odometry.cpp`](../../pipeline/src/odometry/lidar_odometry.cpp) on top of your module 4 ICP.
3. **Pose graph.** Implement `addOdometry`, `addGnss`, `addImu` and `optimize` in [`pipeline/src/backend/graph_builder.cpp`](../../pipeline/src/backend/graph_builder.cpp) (`addPrior` is a worked example). `addLoop` belongs to module 6.
4. **End to end.** Run `run_pipeline` (provided app) on at least two full drives (`data/README.md` suggests 0027 and 0018).
5. **Compare.** Complete [`starter/run_and_compare.py`](starter/run_and_compare.py): odometry only, + GNSS, + GNSS + IMU, and the module 2 ESKF, evaluated against the OXTS ground truth.

### C++ focus: API design and ownership
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "I: Interfaces" (I.27 Pimpl), "R: Resource management"
- [cppreference: std::unique_ptr](https://en.cppreference.com/w/cpp/memory/unique_ptr) — docs

Task: `graph_builder.hpp` hides every GTSAM type behind a `std::unique_ptr<Impl>`. In your PR, explain what that buys (compile times, dependencies, ABI) and why the destructor is defined in the `.cpp`. Your new code must have no owning raw pointers and const-correct accessors.

### Deliverables
- [ ] Approved design doc (merged before the back-end code)
- [ ] Odometry and graph builder merged through PR review
- [ ] Comparison table and trajectory plots on two sequences

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m5`). The sample-drive ATE thresholds come from a reference run (see `tests/test_m5.py`).
- The comparison reports distributions (RMSE, median, p95, CI), not single numbers, with the `prepare` options and seed.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your comparison, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open the PRs (design doc, odometry, graph) and request review.

## Where to look if stuck
- Factor types and noise models in GTSAM: the GTSAM intro sections 2–4; `ImuFactorsExample.cpp` for velocity and bias variables.
- Units of IMU covariances in GTSAM: the ImuFactor documentation (continuous-time densities, as in module 2).
- Odometry that drifts or diverges after many frames: re-read your module 4 self-check answer M4-A04; compare scan-to-map with scan-to-scan on the same frames.
- Frames: odometry comes out in the LiDAR frame, the graph state is the IMU/body frame. Write the conversion down with `CONVENTIONS.md` names.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
