---
layout: default
title: Designing a Multiband 75m to 10m EFHW and Wide-band 56:1 Unun
category: article
date: 2026-05-31
---

The End-Fed Half-Wave (EFHW) antenna is an appealing choice for my situation in terms of deployment and for multi-band operation with one wire. The impedance transformer is the critical component of this system. It transforms the high feedpoint impedance of roughly 2500 ohms to the 50 ohms expected by the radio. The goal of this project is to document a 56:1 transformer and wire system that covers the 75 meter band (3.8 MHz, General license phone band) through 10 meters with flat SWR and acceptable efficiency for operations under 100W, without requiring a tuner.  Wideband operation introduces some engineering trade-offs and conflicts that had to be resolved.  Ultimately such antennas commerically exist and are quite popular, so I took this as evidence that the engineering trade-offs and conflicts are resolvable, and eventually I was able to achieve a functional DIY antenna to meet my goals..


> DIY 75-10m Antenna System, Final nanoVNA Measurements
<img src="{{ '/assets/images/wideband_unun/final_nanovna_antenna.jpg' | relative_url }}" alt="DIY 75-10m Antenna System, Final nanoVNA Measurements
" width="600">

> Deployment of the 75-10m Antenna System in my Yard
<img src="{{ '/assets/images/wideband_unun/7510_deployment_yard.jpg' | relative_url }}" alt="Deployment of the 75-10m Antenna System in my Yard" width="600">



## Antenna System Overview and Goals
This analysis focuses on an antenna design utilizing a single wire consisting of approximately 134 feet of AWG 22 Poly Stealth. To manage resonance and impedance across 75m through 10m, specific matching elements were integrated into the radiator.

* **Center RC Network:** A 150M ohm resistor and a 300pF capacitor in parallel are placed in the center of the antenna wire. The two halves of the wire are in series with this network. Empirical testing with alligator clips showed this pulls the 80m resonance up into the 75m phone segment while minimizing impact to the tuning of the higher bands.
* **Compensation Coil:** This loading coil consists of 8 turns on a 1 inch OD PVC form, placed approximately 6.5 feet from the feedpoint. The PVC form has hook geometries cut into it to allow for rapid adjustment without full disassembly. This coil effectively pulls the resonance frequencies of the upper bands downward.

> Hand-drawn Schematic of the 75-10m Antenna Design
<img src="{{ '/assets/images/wideband_unun/hand_drawn_schematic.jpg' | relative_url }}" alt="Hand-drawn Schematic of the 75-10m Antenna Design" width="600">

> Close up of the Adjustable PVC Compensation Coil
<img src="{{ '/assets/images/wideband_unun/compensation_coil.jpg' | relative_url }}" alt="Close up of the Adjustable PVC Compensation Coil" width="600">

**Hypothesis regarding the RC Network:** While empirical testing showed the desired frequency shift, the operating mechanism is likely entirely capacitive. At 3.8 MHz, a 300pF capacitor presents a capacitive reactance of roughly 139 ohms. Because RF current follows the path of least impedance, it completely bypasses the 150M ohm resistor. The capacitor acts as a series reactance that electrically shortens the antenna at lower frequencies. The resistor is there to provide a static bleed for any static electricity that accumulates on the antenna wire.

The compensation coil functions precisely as expected. By adding series inductance, it introduces electrical length. Because it sits 6.5 feet from the feedpoint, it resides at different voltage and current nodes depending on the harmonic frequency, allowing selective loading of higher harmonics without destroying the fundamental 75m resonance. 

*A note on coil placement:* To maximize a loading coil's effect on a specific higher band, it should be placed at a current maximum (a current loop) for that frequency's standing wave. Conversely, placing it at a voltage maximum (a voltage node) minimizes its effect. Because an EFHW operates as multiple half-waves on its harmonics, calculating the current distribution for a target band like 10m or 15m allows you to pinpoint the exact distance from the feedpoint to install the coil, effectively tuning the high bands independently of the fundamental frequency.

## Wideband Unun Design Engineering Conflicts
Designing a wide-band transformer for this frequency range involves competing technical requirements. To maintain efficiency on the lower bands, the inductive reactance ($X_L$) of the primary must be high enough to prevent the transformer from acting as a shunt to ground. The standard engineering target is an $X_L$ of 4 to 5 times the characteristic impedance (200 to 250 ohms).

Higher frequencies present the opposite challenge. Every additional turn increases path length, leakage inductance, and parasitic capacitance between the windings. Large cores, thick core stacks, and 3-turn primaries create long path lengths. At higher frequencies, these factors cause SWR to climb rapidly.

Based on many experiments winding and testing ununs, I apply the following rules of thumb to balance these conflicts:

1. **Path Length is the Enemy of High Frequencies:** Longer wire paths hurt performance on the upper bands. Big cores, thick stacks, and 3-turn primaries all contribute to excess wire length.
2. **Low Reactance is the Enemy of Low Frequencies:** Too little inductive reactance ($X_L$) on the primary causes the transformer to look like a short circuit to the radio. Lower frequencies demand either a larger core cross-section, more primary turns, or materials with a higher inductance factor.
3. **Core Material Dictates Bandwidth:** The ferrite mix matters significantly. Mix 43 is the most common across HF frequencies, but other mixes favor smaller, specific segments of the amateur bands and will yield different inductance values for the exact same winding geometry.
4. **Wideband is Hard, Narrowband is Easy:** Creating an unun that effectively spans 75m to 10m is tricky. Building ununs for smaller spreads like 160m to 80m, 80m to 40m, or 20m to 10m is comparatively simple.
5. **Wire Gauge Dictates Power, Not Tuning:** AWG 18 through 14 all work fine for HF matching. Core size and wire gauge strictly relate to power handling and duty cycle. For under 100 watts SSB, an FT240 core and AWG 18-14 wire manage heat perfectly.

## Quantitative Analysis of the 2x FT240-43 Stack
To balance the need for high primary inductance on 75m with the need for short wire paths on 10m, I utilized a stacked core design using two FT240-43 ferrites. 

Stacking two identical cores doubles the Inductance Factor ($A_L$).
* Single FT240-43 $A_L$: 1075 nH/turn^2
* Stacked 2x FT240-43 $A_L$: 2150 nH/turn^2

Using the standard inductance formula:
$$L = A_L \times N^2$$

We can calculate the inductance ($L$) and the resulting inductive reactance ($X_L$) using:
$$X_L = 2 \times \pi \times f \times L$$

### Example Calculation: 2-Turn Primary at 3.8 MHz
To demonstrate how the values in the table below are derived, here is the step-by-step calculation for the 2-turn primary at the bottom of the 75m band (3.8 MHz).

**Step 1: Calculate Inductance ($L$)**
$$L = 2150 \times 2^2$$
$$L = 2150 \times 4$$
$$L = 8600 \text{ nH}$$

To convert nanohenries (nH) to microhenries ($\mu$H) for the next formula, divide by 1000:
$$L = 8.6 \mu\text{H}$$

**Step 2: Calculate Inductive Reactance ($X_L$)**
$$X_L = 2 \times \pi \times 3.8 \times 8.6$$
$$X_L = 205.3 \text{ ohms}$$

### Inductive Reactance Results

| Band | Frequency | 2-Turn Primary ($L = 8.6 \mu\text{H}$) | 3-Turn Primary ($L = 19.35 \mu\text{H}$) |
| :--- | :--- | :--- | :--- |
| **75m** | 3.8 MHz | 205 ohms | 462 ohms |
| **40m** | 7.1 MHz | 383 ohms | 863 ohms |
| **20m** | 14.1 MHz | 762 ohms | 1714 ohms |
| **15m** | 21.2 MHz | 1145 ohms | 2577 ohms |
| **10m** | 28.4 MHz | 1534 ohms | 3452 ohms |

A 2-turn primary yields approximately 205 ohms of reactance at 3.8 MHz. This successfully hits the 200 ohm target, providing sufficient reactance to prevent the transformer from acting as a short on 75 meters. A 3-turn primary easily meets the low-frequency requirement but introduces too much wire length, destroying the 10m performance.  I tested and verified this with the nanoVNA.

## Unun Build and Empirical Winding Geometry
The final unit is a 56:1 unun utilizing a 2-turn primary and a 15-turn secondary, wound with AWG 18 wire  since I am operating under 100W SSB and more typically under 50W. A 100pF 1kV C0G/NP0 ceramic capacitor is placed across the primary.  I had no luck with the conventional W1JR winding style for my broadband unun.  Testing with a 2500 ohm non-inductive dummy load, I observed that SWR climbed significantly on the higher bands.

> Conventional W1JR winding for a Wideband 75-10m 56:1 Unun
<img src="{{ '/assets/images/wideband_unun/conventional_w1jr_wind_56_unun.jpg' | relative_url }}" alt="Conventional W1JR winding for a Wideband 75-10m 56:1 Unun" width="600">

From pictures online showing commercially available ununs for similar 75m-10m antenna systems, I saw what appeared to be a different winding style. This, combined with a lack of success on higher bands for broadband ununs with typical W1JR and maximally spaced winding styles, led me to trying to figure out and replicate this unconventional winding style.  I also went with a 2 turn primary because in the pictures of commercial ununs, that is what I saw in commerical unun pictures online, and I did test the same design with a 3 turn primary and it didn't perform as well on the higher bands.

After sweeping numerous winding configurations with a NanoVNA to mitigate the high-band SWR climb, the following hybrid spacing configuration proved to be the only one that maintained relatively flat SWR from 75m through 10m without climbing precipitously on 12m and 10m:

1. A 2-turn bifilar primary/secondary.
2. 5 tightly spaced secondary turns going clockwise around the core.
3. A crossover to the opposite side of the primary.
4. 8 spaced-out secondary turns going counter-clockwise around the core.

The total winding space only occupies about half the circumference of the stacked cores. 

> Exotic Commercially-inspired winding for a Wideband 75-10m 56:1 Unun
<img src="{{ '/assets/images/wideband_unun/exotic_wind_56_unun.jpg' | relative_url }}" alt="Exotic Commercially-inspired winding for a Wideband 75-10m 56:1 Unun" width="600">

To further convince myself that it was the winding spacing that was helping reduce the SWR of the higher bands, I tried a control experiment. I wound a similar style on a roll of electrical tape that was approximately the size of an FT240 core. In this experiment, I am removing the effect of the core itself and the material mix, and any transformation or matching effect must be entirely due to the winding geometry.

> Control Experiment - Exotic Wind on an Inert Core (electrical tape roll) Showing SWR Decrease at Higher Frequencies
<img src="{{ '/assets/images/wideband_unun/tape_unun.jpg' | relative_url }}" alt="Control Experiment - Exotic Wind on an Inert Core (electrical tape roll) Showing SWR Decrease at Higher Frequencies" width="600">

**Operating Mechanism Hypothesis:** The close-spaced initial winds reduce leakage inductance, which severely impacts high-frequency performance. At higher frequencies, the magnetic permeability of Mix 43 drops, and the device likely transitions from a purely magnetic transformer into something else.  I'm currently thinking it is behaving like a non-uniform Transmission Line Transformer (TLT). Or if I am misapplying or misunderstanding the idea of a TLT, perhaps it is just some other form of capacitive and inductive coupling. The specific tight-to-spaced winding geometry appears to facilitate this transition, keeping the self-resonant frequency of the transformer high enough to operate cleanly on 10m.

## Deployment
The antenna deployment in my yard is pragmatic rather than ideal. the feedpoint is mounted outside of a second-story window, traveling 80 to 90 feet to a 25-foot mast mounted on a playhouse. From there, it doglegs and slopes down to a post in the backyard. There is roughly 10 feet of paracord between the post and the antenna end, keeping the lowest portion 8-10 feet above ground.  A large common mode choke (12 turns of coax through an FT240-43 core) is placed immediately after the unun. A dedicated counterpoise wire is attached to the unun ground terminal. Incrementally trimming this counterpoise had a measurable effect on the system tuning, with the final length settling at 8.75 feet.

> Feed Point of my 75-10m Antenna, Common Mode Choke, Unun, and Counterpoise
<img src="{{ '/assets/images/wideband_unun/feed_point.jpg)' | relative_url }}" alt="Feed Point of my 75-10m Antenna, Common Mode Choke, Unun, and Counterpoise" width="600">


> Deployment Map showing Dog-leg Required for Pragmatic Reasons
<img src="{{ '/assets/images/wideband_unun/7510_deployment.png' | relative_url }}" alt="Deployment Map showing Dog-leg Required for Pragmatic Reasons" width="600">

> Far-End of the Antenna
<img src="{{ '/assets/images/wideband_unun/far_end.jpg' | relative_url }}" alt="Far-End of the Antenna" width="600">

## Results
The on-air results have been excellent relevant to my previous antennas. The system operates from 75m to 10m wideband without a tuner with acceptable SWR. I have successfully run WSPR on all 8 bands with solid results and made phone contacts on every band except 12m. 30m does not align as neatly as the other bands but cleans up easily with a tuner. An unexpected benefit is a noticeable reduction in QRM on 20m compared to my previous antennas. My current hypothesis is that this reduction occurs because more of the radiating element is positioned further away from house noise sources. 

73,
KD3CCO
