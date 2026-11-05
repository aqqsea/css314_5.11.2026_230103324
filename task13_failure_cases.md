# Task 13 — Two Algorithms Where Fixed-Time Weak Scaling Breaks

## 1. Dense/Gaussian-elimination LU solve (or any algorithm whose complexity is superlinear in memory with global dependencies)
Work `W ~ N³`, memory `N²`. To keep time constant, N must grow only as `P^{1/3}` (Task 16), but then *the problem is tiny per node*: memory per node falls like `P^{−1/3}` while panel factorisation + pivoting (a serial-like critical path of length `O(N)` with per-step broadcast `O(log P)`) grows with N. The serial share is not constant: `α(P)` rises ⇒ constant-time premise breaks (time grows ∝ N·log P).

## 2. Comparison-based global sort / FFT (all-to-all communication)
Parallel sample-sort or distributed FFT: weak scaling per node `n` constant, but an all-to-all moves `~n` words per node through a bisection bandwidth that grows `P^{2/3}` (3-D torus) or `P` (fat-tree, ideal) — on torus, time per step grows as `P^{1/3}`; additionally `O(n log(nP))` compute includes a `log P` factor, so equal per-node size does *not* give equal time. Synchronisation (barrier on all P) and network contention scale with P.

(Others: conjugate-gradient — global dot-product reductions `O(log P)` plus iteration count grows with condition number ∝ N, so time-to-solution grows with problem size even if time per iteration is flat; BFS, Task 20.)

**Why the premise breaks.** Gustafson needs (i) work per processor ≈ constant for a size increase of P, (ii) constant serial time, (iii) negligible P-dependent communication. Superlinear complexity, iteration counts growing with N, and global collectives violate (i)–(iii), so `T(P)` rises and measured "S = P·T(1)/T(P)" falls below the linear law.
