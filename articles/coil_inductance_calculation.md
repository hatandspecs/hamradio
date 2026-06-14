---
layout: default
title: Calculating and Measuring the Inductance of a Coil
category: article
published: false
date: 2026-04-28
---

As I experiment with antenna designs, I'm finding a need to be able to estimate the inductance of a coil.

## Calculating the Inductance of a Coil
To calculate the inductance of a single-layer air-core coil, the most common and reliable approximation is **Wheeler’s Formula**. 

### The Formula
For dimensions in inches, the inductance $L$ in microhenrys ($\mu\text{H}$) is given by:

$$L = \frac{d^2 \cdot n^2}{18d + 40l}$$

Where:
* $d$ = Mean diameter of the coil in inches
* $l$ = Length of the winding in inches
* $n$ = Number of turns

### The Calculation
Given a mystery coil I purchased online, I measured these dimensions:
* **Diameter ($d$):** 1.6 in
* **Length ($l$):** 1.15 in
* **Turns ($n$):** 20
* **Wire Diameter:** 0.035 in



**1. Calculate the Numerator:**
$$1.6^2 \cdot 20^2 = 2.56 \cdot 400 = 1024$$

**2. Calculate the Denominator:**
$$(18 \cdot 1.6) + (40 \cdot 1.15) = 28.8 + 46 = 74.8$$

**3. Solve for $L$:**
$$L = \frac{1024}{74.8} \approx 13.69 \mu\text{H}$$

---

### Considerations for Precision
* **Winding Pitch:** With 20 turns over a length of 1.15 inches, the pitch (center-to-center distance between wires) is approximately **0.0575 inches**. Since my wire diameter is **0.035 inches**, this is a spaced winding rather than a close-wound coil. 
* **Self-Capacitance:** At higher frequencies, the parasitic capacitance between the turns will create a self-resonant frequency (SRF). Since I am using this for an RF application, the effective inductance will increase as you approach that frequency.
* **Form Material:** Since the coil is wound on plastic, the relative permeability ($\mu_r$) is approximately 1, meaning it behaves almost identically to an air-core coil.


## Measuring a Coil

When I need to verify the inductance of a custom coil, such as the 13-14 $\mu\text{H}$ air-core solenoid we calculated earlier, I rely on my NanoVNA. Whether I am building a general-purpose filter or a loading coil for a specific ham band, I follow this combined workflow to ensure my measurements are accurate and applicable to the real world.

---

### 1. Calibration: The Foundation of Accuracy
Before I even touch the coil, I have to zero out the test leads. If I do not, the VNA will measure the inductance of my clip leads along with the coil itself.

* **1-Port OSL Calibration:** I perform a standard Open, Short, and Load calibration at **Port 1 (CH0)**. 
* **Moving the Measurement Plane:** I calibrate right at the tips of the clips. For the "Short" step, I use a tiny scrap of the same wire I used for the coil. This tricks the VNA into ignoring the leads so the measurement starts exactly where the coil begins.



### 2. Setting the Frequency Range
I choose my frequency sweep based on the end goal for the coil.

* **For General Inductance:** I set a wide, low-frequency sweep (for example, **100 kHz to 5 MHz**). This gives me a stable baseline where parasitic effects are minimal.
* **For Ham Radio Applications:** I narrow the sweep to the specific band I am targeting, such as **7.0 to 7.3 MHz** for 40m. Inductance can shift slightly at higher frequencies due to the skin effect, so I want to know exactly how it performs in its working environment.
* **Identifying the Limit:** I occasionally sweep much higher (up to 30 or 50 MHz) to find the **Self-Resonant Frequency (SRF)**. If the trace crosses the center line of the Smith Chart, I know the coil has stopped acting like an inductor and has become a capacitor.

### 3. Configuring the Display
I typically set up three specific traces on my NanoVNA to get a full picture of the coil behavior:

* **Smith Chart:** I look for the trace to stay in the **top half** of the chart. This is the inductive region.
* **Reactance ($X_L$):** Especially for radio work, I monitor the $+jX$ value. If I need a specific reactance to match an antenna, I can watch this value live while I physically stretch or compress the coil turns.
* **Series L:** If this is available, it gives a direct readout in microhenrys ($\mu\text{H}$). It is the fastest way to see if my 20-turn build matches the 13.69 $\mu\text{H}$ theoretical target. However, if this is not a measurement display option, you can calculate Series $$L = \frac{X_L}{2\pi f}$$


### 4. Taking the Measurement
I connect the coil between the center pin and the outer shield of Port 1. During the measurement, I follow these rules to ensure the environment does not interfere:

* **Avoid Metal:** I place the coil on a plastic or wooden surface. If it sits on a metal bench or too close to the VNA casing, the magnetic field will be disrupted and my inductance reading will drop.
* **Test in the Housing:** If the coil is going inside a PVC pipe or a project box, I take my final measurement with the coil **inside** that housing. The dielectric of the plastic can add a small amount of capacitance, which shifts the effective inductance.



### 5. Verifying the Math
If I am not using a "Series L" display, I pull the reactance ($X$) and frequency ($f$) from the marker and run a quick check:

$$L = \frac{X_L}{2\pi f}$$

By combining these lab-standard calibration techniques with a focus on the specific operating frequency, I can be confident that the coil on my bench will perform exactly as expected once it is installed in a circuit.