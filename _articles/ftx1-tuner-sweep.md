---
layout: default
title: Automating Tuner Memories on the FTX-1 with a CAT-Controlled Band Sweep
category: article
date: 2026-08-01
---

I picked up a mAT-Tuner mAT-30 external automatic antenna tuner for the FTX-1 Optima, and it's great once it's broken in on a given antenna. It stores a tuning memory per frequency, so after it's learned a band it snaps to a match almost instantly. The problem is the learning part. Every time I put the radio on a new or different antenna, I'd have to walk the VFO across a band a step at a time and manually trigger a tune at each stop before the memories were actually useful. That's fine for a couple of test points, tedious for a whole band, and I have several bands and swap antennas often enough that this became the actual bottleneck in getting on the air.

So I built a small tool to do it for me: a local web app that steps the FTX-1's VFO across whatever bands I pick and triggers the mAT-30 at each stop, unattended.

> The app after a completed 12m sweep, VFO/mode/power/tuner telemetry on the left, live sweep log on the right
<img src="{{ '/assets/images/ftx1_tuner_sweep/12m-sweep-complete.png' | relative_url }}" alt="The app after a completed 12m sweep, VFO/mode/power/tuner telemetry on the left, live sweep log on the right">

Code's up at [github.com/hatandspecs/ftx1-tuner-sweep](https://github.com/hatandspecs/ftx1-tuner-sweep) if you want to run it yourself or just poke at how it talks to the radio.

---

## Digging into the CAT protocol

The FTX-1 is new enough that I couldn't just find someone else's tested command reference and trust it. I pulled Yaesu's actual FTX-1 CAT Operation Reference Manual and worked from the primary source rather than guessing at command syntax. Three commands do the real work:

* **`FA`** sets or reads the VFO frequency
* **`AC`** controls the antenna tuner: which tuner (internal or external), and whether it's off, on, or actively starting a tuning cycle
* **`RI`** reads back radio status, including a bit that's supposed to say whether the tuner is currently cycling

The `AC` command turned out to be the interesting one. It takes three parameters, and setting them to "external tuner, start tuning" is functionally identical to holding the front-panel TUNER button for two seconds. That's exactly the trigger the mAT-30 is wired to respond to on the TUNER/LINEAR jack, so CAT control and the physical button end up doing the same thing.

## The gotcha: the radio doesn't know when the tuner is done

My first version polled that `RI` status bit in a loop after triggering a tune, expecting it to flip back to "not tuning" as soon as the mAT-30 finished its cycle, then move on to the next frequency. In testing, it never did. Every single step sat there for the full timeout regardless of how fast the tuner actually finished.

The reason makes sense once you think about the wiring: the mAT-30 is a third-party tuner that does its SWR search completely on its own once triggered. The interface it uses is essentially one-way, a start signal out to the tuner, with no real feedback path telling the radio "I'm done." The FTX-1 can track this for its own internal coupler, where it's directly driving the relays, but it has no way to know what an external tuner is doing.

So the tool doesn't try to detect completion anymore. It just holds each frequency for a fixed dwell time (I've settled on 5 seconds) that comfortably covers how long the mAT-30 actually takes, then moves on. Simpler and it actually works.

## Staying inside my license and off the edges

I didn't want a "sweep the whole band" tool that cheerfully transmits across segments I'm not licensed for or right on a hard band boundary, so two things went into the sweep logic itself:

**License-aware band selection.** The app reads a plain text file of license classes and their legal frequency ranges, and the band checkboxes only show what's actually legal for the class you pick. US General, my default, has mode-restricted splits on several bands, like 80m having a CW/data segment and a separate phone segment with an Extra-only gap between them, and the tool sweeps every listed segment for a band, not the gap. I pulled the US figures straight from 47 CFR 97.301 rather than a summary site, so those are exact. I don't operate outside the US, so the file also has some clearly-flagged placeholder entries for other countries built from the raw ITU region allocation tables rather than fabricated per-country tables. If you're outside the US, treat those as an outer boundary, not your actual privileges.

**Edge padding.** Within a swept segment, the first frequency lands 1 kHz above the segment's lower edge and the last one 1 kHz below its upper edge, so it never transmits exactly on a hard boundary. Everything in between lands on a clean 10 kHz grid. US General's 80m phone segment, for example, sweeps 3.801, then 3.810, 3.820, ... 3.990, then 3.999, not 3.800 or 4.000 themselves.

## Leaving the radio in a sane state

One thing I caught after actually using this for a bit: my first version turned the tuner fully off between steps and at the end of a sweep, which meant I'd finish a sweep and come back to the radio with the tuner bypassed. Not what I wanted. It's fixed now to leave the tuner enabled, in circuit, both between steps and no matter how a sweep ends, whether it finishes normally, gets stopped, or the connection drops mid-sweep.

## Field testing

I ran it against the real FTX-1 Optima and mAT-30 on 15m and 12m. Both the completion-detection issue and the tuner-left-off issue above turned up from actually using it, not from reading the manual, which is exactly why I didn't trust this until I'd run it for real. The screenshot above is a completed 12m sweep at 10 kHz steps and 5 W, mAT-30 cycling through eleven stops with no intervention.

## One operating note

Every step here is a real transmission, brief but real, and the tool has no way to know if a frequency is already in use before it keys up there. I only run this when a band sounds dead or nearly so, at the minimum power that gets a reliable tune (5 W has been plenty), and I keep an ear on it so I can stop it immediately if I'm about to sweep across someone.
