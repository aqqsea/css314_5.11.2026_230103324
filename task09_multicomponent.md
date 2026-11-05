# Task 09 — Multi-Component Workload

Phases (shares of the *parallel* run time): A (I/O + broadcast) 2 %, B (boundary sync) 6 %, C (flux compute) 92 %.

**Classification.** A is serial (single reader/root). B is message-passing synchronisation: treated as non-scaling overhead (does not shrink with P), so counted as serial-like. C parallel.
`α = 0.02 + 0.06 = 0.08`, `p = 0.92`.

| P | S(P) = P − 0.08(P−1) | E(P) |
|---:|---:|---:|
| 512 | 471.12 | 0.9202 |
| 2 048 | 1 884.24 | 0.9200 |

Sensitivity: if B is *not* serial (overlaps/scales, α = 0.02): S(512) = 501.78, S(2048) = 2007.06. If B instead grows as log₂P (Task 12) and 6 % is its share at P = 512 (log₂P = 9), at P = 2048 (log₂P = 11) it becomes ≈ 0.06·11/9 = 7.33 %, so α ≈ 0.0933 and S(2048) ≈ 1857 (E ≈ 0.907) — a visible but modest loss.
