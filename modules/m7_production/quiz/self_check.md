# Module 7 — Self-check

Answer every question in writing **before** opening the answers file. Then score yourself:

| Score (per section) | What to do |
|---|---|
| ≥ 80 % | Proceed. |
| 50–79 % | Revisit the pointers listed for the questions you missed, then re-answer them. |
| < 50 % | Revisit the pointers and talk to your mentor before moving on. |

## Self-check 1 — Readiness

**M7-R01.** What is the difference between `withItems` and `withParam` in Argo?

**M7-R02.** How do two Argo steps exchange a file?

**M7-R03.** Why should a container image never be referenced as `:latest` in a reproducible pipeline?

**M7-R04.** What does "test size" (small/medium/large) mean in Google's testing vocabulary, and where does a full pipeline run on sample data fit?

**M7-R05.** Name two sources of non-determinism in a SLAM pipeline run.

**M7-R06.** What problem does a data-versioning tool solve that git alone does not?

**M7-R07.** What makes a test "flaky", and why is a flaky regression gate worse than none?

**M7-R08.** What does `argo lint --offline` check, and what can it not check?

## Self-check 2 — Apply

**M7-A01.** What resource requests did you choose for `run-one`, and from which measurement?

**M7-A02.** What tolerance did you set for the gate, and what run-to-run spread justified it?

**M7-A03.** How long did your workflow take for N sequences, and what limited the parallel speed-up?

**M7-A04.** What did your production PR change, and what did the reviewer ask you to change?

**M7-A05.** If the baseline must be updated after a genuine improvement, what process do you follow?

## Explain to your mentor
- Walk through the life of one evaluation number: from the commit and data version to the CI gate and the Argo summary.
- Explain what would happen to your gate if someone changed the GNSS simulation seed in `prepare`.
