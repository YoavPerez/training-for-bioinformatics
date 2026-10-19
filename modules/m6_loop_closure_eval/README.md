# Module 6: Loop closure, maps, evaluation
**Tentative effort:** ~1–1.5 weeks (plus several hours of unattended compute for the ablation) · **Phase:** C — Mapping core

## Goal
Close loops reliably, survive wrong loop closures, and evaluate the pipeline with statistical rigour: distributions, confidence intervals and ablations instead of single numbers.

**Builds on:** the factor graph and `ate_errors`/`bootstrap_ci` (module 5), ICP (module 4). **Used by:** the regression gate (module 7) and every number in the mini-project (module 8).

---

## Segment 1 — Learn

### Learn from
- [Kim & Kim — Scan Context (IROS 2018)](https://gisbi-kim.github.io/publications/gkim-2018-iros.pdf) — paper — Section III-A "Scan Context", III-B "Similarity Score", III-C "Two-phase Search"
- [Scan Context repository](https://github.com/gisbi-kim/scancontext) — repo — README; `cpp/module/Scancontext` (read, do not copy)
- [Robust Least Squares for Graph-Based SLAM (Cyrill Stachniss)](https://www.youtube.com/watch?v=z60RbiY18I8) — video — whole lecture (false loops, robust kernels)
- [GTSAM — Robust noise model](https://gtsam.org/2019/09/20/robust-noise-model.html) — docs — whole post
- [GTSAM documentation](https://borglab.github.io/gtsam/) — docs — noise models
- [evo](https://github.com/MichaelGrupp/evo) — repo — README and notebooks (metrics API)
- [evo wiki — Metrics](https://github.com/MichaelGrupp/evo/wiki/Metrics) — docs — "evo_ape", "evo_rpe"
- [KITTI odometry benchmark](https://www.cvlibs.net/datasets/kitti/eval_odometry.php) — docs — how translational (%) and rotational (deg/m) drift are defined
- Maps: [Hornung et al. — OctoMap](https://www.arminhornung.de/Research/pub/hornung13auro.pdf) — paper — Section "OctoMap Mapping Framework" (occupancy, log-odds, clamping); [Oleynikova et al. — Voxblox](https://arxiv.org/abs/1611.03631) — paper — Sections I "Introduction" and IV "TSDF Construction"

Optional, learned place recognition: [PointNetVLAD](https://arxiv.org/abs/1804.03492) and [OverlapTransformer](https://arxiv.org/abs/2203.03397) — abstract and introduction of each; for cameras, Stachniss [Bag of Visual Words](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-12-bag-of-visual-words.pptx.pdf) (slides).

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before coding, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Place recognition.** Implement `makeScanContext`, `scanContextDistance` and `verifyLoop` (re-using your module 4 ICP) in [`pipeline/src/loop/scan_context.cpp`](../../pipeline/src/loop/scan_context.cpp). `LoopDetector` is provided.
2. **Loop factor.** Implement `GraphBuilder::addLoop` with a robust kernel. Choose the kernel **and its width** by experiment: run `run_pipeline --false-loop i j` with at least two kernels and at least two values of `--loop-kernel-width` (in σ; see `graph_builder.hpp`) and keep the evidence. A false loop must be rejected, and a true loop with several metres of drift must still close (`tests/test_false_loop.cpp`). Set `kLoopKernelWidth` in `graph_builder.hpp` to the width you chose.
3. **Evaluation.** Implement `rpe_errors` in [`pipeline/python/slampipe/evaluation.py`](../../pipeline/python/slampipe/evaluation.py) on top of evo (`ate_errors` and `bootstrap_ci` are from module 5).
4. **Loops on real data.** Run `run_pipeline --loops` on a drive with revisits (`2011_09_30_drive_0027` = KITTI odometry 07; `2011_09_30_drive_0018` = 05), with and without GNSS (`--no-gnss`). `<out>/loops.csv` lists every Scan Context candidate and whether verification accepted it. Plot the accepted and rejected loops on the trajectory, and compare the ATE with and without `--loops`.
5. **Ablation.** Complete [`starter/ablation.py`](starter/ablation.py): GNSS, loop closure and deskew each on/off, across at least two drives. Report error distributions and confidence intervals. For the GNSS on/off rows, report ATE both aligned and unaligned (`evaluate(..., align=False)` / `--no-align`). The simulated GNSS depends on `prepare --seed`: prepare each drive with at least 5 seeds, run the GNSS-on combinations once per seed, and report the spread across seeds (mean ± std and min–max of the per-run RMSE) next to the per-pose CI. A per-pose bootstrap does not include seed variance. The `--deskew` option in `run_pipeline` contains a documented assumption about the LiDAR sweep; check whether it holds, using your data. Budget: about 24 runs per drive; on one core a `--loops` run of 0018 alone can take over half an hour. The runs are independent: use `ablation.py --jobs N`, and re-running with the same `--out` skips the runs that already finished.
6. **Map.** On drive 0027, use one `run_pipeline --no-gnss --loops` run (every scan a keyframe). For each scan k, transform `velodyne_points/data/<k>.bin` into the world (local ENU) frame with row k of `odometry.tum`, then with row k of `optimized.tum`. The TUM poses are body/IMU poses, not LiDAR poses: see the header comment of `run_pipeline.cpp`, `<prep>/T_imu_lidar.txt` and the frame names in `CONVENTIONS.md`. Downsample each scan to 0.2 m voxels before accumulating (e.g. Open3D `voxel_down_sample`), then the map again at 0.2 m. Crop a 60 m × 60 m box around one accepted loop (query and match frames from `loops.csv`), 0.5–3 m above the road. Plot both maps from above at the same extent, coloured by pass (first pass vs revisit). Done = two PNGs plus one number per map that shows the change, e.g. the median distance from revisit points to the nearest first-pass point, or the number of occupied 0.2 m cells in the box.

### C++ focus: error handling
- [cppreference: std::optional](https://en.cppreference.com/w/cpp/utility/optional) — docs
- [LearnCpp](https://www.learncpp.com/) — book — Ch. 27 "Exceptions"
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "E: Error handling"

Task: for every failure path in your place-recognition and loop-verification code, decide between an expected "no result" (`std::optional`), an exception (broken precondition) and an `assert` (programming error). List the decisions in your PR.

### Deliverables
- [ ] Scan Context, `verifyLoop`, `addLoop`, `kLoopKernelWidth` and `rpe_errors` merged through PR review
- [ ] False-loop experiment: trajectories and ATE for each kernel and width you tried
- [ ] Evaluation report: ATE/RPE distributions with CIs per sequence, the ablation table, and honest failure cases
- [ ] Map figure: odometry vs optimized poses near a loop closure, with the number you used to compare them

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m6`).
- Every number in the report is tied to a commit, a config/flags, a drive and the `prepare` seed.
- Conclusions about a component are only drawn when the CIs support them; conclusions about GNSS also need the spread across ≥ 5 `prepare` seeds.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) using your report, and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open a PR and request review.

## Where to look if stuck
- What a Scan Context bin stores and how the column shift works: the paper, Sections III-A and III-B. Check the sign of your shift with a scan you rotated yourself.
- Why one kernel rejects a wrong loop and another only dampens it: the robust least-squares lecture; compare the influence (ψ) functions in the GTSAM post. What the width is measured against: the comment on `addLoop` in `graph_builder.hpp`.
- Frame and timestamps of the TUM poses, and the `loops.csv` columns: header comment of `run_pipeline.cpp`.
- ATE alignment, time association and RPE deltas: evo wiki "Metrics" page, sections "evo_ape", "evo_rpe" and "Alignment".
- Confidence intervals by resampling: think of it as a bootstrap over poses; Labbe (module 2) and any statistics text you know from your degree.
- Compute budget: one `run_pipeline --loops` run takes about 3–15 minutes on drive 0027 and several times that on drive 0018, depending on the machine; the full ablation on two drives with 5 seeds is many hours of serial compute. Start it early and unattended (or on Argo, module 7); use `--max-frames` for dry runs.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
