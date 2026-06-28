---
layout: default
title: WSPR Results Analysis on KD3CCO's 15m Rigid V Dipole — Field Day 2026
category: article
published: true
date: 2026-06-27
---


Working with Github Copilot, I previously put together a Jupyter notebook to analyze WSPR results from my DIY 75-10m EFHW. That same notebook is reusable for any WSPR capture, so I pointed it at a different dataset this time: a 46-minute WSPR session captured while running my [DIY rigid V dipole](/hamradio/articles/rigid-v-dipole/) on 15m during Field Day 2026, deployed on top of my [DIY hand-steerable portable mast](/hamradio/articles/portable-mast-build/). It's the same physical antenna used in the [20m WSPR test](/hamradio/articles/20m-dipole-field-day-2026-wspr-results-analysis/), with the telescoping whips shortened to resonate on 15m instead.

This [repository](https://github.com/hatandspecs/wspr_7510_analysis) contains the Jupyter notebook. The dataset file for this run is `15m_dipole_field_day_2026_spots.tsv`, captured under my own callsign, KD3CCO. Unlike the 20m capture, this one came out clean — every spot in the raw file is on 15m, no stray entries to filter out.

The notebook is intentionally structured to explain the purpose of each analysis, guide interpretation of the outputs, and draw conclusions from the actual dataset.

Here's what the antenna under test looks like deployed, for reference (same hub and whips as the 20m test, just retuned shorter for 15m):

> The 15m rigid V dipole deployed at the Field Day 2026 site  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/field_day_2026_15m_dipole.jpg' | relative_url }}" alt="The 15m rigid V dipole deployed at the Field Day 2026 site">

---

## 1. Notebook-based Detailed Analysis

Each analysis in the notebook is documented below, followed by the specific findings from the `15m_dipole_field_day_2026_spots.tsv` dataset.

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- Data covers 2026-06-27 from 16:24 UTC through 17:10 UTC, a 46-minute Field Day 2026 test session, in 15-minute bins.
- Only one band is present, 15m, since this antenna was only tested on 15m in this session.
- Spot counts and mean SNR by time bin: 111 spots at 16:15 (mean SNR ≈ -13.3 dB, a partial bin since the session starts at 16:24), 563 at 16:30 (≈ -14.4 dB), 288 at 16:45 (≈ -14.5 dB), and 146 at 17:00 (≈ -14.2 dB, another partial bin at the close).

**Interpretation from the dataset:**
- Like the 40m loaded-dipole and 20m field tests, this window is too short to say anything real about band opening/closing trends — the dip and partial edge bins here are normal artifacts of a sub-hour test, not a propagation shift.
- Mean SNR is fairly stable across the whole session (-13 to -14.5 dB), suggesting consistent conditions rather than a band that's opening or fading during the capture.


> Band Openings and Closures  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis1_band_openings.png' | relative_url }}" alt="Band Openings and Closures">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- `15m` (the only band present): mean ≈ 3871 km, max ≈ 16744 km, std ≈ 2719 km, n = 1108.

**Interpretation from the dataset:**
- This mean distance (3871 km) is more than double the 20m test's mean (1873 km) — 15m in this capture is skewing much more toward DX and much less toward short/regional contacts.
- The single farthest path is `VK5ARG` in PF95ht (South Australia) at 16744 km, decoded once at 17:06 UTC.
- The real standout is `ZL2005SWL` in RE68mx (New Zealand) at 14237 km — decoded 8 separate times, at 16:26, 16:30, 16:34, 16:38, 16:44, 16:48, 16:52, and 17:06 UTC. That's a sustained opening covering almost the entire 46-minute session, not a brief or one-off catch.


> Distance Profiling by Band  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis2_distance_profiling.png' | relative_url }}" alt="Distance Profiling by Band">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- Top 20 receive grid prefixes (stations hearing KD3CCO):

| Rank | Grid | Count | Region |
|------|------|-------|--------|
| 1 | JN47 | 59 | Switzerland / Southern Germany / Austria border (Lake Constance area) |
| 2 | JN58 | 42 | Southern Germany (Munich area) |
| 3 | DN70 | 31 | Colorado Front Range |
| 4 | EN82 | 29 | Southeast Michigan |
| 4 | DM13 | 29 | Southern California |
| 6 | FM05 | 26 | Central North Carolina |
| 7 | JO40 | 23 | Central Germany |
| 7 | JN87 | 23 | Western Hungary / Eastern Austria |
| 9 | CM87 | 22 | San Francisco Bay Area, California |
| 10 | EN52 | 19 | Southern Wisconsin |
| 11 | IO86 | 18 | Scotland |
| 12 | CM88 | 17 | Northern California |
| 13 | EM84 | 16 | Northern Georgia |
| 13 | JN48 | 16 | Southern Germany (Stuttgart area) |
| 13 | DN31 | 16 | Northern Utah |
| 13 | EN58 | 16 | Northern Minnesota / Ontario border |
| 17 | JN28 | 15 | Northeastern France / Belgium border |
| 17 | JO33 | 15 | Northwestern Germany |
| 19 | EM38 | 14 | Central Missouri |
| 20 | JO31 | 12 | Western Germany (Ruhr area) |

**Interpretation from the dataset:**
- This is a Europe-heavy footprint: 8 of the top 20 grids (JN47, JN58, JO40, JN87, JN48, JN28, JO33, JO31) are European, and the single largest grid overall (JN47, 59 spots) is in central Europe.
- This is a sharp contrast with the 20m test, where no European grid cracked the top 20 by count at all — 15m in this session clearly favored a sustained transatlantic path over domestic reach.
- US grids are still well represented (Colorado, Michigan, California x2, North Carolina, Wisconsin, Georgia, Utah, Missouri), so this wasn't an exclusively DX-only session, just one weighted more toward Europe than the 20m capture.


> Geographical Footprint  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis3_geographical_spread.png' | relative_url }}" alt="Geographical Footprint">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- 15m shows the expected downward trend across its full 0-16744 km range, with SNR running from about +25 dB at short range down to about -27 dB on the longest DX paths.

**Interpretation from the dataset:**
- The trend holds up well even out past 14000 km — the New Zealand and Australia paths sit right where the regression line predicts for their distance, not as wild outliers, which is a good sign that this isn't a fluke decode but a genuine, well-behaved opening.
- The short-range end of the scatter (+25 dB at a few hundred km) shows the antenna is also working fine for closer contacts, not just DX.


> SNR vs Distance Regression  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis4_snr_distance.png' | relative_url }}" alt="SNR vs Distance Regression">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- Only 10 paired measurements were matched within a ±20 minute window — a much smaller sample than the 35 pairs in the 20m test, since KD3CCO's own RX side only logged 153 spots in this short session.
- Mean `SNR_delta` = -0.2 dB, median = -3.0 dB.
- 3 pairs were positive, 7 were negative, none were exactly zero.
- Largest deltas: `WA4GLH` on 15m: +16 dB and +15 dB across two cycles (TX stronger); on the negative side, `W1CLM`: -15 dB and `5Z4GO`: -9 dB (RX stronger).

**Interpretation from the dataset:**
- The median (-3 dB) and the 7-of-10 negative split both point mildly RX-favoring, similar in direction to the 20m test, but with only 10 pairs this is too small a sample to draw a real conclusion from — it would only take one or two different cycles to flip the picture.
- A longer capture would be needed to get a TX/RX asymmetry read on this antenna at 15m that's actually trustworthy.


> TX vs RX Asymmetry  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis5_tx_rx_asymmetry.png' | relative_url }}" alt="TX vs RX Asymmetry">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- Azimuth of TX spots (KD3CCO heard by others) ranges from 2° to 317°, mean ≈ 166°, std ≈ 110°, n = 955.
- Quadrant split: west (200-340°) 47.1%, east (20-160°) 45.8%, south (160-200°) 6.4%, north (>340° or <20°) 0.7%.

**Interpretation from the dataset:**
- This is nearly an even east/west split — a sharp contrast with the 20m test's heavily lopsided 76.0%/14.8% west/east result. Either this V was oriented differently for this session, or 15m propagation that hour was genuinely more balanced between the two headings.
- Both standout DX paths from Analysis 2 fall in the west sector: `VK5ARG` (Australia) at 271° and `ZL2005SWL` (New Zealand) at 245°. The sustained New Zealand opening rode the larger of the two main lobes, not a minor one.
- The near-absence of north (0.7%) and the small south sector (6.4%) suggest a genuine broadside east/west pattern rather than a more circular or omnidirectional response, consistent with this being a dipole rather than something like a vertical.


> Azimuthal Pattern Mapping  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis6_azimuthal_pattern.png' | relative_url }}" alt="Azimuthal Pattern Mapping">

---

### Analysis 7: Band-by-Band Efficiency Normalization

This analysis compares `k/W` across bands for stations that heard KD3CCO on 3 or more bands, to normalize path reach by transmitted power and compare relative efficiency across frequencies.

**Skipped for this dataset:** it requires remote stations heard on 3 or more distinct bands, and this capture has only one band present (15m), so there's no cross-band comparison to make. This antenna was only tested on 15m in this session, so this analysis would only become meaningful if the same station were tested across several bands in one capture.

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- 10th / 25th / 50th percentile distances:
  - `15m`: 598 / 1240 / 3613 km

**Interpretation from the dataset:**
- All three percentiles here are noticeably higher than the 20m test's (536 / 643 / 1304 km) — even the near end of this session's distance distribution is farther out, consistent with the much more DX-leaning footprint seen in Analyses 2 and 3.
- Per the [Mast Height vs. Wavelength discussion](/hamradio/articles/portable-mast-build/#mast-height-vs-wavelength-nvis-or-dx) in the mast build article, the same 30 ft mast sits at roughly 0.65λ on 15m — solidly in the "DX-leaning" range rather than 20m's "general-purpose" 0.43λ — which lines up with this band running farther and DX-heavier than the 20m capture.


> Takeoff Angle Inference  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis8_takeoff_angle.png' | relative_url }}" alt="Takeoff Angle Inference">

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`** (3 dB minimum margin, 100 W maximum radio power):
- 15m has a full phone allocation, so nothing is excluded here. Of 1108 spots, 323 (29.2%) could plausibly support an SSB QSO within 100 W, at a median required power of 501.2 W.

**Interpretation from the dataset:**
- This pass rate (29.2%) is the lowest of the three antenna/band combinations tested so far — well below the 20m test's 53.4% and the 40m loaded-dipole test's 62.3% — and the median required power (501.2 W) is more than 6x the 20m test's 79.4 W.
- This isn't a sign of an underperforming antenna; it's the direct consequence of this capture skewing heavily toward long DX paths (mean distance more than double the 20m test's), which start from a lower SNR baseline and need much more power to clear an SSB margin.
- The short-range contacts in this dataset (the same ones visible at the top of Analysis 4's scatter) are exactly where the low-power, favorable paths on the map below cluster — SSB is still realistic on 15m with this antenna, just more selectively than on 20m.

> 15m — SSB QSO Feasibility Map  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis9_ssb_qso_15m_screenshot.png' | relative_url }}" alt="15m SSB QSO Feasibility Map">  
[Open interactive 15m map]({{ '/assets/15m_dipole_field_day_2026_ssb_qso_15m.html' | relative_url }}){:target="_blank"}

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

**Actual results for `15m_dipole_field_day_2026_spots.tsv`:**
- An interactive HTML map is saved alongside this article's assets.
- Since only 15m is present, the map's band filter has just one option, but the `heard` vs `heard_by` role filter still separates KD3CCO's TX and RX paths.
- The dense European cluster from Analysis 3 is immediately visible, alongside the two long lines reaching to New Zealand and Australia that stand out from everything else on the map.

**Interpretation:**
- The map confirms the same pattern shown statistically in Analyses 2-4: a solid European base layered with US domestic contacts, plus one sustained antipodal-distance opening that dominates the visual.

[Link to Interactive Map]({{ '/assets/15m_dipole_field_day_2026_spots_map.html' | relative_url }}){:target="_blank"}

> Screenshot of Interactive Map  
<img src="{{ '/assets/images/15m_dipole_field_day_2026_wspr_analysis/analysis10_spots_map_screenshot.png' | relative_url }}" alt="Screenshot of Interactive Map">


---

## 2. How to run and reproduce

Open `wspr_7510_analysis.ipynb` in Jupyter, change `TSV_FILENAME` in the configuration cell to `15m_dipole_field_day_2026_spots.tsv`, and execute all cells in order. `CALLSIGN` stays `KD3CCO`, since that's the station that ran the WSPR session during this test.

Dependencies:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `folium`
- `geopy`

The notebook reads the TSV, builds derived fields, runs ten analyses, and displays the results while saving the key images and interactive maps. Analysis 9 (SSB QSO feasibility) and Analysis 10 (interactive path map) both use the helper module `wspr_folium_map.py` to generate their maps.

Analyses 1, 2, 4, and 8 adapt automatically to however many bands are present in a dataset. Analysis 7 specifically requires stations heard on 3 or more distinct bands, so it's skipped on this single-band, 15m-only capture.

---

## 3. Conclusions from this dataset

1. **This was a clean, single-band (15m) capture** from a 46-minute Field Day 2026 session — 1108 spots, all on 15m, with no data issues to filter out this time.
2. **The standout result is a sustained New Zealand opening**: `ZL2005SWL` (RE68mx, 14237 km) was decoded 8 separate times across the session, from 16:26 to 17:06 UTC — almost the entire 46-minute capture. A single Australia decode (`VK5ARG`, 16744 km) came in at the very end. Both are real, well-behaved points on the SNR/distance trend, not anomalous flukes.
3. **The footprint skews heavily European** compared to the 20m test — 8 of the top 20 grids are in Europe, and the largest single grid (JN47, central Europe) had nearly twice the count of any US grid. Mean distance (3871 km) is more than double the 20m capture's.
4. **The azimuthal pattern is close to an even east/west split** (47.1%/45.8%), a sharp contrast with the 20m test's heavily lopsided 76.0%/14.8% result. Both major DX paths (New Zealand and Australia) rode the west lobe.
5. **TX/RX asymmetry leaned mildly RX-favoring** (mean -0.2 dB, median -3 dB, 7 of 10 pairs negative), similar in direction to the 20m test, but the sample (10 pairs) is too small to treat as a reliable result.
6. **SSB odds were the weakest of the three tests so far** — only 29.2% of spots clear a 3 dB margin within 100 W, at a median of 501.2 W, well behind 20m's 53.4%/79.4 W and the 40m loaded dipole's 62.3%/≈40 W. That's a direct consequence of this session being DX-heavy rather than a problem with the antenna — the short-range contacts in this same dataset are still comfortably workable on SSB.
