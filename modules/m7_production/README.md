# Module 7: Productionizing the pipeline
**Tentative effort:** ~1 week · **Phase:** D — Production & research

## Goal
Make the pipeline reproducible, testable and scalable on the team's infrastructure: a pinned runtime image, an Argo workflow over many sequences, a CI regression gate, and one small real contribution to the production codebase.

---

## Segment 1 — Learn

### Learn from
- [Argo Workflows documentation](https://argo-workflows.readthedocs.io/en/latest/) — docs — Walk-through section
- [Argo — Loops](https://argo-workflows.readthedocs.io/en/latest/walk-through/loops/) — docs — `withItems` / `withParam` fan-out
- [Argo — Parameters](https://argo-workflows.readthedocs.io/en/latest/walk-through/parameters/) — docs — whole page
- [Argo — Artifacts](https://argo-workflows.readthedocs.io/en/latest/walk-through/artifacts/) — docs — whole page
- [argo lint](https://argo-workflows.readthedocs.io/en/latest/cli/argo_lint/) — docs — options, incl. `--offline`
- [DVC documentation](https://dvc.org/doc) — docs — Get Started: data and model versioning (or the team's tool)
- [Software Engineering at Google — Ch. 11 "Testing Overview"](https://abseil.io/resources/swe-book/html/ch11.html) — book (free online) — Ch. 11, then Ch. 12 "Unit Testing" and Ch. 14 "Larger Testing"
- [Google Testing Blog](https://testing.googleblog.com/) — docs — "Testing on the Toilet" posts on flaky tests and test sizes
- [GitHub Actions documentation](https://docs.github.com/en/actions) — docs — workflow syntax, containers in jobs, caching
- [MIT Missing Semester](https://missing.csail.mit.edu/2020/) — course — lecture 8 "Metaprogramming" (build systems, dependency pinning)
- Internal: the team's production codebase and contribution guide (ask your mentor for links)

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before starting, then grade yourself.

## Segment 3 — Build

### Assignment
1. **Runtime image.** Complete [`infra/docker/pipeline.Dockerfile`](../../infra/docker/pipeline.Dockerfile): pinned base (the dev image tag), Release build of the apps, `slampipe` installed, non-root user.
2. **Argo workflow.** Complete [`infra/argo/pipeline-workflow.yaml`](../../infra/argo/pipeline-workflow.yaml): fan out over a `sequences` parameter, run and evaluate each sequence, then publish a summary. Measure one run to set resource requests. Submit it on the team cluster for at least 3 sequences.
3. **Regression gate.** Implement `check` in [`pipeline/python/slampipe/gate.py`](../../pipeline/python/slampipe/gate.py). Complete [`starter/regression.yml`](starter/regression.yml) and enable it as `.github/workflows/regression.yml`. Show that a deliberately degraded change fails it. The baseline lives in [`baseline.json`](baseline.json).
4. **Data versioning.** Put the prepared sequences you use under the team's data-versioning tool (DVC by default) and reference the version in your reports.
5. **Production PR.** Read through the team's production codebase with your mentor and submit one small real fix or improvement through the normal review process.

### Deliverables
- [ ] Runtime image and Argo workflow merged; a successful workflow run over ≥ 3 sequences with its summary
- [ ] CI regression gate enabled; a PR showing it fail on a degraded change
- [ ] Data version recorded for the sequences
- [ ] One merged PR to the production codebase

### Acceptance criteria
- Tests in `tests/` pass in CI (`python tools/module_tests.py m7`), including `argo lint --offline`.
- Images and actions are pinned; nothing uses `:latest`.
- The gate tolerance is justified from run-to-run variation, not guessed.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md), and prepare the "Explain to your mentor" prompts.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open the PRs and request review.

## Where to look if stuck
- Fan-out and passing parameters between steps: Argo "Loops" and "Parameters".
- Linting without a cluster: `argo lint --offline`.
- Containers and caching in CI: GitHub Actions docs, "Running jobs in a container" and "Caching dependencies".
- Choosing a tolerance: run the pipeline several times, or with several `prepare` seeds, and look at the spread.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
