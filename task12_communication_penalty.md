# Task 12 — Gustafson with Communication Overhead

**Model.** Keep `s + p = 1` normalisation at P = 1 *base* and let the parallel time per processor stay `p` of compute, plus an added non-overlapped communication/synchronisation term `C(P)` (as a fraction of the base parallel time), with `C(1) = 0`:

`T(P) = s + p + C(P) = 1 + C(P)`  (wall time grows; compute work is `s + P p`).

`S_C(P) = (s + P p)/(1 + C(P)) = (P − α(P−1)) / (1 + C(P))`

`E_C(P) = [1 − α(P−1)/P] / (1 + C(P))`

**Choices of C(P).**
* Tree reduction/barrier: `C = γ log₂P`.
* 2-D mesh/halo-all-to-all-ish: `C = γ √P`.
* Neighbour halo (Task 17): `C = γ` const ⇒ just a larger effective α.

**Limits.** Log: `S_C ≈ (1−α)P/(γ log₂P)` ⇒ `E_C → 0` slowly as `1/log P`; √P: `S_C ≈ (1−α)√P/γ`, `E → 0` as `P^{−1/2}`. Only `C = O(1)` preserves Gustafson's asymptote (`E → (1−α)/(1+γ)`).

**Equivalent effective serial fraction:** defined by `S_C = P − α_eff(P−1)`, i.e. `α_eff = (P − S_C)/(P − 1)`; for small C, `α_eff ≈ α + (1−α)·C(P)·P/(P−1)`.

Example α = 0.04, γ = 0.01, log model, P = 1024: `C = 0.1`, `S = 983.08/1.1 = 893.7`, `E = 0.873` (vs 0.960).

**Parameter fit.** Measure T(P) in a weak-scaling run, `C(P) = T(P)/T(1) − 1`, regress on `log₂P` or `√P` to choose the form.
