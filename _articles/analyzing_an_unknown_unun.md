---
layout: default
title: Analyzing an Commercial 75m to 10m EFHW Unun
category: article
date: 2026-04-29
published: false
---


## Part 1: The FT240 Stack. Reverse Engineering a Commercial Unun

In the world of amateur radio, commercial "black box" ununs often hide their best secrets under layers of heat shrink and epoxy. When a device features an unconventional winding scheme, understanding its true performance, specifically the **primary inductive reactance ($X_L$)**, requires moving beyond simple SWR readings into the realm of slightly more complex admittance modeling.

### The Anatomy of the Device
The EFHW transformer in question promises useable SWR on amateur bands from 75m to 10m.  It is built on two stacked **FT240** toroids of an unknown ferrite mix. These are stacked directly with no spacing to maximize the magnetic cross-sectional area. The winding geometry is a variation of the hybrid Ruthroff/Guanella design, likely intended to function as a 56:1 impedance transformer with a 2:15 turns ratio.

* **Winding Ratio:** 2 Primary turns to 15 Secondary turns (1:7.5 voltage ratio).
* **Winding Style:** A "twisted pair" start for the first 2 turns to maximize coupling, followed by a split-secondary winding. The first 5 secondary turns are wound clockwise (around the circumference of the core) and spaced tightly together (touching). After a crossover, the final 8 turns are wound counter-clockwise (around the circumference of the core) and spaced slightly apart. The entire winding occupies less than half of the core circumference.
* **Compensation:** A **120 pF** ceramic capacitor labeled 121 across the primary.

I made a DIY replica of the device with some known FT240-43 toroids that I had. It is wound the same way as the commercial Unun. I added a 120pF capacitor. My DIY Unun is wound with AWG 18 wire, whereas the commercial unit is wound with approximately AWG 16 wire.  Here are some pictures of my DIY replica, to illustrate the winding style.  In a later section I will measure it and compare it to the commerical Unun.

> DIY Unun, View 1
<img src="{{ '/assets/images/analyzing_an_unknown_unun/diy_view1.jpg' | relative_url }}" alt="DIY Unun, View 1" width="600">

> DIY Unun, View 2
<img src="{{ '/assets/images/analyzing_an_unknown_unun/diy_view2.jpg' | relative_url }}" alt="sDIY Unun, View 2" width="600">

> DIY Unun, View 3
<img src="{{ '/assets/images/analyzing_an_unknown_unun/diy_view3.jpg' | relative_url }}" alt="DIY Unun, View 3" width="600">

---

### Measurements with a 2500 Ohm Dummy Load

To evaluate how the unun performs in a real-world scenario, the device was tested using a 2500 Ohm non-inductive dummy load. This value was chosen to simulate the typical feedpoint impedance of an End-Fed Half-Wave (EFHW) antenna, representing an approximate 50:1 transformation ratio.

The following table details the SWR and complex impedance measured at the primary input side with the NanoVNA:

| Frequency (MHz) | SWR | Complex Impedance ($R + jX$) |
| :--- | :--- | :--- |
| **3.803** | 1.21 | 40.3 + 4.0j $\Omega$ |
| **7.186** | 1.49 | 34.6 - 5.9j $\Omega$ |
| **14.243** | 2.07 | 24.3 - 3.9j $\Omega$ |
| **28.453** | 1.59 | 70.9 + 18.3j $\Omega$ |

These loaded measurements provide the baseline for our performance analysis. While the SWR remains largely usable, being under 2.1:1 for most of the range, the shifting real and imaginary components suggest that the transformation mechanism is evolving as frequency increases.

> Commerical Unun, 2500 Ohms Loaded
<img src="{{ '/assets/images/analyzing_an_unknown_unun/commercial_loaded.jpg' | relative_url }}" alt="Commerical Unun, 2500 Ohms Loaded" width="600">

---

### Decoding the Primary Inductive Reactance ($X_L$)
To find the $X_L$ of the windings alone, we must mathematically remove the 120 pF capacitor. Since the capacitor and the primary winding are in parallel, we convert the series impedance measurements ($Z$) into parallel admittance ($Y$).  I measured the no-load complex impedance at each of the frequencies I was interested in.

#### The Mathematical Model
We calculate the capacitive susceptance ($B_C$) of the 120 pF capacitor at each frequency and subtract it from the measured net susceptance ($B_{net}$) to isolate the inductive susceptance ($B_L$).

$$B_C = 2 \pi f C$$
$$X_L = \frac{1}{|B_{net} - B_C|}$$

| Frequency (MHz) | No-Load Impedance ($Z$) | Net Susceptance ($B_{net}$) | Cap. Susceptance ($B_C$) | **Primary $X_L$** |
| :--- | :--- | :--- | :--- | :--- |
| **3.803** | 335 + 70.2j | -0.00060 S | 0.00287 S | **288.4 $\Omega$** |
| **7.186** | 36.1 - 92.4j | +0.00939 S | 0.00542 S | **251.9 $\Omega$** |
| **14.243** | 6.74 - 32.5j | +0.02948 S | 0.01074 S | **53.4 $\Omega$** |
| **28.435** | 8.03 + 10.1j | -0.06065 S | 0.02144 S | **12.2 $\Omega$** |

> Commerical Unun, Unloaded
<img src="{{ '/assets/images/analyzing_an_unknown_unun/commercial_unloaded.jpg' | relative_url }}" alt="Commerical Unun, Unloaded" width="600">

### Detailed Calculation Steps and Example
To calculate the primary inductive reactance when a capacitor is in parallel, we have to move from the world of **Impedance ($Z$)** to the world of **Admittance ($Y$)**. 

The fundamental problem is that the NanoVNA measures everything in series ($R + jX$), but components in parallel do not add up linearly in that format. They add up linearly as Admittances.

#### 1. The Components of Admittance
Admittance ($Y$) is the reciprocal of Impedance ($Z$). Just as impedance has a real part (resistance) and an imaginary part (reactance), admittance is split into two parts:

$$Y = \frac{1}{Z} = G + jB$$

* **$G$ (Conductance):** The real part, measured in Siemens (S). It represents how easily current flows through the resistive portion of the circuit.
* **$jB$ (Susceptance):** The imaginary part, also measured in Siemens. This represents the "ease" of current flow through the reactive components (inductors and capacitors).



#### 2. Why use Susceptance?
In a series circuit, add reactances ($X_{total} = X_L + X_C$). In a **parallel** circuit, add susceptances:

$$B_{total} = B_C + B_L$$

This additive property is what allows us to mathematically "peel away" the capacitor to see the inductor hiding underneath.

---

#### 3. Step-by-Step Susceptance Calculation

##### Step A: Convert Series Impedance to Admittance
If the NanoVNA gives a reading of $Z = R + jX$, convert it to Admittance using the complex reciprocal:

$$Y = \frac{1}{R + jX} = \frac{R}{R^2 + X^2} - j\frac{X}{R^2 + X^2}$$

From this, we extract the **Net Susceptance ($B_{net}$)**, which is the coefficient of the imaginary part. 

> **Crucial Sign Note:** If $X$ is negative (capacitive), the $B_{net}$ becomes positive. If $X$ is positive (inductive), the $B_{net}$ becomes negative.

##### Step B: Calculate the Capacitor's Susceptance ($B_C$)
Since the capacitor value is known (120 pF), we calculate its individual contribution to the total susceptance. The susceptance of a capacitor is always positive:

$$B_C = \omega C = 2 \pi f C$$

##### Step C: Isolate the Inductive Susceptance ($B_L$)
We know that the total measured susceptance is the sum of the two components. To find the inductor's contribution, we subtract the capacitor's effect:

$$B_L = B_{net} - B_C$$



##### Step D: Convert back to Inductive Reactance ($X_L$)
Once you have isolated $B_L$, you can find the actual reactance of the copper windings. Inductive reactance is the reciprocal of the magnitude of its susceptance:

$$X_L = \frac{1}{|B_L|}$$

---

#### 4. Worked Example (Using the 3.8 MHz data)
1.  **Measured Impedance ($Z$):** $335 + 70.2j$ $\Omega$.
2.  **Calculate $Y$:** $$Y = \frac{1}{335 + 70.2j} \approx 0.00286 - 0.00060j \text{ S}$$
    So, $B_{net} = -0.00060$ S.
3.  **Calculate $B_C$ for 120 pF:**
    $$B_C = 2 \pi (3.803 \times 10^6) (120 \times 10^{-12}) \approx 0.00287 \text{ S}$$
4.  **Find $B_L$:**
    $$B_L = -0.00060 - 0.00287 = -0.00347 \text{ S}$$
5.  **Find $X_L$:**
    $$X_L = \frac{1}{|-0.00347|} \approx 288.2\ \Omega$$

#### 5. Summary of the Physical Meaning
The reason the susceptance calculation is so powerful is that it reveals the "hidden" inductor. 

At 3.8 MHz, the NanoVNA measured a slightly inductive load ($+70.2j$). However, after the math, we see the actual winding has a much higher reactance of **288.2 $\Omega$**. The 120 pF capacitor was "fighting" the inductor, cancelling out most of its reactance and leaving only a small remainder for the VNA to see. This calculation is essential for understanding the true magnetizing impedance of the core without having to physically desolder components.

---

### Estimating the $A_L$ and Ferrite Mix
The $A_L$ value, representing inductance per square turn, is the fingerprint of the ferrite core. The relationship between the inductance, the material permeability, and the physical dimensions of the core is expressed by the following equation:

$$A_L = \frac{L}{N^2} = \frac{\mu_0 \mu_i A_e}{l_e}$$

Where:
* $\mu_0$ is the permeability of free space ($4\pi \times 10^{-7}$ H/m).
* $\mu_i$ is the initial relative permeability of the ferrite material.
* $A_e$ is the effective cross-sectional area of the core.
* $l_e$ is the effective magnetic path length.

Using the 3.8 MHz data, where the inductive component is most stable, we can estimate the inductance ($L$) and the $A_L$ for the stack.

1.  **Inductance ($L$) at 3.8 MHz:** $$L = \frac{X_L}{2 \pi f} \approx 12.07 \text{ }\mu\text{H}$$
2.  **$A_L$ Calculation:** Since $L = A_L \cdot N^2$ (with $N=2$):
    $$A_L = \frac{12,070 \text{ nH}}{4} \approx 3,017 \text{ nH/turn}^2$$

For a stack of two FT240 cores, where the total $A_e$ is doubled while $l_e$ remains constant, an $A_L$ of 3,017 points toward **Type 43 Ferrite**. While nominal single-core values are approximately 1075 nH/turn$^2$, permeability often rises at the lower end of the HF spectrum before the core becomes predominantly resistive. However, there is enough of a discrepency between the expected 2150 nH/turn$^2$ and the 3,017 computed from my measurements that the possibility of a hybrid core stack can not be excluded definitively. For example, the commercial unit could be utilizing a hybrid core stack of Mix 31 and Mix 43 (or some other combination).

---

### Technical Observations
* **Core Loss:** The resistance at 3.8 MHz (335 $\Omega$) is relatively low for an unloaded transformer. This confirms the core is operating in its lossy region, which is common for Type 43 at low frequencies. This unun will convert a measurable portion of power into heat on the 80m band.
* **The Crossover Winding:** The use of a crossover, reversing the winding direction, is a sophisticated touch designed to cancel out phase accumulation and push the self-resonant frequency (SRF) higher.
* **Efficiency:** With the 2500 Ohm load, the 40.3 + 4j reading at 3.8 MHz is excellent. It shows that even though the core is lossy, the transformation ratio is spot-on and the 120 pF capacitor is neutralizing the leakage inductance of the secondary.

---

## Part 2: The Complex Permeability Paradox

We discovered a counter-intuitive phenomenon where the primary inductive reactance ($X_L$) plummeted as frequency increased, dropping from 288.4 $\Omega$ at 3.8 MHz to a mere 12.2 $\Omega$ at 28 MHz. In a perfect air-core inductor, reactance should climb linearly with frequency. However, in ferrite-core transformers, we are at the mercy of **complex permeability**.

### The Ferrite Wall: $\mu'$ vs. $\mu''$
Ferrite materials like Type 43 are defined by $\mu'$ (Mu-prime), the inductive component, and $\mu''$ (Mu-double prime), the resistive component. As frequency increases across the HF spectrum, the $\mu'$ craters. The core stops acting like a storage device for magnetic energy and starts acting like a high-frequency resistor. This explains the collapse of $X_L$ because the value of $L$ is dropping faster than the frequency is rising.



### From Induction to Transmission Line Mode
If the inductive reactance is only 12.2 $\Omega$ at 10m, why is the SWR only 1.59? The secret is the twisted-pair start.

* **At 80m (3.8 MHz):** The device operates primarily via **magnetic induction**. The core does the work.
* **At 10m (28 MHz):** Induction has failed. However, the device shifts into **Transmission Line Transformer (TLT)** mode. Energy is coupled directly between the tightly twisted wires rather than through the ferrite itself.

### The Appropriateness of the Design
Is an unun with 12.2 $\Omega$ of $X_L$ on 10m appropriate?
1.  **For SWR:** It is highly effective. The design cheats the physics of the ferrite to provide a usable match.
2.  **For Efficiency:** It is less than ideal. Because $X_L$ is so low, significant current flows through a core that has become resistive. This leads to **thermal dissipation**. In high-duty cycle modes, this energy becomes heat.


## Part 3: The DIY Replica — Measurements and Calculations

To benchmark the commercial unit, I constructed a DIY replica using two FT240-43 toroids purchased from DigiKey. This unit was wound using the same 2:15 unconventional geometry. A 120 pF compensation capacitor was placed across the primary. While the commercial unit uses approximately AWG 16 wire, this replica utilizes AWG 18.

### Measurements with a 2500 $\Omega$ Dummy Load
The following data represents the loaded performance of the DIY replica:

| Frequency (MHz) | SWR | Complex Impedance ($R + jX$) |
| :--- | :--- | :--- |
| **3.803** | 1.13 | 47.6 - 5.40j $\Omega$ |
| **7.186** | 1.60 | 34.9 - 12.9j $\Omega$ |
| **14.243** | 2.21 | 22.7 - 1.62j $\Omega$ |
| **28.453** | 2.08 | 103.0 - 6.96j $\Omega$ |


> DIY Unun, 2500 Ohms Loaded
<img src="{{ '/assets/images/analyzing_an_unknown_unun/diy_loaded.jpg' | relative_url }}" alt="DIY Unun, 2500 Ohms Loaded" width="600">


---

### Measurements and Primary Reactance ($X_L$) Calculation
The primary inductive reactance was isolated by measuring the unit without a load. Using the admittance model ($Y = 1/Z = G + jB$), the 120 pF capacitor's susceptance ($B_C$) was subtracted from the net susceptance ($B_{net}$) to find the primary inductive reactance ($X_L$).

| Frequency (MHz) | No-Load Impedance ($Z$) | Net Susceptance ($B_{net}$) | **Calculated $X_L$** |
| :--- | :--- | :--- | :--- |
| **3.803** | 163 - 158j | +0.00307 S | **4,950.0 $\Omega$** |
| **7.186** | 22.4 - 76j | +0.01211 S | **149.4 $\Omega$** |
| **14.243** | 5.59 - 28.4j | +0.03389 S | **43.2 $\Omega$** |
| **28.453** | 8.03 + 16.7j | -0.04865 S | **14.3 $\Omega$** |


> DIY Unun, unloaded
<img src="{{ '/assets/images/analyzing_an_unknown_unun/diy_unloaded.jpg' | relative_url }}" alt="DIY Unun, unloaded" width="600">

---

### The Resonance Trap: Understanding the 4,950 $\Omega$ Anomaly

One of the most striking data points in the DIY replica is the primary inductive reactance ($X_L$) of **4,950 $\Omega$** at 3.803 MHz. While this number suggests an incredibly high magnetizing impedance, it is actually a mathematical artifact of **parallel resonance**. 

In an unun with a compensation capacitor, the circuit acts as a parallel resonant tank. The primary winding (an inductor) and the 120 pF capacitor are in a "tug-of-war" on the imaginary axis of the admittance plane. Their relationship is defined by their **susceptance ($B$)**, which is the imaginary component of admittance ($Y$).

#### The Physics of Cancellation
In a parallel circuit, total susceptance is the sum of the individual components. Because inductive susceptance ($B_L$) and capacitive susceptance ($B_C$) have opposite signs, they effectively subtract from one another:

$$B_{net} = B_C - B_L$$


At 3.803 MHz, the DIY replica hits a specific state where these two values are nearly identical:
* **Capacitive Susceptance ($B_C$):** $\approx 0.00287$ Siemens
* **Inductive Susceptance ($B_L$):** $\approx 0.00307$ Siemens

Because these two numbers are so close, the **net susceptance ($B_{net}$)** becomes a very small value (approximately 0.00020 Siemens). When we calculate the inductive reactance ($X_L$) by taking the reciprocal of the susceptance, the result is an "apparent" reactance that explodes toward infinity:

$$X_L = \frac{1}{|B_{net} - B_C|} \approx 4,950\ \Omega$$

#### Apparent vs. Physical Reactance
It is vital to distinguish between **apparent reactance** and **physical reactance**. The 4,950 $\Omega$ value is the apparent reactance seen by the NanoVNA due to the cancellation effect of the capacitor. It does not mean the ferrite core has suddenly become four times stronger at 3.8 MHz. 

In fact, the high sensitivity of this number is a telltale sign of a lower-inductance core. Because the DIY unit has less physical inductance than the commercial unit, its natural resonant frequency was pushed down directly into the 80 meter band. The commercial unit, possessing higher physical inductance, stays far enough away from this resonance point to provide a stable, "real" measurement of its primary reactance ($X_L = 288.4\ \Omega$).

This resonance trap serves as a reminder that at the lower end of the HF spectrum, the compensation capacitor can heavily mask the true performance of the ferrite. To find the real "inductive backbone" of the transformer, one must look at frequencies further away from the resonant peak, such as the 7.1 MHz data, where the core's physical properties are more clearly visible.

### Estimating $A_L$
The $A_L$ value relates the physical inductance to the core geometry and permeability via the following equation:

$$A_L = \frac{L}{N^2} = \frac{\mu_0 \mu_i A_e}{l_e}$$

Using the 7.186 MHz data for the DIY replica ($N=2$):
1. **Inductance ($L$):** $L = X_L / (2 \pi f) \approx 3.31\ \mu\text{H}$
2. **$A_L$ Estimate:** $A_L = 3310\text{ nH} / 4 \approx \mathbf{827.5\text{ nH/turn}^2}$

---

## Part 4: Comparative Analysis

A comparison of the measurements from the commercial unit and the DIY replica reveals several interesting performance trends.

### Transformation and SWR
Both units achieved a usable SWR across the HF spectrum with a 2500 $\Omega$ load. At 3.803 MHz, the DIY replica showed a slightly lower SWR (1.13) compared to the commercial unit (1.21). However, the DIY unit maintained a capacitive imaginary component across most of the lower and middle bands, whereas the commercial unit transitioned from inductive to capacitive reactance as frequency increased.

### Inductive Reactance Trends
The most significant divergence occurs in the calculated primary inductive reactance ($X_L$).

* **Low-Band Behavior (3.8 MHz):** The DIY replica shows an exceptionally high $X_L$ of 4,950 $\Omega$ at 3.803 MHz. This value is a result of parallel resonance, where the inductive susceptance of the windings and the capacitive susceptance of the 120 pF capacitor nearly cancel each other out. The commercial unit, by contrast, measured a more stable $X_L$ of 288.4 $\Omega$ at this frequency.
* **Mid-Band Performance (7.1 MHz):** When moving away from the resonance point, the commercial unit provides higher inductive reactance ($X_L = 251.9\ \Omega$) compared to the DIY replica ($X_L = 149.4\ \Omega$). This indicates that the commercial unit possesses higher physical inductance than the DIY build.
* **High-Band Convergence (28 MHz):** On the 10 meter band, the $X_L$ of both units converged to a range between 12 $\Omega$ and 14 $\Omega$.



### Comparison of Estimated $A_L$
The calculated $A_L$ values provide a clear numerical contrast between the two core stacks.

| Metric | Commercial Unit | DIY Replica |
| :--- | :--- | :--- |
| **Estimated $A_L$** | $\approx$ 3,017 nH/turn$^2$ | $\approx$ 827.5 nH/turn$^2$ |
| **Inductance ($L$) at 7.1 MHz** | $\approx$ 5.57 $\mu$H | $\approx$ 3.31 $\mu$H |

### Summary of Differences
The data illustrates that while the winding geometry is identical, the commercial unit maintains higher inductive reactance across the majority of the HF spectrum. The DIY unit hits a parallel resonance point within the 80 meter band, causing a peak in apparent reactance that is not present in the commercial unit. By 28 MHz, the reactive contribution of the cores in both units becomes nearly identical, suggesting that the transformation at the highest frequencies is dominated by the winding geometry rather than the inductive properties of the core.


## TBD Part 5 - A DIY Hybrid Stack of Mix 31 and Mix 43

## TBD Part 6 - Can I do something useful with Mix 52?