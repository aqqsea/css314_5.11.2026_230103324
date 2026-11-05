# Task 14 — Isoefficiency of a Gustafson-compliant Program

**Definition (Kumar–Grama).** `T_o(W,P) = P·T_P − W` (total overhead). `E = 1/(1 + T_o/W)`. Constant E requires `W = K·T_o(W,P)` with `K = E/(1−E)`. The isoefficiency function is the solution `W(P)`.

**Gustafson program.** Serial part `t_s` (constant absolute time) runs on one processor while P−1 idle; parallel work `W_p = P·w` (w per processor). Overhead: `T_o = (P−1)·t_s` (idle time) — with `T_P = t_s + w` and `W = t_s + P w`.
Efficiency: `E = W/(P T_P) = (t_s + Pw)/(P(t_s + w))`.

Set `E` const: `W = K T_o = K (P−1) t_s` ⇒ `W(P) = Θ(P)` **isoefficiency function Θ(P)** — the best possible (linear, the minimum since every processor must have work). Check: with `W = P·w`, `E ≈ 1/(1 + t_s/w)` const ✓ (equals `1−α` as P → ∞ with `α = t_s/(t_s+w)`).

**Critique.** Linear isoefficiency means "perfectly scalable" — but only if overhead is *only* idle time during the constant serial part. With `T_o = Θ(P log P)` (tree reductions) isoefficiency is `Θ(P log P)`, so keeping per-processor work constant is **insufficient**: work per processor must grow ∝ log P. With `T_o ~ P^{3/2}` (√P-ish) need `W ~ P^{3/2}`. Gustafson-compliance ⇔ isoefficiency Θ(P) ⇔ memory per processor constant is enough.
