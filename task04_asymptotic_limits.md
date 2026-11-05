# Task 04 — Asymptotic Parallel Efficiency

**Gustafson.** `E_G(P) = 1 − α(P−1)/P = 1 − α + α/P`.

Limit: `lim_{P→∞} E_G(P) = 1 − α`.  Proof: `α/P → 0`. Convergence is monotone *decreasing* from E(1)=1; `E_G(P) − (1−α) = α/P`, so the efficiency never drops below `1−α`.
Example α = 0.04 ⇒ E∞ = 0.96.

**Amdahl.** `E_A(P) = S_A/P = 1/(sP + (1−s))`.

Limit: `lim_{P→∞} E_A(P) = 0` since `sP → ∞` for s > 0. Proof: for any ε, `E_A < ε` once `P > (1/ε − (1−s))/s`. Rate `E_A ~ 1/(sP)`. For s = 0.04, E_A = 0.5 at P = 26 and ≈ 0.0025 at P = 10⁴.

**Deduction.** Under weak scaling efficiency converges to a positive constant `1−α`; under strong scaling it decays as 1/P. Efficiency is the quantity which distinguishes the regimes: a Gustafson program can use arbitrarily many processors profitably, an Amdahl program cannot. (Also `S_A → 1/s` finite vs `S_G ~ (1−α)P` unbounded.)
