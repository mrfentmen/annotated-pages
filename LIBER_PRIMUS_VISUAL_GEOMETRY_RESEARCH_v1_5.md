# Liber Primus Visual Geometry Investigation — Research Record v1.5

**Date:** 2026-10-10  
**Master dataset:** `liber_primus_visual_master_dataset_v1_5.xlsx` (v1.4 retained, one audit sheet appended)  
**Pipeline reviewed:** `measure_constellations_v0_2.py`  
**Source-pixel measurements made in this pass:** No

## Result of this round

I continued with the next available reproducibility task: a static audit of the existing centroid-extraction pipeline and an execution of its built-in synthetic self-test. The self-test passed at grayscale thresholds 40, 60, 80, and 100, finding all five synthetic circles with zero rounded-center error. This validates only that narrow synthetic case. It does **not** validate the original JPEG decoder, selected regions of interest, actual dot centroids, repeated artwork, or a cipher connection.

The exact source image bytes still are not present in the local runtime. An attempt to retrieve the raw GitHub image from the runtime failed because external DNS/network access is unavailable there. The public Git blob inventory in v1.4 establishes repository object identity, not independent pixel reproduction.

## Main pipeline audit findings

1. **The script is not a full-corpus detector.** It only processes preselected regions on pages 24, 40, and 73. It cannot support claims about the absence or frequency of similar geometry elsewhere in the 75-page manuscript.
2. **Rejected components are discarded.** The filter keeps only components that look like solid circular dots by area, bounding box, aspect ratio, and fill ratio. Rejected components and rejection reasons are not exported, which prevents auditing detector bias.
3. **The signature normalization differs from the workbook.** The script divides pair distances by the median distance; `Cluster Signatures v1.2` documents RMS pair-distance normalization. These numbers are not directly comparable.
4. **The optional random null is not suitable for inferential claims.** It samples points uniformly in a rectangle rather than modeling the actual page artwork, mark distribution, repeated/mirrored ornaments, detection process, and target-selection process. The script's computed empirical p-values must not be presented as evidence of significance.
5. **Threshold matching is greedy.** It pairs components across thresholds by nearest available centroid. With crowded or irregular regions, greedy pairing can fail to find the globally best one-to-one assignment and may misstate centroid stability.
6. **The decoder cross-check remains open.** The script uses Pillow's grayscale conversion. The stored centroid sheet says its measurements came from a separate JavaScript baseline-JPEG luma decoder. Those outputs need to be compared on identical verified JPEG bytes before either is treated as independently validated.
7. **Signature length is not checked.** The RMS-difference helper uses `zip`, so unequal-length vectors would be silently truncated instead of rejected. Current five-point targets are expected to produce ten distances, but the assumption should be enforced.

## Current interpretation

This audit does not change the geometric evidence. The previously recorded near-identical five-dot signatures for pages 24, 40, and 73 remain a promising descriptive observation, but their original-pixel measurements are not independently reproduced here. The stored page 57/68 equality likewise remains record-level evidence, not a fresh pixel comparison. Neither result establishes a cipher relationship.

## Next evidence gate

1. Acquire the exact original JPEG bytes for pages 24, 40, 57, 68, and 73 (then all pages) in an environment that can write those bytes to disk.
2. Verify each file against its Git blob SHA-1 before decoding.
3. Run Pillow/libjpeg and the recorded JavaScript luma decoder on the exact same bytes; compare decoded luma pixels or, at minimum, independently extracted centroids and connected-component masks.
4. Preserve **all** connected components and their rejection reasons; freeze detector parameters before running the 75-page scan.
5. Blindly review candidate groups, identify copied-artwork families, and only then construct a manuscript-empirical control distribution that repeats the complete target-selection procedure.
6. Keep cipher relevance as a separate test requiring a predeclared coordinate/order-to-rune prediction. Geometry similarity alone is not enough.

## Files

- `liber_primus_visual_master_dataset_v1_5.xlsx` — authoritative master with `Pipeline Audit v1.5` appended.
- `liber_primus_geometry_pipeline_audit_v1_5.json` — machine-readable findings and synthetic self-test result.
- `audit_geometry_pipeline_v1_5.py` — script used to generate this audit.

The v1.4 source integrity inventory and earlier research sheets are retained unchanged in the master workbook.
