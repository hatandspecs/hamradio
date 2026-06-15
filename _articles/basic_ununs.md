---
layout: default
title: Designing a Basic 49:1 Unun
category: article
date: 2026-04-26
---

This document outlines the material properties and design principles required to build a functional 49:1 unun (unbalanced to unbalanced) transformer for an end-fed half-wave antenna.

## 1. Core Material and Permeability
The selection of the ferrite toroid is based on its initial permeability ($\mu_i$). This value determines how much inductance is generated per turn of wire.

| Material Mix | Permeability ($\mu_i$) | Typical Use Case |
| :--- | :--- | :--- |
| **Mix 43** | 850 | Standard for 80m to 10m. Provides high inductance with fewer turns. |
| **Mix 52** | 250 | Better for high power and high frequencies. Resistant to thermal drift. |
| **Mix 61** | 125 | Used for high HF and VHF. Requires more turns for low band operation. |

---

## 2. Inductance and the Inductance Factor ($A_L$)
Each toroid has an **Inductance Factor ($A_L$)** measured in nanohenries per turn squared ($nH/N^2$). This value is a constant that accounts for the magnetic properties of the ferrite and the physical dimensions of the core.

### The Physics of $A_L$
While manufacturers provide $A_L$ as a fixed number, it is actually derived from the geometry of the core and the permeability of the material. The formula for the Inductance Factor is:

$$A_L = \frac{\mu_0 \mu_i A_e}{l_e}$$

In this formula:
* **$\mu_0$** is the permeability of free space (a physical constant).
* **$\mu_i$** is the initial permeability of the ferrite mix (e.g., 850 for Mix 43).
* **$A_e$** is the effective cross-sectional area of the core.
* **$l_e$** is the effective magnetic path length (the distance around the center of the ring).



### Geometry vs. Size
It is a common misconception that only larger cores have higher $A_L$ values. Because $A_L$ is a ratio of the cross-sectional area to the path length, a small core with a very thick cross-section can have a higher Inductance Factor than a large core with a thin cross-section. 

Increasing the thickness of the core increases $A_e$, which raises the $A_L$. Increasing the diameter of the core increases $l_e$, which actually lowers the $A_L$ if all other dimensions remain the same.

### Reference Table for Common Core Sizes
The following table provides the Inductance Factor ($A_L$) for the two core sizes used in these 100W builds.

| Core Size | Mix 43 ($A_L$) | Mix 52 ($A_L$) | Mix 61 ($A_L$) |
| :--- | :--- | :--- | :--- |
| **FT140** (1.40 inch OD) | 885 $nH/N^2$ | 362 $nH/N^2$ | 140 $nH/N^2$ |
| **FT240** (2.40 inch OD) | 1075 $nH/N^2$ | 440 $nH/N^2$ | 170 $nH/N^2$ |

### Why Focus on FT140 and FT240?
In ham radio applications for 49:1 ununs, we choose these specific sizes not just for their $A_L$ values, but for their ability to handle power. While a much smaller core might have a similar $A_L$, it would be unsuitable for 100W operation for two reasons:

1. **Magnetic Saturation:** A smaller core has less volume to store magnetic energy. At 100W, the magnetic flux density ($B_{max}$) can exceed the core's limits, causing the material to saturate. This leads to high SWR, signal distortion, and extreme heat.
2. **Winding Space:** A 49:1 unun requires 14 to 21 secondary turns. To handle 100W, you must use thicker wire (such as 14 AWG or 18 AWG) to minimize resistive heating. Smaller cores do not have enough "window" space in the center to physically fit the required number of turns of heavy gauge wire.

### Inductance Calculation
You calculate the total inductance ($L$) using the following formula:

$$L = N^2 \times A_L$$

In this equation, $N$ is the number of turns. Because the turn count is squared, doubling the number of turns results in four times the total inductance.

---

## 3. Inductive Reactance ($X_L$)
A transformer must have enough **Inductive Reactance ($X_L$)** to avoid acting as a load on the transmitter. Inductive Reactance is a measure of the transformer's opposition to alternating current at a specific frequency. If the reactance is too low, the transformer will dissipate power as heat.

The standard design goal is for the Inductive Reactance to be 4 to 5 times the system impedance. In a 50 $\Omega$ system, the target is $200 \Omega$ to $250 \Omega$ at the lowest operating frequency.

$$X_L = 2\pi f L$$

In this formula, $f$ is the frequency in Hertz and $L$ is the inductance in Henries.

---

## 4. Turns Ratio and Impedance Matching
An end-fed half-wave antenna typically has a feed point impedance near $2450 \Omega$. To match this to $50 \Omega$ coax, a 49:1 impedance ratio is used. Impedance transformation is determined by the square of the turns ratio:

$$\text{Impedance Ratio} = \left(\frac{N_{sec}}{N_{pri}}\right)^2$$

For a 49:1 ratio, the transformer requires a 7:1 turns ratio. Common examples include:
* **2 Primary turns to 14 Secondary turns**
* **3 Primary turns to 21 Secondary turns**

---

## 5. High Frequency Parasitics
At higher frequencies like the 10m band, physical variables called parasitics interfere with the transformer ratio.

* **Leakage Inductance:** This occurs when magnetic flux does not couple perfectly between the primary and secondary windings. It causes SWR to rise on high bands.
* **Inter-winding Capacitance:** This is stray capacitance between the wires. It is caused by turns being placed too close together.

### Common Corrections
* **Winding Spacing:** Spreading the secondary turns around the core reduces capacitance.
* **Bifilar Winding:** Twisting the primary turns with the first few turns of the secondary improves magnetic coupling.
* **Compensation Capacitors:** A high voltage capacitor (often 100pF) placed across the primary can cancel out leakage inductance on 10m.

---

## 6. Core Size and Power
The physical size of the core determines power handling and heat dissipation. Stacking multiple cores increases the total cross-sectional area ($A_e$), which allows the stack to handle more power before reaching magnetic saturation. This prevents the material from reaching its Curie temperature, which is the point where the ferrite loses its magnetic properties and the SWR increases rapidly.

---

# Verifying Performance with a Vector Network Analyzer (VNA)
A Vector Network Analyzer, such as the NanoVNA, is used to verify that the unun is performing as designed before it is attached to an antenna.

## Using a Dummy Load for Ratio Testing
To test a 49:1 unun, you must terminate the secondary side with a resistance that represents the antenna wire at resonance. Since the unun is designed to match $50 \Omega$ to approximately $2450 \Omega$ ($50 \times 49$), you use a $2450 \Omega$ or $2500 \Omega$ resistor. 

The resistor should be a non-inductive type. Wire-wound resistors have internal inductance that will provide inaccurate readings at high frequencies. When you connect the VNA to the input and the resistor across the output, the VNA should show resistance of approximately $50 \Omega$ across the frequency range of intended use.

## Bench SWR vs. Field SWR
It is important to understand that a dummy load test only verifies the transformer ratio. A low SWR on the bench does not guarantee a low SWR when the unun is attached to a real antenna for several reasons:

* **Lack of Counterpoise:** On the bench, there is usually no counterpoise or coax shield acting as a return path. In the field, the coax shield changes the complex impedance of the system.
* **Environmental Parasitics:** Nearby objects and height above ground introduce capacitive and inductive reactances that a simple resistor cannot simulate.
* **Complex Impedance:** An antenna wire is only purely resistive at its resonant points. On other frequencies, it presents a complex impedance that the unun must handle.

If the bench test shows a high SWR on the 10m band with a dummy load, it may actually improve once the antenna is deployed and has a proper counterpoise. The dummy load test verifies build quality, but final tuning must be done with the antenna wire in its operating position.