# Module 6 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M6-R01.** What does one bin of a Scan Context descriptor store, and how are the bins arranged?

**M6-R02.** How does Scan Context achieve invariance to the sensor's heading at a revisit?

**M6-R03.** Why do loop candidates need geometric verification before they enter the graph?

**M6-R04.** Huber vs Cauchy (or Geman-McClure): which one can effectively ignore a grossly wrong constraint, and why?

**M6-R05.** ATE vs RPE: which one measures global consistency, and which one local drift?

**M6-R06.** Why is a trajectory aligned (SE(3) or Sim(3)) before computing ATE, and when must you not align?

**M6-R07.** How is the KITTI translational error defined (units and segment lengths)?

**M6-R08.** You have 3 runs per configuration. Why is a single mean ATE not enough to claim configuration A beats B?

**M6-R09.** SeqSLAM-style place recognition matches *sequences* of descriptors. Which bioinformatics method does that resemble, and what is gained over single-scan matching?

## Self-check 2 — Apply

**M6-A01.** Which kernel did you choose for `addLoop`, and what did the false-loop experiment show for each kernel you tried?

**M6-A02.** How many loops did your pipeline detect and accept on sequence 07 (drive 0027)? How many candidates did verification reject?

**M6-A03.** In your ablation, which component changed ATE the most, and was the difference outside the CIs?

**M6-A04.** Did deskewing help on the full drives? What does that tell you about the sweep assumption in `run_pipeline`?

**M6-A05.** Name one failure case you found and the evidence for its cause.

## Explain to your mentor
- Walk through your evaluation report as if presenting it to the team: question, setup, results with uncertainty, failure cases.
- Show the false-loop experiment and explain the shape of the kernels' influence functions.
