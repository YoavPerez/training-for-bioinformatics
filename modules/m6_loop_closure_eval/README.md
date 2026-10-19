# Module 6: Loop closure, maps, evaluation
**Tentative effort:** ~1 week · **Phase:** C — Mapping core

## Goal
Close loops reliably, survive wrong loop closures, and evaluate the pipeline with statistical rigour: distributions, confidence intervals and ablations instead of single numbers.

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
2. **Loop factor.** Implement `GraphBuilder::addLoop` with a robust kernel. Choose the kernel by experiment: run `run_pipeline --false-loop i j` with at least two kernels and keep the evidence.
3. **Evaluation.** Implement `ate_errors`, `rpe_errors` and `bootstrap_ci` in [`pipeline/python/slampipe/evaluation.py`](../../pipeline/python/slampipe/evaluation.py) on top of evo.
4. **Loops on real data.** Run `run_pipeline --loops` on a drive with revisits (`2011_09_30_drive_0027` = KITTI odometry 07; `2011_09_30_drive_0018` = 05). Plot detected loops on the trajectory.
5. **Ablation.** Complete [`starter/ablation.py`](starter/ablation.py): GNSS, loop closure and deskew each on/off, across at least two drives. Report error distributions and confidence intervals. For the GNSS on/off rows, report ATE both aligned and unaligned (`evaluate(..., align=False)` / `--no-align`). The simulated GNSS depends on `prepare --seed`: prepare each drive with at least 5 seeds, run the GNSS-on combinations once per seed, and report the spread across seeds (mean ± std and min–max of the per-run RMSE) next to the per-pose CI. A per-pose bootstrap does not include seed variance. The `--deskew` option in `run_pipeline` contains a documented assumption about the LiDAR sweep; check whether it holds, using your data.
6. **Map.** On drive 0027, accumulate the scans into one point map in the world frame (voxel-downsampled, e.g. Open3D `voxel_down_sample`), once with the odometry poses and once with the optimized poses. Show the same area near a loop closure from above in both, and say what changed.

### C++ focus: error handling
- [cppreference: std::optional](https://en.cppreference.com/w/cpp/utility/optional) — docs
- [LearnCpp](https://www.learncpp.com/) — book — Ch. 27 "Exceptions"
- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) — docs — "E: Error handling"

Task: for every failure path in your place-recognition and loop-verification code, decide between an expected "no result" (`std::optional`), an exception (broken precondition) and an `assert` (programming error). List the decisions in your PR.

### Deliverables
- [ ] Scan Context, `verifyLoop`, `addLoop` and `evaluation.py` merged through PR review
- [ ] False-loop experiment: trajectories and ATE for each kernel you tried
- [ ] Evaluation report: ATE/RPE distributions with CIs per sequence, the ablation table, and honest failure cases
- [ ] Map figure: odometry vs optimized poses near a loop closure

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
- Why one kernel rejects a wrong loop and another only dampens it: the robust least-squares lecture; compare the influence (ψ) functions in the GTSAM post.
- ATE alignment, time association and RPE deltas: evo wiki "Metrics" and "Alignment".
- Confidence intervals by resampling: think of it as a bootstrap over poses; Labbe (module 2) and any statistics text you know from your degree.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
