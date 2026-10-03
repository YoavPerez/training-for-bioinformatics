# Module 4: Point clouds and registration
**Tentative effort:** ~1 week · **Phase:** C — Mapping core · **Mid-program checkpoint**

## Goal
Implement point-to-plane ICP, benchmark it honestly against established libraries (accuracy, runtime, convergence basin), and make one measured performance optimization.

---

## Segment 1 — Learn

### Learn from
- [ICP & Point Cloud Registration — Part 1: Known Data Association & SVD](https://www.youtube.com/watch?v=dhzLQfDBx2Q) — video (Cyrill Stachniss, 2021) — whole lecture
- [ICP & Point Cloud Registration — Part 2: Unknown Data Association](https://www.youtube.com/watch?v=ktRqKxddjJk) — video — whole lecture
- [ICP & Point Cloud Registration — Part 3: Non-linear Least Squares](https://www.youtube.com/watch?v=CJE59i8oxIE) — video — whole lecture (point-to-plane linearization, robust kernels)
- [Point-to-Plane and Generalized ICP — 5 Minutes with Cyrill](https://www.youtube.com/watch?v=2hC9IG6MFD0) — video
- [Open3D — ICP registration](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) — docs — "Point-to-point ICP", "Point-to-plane ICP" (the baseline API)
- [KISS-ICP paper](https://arxiv.org/abs/2209.15397) — paper — "KISS-ICP – Keep It Small and Simple", Steps 1–4 and "Adaptive Threshold for Data Association"
- [KISS-ICP repository](https://github.com/PRBonn/kiss-icp) — repo — `cpp/kiss_icp/core/` (read, do not copy)
- [small_gicp](https://github.com/koide3/small_gicp) — repo — README "Python" usage and "Benchmark" (benchmark target)
- [Brendan Gregg — Linux perf Examples](https://www.brendangregg.com/perf.html) — docs — sections 3 "One-Liners", 7 "Examples", 8 "Visualizations" (flame graphs)
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "Per: Performance" and "F.call: Parameter passing"

Provided library: [nanoflann](https://github.com/jlblancoc/nanoflann) behind `pipeline/include/slam/registration/kdtree.hpp`.

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

### Assignment
1. **ICP.** Implement `icpPointToPlane` in [`pipeline/src/registration/icp.cpp`](../../pipeline/src/registration/icp.cpp), including the optional Huber kernel (`IcpConfig::huber_threshold`). The KD-tree, voxel downsampling and normal estimation are provided.
2. **Benchmark.** Complete `gt_relative`, `initial_error_sweep` and `main` in [`starter/benchmark.py`](starter/benchmark.py). Compare your ICP with Open3D and small_gicp on at least 50 consecutive pairs from a full drive: translation/rotation error distributions, runtime, and success rate against initial error (the convergence basin).
3. **Profile and optimize.** Profile `icp_register` with `perf` (build `RelWithDebInfo`), make a flame graph, pick **one** hotspot, change it, and measure before/after on the same pairs. The optimization must not change the accuracy beyond noise.

### C++ focus: performance-aware C++
- [Compiler Explorer](https://godbolt.org/) — tool — compare your inner loop at `-O0` and `-O2`
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "Per: Performance"

Task: the ICP inner loop must not allocate. Reuse buffers across iterations (`reserve`, member scratch space), pass large objects by reference, and show with your profile that allocation is not a hotspot.

### Deliverables
- [ ] ICP merged through PR review
- [ ] Benchmark report: error distributions per method, runtime table, convergence-basin plot
- [ ] Profiling before/after: flame graphs and runtime distributions (not single numbers)
- [ ] Mid-program checkpoint with your mentor (see below)

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m4`).
- The benchmark compares methods on the same pairs and with the same downsampling, and says so.
- The optimization is backed by repeated measurements (e.g. median and spread over ≥ 20 runs).

### Mid-program checkpoint
After this module your mentor runs the mid-program checkpoint with you, using [`templates/rubric.md`](../../templates/rubric.md). Bring your benchmark report and your self-check scores from modules 0–4.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your benchmark, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review.

## Where to look if stuck
- Linearizing the point-to-plane residual and the 6×6 system: Stachniss ICP Part 3.
- Why point-to-plane converges faster than point-to-point, and what limits the basin: Stachniss ICP Part 2; Open3D tutorial "Point-to-plane ICP".
- Robust kernels and outlier rejection in practice: KISS-ICP paper, Step 4 and "Adaptive Threshold".
- A pose that slowly stops being a rotation after many updates: check what your update does to `R` over hundreds of iterations (module 1 tests give you the tools).
- Reading `perf report` and flame graphs: Gregg, sections 3 and 8.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
