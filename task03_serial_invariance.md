# Task 03 — Serial-Fraction Invariance Paradox (memo)

**Frames of reference.**
* Amdahl: `s` = serial share of the **1-processor** run of a **fixed** problem W.
* Gustafson: `α` = serial share of the **P-processor** run of the **scaled** problem W(P).

**Conversion.** Let serial *time* be `t_s` (constant) and the parallel part of the scaled job `t_p` on P cores (so single-core time of the scaled job is `t_s + P·t_p`). Then
* `α = t_s/(t_s + t_p)` (measured on the parallel machine),
* the Amdahl fraction of the *same scaled job* on one core is `s_A = t_s/(t_s + P t_p)`.

Divide: `s_A = α / (α + (1−α)P)`.

Check by plugging into Amdahl: the one-core time of the scaled job is `t_s + P·t_p`, and the Amdahl formula with fraction `s_A` reproduces the P-core time `t_s + t_p` (this is just a restatement of the model, so no new information is added), giving
`S = (t_s + P t_p)/(t_s + t_p) = α + (1−α)P = P − α(P−1)` — Gustafson. Hence the laws agree once the same fraction is measured in the same frame.

**Resolving the "paradox".** A uniprocessor measurement of a *large* problem shows tiny `s_A` (e.g. α = 0.04, P = 1024 ⇒ s_A ≈ 4.1·10⁻⁵), so Amdahl's ceiling `1/s_A ≈ 24 600` is far above P: serial overhead does not throttle scaling. The apparent contradiction (a 4 % serial part yet speedup 983×) disappears because the 4 % is *not* the fraction that Amdahl's formula expects; what is invariant is the **absolute serial time**, not the fraction. Serial time is invariant only when it does not grow with problem size (I/O set-up, parameter parsing). Where it does (global reductions, Task 12; gather to root) the invariance fails.

**Critical note.** Measuring α on the parallel machine is practical (the big problem often cannot run on 1 core at all) but needs profiling of the serial section inside the parallel run; load imbalance idles processors and gets counted — correctly — as serial-like time.
