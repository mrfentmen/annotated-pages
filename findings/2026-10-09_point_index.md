# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (twelfth report)  
**Experiment:** 3 — Point-index hypothesis  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Test whether the five points of the primary template (pages 24 / 40 / 73), ordered by rigid-fit correspondence or by spatial sort, function as **indices or shifts** into a local or global rune stream, producing readable plaintext.

---

## 2. Setup

**Reference geometry (page 24 centroids):**
```
P0 (796.9, 3105.8)
P1 (992.5, 3166.6)
P2 (1479.3, 3127.5)
P3 (1527.2, 2936.2)
P4 (1296.9, 2866.8)
```

**Correspondences (from prior rigid fits):**
- 24 → 40 (vertical flip): permutation (0,1,4,3,2), RMS 0.031 px  
- 24 → 73 (horizontal flip): permutation (4,3,2,0,1), RMS 0.206 px  

**Rune streams used:**
- Page-24 block (multi-page range ending at 24): 329 clean Gematria Primus runes  
- Page-73 / “An End” block: 82 clean runes (known plaintext after φ(pₙ)%29)

**Orderings tested:** x-ascending, y-ascending, y-descending, reference 0–4, fit-derived permutation.

---

## 3. Schemes tested

| ID | Scheme | Description |
|----|--------|-------------|
| A  | Rank indices | Point ranks (x or y) mapped into stream positions |
| B  | Normalised position indices | Continuous x/y/sum coordinates scaled to stream length |
| C  | Point-derived shifts | Normalised x or y → shift values 0–28 applied as running Gematria subtract |
| D  | Distance-derived step | Pairwise distances → step size; take every k-th rune |
| E  | Pixel mod 29 | Raw integer coordinates and deltas taken mod 29 as Gematria values |
| F  | Aggregate mod 29 | Sum of x, sum of y, centroid coordinates mod 29 |

---

## 4. Results (summary)

**Schemes A–B (index selection)**  
Five-rune extractions produced short strings such as:
`AMXGM`, `XMAGM`, `MGAMX`, `AOEEEAEO`, `LEATLA`, `ALEALL`  
None are English words or known Cicada key phrases (DIVINITY, PRIMUS, INSTAR, etc.).

**Scheme C (shifts)**  
Longer decrypt fragments, e.g.:
- `ANBEFGLEEAEOEAEOFGGXYSEATAENEATHHNHJW`
- `THBMJMPEALJXMWXOEAEPOEEAHEDRJINGINGSBIRY`  
No readable English spans beyond chance letter groups.

**Scheme D (step sampling)**  
Examples: `AGEOGTHJROUAETHSJYLJFLU`, `ATOSJEOAAIAHCTHPUTHIAE`  
No plaintext.

**Scheme E (coord mod 29)**  
```
X as runes: XGFMING
Y as runes: OGAEWAE
X+Y mod29:  BEOAEYB
X−Y mod29:  JFREOAE
```
Consecutive L→R deltas mod 29: `OE, O, X, M, H, F, M, EO` — no word.

**Scheme F (aggregates)**  
Sum-x ≡ 3, sum-y ≡ 7, centroid ≡ (1, 25) mod 29 — single symbols, not a message.

---

## 5. Interpretation

Under a broad but well-defined family of index and shift constructions that use the five-point geometry as the sole source of positions or key material, **no readable plaintext is recovered**.

This does not prove that no indexing scheme exists; it shows that the most direct and commonly tried mappings (rank, normalised coordinate, mod-29, inter-point distance) fail to unlock the local rune streams associated with the three pages that carry the template.

The negative result is consistent with earlier correlation findings: the geometry is real and extreme, yet has not so far been shown to function as a straightforward key or index into the text.

---

## 6. Limitations & possible extensions

- Only local page-range streams were used; a global concatenation of all Liber Primus runes was not tested.  
- More exotic orderings (convex-hull order, angle from centroid, etc.) were not exhausted.  
- The points were not used as a 5-element permutation applied to blocks of 5 runes (a separate, smaller experiment).  
- No deep search over affine transformations of the coordinates before indexing was performed.

Any of the above could be run as a follow-up if desired; none are strongly motivated by prior positive evidence.

---

## 7. Status of the point-index hypothesis

**Not supported** by the schemes tested.  
The primary five-dot template remains a confirmed geometric constant without a demonstrated cryptographic indexing function.

---

*Negative results reported with the same completeness as positive geometric measurements.*
