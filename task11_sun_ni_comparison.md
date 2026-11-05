# Task 11 — Gustafson vs. Sun–Ni Memory-Bounded Speedup

**Sun–Ni (1990/93).** Let `g(P)` = factor by which the parallel workload grows when memory grows ×P (`W* = s·W + g(P)·(1−s)·W`):

`S_SN(P) = (s + (1−s) g(P)) / (s + (1−s) g(P)/P)`

**Special cases**
* `g(P) = 1` ⇒ Amdahl (fixed size).
* `g(P) = P` ⇒ `(s + (1−s)P)/(s + (1−s)) = s + (1−s)P` = **Gustafson**.
* `g(P) > P` (work grows faster than memory, e.g. dense LU/GEMM: work N³, memory N² ⇒ `g = P^{3/2}`) ⇒ `S_SN ≈ P` for large P (g/P → ∞ dominates): speedup is *higher* than Gustafson's linear-with-penalty value, up to P.
* `g(P) < P`, e.g. `g = P^{1/2}` (workload ~ memory^{1/2}) ⇒ for large P, `S ≈ ((1−s)/s)·√P`: sub-linear, between Amdahl (bounded) and Gustafson (linear).

**When Gustafson over/under-estimates**
* *Overestimates* when the achievable problem growth in the memory budget is smaller than P (`g<P`): solvers whose useful work per byte *drops* (sparse solvers with fill-in limits, bandwidth-bound kernels) or when the fixed-time assumption forces more work than memory holds. Also overestimates if communication or serial part grows with P.
* *Underestimates* when `g > P` (compute-heavy O(N^k) kernels with memory O(N²)): the extra work per byte raises the parallel fraction, so serial share drops even faster; Gustafson's α (frozen) is pessimistic.
* Equal at `g = P`. Gustafson is "fixed-time", Sun–Ni "fixed-memory"; with `time ∝ g(P)/P` they coincide only for `g = P`.

Numerical example: s = α = 0.05, P = 64: Gustafson 60.85; Sun–Ni with `g = P^{1/2} = 8`: `(0.05+0.95·8)/(0.05+0.95·8/64) = 7.65/0.16875 = 45.3` (lower); with `g = P^{3/2} = 512`: `(0.05+486.4)/(0.05+7.6) = 486.45/7.65 = 63.6` (higher, near P).
