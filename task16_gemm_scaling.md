# Task 16 — GEMM under Gustafson Scaling

Work `W(N) = 2N³` flops. Constant parallel time `T` on P processors with per-proc rate `r`: `2N³/(P r) = T` ⇒ `N³ ∝ P`.

**`N(P) = N₁ · P^{1/3}`** (proof: `N(P)³/P = N₁³`).

Memory: `M = 3N² ∝ P^{2/3}` total ⇒ per-node memory *falls* as `P^{−1/3}`: constant-time weak scaling of GEMM does not exhaust memory (compute-bound); conversely scaling memory (`N ∝ P^{1/2}`) makes time grow as `P^{1/2}`.

Targets for N₁ = 1000 (ideal, ignoring communication — real 2-D/2.5-D algorithms add O(N²/√P) words per processor):

| P | N = 1000·P^{1/3} | N/N₁ |
|---:|---:|---:|
| 1 | 1 000 | 1 |
| 8 | 2 000 | 2 |
| 64 | 4 000 | 4 |
| 512 | 8 000 | 8 |
| 4 096 | 16 000 | 16 |
| 32 768 | 32 000 | 32 |

Cube-root growth is slow: 1000× more cores ⇒ only 10× larger matrices at the same wall time.
