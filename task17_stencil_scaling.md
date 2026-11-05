# Task 17 — 7-point 3-D Stencil: Surface-to-Volume

Global domain `N³`, P processes in a `P^{1/3}` per side decomposition; each process owns `n³` with `n = N/P^{1/3}`.

* Compute per step: `~ 8 n³` flops (7 loads, 1 store pattern ≈ O(n³)).
* Halo exchange: 6 faces × n² words = `6n²`.
* Ratio `R = comm/comp = 6n²/n³ ∝ 1/n = P^{1/3}/N`.

**Weak scaling (Gustafson):** `N³ = P·n₀³` ⇒ `n = n₀` constant ⇒ `R = 6/n₀` constant (e.g. n₀ = 128 ⇒ 4.7 % words per point, independent of P). So α from communication stays *constant* — consistent with Gustafson's assumption (neighbour-only exchange, latency per message constant). Global side `N = n₀P^{1/3}` (64 → 4n₀, 512 → 8n₀).

**Strong scaling for contrast:** N fixed ⇒ `R ∝ P^{1/3}` — it *degrades* (P ×8 ⇒ R ×2), which is why Amdahl-type behaviour appears.

**Caveats:** global reductions (dt, residual norms) add `O(log P)`; the per-message latency does not shrink while faces shrink under strong scaling.
