---
layout: default
title: Building a DIY Rigid V Dipole for Portable Ops
category: article
date: 2026-03-09
---


If you have been looking into popular antennas for Parks on the Air (POTA), you have likely seen a specific rigid V dipole gaining a lot of traction. While the commercial version uses a distinct hexagonal hub to achieve its signature look, the physics behind it are surprisingly simple and very easy to replicate at home.

<img src="{{ '/assets/images/rigid_v_dipole/5.jpeg' | relative_url }}" alt="diy rigid v dipole" width="600">

---

## Why the "V" Shape?

A standard horizontal dipole usually has a feedpoint impedance of about **75 ohms**. However, when you bend those elements into a **120° V configuration** and mount them at a typical portable height (less than **0.1 λ**), something magical happens: the impedance drops to right around **50 ohms**. This makes it a perfect match for your radio without needing a complex tuner.

The hexagonal shape of the commercial hubs isn't just for aesthetics. A hexagon's sides naturally provide those 120° mounting surfaces, making it mechanically simple to get the angle right every time.




## Simple Components, Great Results

The beauty of this design is that there are no complicated electrical components involved. It is essentially a mechanical hub, two **18 foot telescoping whips**, and basic hardware. 

The only "extra" you really need is a **1:1 common mode choke** at the feedpoint. This ensures your coax cable doesn't become part of the antenna, which helps keep your SWR stable and prevents RF from coming back into the shack (or onto your microphone).

Some commercial versions include extra nuts for running a single whip as a vertical with a counterpoise, but for this DIY project, I focused strictly on the dipole configuration.

---

## The Build Process

### Version 1: The PVC Prototype
For my first experiment, I kept it low budget by using a **PVC pipe fitting** as the mounting hub. Even with this "ugly" prototype, the results were impressive.

<img src="{{ '/assets/images/rigid_v_dipole/2.jpeg' | relative_url }}" alt="pvc hub rigid v dipole" width="600">

<img src="{{ '/assets/images/rigid_v_dipole/3.jpeg' | relative_url }}" alt="pvc rigid v deployed" width="600">

### Version 2: The 3D Printed Hub
To move toward a more "pro" look, my friend **KD3CCP** 3D-printed a custom hexagonal box for me. This served as a sturdy, lightweight housing for the hardware.

<img src="{{ '/assets/images/rigid_v_dipole/4.jpeg' | relative_url }}" alt="building the 3d printed hub" width="600">


---

## Field Performance and Tuning

Tuning is a breeze with telescoping whips. I extended each side to approximately **5 meters**, screwed them into the hub, and checked the results on my **nanoVNA**. 

With just a few inches of adjustment to the whip lengths, I hit the sweet spot:
* **SWR:** 1.1
* **Impedance:** 52 ohms
* **Reactance:** Nearly zero

### Results on the Air
As soon as I hooked up the radio, I realized I had dropped right into the middle of a DX contest. Using just **6 watts SSB (QRP)**, I logged four DX contacts in under ten minutes!

<img src="{{ '/assets/images/rigid_v_dipole/6.jpeg' | relative_url }}" alt="bands come alive" width="600">


<img src="{{ '/assets/images/rigid_v_dipole/1.png' | relative_url }}" alt="dx contacts" width="600">

---

## Final Thoughts

This antenna is a winner for portable enthusiasts. Setup and teardown each take less than five minutes. If you are looking for a fast, effective antenna for the **20 meter band** and shorter, this is an excellent DIY candidate.

**The Budget Breakdown:**
* **Two Telescoping Whips:** ~$40
* **Hardware/Hub Materials:** <$20
* **Total Cost:** **Under $60** (assuming you already have a tripod)

It is affordable, effective, and a great way to get a high-performing station on the air without breaking the bank. Happy building!