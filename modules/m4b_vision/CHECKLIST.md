# Module 4b — Checklist

- [ ] Self-check 1 (Readiness) done — score: ___ / 11
- [ ] `camera.cpp` complete; `ctest --test-dir build -L '^m4b$'` passes locally
- [ ] `vision.py` complete (no OpenCV inside); compared with `cv2.findFundamentalMat` on real matches
- [ ] LiDAR overlays: three frames + one wrong calibration, each with a one-line observation
- [ ] `mono_vo.py` complete; error plots and trajectory on the sample and one full drive
- [ ] Worst VO steps named and inspected (inlier matches drawn)
- [ ] `two_view_ba.py` complete; before/after table on ≥ 5 pairs
- [ ] `stereo_depth.py` complete; depth error vs depth plot with an explanation of its shape
- [ ] Camera frame axes added to `CONVENTIONS.md`
- [ ] `python tools/module_tests.py m4b` passes
- [ ] C++ focus: `projectCloud` copies nothing, reserves once, reuses `project`; runtime over 20 scans in the PR
- [ ] Self-check 2 (Apply) done — score: ___ / 7
- [ ] "Explain to your mentor" prompts prepared
- [ ] Glossary updated
- [ ] PR(s) opened and review requested
