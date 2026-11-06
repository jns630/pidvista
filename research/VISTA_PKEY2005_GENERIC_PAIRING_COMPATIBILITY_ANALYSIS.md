# PKEY2005 Compatibility Analysis Against the Generic Tate-Pairing Fixture

## Purpose

This report compares the independently reproduced Stanford toy Tate-pairing fixture with the public PKEY2005 field and twist descriptions. It defines a verification-only compatibility boundary and records which assumptions can and cannot be carried from the toy fixture into PKEY2005.

## 1. What the generic fixture establishes

The Stanford dissertation example provides a complete known-answer test over a small field:

- Base field: (mathbb F_{59})
- Extension: (mathbb F_{59}[i]/(i^2+1))
- Curve: (y^2=x^3+x)
- Subgroup order: (5)
- Published Miller intermediates and final pairing output

The repository test `tate_pairing_stanford_2007_kat.py` reproduces those published values. This is evidence that its small-field extension arithmetic and the specific published Miller/final-exponentiation calculation are internally consistent with that example.

It does not establish PKEY2005's curve, twist, field representation, or pairing normalization.

## 2. PKEY2005 public model

The public PKEY2005 write-up describes:

- (K=mathbb F_p)
- (K_3=K[u]/(u^3+u+4))
- (K_6=K_3[t]/(t^2+2))
- Curve (E:y^2=x^3+ax+b)
- A quadratic twist represented over (K_3)
- A stored pairing reference (c=e_m(P,S))

The public write-up states that the stored twist points are represented over (K_3), while the untwisted points used for pairing are in the larger field. Its stated map is:
[
d=t^2,qquad E': y^2=x^3+d^2ax+d^3b,
]
[
	au(x,y)=(t^{-2}x,t^{-3}y).
]

The separate public PKey2005Decoder project describes the same tower and a Tate-pairing computation over (K_6), including final exponentiation and an explanation for omitting Miller denominators that lie in the proper subfield. That is useful corroboration of the broad model, but it is not a known-answer pairing fixture.

## 3. Compatibility matrix

| Area | Generic Stanford fixture | PKEY2005 | Transfer status |
|---|---|---|---|
| Finite-field arithmetic | (mathbb F_{59^2}) | (mathbb F_{p^6}) tower | Concepts transfer; parameters do not |
| Polynomial basis | (1,i) | (1,u,u^2,t,ut,u^2t) | Same principle; different tower |
| Curve | (y^2=x^3+x) | (y^2=x^3+ax+b) | Generic curve formulas transfer |
| Subgroup order | (5) | Public (m), 110-bit value | No numeric transfer |
| Twist | Not the PKEY2005 (K_3/K_6) twist | Quadratic twist over (K_3) | Must be checked separately |
| Miller evaluation | Published toy example | PKEY-specific convention not fully pinned down | No direct equivalence claim |
| Final exponentiation | ((59^2-1)/5) | Depends on PKEY pairing order and convention | Formula pattern transfers, exponent does not |
| Output serialization | Two coefficients | Six 14-byte coefficients | Encoding convention documented; implementation still needs validation |

## 4. PKEY-specific checks still required

The following checks are prerequisites for any future claim that a PKEY2005 pairing implementation is compatible with the public format:

1. **Field tower:** verify the polynomial reductions and coefficient ordering against the public definitions.
2. **Twist curve:** verify the supplied twist coefficients are exactly (d^2a) and (d^3b), with (d=t^2=-2).
3. **Untwist map:** verify that the stated map sends points on the stated twist curve to points on (E/K_6). This should be tested symbolically and with independently supplied points.
4. **Point representation:** establish the exact coordinate interpretation of each 84-byte point block, including coefficient order and canonical range.
5. **Pairing convention:** establish argument order, Miller function convention, denominator treatment, and final exponent from a PKEY-specific independent fixture.
6. **Pairing serialization:** compare a known six-coefficient output with the stored 84-byte convention.

The toy Stanford fixture covers none of the PKEY-specific twist or point-decoding checks.

## 5. Why no PKEY pairing result is claimed

The public materials do not provide a clean, independently checkable PKEY2005 known-answer vector with all pairing inputs, convention details, and expected six-coefficient output.

The separate decoder project is useful as a second public description of the implementation model, but its documented pairing calculations are embedded in a product-key decoding workflow. Its output is not treated here as an independent known-answer vector.

Accordingly, the status of (c^m=1) for the 14 stored pairing references remains **unverified**. Canonical, nonzero coefficients and successful generic toy pairing tests are not substitutes for that check.

## 6. Verification-only boundary

This repository's current work is limited to public-format parsing, public parameter checks, field-arithmetic tests, and independent generic test fixtures. This report does not add product-key parsing, signature construction, H1 recovery, meet-in-the-middle search, private-parameter recovery, or key-generation functionality.

## Sources

- UMSKT PKEY2005 validation write-up: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- PKey2005Decoder public project: https://github.com/laomms/PKey2005Decoder
- Stanford, Ben Lynn, *On the Implementation of Pairing-Based Cryptosystems*: https://crypto.stanford.edu/pbc/thesis.pdf
- Pairing-based cryptography background, *Scaling security in pairing-based protocols*: https://eprint.iacr.org/2005/139.pdf
