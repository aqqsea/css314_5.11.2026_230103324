# Task 06 — Parametric Speedup, α = 0.04

`S(P) = P − 0.04(P−1)`, `E(P) = S/P = 0.96 + 0.04/P`

| P | S(P) | E(P) | Lost to serial (P − S) |
|---:|---:|---:|---:|
| 16 | 15.4000 | 0.962500 | 0.60 |
| 64 | 61.4800 | 0.960625 | 2.52 |
| 256 | 245.8000 | 0.960156 | 10.20 |
| 1 024 | 983.0800 | 0.960039 | 40.92 |
| 4 096 | 3 932.2000 | 0.960010 | 163.80 |
| 16 384 | 15 728.6800 | 0.960002 | 655.32 |

Sample log (P = 1024): `S = 1024 − 0.04·1023 = 1024 − 40.92 = 983.08`; `E = 983.08/1024 = 0.960039`.

**Evaluation.** Efficiency does *not* degrade with exponential growth of P: it drops from 0.9625 and saturates at `1 − α = 0.96` (the decrease is `α/P`, i.e. vanishes). What grows is the **absolute** loss `α(P−1)` (≈ 655 "lost cores" at 16 384), linear in P — the same 4 % tax at every scale. Contrast Amdahl with s = 0.04: S(16384) = 24.99, E = 0.15 %.
