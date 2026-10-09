# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (eleventh report)  
**Experiment:** Complete remaining geometric inventory items — infinity symbols, insect dots (page 19), master workbook update  
**Repository:** mrfentmen/annotated-pages  
**Workbook:** `liber_primus_visual_master_dataset_v0_11.xlsx` (local artifact)

---

## 1. Scope

This report closes the three open geometric follow-ups:

1. Infinity-symbol endpoints / lobes on pages 17–19  
2. Insect-eye and scale dots on page 19  
3. Master workbook update with a consolidated “Asset Reuse & Continuous” sheet

---

## 2. Infinity symbols (pages 17–19)

**Master Dataset:** Infinity-like marks centered above the first text line and below the last text line on each of pages 17, 18, 19.

**Detection:** Local dark-component search around the expected top (~y 600–650) and bottom (~y 2930–2970) central regions recovers consistent blobs. The strongest responses are essentially identical across the three pages.

**Nature:** The marks are continuous lemniscate-style curves. “Endpoints” or “lobes” do not present as large, isolated circular dots; any discrete points would be arbitrary samples of a continuous stroke.

**Classification:** Continuous ornament; asset reuse confirmed across 17–19. Not added to the discrete point-set inventory.

---

## 3. Insect figure on page 19

**Master Dataset / CSV notes:**  
- Insect or larva-like drawing below the text  
- Possible black dot for the cicada’s eye  
- Claim of seven exact scales on the body

**Detection:**  
- Lower-left / lower-middle region (y ≈ 2300–2900) yields only a few small dark components under multiple thresholds.  
- Annotation difference map shows a label near (264, 2524) consistent with the insect location, plus additional labels in the lower text area.  
- No clean set of seven scale dots or a single high-contrast eye dot was isolated by automatic methods.

**Classification:** Continuous (or low-contrast) figure; discrete eye/scale point set unresolved. Recorded as such in the inventory.

---

## 4. Master workbook update (v0_11)

New sheet **“Asset Reuse & Continuous”** summarises every major visual motif examined to date:

| Motif class              | Pages       | Discrete point-set? | Asset reuse? | Status                          |
|--------------------------|-------------|---------------------|--------------|---------------------------------|
| Primary 5-dot template   | 24, 40, 73  | Yes                 | Geometric   | Verified, statistically extreme |
| Plant-side 5+3           | 57, 68      | Yes                 | Pixel-identical | Verified                    |
| 3-dot rows               | 50, 56      | Yes                 | Partial     | Verified                        |
| 6-dot control            | 39          | Yes                 | —           | Verified (control)              |
| Spiral ornaments         | 20–23       | No                  | Yes         | Continuous / unresolved         |
| Cross-like ornaments     | 17–19       | No                  | Yes         | Continuous                      |
| Infinity symbols         | 17–19       | No                  | Yes         | Continuous                      |
| Insect figure            | 19          | Uncertain           | —           | Unresolved                      |

Version history entry added for v0_11.

The workbook remains the single authoritative dataset; all prior measured-centroid and geometry sheets are retained unchanged.

---

## 5. Overall geometric inventory status (end of this pass)

**High-precision discrete point sets (usable for signature / rigid-fit analysis):**
- Primary five-dot template (24 / 40 / 73) — unique, extreme residuals  
- Plant-side clusters (57 / 68)  
- 3-dot rows (50 / 56)  
- 6-dot control (39)

**Confirmed continuous ornaments with systematic asset reuse:**
- Spirals (20–23)  
- Crosses (17–19)  
- Infinity marks (17–19)  
- Plant illustrations (57 / 68)

**No additional discrete point set comparable in precision or statistical extremity to the primary five-dot template has been found.**

---

## 6. Implications

The geometric phase of the investigation has now surveyed every major class of visual element flagged in the Master Dataset and source CSV for discrete dots or constellations. The primary five-dot template stands alone as a high-fidelity, multi-page, statistically extreme discrete structure. All other striking ornaments examined are either:

- continuous line art that is reused as a graphic asset, or  
- lower-precision / lower-contrast marks that do not survive the same measurement pipeline.

This closes the current geometric inventory expansion. Any future claim that another visual element encodes cipher-relevant information would need to begin by producing a comparably precise, reproducible point set.

---

*Workbook v0_11 and this report together constitute the updated geometric baseline for the project.*
