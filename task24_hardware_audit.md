# Task 24 — Hardware Audit and Measured-vs-Theory Discrepancy

## Machine used to produce the committed dataset (sandbox, NOT representative)
| Item | Value |
|---|---|
| CPU | Intel Xeon (Family 6, Model 207), 2.10 GHz, AVX-512/AMX flags — virtualised (KVM) |
| Hardware concurrency | **1 vCPU, 1 thread/core, 1 socket** |
| Caches (reported) | L1d 48 KiB, L1i 32 KiB, L2 2 MiB, L3 260 MiB (shared host cache as seen by the VM) |
| NUMA | 1 node |
| RAM | ≈ 3 GiB (memory channel count not exposed by the hypervisor) |
| Software | Python 3.12.3, NumPy 2.5.4, `multiprocessing` (fork) |

## What the data show (`benchmarks/results.csv`, `results_summary.csv`, `plots/scaling_comparison.*`)
P = 1,2,3,4,6 workers, 5 runs each. Mean wall times 0.136, 0.244, 0.373, 0.552, 0.865 s ⇒ T(P) ≈ P·T(1): all P workers time-share **one** vCPU.
Scaled speedup S(P) = 1.00, 1.12, 1.10, 0.99, 0.95; fitted **α_obs = 0.9997 (R² < 0)**, i.e. "everything serial". This is the correct physical outcome for P > cores and says nothing about the code's parallel quality or about α of real hardware. The curve fit is degenerate (R² negative because the through-origin model cannot explain the flat noise around ~1).
**Do not use these numbers as the submission's scaling result.** Re-run on a multi-core machine: `python benchmarks/weak_scale_bench/weak_bench.py --threads 1 2 4 8 16 && python benchmarks/fit_gustafson.py`, then paste your CPU model (`lscpu`), cache hierarchy (`lscpu -C`, `lstopo`), and memory channels (`sudo dmidecode -t memory`) in the table above.

## Expected deviations on a real machine (to discuss in your write-up)
* **Thermal / power throttling and turbo:** single-core turbo (e.g. 5 GHz) vs all-core clocks (3–3.5 GHz) makes T(P) rise even for perfectly parallel code ⇒ apparent α > 0. Pin governor to `performance`, record frequency (`turbostat`).
* **Memory bandwidth / channel saturation:** this workload is compute-bound (numpy 4/(1+x²) on 1 M-element chunks, ~16 MB working set per pass) but the chunk exceeds L2; with many workers L3 and DRAM bandwidth get shared.
* **NUMA boundaries:** threads crossing sockets pay remote access (1.3–2× latency); use `numactl --cpunodebind=0 --membind=0`, then test across sockets to see the step in T(P).
* **SMT:** 2 hyper-threads share a core ⇒ speedup per extra thread ≈ 0.2–0.3, visible as a knee at physical-core count.
* **Process-pool overheads:** pickling of task args and `map` barrier — included in measured serial share (by design); the fixed `sort` (1.5 M elements) is the intentional serial portion.
