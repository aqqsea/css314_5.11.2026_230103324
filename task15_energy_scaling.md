# Task 15 — Energy under Scaled Speedup

**Model.** Each node draws `P_idle` whenever powered and `P_dyn = P_active − P_idle` extra while computing. Normalise wall-clock `T = s + p = 1` (Gustafson run on P nodes; `α = s`).

**P nodes, scaled problem.**
* Serial phase (duration s): one node active, P−1 idle → `s·[P_active + (P−1)P_idle] = s·[P·P_idle + P_dyn]`.
* Parallel phase (duration p): all active → `p·P·(P_idle + P_dyn)`.

`E_P = P·P_idle·(s+p) + (s + P·p)·P_dyn = P·P_idle·T + S(P)·P_dyn`

Static energy ∝ P (nodes powered for the whole run); dynamic energy ∝ the work done, `S(P) = P − α(P−1)`.

**1 core, identical wall-clock T.** It can finish only the unscaled job (work 1): `E_1 = T·P_active = P_idle + P_dyn`. The P-core machine did S(P)× more science for `E_P/E_1 = [P·P_idle + S·P_dyn]/[P_idle + P_dyn]` energy.

**Energy per unit of work** `e_P = E_P/S(P) = (P/S)·P_idle + P_dyn → P_idle/(1−α) + P_dyn` (P → ∞), versus `e_1 = P_idle + P_dyn`. Penalty: only the factor `1/(1−α)` on *static* power (idle nodes during the serial phase). Dynamic energy per flop is unchanged ⇒ weak scaling is energy-proportional when α is small and `P_idle ≪ P_active` (or when idle nodes can be power-gated).

**Same work, different time.** A single core needs `S(P)·T` to do the scaled job: `E_1,long = S·(P_idle + P_dyn)`.
`E_P/E_1,long = (P/S)·P_idle/(P_idle+P_dyn) + P_dyn/(P_idle+P_dyn)`.
Example α = 0.04, P = 1024, `P_idle = 100 W`, `P_dyn = 150 W`: `P/S = 1.0416` ⇒ ratio = `1.0416·0.4 + 0.6 = 1.0167` — P cores use only **+1.7 % energy** for a **983× shorter** time; the ratio is 1 for `P_idle = 0` and `P/S → 1/(1−α)` bounds it at `0.4/0.96 + 0.6 = 1.0167` asymptotically.
