---
layout: default
title: First Attempt at a Shortened Rigid V-Dipole for 40m
category: article
date: 2026-04-27
---


## **Project Overview**
The goal for this project was to take my existing portable rigid V-dipole, which performs flawlessly on 20m and higher, and extend its range into the 40m band. I use a camera tripod-mounted hub with a **120°** included angle. I originally chose this geometry because it provides a near-perfect **50Ω** feedpoint impedance when mounted low to the ground. This setup allows me to use a simple 1:1 common mode choke instead of a matching transformer.

To operate on 40m with physically shortened elements, I introduced inductive loading at the feedpoint using a pair of pre-made coils that happened to come with M10 threaded interfaces which are compatible with my setup.  I got very inexpensively from an online retailer and decided to place a small bet on mystery coils rather than build something specific. Worst-case scenario, I will disassemble them, use the threaded interfaces and remanufacture the plastic core and wind different coils on them if needed.

---

## **System Configuration**

### **Physical Architecture**
* **Radiators:** Two **5.5m** (approx. 18ft) stainless steel telescoping whips.
* **Geometry:** Rigid "V" configuration with a **120°** included angle.
* **Loading:** Dual non-adjustable base-loading coils **~20 turns** installed at the hub.  I will measure these at some point to see what the actual inductance is.
* **Matching:** A hastily constructed adjustable Beta match (shunt inductor) was added to transform the low radiation resistance up to **50Ω**.

<img src="{{ '/assets/images/coil_loading_rigid_v_dipole/setup_wtih_beta_match.jpg' | relative_url }}" alt="setup with beta match" width="600">


---

## **Experimental Results (40m Band)**

I tuned the system for the center of the 40m phone segment. While I was able to achieve a near-perfect match at the target frequency, the bandwidth proved to be exceptionally narrow.

| Parameter | Measured Value |
| :--- | :--- |
| Resonant Frequency ($f_c$) | **7.236 MHz** |
| Minimum SWR | **1.03:1** |
| SWR < 2.0 Bandwidth | **39 kHz** (7.217 to 7.256 MHz) |
| Percentage Bandwidth | **0.54%** |

<img src="{{ '/assets/images/coil_loading_rigid_v_dipole/bandwidth_measurement.jpg' | relative_url }}" alt="setup with beta match" width="600">

### **Key Observation**
While the Beta match effectively brought the SWR down to **1.03:1** at resonance, the curve is incredibly steep. Moving even **20 kHz** away from $f_c$ causes the SWR to climb rapidly. This effectively limits me to a very small slice of the band without further physical adjustment of the antenna.

---

## **Technical Analysis: Why the Narrow Bandwidth?**

The narrow bandwidth is a direct result of high System Q (Quality Factor). Based on my observations, this is driven by three main factors.

### **1. Reduced Radiation Resistance ($R_r$)**
A full-sized 40m dipole is roughly **20m** tip-to-tip. My **11m** total span is only about **55%** of a natural resonant length. This causes the $R_r$ to drop significantly, likely to the **12Ω** to **18Ω** range, which the Beta match then has to step up to **50Ω**.

### **2. Inductive Reactance**
To reach resonance, the **~20-turn** coils must provide high inductive reactance to cancel the capacitive reactance of the short whips. This high ratio of stored energy to radiated energy creates a "sharp" resonance, meaning the antenna only wants to radiate efficiently in a very tight frequency window.

### **3. Base Loading Position**
Placing the coils at the feedpoint, where current is highest, is mechanically convenient but electrically the least efficient way to achieve bandwidth. It maximizes the influence of the coil on the system Q compared to placing the loading further up the radiator.

---

## **Potential Next Steps (Ranked by Priority)**

I am looking for ways to widen this window to cover more of the 40m phone band (**7.125 MHz** to **7.300 MHz**). Here is my roadmap for future modifications.

### **Priority 1: Top-Hat Loading (Capacity Hats)**
This is my top priority. By adding small "whiskers" or a wire cross at the tips of the whips, I can increase the capacitance at the ends of the antenna. This would allow me to remove turns from or tap out turns from the loading coils. Less inductance should lead to a lower Q and wider bandwidth.

### **Priority 2: Adjustable Inductance**
Since my current coils are fixed, I may look into tapped coils or a sliding contact system. This would not increase the native bandwidth, but it would allow me to shift the **39 kHz** window across the band quickly without having to collapse and adjust the whip lengths manually.

### **Priority 3: Moving the Coils Outward (Center Loading)**
I have considered adding **1m** rigid arms between the hub and the coils. This would transition the system toward center-loading, which increases radiation resistance and lowers System Q. However, moving the coils outward will likely require more than inductance to maintain resonance on 40m.
