#!/usr/bin/env python3
"""Task 23/24 - aggregate results.csv, fit alpha by least squares, plot.

Weak-scaling measured scaled speedup:  S(P) = P * T(1) / T(P)
Gustafson:  S(P) = P - alpha (P-1)   ->  (P - S) = alpha (P-1)
Through-origin LSQ:  alpha = sum((P-1)(P-S)) / sum((P-1)^2)
(Amdahl curve is drawn with the same numeric value as serial fraction.)
"""
import argparse, csv, os, math, collections
import numpy as np

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=os.path.join(here, "results.csv"))
    ap.add_argument("--plots", default=os.path.join(here, "..", "plots"))
    ap.add_argument("--summary", default=os.path.join(here, "results_summary.csv"))
    a = ap.parse_args()

    d = collections.defaultdict(list)
    for r in csv.DictReader(open(a.csv)): d[int(r["threads"])].append(float(r["wall_s"]))
    Ps = sorted(d)
    mean = {P: np.mean(d[P]) for P in Ps}
    sd   = {P: np.std(d[P], ddof=1) if len(d[P]) > 1 else 0.0 for P in Ps}
    n    = {P: len(d[P]) for P in Ps}
    T1 = mean[Ps[0]] if Ps[0] == 1 else mean[1]
    S    = np.array([P * T1 / mean[P] for P in Ps], float)
    # propagate relative error of T(P) (and T1) to S
    rel1 = sd[1] / mean[1] / math.sqrt(n[1])
    Serr = np.array([S[i] * math.hypot(sd[P] / mean[P] / math.sqrt(n[P]), rel1) for i, P in enumerate(Ps)])
    P_arr = np.array(Ps, float)
    x = P_arr - 1
    alpha = float(np.sum(x * (P_arr - S)) / np.sum(x * x)) if np.sum(x * x) > 0 else float("nan")
    ss_res = float(np.sum((S - (P_arr - alpha * x)) ** 2)); ss_tot = float(np.sum((S - S.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    print(f"{'P':>4} {'mean[s]':>9} {'sd[s]':>8} {'S(P)':>7} {'E(P)':>6}")
    for i, P in enumerate(Ps): print(f"{P:4d} {mean[P]:9.4f} {sd[P]:8.4f} {S[i]:7.3f} {S[i]/P:6.3f}")
    print(f"\nalpha_observed = {alpha:.4f}   (R^2 = {r2:.4f})")

    with open(a.summary, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["threads", "runs", "mean_s", "std_s", "S_scaled", "S_stderr", "E"])
        for i, P in enumerate(Ps): w.writerow([P, n[P], mean[P], sd[P], S[i], Serr[i], S[i] / P])
        w.writerow([]); w.writerow(["alpha_observed", alpha, "R2", r2])

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    pp = np.linspace(1, max(Ps), 200)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(pp, pp, "k:", label="Ideal linear speedup S = P")
    ax.plot(pp, pp - alpha * (pp - 1), "-", color="C0", label=f"Gustafson fit (α = {alpha:.3f})")
    if 0 < alpha < 1:
        ax.plot(pp, 1 / (alpha + (1 - alpha) / pp), "--", color="C3", label=f"Amdahl, s = {alpha:.3f}")
    ax.errorbar(Ps, S, yerr=Serr, fmt="o", color="C2", capsize=4, label="Measured (mean ± s.e.)")
    ax.set(xlabel="workers P", ylabel="scaled speedup S(P)", title="Weak-scaling: measured vs. theory")
    ax.grid(alpha=.3); ax.legend()
    fig.tight_layout()
    os.makedirs(a.plots, exist_ok=True)
    for ext in ("png", "pdf"): fig.savefig(os.path.join(a.plots, f"scaling_comparison.{ext}"), dpi=300)
    print("plots written to", os.path.abspath(a.plots))

if __name__ == "__main__":
    main()
