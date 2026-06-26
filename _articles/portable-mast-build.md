---
layout: default
title: DIY 30 Foot Hand-Steerable Portable Mast
category: article
date: 2026-06-26
---

This article covers the build of a hand-steerable, 30 ft (9.14 m) carbon fiber mast designed to support my [DIY rigid V dipole](/hamradio/articles/rigid-v-dipole/). It's built around an inexpensive telescoping carbon fiber window-washing/duster utility pole from Amazon, fitted with a pair of DIY plywood guy rings that let the whole thing be guyed solidly and still rotated by hand. Once it's up and guyed, the pole comes down in seconds to re-tune or re-band the dipole, and a friend of mine came up with a set of DIY center-loaded whipsn (actually two whips are used per dipole element to get the split in the middle for the coil) for the same hub that work well across the 40m band.

> DIY 20m rigid V dipole on top of the DIY hand-steerable mast  
<img src="{{ '/assets/images/portable_mast_build/20m_dipole/PXL_20260621_234031295.jpg' | relative_url }}" alt="DIY 20m rigid V dipole on top of the DIY hand-steerable mast">

---

## The Pole

The mast itself is this [30 ft (9.14 m) telescoping carbon fiber pole](https://a.co/d/065h0aCn), which ran me about \\$120. It's marketed as a window-washing/duster utility pole, but it's plenty rigid for ham radio use, and once guyed it's solid. It easily supports my DIY rigid V dipole, which is manually tunable anywhere from 20m down to 6m just by extending or collapsing the telescoping whips.

## The Guy Rings

I had three requirements for the guy rings:

1. **Removable** — I use this pole for other things, so the rings shouldn't be permanent.
2. **Free-sliding** — they need to slide on the pole so I can collapse it without removing them first.
3. **Free-rotating** — the pole needs to spin freely inside the rings so I can hand-steer whatever antenna is on top. This is going to matter even more once I build a DIY hexbeam.

To make the rings, I used two nested hole saws to cut discs out of 1/2 in (1.3 cm) plywood — one to cut the outer diameter, and a smaller one to cut the center bore.

> Cutting a guy ring blank from 1/2 in (1.3 cm) plywood with nested hole saws  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260619_001302173.jpg' | relative_url }}" alt="Cutting a guy ring blank from 1/2 in (1.3 cm) plywood with nested hole saws">

Each ring is built from two of these discs. I cut each disc in half separately with a thin pull saw, then stacked the two discs so their split lines cross at 90 degrees to each other. I ended up sizing the rings up a bit from what's shown here, since the bolts I eventually ran through them interfered with the locking clamps on the telescoping pole.

> Cutting a disc in half with a pull saw  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260619_003149221.jpg' | relative_url }}" alt="Cutting a disc in half with a pull saw">

With the two discs stacked and taped together, split lines crossing in the center, I drilled a single 1/4 in (6 mm) hole through the middle of each quadrant — four holes per ring. These are where the eye bolts go, and they serve double duty: holding the two discs together, and giving me a place to tie off the guy lines.

> The two finished ring blanks, taped together and ready for the eye bolt holes to be drilled  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260619_004438390.jpg' | relative_url }}" alt="The two finished ring blanks, taped together and ready for the eye bolt holes to be drilled">

With the eye bolts installed, each ring splits cleanly into two halves that clamp around the pole and bolt back together:

> Top/eye side of the assembled guy ring  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_155017599.jpg' | relative_url }}" alt="Top/eye side of the assembled guy ring">

> Bottom/wing nut side of the assembled guy ring  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_155013965.jpg' | relative_url }}" alt="Bottom/wing nut side of the assembled guy ring">

> Guy ring mounted on the pole, with clearance from the telescoping section's locking collar  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_155541420.jpg' | relative_url }}" alt="Guy ring mounted on the pole, with clearance from the telescoping section's locking collar">

## The Guy Lines: Working Out the Geometry

I wanted to guy the 30 ft (9.14 m) mast at two heights, using only 4 stakes total — one line from the upper ring and one from the lower ring sharing each stake. The rings sit at 10 ft 8 in (3.25 m) and 22 ft 0 in (6.71 m) up the pole.

Since both lines from a given stake share the same anchor point, the stake distance ends up being a single compromise, governed mostly by the upper guy's angle — that's the line doing the real work of resisting sway. The lower guy's job is just to keep the mid-section from bowing, so it can be shallower.

**Recommended: stakes 15 ft (4.57 m) from the base.** At that distance the upper guy comes in at about 34° off the pole, which sits right in the sweet spot — you want the top guy somewhere between 30° and 45° off vertical, since below 30° it stops resisting sway effectively. The lower guy ends up around 55°, which is fine for its supporting role.

Straight-line lengths at 15 ft (4.57 m) (before adding slack for tie-off):

| Ring | Height | Line Length | Angle off Pole |
| :--- | :--- | :--- | :--- |
| Upper | 22 ft 0 in (6.71 m) | 26 ft 8 in (8.13 m) | 34° |
| Lower | 10 ft 8 in (3.25 m) | 18 ft 5 in (5.61 m) | 55° |

I cut four upper lines around 26 ft 8 in (8.13 m) and four lower lines around 18 ft 5 in (5.61 m), then added roughly 2 ft (0.61 m) per line to leave enough to tie off at the ring, the stake, and a line tensioner.

If you've got more or less ground to work with, here's how the numbers move:

| Stake Distance | Upper Line | Lower Line | Upper Angle |
| :--- | :--- | :--- | :--- |
| 12 ft (3.66 m) | 25 ft 1 in (7.65 m) | 16 ft 1 in (4.90 m) | 29° |
| 15 ft (4.57 m) | 26 ft 8 in (8.13 m) | 18 ft 5 in (5.61 m) | 34° |
| 18 ft (5.49 m) | 28 ft 5 in (8.66 m) | 20 ft 11 in (6.38 m) | 39° |

12 ft (3.66 m) is about the practical minimum — the top guy angle drops to ~29° there. 18 ft (5.49 m) stiffens the top noticeably if you have the room for it. One thing worth flagging: there's about 8 ft (2.44 m) of unguyed pole above the top ring, so anything heavy or wind-loaded mounted up there (like the center-loaded 40m whips below) leans hard on that upper guy. If the top of the antenna is carrying much weight or wind load, lean toward the wider 18 ft (5.49 m) spacing.

For the lines themselves, I used fluorescent yellow, reflective paracord — easier to see in low light, and harder to trip over.

## The Ground Sleeve and Stake

To anchor the base of the pole, I made a ground sleeve and stake by U-bolting a length of 2 in (5.1 cm) PVC pipe to a piece of angle iron, then grinding a point onto the angle iron so it drives into the ground easily. It doesn't need to go very deep — just enough to hold the base steady. I'll probably trim the angle iron shorter at some point since there's more length than I actually need.

> The ground sleeve/stake assembly: 2 in (5.1 cm) PVC pipe U-bolted to a pointed length of angle iron  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_161453049.jpg' | relative_url }}" alt="The ground sleeve/stake assembly: 2 in (5.1 cm) PVC pipe U-bolted to a pointed length of angle iron">

## Deploying the Mast

1. Find a spot and hammer the ground stake in a few inches — 8-10 in (20-25 cm) is plenty to secure the base.
2. Measure 15 ft (4.57 m) out from the base in four orthogonal directions and hammer in the guy stakes. Aligning these with North, South, East, and West gives you a convenient reference for hand-steering the antenna later, if you can manage it.
3. Bowline the long guy lines to the top ring's eye bolts, and the short guy lines to the bottom ring's eye bolts.
4. Loop each pair of lines (one long, one short, per direction) through its guy stake, but leave them untensioned for now.

> The mast guyed but still down, with lines run to all four stakes  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_225425138.jpg' | relative_url }}" alt="The mast guyed but still down, with lines run to all four stakes">

5. Push the pole up to height, then tension and lock off each guy line. I use Loop Alien-style line tensioners for this.

> The mast guyed and standing, ready to receive an antenna  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_230648051.jpg' | relative_url }}" alt="The mast guyed and standing, ready to receive an antenna">

## Topping It Off: 20m and 40m

With the mast up, the rigid V hub mounts right on top and the whole thing rotates by hand for steering. On 20m, the [DIY rigid V dipole](/hamradio/articles/rigid-v-dipole/) tunes easily and the mast doesn't even notice the load:

> The mast guyed in the field, with the rigid V dipole deployed for a 20m session  
<img src="{{ '/assets/images/portable_mast_build/20m_dipole/PXL_20260621_233411494.jpg' | relative_url }}" alt="The mast guyed in the field, with the rigid V dipole deployed for a 20m session">

My friend KD3CCP also put together a set of DIY center-loaded whips that thread onto the same hub for 40m. The loading coils add some weight out on the whips, which you can see pulling a visible droop into the elements at the hub. I ran a [WSPR test session on this exact setup](/hamradio/articles/40m-center-loaded-dipole-wspr-results-analysis/), if you want to see how it actually performed:

> Close-up of one of the DIY center-loading coils partway up the whip  
<img src="{{ '/assets/images/portable_mast_build/40m_loaded_dipole/PXL_20260622_003600931.jpg' | relative_url }}" alt="Close-up of one of the DIY center-loading coils partway up the whip">

> The loading coils visibly droop the whips under their own weight  
<img src="{{ '/assets/images/portable_mast_build/40m_loaded_dipole/PXL_20260622_004749393.jpg' | relative_url }}" alt="The loading coils visibly droop the whips under their own weight">

Even with that extra weight up top, the mast and guying handle it without issue. The 40m center loaded rigid V ends up drooping to more of a horizontal dipole, but that's not bad and it tuned up well:

> DIY 40m center-loaded rigid V dipole on top of the DIY hand-steerable mast  
<img src="{{ '/assets/images/portable_mast_build/40m_loaded_dipole/PXL_20260622_004738841.jpg' | relative_url }}" alt="DIY 40m center-loaded rigid V dipole on top of the DIY hand-steerable mast">

---

## Mast Height vs. Wavelength: NVIS or DX?

While possible within the limits of the guying, I don't intend to change teh mast height as I switch bands.  However the same 30 ft (9.14 m) of physical height is a very different number electrically depending on what's plugged into the hub. The vertical radiation pattern of a horizontal (or near-horizontal V) dipole is governed by its height in wavelengths above ground, and that's what decides whether the antenna favors near-vertical incidence skywave (**NVIS**, good for working stations a few hundred miles out with no skip zone) or a low takeoff angle (good for long-haul **DX**).

As a rule of thumb for a dipole over average ground:

* **Below ~0.25λ** — radiation is concentrated nearly straight up. This is NVIS territory: great for regional communication within a few hundred miles, at the cost of low-angle gain.
* **Around 0.5λ** — the pattern peels away from the zenith, settling toward a **~25-30° takeoff angle**. This is the classic general-purpose height, a reasonable compromise between regional and DX work.
* **0.75λ and up** — takeoff angle keeps dropping, favoring low-angle DX, though the pattern starts splitting into multiple lobes at different elevation angles (a topic which I don't know too much about yet).

Here's where the apex of this mast (30 ft / 9.14 m) lands on each band the rigid V hub can cover, along with the recommended telescoping whip length (per leg) to hit resonance on each one, using the standard quarter-wave rule of thumb (234 / f(MHz)):

| Band | Ref. Freq | Full λ | λ/2 | Element Length (ea. leg) | Mast Height in λ | Expect |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40m | 7.15 MHz | 41.9 m (137.6 ft) | 21.0 m (68.8 ft) | 997 cm (32 ft 9 in) | **0.22λ** | NVIS-dominant |
| 30m | 10.125 MHz | 29.6 m (97.2 ft) | 14.8 m (48.6 ft) | 704 cm (23 ft 1 in) | **0.31λ** | High-angle, regional-leaning |
| 20m | 14.2 MHz | 21.1 m (69.3 ft) | 10.6 m (34.6 ft) | 502 cm (16 ft 6 in) | **0.43λ** | General-purpose sweet spot |
| 17m | 18.1 MHz | 16.6 m (54.4 ft) | 8.3 m (27.2 ft) | 394 cm (12 ft 11 in) | **0.55λ** | Transitioning to low-angle |
| 15m | 21.2 MHz | 14.1 m (46.4 ft) | 7.1 m (23.2 ft) | 336 cm (11 ft 0 in) | **0.65λ** | DX-leaning |
| 12m | 24.9 MHz | 12.0 m (39.5 ft) | 6.0 m (19.8 ft) | 286 cm (9 ft 5 in) | **0.76λ** | DX-leaning |
| 10m | 28.4 MHz | 10.6 m (34.6 ft) | 5.3 m (17.3 ft) | 251 cm (8 ft 3 in) | **0.87λ** | Low-angle DX |
| 6m | 50.1 MHz | 6.0 m (19.6 ft) | 3.0 m (9.8 ft) | 142 cm (4 ft 8 in) | **1.53λ** | Multi-lobe; VHF propagation modes dominate anyway |

Note: TBD I'm going to update these whip lengths to exact measured values, but for now these are theoretical.

The 20m figure lines up with real-world experience — the [rigid V dipole](/hamradio/articles/rigid-v-dipole/) write-up extended each whip to about 5 m (16 ft 5 in) and only needed a few inches of trim to find the sweet spot.  I have noticed putting the antenna higher seems to raise the resonant frequency, so I found if tuning the antenna in the down position, I should tune it a little low so when I raise it to the full extension of the mast it will end up where I want it. The 40m and 30m figures, on the other hand, call for 997 cm (32 ft 9 in) and 704 cm (23 ft 1 in) of element respectively — well beyond what an 18 ft (549 cm) telescoping whip can reach on its own. That's exactly why 40m needs the center-loading coils rather than just cranking the whip out further; 30m would need the same treatment.  

Note: KD3CCP didn't magically insert a coil in the middle of the 18 foot whip, it clamps on the tip of a partially extended 18 foot whip, and an additional shorter whip is screwed onto the end.  I am looking forward to getting a set of these coils he made!

On **40m and 30m**, this mast puts the apex well under half a wavelength up, so the elements radiate mostly straight overhead. This limitation can be a feature, not a bug, if the goal is reliable regional contacts — POTA hunters, state and county nets, and the like — with no skip zone to fight. It's not the height I'd pick if 40m DX were the priority; that would call for getting the apex closer to 70 ft (21.3 m).  I can't find a 70 foot pole on Amazon yet.

**20m**, at roughly 0.43λ, lands almost where the classic "half-wave-high dipole" advice points — a solid all-around compromise between regional contacts and DX, which tracks with how well this height has performed in practice so far.

From **17m on up through 10m**, the same 30 ft (9.14 m) of mast represents a steadily larger fraction of a wavelength, and the takeoff angle should keep dropping accordingly — electrically, this is a much "taller" DX antenna on 10m than it is on 40m.

**6m** is a special case and one I have the least experience with and have read the least about. My current understanding is that over 1.5λ up, the simple "height sets the takeoff angle" model starts breaking into multiple lobes instead of one clean low-angle beam, but my current limited understanding is it mostly doesn't matter — 6m propagation leans on sporadic-E, meteor scatter, and tropo ducting rather than classic F-layer NVIS/skywave, so the antenna just needs to get the energy out at a reasonably low angle, which this height does fine.  I haven't found anyone to talk to on 6m yet, so TBD I'm going to try to run some 6m WSPR with the antenna at various fractions of a wavelength above the ground and hopefully get enough WSPR spots to learn something about it.

One more detail worth flagging: this is a vertical V, not an inverted V — the hub sits at the bottom of the V, and the elements slope upward and outward from it at 120°, so the tips end up above the apex, not below it. The longer the element (the lower the band), the higher above the mast top the tips reach. That means the real effective height of the radiating elements is consistently a bit higher than the simple apex-height numbers in the table above, nudging every band slightly toward a lower takeoff angle than indicated — most noticeably on the lower bands, where the legs are longest.

These are general expectations from my most basic understanding of dipole-over-ground theory, not measured pattern data (yet, except for 40m) — I haven't run this through modeling software or compared real-world reports band-by-band yet, but it's a reasonable framework for picking which band to chase regional contacts versus DX on a given outing.

---

## Final Thoughts

Once guyed, the pole is very rigid and easily supports both of these DIY dipoles without any noticeable sway. It also steers smoothly by hand while fully deployed, which is great for putting up a rigid dipole and will be essential once I get around to building a DIY hexbeam.

The whole assembly collapses down small and is easy to store and transport.

> The collapsed mast with both guy rings still attached, leaning in a corner  
<img src="{{ '/assets/images/portable_mast_build/PXL_20260621_204211189.jpg' | relative_url }}" alt="The collapsed mast with both guy rings still attached, leaning in a corner">

I also mounted a broom-handle-to-camera-tripod thread adapter on the pole, along with an Arca-Swiss style clamp, since I like to mount my antennas on Arca-Swiss plates so they're quick to swap between poles and tripods.

Total cost came out to about \\$120 for the pole and another \\$50-75 in hardware, paracord, and four tent stakes. I haven't found a non-DIY equivalent that comes close to that price.
