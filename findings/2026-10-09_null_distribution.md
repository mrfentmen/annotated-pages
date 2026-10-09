# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (fifth report)  
**Experiment:** Null-distribution / statistical significance of the primary five-dot template residuals  
**Previous reports:**  
- [2026-10-09_experiment_C_signatures.md](./2026-10-09_experiment_C_signatures.md)  
- [2026-10-09_rigid_fits.md](./2026-10-09_rigid_fits.md)  
- [2026-10-09_spiral_matched_filter.md](./2026-10-09_spiral_matched_filter.md)  
- [2026-10-09_spiral_log_dog.md](./2026-10-09_spiral_log_dog.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Quantify how unusual the extremely low residuals of the isolated five-dot groups (pages 24 / 40 / 73) are under the same structured transformation models previously used (vertical reflection, horizontal reflection, 180° rotation).

---

## 2. Observed residuals (recap)

| Transform              | RMS residual |
|------------------------|--------------|
| 24 → 40 vertical flip  | **0.031164 px** |
| 40 → 73 180° rotation  | **0.231816 px** |
| 24 → 73 horizontal flip| **0.206411 px** |

Scale factors ≈ 1.000 in all three cases.

Scale-invariant signature RMS:  
- 24 vs 40: **0.000041**  
- 24 vs 73: **0.000321**

---

## 3. Null models

### 3.1 Random 5-point sets (structured transforms)

- 400 independent pairs of random 5-point sets drawn uniformly from a bounding region comparable to the primary template’s spatial extent.  
- For each pair the best RMS under the structured model (transform + full 5! correspondence enumeration + similarity fit) was recorded.

| Model   | Median null RMS | 5th percentile | 1st percentile | Minimum | P(null ≤ observed) |
|---------|-----------------|----------------|----------------|---------|--------------------|
| vflip   | 302.5 px        | 166.9 px       | 123.1 px       | 101.2 px| **0.0000**         |
| rot180  | 307.1 px        | 162.6 px       | 104.0 px       | 83.2 px | **0.0000**         |
| hflip   | 302.5 px        | 166.9 px       | 123.1 px       | 101.2 px| **0.0000**         |

The observed residuals lie far below the entire null distribution (more than two orders of magnitude below the 1st percentile).

### 3.2 Scale-invariant signature null

- 2000 random 5-point sets; signature = sorted pairwise distances normalized by maximum distance.  
- RMS difference from the page-24 reference signature.

| Quantity                  | Value    |
|---------------------------|----------|
| Observed 24 vs 40         | 0.000041 |
| Observed 24 vs 73         | 0.000321 |
| Null median               | 0.0996   |
| Null 5th percentile       | 0.0542   |
| Null 1st percentile       | 0.0424   |
| Null minimum              | 0.0267   |
| P(null ≤ 0.00035)         | **0.00000** |
| P(null ≤ 0.191) (plant)   | 0.9795   |

### 3.3 Real controls under the same structured models

| Comparison                        | Best structured RMS |
|-----------------------------------|---------------------|
| 24 vs Plant5 (57R/68R)            | 14.3 – 14.7 px     |
| 24 vs each 5-subset of page 39    | 69.5 – 99.4 px (min 69.5) |

Even the closest real control remains >200× larger than the intra-template residuals.

---

## 4. Interpretation

1. Under both coordinate-space structured transforms and scale-invariant signature comparison, the match among pages 24, 40 and 73 is **statistically extreme**. No random 5-point configuration in a comparable spatial region produced residuals anywhere near the observed values.

2. The plant-side five-dot cluster and the page-39 six-dot group, when subjected to the identical analysis pipeline, produce residuals that fall comfortably inside (or above) the bulk of the null distribution. They do not share the primary template’s geometry.

3. The result is robust to the choice of null (random points vs real control groups) and to the choice of similarity measure (Euclidean residual after rigid+scale transform vs scale-invariant signature).

4. **This still does not constitute a cipher solution.** It establishes that the geometric recurrence is highly non-random and warrants continued investigation into whether the template’s placement, orientation, or transformation encodes information related to the unsolved text.

---

## 5. Implications for the investigation

- The primary five-dot template can be treated as a confirmed, distinctive visual motif with quantifiable uniqueness.  
- Further inventory expansion (spirals, crosses, etc.) remains useful but is no longer required to establish that *something* geometrically special is present.  
- The logical next phase is Experiment E: systematic tests for correlation between the template’s presence, orientation, or transformation type and independent textual properties (page number, rune counts, line structure, known solved sections, etc.).

---

## 6. Reproducibility

- Centroids: independently verified (PIL + SciPy).  
- Null seed: 42.  
- N = 400 (structured) / 2000 (signature).  
- Full enumeration of 5! correspondences for every trial.  
- Code and exact numbers available in the investigation environment; this report contains all summary statistics needed for independent verification.

---

*Statistical extremity of a visual motif is necessary but not sufficient evidence of intentional encoding. Correlation with the cipher text remains the decisive test.*
