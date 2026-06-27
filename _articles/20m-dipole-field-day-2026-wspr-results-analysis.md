---
layout: default
title: WSPR Results Analysis on KD3CCO's 20m Rigid V Dipole — Field Day 2026
category: article
published: true
date: 2026-06-27
---


Working with Github Copilot, I previously put together a Jupyter notebook to analyze WSPR results from my DIY 75-10m EFHW. That same notebook is reusable for any WSPR capture, so I pointed it at a different dataset this time: a 48-minute WSPR session captured while running my [DIY rigid V dipole](/hamradio/articles/rigid-v-dipole/) on 20m during Field Day 2026, deployed on top of my [DIY hand-steerable portable mast](/hamradio/articles/portable-mast-build/).

This [repository](https://github.com/hatandspecs/wspr_7510_analysis) contains the Jupyter notebook. The dataset file for this run is `20m_dipole_field_day_2026_spots.tsv`, captured under my own callsign, KD3CCO. A handful of non-20m entries in the raw capture turned out to be data errors (logging artifacts unrelated to this test) and were removed before analysis — every spot in this dataset is on 20m.

The notebook is intentionally structured to explain the purpose of each analysis, guide interpretation of the outputs, and draw conclusions from the actual dataset.

Here's what the antenna under test looks like deployed, for reference:

> DIY 20m rigid V dipole on top of the DIY hand-steerable mast  
<img src="{{ '/assets/images/portable_mast_build/20m_dipole/PXL_20260621_234031295.jpg' | relative_url }}" alt="DIY 20m rigid V dipole on top of the DIY hand-steerable mast">

> The 20m rigid V dipole deployed in the field on the hand-steerable mast  
<img src="{{ '/assets/images/portable_mast_build/20m_dipole/PXL_20260621_234719939.jpg' | relative_url }}" alt="The 20m rigid V dipole deployed in the field on the hand-steerable mast">

---

## 1. Notebook-based Detailed Analysis

Each analysis in the notebook is documented below, followed by the specific findings from the `20m_dipole_field_day_2026_spots.tsv` dataset.

### Analysis 1: Band Openings and Closures

This analysis tracks spot counts and mean SNR across time bins for each band.

**Purpose:**
- Show when individual amateur bands are most active, and whether propagation is strengthening or weakening over time.
- Highlight changes in the Maximum Usable Frequency (MUF) by comparing multiple bands in the same time window.

**How to interpret:**
- A rising spot count means the band is opening and more stations are being heard.
- An increasing mean SNR indicates better signal strength and propagation quality.
- Bands that drop sharply suggest closures or fading conditions.

**Possible conclusions:**
- Identify the best operating times for each band.
- Determine whether the dataset captures a transition from lower-frequency to higher-frequency propagation.
- Spot any bands that remain weak despite others opening, which may suggest local antenna tuning or band-specific absorption.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- Data covers 2026-06-27 from 14:00 UTC through 14:50 UTC, a 48-minute Field Day 2026 test session, in 15-minute bins.
- Only one band is present, 20m, since this is a single-band test and the dataset is cleaned of stray non-20m entries.
- Spot counts and mean SNR by time bin: 358 spots at 14:00 (mean SNR ≈ -11.8 dB), 328 at 14:15 (≈ -12.2 dB), 433 at 14:30 (≈ -9.5 dB), and 54 at 14:45 (≈ -9.8 dB, the closing edge of the window).

**Interpretation from the dataset:**
- Like the 40m loaded-dipole test, this window is too short to say anything real about band opening/closing trends — the rise and fall in spot count here is normal per-cycle variance and the natural edges of the session (the last bin is a partial slice when transmissions stopped), not a propagation shift.
- A multi-hour capture would be needed to say anything meaningful about how this antenna's 20m performance changes with band conditions over the day.


> Band Openings and Closures  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis1_band_openings.png' | relative_url }}" alt="Band Openings and Closures">

---

### Analysis 2: Distance Profiling

This analysis computes mean, maximum, and standard deviation of path distance `k` for every band.

**Purpose:**
- Quantify how far the station is reaching on each band in the dataset.
- Use the band-specific statistics to compare the effective propagation range across frequencies.

**How to interpret:**
- Mean distance is the typical path length heard on each band.
- Maximum distance shows the furthest recorded reach and can indicate DX potential.
- Standard deviation reveals how variable the propagation is during the session.

**Possible conclusions:**
- Bands with higher mean distance are favoring longer skip paths.
- A low standard deviation on a band suggests stable propagation, while a high value indicates mixed local and DX contacts.
- If a high-frequency band has a very small mean distance, the band may be only marginally open.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- `20m` (the only band present): mean ≈ 1873 km, max ≈ 7246 km, std ≈ 1508 km, n = 1173.

**Interpretation from the dataset:**
- The standard deviation (1508 km) is nearly as large as the mean (1873 km) — the same bimodal signature seen in the 40m loaded-dipole test: a lot of short/regional contacts mixed with several genuine long-haul DX paths.
- The single farthest path is `IU0JJD` in JN61tp (central Italy) at 7246 km, decoded twice 30 minutes apart (14:02 and 14:32 UTC) — a real, if brief, transatlantic opening, not a one-off fluke. Two more notable DX paths landed in Austria (`OE3GBB/Q` and `OE3GBB/P`, both JN87aq, 7042 km, both at 14:14) and Germany (`DL1GCD/2`, JN58oh, 6698 km).
- The bulk of the session is short/regional, with these few standout DX paths layered on top, consistent with a 30 ft mast running a half-wave-class dipole on 20m.


> Distance Profiling by Band  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis2_distance_profiling.png' | relative_url }}" alt="Distance Profiling by Band">

---

### Analysis 3: Geographical Spread

This analysis identifies the strongest footprint by the top *receive* grid prefixes.

**Purpose:**
- Visualize the geographic distribution of contacts by the most active Maidenhead grid areas.
- Understand whether the station is mainly heard domestically, regionally, or in long-distance DX regions.

**How to interpret:**
- The top grid prefixes show the regions that contribute the largest number of spots.
- A dense domestic footprint suggests strong local and regional propagation.
- Presence of distant grid squares indicates longer skip or transoceanic paths.

**Possible conclusions:**
- Assess whether the dataset captures mostly local propagation or meaningful DX reach.
- Identify key target regions that the antenna and current conditions favor.
- Use this information to compare with azimuthal coverage and band-specific reach.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- Top 20 receive grid prefixes (stations hearing KD3CCO):

| Rank | Grid | Count | Region |
|------|------|-------|--------|
| 1 | EN82 | 45 | Southeast Michigan |
| 2 | CM87 | 42 | San Francisco Bay Area, California |
| 3 | DN70 | 36 | Colorado Front Range |
| 4 | FM05 | 33 | Central North Carolina |
| 5 | DM13 | 32 | Southern California |
| 6 | FN42 | 28 | Eastern Massachusetts |
| 7 | EM13 | 23 | North Texas / Southern Oklahoma |
| 8 | CM88 | 21 | Northern California |
| 9 | FN30 | 20 | New York City / Long Island |
| 10 | EN52 | 17 | Southern Wisconsin |
| 11 | EM78 | 14 | Kentucky |
| 11 | EM84 | 14 | Northern Georgia |
| 11 | EM79 | 14 | Central Indiana |
| 14 | EL87 | 13 | West-Central Florida |
| 14 | DM79 | 13 | Colorado (Denver/Colorado Springs area) |
| 14 | DN31 | 13 | Northern Utah |
| 14 | FN41 | 13 | Southeastern Massachusetts / Rhode Island |
| 18 | CM98 | 12 | Sacramento Valley, California |
| 19 | EM70 | 11 | Florida Panhandle |
| 19 | EM34 | 11 | Western Arkansas |

**Interpretation from the dataset:**
- This footprint is essentially continental US, with three separate West Coast grids in the top 20 (CM87, CM88, CM98 — all Northern California) plus DN70/DM79 (Colorado) and DN31 (Utah) — real coast-to-coast reach for a 10 W signal off a 30 ft mast.
- No European or other intercontinental grid cracks the top 20 by count — the Italy/Austria/Germany DX paths from Analysis 2 were real but too few individual spots each to show up here, the same pattern flagged in the 40m write-up: max-distance outliers and top-grid-by-count are different questions.
- Geographic spread is broad but fairly even — no single region dominates the way Europe dominated the home EFHW's transatlantic-opening capture.


> Geographical Footprint  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis3_geographical_spread.png' | relative_url }}" alt="Geographical Footprint">

---

### Analysis 4: SNR vs Distance Regression

This analysis examines path loss trends by plotting SNR against distance for each band.

**Purpose:**
- Measure how signal strength declines with distance on each band.
- Compare the relative attenuation characteristics across bands.

**How to interpret:**
- A downward trend is expected: longer distances usually produce lower SNR.
- A tight regression line indicates consistent path loss behavior.
- Scatter far above the trend suggests strong openings or unusually favorable propagation.

**Possible conclusions:**
- Determine whether some bands are behaving more predictably than others.
- Detect bands where antenna performance or local noise may be affecting SNR independently of distance.
- Spot deviations that could indicate special propagation modes or anomalous paths.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- 20m shows the expected downward trend across its full 0-7246 km range, with the regression line pulled down somewhat by the handful of points beyond 5000 km.

**Interpretation from the dataset:**
- The scatter is wide (about +18 dB down to about -27 dB) even within the short-haul cluster — normal for WSPR across many different remote stations and antenna setups, not a sign of anything wrong with this antenna.
- The downward trend holds up well across the whole range, including through the DX cluster past 5000 km, suggesting the antenna's path loss behavior is reasonably consistent rather than dominated by a few anomalous openings.


> SNR vs Distance Regression  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis4_snr_distance.png' | relative_url }}" alt="SNR vs Distance Regression">

---

### Analysis 5: TX vs RX Asymmetry (Local Noise Floor Test)

This comparison uses reciprocal paths involving KD3CCO as both transmitter and receiver.

**Purpose:**
- Compare how the transmit and receive paths perform for the same remote station and band.
- Reveal whether one direction is consistently stronger, which can indicate local noise, feedline loss, or antenna imbalance.

**How to interpret:**
- The histogram of `SNR_delta` shows whether TX or RX is generally stronger.
- Values above zero mean TX reports stronger signals than RX.
- Values below zero mean RX reports stronger signals than TX.

**Possible conclusions:**
- A positive skew suggests the receive path may be suffering from higher local noise or lower sensitivity.
- A negative skew suggests the transmit path may have more loss or less effective radiation.
- A distribution centered near zero indicates roughly symmetric link performance in both directions.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- 35 paired measurements were matched within a ±20 minute window — comparable to the 38 pairs from the original 75-10m EFHW capture despite this being a much shorter session.
- Mean `SNR_delta` = -1.9 dB, median = 0 dB.
- 13 pairs were positive, 17 were negative, and 5 were exactly zero.
- Largest deltas: `K5XL` on 20m: +36 dB (TX stronger) and `N0KSU`: +10 dB; on the negative side, `AA0O`: -21 dB (RX stronger) and `KW4TN`: -18 dB.

**Interpretation from the dataset:**
- This is close to symmetric — slightly RX-favoring on average, the opposite direction from my home EFHW's persistent +6.3 dB TX-favoring skew, and a step further than even the 40m loaded-dipole field test's mild +1.1 dB TX-favoring result.
- That tracks with the deployment context shared with the 40m test: this is a temporary mast in open ground, away from household electrical noise, so there's no obvious local-RX-noise penalty showing up here — if anything, the receive side did marginally better.
- 35 pairs is a reasonable sample for a sub-hour test, though still well short of a multi-hour capture's statistical weight.


> TX vs RX Asymmetry  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis5_tx_rx_asymmetry.png' | relative_url }}" alt="TX vs RX Asymmetry">

---

### Analysis 6: Azimuthal Pattern Mapping

This polar map shows spot direction and distance for KD3CCO transmissions.

**Purpose:**
- Map how signal strength and path length vary with bearing from the station.
- Identify favored antenna lobes and weak nulls in the horizontal plane.

**How to interpret:**
- Angle corresponds to compass bearing.
- Radius corresponds to path distance.
- Color corresponds to received SNR, so brighter points show stronger paths.

**Possible conclusions:**
- Strong clusters in certain directions may reveal directional gain or propagation favoring those headings.
- Low-density sectors may indicate nulls or blocked bearings.
- Comparing distance and color helps separate directional propagation from antenna pattern effects.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- Azimuth of TX spots (KD3CCO heard by others) ranges from 6° to 322°, mean ≈ 230°, std ≈ 76°, n = 839.
- Quadrant split: west (200-340°) 76.0%, east (20-160°) 14.8%, south (160-200°) 8.9%, north (>340° or <20°) 0.2%.

**Interpretation from the dataset:**
- This is a much sharper lopsidedness than the 40m loaded-dipole test's 81.9%/18.1% broadside/end-on split — here a single lobe (west) accounts for over three-quarters of all spots, with the other three sectors combined barely making up the rest.
- This V dipole is hand-steerable per the [portable mast build](/hamradio/articles/portable-mast-build/), so this pattern reflects however it happened to be oriented for this Field Day session, not a fixed, known heading the way my home EFHW's wire is.
- The Italy/Austria/Germany DX paths from Analysis 2 (bearings in the 45-55° range) sit inside the much smaller east sector, not the dominant west lobe — the strongest DX of the session came through a minor lobe, not the major one.
- Without a repeat test at a different heading, it's hard to separate how much of this 76% west skew is the antenna's real pattern versus this particular hour's propagation simply favoring stations to the west.


> Azimuthal Pattern Mapping  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis6_azimuthal_pattern.png' | relative_url }}" alt="Azimuthal Pattern Mapping">

---

### Analysis 7: Band-by-Band Efficiency Normalization

This analysis compares `k/W` across bands for stations that heard KD3CCO on 3 or more bands, to normalize path reach by transmitted power and compare relative efficiency across frequencies.

**Skipped for this dataset:** it requires remote stations heard on 3 or more distinct bands, and this capture has only one band present (20m), so there's no cross-band comparison to make. This antenna was only tested on 20m in this session, so this analysis would only become meaningful if the same station were tested across several bands in one capture.

---

### Analysis 8: Take-Off Angle Inference via Minimum Skip Boundaries

This analysis examines the shortest paths on the higher bands, which informs the likely takeoff angle and near-skip zone.

**Purpose:**
- Use the lower end of the distance distribution to infer whether the antenna favors low-angle, DX-style radiation or higher-angle local propagation.

**How to interpret:**
- Shorter 10th and 25th percentile distances imply that the band includes nearer, low-angle paths.
- Larger values suggest the first usable skip is farther away, which may correspond to a higher takeoff angle.

**Possible conclusions:**
- A small minimum skip boundary is consistent with a low takeoff angle and good near-field performance.
- A large boundary can indicate a high takeoff angle or that the station is primarily hearing longer-range paths.
- Comparing these percentiles across bands helps reveal whether the antenna pattern changes with frequency.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- 10th / 25th / 50th percentile distances:
  - `20m`: 536 / 643 / 1304 km

**Interpretation from the dataset:**
- The 10th percentile (536 km) is well below the median (1304 km), showing a real near-field component mixed in with the longer DX paths — consistent with a 30 ft mast sitting at roughly 0.43λ on 20m per the [Mast Height vs. Wavelength discussion](/hamradio/articles/portable-mast-build/#mast-height-vs-wavelength-nvis-or-dx) in the mast build article, the "general-purpose sweet spot" height that should support both regional and longer-range contacts.


> Takeoff Angle Inference  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis8_takeoff_angle.png' | relative_url }}" alt="Takeoff Angle Inference">

---

### Analysis 9: SSB QSO Feasibility and Minimum Power Mapping

This analysis estimates whether each WSPR spot's path could plausibly support a voice (SSB) contact, and the minimum radio output power that would be required.

WSPR SNR is reported relative to a ~2500 Hz reference bandwidth, which is close to a typical SSB receive bandwidth. That means a spot's reported SNR scales directly with TX power: running the same station harder by `X` dB raises the SNR by the same `X` dB. Feedline loss and antenna gain are properties of the station, not the path, so as long as the same antenna and feedline are used for the WSPR transmission and the hypothetical SSB attempt, they cancel out of this power ratio and aren't modeled as separate inputs.

**Purpose:**
- Identify which spots in the dataset already represent a workable SSB path, and which would need more power than the radio can provide.
- Quantify the minimum TX power required, spot by spot, to clear a configurable SSB SNR margin (default 3 dB).

**How to interpret:**
- `required_tx_power_w` is the radio output power needed to raise that spot's SNR to the configured minimum.
- Spots with `can_make_ssb_qso == True` are achievable within the configured maximum radio power (default 100 W); the rest would need more power than is available.
- The per-band map below colors each path's great-circle line by the required power (jet colormap); paths that can't meet the SSB threshold within the configured maximum power are shown in gray and drawn beneath the others so the most favorable (lowest-power) paths stand out on top.

**Possible conclusions:**
- A high fraction of gray paths on a band suggests SSB is impractical there at the current power level.
- Clusters of low-power (favorable) paths point to directions/bands where an SSB QSO is comfortably within reach.
- Bands where most spots already clear the threshold at low power are good candidates to actually attempt an SSB contact.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`** (3 dB minimum margin, 100 W maximum radio power):
- 20m has a full phone allocation, so nothing is excluded here. Of 1173 spots, 626 (53.4%) could plausibly support an SSB QSO within 100 W, at a median required power of 79.4 W.

**Interpretation from the dataset:**
- This sits between my home EFHW's own 20m figure (37.6% at median 251.2 W) and the 40m loaded-dipole field test's 40m figure (62.3% at median ≈40 W) — a reasonably good showing for a temporary, hand-steered 30 ft mast antenna: just over half of this session's contacts would clear a 3 dB SSB margin at under 80 W.

> 20m — SSB QSO Feasibility Map  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis9_ssb_qso_20m_screenshot.png' | relative_url }}" alt="20m SSB QSO Feasibility Map">  
[Open interactive 20m map]({{ '/assets/20m_dipole_field_day_2026_ssb_qso_20m.html' | relative_url }}){:target="_blank"}

---

### Analysis 10: Interactive Folium Path Map

This analysis creates a folium map showing the transmit and receive paths across bands.

**Purpose:**
- Explore the geographic footprint and path geometry interactively.
- Separate transmit and receive directions to reveal asymmetry in the visible propagation paths.

**How to interpret:**
- Each path line represents a WSPR spot connection and follows the geodesic (great circle) path between TX and RX grid squares.
- Use the checkboxes to filter by band and direction.
- Popup details include TX/RX callsigns, grid locators, SNR, and path distance.

**Actual results for `20m_dipole_field_day_2026_spots.tsv`:**
- An interactive HTML map is saved alongside this article's assets.
- Since only 20m is present, the map's band filter has just one option, but the `heard` vs `heard_by` role filter still separates KD3CCO's TX and RX paths.
- The broad North American fan dominates, with the small number of lines reaching into Italy, Austria, and Germany clearly visible as the longest paths on the map.

**Interpretation:**
- The map confirms the same pattern shown statistically in Analyses 2-4: a wide North American base with a handful of European DX paths layered on top, all concentrated into the dataset's brief 48-minute window.

[Link to Interactive Map]({{ '/assets/20m_dipole_field_day_2026_spots_map.html' | relative_url }}){:target="_blank"}

> Screenshot of Interactive Map  
<img src="{{ '/assets/images/20m_dipole_field_day_2026_wspr_analysis/analysis10_spots_map_screenshot.png' | relative_url }}" alt="Screenshot of Interactive Map">


---

## 2. How to run and reproduce

Open `wspr_7510_analysis.ipynb` in Jupyter, change `TSV_FILENAME` in the configuration cell to `20m_dipole_field_day_2026_spots.tsv`, and execute all cells in order. `CALLSIGN` stays `KD3CCO`, since that's the station that ran the WSPR session during this test.

Dependencies:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `folium`
- `geopy`

The notebook reads the TSV, builds derived fields, runs ten analyses, and displays the results while saving the key images and interactive maps. Analysis 9 (SSB QSO feasibility) and Analysis 10 (interactive path map) both use the helper module `wspr_folium_map.py` to generate their maps.

Analyses 1, 2, 4, and 8 adapt automatically to however many bands are present in a dataset. Analysis 7 specifically requires stations heard on 3 or more distinct bands, so it's skipped on this single-band, 20m-only capture.

---

## 3. Conclusions from this dataset

1. **This was a clean, single-band (20m) capture** from a 48-minute Field Day 2026 session — 1173 spots, all on 20m, after removing a handful of non-20m entries from the raw capture that turned out to be data errors.
2. **Distance spread is wide** (mean ≈1873 km, max 7246 km, std ≈1508 km), blending many short/regional contacts with several genuine transatlantic DX paths into one session — most notably a repeated decode from `IU0JJD` in central Italy at 7246 km, plus paths to Austria and Germany.
3. **TX/RX asymmetry was close to neutral, slightly RX-favoring** (mean -1.9 dB, median 0 dB, 13 positive/17 negative/5 zero pairs) — the opposite direction from my home EFHW's persistent +6.3 dB TX-favoring skew, and a step past even the 40m loaded-dipole field test's mild +1.1 dB TX-favoring result. Consistent with both field tests being run away from household electrical noise.
4. **The azimuthal pattern is sharply lopsided toward one lobe**: 76.0% of TX spots fell in the west sector, versus 14.8% east, 8.9% south, and 0.2% north — a much sharper split than the 40m test's 81.9%/18.1% broadside/end-on result. This V dipole is hand-steerable, so this reflects however it was oriented for this session; a repeat test at a different heading would be needed to confirm this is the antenna's real pattern and not just this hour's propagation.
5. **SSB is realistically within reach on 20m at 100 W** — 53.4% of spots clear a 3 dB margin at a median of just 79.4 W, a result that sits between my home EFHW's own 20m figure (37.6%/251 W) and the 40m loaded-dipole test's 40m figure (62.3%/40 W).
6. **This was a short, single-band, proof-of-concept capture**, not a multi-hour propagation study. It's enough to confirm the rigid V dipole and mast both work well on 20m, catch some real transatlantic DX, and see a believable (if sharply lopsided) lobe pattern, but a longer capture — and ideally a repeat with the V rotated — would be needed to properly characterize this antenna's day-to-day behavior on 20m.
