# Liber Primus Visual Geometry Investigation — Research Record v1.2

**Date:** 2026-10-10  
**Input master:** `liber_primus_visual_master_dataset_v1_1.xlsx`  
**Output master:** `liber_primus_visual_master_dataset_v1_2.xlsx`  
**Status:** Reproduced arithmetic on inherited measurements; source-pixel decoder validation, corpus-wide search, empirical null and cipher linkage remain open.

## Executive result

The existing v1.1 workbook and `measure_constellations_v0_2.py` were recovered from the Library. v1.1 was imported, its prior sheets were retained, and ten audit/result sheets were appended. All new geometric calculations below were recomputed from the 15 stored threshold-60 centroids in `Pixel Centroids v1.1`; they are therefore independent mathematical refits of the recorded coordinates, **not fresh image extractions**.

The best similarity-transform refits after trying all 120 target point permutations in each of two determinant classes give:

| Pair | Best model | Source→target label mapping | Scale | RMS error (source px) | Max error (source px) | RMS / source-group RMS pair distance |
|---|---|---|---:|---:|---:|---:|
| 24 → 40 | Reflection | 1→1; 2→2; 3→5; 4→4; 5→3 | 1.000020902 | 0.031138 | 0.052693 | 0.00006444 |
| 24 → 73 | Reflection | 1→4; 2→5; 3→3; 4→2; 5→1 | 1.000431004 | 0.206429 | 0.288245 | 0.00042719 |
| 40 → 73 | Proper rotation | 1→4; 2→5; 3→1; 4→2; 5→3 | 1.000410028 | 0.231805 | 0.339007 | 0.00047970 |

Here “proper” means determinant +1 (rotation, no reflection); “reflected” means determinant −1. A similarity transform includes rotation/reflection, uniform scale and translation. The mapping is the best **in-sample** mapping after permutation search, so residuals are descriptively useful but optimistically selected. There are 3 pairs × 2 model classes × 120 correspondence permutations = 720 pilot similarity fits. This is not a p-value and does not account for the broader exploratory search that selected these motifs.

## Artifact access and provenance

Recovered locally:

- `liber_primus_visual_master_dataset_v1_1.xlsx` (133,600 bytes; SHA-256 `e2998d9d646839556f11e80c6dd5eba2c33c63f09cc571fead936b77390e3841`)
- `measure_constellations_v0_2.py`
- `cicadadataset.csv`
- `LIBER_PRIMUS_VISUAL_GEOMETRY_INVESTIGATION_HANDOFF(1).md`
- `Liber_Primus_Art_Survey_18-74.txt`

The v1.1 workbook contains its 19 expected original sheets and these ten v1.2 append-only sheets: Workbook Audit, Geometry Refit, Cluster Signatures, Threshold Sensitivity, Auxiliary Controls, Null Distribution, Decoder Crosscheck, Experiment Log, Coverage Audit, and Cipher Correlation.

Current public GitHub blob IDs were retrieved through the GitHub connector on 2026-10-10 for pages 24, 39, 40, 50, 56, 57, 68 and 73. They match the recorded v1.1 IDs **8/8**. This verifies the source repository object identities against the workbook records. It does not substitute for reading and independently decoding the JPEG bytes locally.

| Page | Current verified Git blob SHA-1 | Match to v1.1 |
|---:|---|---|
| 24 | `2b4e09dbad1a9c602a2919864b1a84f49d7ff501` | yes |
| 39 | `0270e099f35a00dc24a9dc673ce13d4a0a843802` | yes |
| 40 | `feee4eed2a4f6d66456ff5a977f43c7ef297f8eb` | yes |
| 50 | `68d3e28d8c4161fdfe91a542f5bac8e276bc441e` | yes |
| 56 | `819261c833837cbaa2bd200d210ca299d79031f3` | yes |
| 57 | `83f661b6107587c5d153d6dea3f6bf03090a70bc` | yes |
| 68 | `701e47789abf4401d61420ff938c2b72aa03ad2c` | yes |
| 73 | `afa3428764199ddf590baf0c055c8caedc079cb1` | yes |


## Workbook consistency checks

- The target centroid block contains **15 points** (five on each of pages 24, 40, 73). Page, group, point label, source Git blob ID, grayscale threshold, x/y coordinates, ROI and source URL are populated.
- All 15 normalized coordinates match `x / 2400` and `y / 3600` within a tolerance of `2e-5`. Bounding-box dimensions, containment within the recorded ROI and basic per-row required fields pass.
- The page dimensions (2400 × 3600), source-pixel coordinate space, top-left origin and y-down convention are workbook/sheet-level context rather than independently repeated in each centroid row. The v1.2 sheets make that convention explicit in their notes.
- The master data range contains 185 nonblank feature IDs and no duplicate feature ID within the declared range checked.
- The old `Measured Centroids` target block and v1.1 target centroid records differ by at most **0.000510 px** in Euclidean centroid position. That is consistent with stored precision. A page+label join is not safe across the entire legacy centroid sheet by itself; variants and controls can repeat those labels. Future joins should use page + group class + label + threshold + source hash.
- The handoff ROI form `[x, y, width, height]` matches the recorded ROIs. The available Python script's `PAGE_CONFIG` uses corner coordinates `[x0, y0, x1, y1]`, which is a different representation; the equivalent regions are consistent once converted.

## Reconciliation against the stored v1.1 transform-fit sheet

A finer audit found a small but real numerical non-reproduction when fitting from the numeric centroid cells currently stored in `Pixel Centroids v1.1`. The selected mappings and determinant classes are the same, but the best-model RMS residuals differ slightly from `Pixel Transform Fits v1.1`:

| Pair | Model | Stored v1.1 RMS (px) | Refit v1.2 RMS (px) | Refit − stored (px) | Mapping equal? |
|---|---|---:|---:|---:|---|
| 24→40 | reflected | 0.031139094 | 0.031137713 | -0.000001381 | True |
| 24→73 | reflected | 0.206186470 | 0.206429080 | +0.000242609 | True |
| 40→73 | proper | 0.231548888 | 0.231804911 | +0.000256023 | True |


The differences are small in source-pixel terms, but I do **not** label them “exactly reproduced.” The page-24/page-40 RMS delta is near rounding scale; the pairs involving page 73 differ by approximately 0.00024–0.00026 px. The stored v1.1 sheet says it uses the threshold-60 coordinates from the centroid sheet, but its original fit code/full-precision inputs were not recovered. A plausible explanation is that the stored fit was computed from full-precision centroid values before the centroid cells were rounded, but this remains a hypothesis rather than a verified cause. Both values are retained; v1.2 fits are reproducible from the stored numeric centroid cells.

## Normalized pairwise-distance signatures

For each five-point group, the ten Euclidean pair distances were computed in source pixels, sorted ascending, and divided by that group's RMS pair distance. This creates a rotation-, reflection- and uniform-scale-invariant shape vector. It does **not** preserve the point labels or orientation.

| Pair | RMS difference between normalized sorted signatures | Source group RMS pair distances (px) |
|---|---:|---:|
| 24-40 | 0.000063647 | 483.222596 / 483.232699 |
| 24-73 | 0.000485024 | 483.222596 / 483.430977 |
| 40-73 | 0.000530601 | 483.232699 / 483.430977 |

The similarity-signature results reinforce the geometric resemblance across the selected pilot motifs. They do not establish that the motif is a cipher, that the same ornament was independently drawn, or that the arrangement is statistically rare across the manuscript. The point configurations were chosen after visual inspection, and repeated use of an ornament is a live alternative.

## Threshold sensitivity

`Pixel Thresholds v1.1` supplies 60 threshold-specific rows: 15 target points × thresholds 40, 60, 80 and 100. Recalculated displacement from each point's threshold-60 location:

- Maximum displacement across points and thresholds: **0.173612 px**.
- Median of the 15 per-point maximum displacements: **0.050990 px**.

This reproduces the threshold-stability values in the workbook. Because all measurements in this table are inherited from the same recorded decoder output, it is a sensitivity test, not independent decoder validation.

## Controls

### Pages 50 and 56: three-dot rows

| Page | Adjacent gap 1 (px) | Adjacent gap 2 (px) | Gap 1 share | Gap 2 share | Vertical spread (px) |
|---:|---:|---:|---:|---:|---:|
| 50 | 417.625 | 478.154 | 46.621432% | 53.378568% | 0.008 |
| 56 | 196.000 | 224.510 | 46.610069% | 53.389931% | 0.000 |

A same-order rotation/scale/translation fit has RMS error **0.022529 px**, maximum error **0.031836 px**, scale 0.469437383. The matching normalized gap split is consistent with a reused scaled decoration/template. It is not a cipher result.

### Pages 57 and 68: plant-side five-dot group

The five right-side plant-group rows on pages 57 and 68 have exactly equal **recorded** centroid coordinates, component areas, and bounding boxes (`True`). This makes reuse of an ornament the default explanation to test first. No pixelwise comparison of corresponding JPEG crops was completed in the local runtime, so the v1.2 claim is record-level equality, not byte/pixel identity.

### Page 39: six-dot control

All six five-point subsets from the recorded six-dot group were compared to the page-24 target using the same sorted, RMS-normalized ten-distance signature. The closest subset is `label_1; label_2; label_3; label_4; label_6`, with signature RMS difference **0.153383**. The other five subset distances are included in `Auxiliary Controls v1.2`. This is a useful descriptive control but only one local six-dot group; it is not a sample large enough to establish manuscript-wide significance.

## Critical unresolved measurement-provenance gap

The v1.1 centroid sheets describe their measurements as coming from a “new JS baseline-JPEG Y decoder.” The recovered `measure_constellations_v0_2.py`, however, opens JPEGs with **Pillow** (`Image.open`) and implements the connected-component detection. Its `--self-test` creates synthetic circles and checks detection/centroid behavior at thresholds 40, 60, 80 and 100. The synthetic self-test is useful, but it does not re-decode the Liber Primus pages or independently confirm the reported JavaScript decoder output.

The v1.1 sheet names a separate JavaScript decoder, but no such source file was among the recovered artifacts found for this turn. Source JPEG bytes could not be transferred into the local image-analysis runtime, so there is no new side-by-side pixel comparison, MAE/max-difference calculation, component-mask comparison or centroid cross-check to report. **Independent decoder validation remains open.**

The Python script also searches only the three pilot ROIs for pages 24, 40 and 73. It is not a whole-corpus detector, and its CSV output does not retain every rejected connected component. It cannot be described as a corpus-wide search in its current form.

## Null distribution: historical test rejected for inferential use

The v1.0 geometry sheet recorded 250,000 comparisons against synthetic random points sampled from a rectangular coordinate domain, with zero hits, and a small empirical p-value. That number is preserved in `Null Distribution v1.2` as historical audit metadata but is **not accepted as a manuscript-specific significance estimate**:

1. The random points do not reproduce real dot clusters, ornaments, page layout or scanning/detection artifacts.
2. The target motif and pages were selected after visual inspection, creating selection bias.
3. A repeated/copy-pasted ornament could create repeated measurements but is not independent cipher evidence.
4. The full search family—pages, ROIs, thresholds, point subsets, point orderings, transformations and other prior visual explorations—has not been replayed under the null.
5. The available script's default random-pair comparison count is 60,000, while the historic sheet reports 250,000; the run configuration that reconciles those values was not recovered.

No new empirical p-value is reported. The proper next null is manuscript-empirical: detect candidate clusters across the full source corpus with fixed criteria, retain accepted and rejected candidates, merge exact/near-copy ornament families, and rerun the same complete selection procedure on matched null comparisons.

## Work completed vs not completed

| Task | Status | Interpretation |
|---|---|---|
| Recover workbook and script | Confirmed | Available and read locally. |
| Audit target centroid rows and normalization | Reproduced | Primary workbook records are internally consistent. |
| Confirm eight pilot source object IDs | Independently checked via GitHub metadata | 8/8 Git blob IDs match; no pixel decode performed. |
| Refit target transforms over all point permutations | Reproduced mathematically | Mappings and model classes agree; small residual discrepancies against v1.1 are itemized in the reconciliation block. |
| Recompute normalized distance signatures | Reproduced mathematically | Same normalizer applied to all target groups; descriptive only. |
| Recompute pages 50/56 controls | Reproduced mathematically | Similar three-dot spacing and scaled fit. |
| Compare p57/p68 records | Reproduced at record level | Equality of saved coordinates/boxes/areas; exact pixel identity unresolved. |
| Compare page39 subset control | Reproduced mathematically | Closest signature difference 0.153383; only one local control cluster. |
| Cross-decode raw JPEG pixels | Unresolved / blocked | Need source bytes in local runtime and a documented decoder implementation. |
| Scan entire corpus | Not run | No whole-corpus local detection table. |
| Build manuscript-empirical null | Deferred | Existing synthetic null is not fit for inferential use. |
| Test a text/rune mapping | Deferred | No predeclared signal-to-cipher rule or held-out prediction. |

## Next experiment — prioritized

**Make the detection pipeline reproducible before expanding the hypothesis.** Recover/version the exact JavaScript decoder source referenced by v1.1 or extract source JPEG bytes into the local runtime. Decode the same pilot pages with Pillow/libjpeg and the custom implementation independently; record per-pixel agreement, grayscale conversion convention, MAE and maximum difference, then rerun component detection against the same ROIs and thresholds. After the data-generation gap is closed, expand the detector to all 00–74 pages and preserve all rejected candidates, then build the real-cluster null distribution. Cipher correlation should remain deferred until the selected motif beats that null.

## Files and source locations

- Input workbook: `liber_primus_visual_master_dataset_v1_1.xlsx`
- New workbook: `liber_primus_visual_master_dataset_v1_2.xlsx`
- Refit/build script: `build_liber_primus_geometry_v1_2.py`
- Machine-readable results: `liber_primus_visual_geometry_audit_v1_2.json`
- Extraction script recovered: `measure_constellations_v0_2.py`
- Public source repository: [https://github.com/scream314/cicada3301/blob/master/assets/2014/liber-primus-complete](https://github.com/scream314/cicada3301/tree/master/assets/2014/liber-primus-complete)

**Bottom line:** the geometric repetition survives consistent arithmetic refitting on the recorded coordinates, but the current evidence does not yet distinguish a copied decorative template from an unusual independent structure, and it does not establish any relation to the cipher. Source-pixel cross-validation and an empirical corpus null are the next falsification gates.
