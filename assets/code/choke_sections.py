#!/usr/bin/env python3
"""Sectioned ferrite-sleeve common-mode choke, modeled from complex permeability.

A tubular common-mode choke of this kind is several short windings in series on
cylindrical ferrite sleeves, each winding resonating at a different frequency.
This script models one section at a time and sums them.

    Z_core(f) = j*w * N^2 * n_c * L0 * (mu' - j*mu'')
    Z_sec(f)  = Z_core / (1 + j*w*Cp*Z_core)
    Z_total   = sum over sections

with L0 = (mu0/2pi) * h * ln(OD/ID), the core constant from the sleeve geometry
alone, N the turns in the section, n_c the cores stacked under that winding and
Cp the winding capacitance across it.

PERMEABILITY DATA
-----------------
Real Fair-Rite mu'/mu'' CSV files are used when they are present, named
<mix>.csv in --mu-dir with columns frequency_hz, mu_prime, mu_double_prime.
Without them the script falls back to a single-pole Debye model

    mu(f) = mu_i / (1 + j*f/f_r)

whose relaxation frequency f_r is fitted to the published single-pass
impedance at 100 MHz for mixes 31, 43 and 46, and to Snoek's product for 75,
which has no published figure here. THAT MODEL IS AN APPROXIMATION. It gets
the shape and the ordering of the mixes right and should not be quoted as a
datasheet value. Every table and chart says which source was used.

Cp is not measured. It is an assumption until one real section is swept, and
--cp-sweep shows how much the answer depends on it.

Written for https://hatandspecs.github.io/hamradio/ , public domain.
"""

import argparse
import cmath
import csv
import math
import os
import sys

MU0 = 4e-7 * math.pi

# Sleeve geometry, Fair-Rite 26xx102002 family: 25.9 OD, 12.8 ID, 28.6 long mm.
OD, ID, H = 25.9e-3, 12.8e-3, 28.6e-3
L0 = (MU0 / (2 * math.pi)) * H * math.log(OD / ID)

MU_I = {'75': 5000.0, '31': 1500.0, '43': 800.0, '46': 500.0,
        '61': 125.0}

# Published single-pass impedance magnitude at 100 MHz, ohm. Mix 75 has none.
Z1T_100M = {'31': 260.0, '43': 204.0, '46': 212.0}

BANDS = [('80 m', 3.5), ('40 m', 7.1), ('30 m', 10.1), ('20 m', 14.2),
         ('17 m', 18.1), ('15 m', 21.2), ('12 m', 24.9), ('10 m', 28.4)]


def fit_relaxation():
    """Debye f_r per mix, from the 100 MHz single-pass impedance."""
    fr = {}
    w = 2 * math.pi * 100e6
    for mix, z in Z1T_100M.items():
        mu_mag = z / (w * L0)                       # |Z| = w*L0*|mu|
        ratio = MU_I[mix] / mu_mag                  # = sqrt(1 + (f/fr)^2)
        fr[mix] = 100e6 / math.sqrt(max(ratio ** 2 - 1.0, 1e-9))
    # Snoek: mu_i * f_r is roughly constant within a material family. Mix 75
    # and mix 31 are both MnZn, so 31's product carries over.
    fr['75'] = MU_I['31'] * fr['31'] / MU_I['75']
    return fr


FR = fit_relaxation()


class Permeability:
    """mu(f) for one mix, from a CSV when there is one, else Debye."""

    def __init__(self, mix, mu_dir=None):
        self.mix = mix
        self.rows = None
        self.source = None
        if mu_dir:
            path = os.path.join(mu_dir, '%s.csv' % mix)
            if os.path.exists(path):
                self.rows = self._read(path)
                self.source = 'Fair-Rite CSV, %d points' % len(self.rows)
        if self.rows is None:
            if mix not in FR:
                raise SystemExit(
                    'mix %s has no fallback model, so it needs a measured '
                    'CSV. Pass --mu-dir pointing at %s.csv' % (mix, mix))
            self.source = 'Debye model, f_r = %.2f MHz' % (FR[mix] / 1e6)

    @staticmethod
    def _read(path):
        """Fair-Rite's published complex permeability files.

        They are not uniform. Some are CR-terminated with the header glued to
        the first data row, one is CRLF with a four-line preamble, and the mu
        symbols are in a non-UTF-8 encoding. So this ignores structure and
        takes any line whose first three comma-separated fields parse as
        numbers with a plausible frequency in the first.
        """
        with open(path, 'rb') as fh:
            text = fh.read().decode('latin-1')
        out = []
        for line in text.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
            parts = line.split(',')
            if len(parts) < 3:
                continue
            try:
                f, a, b = (float(parts[0]), float(parts[1]), float(parts[2]))
            except ValueError:
                continue
            if f < 1e3 or f > 1e12:
                continue
            out.append((f, a, b))
        out.sort()
        if not out:
            raise SystemExit('%s: no usable rows' % path)
        return out

    def __call__(self, f):
        if self.rows is None:
            return MU_I[self.mix] / (1 + 1j * f / FR[self.mix])
        xs = self.rows
        if f <= xs[0][0]:
            return complex(xs[0][1], -xs[0][2])
        if f >= xs[-1][0]:
            return complex(xs[-1][1], -xs[-1][2])
        lo, hi = 0, len(xs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if xs[mid][0] <= f:
                lo = mid
            else:
                hi = mid
        (f0, a0, b0), (f1, a1, b1) = xs[lo], xs[hi]
        t = (math.log(f / f0) / math.log(f1 / f0)) if f1 > f0 else 0.0
        return complex(a0 + t * (a1 - a0), -(b0 + t * (b1 - b0)))


class Section:
    """One winding: N turns through n_c stacked cores of one mix."""

    def __init__(self, mix, turns, cores=1, cp=2.0e-12, mu_dir=None):
        self.mix, self.turns, self.cores, self.cp = mix, turns, cores, cp
        self.mu = Permeability(mix, mu_dir)

    @property
    def label(self):
        stack = '%d x ' % self.cores if self.cores > 1 else ''
        return '%s#%s %dT' % (stack, self.mix, self.turns)

    @property
    def s_value(self):
        """N * sqrt(n_c * mu_i), the first-order peak-placement number."""
        return self.turns * math.sqrt(self.cores * MU_I[self.mix])

    def z_core(self, f):
        w = 2 * math.pi * f
        return 1j * w * self.turns ** 2 * self.cores * L0 * self.mu(f)

    def z(self, f):
        zc = self.z_core(f)
        w = 2 * math.pi * f
        return zc / (1 + 1j * w * self.cp * zc)


CP_PER_TURN = 0.18e-12
"""Winding capacitance per turn, farads.

Capacitance is not a constant per section. The ends of a winding approach each
other as turns are added, and the ends are what the capacitance is mostly
between, so it grows with turn count. A single scaling is the least that can
be said:

    Cp(N) = CP_PER_TURN * N

**This rests on one measurement.** The two-section choke in the transmit-grade
article, nine turns of RG-400 per section, fits a stray of 0.82 pF across the
pair, which is 1.64 pF per section in series, giving 0.18 pF per turn. That is
a different core, a W1JR crossover winding and one data point, so the slope is
an assumption and the sensitivity to it is reported rather than hidden.

Scaling with bore or cable diameter is left out deliberately. A narrower bore
crowds the turns and should raise it, which would roughly double the figure on
this sleeve, and a published four-section commercial choke fits lower than
that. The two anchors disagree, so neither correction is applied and the range
is carried as uncertainty instead.
"""


def cp_for(turns, cp_per_turn=CP_PER_TURN):
    return cp_per_turn * turns


def k_factor(mix, f, mu_dir=None):
    """Resistance one unit of N^2 * n_c buys from this mix at this frequency.

    The series resistance of a section is exactly

        R = w * N^2 * n_c * L0 * mu''(f)

    so it factors into a build term, N^2 * n_c, and a material term,
    2*pi*f*L0*mu''(f), which depends on the mix and nothing else. That makes
    the material term the only table needed to compare mixes, and N^2 * n_c
    the only number that describes what a build spends.

    This holds for any permeability data. It is not a model.
    """
    mu = Permeability(mix, mu_dir)(f)
    return 2 * math.pi * f * L0 * (-mu.imag)


def flat_resistance(sec):
    """Debye-only: the resistance a section settles at above its relaxation.

    With mu(f) = mu_i/(1 + j f/f_r), above f_r the loss term goes as
    mu'' -> mu_i * f_r / f, so R -> 2*pi * N^2 * n_c * L0 * mu_i * f_r, with
    no frequency in it.

    **Fair-Rite's measured curves do not behave that way**, so this number is
    meaningful only when the fallback model is in use. With real data the
    loss term rises with frequency for mixes 31, 43 and 46 and falls for 75,
    and k_factor is the quantity to use instead.
    """
    return (2 * math.pi * sec.turns ** 2 * sec.cores * L0
            * MU_I[sec.mix] * FR[sec.mix])


class Stack:
    """A section whose stacked sleeves are not all the same mix.

    Stacked sleeves share one winding, so their permeabilities add.
    """

    def __init__(self, mixes, turns, cp=1.0e-12, mu_dir=None):
        self.mixes = tuple(mixes)
        self.turns = turns
        self.cores = len(self.mixes)
        self.cp = cp
        self.parts = [Section(m, turns, 1, cp, mu_dir) for m in self.mixes]
        self.mix = self.mixes[0]
        self.mu = self.parts[0].mu

    @property
    def label(self):
        return '%s %dT' % ('+'.join('#%s' % m for m in self.mixes), self.turns)

    @property
    def s_value(self):
        return self.turns * math.sqrt(sum(MU_I[m] for m in self.mixes))

    def z_core(self, f):
        return sum(p.z_core(f) for p in self.parts)

    def z(self, f):
        zc = self.z_core(f)
        return zc / (1 + 1j * 2 * math.pi * f * self.cp * zc)


class Build:
    def __init__(self, name, span, sections):
        self.name, self.span, self.sections = name, span, sections

    def z(self, f):
        return sum(s.z(f) for s in self.sections)

    @property
    def flat_r(self):
        return sum(flat_resistance(s) for s in self.sections)

    @property
    def turn_sum(self):
        return sum(s.turns ** 2 * s.cores for s in self.sections)

    def peak(self, lo=0.5e6, hi=60e6, n=4000):
        best = (0.0, lo)
        for i in range(n):
            f = lo * (hi / lo) ** (i / (n - 1.0))
            m = abs(self.z(f))
            if m > best[0]:
                best = (m, f)
        return best[1], best[0]


def sweep(obj, lo=1e6, hi=60e6, n=1200):
    fs = [lo * (hi / lo) ** (i / (n - 1.0)) for i in range(n)]
    return fs, [obj.z(f) for f in fs]


# The candidate sections from the design tables, low S to high S.
def catalog(cp, mu_dir):
    spec = [('75', 4, 2), ('75', 4, 1), ('31', 4, 2), ('31', 4, 1),
            ('31', 3, 1), ('43', 4, 1), ('46', 4, 1), ('43', 3, 1),
            ('46', 3, 1), ('43', 2, 1), ('46', 2, 1)]
    return [Section(m, n, c, cp, mu_dir) for m, n, c in spec]


def builds(cp, mu_dir):
    """The builds the three cable searches pick, plus the nominal leader.

    cp is ignored for these: each section takes cp_for(turns), the per-turn
    model, because the whole point of the comparison is turn count.
    """
    def S(m, n, c=1):
        return Section(m, n, c, cp_for(n), mu_dir)

    def K(mixes, n):
        return Stack(mixes, n, cp_for(n), mu_dir)

    return [
        Build('RG-400, four sections', (3.5, 29.7),
              [S('75', 4), S('75', 4), S('31', 4), S('31', 4)]),
        Build('RG-400, two sections', (3.5, 29.7),
              [S('75', 4), K(('75', '31', '31'), 4)]),
        Build('RG-303, four sections', (3.5, 29.7),
              [S('75', 5), S('75', 5), S('31', 5), S('31', 5)]),
        Build('RG-316, four sections', (3.5, 29.7),
              [S('75', 8), S('31', 6), S('31', 6), S('43', 6)]),
    ]


def band_rows(obj, span=None):
    out = []
    for name, fm in BANDS:
        z = obj.z(fm * 1e6)
        inband = span is None or (span[0] * 0.98 <= fm <= span[1] * 1.02)
        out.append((name, fm, z, inband))
    return out


def report_section(sec):
    print('-' * 70)
    print('%s   S = %.0f   Cp = %.2f pF' % (sec.label, sec.s_value,
                                            sec.cp * 1e12))
    print('  permeability: %s' % sec.mu.source)
    fs, zs = sweep(sec)
    i = max(range(len(zs)), key=lambda k: abs(zs[k]))
    print('  peak |Z| %.0f ohm at %.2f MHz' % (abs(zs[i]), fs[i] / 1e6))
    print('  %-7s %9s %10s %9s' % ('band', 'R ohm', 'X ohm', '|Z| ohm'))
    for name, fm, z, _ in band_rows(sec):
        print('  %-7s %9.0f %+10.0f %9.0f' % (name, z.real, z.imag, abs(z)))


def report_build(b):
    print('=' * 70)
    print('%s' % b.name)
    print('  sections, low to high: %s'
          % ', '.join(s.label for s in b.sections))
    print('  S values: %s' % ' / '.join('%.0f' % s.s_value for s in b.sections))
    print('  cores used: %d' % sum(s.cores for s in b.sections))
    print('  sum of N^2 * n_c: %d' % b.turn_sum)
    print('  flat resistance if nothing shunted it: %.0f ohm' % b.flat_r)
    fpk, zpk = b.peak()
    print('  peak |Z| %.0f ohm at %.2f MHz' % (zpk, fpk / 1e6))
    print()
    head = '  %-7s %9s %10s %9s %8s  %s' % ('band', 'R ohm', 'X ohm',
                                            '|Z| ohm', 'R/|Z|', 'in range')
    print(head)
    worst_r, worst_band = None, None
    for name, fm, z, inband in band_rows(b, b.span):
        print('  %-7s %9.0f %+10.0f %9.0f %8.2f  %s'
              % (name, z.real, z.imag, abs(z), z.real / abs(z),
                 'yes' if inband else '.'))
        if inband and (worst_r is None or z.real < worst_r):
            worst_r, worst_band = z.real, name
    print()
    print('  lowest R inside the target range: %.0f ohm on %s'
          % (worst_r, worst_band))
    rx = [(n, z) for n, fm, z, ib in band_rows(b, b.span) if ib
          and z.real < abs(z.imag)]
    if rx:
        print('  reactance exceeds resistance on: %s'
              % ', '.join(n for n, _ in rx))
    else:
        print('  resistance exceeds reactance on every band in range')
    return worst_r


# ---------------------------------------------------------------- plotting
INK, MUTED, GRID = '#1b1b1a', '#6b6b66', '#d8d8d2'
C_MAG, C_R, C_X = '#1f77b4', '#d9603b', '#2a9d7f'
FACE = '#fcfcfb'


def _axis(ax, lo, hi):
    ax.set_xscale('log')
    ax.set_xlim(lo, hi)
    ax.grid(axis='y', color=GRID, lw=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8.5)


def plot_permeability(out, mu_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 6.4), facecolor=FACE)
    fs = [1e5 * (1e3) ** (i / 399.0) for i in range(400)]
    for ax, mix in zip(axes.ravel(), ('75', '31', '43', '46')):
        mu = Permeability(mix, mu_dir)
        vals = [mu(f) for f in fs]
        ax.plot([f / 1e6 for f in fs], [v.real for v in vals], lw=2.0,
                color=C_MAG, label="mu'")
        ax.plot([f / 1e6 for f in fs], [-v.imag for v in vals], lw=1.8,
                ls='--', color=C_R, label='mu"')
        ax.set_yscale('log')
        _axis(ax, 0.1, 100)
        ax.set_title('mix %s, mu_i %d' % (mix, MU_I[mix]), fontsize=9.5,
                     color=INK, loc='left')
        ax.set_facecolor(FACE)
        neg = [f for f, v in zip(fs, vals) if v.real < 0]
        if neg:
            ax.annotate("mu' turns negative\nabove %.1f MHz" % (neg[0] / 1e6),
                        (neg[0] / 1e6, ax.get_ylim()[0]), xytext=(6, 26),
                        textcoords='offset points', fontsize=8,
                        color=C_MAG)
    axes[0][0].legend(fontsize=8.5, frameon=False, loc='lower left')
    for ax in axes[1]:
        ax.set_xlabel('MHz', fontsize=9, color=MUTED)
    src = Permeability('31', mu_dir).source
    title = ('Complex permeability, Fair-Rite measured data'
             if 'CSV' in src else 'Complex permeability, fallback model')
    fig.suptitle(title, fontsize=11.5, color=INK, x=0.012, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out, dpi=150, facecolor=FACE)
    print('wrote %s' % out)


def plot_sections(secs, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9.5, 5.4), facecolor=FACE)
    cmap = plt.get_cmap('viridis')
    for i, sec in enumerate(secs):
        fs, zs = sweep(sec)
        ax.plot([f / 1e6 for f in fs], [abs(z) for z in zs], lw=1.8,
                color=cmap(i / max(len(secs) - 1, 1)),
                label='%s  S=%.0f' % (sec.label, sec.s_value))
    ax.axhline(5000, color=MUTED, lw=0.9, ls=(0, (6, 4)))
    ax.annotate('5 kohm', (1.1, 5000), xytext=(0, 5),
                textcoords='offset points', fontsize=8.5, color=MUTED)
    _axis(ax, 1, 60)
    ax.set_facecolor(FACE)
    ax.set_ylabel('|Z| ohm', fontsize=9, color=MUTED)
    ax.set_xlabel('MHz', fontsize=9, color=MUTED)
    ax.legend(fontsize=8, frameon=False, ncol=2, loc='upper right')
    fig.suptitle('Modeled impedance of each candidate section',
                 fontsize=11.5, color=INK, x=0.012, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out, dpi=150, facecolor=FACE)
    print('wrote %s' % out)


def plot_builds(bs, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows = (len(bs) + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(11, 3.2 * rows),
                             facecolor=FACE, squeeze=False)
    flat = axes.ravel()
    for ax, b in zip(flat, bs):
        fs, zs = sweep(b)
        mhz = [f / 1e6 for f in fs]
        ax.axhline(5000, color=MUTED, lw=0.9, ls=(0, (6, 4)))
        ax.axhline(0, color=GRID, lw=1.0)
        ax.axvspan(b.span[0], b.span[1], color=C_MAG, alpha=0.05)
        ax.plot(mhz, [z.imag for z in zs], lw=1.5, ls=':', color=C_X,
                label='X')
        ax.plot(mhz, [z.real for z in zs], lw=1.5, ls='--', color=C_R,
                label='R')
        ax.plot(mhz, [abs(z) for z in zs], lw=2.2, color=C_MAG, label='|Z|')
        _axis(ax, 1, 60)
        ax.set_facecolor(FACE)
        ax.set_title('%s\n%s' % (b.name,
                                 ', '.join(s.label for s in b.sections)),
                     fontsize=9, color=INK, loc='left')
    for ax in flat[len(bs):]:
        ax.set_visible(False)
    flat[0].legend(fontsize=8.5, frameon=False, loc='lower left')
    for ax in flat[:len(bs)]:
        ax.set_ylabel('ohm', fontsize=8.5, color=MUTED)
        ax.set_xlabel('MHz', fontsize=8.5, color=MUTED)
    fig.suptitle('Modeled R, X and |Z| for each build, shaded over its '
                 'target range', fontsize=11.5, color=INK, x=0.008, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(out, dpi=150, facecolor=FACE)
    print('wrote %s' % out)


def plot_build_detail(b, out):
    """One build on its own, R, X and |Z|, in the style of the bench sweeps."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9.5, 5.6), facecolor=FACE)
    fs, zs = sweep(b, 1e6, 60e6, 1500)
    mhz = [f / 1e6 for f in fs]
    ax.axvspan(b.span[0], b.span[1], color=C_MAG, alpha=0.05)
    ax.axhline(5000, color=MUTED, lw=0.9, ls=(0, (6, 4)))
    ax.axhline(0, color=GRID, lw=1.0)
    debye = 'CSV' not in b.sections[0].mu.source
    if debye:
        ax.axhline(b.flat_r, color=C_R, lw=0.9, ls=(0, (2, 3)), alpha=0.8)
    ax.plot(mhz, [z.imag for z in zs], lw=1.6, ls=':', color=C_X, label='X')
    ax.plot(mhz, [z.real for z in zs], lw=1.8, ls='--', color=C_R, label='R')
    ax.plot(mhz, [abs(z) for z in zs], lw=2.4, color=C_MAG, label='|Z|')
    fpk, zpk = b.peak()
    ax.plot([fpk / 1e6], [zpk], 'o', ms=6, color=C_MAG, mec='white', mew=1.5,
            zorder=5)
    ax.annotate('peak |Z| %.1f kohm\nat %.1f MHz' % (zpk / 1000, fpk / 1e6),
                (fpk / 1e6, zpk), xytext=(8, 6), textcoords='offset points',
                fontsize=8.5, color=INK)
    if debye:
        ax.annotate('flat R ceiling %.1f kohm' % (b.flat_r / 1000),
                    (1.15, b.flat_r), xytext=(0, 5),
                    textcoords='offset points', fontsize=8.5, color=C_R)
    ax.annotate('5 kohm', (56, 5000), xytext=(0, 6), ha='right',
                textcoords='offset points', fontsize=8.5, color=MUTED)
    _axis(ax, 1, 60)
    if debye:
        ax.set_ylim(top=b.flat_r * 1.10)
    ax.set_facecolor(FACE)
    ax.set_ylabel('ohm', fontsize=9, color=MUTED)
    ax.set_xlabel('MHz', fontsize=9, color=MUTED)
    ax.legend(fontsize=9, frameon=False, loc='lower left')
    fig.suptitle('%s: %s' % (b.name,
                             ', '.join(s.label for s in b.sections)),
                 fontsize=11.5, color=INK, x=0.012, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.945))
    fig.savefig(out, dpi=150, facecolor=FACE)
    print('wrote %s' % out)


def plot_contributions(b, out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=FACE)
    fs = [1e6 * 60 ** (i / 999.0) for i in range(1000)]
    mhz = [f / 1e6 for f in fs]
    cmap = plt.get_cmap('viridis')
    for i, s in enumerate(b.sections):
        col = cmap(i / max(len(b.sections) - 1, 1))
        axes[0].plot(mhz, [abs(s.z(f)) for f in fs], lw=1.6, color=col,
                     label=s.label)
        axes[1].plot(mhz, [s.z(f).imag for f in fs], lw=1.6, color=col,
                     label=s.label)
    axes[0].plot(mhz, [abs(b.z(f)) for f in fs], lw=2.4, color=C_MAG,
                 label='total |Z|')
    axes[1].plot(mhz, [b.z(f).imag for f in fs], lw=2.4, color=C_MAG,
                 label='total X')
    axes[1].axhline(0, color=GRID, lw=1.0)
    for ax, lab, loc in zip(axes, ('|Z| ohm', 'X ohm'),
                            ('upper left', 'lower left')):
        _axis(ax, 1, 60)
        ax.set_facecolor(FACE)
        ax.set_ylabel(lab, fontsize=9, color=MUTED)
        ax.set_xlabel('MHz', fontsize=9, color=MUTED)
        ax.legend(fontsize=8, frameon=False, loc=loc)
    axes[0].set_title('each section and the sum', fontsize=9.5, color=INK,
                      loc='left')
    axes[1].set_title('reactance of each section and the sum',
                      fontsize=9.5, color=INK, loc='left')
    fig.suptitle('Where the sections of %s contribute' % b.name,
                 fontsize=11.5, color=INK, x=0.008, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out, dpi=150, facecolor=FACE)
    print('wrote %s' % out)


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--cp', type=float, default=1.0,
                   help='winding capacitance per section, pF (default 1.0)')
    p.add_argument('--mu-dir', help='directory of Fair-Rite <mix>.csv files')
    p.add_argument('--cp-sweep', action='store_true',
                   help='repeat every build at 1, 2 and 4 pF')
    p.add_argument('--sections', action='store_true',
                   help='also print a table per candidate section')
    p.add_argument('--plot-dir', help='write the PNGs here')
    a = p.parse_args()
    cp = a.cp * 1e-12

    print('Sleeve %.1f x %.1f x %.1f mm, L0 = %.3f nH per turn^2 per unit mu'
          % (OD * 1e3, ID * 1e3, H * 1e3, L0 * 1e9))
    src = Permeability('31', a.mu_dir).source
    print('Permeability source: %s' % src)
    if 'Debye' in src:
        print('  f_r fitted per mix: %s'
              % ', '.join('#%s %.2f MHz' % (m, FR[m] / 1e6)
                          for m in ('75', '31', '43', '46')))
        print('  This is a model, not datasheet data. See the docstring.')
    print('Winding capacitance assumed: %.2f pF per section, not measured'
          % a.cp)
    print()

    secs = catalog(cp, a.mu_dir)
    if a.sections:
        for s in secs:
            report_section(s)
        print()

    bs = builds(cp, a.mu_dir)
    for b in bs:
        report_build(b)
        print()

    if a.cp_sweep:
        print('=' * 70)
        print('Sensitivity to the assumed winding capacitance')
        print('  %-40s %9s %9s %9s'
              % ('build', '0.5 pF', '1 pF', '2 pF'))
        for name in [b.name for b in bs]:
            cells = []
            for trial in (0.5e-12, 1e-12, 2e-12):
                b = [x for x in builds(trial, a.mu_dir) if x.name == name][0]
                worst = min(z.real for _, fm, z, ib in band_rows(b, b.span)
                            if ib)
                cells.append(worst)
            print('  %-40s %9.0f %9.0f %9.0f' % (name, *cells))
        print('  lowest modeled R inside each target range, ohm')
        print()

    if a.plot_dir:
        d = a.plot_dir
        plot_permeability(os.path.join(d, 'permeability-model.png'), a.mu_dir)
        plot_sections(secs, os.path.join(d, 'sections.png'))
        plot_builds(bs, os.path.join(d, 'variants.png'))
        byname = {b.name: b for b in bs}
        plot_contributions(byname['RG-400, four sections'],
                           os.path.join(d, 'section-contributions.png'))
        plot_build_detail(byname['RG-400, four sections'],
                          os.path.join(d, 'build-rg400.png'))
        plot_build_detail(byname['RG-303, four sections'],
                          os.path.join(d, 'rg303-option.png'))
        plot_build_detail(byname['RG-316, four sections'],
                          os.path.join(d, 'rg316-option.png'))


if __name__ == '__main__':
    main()
