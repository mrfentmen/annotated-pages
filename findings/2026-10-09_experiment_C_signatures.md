# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09  
**Experiment:** C (Geometric Signature Matching) + completion of A/B validation  
**Workbook:** `liber_primus_visual_master_dataset_v0_10.xlsx`  
**Repository:** mrfentmen/annotated-pages

---

## 1. Summary of Status

All previously reported centroids for the core groups have been **independently reproduced** using a standard library pipeline (PIL grayscale + SciPy connected-component / center-of-mass). No reliance remains on the earlier custom JPEG decoder.

**10 groups now fully verified:**

| Group ID       | Page | Type                              | Dots | Status   |
|----------------|------|-----------------------------------|------|----------|
| G-5DOT-24      | 24   | Isolated five-dot constellation   | 5    | VERIFIED |
| G-5DOT-40      | 40   | Isolated five-dot constellation   | 5    | VERIFIED |
| G-5DOT-73      | 73   | Isolated five-dot constellation   | 5    | VERIFIED |
| G-3DOT-50      | 50   | Three-dot horizontal row          | 3    | VERIFIED |
| G-3DOT-56      | 56   | Three-dot horizontal row          | 3    | VERIFIED |
| G-PLANT5-57R   | 57   | Right plant-adjacent 5-dot        | 5    | VERIFIED |
| G-PLANT5-68R   | 68   | Right plant-adjacent 5-dot        | 5    | VERIFIED |
| G-PLANT3-57L   | 57   | Left plant-adjacent 3-dot         | 3    | VERIFIED |
| G-PLANT3-68L   | 68   | Left plant-adjacent 3-dot         | 3    | VERIFIED |
| G-6DOT-39      | 39   | Six-dot cluster (negative control)| 6    | VERIFIED |

---

## 2. Key Geometric Findings (Experiment C)

### 2.1 Scale-invariant sorted pairwise-distance signatures

Signatures are the sorted vector of all pairwise Euclidean distances, divided by the maximum distance in the group (scale-invariant).

**Primary isolated 5-dot template (pages 24 / 40 / 73):**

```
[0.2631, 0.2732, 0.3207, 0.4244, 0.5700, 0.6514, 0.7392, 0.7766, 0.9106, 1.0000]
```

RMS differences among the three instances:
- 24 vs 40: **0.000041**
- 24 vs 73: **0.000321**
- 40 vs 73: **0.000349**

These are consistent with a single geometric template under rigid transformations (reflection / 180° rotation) plus sub-pixel measurement noise.

**Ornamental plant-side 5-dot cluster (57R / 68R):**

```
[0.5280, 0.5523, 0.5527, 0.6158, 0.6767, 0.8793, 0.9205, 0.9411, 0.9762, 1.0000]
```

RMS vs primary template: **≈ 0.1913** (clearly distinct).

**Three-dot horizontal rows (50 / 56):**

```
[0.4662, 0.5338, 1.0000]   (page 50)
[0.4661, 0.5339, 1.0000]   (page 56)
```

RMS between them: **0.000093**. End-to-end span ratio ≈ 2.130×.

**Left plant 3-dot (57L / 68L):**

```
[0.5408, 0.9007, 1.0000]
```

RMS vs the 50/56 three-dot motif: ≈ 0.216 (distinct).

### 2.2 Page 39 six-dot negative control

All six possible 5-point subsets were tested against the primary template signature.

| Subset indices | RMS vs G-5DOT-24 |
|----------------|------------------|
| (0,1,2,3,5)    | **0.105133** (best) |
| (0,1,2,3,4)    | 0.108252 |
| (0,1,2,4,5)    | 0.117572 |
| (0,2,3,4,5)    | 0.120334 |
| (1,2,3,4,5)    | 0.127046 |
| (0,1,3,4,5)    | 0.195960 |

Even the closest 5-subset remains more than **300× farther** from the primary template than the intra-template differences (0.00004–0.00035).

### 2.3 Absolute scale comparison (max pairwise distance)

| Group              | Max pairwise distance |
|--------------------|-----------------------|
| Primary 5-dot      | ≈ 750 px             |
| 3-dot (page 50)    | ≈ 896 px             |
| 3-dot (page 56)    | ≈ 421 px             |
| Plant 5-dot        | ≈ 66 px              |
| Plant 3-dot        | ≈ 64 px              |
| Page 39 six-dot    | ≈ 641 px             |

The ornamental plant clusters are an order of magnitude smaller than the isolated template.

---

## 3. Interpretation (strictly observational)

1. **Multiple distinct recurring visual templates exist.**
   - Isolated large 5-dot constellation (24/40/73).
   - Horizontal 3-dot row at two scales (50/56).
   - Small ornamental plant-adjacent clusters (57/68 left 3-dot + right 5-dot).

2. **Pages 57 and 68 share identical pixel-level plant + dot assets** (both left and right clusters). This is strong evidence of a reused graphic element rather than independent drawing.

3. **The isolated 5-dot template is geometrically unusual** relative to the measured controls (ornamental clusters and the page-39 six-dot group). Intra-template RMS values are two to four orders of magnitude smaller than the best control matches.

4. **No cipher claim is made.** Geometric recurrence of a template is necessary but not sufficient evidence of information encoding. Correlation testing against textual features (Experiment E) has not yet been performed.

---

## 4. Source Integrity

Original scan Git blob SHA-1s (scream314/cicada3301):

| Page | SHA-1 |
|------|-------|
| 24   | `2b4e09dbad1a9c602a2919864b1a84f49d7ff501` |
| 39   | `0270e099f35a00dc24a9dc673ce13d4a0a843802` |
| 40   | `feee4eed2a4f6d66456ff5a977f43c7ef297f8eb` |
| 50   | `68d3e28d8c4161fdfe91a542f5bac8e276bc441e` |
| 56   | `819261c833837cbaa2bd200d210ca299d79031f3` |
| 57   | `83f661b6107587c5d153d6dea3f6bf03090a70bc` |
| 68   | `701e47789abf4401d61420ff938c2b72aa03ad2c` |
| 73   | `afa3428764199ddf590baf0c055c8caedc079cb1` |

All images 2400 × 3600. Measurement method: PIL `convert('L')` + SciPy `ndimage.label` / `center_of_mass` (closest or largest component to seed, threshold 60 primary).

---

## 5. Next Steps

1. Expand inventory to spiral-associated 8-dot aggregates on pages 20–23 and cross ornaments on 17–19 (coordinate extraction required).
2. Formal Procrustes / least-squares rigid + reflection fits with correspondence enumeration for all verified pairs.
3. Build a simple null distribution (random 5-point sets drawn from comparable page regions or shuffled controls) to quantify how unusual the 0.00004-level matches are.
4. Only after the above, begin testing for correlation with page number, rune counts, or other independent textual properties (Experiment E).

---

*This report was generated as part of the ongoing evidence-driven investigation. All coordinates and signatures are reproducible from the verified original scans and the methods described above.*
