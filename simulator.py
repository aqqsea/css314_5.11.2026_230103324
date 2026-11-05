#!/usr/bin/env python3
"""Task 21 - Amdahl vs Gustafson parametric simulator.

Usage:
  python simulator.py                       # default sweep, writes CSV + plot
  python simulator.py --alphas 0.01 0.05 --pmax 4096 --outdir ../plots
Valid ranges: 1 <= P <= 65536, 0.001 <= alpha <= 0.20.
"""
import argparse, csv, os, sys

def amdahl(P, s):     return 1.0 / (s + (1.0 - s) / P)
def gustafson(P, a):  return P - a * (P - 1)

def core_counts(pmax):
    ps, p = [], 1
    while p <= pmax:
        ps.append(p); p *= 2
    if ps[-1] != pmax: ps.append(pmax)
    return ps

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--alphas", type=float, nargs="+", default=[0.001, 0.01, 0.04, 0.08, 0.20])
    ap.add_argument("--pmax", type=int, default=65536)
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plots"))
    ap.add_argument("--csv", default=None, help="CSV path (default: <outdir>/simulator_output.csv)")
    ap.add_argument("--no-plot", action="store_true")
    a = ap.parse_args()

    if not 1 <= a.pmax <= 65536: sys.exit("pmax must be in [1, 65536]")
    for x in a.alphas:
        if not 0.001 <= x <= 0.20: sys.exit(f"alpha {x} outside [0.001, 0.20]")
    os.makedirs(a.outdir, exist_ok=True)
    csv_path = a.csv or os.path.join(a.outdir, "simulator_output.csv")
    Ps = core_counts(a.pmax)

    rows = []
    for al in a.alphas:
        for P in Ps:
            sa, sg = amdahl(P, al), gustafson(P, al)
            rows.append(dict(alpha=al, P=P, S_amdahl=sa, S_gustafson=sg,
                             E_amdahl=sa / P, E_gustafson=sg / P,
                             amdahl_ceiling=1 / al, ratio_G_over_A=sg / sa))
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {csv_path}")

    if a.no_plot: return
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cmap = plt.get_cmap("viridis")
    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    for i, al in enumerate(a.alphas):
        c = cmap(i / max(1, len(a.alphas) - 1))
        ax[0].loglog(Ps, [gustafson(P, al) for P in Ps], "-", color=c, label=f"Gustafson α={al}")
        ax[0].loglog(Ps, [amdahl(P, al) for P in Ps], "--", color=c, label=f"Amdahl s={al}")
        ax[1].semilogx(Ps, [gustafson(P, al) / P for P in Ps], "-", color=c)
        ax[1].semilogx(Ps, [amdahl(P, al) / P for P in Ps], "--", color=c)
    ax[0].loglog(Ps, Ps, "k:", label="ideal S=P")
    ax[0].set(xlabel="processors P", ylabel="speedup", title="Weak (solid) vs strong (dashed) scaling")
    ax[0].legend(fontsize=7, ncol=2); ax[0].grid(True, which="both", alpha=.3)
    ax[1].set(xlabel="processors P", ylabel="efficiency E=S/P", title="Parallel efficiency", ylim=(0, 1.02))
    ax[1].grid(True, which="both", alpha=.3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        p = os.path.join(a.outdir, f"simulator_overlay.{ext}"); fig.savefig(p, dpi=200); print("wrote", p)

if __name__ == "__main__":
    main()
