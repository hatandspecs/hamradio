#!/usr/bin/env python3
"""Exhaustive search over sectioned ferrite-sleeve choke configurations.

Enumerates every way to split a core budget into sections, assign a ferrite
mix to each core, and pick a turn count for each section, then scores each
arrangement against a target band range.

A section is one winding of N turns through a stack of one or more sleeves.
Sections are in series, so their impedances add and their order along the tube
does not enter the model. Two builds that differ only in section order are
therefore the same build and are counted once.

    section type = (multiset of mixes in the stack, turns)
    build        = multiset of section types, total cores within budget

Turns run 1 to 4. Four is the bore limit for RG-400 in a 12.8 mm sleeve.

SCORING
-------
Ranked by the lowest resistance at any band center inside the target range,
with builds that keep R >= |X| on every band in range ranked above those that
do not. That is the grading used in the design article: resistance is the part
a feedline's own common-mode reactance cannot cancel, so a build that is
reactance-dominated somewhere in its range has not covered that band.

The impedance model, the permeability and the winding-capacitance assumption
all come from choke_sections.py. Everything that is uncertain there is equally
uncertain here, and a search over a model is a search over a model.

    python3 choke_search.py
    python3 choke_search.py --cp 0.8 --top 5 --markdown

Written for https://hatandspecs.github.io/hamradio/ , public domain.
"""

import argparse
import itertools
import math
import sys

import choke_sections as cs

MIXES = ['75', '31', '43', '46', '61']

# Target ranges and the core budget allowed for each.
VARIANTS = [
    ('80 m to 10 m', 3.5, 29.7, 4),
]


def section_types(max_stack, turns_range):
    """Every (stack, turns) a section can be, canonically ordered."""
    out = []
    for k in range(1, max_stack + 1):
        for stack in itertools.combinations_with_replacement(MIXES, k):
            for n in turns_range:
                out.append((stack, n))
    return out


def label(stype):
    stack, n = stype
    if len(stack) == 1:
        core = '#%s' % stack[0]
    elif len(set(stack)) == 1:
        core = '%d x #%s' % (len(stack), stack[0])
    else:
        core = '+'.join('#%s' % m for m in stack)
    return '%s %dT' % (core, n)


class Cache:
    """Impedance and flat resistance of each section type, precomputed."""

    def __init__(self, types, cp, freqs, mu_dir=None, cp_per_turn=None):
        self.types = types
        self.z = []
        self.nnc = []
        self.cores = []
        self.cp_of = []
        for stack, n in types:
            c = cs.cp_for(n, cp_per_turn) if cp_per_turn else cp
            secs = [cs.Section(m, n, 1, c, mu_dir) for m in stack]
            self.cp_of.append(c)
            # Stacked cores share one winding: permeabilities add.
            self.z.append(tuple(sum(s.z_core(f) for s in secs) for f in freqs))
            self.cores.append(len(stack))
            self.nnc.append(n * n * len(stack))
        self.cp = cp
        self.freqs = freqs

    def section_z(self, i):
        cp = self.cp_of[i]
        out = []
        for z, f in zip(self.z[i], self.freqs):
            w = 2 * math.pi * f
            out.append(z / (1 + 1j * w * cp * z))
        return tuple(out)


def enumerate_builds(cache, budget, exact=False, smin=1, smax=None):
    """Every multiset of section types within the core budget.

    exact requires the budget be spent in full rather than merely not
    exceeded; smin and smax bound the number of sections.
    """
    n = len(cache.types)
    smax = smax or budget
    out = []

    def walk(start, used, chosen):
        if (len(chosen) >= smin and len(chosen) <= smax
                and (used == budget or not exact)):
            out.append(tuple(chosen))
        if len(chosen) >= smax:
            return
        for i in range(start, n):
            c = cache.cores[i]
            if used + c <= budget:
                chosen.append(i)
                walk(i, used + c, chosen)
                chosen.pop()

    walk(0, 0, [])
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--cp', type=float,
                   help='fixed winding capacitance per section, pF, '
                        'overriding the per-turn model')
    p.add_argument('--cp-turn', type=float, default=0.18,
                   help='winding capacitance per turn, pF (default 0.18, '
                        'from the one measured choke)')
    p.add_argument('--top', type=int, default=3)
    p.add_argument('--detail', type=int, default=0,
                   help='print a band-by-band table for the top N builds')
    p.add_argument('--max-turns', type=int, default=4,
                   help='bore limit for the cable in use: 4 for RG-400, '
                        '5 for RG-303, 12 for RG-316 (default 4)')
    p.add_argument('--min-turns', type=int, default=1,
                   help='fewest turns a section may have (default 1)')
    p.add_argument('--cores', type=int,
                   help='core budget, overriding the per-variant default')
    p.add_argument('--exact-cores', action='store_true',
                   help='spend the whole budget rather than up to it')
    p.add_argument('--min-sections', type=int, default=1)
    p.add_argument('--max-sections', type=int)
    p.add_argument('--markdown', action='store_true')
    p.add_argument('--mu-dir',
                   help='directory of Fair-Rite <mix>.csv files, which '
                        'replaces the fitted permeability')
    p.add_argument('--mixes',
                   help='comma-separated subset of mixes to search, e.g. '
                        '31,43,46 to leave out the one whose relaxation is '
                        'assumed rather than fitted')
    p.add_argument('--fr75', type=float,
                   help='override mix 75 relaxation frequency, MHz. Its '
                        'default is assumed from Snoek rather than fitted '
                        'to a published impedance, and it decides the '
                        'answer, so it is worth varying')
    a = p.parse_args()
    if a.fr75:
        cs.FR['75'] = a.fr75 * 1e6
    if a.mixes:
        keep = [m.strip().lstrip('#') for m in a.mixes.split(',')]
        unknown = [m for m in keep if m not in MIXES]
        if unknown:
            raise SystemExit('unknown mix: %s' % ', '.join(unknown))
        MIXES[:] = [m for m in MIXES if m in keep]
    cp = (a.cp or 1.0) * 1e-12
    cpt = None if a.cp else a.cp_turn * 1e-12
    turns = range(a.min_turns, a.max_turns + 1)

    freqs = [fm * 1e6 for _, fm in cs.BANDS]
    names = [n for n, _ in cs.BANDS]
    mhz = [fm for _, fm in cs.BANDS]

    print('Exhaustive search over sectioned ferrite-sleeve chokes')
    print('  sleeve %.1f x %.1f x %.1f mm, L0 = %.3f nH'
          % (cs.OD * 1e3, cs.ID * 1e3, cs.H * 1e3, cs.L0 * 1e9))
    print('  mixes %s, turns %d to %d'
          % (', '.join('#' + m for m in MIXES), min(turns), max(turns)))
    print('  Cp %s'
          % ('%.2f pF per section, fixed' % a.cp if a.cp
             else '%.2f pF per turn, so %.2f pF at %d turns'
                  % (a.cp_turn, a.cp_turn * max(turns), max(turns))))
    print('  sections %d to %s, cores %s'
          % (a.min_sections, a.max_sections or 'budget',
             'exactly the budget' if a.exact_cores else 'up to the budget'))
    print('  permeability: %s' % cs.Permeability('31', a.mu_dir).source)
    print()

    for vname, lo, hi, budget in VARIANTS:
        if a.cores:
            budget = a.cores
        types = section_types(budget, turns)
        cache = Cache(types, cp, freqs, a.mu_dir, cpt)
        builds = enumerate_builds(cache, budget, a.exact_cores,
                                  a.min_sections, a.max_sections)
        zs = [cache.section_z(i) for i in range(len(types))]
        inband = [k for k, f in enumerate(mhz) if lo * 0.98 <= f <= hi * 1.02]

        scored = []
        for b in builds:
            tot = [sum(zs[i][k] for i in b) for k in inband]
            minr = min(z.real for z in tot)
            ok = all(z.real >= abs(z.imag) for z in tot)
            scored.append((ok, minr, b, tot))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)

        print('=' * 74)
        print('%s   %.1f to %.1f MHz   up to %d cores'
              % (vname, lo, hi, budget))
        print('  %d section types, %d distinct builds searched'
              % (len(types), len(builds)))
        print()
        rows = []
        for ok, minr, b, tot in scored[:a.top]:
            cores = sum(cache.cores[i] for i in b)
            nnc = sum(cache.nnc[i] for i in b)
            worst = names[inband[min(range(len(tot)),
                                     key=lambda k: tot[k].real)]]
            desc = ', '.join(label(types[i]) for i in b)
            rows.append((cores, len(b), desc, nnc, minr, worst,
                         max(abs(z) for z in tot), ok))
        if a.markdown:
            print('| Cores | Sections | Build, low to high | Sum N^2 n_c |'
                  ' Lowest in-band R, ohm | on |'
                  ' Peak &#124;Z&#124; in band, ohm | R over &#124;X&#124; |')
            print('|---|---|---|---|---|---|---|---|')
            for c, s_, d, nn, mr, w, pk, ok in rows:
                print('| %d | %d | %s | %d | %s | %s | %s | %s |'
                      % (c, s_, d, nn, format(int(round(mr)), ','), w,
                         format(int(round(pk)), ','),
                         'yes' if ok else 'no'))
        else:
            print('  %-5s %-8s %-30s %6s %9s %-7s %9s %6s'
                  % ('cores', 'sections', 'build', 'N2nc', 'min R', 'on',
                     'peak |Z|', 'R>|X|'))
            for c, s_, d, nn, mr, w, pk, ok in rows:
                print('  %-5d %-8d %-30s %6d %9.0f %-7s %9.0f %6s'
                      % (c, s_, d, nn, mr, w, pk, 'yes' if ok else 'no'))
        print()
        for rank, (ok, minr, b, tot) in enumerate(scored[:a.detail], 1):
            print('  #%d  %s' % (rank,
                                 ', '.join(label(types[i]) for i in b)))
            if a.markdown:
                print('')
                print('| Band | MHz | R, ohm | X, ohm | &#124;Z&#124;, ohm |'
                      ' R / &#124;Z&#124; |')
                print('|---|---|---|---|---|---|')
            for k, z in zip(inband, tot):
                if a.markdown:
                    print('| %s | %.1f | %s | %s | %s | %.2f |'
                          % (names[k], mhz[k], format(int(round(z.real)), ','),
                             ('+' if z.imag >= 0 else '-')
                             + format(int(round(abs(z.imag))), ','),
                             format(int(round(abs(z))), ','),
                             z.real / abs(z)))
                else:
                    print('      %-7s %6.1f MHz  R %8.0f  X %+9.0f  |Z| %8.0f'
                          % (names[k], mhz[k], z.real, z.imag, abs(z)))
            print()
        best_by_cores = {}
        for ok, minr, b, tot in scored:
            c = sum(cache.cores[i] for i in b)
            if c not in best_by_cores:
                best_by_cores[c] = (ok, minr, b)
        print('  best at each core count:')
        for c in sorted(best_by_cores):
            ok, minr, b = best_by_cores[c]
            print('    %d core%s: %6.0f ohm  %s  R>|X| %s'
                  % (c, ' ' if c == 1 else 's', minr,
                     ', '.join(label(types[i]) for i in b),
                     'yes' if ok else 'no'))
        print()


if __name__ == '__main__':
    main()
