# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (eighth report)  
**Experiment:** E continued — Other known-method section endings and transliteration of the 56–73 block  
**Previous:** [2026-10-09_correlation_E2.md](./2026-10-09_correlation_E2.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Test the provisional “section-boundary marker” hypothesis more rigorously by:
1. Listing all known-method sections and their ending pages.
2. Checking whether those ending pages carry the primary five-dot (or other verified geometric motifs).
3. Attempting a basic transliteration of the short runic content of the 56–73 block that ends with the five-dot page.

---

## 2. Known-method sections and ending pages

From `pages_and_ciphers.md` (method ≠ “?” and ≠ “english”):

| Ending page (approx.) | Method summary                          | Verified geometric motif? |
|-----------------------|-----------------------------------------|---------------------------|
| 01                    | Reversed Gematria                       | No                        |
| 04                    | DIVINITY shift                          | No                        |
| 05                    | Default Gematria                        | No                        |
| 09                    | Shift 3 down reversed                   | No                        |
| 4 (index)             | Default Gematria                        | No                        |
| 167                   | FIRFUMFERENFE shift                     | No                        |
| 229                   | Default Gematria                        | No                        |
| **73**                | **φ(pₙ) % 29**                          | **Yes — primary 5-dot**   |
| 74                    | Default Gematria                        | No                        |

**Result:** Among all known-method section endings, **only page 73** carries the primary five-dot template (in our verified inventory).  

Therefore the five-dot is **not** a general “end of every known-method section” marker.

---

## 3. Transliteration of the 56–73 runic block

Raw content (from pages_and_ciphers.md) contains:
- A short runic passage,
- Five lines of hexadecimal / hash-like data,
- A final short runic line.

Basic Futhorc → Latin mapping (Cicada/Gematria-Primus style) yields (noisy because of a few unmapped or corrupted characters):

```
AE[?] OESR MYLOH OAE CTHGW WLAE L
OAP MDDUGW L D[?]Y[?] CFIA AET
PEOATH CAE

[hex block]

CD FN IAE FNCING RF AEIRDE SYJEAUINGW XO MEAWF RGIA INGRB AENUS
```

No immediate English plaintext is visible. This is expected: the published method is a **position-dependent shift** (`φ(nth prime) % 29`), not a simple monoalphabetic substitution. A correct decipherment requires applying that transform letter-by-letter and handling the skip-F rule. That full decipherment was not re-implemented in this pass.

Nothing in the raw or naïvely transliterated text obviously refers to dots, geometry, orientation, or page numbers.

---

## 4. Updated status of the boundary-marker hypothesis

| Claim | Status after this round |
|-------|-------------------------|
| Five-dot marks the end of *every* known-method section | **Rejected** |
| Five-dot marks the end of the specific 56–73 φ(pₙ)%29 section | Still true positionally, but no longer generalisable |
| Five-dot appears only on unsolved pages | Already rejected (E1) |
| Simple page-number arithmetic selects the set | Already unsupported (E1) |

The positional observation (five-dot at the bottom of page 73, after a short known-method block and before the “PARABLE…” unit) remains factually correct but has lost most of its force as a general organising principle.

---

## 5. Interpretation

After two rounds of correlation testing:
- The geometric distinctiveness of the 24/40/73 five-dot template stands.
- No simple, robust mapping from that geometry to solved/unsolved status, page-number arithmetic, or “end of cipher section” has been found.
- The only remaining structural curiosity is local to page 73 and does not generalise to other known-method endings.

This is a normal and useful outcome: many attractive hypotheses are eliminated, narrowing the space of possible functions the motif could still have.

---

## 6. Recommended next directions

Given the pattern of negative correlation results, the highest-value remaining options are:

1. **Pause correlation** and return to geometric inventory (e.g. cross ornaments on 17–19, or a careful manual seeding of the spiral dots) so that more motifs are available for future tests.  
2. **Obtain true per-page rune counts** from a community transcription; the multi-page blocks currently limit quantitative tests.  
3. **Fully re-implement the φ(pₙ)%29 decipherment** on the 56–73 block and inspect the resulting plaintext for any internal reference to the five-dot or to orientation.  
4. Accept that the five-dot may be a high-precision decorative reuse (like the plant clusters) and document it as such unless new positive evidence appears.

---

*Negative results continue to be reported with full detail. The investigation remains evidence-driven rather than hypothesis-driven.*
