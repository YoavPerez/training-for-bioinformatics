# Phase gate C — Mapping core (modules 4–6)

Closed-book, 45 minutes. Score yourself with `phase_C_answers.md`.

**PC-01.** Derive the Jacobian row of a point-to-plane residual with respect to a left rotation perturbation w.

**PC-02.** Why does point-to-plane ICP usually converge in fewer iterations than point-to-point?

**PC-03.** Your ICP converges with a low RMSE but the pose is 1 m off in a tunnel. Explain.

**PC-04.** Why can repeated `T = dT * T` updates corrupt a pose, and what is a cheap fix?

**PC-05.** What do the poses of a pose graph look like before optimization, and where does the initial guess come from?

**PC-06.** Which variables would be unobservable if you removed the prior on the first pose?

**PC-07.** Why does the odometry factor's noise have to be consistent with the actual odometry error, and what happens otherwise?

**PC-08.** Your loop detector returns a match with distance 0.12 between scans 200 m apart. What do you do before adding it to the graph?

**PC-09.** Explain why a Cauchy kernel rejects a false loop that a Huber kernel only dampens.

**PC-10.** RPE at 100 m vs ATE: which one is more comparable across sequences of different length, and why?

**PC-11.** Your ablation shows loop closure reducing ATE from 2.1 m to 1.9 m with overlapping CIs. How do you report it?

**PC-12.** Bridge: sequence-based place recognition (SeqSLAM-style) vs single-scan Scan Context: what does the alignment of descriptor sequences buy you, in the terms you would use for read alignment?
