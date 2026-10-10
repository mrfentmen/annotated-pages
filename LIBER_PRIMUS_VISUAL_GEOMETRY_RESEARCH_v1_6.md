# Liber Primus Visual Geometry Investigation — Research Record v1.6

**Date:** 2026-10-10  
**Master workbook:** `liber_primus_visual_master_dataset_v1_6.xlsx`  
**Prior records:** All v1.5 and earlier sheets retained; v1.6 adds `Coordinate Refit v1.6` and `Source Acquisition v1.6`.  
**Original image pixels processed in this pass:** No.

## 1. Source acquisition outcome

The v1.5 project artifacts were found in the Library and materialized for inspection: the master workbook, v1.4 source-integrity manifest, v1.5 audit script, v1.5 audit JSON, and v1.5 research report. The manifest records 75 GitHub page objects (`00.jpg`–`74.jpg`).

The current GitHub directory metadata returned entries for pages 24, 40, 57, 68, and 73, including their Git blob identifiers. The identifiers for pages 24, 40, and 73 agree with those recorded in the workbook's inherited centroid table. This is a metadata/provenance cross-check only.

A local raw-image retrieval attempt failed with:

`curl: (6) Could not resolve host: raw.githubusercontent.com`

The GitHub connector also returned page 24 content in base64 form, but it was not transferred into the local pixel-analysis filesystem as a decodable image file. The new acquisition script was then run against page 24; it returned `BLOCKED_DOWNLOAD` with `URLError: <urlopen error [Errno -3] Temporary failure in name resolution>` and wrote `source_acquisition_audit_v1_6.json`. Therefore, no local SHA-256 was computed for the original image bytes, no local JPEG was decoded, and no fresh component/centroid measurement was performed. **This does not complete the original-pixel validation stage.**

A runnable acquisition script, `acquire_verify_liber_primus_sources_v1_6.py`, is included. It downloads the five priority pages by default (or all 75 via `--all-pages`), computes the Git blob SHA-1 from the acquired bytes, checks it against the manifest, computes SHA-256, verifies JPEG format and expected dimensions, and records successes and failures to JSON. Its local self-test passed, checking only the Git blob hashing helper, not the actual page images. The scripted page-24 download test also failed at DNS resolution and correctly generated a failure record without claiming byte verification.

## 2. Coordinate-level refit (inherited values only)

I independently recomputed the similarity transforms directly from the five stored centroids per page in `Pixel Centroids v1.1`. For each page pair, the search enumerated all 120 correspondences under both determinant-constrained model classes: 240 fits per pair. The results reproduce the earlier workbook values to the expected rounding.

| Page pair | Best transform | Mapping (source → target) | Scale | RMS residual | Maximum residual |
|---|---|---|---:|---:|---:|
| 24 → 40 | Reflection | 1→1; 2→2; 3→5; 4→4; 5→3 | 1.000020902 | 0.031138 px | 0.052693 px |
| 24 → 73 | Reflection | 1→4; 2→5; 3→3; 4→2; 5→1 | 1.000431004 | 0.206429 px | 0.288245 px |
| 40 → 73 | Proper rotation | 1→4; 2→5; 3→1; 4→2; 5→3 | 1.000410028 | 0.231805 px | 0.339007 px |

The page 24 → 40 fit is particularly close to a vertical reflection plus translation: scale 1.000020902, translation (-0.2099, 3674.0080) pixels, RMS residual 0.03114 px. That pattern is consistent with mirrored or reused artwork, but the stored coordinates alone cannot distinguish exact pixel reuse from template reuse or another production process.

The normalized, sorted pair-distance signature RMS differences are:

| Pair | RMS difference |
|---|---:|
| 24–40 | 0.0000636469 |
| 24–73 | 0.0004850238 |
| 40–73 | 0.0005306006 |

These are descriptive calculations based on inherited centroid values. The small residuals were selected after searching correspondences and two determinant classes. They are not p-values, do not account for the full manuscript-wide selection process, and do not establish cipher relevance. No claim is made that the raw image pixels have now independently confirmed these coordinates.

## 3. What remains unresolved

The primary blocker is still the absence of exact source JPEG bytes in a filesystem where they can be decoded. The stored page 24/40/73 centroid records remain unverified at the pixel level. The page 57/68 plant-ornament equality also remains an inherited table observation; this pass did not inspect those pixels.

After successful acquisition, the next measurement pass should verify the downloaded bytes against the manifest before decoding, compare the Pillow/luma decoder path against the recorded JavaScript baseline on identical bytes, retain all connected components and rejection reasons, and use globally optimal one-to-one matching for threshold stability. A corpus-wide detector and a manuscript-empirical null must follow only after the extraction pipeline is frozen and checked on controls.

Visual geometry remains separate from the keystream-source investigation. This update establishes no plaintext, key, keystream source, or geometric cipher mapping.
