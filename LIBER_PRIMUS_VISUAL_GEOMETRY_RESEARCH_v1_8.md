# Liber Primus Visual Geometry Research — v1.8

**Date:** 2026-10-10  
**Scope:** Harmonized comparison of previously recorded dot-cluster geometry plus qualitative review of browser-rendered source scans.  
**Status:** Descriptive evidence only; independent local source-pixel validation remains blocked.

## Summary

This version addresses a known comparability issue in the historical workbook: the five-dot target signature sheet uses distances normalized by each cluster's RMS pair distance, while some control summaries use maximum-distance normalization. Both measures are now recomputed consistently from the same threshold-60 centroid records for the target groups and controls.

The primary observation remains stable. The isolated five-dot groups on pages 24, 40, and 73 have almost identical order-independent normalized pair-distance signatures. The page-68 plant-adjacent five-dot control and the best five-of-six subset from the page-39 six-dot control are substantially different under both normalization conventions. The right-side plant-dot records on pages 57 and 68 are identical point-by-point in the stored centroid, area, and bounding-box data, consistent with repeated decorative artwork. Pages 50 and 56 contain a separate three-dot horizontal-row candidate with nearly identical normalized spacing despite a roughly 2.13× difference in end-to-end span.

This supports multiple recurring graphic templates as a reasonable working explanation. It does not establish that any of the motifs encode a key, rune values, or plaintext.

## 1. Harmonized five-point signature comparisons

For each five-point group, all ten Euclidean pairwise distances are sorted ascending. Two signatures are computed:

1. Each distance divided by the RMS of all ten distances in that group.
2. Each distance divided by the maximum of the ten distances in that group.

For each normalization, the signature distance is the RMS difference between the equal-length sorted signatures. These comparisons ignore point labels and are invariant to translation, rotation, reflection, and uniform scale. They do not replace the point-correspondence transform fits already preserved in the workbook.

| Comparison | RMS-normalized signature difference | Max-normalized signature difference |
|---|---:|---:|
| Page 24 vs 40 | 0.000063647 | 0.000041311 |
| Page 24 vs 73 | 0.000485024 | 0.000321098 |
| Page 40 vs 73 | 0.000530601 | 0.000348780 |
| Page 24 vs page-68 plant control | 0.180217842 | 0.191306768 |
| Page 40 vs page-68 plant control | 0.180202301 | 0.191302617 |
| Page 73 vs page-68 plant control | 0.180194597 | 0.191345132 |
| Page 24 vs best page-39 five-of-six subset | 0.153383071 | 0.105133361 |
| Page 40 vs best page-39 five-of-six subset | 0.153403888 | 0.105147517 |
| Page 73 vs best page-39 five-of-six subset | 0.153535007 | 0.105244265 |
| Page 57 plant cluster vs page 68 plant cluster | 0 | 0 |

The largest target-to-target signature difference is **0.000530601** under RMS normalization and **0.000348780** under maximum-distance normalization. Compared on the same scale, the page-68 control is about **340×** and **549×** these respective baseline differences; the closest page-39 five-of-six control is about **289×** and **301×** the respective baseline differences.

The page-39 comparison explicitly searches all six possible five-point subsets, separately under each normalization. The same subset (stored labels 1, 2, 3, 4, 6) is closest under both measures for each target. This subset selection makes the result descriptive and selection-conditioned.

The two normalizations produce different absolute distances, but the main conclusion is robust: the target groups are mutually much more similar than either stored control. These ratios are **not p-values** and do not estimate the frequency of such motifs across the manuscript.

## 2. Repeated decorative motif: pages 57 and 68

The stored threshold-60 records for all five points in the right-side plant-adjacent group match point-for-point across pages 57 and 68: centroid coordinates, component areas, and bounding-box fields all match at the precision recorded in the workbook (5/5 records).

The browser-rendered source scans also show the same-looking botanical border artwork and small adjacent dot clusters on both pages, alongside different text content:

- [Page 57 original repository image](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/57.jpg)
- [Page 68 original repository image](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/68.jpg)

This strengthens the repeated-decoration explanation for that control. It remains a visual observation and a stored-record match, not a pixel-by-pixel crop identity test. That test still requires locally available original JPEG bytes.

## 3. Separate three-dot row: pages 50 and 56

The stored left-to-right gap proportions are:

| Measure | Page 50 | Page 56 |
|---|---:|---:|
| First gap as share of row span | 46.6214% | 46.6101% |
| Second gap as share of row span | 53.3786% | 53.3899% |

The page-50 end-to-end span is 895.779 px; page 56's is 420.510 px, a span ratio of **2.130220**. The RMS-normalized signature difference is **0.000131015**; the maximum-normalized signature difference is **0.000092783**. This looks like another recurring layout motif at two sizes, distinct from the five-dot constellation. The three-point row must not be mixed into a five-point control distribution.

Browser-rendered source images:

- [Page 50 original repository image](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/50.jpg)
- [Page 56 original repository image](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/56.jpg)

## 4. Qualitative visual cross-check of the target pages

The raw image URLs for pages 24, 40, and 73 rendered in the browser:

- [Page 24](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/24.jpg): five large dark dots below a red-highlighted block.
- [Page 40](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/40.jpg): five large dark dots above the text block, with a visually corresponding shape under vertical reversal.
- [Page 73](https://raw.githubusercontent.com/scream314/cicada3301/master/assets/2014/liber-primus-complete/73.jpg): five large dark dots below the lower text; the inherited signature is related but not as close as pages 24 and 40.

The browser-rendered images are scaled for display. They support qualitative placement and motif classification only; they do not supply local decoded pixels to the numerical pipeline. Page 39's raw image did not render successfully in this pass, so its use remains based on inherited coordinates.

## 5. Source acquisition and provenance

The source inventory and Git blob SHA-1 values remain available in `liber_primus_visual_source_integrity_v1_4.json`. In this run, local shell requests to both `raw.githubusercontent.com` and `api.github.com` failed with DNS name-resolution errors. The browser could render several raw scan URLs, but that did not transfer the JPEG bytes to the local analysis filesystem.

Consequently, this version has **not** recomputed the source JPEG SHA-256 or Git blob SHA-1, validated local image dimensions, compared JPEG decoder implementations, or performed image-mask/crop difference analysis. The centroid and component values remain inherited workbook records. No full-page detection was run, and rejected component records were not newly enumerated.

## 6. Interpretation and next gate

Current working interpretation:

- Pages 24, 40, and 73 remain a strong descriptive geometric-recurrence candidate.
- Pages 57 and 68 provide a useful repeated-decoration control.
- Pages 50 and 56 provide a separate scaled three-dot-row candidate.
- The page-39 six-dot control is much less similar to the target five-dot signature.
- Nothing in this update identifies a dot-to-rune mapping or proves cipher relevance.

**Next critical gate:** obtain the original page JPEGs locally (start with 24, 40, 57, 68, 73; include 39, 50, and 56 for controls), verify their Git blob identifiers and SHA-256 hashes, decode them using a standard independent JPEG pipeline, and reproduce the centroids from prespecified ROIs. Only after that should the corpus-wide detector be frozen and expanded. No significance test should be attempted until the broader candidate-selection process can be rerun against a manuscript-appropriate empirical null.

This geometry investigation remains separate from the keystream-source investigation. No relation between these dot patterns and a keystream or plaintext is currently supported.
