# Liber Primus Visual Geometry Investigation — Research Record v1.7

**Date:** 2026-10-10  
**Master workbook:** `liber_primus_visual_master_dataset_v1_7.xlsx`  
**Previous record:** `LIBER_PRIMUS_VISUAL_GEOMETRY_RESEARCH_v1_6.md` remains unchanged.  
**New workbook sheet:** `Threshold Match v1.7`  
**Original source JPEG bytes downloaded and reprocessed in this pass:** No.

## 1. What changed in v1.7

The v1.7 workbook preserves the prior v1.6 sheets and adds a threshold-robustness audit. It reuses stored rows from `Pixel Thresholds v1.1` at gray thresholds 40, 60, 80, and 100. For each of the three page pairs, v1.7 holds the previously selected point mapping fixed and fits a simpler transform with no free scale or rotation:

- **24 → 40:** vertical reflection plus translation, `x40 = x24 + dx`, `y40 = C − y24`.
- **24 → 73:** horizontal reflection plus translation, `x73 = Kx − x24`, `y73 = y24 + dy`.
- **40 → 73:** 180-degree rotation plus translation, `x73 = Kx − x40`, `y73 = Ky − y40`.

The constants are re-estimated by least squares separately at each threshold. Point mapping and model families come from prior exploratory work; they were not independently selected or preregistered in v1.7. The analysis is therefore a robustness check, not a confirmatory test.

## 2. Results

### Page 24 → page 40

| Gray threshold | RMS residual (px) | Maximum residual (px) | Equal component areas | Equal bbox dimensions | Mean absolute area delta (px²) |
|---:|---:|---:|---:|---:|---:|
| 40 | 0.060901 | 0.097696 | 2/5 | 4/5 | 7.60 |
| 60 | 0.036802 | 0.073604 | 4/5 | 4/5 | 1.80 |
| 80 | 0.036802 | 0.073604 | 4/5 | 4/5 | 1.80 |
| 100 | 0.047069 | 0.067875 | 0/5 | 4/5 | 9.80 |

The fixed vertical-reflection model stays below 0.10 px maximum centroid residual at every stored threshold. At T=60 and T=80, four of five mapped components have identical stored areas and four of five have identical bounding-box dimensions. The recurring discrepancy is one component whose T=60/T=80 area differs by 9 px² and whose bounding-box height differs by one pixel. At T=100, segmentation areas change enough that none of the five areas are exactly equal, although the recorded bbox dimensions still match for four of five.

This is consistent with a shared or reused geometric template and is the strongest pairwise match in this audit. It does not show whether the original dot-mask pixels are identical after reflection and translation.

### Page 24 → page 73

| Gray threshold | RMS residual (px) | Maximum residual (px) | Equal component areas | Equal bbox dimensions |
|---:|---:|---:|---:|---:|
| 40 | 0.243089 | 0.345707 | 0/5 | 2/5 |
| 60 | 0.245999 | 0.315574 | 0/5 | 2/5 |
| 80 | 0.245999 | 0.315574 | 0/5 | 2/5 |
| 100 | 0.223387 | 0.303115 | 0/5 | 2/5 |

### Page 40 → page 73

| Gray threshold | RMS residual (px) | Maximum residual (px) | Equal component areas | Equal bbox dimensions |
|---:|---:|---:|---:|---:|
| 40 | 0.274411 | 0.408778 | 0/5 | 3/5 |
| 60 | 0.263280 | 0.346166 | 0/5 | 3/5 |
| 80 | 0.263280 | 0.346166 | 0/5 | 3/5 |
| 100 | 0.230827 | 0.299019 | 0/5 | 3/5 |

Both pairs involving page 73 preserve a broadly similar geometry under the inherited mapping, but their restricted-transform residuals are larger than for 24 → 40. None of the mapped areas are exactly equal across these pairs at any tested threshold. The stored measurements therefore support a descriptive hierarchy: **24/40 is the strongest near-copy candidate; page 73 is a looser geometric match.**

The smaller residuals at T=100 for page 73 do not imply that T=100 is a better detector. Threshold-dependent segmentation changes component areas, and the mappings were already selected from the same five-point groups.

## 3. Evidence classification

**Newly computed in v1.7:** fixed-transform constants, per-point residuals, summary RMS/max residuals, exact stored area-equality counts, exact stored bbox-dimension-equality counts, and mean absolute area deltas at each threshold. These computations were independently reproduced from the workbook records by `analyze_liber_primus_threshold_match_v1_7.py`.

**Inherited rather than independently measured:** centroid coordinates, component areas, bounding boxes, threshold labels, point identities, correspondence mappings, and source Git blob IDs. The rows originate from `Pixel Thresholds v1.1` and previous exploratory measurements.

**Still not performed:** obtaining exact original JPEG bytes into the current runtime, calculating their hashes locally, independently decoding the images, independently re-extracting components, comparing transformed pixel masks, or rechecking the page 57/68 plant ornaments.

The latest acquisition attempts remain blocked by network name resolution (`Temporary failure in name resolution`). GitHub directory metadata and the manifest can corroborate recorded object identifiers, but cannot replace local byte-level validation.

## 4. What the evidence supports—and does not support

The most economical interpretation of the page 24/40 relationship is repeated or mirrored artwork/layout, pending a direct crop comparison. The v1.7 result strengthens the *descriptive robustness* of this geometric observation because the fixed-transform match remains tight when the recorded segmentation threshold changes.

No manuscript-specific p-value or defensible null distribution has been established. The point correspondences and target groups were selected during prior exploration; the test has not accounted for manuscript-wide motif selection, repeated artwork, detector behavior, or the complete family of transformations and pages examined. The page 39 control and page 68 cluster remain descriptive controls only. The historical rectangular random-point simulation is not used as inferential evidence.

Most importantly, geometric repetition alone does not establish encoding. No mapping from the measured features to rune values, plaintext, reading order, page indices, or key material was tested or supported. This remains separate from the keystream-source investigation.

## 5. Next concrete experiment

The next decisive step remains acquisition of locally usable source bytes for pages 24, 40, 57, 68, and 73. Run the existing `acquire_verify_liber_primus_sources_v1_6.py` in a network-enabled environment, then provide the verified images and acquisition audit. With byte identity established, the next test should:

1. Reproduce the existing threshold-60 component masks and centroids independently.
2. Apply the fixed page 24 → 40 vertical reflection/translation, then compare the two actual image crops with pixelwise absolute-difference and overlap metrics.
3. Repeat at thresholds 40, 60, 80, and 100 using the same preprocessing.
4. Inspect all detected and rejected components and then run the same frozen procedure on the page 57/68 plant-ornament comparison.

If the dot masks are repeated artwork, that would explain the geometric match without requiring a cipher hypothesis. If they are not, the differences can be measured and used to define a subsequent falsifiable experiment. The current evidence is not sufficient to choose between those possibilities.
