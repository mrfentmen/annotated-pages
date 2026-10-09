# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (seventh report)  
**Experiment:** E continued — Rune-count context, solved-section structure, and placement of the five-dot on page 73  
**Previous correlation report:** [2026-10-09_correlation_E1.md](./2026-10-09_correlation_E1.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Deepen the correlation tests by examining:
- Approximate rune/line volume of the page ranges that contain the five-dot and three-dot motifs.
- The structure of the known-method section 56–73 that ends with the five-dot page.
- Placement of the five-dot relative to text and to the following “PARABLE” unit.

---

## 2. Rune / line volume from pages_and_ciphers.md

Page ranges are multi-page, so exact per-page rune counts are not directly available. Approximate totals for the blocks that contain our motifs:

| Page range (containing motif) | Cipher method          | Approx. runes in block | Approx. lines | Motif pages |
|-------------------------------|------------------------|------------------------|---------------|-------------|
| 6.jpg/2–7.jpg – 23.jpg/2–24.jpg | ?                    | 333                    | 6             | 24          |
| 15.jpg/2 – 32.jpg/2–39.jpg    | ?                      | 1894                   | 20            | 39 (control)|
| – – 40.jpg–43.jpg             | ?                      | 1021                   | 9             | 40          |
| 33.jpg – 50.jpg/1             | ?                      | 91                     | 3             | 50 (3-dot)  |
| 50.jpg/2–56.jpg/1             | ?                      | 1468                   | 19            | 50, 56      |
| 56.jpg/2                      | ?                      | 121                    | 3             | 56          |
| **56.jpg – 73.jpg**           | **φ(pₙ) % 29**         | **84**                 | **11**        | **73**      |
| 57.jpg – 74.jpg               | default Gematria       | 94                     | 4             | (follows)   |

**Observation:** The block that ends with the five-dot page (56–73) is unusually short in rune count (84 runes) compared with the long unsolved blocks that contain pages 24 and 40.

---

## 3. Structure around page 73

From `pages_and_ciphers.md`:

- **56.jpg – 73.jpg**  
  Method: `nth letter’s shift = φ(nth prime) % 29` (shift down, forward Gematria; skip cleartext F).  
  Content includes a short runic passage, intermediate hexadecimal/hash-like strings, and a final short runic line.  
  The five-dot constellation sits at the **bottom** of page 73, after the text of this block.

- **Immediately following (57.jpg – 74.jpg)**  
  Method: Substitution with default Gematria.  
  The PRE block begins with clearly English-derived runes that transliterate to:

  ```
  PARABLE
  LIKE THE INSTAR TUNNELING TO THE SURFACE
  WE MUST SHED OUR OWN CIRCUMFERENCES
  FIND THE DIVINITY WITHIN AND EMERGE
  ```

  This matches community notes about a solved or partially solved unit near pages 56–57.

**Geometric placement:**  
The five-dot on page 73 is positioned at the bottom of the page, i.e. after the text of the φ(pₙ)%29 block and at the boundary before / near the “PARABLE…” unit.

---

## 4. Correlation assessment

| Hypothesis | Evidence | Status |
|------------|----------|--------|
| Five-dot marks unsolved pages only | Present on both ? and known-method pages | **Rejected** |
| Five-dot marks the end of a cipher unit | Sits at the bottom of the final page of the 56–73 known-method block | **Plausible, unproven** |
| Page-number arithmetic uniquely selects the set | No clean low-complexity rule found | **Not supported** |
| Orientation encodes solved vs unsolved | 24 & 40 (unsolved) use vertical-reflection pair; 73 (known method) is related by 180°/horizontal | **Insufficient data** |
| Rune density differs systematically | 56–73 block is short (84 runes); 24/40 blocks are longer | **Suggestive only** (multi-page blocks) |

---

## 5. Interpretation

The strongest structural observation so far is **positional**: the five-dot on page 73 appears at the bottom of the last page of a known-method cipher block and immediately before a short, English-readable “PARABLE / INSTAR / DIVINITY” unit.  

This is consistent with (but does not prove) a role as a section terminator or boundary marker. The same motif on pages 24 and 40 sits inside longer unsolved blocks, so the marker hypothesis, if true, would have to be more nuanced than “end of every cipher section.”

No quantitative correlation with rune count, line count, or simple arithmetic has been established that survives controls.

---

## 6. Next concrete steps

1. Obtain or derive **true per-page** rune and line counts (ideally from a community-maintained transcription or by OCR/counting on the original images) for pages 20–73.  
2. Check whether any other known-method section ends with a comparable geometric marker.  
3. Transliterate / examine the short runic content of the 56–73 block itself for any internal reference to geometry, dots, or orientation.  
4. Only if a consistent boundary or indexing pattern emerges should more elaborate mappings (point-to-keystream, etc.) be attempted.

---

*The distinctive geometry remains solidly established. The first textual correlations are weak or negative; the boundary-marker observation is the only positive structural lead and remains provisional.*
