---
layout: default
title: Lessons in Velocity Factor, A 20m T2LT Build
category: article
date: 2026-02-28
---


This week, I spent some time experimenting with a **Tuned Transmission Line Trap (T2LT)** antenna. My goal was to create something ultra-light for field use, so I reached for some lightweight materials I had in the shop: **RG-316 coax** and **AWG 22 antenna wire**.

The T2LT is a fantastic design for portable ops because the antenna and the feedline are essentially the same piece of cable, making it incredibly stealthy and easy to deploy.

<img src="{{ '/assets/images/diy_t2lt/4.jpeg' | relative_url }}" alt="stowed 20m t2lt antenna" width="600">


---

## The Build Specs: 20m Band

Here is the breakdown of the measurements and materials used for this specific build:

* **Radiator (Top Section):** 4.9 meters of AWG 22 antenna wire.
* **Sleeve Section (Lower Radiator):** 4.9 meters of RG-316 coax.
* **Assembly:** The AWG 22 wire is soldered directly to the center conductor of the RG-316. I used two layers of adhesive-lined heat shrink to provide robust strain relief at the solder joint.
* **The Trap (RF Choke):** I used an **FT140-43 ferrite toroid** with **14 turns** of the RG-316 coax. 

The placement of the trap is critical: it is positioned exactly **16 feet 1 inch** from the point where the top wire attaches. This creates the high impedance necessary to "stop" the antenna and keep the rest of the feedline "cold" (RF-free).

<img src="{{ '/assets/images/diy_t2lt/2.jpeg' | relative_url }}" alt="test choke" width="600">


During bench testing, this choke measured at least **-35dB of suppression** across the 20m band, which is exactly what you want to see for effective common-mode rejection.

<img src="{{ '/assets/images/diy_t2lt/3.jpeg' | relative_url }}" alt="choke measurement" width="600">

---

## The "Aha!" Moment: Velocity Factor

If you build one of these, watch out for a common pitfall regarding **Velocity Factor (VF)**. I originally calculated the lower 1/4 wavelength section using a VF of **0.7** because that is the standard rating for RG-316. 

However, I quickly realized my mistake: **when coax is used as an antenna radiator, the RF travels on the *outside* of the shield.** In this scenario, the VF is closer to **0.95**, not 0.7. 

My first attempt was four feet too short, and the **nanoVNA** immediately showed the resonance was way too high. I had to unwrap the choke and move it to the **16' 1"** mark. Once I corrected for the proper velocity factor, I was right in the ballpark and only needed a tiny bit of trimming on the top wire to hit my target frequency.

<img src="{{ '/assets/images/diy_t2lt/1.jpeg' | relative_url }}" alt="great swr and bandwidth on the completed t2lt" width="600">


---

## Field Testing vs. The Wind

Deployment was incredibly fast—it took only about five minutes to get the telescoping pole up and the antenna on the air. 

Testing took place on a particularly gusty Friday night. I was using a **34 foot carbon fiber "POTA" pole**, and while the manufacturer claims they are freestanding without support, I felt like I was placing a $150 wager against the valley winds. 

<img src="{{ '/assets/images/diy_t2lt/0.jpeg' | relative_url }}" alt="deployed t2lt" width="600">


Even as the pole reached the limits of its elastic modulus, it held up beautifully. The antenna performed well; I heard plenty of activity on 20m, and **KD3CCP** even caught me calling CQ on his SDR across town.

### Final Verdict
I eventually packed it in when the gusts got too intense, but teardown took a mere three minutes. If you want a lightweight, high-performance antenna that you can deploy in minutes, the T2LT is hard to beat—just remember to calculate your lengths based on the outside of the wire!