# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (fourth report)  
**Experiment:** Spiral-associated dots on pages 20–23 — multi-scale LoG / DoG blob detection  
**Previous reports:**  
- [2026-10-09_experiment_C_signatures.md](./2026-10-09_experiment_C_signatures.md)  
- [2026-10-09_rigid_fits.md](./2026-10-09_rigid_fits.md)  
- [2026-10-09_spiral_matched_filter.md](./2026-10-09_spiral_matched_filter.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Continue the attempt to extract the spiral-associated dots on pages 20–23 using multi-scale blob detection (Laplacian of Gaussian / Difference of Gaussian), after circular matched filtering proved inconclusive.

---

## 2. Method

- Images inverted so dark ink features become bright.
- Multi-scale DoG and scale-normalized LoG computed with σ ranging from ~1.2 to 5.0.
- Local-maximum suppression (min distance ≈ 18–22 px).
- Post-filtering requiring:
  - Near-black local minimum (≤ 30),
  - Low-to-moderate local mean intensity,
  - Response above a relative threshold.
- Applied to left and right spiral regions; consistency checked across pages 20, 21 and 22.

Implementation: pure SciPy / NumPy (no scikit-image dependency).

---

## 3. Key Results

### 3.1 Extreme cross-page consistency

The strongest small-scale dark-blob responses are **pixel-identical (or extremely close) across pages 20, 21 and 22**:

| Rank | Approx. location (Left) | Appears on |
|------|-------------------------|------------|
| 1    | (248, 1061)             | 20, 21, 22 |
| 2    | (264–265, 1072–1074)    | 20, 21, 22 |
| 3    | (247, 1083–1089)        | 20, 21, 22 |
| 4    | (233, 1661)             | 20, 21, 22 |
| …    | further candidates also match | 20, 21, 22 |

Right-side responses are the expected horizontal mirrors of the left-side set.

This is the same pattern previously observed for the plant + dot assets on pages 57/68: **the spiral ornamentation itself is a reused graphic element**, not independently drawn on each page.

### 3.2 Candidate volume vs claimed count

Even after intensity filtering, each side still yields >100 candidates. The strongest responses cluster in two vertical bands (roughly y ≈ 1060–1090 and y ≈ 1640–1690), which likely correspond to particular turns or terminations of the spiral arms.

No automatic criterion cleanly isolates a unique set of exactly four dots per side that matches the CSV description (“3 outside 2nd spiral + 1 inside 3rd spiral”).

### 3.3 Comparison with earlier detection methods

| Method                        | Outcome |
|-------------------------------|---------|
| Global / regional thresholding | Too few isolated components |
| Circular matched filter       | Peaks dominated by spiral-arm features |
| Multi-scale LoG / DoG         | Many consistent dark blobs; still no unique 8-dot set |

All three approaches converge on the same conclusion: the spiral “dots” are not large, high-contrast, isolated circular marks of the kind measured on pages 24/40/73.

---

## 4. Interpretation

1. **Asset reuse is confirmed** for the spiral ornaments on pages 20–22 (and almost certainly 23). This is now a repeated design pattern in *Liber Primus* (spirals 20–23, plant clusters 57/68).

2. **Coordinate extraction of a discrete 8-dot constellation remains unresolved.** The claimed dots appear to be local features of continuous spiral line work rather than separate marks that blob detectors can uniquely identify.

3. Because the geometry is reused, any future successful extraction on one page can be transferred to the other pages with high confidence.

---

## 5. Recommended Next Actions

1. **Manual seeding** remains the most reliable path: visual identification of the four intended dots per side on one annotated page, followed by local centroid refinement and transfer to the other pages.
2. Alternatively, skeletonize the spiral and extract endpoints / high-curvature points, then test whether a stable subset of four per side emerges.
3. Until discrete coordinates are obtained, keep the spiral groups in the inventory as `ANNOTATED_ONLY / positions unresolved` and do not include them in geometric matching against the primary five-dot template.

---

## 6. Relation to the Primary Investigation

The isolated five-dot template (24/40/73) and the plant-side clusters continue to stand as the only fully verified, high-precision point sets. The spiral pages have added strong evidence of systematic graphic-asset reuse but have not yet contributed new testable coordinates.

---

*Negative and partial results are reported with the same detail as positive ones so the investigation remains reproducible and does not silently drop difficult cases.*
