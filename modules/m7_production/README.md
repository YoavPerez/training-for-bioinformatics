# Module 7: Productionizing the pipeline
**Tentative effort:** ~1–1.5 weeks; the production PR may run in parallel into module 8 (it is an exit criterion) · **Phase:** D — Production & research

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
- [Kubernetes — Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) — docs — "Requests and limits", "Resource units in Kubernetes"
- [DVC documentation](https://dvc.org/doc) — docs — Get Started: data and model versioning (or the team's tool)
- [Software Engineering at Google — Ch. 11 "Testing Overview"](https://abseil.io/resources/swe-book/html/ch11.html) — book (free online) — Ch. 11, then Ch. 12 "Unit Testing" and Ch. 14 "Larger Testing"
- [Google Testing Blog](https://testing.googleblog.com/) — docs — posts "Flaky Tests at Google and How We Mitigate Them" (2016/05) and "Test Sizes" (2010/12)
- [GitHub Actions documentation](https://docs.github.com/en/actions) — docs — workflow syntax, containers in jobs, caching
- [MIT Missing Semester](https://missing.csail.mit.edu/2020/) — course — lecture 8 "Metaprogramming" (build systems, dependency pinning)
- Internal: the team's production codebase and contribution guide (ask your mentor for links)

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md) before starting, then grade yourself.

## Segment 3 — Build

### The team provides
Ask your mentor for these before you start; you cannot create them yourself:
- the Argo namespace, the PVC name and its contents in the layout given in the header of [`infra/argo/pipeline-workflow.yaml`](../../infra/argo/pipeline-workflow.yaml), including the prepared `prep/<name>` folders;
- the artifact repository of the namespace (used by the summary step's output artifact);
- the registry for the runtime image, push access to it and the cluster's image pull secret;
- the data-versioning remote (DVC by default) and its credentials;
- links to the production codebase, its contribution guide and a candidate small fix.

### Assignment
1. **Runtime image.** Complete [`infra/docker/pipeline.Dockerfile`](../../infra/docker/pipeline.Dockerfile): pinned base (the dev image tag), Release build of the apps, `slampipe` installed, non-root user.
2. **Argo workflow.** Complete [`infra/argo/pipeline-workflow.yaml`](../../infra/argo/pipeline-workflow.yaml): fan out over a `sequences` parameter, run and evaluate each sequence, then publish a summary. Measure one run to set resource requests. Register the template on the team cluster (see the file header) and submit it for at least 3 sequences.
3. **Regression gate.** Implement `check` in [`pipeline/python/slampipe/gate.py`](../../pipeline/python/slampipe/gate.py). Complete [`starter/regression.yml`](starter/regression.yml) and enable it as `.github/workflows/regression.yml`. Show that a deliberately degraded change fails it. The shipped [`baseline.json`](baseline.json) is only an example from a reference pipeline: replace its numbers with those of **your own** pipeline on the CI sample, in a reviewed PR that says how you produced them; its `_note` states the `run_pipeline` flags and the `prepare` seed.
4. **Data versioning.** Put the prepared sequences you use under the team's data-versioning tool (DVC by default, `pip install dvc`; it is not in the dev image) with the remote from your mentor, and reference the version in your reports.
5. **Production PR.** Read through the team's production codebase with your mentor and submit one small real fix or improvement through the normal review process.

### C++ focus: static analysis and packaging
- [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) — docs — usage and the list of checks
- [An Introduction to Modern CMake](https://cliutils.gitlab.io/modern-cmake/) — book — "Exporting and Installing"

Task: run clang-tidy with the repository's `.clang-tidy` over the pipeline sources you wrote, and fix or justify every finding. Add `install()` rules for the apps so the runtime image can use `cmake --install` instead of copying binaries.

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
- Peak memory and CPU time of one run: `/usr/bin/time -v` ("Maximum resident set size"; Debian package `time`, not in the dev image) or Python's `resource.getrusage(resource.RUSAGE_CHILDREN)` after the run.
- Containers and caching in CI: GitHub Actions docs, "Running jobs in a container" and "Caching dependencies".
- Choosing a tolerance: the pipeline is deterministic for a fixed input, so repeated runs give identical numbers. The spread comes from the inputs: run with several `prepare` seeds (and, if you like, small configuration changes) and look at the spread of the gated metrics. Decide how a spread across seeds becomes a relative tolerance against your single-seed baseline, and write the rule and its numbers in the baseline PR.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
