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
