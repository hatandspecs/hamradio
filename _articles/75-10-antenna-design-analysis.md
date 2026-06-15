---
layout: default
title: Theory of Operation for a 75-10 EFHW Design
category: article
published: true
date: 2026-06-06
---


**A full-length 80m end-fed half-wave antenna tuned to 75m phone by series capacitor, with inductor coil harmonic correction on the upper bands**

This is an analysis and pontification on a very popular EFHW antenna design that works on 8 bands from 75m to 10m.  I built a DIY version of one of these and have been fascinated with how the complicating elements such as the wideband 56:1 unun with unconventional wind, the inductive compensation coil and the midpoint capacitor are actually working.  Initially I just built the design as specified online and based on pictures of other builds and then tuned it according to instructions/rules of thumb.  Now I'm trying to figure out "why".

> Hand-drawn Schematic of the 75-10m Antenna Design
<img src="{{ '/assets/images/wideband_unun/hand_drawn_schematic.jpg' | relative_url }}" alt="Hand-drawn Schematic of the 75-10m Antenna Design" width="600">

> Close up of the Adjustable PVC Compensation Coil
<img src="{{ '/assets/images/wideband_unun/compensation_coil.jpg' | relative_url }}" alt="Close up of the Adjustable PVC Compensation Coil" width="600">


---

## Part I: The Basic Idea

An end-fed half-wave antenna (EFHW) is a single wire, fed at one end, cut to approximately a half wavelength at the lowest operating frequency. What makes it useful to me as a multiband antenna is a basic fact about harmonics: a wire that is a half wavelength long at some frequency is also a full wavelength at twice that frequency, three half-wavelengths at three times that frequency, and so on.  I am also antenna-mounting-point deprived, so I can mount EFHW antennas easily between my house and a mast I put up in my yard. The wire resonates at all integer multiples of its fundamental, which means a single piece of wire can work on many bands at once, provided those bands line up with the harmonics.

For an 80m wire, the harmonics fall near 80m, 40m, 20m, 15m, and 10m. That is a convenient set of frequencies, because those are several of the major HF amateur bands. 

### EFHW Non-ideal Aspects

A half-wave wire fed at its end presents a very high impedance, on the order of thousands of ohms, rather than the 50 ohms a modern transceiver expects. This is a direct consequence of where you are feeding the wire relative to its standing wave. At the end of a resonant wire, voltage is at a maximum and current is at a minimum. Impedance is voltage divided by current, so at the end of the wire, impedance is very high. A transformer, typically a 49:1 (or in my case 56:1) unun wound on a ferrite core, handles this mismatch by stepping the antenna's impedance down to something close to 50 ohms for the feedline.

Another non-ideal aspect of EFHWs is that they can create common mode current on the shield of the feedline coax.  This creates issues like RF in the shack and noise.  The way to deal with this problem is to build your EFHW antenna with its own dedicated counterpoise wire, attached to the unun ground lug, and to add a beefy common mode choke to the feedline right after the unun.


### The 75m Phone Problem
A full 80m EFHW is roughly 136 feet long and resonates near 3.5 MHz, the CW end of the band. Builders who want to work 75m phone need the fundamental resonance somewhere around 3.85 MHz instead. The obvious fix is to shorten the wire, and many builders do exactly that.

The problem with physical shortening is that it shifts every harmonic upward by the same percentage. Shorten the wire enough to move the fundamental from 3.5 to 3.85 MHz and every other resonance shifts up by the same 10%. The 40m harmonic drifts up toward 7.7 MHz. The 20m harmonic drifts up proportionally. You have solved the 75m problem at the cost of cascading misalignment through every other band.

The design described in this article takes a different approach. Instead of shortening the wire, it keeps the wire at nearly its full 80m length and places a series capacitor at the wire's midpoint. The capacitor adds series reactance that electrically shortens the antenna's apparent length at the fundamental frequency, pulling the resonance up from 3.5 MHz into the 75m phone segment, without physically disturbing the wire length that the upper band harmonics depend on. After a small amount of wire trimming to finish the tuning, the wire ends up around 130 to 134 feet rather than the 118 to 125 feet that physical shortening would require. The upper band harmonics stay close to their natural positions, and a small inductor coil near the feedpoint handles whatever residual correction they need.

At 300 pF and 3.85 MHz, it presents about 138 ohms of series reactance, which is large enough to meaningfully shift the fundamental resonance of the full wire upward into 75m phone territory. It is acting as a frequency-selective electrical shortener at the fundamental while becoming increasingly transparent at higher frequencies where its reactance drops. At 28 MHz its reactance is only about 19 ohms, so the upper bands see essentially the full wire.

A resistor appears in parallel with the capacitor. It is not an RF element. It is a static bleed resistor, typically around 150k ohms, that provides a DC path across the series capacitor. Because the capacitor breaks the wire at the midpoint, the far section of wire has no DC connection to ground through the feedpoint. Static charge can accumulate on that far section from wind, precipitation, and normal atmospheric charge separation. The resistor lets that charge drain continuously rather than building until it arcs. At RF frequencies, 150k ohms is so far above the capacitor's reactance that it has no meaningful effect on antenna behavior.


### Pulling Down the Upper Band Resonances a Bit
The inductor coil near the feedpoint is a lumped inductive element that is small enough to act as a small perturbation. It nudges the upper band harmonics that drifted slightly high during wire trimming and non-idealities of the deployment back down into their correct positions, with an effect on each band that is precisely predictable from the wave physics of the wire.

To understand why the inductor coil affects some bands more than others, and why its placement can be used to tune the upper band resonances, you need a picture of how standing waves distribute themselves along a wire. The clearest path to that picture runs through a mechanical analogy.

---

## Part II: The Guitar String Analogy

Imagine a guitar string stretched between two fixed endpoints. Pluck it, and it vibrates. The simplest vibration, the fundamental mode, has the entire string moving together, with maximum displacement at the center and no motion at the endpoints. At twice the fundamental frequency, the string vibrates in two halves, with a stationary point at the center. At three times the fundamental, it vibrates in three segments. The stationary points are called nodes, and the points of maximum displacement are called antinodes.

Now clip a small split-shot fishing weight to the string at some location. Mass resists acceleration: it takes more force to move something heavy than something light. If you put the weight at a node, it has almost no effect, because that point is not moving anyway and the added resistance to motion does not matter. If you put it at an antinode, the point the string is most actively trying to move, it has the maximum possible effect. The weight fights the motion at that point and lowers the resonant frequency of that mode.

The key insight is that different modes have their antinodes in different places. A weight at the quarter point of the string sits at the antinode of the second harmonic, which has antinodes at the quarter and three-quarter points. But the fourth harmonic has a node at the quarter point, so the same weight barely affects the fourth harmonic at all. You can selectively shift some modes down while leaving others nearly alone, just by choosing where to place the weight. Moving the weight changes which modes are affected most.

This is not a loose analogy for what happens on the antenna wire. It is the same mathematics running on the same underlying physics.  Apparantly, waves and fields behave the same regardless of medium, and can be described with teh same mathematics regardless of medium.  While this fact is something that physicists know like the back of their hand, this is quite amazing to think about for me.

### The Correspondence: Velocity and Current

I have recently learned that the standard mapping between the mechanical string and the electromagnetic wire is this: the transverse velocity of the string corresponds to the current on the wire, and the transverse displacement of the string corresponds to the voltage on the wire.

This mapping is convenient because of where the energy lives. On the string, kinetic energy is stored in the moving mass and is proportional to velocity squared. On the wire, magnetic energy is stored in the inductance and is proportional to current squared. Potential energy on the string is stored in the tension and is proportional to displacement gradient squared. Electric energy on the wire is stored in the capacitance and is proportional to voltage squared. Matching the energy storage forms gives the correct correspondence.

An inductor is a device that pays attention to current. It stores energy in its magnetic field in proportion to the current flowing through it. It resists changes in current the same way mass resists changes in velocity. This is why the split-shot weight is the right mechanical analog for the inductor coil: both resist changes in their respective quantities, both store energy proportional to the square of that quantity, and both shift resonant frequencies downward in proportion to the square of the relevant quantity at their placement location.

A capacitor is a device that pays attention to voltage. It stores energy in its electric field in proportion to the voltage across it. It resists changes in voltage the same way a spring resists changes in displacement. A spring added to a vibrating string at a point of large displacement strongly affects modes with large displacement there and barely affects modes with small displacement there. A capacitor placed on a wire at a point of large voltage strongly affects modes with large voltage there and barely affects modes with small voltage there.

On the resonant wire, voltage and current are spatially 90 degrees out of phase: where current is maximum, voltage is zero, and where voltage is maximum, current is zero. This means an inductor and a capacitor placed at the same point on the wire affect different sets of modes. The inductor maximally affects modes with a current antinode there. The capacitor maximally affects modes with a voltage antinode there, which are exactly the modes with a current node at that point.

| Mechanical | Electromagnetic |
|------------|-----------------|
| Transverse velocity $\partial y / \partial t$ | Current $I$ |
| Transverse displacement $y$ | Voltage $V$ |
| Point mass $m$ | Lumped inductance $\ell$ |
| Spring compliance $\kappa$ | Lumped capacitance $C$ |
| Total string mass $M = \mu L$ | Total distributed inductance $L_{dist} L$ |
| Linear mass density $\mu$ | Distributed inductance per unit length $L_{dist}$ |
| String tension $T$ | Reciprocal of distributed capacitance $1/C_{dist}$ |
| Wave speed $\sqrt{T/\mu}$ | Wave speed $1/\sqrt{L_{dist} C_{dist}}$ |

---

## Part III: The Wave Equation

Both the vibrating string and the resonant antenna wire are governed by the one-dimensional wave equation:

$$\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$$

where $u(x,t)$ is the relevant physical quantity, $x$ is position along the wire or string, $t$ is time, and $c$ is the wave propagation speed.

For the mechanical string:

$$c_{string} = \sqrt{\frac{T}{\mu}}$$

where $T$ is the string tension and $\mu$ is the linear mass density in mass per unit length.

For the antenna wire, treated as a transmission line:

$$c_{line} = \frac{1}{\sqrt{L_{dist} \cdot C_{dist}}}$$

where $L_{dist}$ is the distributed inductance per unit length and $C_{dist}$ is the distributed capacitance per unit length.

These are formally the same expression. The physics does not know whether it is modeling a string or a wire. It sees a one-dimensional system in which a disturbance propagates at speed $c$ and reflects at the boundaries. The guitar string analogy works precisely because it is the same equation.

### Boundary Conditions

The shape of the allowed modes depends on the boundary conditions at the ends of the wire. For the EFHW:

- At the feedpoint ($x = 0$): voltage is at a maximum and current is zero. This is a current node and a voltage antinode.
- At the far end ($x = L$): current is at a maximum and voltage is near zero. This is a current antinode and a voltage node.

These boundary conditions give the following mode shapes. The current distribution for mode $n$ is:

$$I_n(x) = I_0 \sin\!\left(\frac{n\pi x}{L}\right), \quad n = 1, 2, 3, \ldots$$

and the corresponding voltage distribution is:

$$V_n(x) = V_0 \cos\!\left(\frac{n\pi x}{L}\right)$$

The sine and cosine are spatially 90 degrees out of phase, which is the mathematical expression of the fact that current maxima and voltage maxima never occur at the same point on the wire. The resonant frequencies are:

$$f_n = \frac{n \cdot c \cdot k_v}{2L}$$

where $k_v$ is the velocity factor of the wire (typically 0.95 to 0.98 for bare wire in free space) and $c = 3 \times 10^8$ m/s.

---

## Part IV: Finding the Nodes and Antinodes

### Current Antinodes

The current distribution is $I_n(x) = I_0 \sin(n\pi x / L)$. The current antinodes, the points of maximum current magnitude, occur where the sine function reaches its peak:

$$x_{I,max} = \frac{(2k-1)L}{2n}, \quad k = 1, 2, \ldots, n$$

This gives $n$ antinodes per mode. For a wire of $L \approx 132$ ft (close to full 80m length, trimmed slightly during tuning), the antinode positions for each amateur band are:

| Band | $n$ | Current antinode positions (feet from feedpoint) |
|------|-----|--------------------------------------------------|
| 75m  | 1   | 66 |
| 40m  | 2   | 33, 99 |
| 30m  | 3   | 22, 66, 110 |
| 20m  | 4   | 16.5, 49.5, 82.5, 115.5 |
| 17m  | 5   | 13.2, 39.6, 66, 92.4, 118.8 |
| 15m  | 6   | 11, 33, 55, 77, 99, 121 |
| 12m  | 7   | 9.4, 28.3, 47.1, 66, 84.9, 103.7, 122.6 |
| 10m  | 8   | 8.3, 24.8, 41.3, 57.8, 74.3, 90.8, 107.3, 123.8 |

Higher harmonics pack more antinodes into the wire. Any fixed point near the feedpoint end of the wire is progressively closer to a current antinode of higher harmonics, simply because higher harmonics have more antinodes to distribute.

### Current Nodes

The current nodes, points of zero current, occur where the sine function crosses zero:

$$x_{I,node} = \frac{kL}{n}, \quad k = 0, 1, 2, \ldots, n$$

The feedpoint itself ($x = 0$) is always a current node, for every mode. This is why the feedpoint sees high impedance on every band.

### Voltage Antinodes

The voltage distribution is $V_n(x) = V_0 \cos(n\pi x / L)$. Voltage antinodes occur at:

$$x_{V,max} = \frac{kL}{n}, \quad k = 0, 1, 2, \ldots, n$$

Voltage antinodes and current nodes occur at the same positions. The feedpoint is a voltage antinode on every band, which is consistent with the high voltage and high impedance there.

### Voltage Nodes

Voltage nodes (zero voltage) occur at:

$$x_{V,node} = \frac{(2k-1)L}{2n}, \quad k = 1, 2, \ldots, n$$

Voltage nodes and current antinodes coincide. Wherever the current is at its peak, the voltage is at zero.

---

## Part V: The Series Capacitor as Electrical Shortener

Before getting to the perturbation method that governs the inductor coil, it is worth treating the series capacitor separately, because it is operating in a different regime entirely.

A series capacitor inserted into a wire presents a frequency-dependent series reactance:

$$X_C = \frac{1}{2\pi f C}$$

This reactance is in series with the wire's radiation resistance and distributed reactance. At lower frequencies where $X_C$ is large, the capacitor impedes current flow along the wire and effectively makes the wire look electrically shorter than it is. At higher frequencies where $X_C$ is small, the capacitor becomes nearly transparent and the wire behaves as its full physical length.

For a 300 pF capacitor at the midpoint of the wire:

| Band | Freq (MHz) | $X_C$ (ohms) | Capacitor behavior |
|------|------------|---------------|--------------------|
| 75m  | 3.85  | 138 | significant series impedance, electrically shortens wire |
| 40m  | 7.15  | 74  | moderate impedance |
| 30m  | 10.1  | 53  | moderate impedance |
| 20m  | 14.2  | 37  | smaller impedance |
| 17m  | 18.1  | 29  | small impedance |
| 15m  | 21.2  | 25  | small impedance |
| 12m  | 24.9  | 21  | small impedance |
| 10m  | 28.5  | 19  | nearly transparent |

At 75m, 138 ohms of series reactance is large enough to shift the apparent resonant frequency of the full 132 ft wire upward from about 3.5 MHz into the 75m phone segment around 3.85 MHz. This is the primary job of the capacitor. It is not nudging a resonance by a small amount; it is making a full-length 80m wire behave like a somewhat shorter wire at the fundamental frequency, without physically shortening it.

At 10m, 19 ohms of series reactance is small compared to the antenna's impedance environment, and the wire behaves essentially as its full physical length. The transition between these two regimes is gradual across the HF spectrum.

This frequency selectivity is the key advantage over physical shortening. Physical shortening moves all harmonics upward together. The series capacitor preferentially affects the fundamental, where its reactance is highest, and has progressively less effect on higher harmonics where its reactance is lower. The upper band harmonics of the full-length wire are largely preserved, which is exactly what you observe when you tune this antenna: the upper bands stay reasonably well behaved when the capacitor is added, in a way they would not if you had simply trimmed 10% off the wire.

The residual correction that the upper bands need after the capacitor does its job is handled by the inductor coil, which is where the perturbation method becomes the right framework.

---

## Part VI: The Perturbation Method and the Inductor Coil

The perturbation method is a way of calculating how a small addition to a system shifts its resonant frequencies, without having to solve everything from scratch. The central idea is that the frequency shift caused by a small lumped element is proportional to the ratio of the energy that element stores to the total energy of the mode being perturbed.

A resonant wire oscillates by continuously exchanging energy between its magnetic field (stored in the distributed inductance, proportional to $I^2$) and its electric field (stored in the distributed capacitance, proportional to $V^2$). The resonant frequency is set by the balance between these two forms of storage. Adding a lumped inductor tips the balance toward extra magnetic energy storage and shifts the frequency downward for modes where the inductor sees significant current.

The inductor coil pays attention to current. It stores extra magnetic energy proportional to $I^2$ at its location. If it sits where current is large for a given mode, it stores a lot of extra energy for that mode and shifts it down noticeably. If it sits where current is small, it stores very little extra energy and barely moves that mode's frequency. This is the split-shot weight on the guitar string: maximum effect at an antinode, no effect at a node.

### The Inductor Shift Equation

For a lumped inductance $\ell$ placed at position $x = d$ on a wire of length $L$ with distributed inductance $L_{dist}$ per unit length, the fractional frequency shift for mode $n$ is:

$$\frac{\Delta f_n}{f_n} \approx -\frac{\ell \cdot I_n(d)^2 / 2}{\displaystyle\int_0^L L_{dist}\, I_n(x)^2\, dx}$$

Substituting $I_n(x) = I_0 \sin(n\pi x / L)$ and evaluating the integral in the denominator, which works out to $L_{dist} L I_0^2 / 2$:

$$\frac{\Delta f_n}{f_n} \approx -\frac{\ell}{L_{dist} L} \sin^2\!\left(\frac{n\pi d}{L}\right)$$

The prefactor $\ell / (L_{dist} L)$ is the ratio of the lumped inductance to the total distributed inductance of the wire, a small number for a compact coil on a long wire. Everything about which modes get shifted and by how much is captured in:

$$\boxed{\Delta f_n \propto -\sin^2\!\left(\frac{n\pi d}{L}\right)}$$

This is the key equation for the inductor coil. The frequency shift of mode $n$ is proportional to the square of the sine evaluated at the coil's fractional position along the wire.

### Quantitative Estimation

To get a numerical prediction of the shift, you need the distributed inductance of the wire. For a wire of diameter $D$ at average height $h$ above ground:

$$L_{dist} \approx \frac{\mu_0}{2\pi} \ln\!\left(\frac{4h}{D}\right) \quad \text{(H/m)}$$

For a typical field deployment, say 22 AWG wire (diameter 0.644 mm) at 10m average height:

$$L_{dist} \approx \frac{4\pi \times 10^{-7}}{2\pi} \ln\!\left(\frac{40}{0.000644}\right) \approx 2 \times 10^{-7} \times 11.04 \approx 2.21\;\mu\text{H/m}$$

For a 132 ft (40.2 m) wire, total distributed inductance $L_{dist} L \approx 2.21 \times 40.2 \approx 89\;\mu\text{H}$.

If the coil is $\ell = 4\;\mu\text{H}$ and sits at $d = L/16$ (about 8.3 feet from the feedpoint), the shift on 10m ($n = 8$) is:

$$\frac{\Delta f_8}{f_8} \approx -\frac{4}{89} \times \sin^2\!\left(\frac{8\pi}{16}\right) = -0.045 \times 1.0 = -4.5\%$$

At 28.5 MHz that is about 1.3 MHz of downward pull. On 75m ($n = 1$):

$$\frac{\Delta f_1}{f_1} \approx -\frac{4}{89} \times \sin^2\!\left(\frac{\pi}{16}\right) = -0.045 \times 0.038 \approx -0.17\%$$

At 3.85 MHz that is about 6.5 kHz. The coil is essentially invisible to the 75m fundamental.

### Effect of the Coil at $d \approx L/16$

A coil placed approximately 8 feet from the feedpoint on a 132 ft wire sits at $d/L \approx 1/16$. The relative effect on each amateur band is:

| Band | $n$ | $\sin^2(n\pi/16)$ | Relative pull-down |
|------|-----|--------------------|--------------------|
| 75m  | 1   | $\sin^2(\pi/16) \approx 0.038$ | very small |
| 40m  | 2   | $\sin^2(2\pi/16) \approx 0.146$ | small |
| 30m  | 3   | $\sin^2(3\pi/16) \approx 0.308$ | moderate |
| 20m  | 4   | $\sin^2(4\pi/16) = 0.500$ | moderate |
| 17m  | 5   | $\sin^2(5\pi/16) \approx 0.692$ | significant |
| 15m  | 6   | $\sin^2(6\pi/16) \approx 0.854$ | large |
| 12m  | 7   | $\sin^2(7\pi/16) \approx 0.962$ | very large |
| 10m  | 8   | $\sin^2(8\pi/16) = 1.000$ | maximum |

The 75m fundamental is barely touched. Higher bands get progressively more correction, with 10m pulled down maximally. The coil sits near the first current antinode of the 10m mode and near the current node of the 75m fundamental. Moving the coil toward the feedpoint reduces all corrections proportionally while preserving the $\sin^2$ weighting. Moving it away from the feedpoint increases the correction on the lower bands. A VNA showing resonances on multiple bands while you slide the coil along the wire is displaying this $\sin^2$ relationship in real time.

---

## Part VII: The Complete Design Theory

The design now makes sense as a coherent three-layer architecture.

**Layer one: the full-length wire.** The wire starts at approximately 136 feet, which is a natural half-wave for 80m CW near 3.5 MHz. The full-length wire has harmonics that fall close to 40m, 30m, 20m, 17m, 15m, 12m, and 10m without correction. This is the harmonic foundation the design is built on. It is preserved by not physically shortening the wire down to 75m phone length.

**Layer two: the series capacitor.** Inserted at the midpoint of the wire, the capacitor presents 138 ohms of series reactance at 3.85 MHz. This electrically shortens the apparent resonant length of the wire at the fundamental, pulling it up from 3.5 MHz into the 75m phone segment. Because the capacitor's reactance drops with frequency, it has progressively less effect on higher harmonics and becomes nearly transparent at 10m. The upper band harmonic structure of the full wire is largely undisturbed. A small amount of wire is trimmed during tuning to land precisely in the phone segment, leaving the wire at roughly 130 to 134 feet. The resistor across the capacitor bleeds static charge off the far section of wire, which is otherwise DC-isolated by the series capacitor.

**Layer three: the inductor coil.** After the capacitor resolves the 75m problem, the upper band harmonics have drifted slightly high due to the wire trimming and the residual reactance of the capacitor at those frequencies. The inductor coil, placed approximately 8 feet from the feedpoint, applies a $\sin^2$-weighted correction that increases with harmonic number, pulling the upper bands back down by the right proportional amounts. Its position is adjusted empirically using a VNA.

### Why This Is Better Than Physical Shortening

Physical shortening to 75m phone length would require removing roughly 10 to 12 feet of wire, shifting every harmonic upward by about 10%. The inductor coil would then need to provide 10% correction across all upper bands, which pushes it outside the regime where the perturbation equations are reliable and requires a physically larger coil that interacts more strongly with the antenna's current distribution. The series capacitor approach leaves the upper bands close to their natural positions, requiring only a few percent of correction from the coil. That is a correction the perturbation equations handle accurately and that a small coil can provide cleanly.

### Tuning Sequence

The theory implies a specific order of operations:

1. Start with approximately 136 feet of wire and install the series capacitor at the midpoint. Verify the 75m resonance with a VNA and trim wire from the far end until the fundamental lands in the phone segment. Expect to remove only a few feet.
2. Place the inductor coil approximately 8 feet from the feedpoint. Observe the upper band resonances on the VNA.
3. Slide the coil along the wire to distribute the correction across the upper bands as needed. Moving it toward the feedpoint reduces all upper band corrections proportionally. Moving it away from the feedpoint increases correction on the lower bands.
4. Iterate between coil position and any final wire trimming until all target bands are in acceptable positions.
5. If any upper band harmonic cannot be corrected with a physically small coil, the wire trimming in step 1 removed too much wire. The perturbation equations are only reliable for corrections of a few percent. Larger corrections require a physically larger coil that is no longer a small perturbation.

### Design Equations Reference

**Resonant frequencies of the wire:**

$$f_n = \frac{n \cdot c \cdot k_v}{2L}$$

**Series capacitor reactance:**

$$X_C = \frac{1}{2\pi f C}$$

**Current distribution, mode $n$:**

$$I_n(x) = I_0 \sin\!\left(\frac{n\pi x}{L}\right)$$

**Voltage distribution, mode $n$:**

$$V_n(x) = V_0 \cos\!\left(\frac{n\pi x}{L}\right)$$

**Current antinode positions:**

$$x_{I,max} = \frac{(2k-1)L}{2n}, \quad k = 1, 2, \ldots, n$$

**Voltage antinode positions:**

$$x_{V,max} = \frac{kL}{n}, \quad k = 0, 1, \ldots, n$$

**Frequency shift from inductor $\ell$ at position $d$:**

$$\frac{\Delta f_n}{f_n} = -\frac{\ell}{L_{dist} L} \sin^2\!\left(\frac{n\pi d}{L}\right)$$

**Distributed inductance per unit length:**

$$L_{dist} \approx \frac{\mu_0}{2\pi} \ln\!\left(\frac{4h}{D}\right) \quad \text{(H/m)}$$

**Distributed capacitance per unit length:**

$$C_{dist} \approx \frac{2\pi\epsilon_0}{\ln(4h/D)} \quad \text{(F/m)}$$



