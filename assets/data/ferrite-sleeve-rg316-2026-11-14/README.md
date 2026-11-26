# RG-316 single-sleeve sweeps, 2026-11-14

NanoVNA-F V2, SOLT calibrated, series-through fixture, 1 to 30 MHz, 301 points,
Touchstone real/imaginary, 50 ohm. Same fixture and clip separation as the
RG-400 set in `../ferrite-sleeve-2026-11-13/`.

## Fixture references

| File | What |
|---|---|
| SJ000014 | through, clips closed as far as they go (185 nH residual) |
| SJ000015 | through, long wire (403 nH). Not used. |
| SJ000016 | open |
| SJ000026 | **through, short wire at the separation the cores occupied (287 nH). The reference removed from the single-sleeve sweeps, files 27 through 44.** `auto` subtracts it, fitting the lumped model 1.1x better than a 2.84 ns delay, which is a weak margin: check it before relying on the R/X split from these files. |

## Measurements, mix and turns to file

| Turns | mix 75 | mix 31 | mix 43 |
|---|---|---|---|
| 10 | SJ000027 | SJ000028 | SJ000029 |
| 8 | SJ000032 | SJ000031 | SJ000030 |
| 6 | SJ000033 | SJ000034 | SJ000035 |
| 4 | SJ000038 | SJ000037 | SJ000036 |
| 2 | SJ000039 | SJ000040 | SJ000041 |
| 1 | SJ000044 | SJ000043 | SJ000042 |

A turn is one pass through the bore.

## Built assemblies, same day

Eleven four-core chokes wound and swept, with their own references taken at the
build geometry rather than the single-sleeve one. The build geometry's short
reference measures 455 nH against the single-sleeve 289, so **file 46 and not
file 26 is the correct subtraction for files 47 through 58.** All eleven were
swept the same day, same fixture, same lead distances, so one reference covers
them all.

The article numbers these 1 through 11 in the order wound. Chokes 1 to 3 were
wound from a model since withdrawn; 4 to 11 vary one section at a time from a
common base.

| File | Choke | Sections | Worst R, 80-10 m | At | Lowest R/\|Z\| |
|---|---|---|---|---|---|
| SJ000045 | | open, long wire. The ceiling: 2.1 MOhm at 160 m to 173 kOhm at 10 m. | | | |
| SJ000046 | | **short, long wire. The reference subtracted from 47 through 58.** | | | |
| SJ000047 | 1 | `#75@8T + #75@8T + #43@5T + #43@5T` | **6,307** | 80 m | **0.77** |
| SJ000048 | 2 | `#75@8T + #75@8T + #31@4T + #43@5T` | **6,706** | 10 m | **0.76** |
| SJ000049 | 3 | `#75@10T + #31@4T + #31@4T + #31@5T` | 3,762 | 10 m | 0.57 |
| SJ000050 | 4 | `#75@8T + #75@8T + #43@6T + #43@6T` | 5,575 | 10 m | 0.66 |
| SJ000052 | 5 | `#75@8T + #75@8T + #43@5T + #43@6T` | 5,098 | 10 m | 0.66 |
| SJ000054 | 6 | `#75@8T + #75@8T + #31@4T + #43@6T` | 3,666 | 10 m | 0.62 |
| SJ000053 | 7 | `#75@8T + #75@8T + #31@6T + #43@6T` | 5,638 | 10 m | 0.66 |
| SJ000055 | 8 | `#75@8T + #31@6T + #31@6T + #43@6T` | 4,378 | 10 m | 0.58 |
| SJ000056 | 9 | `#75@8T + #31@6T + #31@6T + #43@8T` | 6,282 | 10 m | 0.55 |
| SJ000057 | 10 | `#75@9T + #31@6T + #31@6T + #43@6T` | 4,256 | 10 m | 0.55 |
| SJ000058 | 11 | `#75@9T + #31@6T + #31@6T + #43@5T` | 7,369 | 10 m | 0.59 |

File 51 was not used. Resistance in ohms. A choke is resistance-dominant where
R/|Z| is 0.707 or above, so **only chokes 1 and 2 clear 5 kOhm on every band
from 80 to 10 m while staying resistance-dominant.** Choke 11 has the highest
worst-band resistance of the eleven and is 81 percent reactive by magnitude at
10 m.

Seven of the eleven clear 5 kOhm everywhere from 80 to 10 m. The limiting band
is 10 m for ten of the eleven.

These eleven are the evidence that no model in this work predicts a build.
Summing the measured single sleeves of a choke misses by 40 percent on average;
a section library solved from the assemblies themselves fits them to 1-8
percent but misses a held-out choke by 27 percent. Sections do add in series.
The per-section values taken from bench sweeps do not transfer, because the
bench dress is looser than any assembly's.

## Choke 2 re-wound with tidier leads (2026-11-15)

| File | Choke | Sections | Worst R, 80-10 m | At | Lowest R/\|Z\| |
|---|---|---|---|---|---|
| SJ000059 | 2, re-dressed | `#75@8T + #75@8T + #31@4T + #43@5T` | **6,858** | 80 m | **0.89** |

Same sleeves, same turn counts, same cable; only the lead and inter-section
dressing changed, shorter and closer to the cores. Swept the next day against
**the same reference, SJ000046**, with the fixture and calibration untouched.

Band by band against the original build, resistance in ohms:

| Band | 160 | 80 | 40 | 30 | 20 | 17 | 15 | 12 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| SJ000048, original | 8283 | 6851 | 6736 | 7800 | 9957 | 10940 | 9888 | 8242 | 6706 |
| SJ000059, re-dressed | 8523 | 6858 | 6873 | 7741 | 10006 | 12392 | 13059 | 11509 | 10166 |
| change | +3% | 0% | +2% | -1% | 0% | +13% | +32% | +40% | +52% |

**Nothing below 20 m moved and everything above it did**, which is stray
capacitance and nothing else. This is now the best choke in the set: it beats
the original on worst-band R, 6,858 against 6,706, and its limiting band moves
from 10 m to 80 m.

Reproduce the figure with:

```
python3 assets/code/choke_s2p.py SJ000059.s2p --ref SJ000046.s2p \
  --xzero downward \
  --bands 1.9,3.5,7.1,10.1,14.2,18.1,21.2,24.9,28.4 --plot out.png
```

**`--ref-mode` defaults to `auto`**, which fits a delay and a lumped
inductance to the reference and uses whichever matches. On SJ000046 it reports
`453 nH lumped fits 1.9x better than a 4.35 ns delay` and subtracts. Do not
force `divide` on this fixture: the toroid article's compact short is a 0.85 ns
delay and wants division, this long-wire reference is not, and the two are not
interchangeable.

## 1:1 current balun, three sleeves (2026-11-22)

Not one of the eleven and not part of the design search. Wound as a 1:1
current balun to take a doublet's 300 ohm twin lead into a wide-range tuner,
and kept because it measures well as a choke and does not work as the balun.

| File | Sections | Worst R, 80-10 m | At | Lowest R/\|Z\| |
|---|---|---|---|---|
| SJ000060 | `#31@8T + #31@8T + #43@6T` | **5,007** | 10 m | **0.59** |

Swept against **the same reference, SJ000046**, same fixture and lead dressing
as the assemblies. Self-resonance 7.86 MHz, peak |Z| 14,930 ohm at 6.61 MHz,
stray 0.60 pF from the R-L-C fit above 9 MHz.

**The reference barely matters for this winding**, unlike the single-sleeve
sweeps: subtracting SJ000046 and using no reference at all agree within 0.3
percent on every band, because 453 nH is 81 ohms at 28.4 MHz against 8,400 of
winding. Dividing the same reference gives −765 ohms at 28.4 MHz, unphysical,
which is the delay-versus-lumped discriminator restated on an assembly.

```
python3 ../../code/choke_s2p.py SJ000060.s2p --ref SJ000046.s2p \
  --xzero downward --plot out.png
```

## Chokes 12 and 13, 2026-11-22

Wound eight days after the other eleven, against the same SJ000046 reference
and the same fixture. Numbered as chokes 12 and 13 in the article, continuing
the series. Choke 12 was swept as wound, then re-dressed with nothing else
changed; choke 13 is the same assembly again with its mix-43 section cut from
six turns to five.

| File | Choke | Sections | Worst R, 80-10 m | Lowest R/\|Z\| | SRF | stray C |
|---|---|---|---|---|---|---|
| SJ000061 | 12 | `#75@8T + #31@8T + #31@6T + #43@6T` | 7,312 | 0.674 | 10.29 MHz | 0.45 pF |
| SJ000062 | 12 re-dressed | same winding | 8,925 | 0.705 | 11.80 MHz | 0.38 pF |
| SJ000063 | **13** | `#75@8T + #31@8T + #31@6T + #43@5T` | **8,587** | **0.782** | 9.77 MHz | 0.35 pF |

**Choke 13 is the best choke in the set**, 8,587 ohm worst band over 80-10 m
and resistance-dominant on all nine bands from 160 m to 10 m, against choke 2
re-dressed at 6,858 and 0.888. Three of the thirteen now meet both halves of
the criterion: 1, 2 and 13.

**Re-dressing alone (61 to 62) bought 22 percent at 10 m** and cut stray C by
16 percent, but did NOT win dominance: 0.705 against the 0.707 line. Cutting
capacitance also raises Rp, so conductance and susceptance fall together and
the ratio barely moves. **What won 10 m was the mix-43 section going 6T to
5T**, which dropped Rp at 28.4 MHz from 17,938 to 14,045 and so raised the
conductance 28 percent with the susceptance unchanged. Loss, not geometry.

**SJ000062's 160 m reading of 4,063 ohm is a bad sample**, not a feature: 1.8
and 1.9 MHz dip two to three kilohms below their neighbors while 61 and 63 run
smoothly through. All three carry `|S11| > 1` over 1.0 to 2.26 MHz, which does
not affect the series-through R and X but is a reason not to lean on 160 m.

```
python3 ../../code/choke_s2p.py SJ000063.s2p --ref SJ000046.s2p \
  --style pass --plot out.png
```

## Choke 14, 2026-11-23

`SJ000064`. Choke 13 with its fourth sleeve changed from mix 43 to mix 31 at
the same five turns, and nothing else touched. The first build in the set with
no mix 43 in it at all.

| File | Choke | Sections | Worst R, 80-10 m | Lowest R/\|Z\| | SRF | stray C |
|---|---|---|---|---|---|---|
| SJ000064 | **14** | `#75@8T + #31@8T + #31@6T + #31@5T` | **8,094** | **0.725** | 9.54 MHz | 0.39 pF |

**Choke 14 meets both halves of the criterion**, which makes four of fourteen:
1, 2, 13 and 14. On worst-band resistance it is second of all fourteen, 8,094
ohms at 10 m against choke 13's 8,587, and it displaces choke 2 re-dressed
from second place.

**The reference barely matters for this winding**, as with SJ000060: against
SJ000046 and against nothing at all, every band agrees within 0.2 percent,
because 453 nH is 81 ohms at 28.4 MHz against 8,000 of winding. The result
does not depend on the fixture reference being carried over from 2026-11-14.

Band by band against choke 13, the only difference being the fourth sleeve's
mix. Resistance in ohms, `R/|Z|` beneath each.

| Band | 160 | 80 | 40 | 30 | 20 | 17 | 15 | 12 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| SJ000063, `#43@5T` | 7093 | 11181 | 13866 | 14655 | 14254 | 12648 | 11547 | 10113 | **8587** |
| | 0.82 | 0.90 | 0.99 | 1.00 | 0.98 | 0.93 | 0.88 | 0.83 | **0.78** |
| SJ000064, `#31@5T` | 7337 | 11291 | 15612 | 16509 | 16060 | 13728 | 11748 | 9630 | **8094** |
| | 0.81 | 0.87 | 0.99 | 1.00 | 0.97 | 0.89 | 0.83 | 0.77 | **0.72** |
| change in R | +3% | +1% | +13% | +13% | +13% | +9% | +2% | -5% | -6% |

**Mix 43 at the top buys 10 m and costs the middle.** Swapping it out for mix
31 at the same turn count raises 40 through 17 m by 9 to 13 percent and lowers
12 and 10 m by 5 to 6 percent, and the dominance ratio falls on every band
above 40 m. That is the loss mechanism restated: mix 43 is lossier at 28 MHz,
and dominance at the top is bought with loss.

**Choke 14's 10 m pass is inside the noise and should not be leaned on.**
Across the whole 10 m band rather than at its center, its worst `R/|Z|` is
0.7104 at 29.52 MHz, clearing the 0.707 line by 0.0034. Choke 13 at the same
frequency is 0.7628. Choke 12 re-dressed failed the same line by 0.002. With
build-to-build scatter still unmeasured, a margin of 0.0034 is not a pass that
distinguishes itself from a fail. Choke 14 also goes reactance-dominant at
29.90 MHz, above the band edge but inside the sweep, where choke 13 holds
0.758 to 30 MHz.

```
python3 ../../code/choke_s2p.py SJ000064.s2p --ref SJ000046.s2p \
  --style pass --plot out.png
```
