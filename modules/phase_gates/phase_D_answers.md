# Phase gate D — answers

**PD-01.** Base image tag/digest, dependency versions, code commit, configs, dataset version, random seeds. See: missing_semester — lecture 8 "Metaprogramming"
**PD-02.** Workflow parallelism, cluster capacity, pending pods, shared storage throughput. See: argo_loops — whole page
**PD-03.** Output artifacts (artifact repository) or a shared volume read by the summary step. See: argo_artifacts — whole page
**PD-04.** A flaky/non-deterministic pipeline or tolerance too tight; a changed base image or data. See: google_testing_blog — "Flaky Tests at Google and How We Mitigate Them"
**PD-05.** From the measured run-to-run (or seed-to-seed) spread, set above it but below meaningful regressions. See: swe_book_testing — Ch. 11 (test sizes and flakiness)
**PD-06.** Unit tests check behaviour of small pieces quickly; a benchmark checks end-to-end quality on data. See: swe_book_testing — Ch. 11 "Testing Overview"
**PD-07.** In the Setup section (`templates/tech_report.md`). See: sandve_reproducible — Rule 1 and Rule 9 "Connect Textual Statements to Underlying Results"
**PD-08.** It predicts an outcome that an experiment could contradict, e.g. "drift increases monotonically above 1 m voxels". See: spj_great_paper — "Identify your key idea"
**PD-09.** Inconclusive: the data are compatible with no effect or a negative one. See: statistics_done_wrong — "Statistical power and underpowered statistics"
**PD-10.** E.g. don't wait: write; identify your key idea; tell a story; nail your contributions; related work later; put readers first; listen to readers. See: spj_great_paper — slides
**PD-11.** Explicitly stating what you will not do; decide it in the plan, before running. See: spj_great_paper — "Nail your contributions"
**PD-12.** Drive id ↔ sample/accession id; seed ↔ random seeds of simulation/subsampling steps; commit ↔ pipeline version. See: dvc_docs — Get Started
