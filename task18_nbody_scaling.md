# Task 18 — N-Body: All-Pairs vs. Barnes–Hut under Fixed-Time Scaling

Constant time per iteration on P processors ⇒ total work `W(N) = P·w₀`.

## Direct all-pairs, `W = c N²`
`N² ∝ P` ⇒ **`N = N₀ √P`**. Particles per processor `N/P = N₀/√P` *shrinks*. Parallel work/processor constant, but each processor needs *all* N positions (all-gather): communication `O(N) = O(√P)` words/processor, per-processor compute fixed ⇒ comm/comp ratio ∝ `√P`. The serial/parallel ratio worsens: `α(P) ≈ α₀ + γ√P`. (Systolic/ring schemes keep volume `O(N)` per proc.) Result: weak scaling is clean in *flops*, but the data-replication/communication share grows as √P.

## Barnes–Hut, `W = c N log N`
`N log N = P·N₀ log N₀` ⇒ `N = P·N₀·(log N₀/log N)` — slightly sub-linear in P: `N/P` decreases slowly, as `log N₀/log N`. Serial part: tree build (O(N log N) if built centrally, O(N) top-level) and top-of-tree broadcast: with a central build, serial time `t_s ∝ N log N ∝ P` — **grows with P** (α → const·P/(…) ⇒ breaks Gustafson). With a distributed (locally essential tree) build the serial part is O(log P) per level and the comm per proc `O((N/P)^{2/3}) + O(log P)` ⇒ ratio nearly flat. Numerical example (N₀ = 10⁵ at P = 1, log base 2): P = 64 ⇒ solving `N log₂N = 64·10⁵·16.61 ≈ 1.06·10⁸` gives N ≈ 4.8·10⁶ (vs 6.4·10⁶ for perfectly linear, vs 8·10⁵ for all-pairs).

## Comparison
| | all-pairs | Barnes–Hut |
|---|---|---|
| N(P) | `N₀P^{1/2}` | ≈ `N₀P / log` factor |
| particles / proc | ↓ `P^{-1/2}` | ↓ slowly (`1/log P`) |
| comm per proc | ↑ `O(√P)` words | ~const (+ log P) |
| α trend | grows ~√P | ~flat (distributed), ~P (centralised build) |
Take-away: the O(N log N) algorithm weak-scales to far larger N, and its serial/parallel ratio stays flat only if the serial tree phase is itself parallelised.
