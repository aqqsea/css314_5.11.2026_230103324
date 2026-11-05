# Task 08 — Amdahl vs. Gustafson at s = α = 0.08, P = 128

**Amdahl:** `S_A = 1/(0.08 + 0.92/128) = 1/(0.08 + 0.0071875) = 1/0.0871875 = 11.4695`  
**Gustafson:** `S_G = 128 − 0.08·127 = 128 − 10.16 = 117.84`

* Ratio `S_G/S_A = 10.274`.
* Discrepancy relative to Amdahl: `(117.84 − 11.4695)/11.4695 = +927.4 %`.
* Amdahl is lower than Gustafson by `(117.84 − 11.4695)/117.84 = 90.27 %`.

**Why they diverge.** They answer different questions with the same number: Amdahl's `s` is a fraction of the *fixed* 1-core run; the speedup saturates at `1/s = 12.5` (already at 91.8 % of ceiling at P = 128). Gustafson's `α` is a fraction of the *scaled* P-core run, so the serial time is spread over a P-times larger workload: slope `1 − α = 0.92` forever. The ratio `S_G/S_A → ∞` as P → ∞ (≈ `0.92P/12.5 = 0.0736P` for large P); e.g. at P = 8 the ratio is only `(8 − 0.56)/(1/(0.08+0.115)) = 7.44/5.13 = 1.45`.
(The two values are not rival predictions of one experiment; they use the same α in different frames, see Task 03.)
