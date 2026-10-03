# Module 4 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M4-R01.** With known correspondences, what is the closed-form way to find the best rigid transform between two point sets?

**M4-R02.** What are the two alternating steps of ICP?

**M4-R03.** Write the point-to-plane residual for a source point p (after transform) matched to target point q with normal n.

**M4-R04.** Why can point-to-plane ICP slide along a long flat wall or a tunnel? What is this property called?

**M4-R05.** What does a maximum correspondence distance trade off?

**M4-R06.** What is the effect of a Huber (or other robust) kernel on the normal equations?

**M4-R07.** KD-tree vs voxel hash map for nearest-neighbour search: name one advantage of each in a LiDAR odometry setting.

**M4-R08.** How does a sampling profiler like `perf record` decide where time is spent?

**M4-R09.** In this module's sequence-alignment analogy (from bioinformatics), what plays the role of the scoring function, and what plays the role of the alignment?

## Self-check 2 — Apply

**M4-A01.** In your benchmark, what were the median and 90th-percentile translation errors of your ICP, compared with Open3D and small_gicp?

**M4-A02.** Up to what initial translation error did your ICP converge reliably (success rate ≥ 90 %)? What limits it?

**M4-A03.** Which function was the top hotspot in your profile, and by how much did your optimization change the runtime distribution?

**M4-A04.** Repeated left-multiplication of `T` by small updates can slowly turn `T.linear()` into a non-rotation. How would you detect it in a test, and how do you prevent it?

**M4-A05.** Pick one pair where your ICP did clearly worse than small_gicp. What is special about the scene?

## Explain to your mentor
- Derive the 6×6 system for one point-to-plane correspondence on the whiteboard.
- Show your convergence-basin plot and explain the shape of each curve.
- Explain why your optimization did not change accuracy, with evidence.
