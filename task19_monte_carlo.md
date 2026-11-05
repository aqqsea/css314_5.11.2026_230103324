# Task 19 — Monte Carlo: Ideal Weak Scaling and the Residual α

Work: M samples per processor, total `P·M`; each sample independent ⇒ `p ≈ 1`. Non-zero α originates from:

1. **PRNG seed management** — creating P independent streams (counter-based Philox/Threefry: O(1) per stream; leap-frog/jump-ahead LCG: O(log skip) per stream; central seeding loop: O(P) serial). Use `SeedSequence.spawn` / counter-based RNGs → negligible, otherwise `t_s ∝ P`.
2. **Reduction** of P partial results (mean, variance, histogram).
3. **Output serialisation** (rank-0 writes, size of output `∝ P` if per-rank output).
4. **Start-up/launch, I/O of the model input** — constant.
5. Load imbalance when paths have random length (barriers wait for the slowest; time = max of P random variables ≈ mean + σ√(2 ln P)).

**Tree reduction cost.** With `t_c` per combine step (latency+op): flat gather `(P−1)·t_c` (serial, ∝ P) vs binomial tree `⌈log₂P⌉·t_c`.
With sample time `T_s` per processor: `α(P) = (t_s + t_c·log₂P)/(T_s + t_s + t_c log₂P)`.
Example `T_s = 10 s`, `t_s = 0.05 s`, `t_c = 20 µs`: P = 1024 ⇒ `t_c log₂P = 0.2 ms`; α ≈ 0.0050; S = 1024 − 0.00501·1023 = 1018.9 (E = 0.995). Flat gather: `(1023)·20 µs = 20.5 ms` ⇒ α = 0.00705 ⇒ S = 1016.8 — the tree mostly matters at larger P or large payloads (a 1 MB histogram: `t_c ≈ 100 µs` per hop).
**Conclusion:** the log-term is the only term that grows with P, and it enters `S(P)` as `~ P·t_c log P/T_s`, i.e. a relative loss ≪ 1 % unless the samples per rank are tiny (strong-scaling regime).
