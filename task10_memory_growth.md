# Task 10 — Memory Ceilings for a 3-D Grid

Per node cap `M_node = 32 GiB = 2³⁷ B`. Assumption (state in report): double precision, 2 arrays (u_old, u_new) ⇒ `b = 16 B` per grid point. Aggregate footprint `M(P) = c·P` with `c = M_node`.

Total points that fit: `N³ ≤ P·M_node/b` ⇒ `N_max(P) = (P·2³⁷/2⁴)^{1/3} = (P·2³¹)^{1/3} = 1290.16·P^{1/3}`.

| Nodes P | max points | N_max (cube side) | per-node sub-cube |
|---:|---:|---:|---:|
| 1 | 2.147·10⁹ | 1 290 | 1 290 |
| 64 | 1.374·10¹¹ | **5 161** | 1 290 |
| 512 | 1.100·10¹² | **10 321** | 1 290 |

Other footprints (cube side, P = 64 / 512): 8 B/pt → 6 502 / 13 004; 24 B/pt → 4 508 / 9 016; 40 B/pt → 3 802 / 7 605.

**Insight.** Linear growth of memory/work with P gives `N ∝ P^{1/3}` in 3-D: 8× more nodes only doubles N. Weak scaling is bounded by the *per-node* cap, not by the machine total, as long as the local sub-cube is unchanged (halo/ghost cells would reduce it slightly: e.g. 1 layer at 1290³ costs ≈ 0.5 %).
