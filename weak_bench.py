#!/usr/bin/env python3
"""Task 22/23 - weak-scaling benchmark (Python multiprocessing).

Workload per run with P workers:
  * serial phase (parent only, size FIXED): sort of --serial-n random numbers
    (models setup / I/O / final aggregation; this is the "s" part)
  * parallel phase: each worker integrates 4/(1+x^2) on [0,1] with K midpoint
    subintervals (K per worker is CONSTANT -> total work grows as P*K).
  * reduction in parent (P partial sums).
Wall-clock is measured around the whole run (pool already warmed up).

Examples:
  python weak_bench.py                              # threads = 1,2,4,.. up to CPU count
  python weak_bench.py --threads 1 2 3 4 6 --runs 5 # explicit (oversubscribes if > cores)
"""
import argparse, csv, os, statistics, time, multiprocessing as mp
import numpy as np

def integrate(k, chunk=1_000_000):
    h, acc, i = 1.0 / k, 0.0, 0
    while i < k:
        n = min(chunk, k - i)
        x = (np.arange(i, i + n) + 0.5) * h
        acc += float(np.sum(4.0 / (1.0 + x * x)))
        i += n
    return acc * h

def serial_phase(n):
    rng = np.random.default_rng(12345)
    return float(np.sort(rng.random(n))[n // 2])

def one_run(pool, P, k, serial_n):
    t0 = time.perf_counter()
    serial_phase(serial_n)                      # fixed serial work
    parts = pool.map(integrate, [k] * P, chunksize=1)  # P tasks, K each
    pi = sum(parts) / P                          # reduction (mean over equal slices of same integral)
    return time.perf_counter() - t0, pi

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--threads", type=int, nargs="+", default=None)
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--k", type=int, default=30_000_000, help="subintervals per worker (constant)")
    ap.add_argument("--serial-n", type=int, default=1_500_000, help="fixed serial sort size")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results.csv"))
    a = ap.parse_args()
    ncpu = os.cpu_count() or 1
    if a.threads is None:
        a.threads, p = [], 1
        while p <= ncpu: a.threads.append(p); p *= 2
        if a.threads[-1] != ncpu: a.threads.append(ncpu)
    if len(a.threads) < 5: print(f"note: only {len(a.threads)} thread counts; Task 23 wants >= 5 (use --threads)")
    print(f"hardware concurrency = {ncpu}; thread counts = {a.threads}")
    rows = []
    for P in a.threads:
        with mp.Pool(P) as pool:
            pool.map(integrate, [10_000] * P)    # warm-up
            for r in range(1, a.runs + 1):
                t, pi = one_run(pool, P, a.k, a.serial_n)
                rows.append(dict(threads=P, run=r, wall_s=t, pi_est=pi, k_per_worker=a.k,
                                 serial_n=a.serial_n, cpu_count=ncpu))
                print(f"P={P:3d} run={r} t={t:.4f}s pi={pi:.10f}")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
