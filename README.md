# Gustafson's Law & Weak Scaling — Practice Repository

Course: Parallel & Distributed Computing Architecture (Instructor: Sufyan bin Uzayr). Ungraded comprehensive practice, tasks 01–25.

## Contents
- [Quick reference](#quick-reference)
- [Run everything](#run-everything)
- [When to design for Gustafson weak scaling](#when-to-design-for-gustafson-weak-scaling)
- [Architectural synthesis](#architectural-synthesis)
- [Artifact index](#artifact-index)
- [Honest status / caveats](#honest-status--caveats)

## Quick reference
| Rule | Formula |
|---|---|
| Gustafson scaled speedup | `S(P) = P − α(P−1)` |
| Efficiency | `E(P) = 1 − α(P−1)/P → 1 − α` |
| Amdahl | `S_A = 1/(s + (1−s)/P) → 1/s`, `E_A → 0` |
| Frame conversion | `s_A = α/(α + (1−α)P)` |
| Sun–Ni | `S = (s + (1−s)g(P))/(s + (1−s)g(P)/P)` (`g=1` Amdahl, `g=P` Gustafson) |
| With communication | `S_C = S(P)/(1 + C(P))` |
| Isoefficiency of ideal weak scaling | `W = Θ(P)` |
| Max tolerable α | `α ≤ (P − S_target)/(P − 1)` |

Key numbers: α = 4 % ⇒ S(1024) = 983.08, E → 0.96 (T06). P = 8192, S ≥ 7500 ⇒ α ≤ 8.45 % (T07). s = α = 0.08, P = 128: Amdahl 11.47 vs Gustafson 117.84 (T08). 3-D grid, 32 GiB/node, 16 B/pt: N = 5161 (64 nodes), 10321 (512 nodes) (T10).

## Run everything
```bash
pip install numpy matplotlib
python benchmarks/simulator.py                       # T21: CSV + overlay plots in plots/
python benchmarks/weak_scale_bench/weak_bench.py --threads 1 2 4 8 16 --runs 5   # T22/T23 -> benchmarks/results.csv
python benchmarks/fit_gustafson.py                   # T23/T24: fit alpha, plots/scaling_comparison.{png,pdf}
```

## When to design for Gustafson weak scaling
Use it when (1) users can and want to enlarge the problem (resolution, ensemble size, particle count); (2) serial work is constant (set-up, I/O) rather than growing with size; (3) communication is neighbour-local (stencils, Monte-Carlo, particle-in-cell with local halos); (4) per-node memory sets the local problem size. Prefer Amdahl/strong-scaling analysis for latency-bound interactive jobs and fixed-size problems; use Sun–Ni / isoefficiency when memory limits or superlinear algorithms, global collectives or irregular data (T11–T14, T20) break the constant-time premise; track energy as `P·P_idle·T` (T15).

## Architectural synthesis
1. Amdahl and Gustafson are the same time model under different constraints (T01–T03); report which frame α was measured in.
2. Efficiency saturates at `1−α` under weak scaling, decays like 1/P under strong scaling (T04, T06).
3. The 1988 nCUBE result is explained by growing the problem (T05).
4. Real limits are P-dependent overheads: `log P` reductions, `√P` or all-to-all communication, load imbalance (T12, T13, T19, T20); a good weak-scaling kernel has Θ(P) isoefficiency (T14): stencils (T17), GEMM only with `N ∝ P^{1/3}` (T16), Monte Carlo (T19).
5. Memory-bound growth: 3-D grids grow only as `P^{1/3}` in side length (T10).

## Artifact index
| Task | File |
|---|---|
| 01 | [theory/task01_scaling_models.md](theory/task01_scaling_models.md) |
| 02 | [theory/task02_derivation.md](theory/task02_derivation.md) |
| 03 | [theory/task03_serial_invariance.md](theory/task03_serial_invariance.md) |
| 04 | [theory/task04_asymptotic_limits.md](theory/task04_asymptotic_limits.md) |
| 05 | [theory/task05_historical_ncube.md](theory/task05_historical_ncube.md) |
| 06 | [calculations/task06_parametric_table.md](calculations/task06_parametric_table.md) |
| 07 | [calculations/task07_tolerable_serial.md](calculations/task07_tolerable_serial.md) |
| 08 | [calculations/task08_cross_divergence.md](calculations/task08_cross_divergence.md) |
| 09 | [calculations/task09_multicomponent.md](calculations/task09_multicomponent.md) |
| 10 | [calculations/task10_memory_growth.md](calculations/task10_memory_growth.md) |
| 11 | [theory/task11_sun_ni_comparison.md](theory/task11_sun_ni_comparison.md) |
| 12 | [theory/task12_communication_penalty.md](theory/task12_communication_penalty.md) |
| 13 | [theory/task13_failure_cases.md](theory/task13_failure_cases.md) |
| 14 | [theory/task14_isoefficiency.md](theory/task14_isoefficiency.md) |
| 15 | [theory/task15_energy_scaling.md](theory/task15_energy_scaling.md) |
| 16 | [calculations/task16_gemm_scaling.md](calculations/task16_gemm_scaling.md) |
| 17 | [calculations/task17_stencil_scaling.md](calculations/task17_stencil_scaling.md) |
| 18 | [analysis/task18_nbody_scaling.md](analysis/task18_nbody_scaling.md) |
| 19 | [analysis/task19_monte_carlo.md](analysis/task19_monte_carlo.md) |
| 20 | [analysis/task20_graph_processing.md](analysis/task20_graph_processing.md) |
| 21 | [benchmarks/simulator.py](benchmarks/simulator.py), [plots/simulator_output.csv](plots/simulator_output.csv), [plots/simulator_overlay.png](plots/simulator_overlay.png) |
| 22 | [benchmarks/weak_scale_bench/](benchmarks/weak_scale_bench/) |
| 23 | [benchmarks/results.csv](benchmarks/results.csv), [benchmarks/results_summary.csv](benchmarks/results_summary.csv), [benchmarks/fit_gustafson.py](benchmarks/fit_gustafson.py) |
| 24 | [plots/scaling_comparison.png](plots/scaling_comparison.png) (+ `.pdf`), [analysis/task24_hardware_audit.md](analysis/task24_hardware_audit.md) |
| 25 | this README |

## Honest status / caveats
- The committed benchmark data were produced in a **1-vCPU sandbox**, so they show α ≈ 1 (no real parallelism). **Re-run Tasks 22–24 on your own multi-core machine** and update the hardware audit before submitting.
- Task 05 historical figures are from memory of Gustafson (1988); verify against the paper. Task 10 uses an explicit assumption of 16 B per grid point.
- Suggested commits: one atomic commit per task (`feat: complete task NN ...`).
