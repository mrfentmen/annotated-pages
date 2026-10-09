# Liber Primus Visual Geometry — Findings Report
**Date:** 2026-10-09 (ninth report)  
**Experiment:** Independent re-implementation of the φ(pₙ) % 29 decipherment on the page that carries the primary five-dot (page 73 / 56.jpg)  
**Previous:** [2026-10-09_correlation_E3.md](./2026-10-09_correlation_E3.md)  
**Repository:** mrfentmen/annotated-pages

---

## 1. Objective

Fully re-implement the published solution method for the 56–73 block  
(`nth letter’s shift = φ(nth prime) % 29`, shift down, forward Gematria, cleartext-F skip)  
and inspect the resulting plaintext for any reference to geometry, dots, orientation, or visual markers.

---

## 2. Method

- Gematria Primus alphabet (29 runes):  
  `ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ`
- Keystream: consecutive primes pᵢ; shiftᵢ = (pᵢ − 1) mod 29  (= φ(pᵢ) mod 29).
- Decryption: for each consuming rune, plaintext = (ciphertext − shift) mod 29.
- Non-rune characters (hex digits, punctuation, newlines) do not consume keystream symbols.
- Two variants tested: advance keystream on every rune, and skip advance when recovered plaintext is F.

Ciphertext source: canonical form from scream314/cicada3301 and Boxentriq documentation.

---

## 3. Resulting plaintext

```
AN END
WITHIN THE DEEP WEB
THERE EXISTS A PAGE THAT HASHES TO
36367763ab73783c7af284446c
59466b4cd653239a311cb7116
d4618dee09a8425893dc7500b
464fdaf1672d7bef5e891c6e227
4568926a49fb4f45132c2a8b4
IT IS THE DUTY OF EVERY PILGRIM TO SEEK OUT THIS PAGE
```

(Final line orthography in community sources appears as “EUERY” / “PILGRIM”; the first three lines and the hash recover exactly.)

This matches the long-published solution of the “An End” page.

---

## 4. Relevance to the geometric investigation

The plaintext of the only known-method page that carries the primary five-dot template is:

- A short declarative message about a deep-web page whose SHA-512 begins with the given hex string.
- An instruction that it is the duty of every pilgrim to seek that page.

**There is no reference to dots, five-point figures, orientation, reflection, rotation, page geometry, or any visual marker.**

Consequently:

- The presence of the five-dot on this page does not appear to be “explained” or indexed by the text itself.
- The text does not supply a reading rule, key, or transformation instruction that would make the geometric recurrence on pages 24/40/73 cryptographically functional.

---

## 5. Updated correlation status

| Hypothesis | Status |
|------------|--------|
| Five-dot marks unsolved pages | Rejected (E1) |
| Simple page-number arithmetic selects the set | Unsupported (E1) |
| Five-dot is a general end-of-known-method-section marker | Rejected (E3) |
| Five-dot on page 73 is referenced or explained by that page’s plaintext | **Rejected (this report)** |
| Five-dot is a high-precision decorative / structural reuse with no demonstrated textual function | Still the most economical description consistent with all evidence |

---

## 6. Conclusion for Experiment E (so far)

After geometric confirmation, statistical null tests, and three rounds of correlation work (including a full independent decipherment of the only solved page that carries the motif), **no robust textual function for the isolated five-dot template has been found**.

The motif remains:
- Geometrically distinctive (residuals ≪ 0.25 px, P ≈ 0 under multiple nulls),
- Reused with exacting fidelity across pages 24, 40 and 73,
- Unexplained by the solved text that shares a page with it.

Further progress on a cryptographic role would require either new positive evidence or a different class of test (e.g. treating the five points as indices into a larger key stream, or correlating orientation with properties of still-unsolved pages). Until such evidence appears, the five-dot stands as a confirmed, high-precision visual constant of *Liber Primus* whose purpose, if any, is not yet demonstrated.

---

*Independent re-implementation confirms the published plaintext; that plaintext contains nothing that illuminates the geometry.*
