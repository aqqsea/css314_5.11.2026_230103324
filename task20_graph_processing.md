# Task 20 — Why Gustafson Weak Scaling is Hard for Graph Analytics

**Dense linear algebra:** regular, predictable access; work per rank is a closed-form function of local size; communication is a known function (surface/volume), perfectly balanced; arithmetic intensity grows with block size.

**Power-law graph BFS / PageRank:**
1. **Work is not a function of vertex count.** Edge count, diameter and degree distribution determine time; "doubling the graph" (e.g. RMAT scale+1) changes diameter and frontier shape — the fixed-time premise cannot be set a priori. BFS levels ≈ diameter (grows ~log N) ⇒ number of synchronisation steps grows with size.
2. **Frontier imbalance.** Most work is in 2–3 middle BFS levels; hubs (degree ≫ mean) make one rank own a large part of the frontier ⇒ time = max, not mean ⇒ effective α grows with P.
3. **Irregular memory access.** Random pointer chasing is latency-bound (cache-miss rate ~1; TEPS limited by memory-access rate not flops); extra cores contend for memory/network ports, raising T per edge.
4. **Communication volume ∝ edges cut**, not surface area: random/hash partitioning of a power-law graph cuts ≈ `(1 − 1/P)` of edges ⇒ all-to-all message volume ~ constant *fraction of all edges*, so comm per rank doesn't stay constant; small messages dominate (latency/injection-rate bound).
5. **Data-dependent synchronisation:** a global barrier + allreduce (frontier empty?) every level; PageRank has a global convergence check per iteration; iteration count can depend on size.
6. **Memory capacity**: weak scaling of RMAT keeps edges/rank constant but the hubs' adjacency lists do not fit evenly.

**Measures used in practice:** Graph500 reports TEPS at scale S with edge-factor 16; weak scaling efficiency typically 30–60 % at large P (vs > 90 % for stencils) — treat the numbers as indicative.
**Mitigations:** 2-D partitioning (O(√P) partners), direction-optimising BFS, delegate/ghost hub vertices, degree-aware partitioning, asynchronous/bulk-synchronous hybrids, communication aggregation.
