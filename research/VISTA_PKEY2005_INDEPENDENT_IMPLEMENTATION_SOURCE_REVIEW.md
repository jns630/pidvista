# PKEY2005 Independent Implementation Source Review

## Objective

Look for a public, independently checkable known-answer test vector for the PKEY2005 pairing reference, suitable for validating the field and pairing arithmetic without relying on the same implementation assumptions.

## Sources reviewed

### UMSKT PKEY2005 write-up

The UMSKT write-up describes the public-key serialization, the field tower, the polynomial-basis encoding, and the high-level verification relation. It explains that the stored value is (c=e_m(P,S)), while the public-key blob contains the curve parameters, extension polynomials, radices, twist points, and stored reference value.

The write-up does not supply a complete known-answer test vector containing both pairing input points, the precise pairing normalization/convention, and the expected output. It also describes unresolved implementation details in the PKEY2005 validation process.

### laomms/PKey2005Decoder

The public project documentation describes a decoder workflow that parses public-key data, calculates Tate-pairing-derived values for the public twist points, and compares combinations against the stored pairing reference.

This is useful evidence that another implementation path exists, but it is not a clean known-answer fixture. Its stated purpose is product-key decoding and its workflow includes a meet-in-the-middle search. Therefore, its results should not be presented as an independent pairing test vector or as proof of the correctness of a separately written pairing implementation.

No decoding, search, or private-parameter recovery procedure was imported into this repository.

## Result

No independently checkable PKEY2005 pairing known-answer vector was identified in the sources reviewed.

The following distinction is retained:

- **Documented:** public field and point serialization conventions, and the high-level pairing verification relation.
- **Tested separately:** finite-field arithmetic identities for the documented tower.
- **Not independently validated:** the 14 stored pairing-reference values and their target-subgroup order.

## Evidence needed to close the gap

A suitable fixture would need to disclose:

1. both pairing input points in an unambiguous coordinate representation;
2. the exact curve, field tower, and subgroup order;
3. the precise Tate-pairing variant, argument order, divisor/denominator treatment, and final exponentiation;
4. the expected result as six canonical base-field coefficients;
5. a provenance independent of the implementation being tested.

A generic Tate-pairing test over a small unrelated curve can validate a pairing library's generic implementation, but cannot by itself establish that the PKEY2005-specific tower, twist mapping, and stored pairing convention are correctly reproduced.

## Scope

This review is verification-only. It does not recover private signing material, derive new signatures, or generate product keys.

## References

- UMSKT PKEY2005 write-up: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- PKey2005Decoder public project: https://github.com/laomms/PKey2005Decoder
