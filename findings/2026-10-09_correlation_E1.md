# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (sixth report)  
**Experiment:** E — First correlation tests between the primary five-dot template and independent page/text properties  
**Previous reports:** all earlier 2026-10-09 findings in this folder  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Test whether the presence, orientation, or transformation type of the isolated five-dot template (pages 24, 40, 73) correlates with independently measurable textual or structural properties of *Liber Primus*.

---

## 2. Data used

**Geometric facts (verified):**
- Pages carrying the primary five-dot template: **24, 40, 73**
- Structured transforms (scale ≈ 1, residuals ≤ 0.23 px):
  - 24 → 40: vertical reflection (bottom → top of page)
  - 40 → 73: 180° rotation
  - 24 → 73: horizontal reflection
- Vertical placement: 24 bottom, 40 top, 73 bottom

**Textual / structural facts (from scream314/cicada3301 `pages_and_ciphers.md` and community status):**
- Page 24 lies in the range marked cipher method **"?"** (unsolved).
- Page 40 lies in the range marked cipher method **"?"** (unsolved).
- Page 73 lies in the range **56.jpg – 73.jpg**, which has a published solution method:  
  `nth letter’s shift = φ(nth prime) % 29` (shift down, forward Gematria; skip cleartext F = ᚠ).

---

## 3. Correlation tests performed

### 3.1 Presence vs solved / unsolved status

| Page | Five-dot present | Cipher status in pages_and_ciphers.md |
|------|------------------|---------------------------------------|
| 24   | Yes              | ? (unsolved)                          |
| 40   | Yes              | ? (unsolved)                          |
| 73   | Yes              | Known method (φ(pₙ) % 29)             |

**Result:** The template appears on both unsolved and solved pages.  
**Conclusion:** Simple presence of the five-dot motif does **not** mark a page as unsolved (or solved).

### 3.2 Page-number arithmetic

- Differences: 40 − 24 = **16**, 73 − 40 = **33**, 73 − 24 = **49**
- Sum: 24 + 40 + 73 = **137**
- 3301 ÷ 24 ≈ 137.54 (remainder 13)
- No common small modulus (mod 3/5/7/11) is shared by all three pages.
- Parity: even, even, odd — no uniform pattern.

137 is a number that appears elsewhere in Cicada discussion (sometimes linked to the fine-structure constant or other numerical references), but a single arithmetic coincidence is not treated as evidence.

### 3.3 Orientation / transformation vs page position

- The vertical-reflection transform (24 → 40) moves a bottom-of-page motif to the top of the page — geometrically consistent with the measured y-coordinates.
- 180° and horizontal transforms map between bottom placements.
- No additional textual variable (line count, rune count, red-glyph presence) has yet been systematically tabulated for these three pages, so further orientation tests are pending data.

### 3.4 Comparison with the three-dot motif

Pages 50 and 56 also carry a recurring (but different) three-dot motif.  
Page 56 falls inside the same solved-method range as page 73 (56–73).  
Page 50 is earlier.  
No clear shared rule with the five-dot pages has been identified yet.

---

## 4. What has **not** been found

- No simple modular or arithmetic progression that uniquely selects {24, 40, 73}.
- No one-to-one mapping from transformation type to solved/unsolved status.
- No evidence yet that the dots encode page-local rune counts or line structure (those quantities have not been fully extracted for the three pages in this pass).

---

## 5. Interpretation (strict)

The first round of correlation tests is largely negative or inconclusive. The geometrically distinctive five-dot template does not appear to be a simple “this page is unsolved” flag, nor does its page-number set follow an obvious low-complexity arithmetic rule that has been tested.

This is useful: it rules out the most superficial mappings and forces any future cipher hypothesis to be more specific (e.g., the orientation or the particular transform might index a key stream, a reading order, or a subsection boundary that is not visible from page number alone).

---

## 6. Immediate next correlation work

1. Extract or obtain reliable per-page rune counts and line counts for pages 24, 40, 50, 56, 73 (and a control set of pages without the motifs).  
2. Test whether the transformation type (reflection vs 180°) correlates with any change in rune density, presence of red glyphs, or chapter boundaries.  
3. Examine the solved plaintext of the 56–73 section (where available) for any structural feature that aligns with the placement of the five-dot on page 73.  
4. Only after the above, consider more elaborate mappings (e.g., using the five points as indices into a key or as a permutation of a local text block).

---

*Negative correlation results are reported with the same care as positive geometric results. The distinctive geometry remains established; a textual function for it has not yet been demonstrated.*
