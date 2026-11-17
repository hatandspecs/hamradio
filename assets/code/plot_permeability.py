#!/usr/bin/env python3
"""Measured against published complex permeability for the three sleeve mixes.

Measured curves come from the single-sleeve RG-400 sweeps in
assets/data/ferrite-sleeve-2026-11-13/, de-embedded of their winding
capacitance and divided by w*N^2*L0.  One line per turn count: where the three
lie on top of each other the N^2 law holds, and where they fan apart it does
not.  Published curves are Fair-Rite's own.

  python3 plot_permeability.py ../images/diy-ferrite-sleeve-choke-design/permeability-measured.png
"""
import io, math, os, re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import choke_measured as C

SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
MEASURED, PUBLISHED, GRID = "#2a78d6", "#eb6834", "#e3e2de"
BANDS = [("80", 3.513), ("40", 7.187), ("20", 14.34), ("10", 28.356)]

def published(mix):
    """Fair-Rite complex permeability, cached beside the measurement data."""
    path = os.path.join(HERE, "..", "data", "fairrite", "%d.csv" % mix)
    txt = io.open(path, encoding="utf-8", errors="replace").read()
    v = [float(x) for x in re.findall(r"[0-9]*\.?[0-9]+(?:[Ee][+-]?[0-9]+)?", txt)]
    pts, i = [], 0
    while i + 2 < len(v):
        f, mr, mi = v[i], v[i+1], v[i+2]
        if 1e3 <= f <= 2e9 and mr >= 0 and mi >= 0:
            pts.append((f, mi)); i += 3
        else:
            i += 1
    return sorted(set(pts))

def measured(mix, n):
    """Single-sample spikes in the sweep are instrument noise, not material.
    A 5-point running median removes them without smoothing the curve."""
    raw = []
    for i, f in enumerate(C.FREQ):
        if not 1.2e6 <= f <= 29.5e6:
            continue
        r = C._CORE[(mix, n)][i].real
        raw.append((f, r / (2 * math.pi * f * n * n * C.L0)))
    out = []
    for i, (f, mu) in enumerate(raw):
        w = sorted(v for _, v in raw[max(0, i-2):i+3])
        med = w[len(w)//2]
        if med > 0:
            out.append((f, med))
    return out

def main(out_path):
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.5), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, mix in zip(axes, (31, 43, 75)):
        ax.set_facecolor(SURFACE)
        pub = [(f, m) for f, m in published(mix) if 1.2e6 <= f <= 29.5e6]
        ax.plot([f/1e6 for f, _ in pub], [m for _, m in pub],
                color=PUBLISHED, lw=2.4, ls=(0, (5, 2)), zorder=3,
                label="Fair-Rite published")
        for k, n in enumerate((1, 2, 3)):
            d = measured(mix, n)
            ax.plot([f/1e6 for f, _ in d], [m for _, m in d], color=MEASURED,
                    lw=1.6, alpha=(0.45, 0.7, 1.0)[k], zorder=4,
                    label="measured, 1 to 3 turns" if n == 1 else None)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(1.2, 30); ax.set_ylim(20, 3000)
        ax.set_xticks([b[1] for b in BANDS])
        ax.set_xticklabels([b[0] + " m" for b in BANDS], fontsize=9, color=INK2)
        ax.tick_params(axis="y", labelsize=9, colors=INK2, which="both")
        ax.grid(True, which="major", color=GRID, lw=0.8, zorder=0)
        ax.grid(True, which="minor", color=GRID, lw=0.4, alpha=0.6, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.set_title("mix %d" % mix, fontsize=12, color=INK, pad=8, loc="left")
    axes[0].set_ylabel("loss term $\\mu''$", fontsize=10, color=INK2)
    axes[0].legend(loc="lower left", frameon=False, fontsize=9,
                   labelcolor=INK2)
    fig.suptitle("Measured loss permeability against Fair-Rite's published curves, "
                 "25.9 mm sleeves",
                 fontsize=13, color=INK, x=0.011, ha="left", y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path, dpi=150, facecolor=SURFACE)
    print("wrote", out_path)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "permeability-measured.png")
