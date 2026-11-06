# PKEY2005 Pairing Known-Answer Vector Search

## Finding

The public PKEY2005 write-up documents the serialized public-key layout and the polynomial-basis encoding of extension-field elements. It states that the final 84-byte region stores six little-endian base-field coefficients for the pairing reference (c=e_m(P,S)).

The write-up does **not** provide a known-answer pairing test vector consisting of independently known input points, a complete pairing convention, and an expected output that can be used to validate a fresh implementation end-to-end.

The serialized public key itself supplies the public curve and field parameters, the compressed twist-point vector, and the reference pairing value. It does not serialize the generator (P) and signature base point (S) as direct pairing inputs. The write-up explicitly notes that the reference value is stored instead of those points.

## What has been independently checked

The six-limb interpretation follows the documented polynomial basis:
[
(z_0+z_1u+z_2u^2)+(z_3+z_4u+z_5u^2)t.
]

The finite-field arithmetic implementation was separately exercised in this session using deterministic sample elements. Multiplicative inverses, the (p^6-1) exponent identity, associativity, and distributivity passed. These tests validate arithmetic operations on samples; they are not pairing known-answer tests.

## What is still not established

- No independent known-answer Tate-pairing vector was found in the cited public write-up.
- No independently sourced (P,S) pair and expected (e_m(P,S)) value was found.
- The 14 stored pairing references have not been shown to satisfy (c^m=1) by an independently validated implementation.
- The existence of six canonical, nonzero coefficients does not establish target-subgroup membership.

## Next evidence required

A sound end-to-end pairing check needs a public known-answer vector specifying:

1. the exact base field and both extension polynomials;
2. the curve and subgroup order;
3. the two input points, including their field and twist representation;
4. the pairing variant, argument order, normalization, and final exponentiation convention;
5. the expected six-coefficient output in the documented serialization order.

Without those items, a result from a locally written pairing routine would be circular: the same assumptions under test would define both the implementation and its expected interpretation.

## Scope

This is verification-only research. It does not attempt to recover private signing parameters, produce signatures, or generate product keys.

## References

- UMSKT PKEY2005 public-key binary format and verification discussion: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- UMSKT PKEY2005 validation overview: https://git.enderman.ch/UMSKT/writeups/src/commit/4d5de36e804f820321d2780a0b1acc0120adf606/PKEY2005.md
