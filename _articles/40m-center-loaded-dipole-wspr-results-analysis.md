---
layout: default
title: WSPR Results Analysis on KD3CCP's 40m Center-Loaded Rigid V Dipole
category: article
published: true
date: 2026-06-26
---


Working with Github Copilot, I previously put together a Jupyter notebook to analyze WSPR results from my DIY 75-10m EFHW. That same notebook is reusable for any WSPR capture, so I pointed it at a different dataset this time: a 30-minute WSPR session captured while field-testing my friend KD3CCP's DIY 40m center-loaded rigid V dipole, deployed on top of my [DIY hand-steerable portable mast](/hamradio/articles/portable-mast-build/).

This [repository](https://github.com/hatandspecs/wspr_7510_analysis) contains the Jupyter notebook. The dataset file for this run is `40m_loaded_dipole_30ft_mast_spots.tsv`, captured under my own callsign, KD3CCO, since the WSPR transmissions during the mast test were run from my station.

The notebook is intentionally structured to explain the purpose of each analysis, guide interpretation of the outputs, and draw conclusions from the actual dataset. It also adapts automatically to however many bands are present — since this capture is 40m-only, a couple of the multi-band analyses skip themselves as designed.

Here's what the antenna under test looks like deployed, for reference:

> Close-up of one of KD3CCP's DIY center-loading coils, partway up the whip  
<img src="{{ '/assets/images/portable_mast_build/40m_loaded_dipole/PXL_20260622_003600931.jpg' | relative_url }}" alt="Close-up of one of KD3CCP's DIY center-loading coils, partway up the whip">

> The 40m center-loaded rigid V dipole deployed on top of the hand-steerable mast  
<img src="{{ '/assets/images/portable_mast_build/40m_loaded_dipole/PXL_20260622_004738841.jpg' | relative_url }}" alt="The 40m center-loaded rigid V dipole deployed on top of the hand-steerable mast">

---

## 1. Notebook-based Detailed Analysis

Each analysis in the notebook is documented below, followed by the specific findings from the `40m_loaded_dipole_30ft_mast_spots.tsv` dataset.

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- Data covers a deliberately short window: 2026-06-21 from 21:30 UTC through 22:00 UTC, only 30 minutes.
- Only one band is present, 40m, since this antenna is purpose-built for that band alone.
- Spot counts and mean SNR by 15-minute time bin:
  - `21:30` bin: 324 spots, mean SNR ≈ -7.9 dB.
  - `21:45` bin: 491 spots, mean SNR ≈ -7.9 dB.
  - `22:00` bin (the closing edge of the window): 11 spots, mean SNR ≈ -16.5 dB.

**Interpretation from the dataset:**
- This analysis isn't really meaningful over a window this short. With only 30 minutes and 3 time bins, the rise and fall here is just noise and the natural edges of a single test session, not a real band-opening/closing trend the way it would be over a multi-hour capture.
- A multi-hour capture, like the 75-10m EFHW dataset, would be needed to say anything meaningful about how this antenna's 40m performance changes with band conditions over an evening.


> Band Openings and Closures  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis1_band_openings.png' | relative_url }}" alt="Band Openings and Closures">

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- `40m` (the only band present): mean ≈ 1803 km, max ≈ 18,429 km, std ≈ 2408 km, n = 826.

**Interpretation from the dataset:**
- That mean is, oddly enough, almost identical to my home EFHW's own 40m mean distance from the 75-10m dataset (≈1764 km over 806 spots, captured across a full 3-hour evening) — a different antenna, location, and a 6x shorter capture window landing on nearly the same average.
- The standard deviation (2408 km) is larger than the mean itself (1803 km), which flags a strongly bimodal distribution: most contacts are short and regional, with a handful of outsized DX paths pulling both the mean and the max way up.
- A max of 18,429 km is close to the practical maximum distance achievable on Earth — essentially an antipodal-scale path. That matches what you'd expect from a low, near-vertical-incidence-skywave-leaning antenna: a strong regional lobe most of the time, with an occasional long-haul opening.


> Distance Profiling by Band  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis2_distance_profiling.png' | relative_url }}" alt="Distance Profiling by Band">

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- Top 20 receive grid prefixes (stations hearing KD3CCO):

| Rank | Grid | Count | Region |
|------|------|-------|--------|
| 1 | FM18 | 45 | Washington DC area |
| 2 | FN30 | 35 | New York City / Long Island |
| 3 | EN82 | 32 | Southeast Michigan |
| 4 | FM05 | 28 | Central North Carolina |
| 5 | DN70 | 21 | Colorado Front Range |
| 6 | FN21 | 19 | Northeastern Pennsylvania / Southern NY |
| 7 | FN31 | 16 | Hudson Valley NY / Western Connecticut |
| 7 | FM08 | 16 | Virginia / West Virginia |
| 7 | FN20 | 16 | Eastern Pennsylvania |
| 7 | FN42 | 16 | Eastern Massachusetts |
| 11 | EM38 | 14 | Central Missouri |
| 12 | EL98 | 13 | Central Florida |
| 13 | EM13 | 12 | North Texas / Southern Oklahoma |
| 13 | JN87 | 12 | Western Hungary |
| 15 | EN52 | 10 | Southern Wisconsin |
| 15 | EN80 | 10 | West-Central Ohio |
| 15 | FN13 | 10 | Upstate New York |
| 15 | DN31 | 10 | Northern Utah |
| 19 | EN58 | 9 | Far Northern Wisconsin |
| 20 | IL38 | 8 | Canary Islands / Western Sahara coast |

**Interpretation from the dataset:**
- This footprint is almost entirely a continental-scale regional one, covering the eastern half of North America with reach out to Colorado and Utah — exactly what a near-vertical-incidence-skywave-heavy 40m antenna should produce over a half-hour evening test.
- Only two grids in the top 20 are intercontinental: `JN87` (Western Hungary) and `IL38` (Canary Islands/Western Sahara coast), both consistent with the moderate-DX cluster visible in the SNR/distance scatter around 7,000–8,000 km.
- Notably absent from this top-20 list is the single most extreme contact in the dataset (Western Australia, 18,429 km) — it was strong and repeated, but with too few individual spots to crack the top 20 grid-count ranking. That underscores why Analysis 2's max/mean comparison is the better tool for catching this kind of outlier path.


> Geographical Footprint  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis3_geographical_spread.png' | relative_url }}" alt="Geographical Footprint">

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- The bulk of the 826 spots sit under 2,500 km, with SNR ranging from about +20 dB down to -30 dB — a wide spread for what is mostly regional/NVIS-style propagation.
- A second, visibly separated cluster sits around 5,500–8,000 km, including paths to `SV1BTL` (Greece, 8,183 km), `LU8MIL` (Argentina, 8,199 km, heard on 3 separate WSPR cycles), and `SP8MK` (Poland, 7,231 km).
- A small set of points beyond 18,000 km — all `VK6PVL` in Western Australia, 18,429 km — sit well past everything else on the plot. This path was decoded 5 separate times across the half-hour test (21:34, 21:38, 21:48, 21:52, and 21:56 UTC), so it was a real, sustained opening, not a single fluke decode.

**Interpretation from the dataset:**
- The overall downward trend is clear despite the short capture, and the regression line is pulled down by that one Australia outlier.
- The repeated VK6PVL decodes are the most notable result in this dataset: a 5 W, electrically very low, temporarily-deployed 40m dipole sustained a long-path opening to Australia for at least 22 minutes.
- The Argentina and European paths are a secondary group of moderate DX, while the bulk of the spots confirm the antenna is, as expected, primarily a strong regional performer at this height.


> SNR vs Distance Regression  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis4_snr_distance.png' | relative_url }}" alt="SNR vs Distance Regression">

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- Only 11 paired measurements were matched within a ±20 minute window — a much smaller sample than the 38 pairs in the 75-10m EFHW dataset, as expected from a 30-minute capture.
- Mean `SNR_delta` = +1.1 dB, median = +4 dB.
- 6 pairs were positive and 5 were negative — close to an even split.
- Largest deltas in either direction:
  - `KD2CLR` on 40m: +24 dB (TX stronger)
  - `N4JJS` on 40m: -21 dB (RX stronger)
  - `KB3EDF` on 40m: +16 dB (TX stronger)
  - `KA3SKN` on 40m: -16 dB (RX stronger)

**Interpretation from the dataset:**
- This is much closer to symmetric than my home EFHW's persistent +6.3 dB TX-favoring skew from the 75-10m dataset.
- That tracks with the deployment context: this antenna was tested out in an open field on a temporary mast, away from the house, rather than feedpoint-mounted a few inches off the siding the way my EFHW is. Less proximity to household electrical noise on receive would plausibly close that asymmetry gap.
- With only 11 pairs, this is suggestive rather than conclusive — a longer capture would be needed to confirm whether the near-zero skew holds up.


> TX vs RX Asymmetry  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis5_tx_rx_asymmetry.png' | relative_url }}" alt="TX vs RX Asymmetry">

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- This rigid V dipole is hand-steerable per the [portable mast build](/hamradio/articles/portable-mast-build/), and for this test it was oriented approximately north-to-south, which puts its broadside lobes pointing east and west.
- Azimuth of TX spots ranges from 5° to 331°, mean ≈ 181°, std ≈ 96°.
- Splitting spots into compass quadrants: 34.7% fall in the east sector (azimuth 20–160°) and 47.2% fall in the west sector (200–340°) — 81.9% combined. Only 2.6% fall in the narrow north sector (>340° or <20°) and 15.5% in the south sector (160–200°).
- The moderate-DX paths (Greece, Poland, ~45–55°) sit inside the east lobe, while the Argentina path (~172°) sits right at the edge of the south null and the Australia path (~304°) sits inside the west lobe.

**Interpretation from the dataset:**
- This lines up well with basic dipole theory: with the wire running roughly north-south, the antenna should radiate most strongly broadside to itself (east/west) and weakest off the ends (north/south) — and that's exactly the lopsided 81.9% vs. 18.1% split seen here.
- The Australia path, despite being the most extreme distance in the whole dataset, came in through the west lobe, not through some odd off-axis direction — consistent with it riding the antenna's actual main lobe rather than being a fluke through a null.
- The Argentina contact sitting near the south null is the one result that doesn't fit cleanly; that's more likely explained by a strong enough path on the night to punch through a weaker lobe than by the antenna pattern itself.
- Unlike my home EFHW, which has a single fixed, known wire azimuth, this V is hand-steered and could be re-oriented for a future test — repeating this capture with the V turned 90° (east-west wire, lobes north-south) would be a good way to confirm this pattern is really coming from the antenna and not just the night's propagation.


> Azimuthal Pattern Mapping  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis6_azimuthal_pattern.png' | relative_url }}" alt="Azimuthal Pattern Mapping">

---

### Analysis 7: Band-by-Band Efficiency Normalization

This analysis compares `k/W` across bands for stations that heard KD3CCO on 3 or more bands, to normalize path reach by transmitted power and compare relative efficiency across frequencies.

**Skipped for this dataset:** it requires remote stations heard on 3 or more distinct bands, and this capture has only one band present (40m), so there's no cross-band comparison to make. This antenna is purpose-built for 40m only, so this analysis would only become meaningful if the same station were tested across several bands in one capture.

---

### Analysis 8: Take-Off Angle Inference via Minimum Skip Boundaries

This analysis examines the shortest paths on the higher bands, which informs the likely takeoff angle and near-skip zone.

**Skipped for this dataset:** it only looks at the higher bands (20m, 17m, 15m, 12m, 10m), none of which are present in a 40m-only dataset. This isn't a gap in the antenna's performance, just outside this analysis's scope here — for what it's worth, the [Mast Height vs. Wavelength discussion](/hamradio/articles/portable-mast-build/#mast-height-vs-wavelength-nvis-or-dx) in the mast build article already predicts this antenna sits at roughly 0.22λ on 40m, solidly in NVIS territory, which lines up with the regional-heavy, occasionally-DX-punctuated pattern seen in Analyses 2 and 4 above.

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
- The per-band maps color each path's great-circle line by the required power (jet colormap); paths that can't meet the SSB threshold within the configured maximum power are shown in gray and drawn beneath the others so the most favorable (lowest-power) paths stand out on top.

**Possible conclusions:**
- A high fraction of gray paths on a band suggests SSB is impractical there at the current power level.
- Clusters of low-power (favorable) paths point to directions/bands where an SSB QSO is comfortably within reach.
- Bands where most spots already clear the threshold at low power are good candidates to actually attempt an SSB contact.

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`** (3 dB minimum margin, 100 W maximum radio power):
- 40m is the only band present, and it has a phone allocation, so nothing is excluded here. Of 826 spots, 515 (62.3%) could plausibly support an SSB QSO within 100 W.
- Median required power across all spots: ≈39.7 W.
- All of KD3CCO's own WSPR transmissions in this capture ran at a fixed 5 W.

**Interpretation from the dataset:**
- This pass rate (62.3%) is noticeably better than the 75-10m EFHW's own 40m figure from the other dataset (55.1% at a median 79.4 W) — consistent with this capture being even more weighted toward short, high-SNR regional contacts.
- A would-be SSB contact on this antenna is realistic at modest power for the majority of this capture's paths, which is a good sign for actually working stations on phone with this antenna in the field, not just logging WSPR beacons.

> 40m — SSB QSO Feasibility Map  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis9_ssb_qso_40m_screenshot.png' | relative_url }}" alt="40m SSB QSO Feasibility Map">  
[Open interactive 40m map]({{ '/assets/40m_loaded_dipole_ssb_qso_40m.html' | relative_url }}){:target="_blank"}

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

**Actual results for `40m_loaded_dipole_30ft_mast_spots.tsv`:**
- An interactive HTML map is saved alongside this article's assets.
- Since only 40m is present, the map's band filter has just one option, but the `heard` vs `heard_by` role filter still separates KD3CCO's TX and RX paths.
- The broad North American fan is immediately visible, along with the small number of long lines reaching into Europe, South America, and the single line stretching to Western Australia.

**Interpretation:**
- The map confirms the same pattern shown statistically in Analyses 2–4: a wide regional base with a few standout long-haul paths layered on top.

[Link to Interactive Map]({{ '/assets/40m_loaded_dipole_spots_map.html' | relative_url }}){:target="_blank"}

> Screenshot of Interactive Map  
<img src="{{ '/assets/images/40m_center_loaded_dipole_wspr_analysis/analysis10_spots_map_screenshot.png' | relative_url }}" alt="Screenshot of Interactive Map">

---

## 2. How to run and reproduce

Open `wspr_7510_analysis.ipynb` in Jupyter, change `TSV_FILENAME` in the configuration cell to `40m_loaded_dipole_30ft_mast_spots.tsv`, and execute all cells in order. `CALLSIGN` stays `KD3CCO` since that's the station that ran the WSPR session during this test.

Dependencies:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `folium`
- `geopy`

The notebook reads the TSV, builds derived fields, runs ten analyses, and displays the results while saving the key images and interactive maps. Analysis 9 (SSB QSO feasibility) and Analysis 10 (interactive path map) both use the helper module `wspr_folium_map.py` to generate their maps.

Analyses 1, 2, 4, and 8 adapt automatically to however many bands are present in a dataset. Analysis 7 specifically requires stations heard on 3 or more distinct bands, and Analysis 8 only looks at bands above 20m — both skip themselves as designed on this single-band, 40m-only capture.

---

## 3. Conclusions from this dataset

1. **The most notable result is a sustained, repeated opening to Western Australia (18,429 km) on a 5 W, electrically very low, temporarily-deployed 40m dipole.** `VK6PVL` was decoded 5 separate times across the 30-minute test, so this wasn't a fluke — it was a real long-path opening that this antenna and this short test session happened to catch.
2. **The bulk of the capture is dominated by short, regional, high-SNR contacts**, with a mean distance (1,803 km) that's nearly identical to my home EFHW's own 40m mean from a completely different antenna, location, and a 3-hour-longer capture window. This lines up with the [Mast Height vs. Wavelength analysis](/hamradio/articles/portable-mast-build/#mast-height-vs-wavelength-nvis-or-dx) predicting this antenna sits around 0.22λ up on 40m, solidly in NVIS-favoring territory.
3. **TX/RX asymmetry was close to neutral here** (+1.1 dB mean, nearly an even split of positive/negative pairs), in contrast to the home EFHW's persistent +6.3 dB TX-favoring skew — plausibly because this test happened in an open field away from household electrical noise, though the sample size (11 pairs) is small.
4. **SSB is realistically achievable for most of this capture's paths** — 62.3% clear a 3 dB margin within 100 W, at a median requirement of just ~40 W — a better showing than the home EFHW's 40m figure, likely because this capture skews even more regional.
5. **The azimuthal pattern matches basic dipole theory.** With the V oriented roughly north-south, 81.9% of spots fell in the broadside east/west sectors versus only 18.1% off the ends — including the Australia DX path, which arrived through the west lobe rather than some odd off-axis direction.
6. **This was a short, single-band, proof-of-concept capture**, not a multi-hour propagation study. It's enough to confirm the antenna and mast both work, catch one notable DX opening, and see a believable dipole lobe pattern, but a longer capture — and ideally a repeat with the V rotated 90° — would be needed to properly characterize this antenna's day-to-day behavior and confirm the lobe pattern isn't just coincidental to this one night's propagation.
