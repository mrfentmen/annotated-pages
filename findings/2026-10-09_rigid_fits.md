# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (second report)  
**Experiment:** C continued — Formal rigid / reflection / 180° fits with correspondence enumeration  
**Previous report:** [findings/2026-10-09_experiment_C_signatures.md](./2026-10-09_experiment_C_signatures.md)  
**Workbook:** `liber_primus_visual_master_dataset_v0_10.xlsx`  
**Repository:** mrfentmen/annotated-pages

---

## 1. Purpose

The previous report established that the scale-invariant pairwise-distance signatures of the three isolated five-dot groups (pages 24, 40, 73) are essentially identical (RMS 0.00004–0.00035). This report tests explicit geometric transformation models and recovers the best point correspondences.

---

## 2. Method

- Similarity transform (uniform scale + rotation + translation) estimated via the Umeyama / Kabsch procedure.
- Full enumeration of the 5! = 120 possible point correspondences for each pair.
- Structured models tested in addition to free similarity:
  - Vertical reflection about the group centroid
  - Horizontal reflection about the group centroid
  - 180° rotation about the group centroid
- After applying the structured transform, the best residual correspondence is found by enumeration and a final similarity is fit (allowing residual scale/rotation/translation).

All coordinates are the independently verified centroids from the PIL + SciPy pipeline (source 2400 × 3600 pixels).

---

## 3. Results — Primary five-dot template

### 3.1 Structured models (best correspondence after transform)

| Transform model              | RMS residual | Scale   | Residual angle | Best correspondence (0-based) |
|------------------------------|--------------|---------|----------------|-------------------------------|
| 24 → 40 via **vertical flip**    | **0.031164 px** | 1.000021 | 0.0035°     | (0, 1, 4, 3, 2)               |
| 40 → 73 via **180° rotation**    | **0.231816 px** | 1.000410 | 0.0015°     | (2, 3, 4, 0, 1)               |
| 24 → 73 via **horizontal flip**  | **0.206411 px** | 1.000431 | 0.0049°     | (4, 3, 2, 0, 1)               |

### 3.2 Free similarity (no forced reflection/rotation)

| Pair     | Best free RMS | Notes |
|----------|---------------|-------|
| 24 → 40  | 95.50 px      | Falls into a poor local correspondence; the reflection structure is required for the tight fit |
| 40 → 73  | 0.232 px      | Recovers the same 180° solution |
| 24 → 73  | 95.57 px      | Same issue as 24→40; structured horizontal flip is needed |

**Interpretation:** The three instances are related by simple orientation-reversing or 180° transformations with scale factor indistinguishable from 1.0 and residuals at or below the level of centroid measurement uncertainty (~0.03–0.23 px). The free similarity search without the reflection constraint does not reliably find these solutions because many correspondences produce higher residuals.

### 3.3 Recovered point mappings (structured models)

Using the best permutations above and the original physical labels:

- **24 → 40 (vertical reflection)**  
  lower-left ↔ upper-left  
  bottom ↔ upper-middle  
  upper-middle ↔ lower-left  
  upper-right ↔ lower-right  
  lower-right ↔ upper-right  

- **40 → 73 (180° rotation)**  
  Corresponds to the permutation (2, 3, 4, 0, 1) on the ordered lists used in measurement.

These mappings are consistent with the exploratory correspondences noted in earlier work, now placed on a fully enumerated and residual-quantified footing.

---

## 4. Comparison with ornamental plant-side cluster

A free similarity fit of the primary template (page 24) to the plant-side five-dot cluster (57R) yields:

- RMS ≈ 10.4 px  
- Scale ≈ 0.096 (the plant marks are ~10× smaller)  

Even after optimal correspondence and scale, the residual remains two orders of magnitude larger than the intra-template structured fits. This reinforces that the ornamental cluster is a different geometric motif.

---

## 5. Conclusions from this block

1. The isolated five-dot groups on pages 24, 40 and 73 form a single geometric template related by:
   - vertical reflection (24 ↔ 40),
   - 180° rotation (40 ↔ 73),
   - horizontal reflection (24 ↔ 73),
   with scale factor = 1 and residuals ≤ 0.23 px.

2. Full correspondence enumeration confirms that the extremely low residuals are not an artefact of a lucky fixed ordering; the best permutation under the structured models is uniquely strong.

3. The plant-side five-dot clusters remain geometrically and metrically distinct.

4. No claim is made that these transformations encode cipher instructions. They establish a clean, reproducible geometric relationship that any later cipher hypothesis must either exploit or explain as decorative reuse.

---

## 6. Source & Reproducibility

- Centroids: independently verified (see previous report and workbook `Measured Centroids` / `Contextual Controls` sheets).
- Code: Umeyama similarity + exhaustive permutation search (Python / NumPy).
- Original image SHA-1s unchanged from previous report.

---

## 7. Immediate next work

1. Begin coordinate extraction for the spiral-associated dot groups on pages 20–23 (the sequence that culminates in the page-24 five-dot).
2. Add a minimal null distribution (random 5-point sets or shuffled controls) to quantify the rarity of RMS < 0.25 px under the structured models.
3. Update the master workbook with a new “Rigid Fits” sheet containing the transformation parameters and correspondence tables.

---

*Report generated as part of the ongoing evidence-driven investigation. All numbers are reproducible from the verified centroids and the method described above.*
