# Module 8: Research skills mini-project
**Tentative effort:** remainder of the program · **Phase:** D — Production & research

## Goal
Practise scoping, running and communicating a small research question end to end, on the pipeline you built, before the larger applied project.

**Builds on:** everything: the pipeline (modules 1–6), the evaluation tools (modules 5–6) and Argo (module 7). **Used by:** the applied project.

---

## Segment 1 — Learn

### Learn from
- [Keshav — How to Read a Paper](http://ccr.sigcomm.org/online/files/p83-keshavA.pdf) — paper — Section 3 "Doing a literature survey"
- [Simon Peyton Jones — How to Write a Great Research Paper](https://simon.peytonjones.org/great-research-paper/) — talk — slides (PDF) and the [video](https://www.youtube.com/watch?v=VK51E3gHENc): the seven suggestions
- [Statistics Done Wrong](https://www.statisticsdonewrong.com/) — book (free online) — chapters "Statistical power and underpowered statistics", "Pseudoreplication: choose your data wisely", "When differences in significance aren't significant differences"
- [Sandve et al. — Ten Simple Rules for Reproducible Computational Research](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285) — paper — Rules 1, 3, 4, 6 and 9
- [`templates/tech_report.md`](../../templates/tech_report.md) and [`templates/rubric.md`](../../templates/rubric.md) — how your report is judged
- Internal: two past tech reports from the team (ask your mentor) as examples of the expected format. If none are available yet, the template sections and the rubric are the format; do not wait for examples to start.

## Segment 2 — Self-check 1: Readiness
Answer the Readiness part of [`quiz/self_check.md`](quiz/self_check.md), then grade yourself.

## Segment 3 — Build

### Candidate questions
Pick one (or propose your own and get it approved). Each one can be answered with the pipeline and data you already have, plus small `prepare` extensions where a question says so (question 9 also needs the drive's camera images).

1. Does weighting GNSS factors by a time-varying fix quality reduce drift when GNSS degrades? Extend `prepare` to simulate degraded segments (larger noise, with the larger σ reported in `sx,sy,sz`) and compare a constant σ against the reported σ.
2. How does the keyframe policy (every scan vs every N metres) trade accuracy against optimization time?
3. How does the map voxel size affect odometry drift and runtime? Is there a sweet spot?
4. Does deskewing reduce odometry error on KITTI raw scans, and does the sweep-timing convention matter?
5. How much GNSS outage can the graph (odometry + IMU) bridge before the error exceeds 2 m?
6. Does the Scan Context distance threshold trade loop recall against false loops, and does the robust kernel make high recall safe?
7. How sensitive is the ESKF to a mis-specified IMU noise density (×0.1 … ×10)? Is the NEES a reliable detector?
8. Does a robust kernel on GNSS factors help when you inject multipath-like outliers in `prepare`?
9. Does camera place recognition with a learned visual vocabulary (ORB descriptors from module 4b, a vocabulary built by k-means, bag-of-words retrieval) find the same loops as Scan Context on drive 0027, and where does each fail? Decide how you cluster binary ORB descriptors (Hamming vs Euclidean) and justify it. Fetch the images with `data/download.py --camera`; see Stachniss [Bag of Visual Words](https://www.ipb.uni-bonn.de/html/teaching/photo12-2021/2021-pho2-12-bag-of-visual-words.pptx.pdf).

### Assignment
1. **Scope.** Write a one-paragraph plan: question, hypothesis, metrics, data, and a scope cut (what you will not do). Time-box it with your mentor (typically 1–2 weeks).
2. **Run.** Run the experiments on at least two full drives, tracked so every number is tied to a commit, flags, drive and seed. Use Argo for sweeps.
3. **Write.** Write a 2–3 page report at `modules/m8_research_mini_project/report/report.md` from [`templates/tech_report.md`](../../templates/tech_report.md), with figures in the same folder.
4. **Present.** Present it to the team (10 minutes plus questions).

### Deliverables
- [ ] Approved one-paragraph plan
- [ ] `report/report.md` with figures, merged through review
- [ ] Presentation to the team

### Acceptance criteria
- Tests in `tests/` pass (`python tools/module_tests.py m8`): the report has every template section, a commit hash, no leftover placeholders, existing figures, and a 2–3 page length.
- The report is judged with [`templates/rubric.md`](../../templates/rubric.md): correctness, evaluation rigour, code quality, communication, independence.
- **Exit criteria for the training** (the same list is in the mentors' grading guide):
  - [ ] All module deliverables merged (checklists complete).
  - [ ] The pipeline runs end to end on Argo over ≥ 3 sequences, with the summary published.
  - [ ] CI regression gate enabled and green on main.
  - [ ] One merged PR to the production codebase.
  - [ ] Mini-project report reviewed with the rubric (pass rule in `templates/rubric.md`) and presented.
  - [ ] Phase gate D taken and discussed with the mentor.
  - [ ] Mentor sign-off.

## Segment 4 — Self-check 2: Apply
Answer the Apply part of [`quiz/self_check.md`](quiz/self_check.md) about your own project.

## Segment 5 — Review
Tick [`CHECKLIST.md`](CHECKLIST.md), open the PR, present, and request the final sign-off.

## Where to look if stuck
- Finding related work fast: Keshav, Section 3.
- Structuring the story: Peyton Jones, suggestions 2–4 (key idea, story, contributions).
- Statistics of your results: your module 6 evaluation tools and the bootstrap CIs.
- Scope creep: re-read your scope cut; ask your mentor before adding anything.
- Stuck for ~2 hours? Write down what you tried and ask your mentor.
