#!/usr/bin/env python3
"""Sectioned ferrite-sleeve choke design from measured single-sleeve sweeps.

Unlike choke_search.py, which models sections from published complex
permeability, this builds every section out of a sleeve that was actually
measured: mixes 75, 31 and 43 at one, two and three turns of RG-400, taken
2026-11-13 and stored in assets/data/ferrite-sleeve-2026-11-13/.

The only fitted quantity is the stray capacitance per turn, 0.71 pF, obtained
by finding the value that collapses mix 31's three turn counts onto a single
mu'' curve (2.8 percent spread).  Mix 43 and mix 75 do not collapse, for
reasons discussed in the article, so mix 31's figure is used for all three.

A four-turn section is extrapolated by the square law off the three-turn
measurement, derated for mix 75 by its own measured per-turn efficiency.  No
sleeve has been measured at four turns.

  python3 choke_measured.py --sleeves 4
  python3 choke_measured.py --sleeves 4 --turns 1 2 3 4 --max-sections 4
  python3 choke_measured.py --profile '31@3T x4'
"""
import argparse, cmath, io, math, os, sys

Z0 = 50.0
MU0 = 4e-7 * math.pi
OD, ID, H = 25.91e-3, 12.80e-3, 28.60e-3
L0 = (MU0 / (2 * math.pi)) * H * math.log(OD / ID)      # 4.034 nH
CP_PER_TURN = 0.71e-12
STACK_ALPHA = 0.5          # Cp grows as N * n_c**alpha; fitted to one stacked build

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "data", "ferrite-sleeve-2026-11-13")
REF_FILE = 26
DUT = {(75, 3): 17, (31, 3): 18, (43, 3): 19, (43, 2): 20, (31, 2): 21,
       (75, 2): 22, (75, 1): 23, (31, 1): 24, (43, 1): 25}

BANDS = [("80 m", 3.513e6), ("40 m", 7.187e6), ("30 m", 10.130e6),
         ("20 m", 14.340e6), ("17 m", 18.110e6), ("15 m", 21.060e6),
         ("12 m", 24.930e6), ("10 m", 28.356e6)]


def read_s2p(n):
    freq, s21 = [], []
    with io.open(os.path.join(DATA, "SJ%06d.s2p" % n)) as fh:
        for line in fh:
            line = line.strip()
            if not line or line[0] in "!#":
                continue
            p = line.split()
            freq.append(float(p[0]))
            s21.append(complex(float(p[3]), float(p[4])))
    return freq, s21


FREQ, SREF = read_s2p(REF_FILE)


def _interp(vals, ft):
    for i in range(len(FREQ) - 1):
        if FREQ[i] <= ft <= FREQ[i + 1]:
            t = (ft - FREQ[i]) / (FREQ[i + 1] - FREQ[i])
            return vals[i] + t * (vals[i + 1] - vals[i])
    return vals[-1] if ft > FREQ[-1] else vals[0]


# measured sleeve impedance, then the same with its own stray removed
_Z, _CORE = {}, {}
for key, num in DUT.items():
    _, s = read_s2p(num)
    z = [2 * Z0 * (1 - s[i] / SREF[i]) / (s[i] / SREF[i]) for i in range(len(FREQ))]
    _Z[key] = z
    _CORE[key] = [1 / (1 / z[i] - 1j * 2 * math.pi * FREQ[i] * CP_PER_TURN * key[1])
                  for i in range(len(FREQ))]


def core_one(mix, turns, ft):
    """One sleeve at `turns` passes, stray capacitance removed."""
    if turns <= 3:
        return _interp(_CORE[(mix, turns)], ft)
    z3 = _interp(_CORE[(mix, 3)], ft)
    scale = (turns / 3.0) ** 2
    if mix == 75:                       # this mix loses efficiency as turns rise
        r1 = _interp(_CORE[(75, 1)], ft).real
        r3 = _interp(_CORE[(75, 3)], ft).real
        scale *= max(0.5, (r3 / 9.0) / (r1 if r1 > 1 else 1))
    return z3 * scale


def section_z(mix, n_cores, turns, ft):
    zc = core_one(mix, turns, ft) * n_cores
    cp = CP_PER_TURN * turns * (n_cores ** STACK_ALPHA)
    return 1 / (1 / zc + 1j * 2 * math.pi * ft * cp)


def build_z(sections, ft):
    return sum(section_z(m, nc, n, ft) for m, nc, n in sections)


def profile(sections):
    return [(bn, build_z(sections, ft)) for bn, ft in BANDS]


def worst_R(sections):
    return min(z.real for _, z in profile(sections))


def label(sections):
    return " + ".join("%dx#%d@%dT" % (nc, m, n) if nc > 1 else "#%d@%dT" % (m, n)
                      for m, nc, n in sections)


def enumerate_builds(total, max_sections, turns, stacks, mixes):
    types = [(m, nc, n) for m in mixes for nc in stacks for n in turns]
    out = []

    def rec(start, left, acc):
        if left == 0:
            if acc:
                out.append(tuple(acc))
            return
        if len(acc) >= max_sections:
            return
        for i in range(start, len(types)):
            if types[i][1] <= left:
                acc.append(types[i])
                rec(i, left - types[i][1], acc)
                acc.pop()
    rec(0, total, [])
    return out


def print_profile(sections):
    prof = profile(sections)
    print("     " + "".join("%9s" % bn for bn, _ in prof))
    print("   R " + "".join("%9.0f" % z.real for _, z in prof))
    print("   X " + "".join("%+9.0f" % z.imag for _, z in prof))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sleeves", type=int, default=4, help="total sleeves (default 4)")
    ap.add_argument("--max-sections", type=int, default=6)
    ap.add_argument("--turns", type=int, nargs="+", default=[1, 2, 3],
                    help="turn counts allowed per section (4 extrapolates)")
    ap.add_argument("--stacks", type=int, nargs="+", default=[1, 2, 3],
                    help="sleeves per section allowed; pass 1 to forbid stacking")
    ap.add_argument("--mixes", type=int, nargs="+", default=[31, 43, 75])
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--sleeves-table", action="store_true",
                    help="print the measured single-sleeve impedances and exit")
    args = ap.parse_args()

    if args.sleeves_table:
        for mix in sorted(set(k[0] for k in DUT)):
            print("mix %d" % mix)
            print("%6s" % "band" + "".join("%21s" % ("N=%d" % n) for n in (1, 2, 3)))
            for bn, ft in BANDS:
                row = ""
                for n in (1, 2, 3):
                    z = _interp(_Z[(mix, n)], ft)
                    row += "%8.0f%+7.0f%6.0f" % (z.real, z.imag, abs(z))
                print("%6s %s" % (bn, row))
            print()
        return

    builds = enumerate_builds(args.sleeves, args.max_sections, args.turns,
                              args.stacks, args.mixes)
    if not builds:
        sys.exit("no arrangement fits those constraints")
    ranked = sorted(((worst_R(b), b) for b in builds), key=lambda x: -x[0])
    print("%d sleeves, %s turns, %d arrangements"
          % (args.sleeves, args.turns, len(builds)))
    for rank, (w, b) in enumerate(ranked[:args.top], 1):
        print("\n%d. %-40s worst R %6.0f ohm" % (rank, label(b), w))
        print_profile(b)


if __name__ == "__main__":
    main()
