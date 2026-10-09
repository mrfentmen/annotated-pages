# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (third report)  
**Experiment:** Spiral-associated dots on pages 20–23 — matched-filter detection attempt  
**Previous reports:**  
- [2026-10-09_experiment_C_signatures.md](./2026-10-09_experiment_C_signatures.md)  
- [2026-10-09_rigid_fits.md](./2026-10-09_rigid_fits.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Extract coordinates for the spiral-associated dots described in the source CSV for pages 20–23:

> “3 DOTS ON THE OUTSIDE 2ND SPIRAL OF THE PAGE AND 1 DOT ON THE INSIDE THE 3RD SPIRAL BOTH SIDES OF THE PAGE”

Total claimed: 8 dots per page (4 left + 4 right). These pages immediately precede the isolated five-dot constellation on page 24.

---

## 2. Data Retrieved

| Page | Original SHA-1 (scream314) | Annotated available |
|------|----------------------------|---------------------|
| 20   | `3a7badc18e859868ef28d5b8b81bfde38e0ebbde` | Yes |
| 21   | `9cc256b5356a9382713214324dbce89ba02b01b0` | Yes |
| 22   | `d80bf744990eb4263c2137fb3ba13dbe775c0fa5` | Yes |
| 23   | `f442a9333c78e39bef3f53487ca24dac0c7942de` | No |

All originals are 2400 × 3600.

---

## 3. Methods Attempted

1. **Simple thresholding + connected components**  
   Multiple thresholds (40–80), area filters (40–400 px), left/right margin ROIs.  
   Result: Very few isolated components recovered; most dark ink belongs to continuous spiral arms.

2. **Annotation-difference seeding**  
   Differenced annotated vs original page 20 to locate label marks, then searched locally for dark centroids.  
   Recovered a handful of small dark marks near labels, but not a consistent set of 8.

3. **Matched filtering (this report)**  
   - Circular dark-blob templates (radii ≈ 3–5 px, soft Gaussian edge).  
   - Inverted image so dark features produce positive correlation peaks.  
   - Normalized cross-correlation via `scipy.signal.correlate2d`.  
   - Local-maximum suppression (min distance 25–30 px).  
   - Applied separately to left and right spiral regions.

---

## 4. Matched-Filter Results (Page 20 representative)

Strongest peaks are highly left/right symmetric (expected for mirrored spiral designs). However, inspection of local intensity and spatial distribution indicates that the highest responses correspond primarily to:

- Dark terminations or high-curvature points on the spiral arms themselves, and  
- Occasional isolated ink blobs that may or may not be the “dots” referenced in the CSV.

No clean, reproducible set of 8 discrete, roughly circular dots analogous to the isolated five-dot template (pages 24/40/73) or the plant-side clusters was isolated.

Example top responses (radius≈4 template, page 20):

**Left region**  
- (439, 1150), (449, 1491), (269, 1683), …  

**Right region** (mirrored)  
- (1960, 1150), (1950, 1491), (2130, 1683), …  

These locations are consistent across template scales but do not form an obvious 3+1 per side configuration that can be confidently labeled without visual ground truth.

---

## 5. Interpretation & Limitation

- The spiral “dots” appear to be stylistically different from the large, high-contrast, isolated circular marks measured earlier.  
- They are either integrated into the continuous spiral line work or are low-contrast / small enough that circular matched filters do not cleanly separate them from the surrounding ornament.  
- Automatic extraction of a reliable 8-point coordinate set for pages 20–23 is **not yet achieved**.

This is a negative but informative result: the spiral-associated marks do not behave like the primary five-dot template under the same detection pipeline.

---

## 6. Recommended Follow-up

1. Manual seeding from high-resolution visual inspection of the annotated images (or user-provided approximate locations) followed by local centroid refinement.  
2. Alternative detectors: ridge/endpoint detection on the spiral skeleton, or multi-scale blob detection (LoG / DoG) tuned to the expected dot diameter.  
3. If coordinates remain elusive, retain the groups in the inventory as `ANNOTATED_ONLY / positions unresolved` and do not force a geometric comparison with the primary template.

---

## 7. Relation to Prior Work

The isolated five-dot template (24/40/73) and the plant-side clusters remain cleanly measured and geometrically distinct. The spiral pages have not yet added new verified point sets that can be tested against those templates.

---

*This report records a negative detection result with full method detail so that the limitation is transparent and future attempts can build on it.*
