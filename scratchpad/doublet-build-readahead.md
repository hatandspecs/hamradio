# Doublet build: read ahead

Working brief for the two-doublet build. The reasoning is in
`_articles/two-doublets-2026-11.md`; this is the short form to read before
starting and to carry to the bench.

Station: **100 W SSB maximum, about 20 W digital.** No amplifier planned.

---

## 1. The two antennas

| | Portable inverted V | Fixed flat top |
|---|---|---|
| Wire | 132 ft, 22 AWG PolyStealth | 88 ft, 14 AWG PolyStealth |
| Shape | apex 40 ft, ends 10 ft | horizontal, house to playhouse mast |
| Span needed | 117 ft | 88 ft |
| Apex angle | 125 deg | n/a |
| Feedline | 300 ohm TV twin lead | 300 ohm 18 AWG window line (DXE-LL300) |
| Balun | one 2631828302, 9T | identical |
| Lowest band | 80 m, true half wave | 40 m, 80 m through the tuner |

**Why these numbers**

- 132 ft is a half wave at 3.72 MHz in free space, nearer 3.55 MHz corrected.
  That is the lower half of 80 m, not the phone end, and it is not why the
  length was picked.
- **Its full-wave points do not all land above a band.** Free space gives
  7.45, 14.90, 22.35 and 29.82 MHz, all just clear. End effect moves them
  down: the one-wave point lands in 40 m (7.27 or 7.08) and the four-wave
  point in 10 m (29.64 or 29.45). 20 m and 15 m stay clear either way.
  Expect the high-impedance case on 40 m and 10 m, and sweep both in test D.
- 88 ft beats 94 ft, but on the **one-wave** point, not the two-wave one.
  94 ft's two-wave point is 20.94 MHz, 64 kHz *below* 15 m and not inside it.
  Its one-wave point is 10.47 MHz free space and 10.21 or 9.95 corrected,
  astride a 30 m band 50 kHz wide. 88 ft clears both points under both
  corrections, by 355 kHz at the worst.
- 14 AWG on the flat top buys 0.36 to 0.48 dB on 80 m over 22 AWG and almost
  nothing on other bands. Worth it on a fixed span, not worth the weight on a
  portable one.
- 300 ohm on both. The 450 ohm advantage is 0.41 dB in one modeled corner
  (10 m into 3,000 ohm) and a tie on the other three. 300 ohm is lower
  voltage and caps the high excursion lower, and against the mAT-30's 5 to
  1,500 ohm window it wins on **every** load, by 1 to 9 points on the
  fraction of feedline lengths that land inside. The 450 ohm line's extra
  excursion is all above the ceiling. The old "~95% either way" figure is
  withdrawn: it was an artifact of how the load range was sampled, and the
  ranking flipped between samplings. Wet weather costs ~1 dB, more than this
  choice does.

---

## 2. Shopping list

Already on hand: FT240-31 20 mm cores (2631828302), AWG 14 enamel, 22 AWG
PolyStealth, 300 ohm TV twin lead, SO-239 connectors, NanoVNA, sleeve choke,
mAT-30 tuner.

**The tuner sets three numbers in this brief**, from its manual: it tunes
**5 to 1,500 ohm** loads, takes **120 W SSB/CW peak and 30 W digital** on HF,
and covers 1.8 to 54 MHz. Its ANTENNA port is an SO-239, so the balun mounts
straight to it. The manual's power warning is unusually direct: power
significantly over spec "will definitely damage or destroy" the tuner and may
take the transceiver with it. 100 W SSB is 83% of the ceiling, 20 W digital
67%.

To buy:

- [ ] 88 ft of 14 AWG PolyStealth, plus spare
- [ ] 300 ohm 18 AWG window line, DXE-LL300, start with 65 ft (section 5).
      Nominal is 272 ohm, VF 0.88. Measure it, card A.
- [ ] 2 plastic project boxes, roughly 4 x 4 x 2 in
- [ ] Screw terminals or eye bolts, 2 pairs
- [ ] #14 PTFE-insulated hookup wire, ~5 ft, for the two balun windings.
      **Record maker, part number, OD and rated voltage.** The 88 ohm figure
      assumes a 2.40 mm OD and the voltage argument assumes a real wall; both
      vary by maker across the five options in section 8
- [ ] Center insulators, 2. A ladder-line mount such as the WA1FFL
      Ladder-Loc carries the line and the wires on separate paths
- [ ] End insulators, shock cord or a pulley and weight
- [ ] Plastic standoffs for line support. An inch of clearance is a rule of
      thumb, not a specification; take the DXE-LL300 guidance for the actual
      line and give it as much room as the run allows
- [ ] Short length of good coax for the jumper, inches not feet. The mAT-30
      manual calls for 50 ohm coax "rated 120 watts or greater" on its radio
      side; the output-side jumper carries the transformed impedance, so rate
      it against 775 V peak. Check the SO-239 too: the format is not a rating

---

## 3. Build order

1. **Balun one.** Wind it, run bench tests A, B, C before building the second.
2. **Flat top**, since it is the fixed installation. Wire, center insulator,
   line, then test D and E.
3. **Balun two**, once the first design is confirmed.
4. **Portable V** last.

---

## 4. Balun build card

**One Fair-Rite 2631828302. Nine close-wound turns of #14 PTFE hookup wire.**
Two cores build both baluns, one each.

| | |
|---|---|
| Wound line | 0.65 m per conductor |
| Predicted choke R | 2.0 to 3.9 kohm, 80 m to 10 m |
| Target Zo of the wound pair | 88 ohm, close wound, 2.40 mm center spacing |

**Close-wound #14 PTFE hookup wire. No sleeve, no spacer.** The insulation
wall sets the spacing by itself: about 2.40 mm between centers, lands near
88 ohms. W2WDX builds several dozen this way and K6JCA measures ordinary #14
bifilar at 60 to 100 ohms. One part, no lacing step.

| Wire | OD | Zo | 9T fill |
|---|---|---|---|
| bare enamel (on hand) | 1.75 mm | 43 ohm | 30% |
| **#14 PTFE standard wall** | **2.40 mm** | **88 ohm** | **41%** |
| #14 PTFE thin wall | 2.13 mm | 74 ohm | 37% |
| #14 silicone | 3.20 mm | 107 ohm | 57% |
| #14 THHN | 2.90 mm | 88 ohm | 51% |

**Bare enamel also works** and is what LDG and M0UKD build. The reason to buy
PTFE is the 894 V peak this station can put at the balun against a real
insulation wall rather than a film, plus abrasion at the bore edge. Not
performance.

**The withdrawn-cord air-gap version is dropped.** It reached ~203 ohms and
nothing in the field is built that way: LDG and M0UKD close-wind bare enamel,
W2WDX and DX Engineering use thick PTFE insulation, Balun Designs sleeves.
Every one is a bifilar pair of insulated wire, 9 to 18 turns, on one or two
FT240-class cores, spaced only by the insulation. The cord variant also cost
bore space and loosened the coupling the balun works by.

Test C still runs, but it decides an optimization and not whether the thing
works. A tuner inches away matches any of these readings.

**Winding.** W1JR crossover: half the turns from one side, cross over the
outside, the rest from the other, so the two ends finish physically apart.

**Connections.** One transmission line, four ends, nothing else. No third
winding, no link between the two wires, no ground on the balanced side.

| End | Goes to |
|---|---|
| Wire A in | coax center |
| Wire B in | coax shield |
| Wire A out | balanced terminal 1 |
| Wire B out | balanced terminal 2 |

**Hardware.** Screw terminals through the box wall so the line's tension is on
hardware, not a solder joint. SO-239 on the coax end. Line enters away from
the coax, neither run near the other or near metal.

**Bore fill, close-wound #14 PTFE (4.80 mm ribbon, 106 mm of bore):**

| Turns | Fill | Gap between pairs | |
|---|---|---|---|
| **9** | **41%** | **6.8 mm** | **the build** |
| 12 | 55% | 3.9 mm | fine |
| 14 | 65% | 2.6 mm | fine |

The dropped air-spaced version was 84% at 14 turns. Close winding removes the
turn-count constraint entirely.

**Escalation if the measurement says it is not enough:** 12 turns on the same
single core gives 3.6 to 6.9 kohm for 0.86 m of line, and that is as far as
one core goes. Past twelve, a second core is the only route: stacking makes
the bore longer, not narrower, so nine turns on two stacked is the same 54%
fill as nine on one.

---

## 5. Where the balun goes, which matters more than what it is

N6BV, 40 m inverted V at 14.1 MHz, 1,500 W, power reaching the antenna:

| Arrangement | To the antenna |
|---|---|
| Balanced tuner, open wire all the way | 1,325 W |
| Choke at the unbalanced tuner's 50 ohm input | 1,314 W |
| **Balun at the window, 20 ft coax jumper** | **397 W** |

The third row is the common build and it loses 696 W in the jumper. Scaled to
100 W that is 46 W, and the fraction does not change with power.

**So: balun bolted to the tuner's antenna connector. Jumper in inches.**
A second choke, the sleeve choke, goes between the radio and the tuner.

The coax-only tuner is what forces this. A balanced or link-coupled tuner is
the upgrade the measurement argues for.

---

## 6. Measurement cards

### A. Feedline Zo and velocity factor

Both lines, before anything else, because "300 ohm" line is nominally 272 and
"450 ohm" line is usually nearer
400.

Take 20 to 30 ft, sweep 1 to 30 MHz twice, far end shorted then open.

- `vf = 2 * L * f / c` from the first impedance minimum with the end shorted
- `Zo = sqrt(Zoc * Zsc)` at one frequency, repeated at several to check

Keep the far-end short physically short. Inches of wire is an inductor at
28 MHz.

### B. Balun common-mode impedance

Series-through, port 1 to both conductors shorted at one end, port 2 to both
shorted at the other, normalized against the shorted-clips reference.

```
Zcm = 2 * Z0 * (1 - S21) / S21     S21 complex and linear, not dB
```

Grade on resistance, not magnitude. Expect 2.0 to 3.9 kohm.

### C. Transparency test, the one that decides the design

300 ohm non-inductive resistor across the balanced terminals, S11 from the
coax end, 1 to 30 MHz.

| Band | Should read |
|---|---|
| 80 m | 287 − 58j |
| 40 m | 258 − 99j |
| 20 m | 184 − 136j |
| 15 m | 126 − 132j |
| **10 m** | **88 − 115j** |

**Near 88 − 115j at 10 m is consistent with the assumed wall and velocity
factor. Near 34 − 86j is consistent with a thinner wall behaving like bare
enamel at ~43 ohms.** Neither reading proves a wall thickness on its own:
winding geometry, parasitic capacitance, core coupling and the fixture all
move it. What the test establishes is the transformation the finished winding
actually applies, which is the thing the old coax-wound balun got wrong.
Either reading still works into the tuner; the low one is an optimization
missed, not a failed build. Record the whole sweep, not one number per band.

Optional test C2, balance: two matched 150 ohm non-inductive
resistors in series across the terminals, junction to the coax shield. Should
read 300 ohms with the junction grounded and floating; the difference is the
balance error. **Below 30 MHz the fixture is most of this measurement**, so
pin it down before trusting a number: carbon composition or thin-film
resistors matched on a meter first, leads under half an inch, the ground
connection a direct strap to the shell rather than a clip lead, and the
calibration plane at the balun's own connector. A result that moves when the
leads move is the fixture talking.

### D. What the tuner will see

1. Calibrate open, short, load **at the connector that plugs into the tuner**,
   jumper in place.
2. Clip the sleeve choke onto the jumper between NanoVNA and balun.
3. Connect jumper, balun, feedline, antenna. Sweep 3 to 30 MHz.
4. Record R and X at each band center, and at both edges of 80 m.
5. Flag any band where R falls outside **5 to 1,500 ohms**, the mAT-30's
   rated load range.

**That is the real window, from the mAT-30 manual: "Tunes 5 to 1500 ohm
loads."** It is narrower at the top than the 20 to 2,000 placeholder this
brief used to carry, and wider at the bottom. It is also only half a
criterion: the manual gives a resistive-load range and says nothing about
how much reactance comes with it, and 100 ohm with a few ohms reactive is not
the same job as 100 ohm with 2,000 ohms reactive. **Record X at every band
center alongside R**, and treat a band near 1,500 ohm with a large X as a
flag even though R is inside.

**If touching the jumper moves the trace, the reading is common-mode current,
not the antenna.** Add choking until it stops moving.

### E. Choosing the feedline length

Add line in a few-foot increments, sweep again, keep the table with the
fewest bands outside range. A switchable insertion loop makes this a minute
per trial. First length that puts every band inside range wins; there is no
optimum to chase across eight bands.

**Starting lengths**, from the ARRL feedline-plus-half-dipole table:

| Target sum | 132 ft V | 88 ft flat top |
|---|---|---|
| 75 ± 2 ft | too short | 31 ft |
| 95.5 ± 3 ft | 29.5 ft | 51.5 ft |
| 109 ± 3 ft | 43 ft | **65 ft** |
| 145 ± 3 ft | 79 ft | 101 ft |

Avoid a line a half wavelength long or any multiple: it reproduces the
feedpoint impedance at the shack end, and on the high-impedance bands that is
several thousand ohms.

**What D and E cannot show:** the impedance at the tuner says nothing about
how much power got there. Feel the balun after operating, not during. A warm
balun is converting transmitted energy into heat.

---

## 7. Numbers to check against

| | |
|---|---|
| Line voltage, 100 W, 300 ohm at 40:1 | 1,095 V RMS, the only case over W8JI's 1,000 V wet-weather threshold |
| Balun dissipation, worst case scaled | 2.6 W average SSB, 2.1 W continuous digital |
| Connector voltage, 100 W into 4,000 ohm | 894 V peak |
| Wire loss, 88 ft on 80 m, 14 AWG | 1.3 ohm, 92 to 94% efficient |
| Wire loss, 132 ft on 80 m, 22 AWG | 5.0 ohm, about 93% efficient |

---

## 8. Settled, do not relitigate

- **1:1, not 4:1.** A 4:1 helps where impedance is reliably high and hurts
  where it is low, and a doublet is low on some bands by construction.
- **A ratio is not chosen from the line's Zo.** A 4:1 fed from 450 ohm line is
  not matching 450 to 50. The "450 ohm needs a 9:1" idea is a myth.
- **Mix 31, not the FT240-43s.** 31 peaks low and holds through the bottom of
  HF, which is where an 80 m choke works.
- **One core. Settled on power, by a factor of ten.** PA9X rates a bifilar
  FT240 in AWG 18 PTFE at 1 kW SSB and ~200 W continuous digital; this is
  100 W SSB and 20 W digital on heavier AWG 14, on a 20 mm core worth 1.57
  standard FT240s. KV5R runs a Balun Designs 1171 cool at 1 kW on a
  ladder-line doublet. The field stacks (M0UKD, W2WDX) to buy power handling
  this station does not need. Stacking also gives ~10% more wound line for
  the same choking impedance. **The margin is an inference across builds**,
  since PA9X's figure is a different wire gauge on its own geometry and a
  choke's power handling tracks the common-mode voltage it sees as much as
  the ferrite; a factor of ten carries that, and the warm-balun check after
  test D confirms it. Revised 2026-11-25.
- **SO-239 throughout.**
- **No amplifier**, so no 1,500 W margins anywhere.

---

## 8b. Documented builds to check against

All are a bifilar pair on one or two FT240-class cores, spaced only by
insulation. None uses an air gap.

| Build | What it reports |
|---|---|
| KV5R 80 m doublet, Balun Designs 1171 | cool at 1 kW; 1:1 over 4:1 because 4:1 raises current |
| M0PZT, FT240-31 | **9 turns resistive 3.5 to 30 MHz**, same as this build |
| K6JCA, measured survey | #16 and #14 bifilar lands at Zo 60 to 100 ohm |
| VK6YSF | single core, 10 turns, 1.25 mm enamel, crossover, 1.8 to 30 MHz |
| PA0FRI | ~300 uH is the 1.8 to 30 MHz compromise; 13 turns gave 308 uH |
| PA9X | FT240 AWG 18 PTFE bifilar: 1 kW SSB, x0.4 contest, x0.2 digital |

## 9. Still unknown

- The choke impedance is scaled from one measurement of nine turns of RG400
  on one of these cores. The scaling is standard; the winding is different.
- How much reactance the mAT-30 tolerates at a given resistance. "5 to 1500
  ohm loads" is a resistive figure and the manual gives no R-X chart, so the
  only way to find the edge is test D on the real antenna.
- Which side of the band edge the 132 ft wire's one-wave and four-wave points
  land on. Both corrections put them in 40 m and 10 m and disagree by 190 kHz
  about where, and neither accounts for height, ground or the bend. A NEC
  model of the real geometry would settle it before the wire goes up.
- What the finished winding's Zo actually is. 88 ohm is computed from a
  nominal 2.40 mm spacing and an assumed effective permittivity, and spacing
  varies around a toroid. Close winding removed the question of holding a gap
  open; it did not answer this one. Test C decides.
- Whether the PolyStealth cladding is three skin depths thick at 3.75 MHz
  (102 micrometers). If it is thinner, the 80 m wire loss is worse than the
  table.
- What either antenna does at this height over this ground. The published
  impedance tables are for a 131 ft doublet at 33 ft and an 88 ft dipole at
  30 ft, neither of which is this installation.
- Whether the ARRL length table means anything here. Wide tolerances, a 1999
  reprint of an older chart.

**The failure that would change the plan:** test D showing a band that no
feedline length brings inside the tuner's range. That means a different wire
length, or accepting the antenna does not cover that band.
