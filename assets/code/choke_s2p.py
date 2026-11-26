#!/usr/bin/env python3
"""Common-mode choke impedance from a series-through .s2p sweep.

A common-mode choke measured series-through between two 50 ohm VNA ports
presents

    Zcm = 2 * Z0 * (1 - S21) / S21

with S21 complex and linear. Magnitude alone is not enough to grade a choke:
a winding can show 6 kohm of mostly reactance, which can series-resonate with
the feedline's own common-mode reactance and make things worse. This script
keeps the real and imaginary parts separate so R and X can be read off.

Usage
-----
    python3 choke_s2p.py SWEEP.s2p [MORE.s2p ...]
    python3 choke_s2p.py --plot out.png SWEEP.s2p
    python3 choke_s2p.py --bands 3.5,7.1,14.2 SWEEP.s2p

Options
-------
    --plot FILE    write a PNG of R, X and |Z| (needs matplotlib)
    --bands LIST   comma-separated MHz instead of the default band centers
    --z0 OHMS      port reference impedance (default: from the file, else 50)
    --csv FILE     write the full swept R/X/|Z| table
    --ref SHORT    remove a fixture reference sweep
    --ref-mode M   auto (default), subtract or divide
    --style MODE   rxz (default: R, X, |Z|) or pass (R vs |X|, shaded)
    --xzero MODE   which X = 0 crossing to mark: downward or first
    --label TEXT   panel title instead of the file name

HOW THE REFERENCE IS REMOVED DEPENDS ON WHAT THE REFERENCE IS
    There is no single right answer, and picking the wrong one is worth
    hundreds of ohms in the R/X split, which is the half a grade depends on.

    divide    exact for a DELAY. A matched line contributes phase at unit
              magnitude, and dividing by a unit-magnitude phasor removes it
              leaving Z untouched.
    subtract  exact for a LUMPED SERIES IMPEDANCE. Two series elements add as
              Z1 + Z2, which is not multiplicative in S21: dividing returns
              Z/(1 + Za/(2*Z0)), which is not Z - Za.

    `auto`, the default, fits both models to the reference sweep over 8 to
    29 MHz and uses whichever matches, printing which and by how much. The
    discriminator is |S21|: a delay holds it at 1, a lumped reactance drops it
    as frequency rises. Measured on this project's own fixtures, the compact
    short with the fixture ends brought together is a 0.85 ns delay and wants
    division, while a long wire spanning a build's geometry is a 450 nH lumped
    inductance and wants subtraction. Two fixtures, two answers, and the
    fixture decides.

Reads Touchstone 1.x two-port files in RI, MA or DB format, any frequency
unit. Only S21 is used, so a one-path two-port sweep (S12 and S22 left at
zero, which is what a NanoVNA writes) is fine.

Written for https://hatandspecs.github.io/hamradio/ , public domain. The
method and the measurements it was written against are in "Common-Mode
Chokes: Why They Matter, Where They Go, and How to Bench-Test Them".
"""

import argparse
import cmath
import csv
import math
import sys

# Band centers used for the summary table, in MHz.
DEFAULT_BANDS = [1.9, 3.5, 7.1, 10.1, 14.2, 18.1, 21.2, 24.9, 28.4]

UNITS = {'HZ': 1.0, 'KHZ': 1e3, 'MHZ': 1e6, 'GHZ': 1e9}


def read_touchstone(path):
    """Return (freqs_hz, s11, s21, z0). Touchstone 1.x, two-port."""
    unit, fmt, z0 = 'GHZ', 'MA', 50.0
    freqs, s11, s21 = [], [], []

    with open(path) as fh:
        for raw in fh:
            line = raw.split('!', 1)[0].strip()
            if not line:
                continue

            if line.startswith('#'):
                tok = line[1:].upper().split()
                i = 0
                while i < len(tok):
                    t = tok[i]
                    if t in UNITS:
                        unit = t
                    elif t in ('RI', 'MA', 'DB'):
                        fmt = t
                    elif t == 'R' and i + 1 < len(tok):
                        z0 = float(tok[i + 1])
                        i += 1
                    i += 1
                continue

            parts = line.split()
            if len(parts) < 5:
                continue
            try:
                vals = [float(p) for p in parts]
            except ValueError:
                continue

            # f  S11a S11b  S21a S21b  [S12a S12b  S22a S22b]
            freqs.append(vals[0] * UNITS[unit])

            def conv(a, b):
                if fmt == 'RI':
                    return complex(a, b)
                if fmt == 'MA':
                    return cmath.rect(a, math.radians(b))
                return cmath.rect(10.0 ** (a / 20.0), math.radians(b))

            s11.append(conv(vals[1], vals[2]))
            s21.append(conv(vals[3], vals[4]))

    if not freqs:
        raise SystemExit('%s: no data rows found' % path)
    return freqs, s11, s21, z0


def zcm(s21, z0):
    """Common-mode impedance from a series-through S21.

    The G3TXQ / K9YC series-through result. It assumes the fixture adds no
    shunt admittance at either port.
    """
    if s21 == 0:
        return complex(float('inf'), 0.0)
    return 2.0 * z0 * (1.0 - s21) / s21


def zcm_y21(s11, s21, z0):
    """Common-mode impedance by the Y21 method (K6JCA / W1QG).

        Zdut = Z0 * (S11 + S22 + S11*S22 - S12*S21 + 1) / (2 * S21)

    Modeling the fixture as a pi network, Y21 is the series branch alone, so
    this cancels the shunt-to-ground parasitics at both ports that the plain
    series-through formula folds into the answer.

    It needs a full two-port sweep. A NanoVNA measures only S11 and S21, so
    this uses S12 = S21 (exact for any reciprocal passive network) and
    S22 = S11 (true only if choke and fixture are symmetric end to end).
    Treat the result as a cross-check on the series-through number rather
    than as a better measurement: if the two agree, the port shunts are too
    small to matter, which is the useful thing to know.

    What it cannot remove is capacitance directly across the DUT, input
    connector to output connector. That is electrically part of the choke
    and only geometry will shift it.
    """
    if s21 == 0:
        return complex(float('inf'), 0.0)
    s12, s22 = s21, s11
    return z0 * (s11 + s22 + s11 * s22 - s12 * s21 + 1.0) / (2.0 * s21)


def port_shunt(s11, s21, z0, f):
    """The pi model's input shunt, as a capacitance in pF, or None."""
    num = z0 * (2.0 * s11 + s11 * s11 - s21 * s21 + 1.0)
    den = 1.0 - s11 * s11 + s21 * s21 - 2.0 * s21
    if den == 0:
        return None
    z = num / den
    if z.imag >= 0:
        return None
    return 1.0 / (2 * math.pi * f * -z.imag) * 1e12


def at(freqs, values, f_target):
    """Linear interpolation of a complex series onto one frequency."""
    if f_target <= freqs[0]:
        return values[0]
    if f_target >= freqs[-1]:
        return values[-1]
    for i in range(1, len(freqs)):
        if freqs[i] >= f_target:
            span = freqs[i] - freqs[i - 1]
            t = 0.0 if span == 0 else (f_target - freqs[i - 1]) / span
            return values[i - 1] + t * (values[i] - values[i - 1])
    return values[-1]


def outlier_mask(zs, window=5, tol=0.25):
    """True where |Z| departs from its neighbors by more than tol.

    A VNA occasionally returns one bad sample. On a smooth choke sweep that
    shows up as a single spike, and it will drag a curve fit and ruin a plot.
    Compared against a local median so a real resonance is not flagged.
    """
    mags = [abs(z) for z in zs]
    n = len(mags)
    half = window // 2
    bad = []
    for i in range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        nb = sorted(mags[lo:i] + mags[i + 1:hi])
        if not nb:
            bad.append(False)
            continue
        med = nb[len(nb) // 2]
        bad.append(med > 0 and abs(mags[i] - med) / med > tol)
    return bad


def parallel_equivalent(z, f):
    """Series R+jX as an equivalent parallel Rp with a shunt C or L.

    A ferrite choke is physically a loss resistance with the winding's stray
    capacitance across it, so the parallel form is the one whose parts mean
    something. Rp should come out roughly flat across HF for mix 31, and Cp
    is the number that sets the impedance ceiling at the top of the band.
    """
    mag2 = z.real ** 2 + z.imag ** 2
    if z.real == 0 or mag2 == 0:
        return float('nan'), 'n/a'
    rp = mag2 / z.real
    if z.imag == 0:
        return rp, 'pure R'
    xp = mag2 / z.imag
    w = 2 * math.pi * f
    if xp < 0:                      # capacitive
        return rp, '%.2f pF' % (1.0 / (w * -xp) * 1e12)
    return rp, '%.0f uH' % (xp / w * 1e6)


def grade(z):
    """The grading table from the article, applied to one impedance.

    Every threshold is on R, not on |Z|. Reconciled 2026-11-22: the
    articles already SCORED builds on worst-band R and the figures
    shade on R, while this function tested |Z| and so graded one band
    more generously than either. |Z| = R*sqrt(2) at the dominance
    boundary, so a |Z| test always passes at least 41% before an R
    test does. K9YC: the safest approach is to count only the series
    equivalent resistance.
    """
    r, x = z.real, abs(z.imag)
    if r < 1000:
        return 'not a choke here'
    if r >= 5000:
        return 'transmit' if r >= x else 'band-limited, X dominates'
    return 'receive / QRP' if r >= x else 'weak and reactive'


def fit_parallel_rc(freqs, zs, fmin=1e6, fmax=30e6):
    """Least-squares parallel R-C fit to |Z|, R constant across the span.

    Crude by design: R really does rise with frequency in mix 31. The fit is
    here to recover an effective shunt C, which is the number that sets the
    ceiling at the top of HF, not to model the ferrite.
    """
    pts = [(f, abs(z)) for f, z in zip(freqs, zs) if fmin <= f <= fmax]
    if len(pts) < 4:
        return None

    best = None
    r = 1000.0
    while r <= 40000.0:
        c = 0.1e-12
        while c <= 10.0e-12:
            err = 0.0
            for f, mag in pts:
                w = 2 * math.pi * f
                model = r / math.hypot(1.0, w * r * c)
                err += (math.log(model / mag)) ** 2
            if best is None or err < best[0]:
                best = (err, r, c)
            c *= 1.04
        r *= 1.04
    err, r, c = best
    return r, c, math.sqrt(err / len(pts))


def self_resonance(freqs, zs):
    """Frequency of peak |Z|, and that peak."""
    i = max(range(len(zs)), key=lambda k: abs(zs[k]))
    return freqs[i], abs(zs[i])


def x_crossing(freqs, zs, mode='first'):
    """Frequency where X changes sign, interpolated, and |Z| there.

    This is self-resonance proper: the winding's inductance cancelling its
    own stray capacitance. It is not the same frequency as the peak of |Z|,
    and on a lossy ferrite the two can sit well apart, because the peak is
    pulled upward by Rp rising with frequency. Reported separately.

    mode='first'    lowest crossing of any direction. The original behaviour,
                    and what the 2026-11-08 figures were made with.
    mode='downward' the inductive-to-capacitive crossing, X going positive to
                    negative. On a multi-section sleeve choke X can cross
                    upward near the bottom of the sweep, where the highest
                    permeability mix is already past its own relaxation, and
                    that low crossing is not the assembly's self-resonance.
    """
    hits = []
    for k in range(1, len(zs)):
        a, b = zs[k - 1].imag, zs[k].imag
        if a == 0.0:
            hits.append((freqs[k - 1], abs(zs[k - 1]), b < 0))
            continue
        if (a > 0) != (b > 0):
            t = a / (a - b)
            f0 = freqs[k - 1] + t * (freqs[k] - freqs[k - 1])
            z0 = abs(zs[k - 1]) + t * (abs(zs[k]) - abs(zs[k - 1]))
            hits.append((f0, z0, a > 0 and b <= 0))
    if mode == 'downward':
        hits = [h for h in hits if h[2]]
    if not hits:
        return None, None
    return hits[-1][0], hits[-1][1] if mode == 'downward' else hits[0][1]


def fit_parallel_rlc(freqs, zs, f_from):
    """Stray C and winding L from the susceptance, above self-resonance.

    Cp as tabulated is net susceptance, not stray capacitance: it carries
    the winding's own inductive susceptance as well, so it reads low below
    self-resonance and climbs toward the true stray above it. Fitting
    B = w*C - 1/(w*L) over the capacitive region separates them and returns
    the stray C a geometry change actually has to beat.

    Fitted above f_from only. Mix 31's permeability falls with frequency,
    so a single L cannot describe the whole sweep, and forcing it to try
    throws the C off as well.
    """
    pts = [(2 * math.pi * f, (1 / z).imag)
           for f, z in zip(freqs, zs) if f >= f_from and abs(z) > 100]
    if len(pts) < 8:
        return None
    saa = sum(w * w for w, _ in pts)
    sab = sum(-1.0 for _ in pts)
    sbb = sum(1 / (w * w) for w, _ in pts)
    say = sum(w * b for w, b in pts)
    sby = sum(-b / w for w, b in pts)
    det = saa * sbb - sab * sab
    if abs(det) < 1e-30:
        return None
    c = (say * sbb - sby * sab) / det
    inv_l = (saa * sby - sab * say) / det
    if c <= 0 or inv_l <= 0:
        return None
    l = 1.0 / inv_l
    res = [abs((w * c - 1 / (w * l)) - b) / w for w, b in pts]
    return c, l, max(res)


def ref_mode_name(m):
    return 'delay, dividing it out' if m == 'divide' else \
           'lumped series impedance, subtracting it'


def classify_reference(freqs, rs21, z0):
    """Fit a pure delay and a pure lumped inductance to the reference.

    Returns ('divide'|'subtract', explanation). The real part of the
    de-embedded reference impedance is what separates them: a lumped
    inductance has none, a delay has a small negative one.
    """
    import cmath
    sel = [(f, s) for f, s in zip(freqs, rs21) if 8e6 <= f <= 29e6]
    if len(sel) < 10:
        return 'subtract', 'too few points to tell, defaulting to subtract'
    taus = sorted(-cmath.phase(s) / (2 * math.pi * f) for f, s in sel)
    tau = taus[len(taus) // 2]
    ls = sorted((2 * z0 * (1 - s) / s).imag / (2 * math.pi * f) for f, s in sel)
    ind = ls[len(ls) // 2]
    ed = el = 0.0
    for f, s in sel:
        ed += abs(s - cmath.exp(-1j * 2 * math.pi * f * tau))
        el += abs(s - 2 * z0 / (2 * z0 + 1j * 2 * math.pi * f * ind))
    n = len(sel)
    if ed < el:
        return 'divide', ('%.2f ns delay fits %.1fx better than %.0f nH lumped'
                          % (tau * 1e9, el / ed if ed else 999, ind * 1e9))
    return 'subtract', ('%.0f nH lumped fits %.1fx better than a %.2f ns delay'
                        % (ind * 1e9, ed / el if el else 999, tau * 1e9))


def report(path, bands, z0_override, csv_path, ref=None, ref_mode='auto'):
    freqs, s11, s21, z0 = read_touchstone(path)
    if z0_override:
        z0 = z0_override
    sub = None
    if ref is not None:
        rf, _, rs21, _ = read_touchstone(ref)
        lookup = dict(zip((round(f) for f in rf), rs21))
        keep = [i for i, f in enumerate(freqs) if round(f) in lookup]
        if len(keep) < 2:
            raise SystemExit('%s: reference sweep covers no common points'
                             % ref)
        freqs = [freqs[i] for i in keep]
        s11 = [s11[i] for i in keep]
        rsel = [lookup[round(freqs[k])] for k in range(len(keep))]
        s21 = [s21[i] for i in keep]
        if ref_mode == 'auto':
            ref_mode, why = classify_reference(freqs, rsel, z0)
            print('  reference looks like a %s (%s)' % (ref_mode_name(ref_mode), why))
        if ref_mode == 'divide':
            s21 = [s21[k] / rsel[k] for k in range(len(s21))]
        else:
            # Subtract the reference as an IMPEDANCE, which is what a lumped
            # series residual is. Two series elements compose as Z1 + Z2, and
            # that is not multiplicative in S21, so dividing is exact only for
            # a cascaded two-port such as a length of line. The RG-316 sleeve
            # work uses this mode and its numbers are not comparable with the
            # divided ones once the residual stops being small.
            sub = [zcm(r, z0) for r in rsel]
    zs = [zcm(s, z0) for s in s21]
    if sub is not None:
        zs = [zs[k] - sub[k] for k in range(len(zs))]
    zy = [zcm_y21(a, b, z0) for a, b in zip(s11, s21)]
    spike = outlier_mask(zs)
    keep = [i for i in range(len(freqs)) if not spike[i]]
    freqs = [freqs[i] for i in keep]
    s11 = [s11[i] for i in keep]
    s21 = [s21[i] for i in keep]
    zs = [zs[i] for i in keep]
    zy = [zy[i] for i in keep]
    n_spike = sum(spike)

    print('=' * 72)
    print(path)
    print('  %d points, %.3f to %.3f MHz, Z0 = %g ohm'
          % (len(freqs), freqs[0] / 1e6, freqs[-1] / 1e6, z0))
    if ref is not None and ref_mode == 'subtract':
        print('  reference %s subtracted as an impedance' % ref)
        print('    correct for a lumped series residual; not interchangeable')
        print('    with the divided convention.')
    elif ref is not None:
        print('  normalized to %s' % ref)
        print('    that sweep becomes the zero-impedance reference, so the')
        print('    fixture residual and any through-calibration error in it')
        print('    divide out. Check it worked by normalizing a known series')
        print('    inductor: it should return a flat L and R near zero.')
    print()
    print('  series equivalent                    parallel equivalent')
    print('  %-9s %8s %9s %8s %6s  %8s %8s  %s'
          % ('band', 'Rs', 'Xs', '|Z|', 'Rs/|Z|', 'Rp', 'Cp or Lp', 'grade'))
    for fm in bands:
        f = fm * 1e6
        if not (freqs[0] <= f <= freqs[-1]):
            continue
        z = at(freqs, zs, f)
        rp, reactive = parallel_equivalent(z, f)
        print('  %5.1f MHz %8.0f %+9.0f %8.0f %6.2f  %8.0f %8s  %s'
              % (fm, z.real, z.imag, abs(z), z.real / abs(z),
                 rp, reactive, grade(z)))
    print()
    print('  Rp is the ferrite loss; Cp is the stray capacitance across it.')
    print('  A flat Rp with a steady Cp means the model is a parallel R-C,')
    print('  and Cp sets the ceiling 1/(2*pi*f*Cp) that Rp cannot exceed.')

    fsr, zsr = self_resonance(freqs, zs)
    fx, zx = x_crossing(freqs, zs)
    print()
    if fx is not None:
        print('  self-resonance (X crosses zero) %.2f MHz, |Z| %.0f ohm'
              % (fx / 1e6, zx))
    else:
        print('  self-resonance: X does not change sign in this sweep')
    print('  peak |Z| %.0f ohm at %.2f MHz' % (zsr, fsr / 1e6))
    if fx is not None and abs(fsr - fx) > 0.02 * fx:
        print('    the two differ because Rp rises with frequency, which')
        print('    pulls the magnitude peak above the actual resonance')
    if fsr >= freqs[-1] * 0.98:
        print('    (at the top of the sweep: the real peak is above it)')

    fit = fit_parallel_rc(freqs, zs)
    if fit:
        r, c, rms = fit
        print('  parallel R-C fit: R = %.0f ohm, C = %.2f pF (rms %.0f%%)'
              % (r, c * 1e12, 100 * rms))
        f_top = min(freqs[-1], 30e6)
        ceil = 1.0 / (2 * math.pi * f_top * c)
        print('    capacitive ceiling at %.1f MHz: %.0f ohm'
              % (f_top / 1e6, ceil))
    if fx is not None:
        rlc = fit_parallel_rlc(freqs, zs, 1.15 * fx)
        if rlc:
            c, l, worst = rlc
            print('  R-L-C fit above %.1f MHz: stray C = %.2f pF, '
                  'L = %.0f uH' % (1.15 * fx / 1e6, c * 1e12, l * 1e6))
            print('    worst residual %.3f pF; that C is the real stray, '
                  'and the' % (worst * 1e12))
            print('    tabulated Cp is net susceptance, which reads lower')
            print('    the further below self-resonance it is taken')
            cap = 1.0 / (2 * math.pi * 28.4e6 * c)
            print('    it caps |Z| at 28.4 MHz to %.0f ohm, or %.0f ohm '
                  'with R >= |X|' % (cap, cap / math.sqrt(2)))

    print()
    if n_spike:
        print('  %d isolated |Z| spike(s) dropped as bad samples' % n_spike)
    bad11 = [f for f, a in zip(freqs, s11) if abs(a) > 1.001]
    if bad11:
        print('  |S11| exceeds 1 at %d points, %.3f to %.3f MHz'
              % (len(bad11), bad11[0] / 1e6, bad11[-1] / 1e6))
        print('    S11 is wrong there, so the Y21 cross-check below skips')
        print('    those points. The series-through R and X use S21 alone')
        print('    and are unaffected. A run of them means a stale')
        print('    calibration or an intermittent connector.')

    print()
    print('  Y21 cross-check (S12 = S21, S22 = S11):')
    diffs = [abs(abs(b) - abs(a)) / abs(a)
             for f, a, b, p1, p2 in zip(freqs, zs, zy, s11, s21)
             if abs(a) > 100 and abs(p1) <= 1.001 and abs(p2) <= 1.001]
    if diffs:
        diffs.sort()
        med = diffs[len(diffs) // 2]
        p90 = diffs[int(0.9 * (len(diffs) - 1))]
        print('    |Z| difference: median %.2f%%, 90th pct %.2f%%'
              % (100 * med, 100 * p90))
        if p90 < 0.02:
            print('    the two agree, so the port shunts are too small to')
            print('    matter and the series-through number stands')
        else:
            print('    the two disagree: prefer Y21, and shorten the fixture')
    shunts = [c for c in (port_shunt(a, b, z0, f)
                          for f, a, b in zip(freqs, s11, s21)
                          if f > 5e6 and abs(a) <= 1.001)
              if c is not None]
    if shunts:
        shunts.sort()
        print('    implied shunt to ground at each port, median %.1f pF'
              % shunts[len(shunts) // 2])

    if csv_path:
        with open(csv_path, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['freq_hz', 'R_ohm', 'X_ohm', 'mag_ohm',
                        'Rp_ohm', 'Cp_pF', 'R_y21_ohm', 'X_y21_ohm'])
            for f, z, y in zip(freqs, zs, zy):
                rp, _ = parallel_equivalent(z, f)
                m2 = z.real ** 2 + z.imag ** 2
                cpf = ''
                if z.imag < 0:
                    cpf = '%.3f' % (1.0 / (2 * math.pi * f * (m2 / -z.imag))
                                    * 1e12)
                w.writerow(['%.0f' % f, '%.1f' % z.real, '%.1f' % z.imag,
                            '%.1f' % abs(z), '%.1f' % rp, cpf,
                            '%.1f' % y.real, '%.1f' % y.imag])
        print('  wrote %s' % csv_path)

    return freqs, zs


def plot(series, out, xzero='first', style='rxz'):
    """Small multiples, one panel per sweep.

    style='rxz' draws R, X and |Z|, which is the ferrite-datasheet
    convention and the one every figure published before 2026-11-22 uses.

    style='pass' draws R against |X| and shades where the choke is usable.
    A choke is usable where R clears 5 kohm AND R >= |X|, the second being
    G3TXQ's resistance-dominance test, so both become 'is the R line above
    the other line' with no arithmetic. |Z| is dropped on purpose: it is
    the largest of the three by construction and can never fail, so it
    flatters a reactive choke. K9YC puts it plainly, that the safest
    approach is to count only the series equivalent resistance.

    Colors are categorical slots 1 to 3 of the palette this site uses, in
    fixed order. Line style repeats the identity so the panel survives
    color-blind viewing and black-and-white printing.
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.transforms as mtransforms
    except ImportError:
        print('matplotlib not installed, skipping the plot', file=sys.stderr)
        return

    C_MAG, C_R, C_X = '#2a78d6', '#eb6834', '#1baf7a'
    C_PASS, C_FAIL = '#0ca30c', '#d03b3b'   # status, never themed
    INK, MUTED, GRID = '#1a1a19', '#5c5b55', '#d8d7d2'

    n = len(series)
    fig, axes = plt.subplots(1, n, figsize=(6.2 * n, 4.6), sharey=True,
                             squeeze=False)
    for ax, (label, freqs, zs) in zip(axes[0], series):
        mhz = [f / 1e6 for f in freqs]
        if not label.startswith('\0'):
            label = (label.replace('cmc-2026-11-08-', '')
                          .replace('fixture2-a', 'short fixture')
                          .replace('fixture2-b', 'short fixture, repeat')
                          .replace('-', ' '))
        else:
            label = label[1:]
        if style == "pass":
            # Hues match the rxz style so the two conventions never
            # disagree about what a color means: R orange, X green.
            # |Z| is deliberately NOT drawn. It is sqrt(R^2 + X^2), so
            # both its terms are already on the chart, and because
            # |Z| = R*sqrt(2) at the dominance boundary it always
            # clears a threshold at least 41% before R does. On a
            # chart with a 5 kohm line that makes the most eye-catching
            # comparison available the permissive one. The R/X/|Z|
            # table beside every one of these figures carries |Z| for
            # anyone comparing against a magnitude-quoted part.
            R = [z.real for z in zs]
            X = [z.imag for z in zs]
            AX = [abs(v) for v in X]
            ok = [R[i] >= 5000 and R[i] >= AX[i] for i in range(len(zs))]
            i = 0
            while i < len(ok):
                if ok[i]:
                    j = i
                    while j + 1 < len(ok) and ok[j + 1]:
                        j += 1
                    ax.axvspan(mhz[i], mhz[j], color=C_PASS, alpha=0.11,
                               lw=0, zorder=0)
                    i = j + 1
                else:
                    i += 1
            ax.axhline(5000, color=MUTED, lw=1.0, ls=(0, (6, 4)), zorder=1)

            # |X| folds the sign away, so line style carries it back and
            # the dip to zero IS the crossing. Style, not a second hue,
            # so it survives CVD and black-and-white print.
            seg, cur = [], [0]
            for q in range(1, len(X)):
                if (X[q] >= 0) != (X[q - 1] >= 0):
                    cur.append(q)
                    seg.append((X[q - 1] >= 0, cur))
                    cur = [q]
                else:
                    cur.append(q)
            seg.append((X[-1] >= 0, cur))

            for ind, idx in seg:
                ax.plot([mhz[q] for q in idx], [AX[q] for q in idx],
                        lw=1.8, ls="--" if ind else (0, (1, 1.6)),
                        color=C_X, zorder=3)
            ax.plot(mhz, R, lw=2.8, color=C_R, label="R  resistance",
                    zorder=4)
            ax.plot([], [], lw=1.8, ls="--", color=C_X,
                    label="|X|, inductive")
            ax.plot([], [], lw=1.8, ls=(0, (1, 1.6)), color=C_X,
                    label="|X|, capacitive")

            # Every sign change, both directions. A choke with a mix-75
            # section is capacitive at the bottom too, so marking only
            # the downward crossing tells a third of the story. Runs
            # shorter than 1 MHz on either side are noise near zero.
            marks = []
            for q in range(1, len(seg)):
                was, now = seg[q - 1], seg[q]
                if (mhz[was[1][-1]] - mhz[was[1][0]] < 1.0
                        or mhz[now[1][-1]] - mhz[now[1][0]] < 1.0):
                    continue
                q0 = now[1][0]
                x0, x1 = X[q0 - 1], X[q0]
                t = 0.0 if x1 == x0 else (0.0 - x0) / (x1 - x0)
                marks.append((mhz[q0 - 1] + t * (mhz[q0] - mhz[q0 - 1]),
                              now[0]))
            tr = mtransforms.blended_transform_factory(ax.transData,
                                                       ax.transAxes)
            for q, (fm, turns_inductive) in enumerate(marks):
                ax.axvline(fm, color=MUTED, lw=1.0, ls=(0, (2, 3)), zorder=2)
                txt = ("X turns inductive\n %.1f MHz" % fm
                       if turns_inductive else
                       "self-resonance\n %.1f MHz" % fm)
                ax.text(fm, 0.70 if q % 2 == 0 else 0.50, " " + txt,
                        transform=tr, fontsize=8.5, color=MUTED,
                        ha="left", va="center")
            ax.set_ylim(bottom=0)
            runs, a = [], None
            for q in range(len(ok)):
                if ok[q] and a is None:
                    a = q
                if a is not None and (q + 1 == len(ok) or not ok[q + 1]):
                    runs.append((mhz[a], mhz[q]))
                    a = None
            runs = [r for r in runs if r[1] - r[0] > 0.2]
            sub = (", ".join("%.1f-%.1f" % r for r in runs) + " MHz"
                   if runs else "never usable")
            ax.set_title("%s\n usable %s" % (label, sub) if runs
                         else "%s\n %s" % (label, sub),
                         fontsize=10.5, color=INK, loc="left", pad=14)
        else:
            ax.axhline(5000, color=MUTED, lw=0.9, ls=(0, (6, 4)), zorder=1)
            ax.axhline(0, color=GRID, lw=1.0, zorder=1)
            ax.plot(mhz, [z.imag for z in zs], lw=1.6, ls=':', color=C_X,
                    label='X', zorder=2)
            ax.plot(mhz, [z.real for z in zs], lw=1.6, ls='--', color=C_R,
                    label='R', zorder=3)
            ax.plot(mhz, [abs(z) for z in zs], lw=2.4, color=C_MAG,
                    label='|Z|', zorder=4)

            fsr, zsr = self_resonance(freqs, zs)
            ax.plot([fsr / 1e6], [zsr], 'o', ms=6, color=C_MAG,
                    mec='white', mew=1.5, zorder=5)
            ax.annotate('peak |Z| %.1f kohm\nat %.1f MHz'
                        % (zsr / 1000, fsr / 1e6),
                        (fsr / 1e6, zsr), xytext=(8, 6),
                        textcoords='offset points', fontsize=8.5, color=INK)

            fx, _ = x_crossing(freqs, zs, xzero)
            if fx is not None:
                ax.axvline(fx / 1e6, color=C_X, lw=0.9, ls=(0, (2, 3)),
                           zorder=1)
                ax.annotate('X = 0, self-resonance\n%.1f MHz' % (fx / 1e6),
                            (fx / 1e6, 0), xytext=(-6, -34),
                            textcoords='offset points', fontsize=8.5,
                            color=C_X, ha='right')

            z28 = at(freqs, zs, 28.4e6)
            ax.annotate('10 m: R %.1fk, X %.1fk' % (z28.real / 1000,
                                                    z28.imag / 1000),
                        (28.4, z28.imag), xytext=(-8, 10),
                        textcoords='offset points', fontsize=8.5,
                        color=MUTED, ha='right')

            ax.set_title(label, fontsize=10.5, color=INK, loc='left',
                         pad=14)
        ax.set_xlabel('MHz', fontsize=9.5, color=MUTED)
        ax.set_xlim(1, 30)
        ax.grid(axis='y', color=GRID, lw=0.7, alpha=0.7)
        ax.set_axisbelow(True)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        for side in ('left', 'bottom'):
            ax.spines[side].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=9)

    axes[0][0].set_ylabel('ohm', fontsize=9.5, color=MUTED)
    if style == 'pass':
        axes[0][-1].annotate('5 kohm', (29.6, 5000), xytext=(0, 5),
                             textcoords='offset points', fontsize=8.5,
                             color=MUTED, ha='right')
    else:
        axes[0][0].annotate('5 kohm, transmit grade', (1.4, 5000),
                            xytext=(0, 6), textcoords='offset points',
                            fontsize=8.5, color=MUTED)
    if style == 'pass':
        axes[0][0].legend(fontsize=9.5, loc='upper right', frameon=True,
                          facecolor='#fcfcfb', edgecolor=GRID,
                          framealpha=0.92)
    else:
        axes[0][0].legend(fontsize=9.5, frameon=False, loc='lower left')
    head = ('Common-mode choking impedance, series-through on a NanoVNA-F V2'
            if style == 'rxz' else
            'Where the choke is usable: R past 5 kohm and R above |X|')
    fig.suptitle(head, fontsize=11.5, color=INK, x=0.012, ha='left')
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out, dpi=150, facecolor='#fcfcfb')
    print('wrote %s' % out)


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('files', nargs='+', metavar='S2P')
    p.add_argument('--plot', metavar='PNG')
    p.add_argument('--csv', metavar='CSV',
                   help='full swept table; with several inputs, one file each')
    p.add_argument('--bands', help='comma-separated MHz')
    p.add_argument('--z0', type=float)
    p.add_argument('--label', help='panel title, instead of the file name')
    p.add_argument('--style', choices=('rxz', 'pass'), default='rxz',
                   help="'rxz' (default) plots R, X and |Z|, the "
                        'convention every figure published before '
                        "2026-11-22 uses. 'pass' plots R against "
                        '|X| and shades where the choke clears '
                        '5 kohm AND stays resistance-dominant, '
                        'which makes both tests a line comparison.')
    p.add_argument('--xzero', choices=('first', 'downward'), default='first',
                   help="which X = 0 crossing to mark. 'downward' is the "
                        "inductive-to-capacitive one, which is the assembly's "
                        "self-resonance; 'first' is the original behaviour.")
    p.add_argument('--ref-mode', choices=('auto', 'subtract', 'divide'),
                   default='auto',
                   help='how to remove the reference. auto, the default, '
                        'fits both a delay and a lumped inductance to the '
                        'reference sweep and uses whichever matches, '
                        'printing which and by how much. subtract is correct '
                        'for a lumped series residual and divide for a '
                        'delay; forcing the wrong one moves the split '
                        'between R and X by hundreds of ohms.')
    p.add_argument('--ref', metavar='SHORT.s2p',
                   help='a sweep of the fixture shorted at the DUT plane; '
                        'it is removed from every input as --ref-mode says, '
                        'which de-embeds the fixture and replaces a bad '
                        'through calibration')
    p.add_argument('--avg', action='store_true',
                   help='average Z across the inputs and report that as '
                        'one series; repeat sweeps of the same assembly '
                        'belong here, and the spread between them is the '
                        'repeatability figure')
    a = p.parse_args()

    bands = ([float(x) for x in a.bands.split(',')] if a.bands
             else DEFAULT_BANDS)

    series = []
    for i, path in enumerate(a.files):
        csv_path = a.csv
        if csv_path and len(a.files) > 1:
            stem, _, ext = csv_path.rpartition('.')
            csv_path = '%s-%d.%s' % (stem or csv_path, i + 1, ext or 'csv')
        freqs, zs = report(path, bands, a.z0, csv_path, a.ref, a.ref_mode)
        label = path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        series.append((label, freqs, zs))
        print()

    if a.avg and len(series) > 1:
        common = set(round(f) for _, fs, _ in series for f in fs)
        for _, fs, _ in series:
            common &= set(round(f) for f in fs)
        grid = sorted(common)
        cols = []
        for _, fs, zz in series:
            d = dict(zip((round(f) for f in fs), zz))
            cols.append([d[f] for f in grid])
        zavg = [sum(col[i] for col in cols) / len(cols)
                for i in range(len(grid))]
        freqs = [float(f) for f in grid]
        print('=' * 72)
        print('average of %d sweeps' % len(series))
        spread = [max(abs(col[i]) for col in cols)
                  / min(abs(col[i]) for col in cols) - 1
                  for i in range(len(grid)) if min(abs(col[i])
                                                   for col in cols) > 100]
        if spread:
            spread.sort()
            print('  sweep-to-sweep spread in |Z|: median %.2f%%, '
                  'worst %.2f%%'
                  % (100 * spread[len(spread) // 2], 100 * spread[-1]))
        print()
        print('  %-9s %8s %9s %8s %6s  %8s %8s  %s'
              % ('band', 'Rs', 'Xs', '|Z|', 'Rs/|Z|', 'Rp', 'Cp or Lp',
                 'grade'))
        for fm in bands:
            f = fm * 1e6
            if not (freqs[0] <= f <= freqs[-1]):
                continue
            z = at(freqs, zavg, f)
            rp, reactive = parallel_equivalent(z, f)
            print('  %5.1f MHz %8.0f %+9.0f %8.0f %6.2f  %8.0f %8s  %s'
                  % (fm, z.real, z.imag, abs(z), z.real / abs(z),
                     rp, reactive, grade(z)))
        fsr, zsr = self_resonance(freqs, zavg)
        fx, zx = x_crossing(freqs, zavg)
        print()
        if fx is not None:
            print('  self-resonance (X crosses zero) %.2f MHz, |Z| %.0f ohm'
                  % (fx / 1e6, zx))
            rlc = fit_parallel_rlc(freqs, zavg, 1.15 * fx)
            if rlc:
                c, l, worst = rlc
                print('  R-L-C fit above %.1f MHz: stray C = %.2f pF, '
                      'L = %.0f uH (worst residual %.3f pF)'
                      % (1.15 * fx / 1e6, c * 1e12, l * 1e6, worst * 1e12))
        print('  peak |Z| %.0f ohm at %.2f MHz' % (zsr, fsr / 1e6))
        print()
        series = [('two sections in series', freqs, zavg)]

    if a.plot:
        if a.label and len(series) == 1:
            series = [('\0' + a.label, series[0][1], series[0][2])]
        plot(series, a.plot, a.xzero, a.style)


if __name__ == '__main__':
    main()
