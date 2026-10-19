# Module 7 — Self-check answers

Answers and pointers only. If you missed one, read the pointer, not just the answer.

## Self-check 1 — Readiness
**M7-R01.** `withItems`: a literal list in the spec; `withParam`: a JSON list from a parameter or a previous step's output. See: argo_loops — whole page
**M7-R02.** Through artifacts (an artifact repository) or a shared volume. See: argo_artifacts — whole page
**M7-R03.** The tag can move to a different image, so the same workflow runs different code. See: missing_semester — lecture 8 "Metaprogramming" (dependency management)
**M7-R04.** Size = resources the test may use (single process / single machine / anything); a sample run is medium or large. See: swe_book_testing — Ch. 11, "Test Size"
**M7-R05.** E.g. multithreading order, unseeded randomness, floating-point reduction order, unordered containers. See: swe_book_testing — Ch. 11 (flakiness)
**M7-R06.** Versioning large binary data with pointers and caches, tied to code commits. See: dvc_docs — Get Started
**M7-R07.** It passes and fails without code changes; people learn to ignore it. See: google_testing_blog — "Flaky Tests at Google and How We Mitigate Them"
**M7-R08.** Schema and template/parameter references; not cluster-side issues (images, PVCs, RBAC). See: argo_lint — options

## Self-check 2 — Apply
**M7-A01.** Depends on your measurement (peak RSS and CPU time of one run). See: k8s_resources — "Requests and limits"
**M7-A02.** Depends on your runs; tolerance (relative to the baseline) above the observed spread. See: swe_book_testing — Ch. 14 "Larger Testing"
**M7-A03.** Depends on your cluster; limits are parallelism, node resources and shared storage. See: argo_loops — whole page
**M7-A04.** Depends on your PR. See: cpp_core_guidelines — sections used in review
**M7-A05.** A reviewed PR that changes `baseline.json` with evidence and an explanation. See: swe_book_testing — Ch. 14 "Larger Testing"
