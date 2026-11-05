# Task 05 — The 1988 nCUBE/10 Experiment and "Amdahl's Pessimism"

*Source: J. L. Gustafson, "Reevaluating Amdahl's Law", CACM 31(5), 1988 (reconstructed from the published account; figures below are as I recall them — verify against the paper before citing).*

**Context.** In the 1980s the textbook reading of Amdahl's Law was that with ≥ 1 % serial work, massively parallel machines (hundreds to thousands of processors) were pointless: `S ≤ 100`. At Sandia, Gustafson, Montry and Benner ran three real applications (beam strain analysis, surface-wave simulation, unstable fluid dynamics) on a **1024-processor nCUBE/10 hypercube** and reported **scaled speedups of roughly 1009, 1020 and 1016** — i.e. ≈ 98–99.6 % efficiency.

**Why this seemed impossible.** Amdahl: with serial fraction `s = 0.4 %`, `S_A(1024) = 1/(0.004 + 0.996/1024) ≈ 204`; the ceiling `1/s = 250`. Observed ≈ 1000, 4–5× above the "ceiling".

**How problem expansion resolves it.**
1. Each processor had its own fixed local memory; the researchers grew the problem (grid points / elements) proportionally to P so the **parallel time per processor stayed the same**, e.g. ≈ constant minutes.
2. Serial parts (program load, set-up, I/O) were roughly **constant absolute time**, so their *fraction* of the scaled run was tiny. The 0.4–0.8 % was measured **on the 1024-processor run** (α), not on a 1-processor run.
3. Gustafson formula: `S = 1024 − 0.004·1023 ≈ 1019.9` ✓ (in line with the measured 1009–1020).
4. A 1-processor run of the scaled problem was impossible (memory); the single-processor time was *estimated* from the serial and parallel times measured in the parallel run — the same assumption as in Task 02 (and a standard caveat: it ignores cache effects of the larger working set on one CPU).

**Lesson.** Amdahl's ceiling is a statement about a *fixed* workload. When users choose to enlarge workloads with capacity, the serial *fraction* shrinks with size and the ceiling vanishes.
