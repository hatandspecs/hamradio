#!/usr/bin/env python3
"""RG-316 sleeve characterization and choke search, from the 2026-11-14 sweeps.

THE SEARCH RANKING IS FALSIFIED. DO NOT USE IT TO CHOOSE A BUILD.
    Three builds this search ranked highest were wound and swept on
    2026-11-14 and came in 24, 31 and 75 percent below prediction. Across
    eleven measured assemblies, five independent prediction routes all failed
    at 23 to 47 percent on worst-band resistance. Series summation itself is
    sound, measured to within 1 to 8 percent; what is wrong is the per-section
    impedances this script derives from single-sleeve bench sweeps, which were
    taken at a looser lead dressing (289 nH of fixture) than any assembly
    (455 nH). --search is retained to reproduce the article's record of the
    failure. The best measured choke is 316-2, #75@8T + #75@8T + #31@4T +
    #43@5T, at 6,706 ohms worst band.

Companion to choke_measured.py, which does the same for RG-400. Three mixes at
one, two, four, six, eight and ten turns, same fixture and clip separation as
the RG-400 set, so the two are directly comparable.

    Zcm      = 2*Z0*(1 - S21)/S21  -  Zref        subtraction, not division
    Z_core   = 1/(1/Zcm - j*w*Cp*N)                     stray removed
    mu''     = Re(Z_core)/(w * N^2 * L0)
    Z_sec    = Z_core*n_c / (1 + j*w*Cp*N*sqrt(n_c)*Z_core*n_c)
    Z_total  = sum over sections

WHAT THE SEARCH IS DRIVEN BY, AND WHY
    Not the raw per-frequency extraction. Deciding which turn counts to trust
    at each frequency defeated four tests, each recorded in the article:
    largest |Z| (a bad reference sample near 9.5 MHz spikes every DUT there),
    inductive-only (admits mix 75's post-resonance windings), low-edge peak
    (confuses mix 75's material relaxation with an LC resonance) and the
    reactance zero crossing (fires at 1.2 MHz for mix 75 because at 70 to 100
    ohms the sign of X is fixture noise).

    What survives is the ratio. Measured mu'' tracks the published shape at a
    mix-dependent fraction, flat to 5-9 percent with frequency and agreeing
    between the two cable datasets to a few percent. So the search uses
    k * published, with k measured over 1.9 to 14.2 MHz where both datasets
    extract cleanly. k is a property of the ferrite, not of the coax, and is
    deliberately NOT refitted per cable: doing that while using the other
    cable's Cp drags mix 31 from 0.91 to 0.68 and triples the spread, which is
    an over-correction and not a material result.

    Cp per turn IS a property of the cable and is fitted per mix below.

  python3 choke_rg316.py --measured          direct sums, no model
  python3 choke_rg316.py --search --cores 4
  python3 choke_rg316.py --cp-fit
"""
import argparse, io, itertools, math, os, re, statistics

Z0, MU0 = 50.0, 4e-7 * math.pi
OD, ID, H = 25.91e-3, 12.80e-3, 28.60e-3
L0 = (MU0 / (2 * math.pi)) * H * math.log(OD / ID)      # 4.034 nH
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "ferrite-sleeve-rg316-2026-11-14")
FAIR = os.path.join(HERE, "..", "data", "fairrite", "%d.csv")
REF = 26

# mix -> turns -> file. A turn is one pass through the bore.
DUT = {75: {10: 27, 8: 32, 6: 33, 4: 38, 2: 39, 1: 44},
       31: {10: 28, 8: 31, 6: 34, 4: 37, 2: 40, 1: 43},
       43: {10: 29, 8: 30, 6: 35, 4: 36, 2: 41, 1: 42}}
# Fitted per mix under series subtraction, see --cp-fit.
CP = {75: 0.48e-12, 31: 0.33e-12, 43: 0.26e-12}
# measured/published, from pre-resonance windings only. RG-400 independently
# gives 0.77 and 0.59, so k is a property of the ferrite and not of the coax.
# Mix 75 is ABSENT deliberately: every mix-75 winding in both datasets, down to
# one turn, is already past its impedance maximum at the 1 MHz start of the
# sweep, so neither dataset can supply a figure for it. A sweep from 100 kHz
# would. Until then it cannot appear in a design search.
K = {31: 0.80, 43: 0.60}
BANDS = [("160/80", 1.9e6), ("80", 3.5e6), ("40", 7.1e6), ("30", 10.1e6),
         ("20", 14.2e6), ("17", 18.1e6), ("15", 21.2e6), ("12", 24.9e6),
         ("10", 28.4e6)]


def read(n):
    f, s = [], []
    path = os.path.join(DATA, "SJ%06d.s2p" % n)
    for line in io.open(path, encoding="latin-1"):
        line = line.strip()
        if not line or line[0] in "!#":
            continue
        p = line.split()
        f.append(float(p[0])); s.append(complex(float(p[3]), float(p[4])))
    return f, s


FREQ, SREF = read(REF)


def _z(s):
    return [2 * Z0 * (1 - s[i]) / s[i] if abs(s[i]) > 1e-12 else complex(0)
            for i in range(len(FREQ))]


ZREF = _z(SREF)


def zmeas(mix, turns):
    """One measured sleeve with the fixture residual SUBTRACTED.

    Not divided. For a series element S21 = 2*Z0/(2*Z0+Z) and two series
    elements compose as Z1+Z2, which is not multiplicative in S21. Division is
    exact only for a cascaded two-port such as a delay line, and reference 26
    measures a lumped 289 nH. The two conventions agree below resonance and
    differ by a factor of 40 above it.
    """
    _, s = read(DUT[mix][turns])
    z = _z(s)
    return [z[i] - ZREF[i] for i in range(len(FREQ))]


def at(vals, ft):
    for i in range(len(FREQ) - 1):
        if FREQ[i] <= ft <= FREQ[i + 1]:
            t = (ft - FREQ[i]) / (FREQ[i + 1] - FREQ[i])
            return vals[i] + t * (vals[i + 1] - vals[i])
    return vals[-1] if ft > FREQ[-1] else vals[0]


def published(mix):
    txt = io.open(FAIR % mix, encoding="utf-8", errors="replace").read()
    v = [float(x) for x in re.findall(r"[0-9]*\.?[0-9]+(?:[Ee][+-]?[0-9]+)?", txt)]
    pts, i = [], 0
    while i + 2 < len(v):
        f, mr, mi = v[i], v[i + 1], v[i + 2]
        if 1e3 <= f <= 2e9 and mr >= 0 and mi >= 0:
            pts.append((f, mr, mi)); i += 3
        else:
            i += 1
    return sorted(set(pts))


PUB = {m: published(m) for m in DUT}


def mu(mix, ft):
    """k * published complex permeability."""
    p = PUB[mix]
    for i in range(len(p) - 1):
        if p[i][0] <= ft <= p[i + 1][0]:
            t = (ft - p[i][0]) / (p[i + 1][0] - p[i][0])
            mp = p[i][1] + t * (p[i + 1][1] - p[i][1])
            mpp = p[i][2] + t * (p[i + 1][2] - p[i][2])
            return K[mix] * mp, K[mix] * mpp
    e = p[-1] if ft > p[-1][0] else p[0]
    return K[mix] * e[1], K[mix] * e[2]


def section_z(stack, turns, ft):
    w = 2 * math.pi * ft
    acc = 0j
    for m in stack:
        mp, mpp = mu(m, ft)
        acc += complex(mp, -mpp)
    zc = 1j * w * turns * turns * L0 * acc
    cp = statistics.fmean(CP[m] for m in stack) * turns * (len(stack) ** 0.5)
    return 1 / (1 / zc + 1j * w * cp) if abs(zc) > 1e-12 else 0j


def build_z(sections, ft):
    return sum(section_z(st, n, ft) for st, n in sections)


def grade(sections):
    zs = [build_z(sections, ft) for _, ft in BANDS]
    return (1 if all(z.real >= abs(z.imag) for z in zs) else 0,
            min(z.real for z in zs)), zs


def label(sections):
    return " + ".join("%s@%dT" % ("+".join("#%d" % m for m in st), n)
                      for st, n in sections)


def cmd_cp_fit():
    """The value per mix that collapses the six turn counts onto one mu''."""
    print("Cp per turn, fitted by collapsing turn counts onto one mu'' curve\n")
    print("%-5s %12s %9s" % ("mix", "Cp/turn pF", "spread"))
    for mix in (75, 31, 43):
        Z = {n: zmeas(mix, n) for n in DUT[mix]}

        def spread(cp):
            out = []
            for i, f in enumerate(FREQ):
                if not 1.5e6 <= f <= 29e6:
                    continue
                w = 2 * math.pi * f
                vals = []
                for n in Z:
                    z = Z[n][i]
                    if abs(z) < 1e-9:
                        continue
                    y = 1 / z - 1j * w * cp * n
                    if abs(y) < 1e-15:
                        continue
                    v = (1 / y).real / (w * n * n * L0)
                    if v > 1:
                        vals.append(v)
                if len(vals) >= 4:
                    out.append(statistics.pstdev(vals) / statistics.fmean(vals))
            return statistics.median(out) if out else float("inf")

        best = min((x * 0.01e-12 for x in range(1, 121)), key=spread)
        print("%-5d %12.3f %8.1f%%" % (mix, best * 1e12, spread(best) * 100))
    print("\nRG-400 fitted 0.71 pF/turn for all three mixes on mix 31 alone,")
    print("over turn counts 1 to 3 only.")


def resonance(mix, turns):
    """Smoothed impedance maximum, used as a proxy for self-resonance.

    Smoothed because the reference sweep has one bad sample near 9.5 MHz and a
    raw maximum mistakes it for a resonance. It is a proxy and not a
    measurement, and mix 75 is the case where the proxy fails.
    """
    z = zmeas(mix, turns)
    mg = [abs(v) for v in z]
    sm = [sorted(mg[max(0, k - 2):k + 3])[len(mg[max(0, k - 2):k + 3]) // 2]
          for k in range(len(mg))]
    i = max(range(len(sm)), key=lambda k: sm[k])
    return FREQ[i] if i < len(FREQ) - 3 else float("inf")


def cmd_measured():
    """Direct sums of measured sleeves. No permeability model at all.

    Cells marked * have at least one winding above its own resonance. Those
    carry no information: the two de-embedding conventions differ by a factor
    of 40 there, two implementations of the same convention differ by 2, and an
    independent model calculation sits between all of them. They are printed
    only so the shape of the fall-off is visible, and must not be quoted.
    """
    print("Measured sleeves summed directly, fixture residual subtracted.")
    print("* = a constituent winding is past its own resonance: not data.\n")
    cands = [[(31, 8)], [(31, 6), (31, 8)], [(31, 6), (31, 8), (31, 8)]]
    print("%-26s %s %9s" % ("build", "".join("%8s" % b for b, _ in BANDS),
                            "worst ok"))
    for c in cands:
        fres = min(resonance(m, n) for m, n in c)
        cells, clean = [], []
        for _, ft in BANDS:
            tot = sum(at(zmeas(m, n), ft) for m, n in c)
            if ft >= fres:
                cells.append("%7.0f*" % tot.real)
            else:
                cells.append("%8.0f" % tot.real); clean.append(tot.real)
        name = " + ".join("#%d@%dT" % (m, n) for m, n in c)
        print("%-26s %s %9s" % (name, "".join(cells),
                                "%.0f" % min(clean) if clean else "none"))
    print("\nNothing in the article is quoted from a starred cell.")


def cmd_search(cores, max_sections, max_turns, top):
    types = [(st, n)
             for nc in range(1, cores + 1)
             for st in itertools.combinations_with_replacement(tuple(sorted(K)), nc)
             for n in range(1, max_turns + 1)]
    builds = []

    def rec(start, left, secs, acc):
        if acc:
            builds.append(tuple(acc))
        if not left or not secs:
            return
        for i in range(start, len(types)):
            st, n = types[i]
            if len(st) <= left:
                rec(i, left - len(st), secs - 1, acc + [(st, n)])
    rec(0, cores, max_sections, [])
    scored = sorted(((grade(b)[0], b) for b in builds), reverse=True)
    print("%d builds, up to %d cores, %d sections, %d turns.\n"
          % (len(builds), cores, max_sections, max_turns))
    for rank, ((rdom, worst), b) in enumerate(scored[:top], 1):
        _, zs = grade(b)
        print("%d. %s" % (rank, label(b)))
        print("   %d cores, %d sections, worst R %.0f ohm, R>=|X| everywhere: %s"
              % (sum(len(st) for st, _ in b), len(b), worst,
                 "yes" if rdom else "no"))
        print("   band %s" % "".join("%8s" % n for n, _ in BANDS))
        print("   R    %s" % "".join("%8.0f" % z.real for z in zs))
        print("   X    %s" % "".join("%8.0f" % z.imag for z in zs))
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cp-fit", action="store_true")
    ap.add_argument("--measured", action="store_true")
    ap.add_argument("--search", action="store_true")
    ap.add_argument("--cores", type=int, default=4)
    ap.add_argument("--max-sections", type=int, default=4)
    ap.add_argument("--max-turns", type=int, default=10)
    ap.add_argument("--top", type=int, default=3)
    a = ap.parse_args()
    if a.cp_fit:
        cmd_cp_fit()
    if a.measured:
        cmd_measured()
    if a.search or not (a.cp_fit or a.measured):
        print("WARNING: this ranking is falsified. Three builds it ranked "
              "highest measured\n         24, 31 and 75 percent below "
              "prediction. See the module docstring.\n")
        cmd_search(a.cores, a.max_sections, a.max_turns, a.top)


if __name__ == "__main__":
    main()
