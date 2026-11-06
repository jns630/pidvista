# Vista PKEY2005 signature-verification readiness

## Purpose and status

This note separates what the supplied Vista public-key records establish from
what is still required for an independent cryptographic verification result.
The repository's current parser is a structural inspector. It does not claim
to verify a product-key signature.

**Status: public format substantially mapped; independent signature
verification not completed.** No signature pass/fail result is claimed.

## Publicly documented verification model

The public UMSKT PKEY2005 write-up describes the high-level pairing check:

1. Decode the product-key payload to an integer `HASH(M)` using the
   PKEY2005 base-24 alphabet.
2. Derive the message vector `v = H1(M)` and the curve point
   `T = H2(M)`.
3. Form `Q = sum(v_i * Q_i)` from the public point vector.
4. Compute the order-`m` Tate pairing `e_m(Q, T)`.
5. Compare it with the stored reference pairing `c = e_m(P, S)`.
6. A match is the documented cryptographic acceptance condition.

The serialized public key stores the `Q_i'` point vector and the reference
pairing value, rather than exposing the private vector or the original
`P, S` pair. The stored point entries are represented over the cubic
extension and require the documented untwist operation before use in the
pairing calculation.

This is a description of the public verification model, not a working
implementation in this repository.

## Mapping to the supplied 1,579-byte records

Based on the published ImHex layout and the byte-boundary audit of the
supplied configuration:

| Region | Absolute offsets | Meaning |
|---|---:|---|
| Outer header | 0–11 | Magic, version, field-data length |
| Field data | 12–318 | Field and hash parameters |
| Point vector | 319–1494 | `size_modulus` compressed `Q_i'` entries |
| Pairing reference | 1495–1578 | `ext_deg1 * ext_deg2` limbs |

For this supplied file, `size_modulus = 14`, `ext_deg1 = 3`,
`ext_deg2 = 2`, and each bignum is 14 bytes. Therefore each point occupies
six bignums (84 bytes), and the pairing reference occupies six bignums
(84 bytes).

**Field-map correction:** the 32-bit word at field-data relative offset
`0x1f` is named `offset_modulus` in the published layout. It is not the
point count. The point count is derived from `size_modulus`. Both values
happen to be 14 in the supplied records, which concealed the earlier parser
labeling error. The parser now reports these separately.

## What remains unresolved for a reproducible verifier

The public write-up explicitly describes parts of PKEY2005 as incompletely
reverse-engineered. The following items prevent this repository from making
an independent cryptographic pass/fail claim:

- The exact product-key `HASH(M)` derivation is not established by the
  public-key blob. Base-24 decoding is only a payload conversion step.
- The exact `H1(M)` vector recovery and all implementation details needed
  to reproduce the required vector must be independently confirmed.
- `H2(M)` includes a point-lifting/sign choice whose selection mechanism is
  described as unknown in the cited write-up.
- The extension-field representation, polynomial conventions, point
  validation, twist/untwist mapping, and Tate-pairing implementation must
  agree byte-for-byte and mathematically with the target implementation.
- A trustworthy, independently obtained known-good test vector is needed:
  a key sample, the matching exact public-key group/configuration, and an
  authoritative expected verification outcome. A local PidGenX HRESULT alone
  is not a published pairing test vector.

The structural parser checks record framing and boundaries. It does not prove
that the field values form valid finite fields, that every point lies on the
expected curve, or that a pairing comparison succeeds.

## Safe validation plan

The next defensible engineering steps are:

1. Keep the structural parser and its regression checks independent from
   product-key processing.
2. Add finite-field and curve-parameter sanity checks over public parameters
   only, without attempting to solve for private scalars.
3. Add point-decoding and on-curve checks for the public point vector, with
   explicit tests for malformed lengths, out-of-range coordinates, and
   invalid points.
4. Implement the published extension-field and pairing operations only as a
   verification component, and only test it against independently sourced
   public test vectors with documented expected outcomes.
5. Compare local diagnostic observations with the independent result while
   keeping the meanings separate: local PidGenX processing, cryptographic
   signature validity, licence entitlement, and activation are distinct.

No private signing vector, private scalar, or signing operation is part of
this plan. The repository remains read-only with respect to licensing
configuration and does not generate product keys or signatures.

## References

- UMSKT, [PKEY2005 Validation](https://git.enderman.ch/UMSKT/writeups/src/commit/5e9c37af411e8a3b5491ff2505c6e79abd3ea8f1/PKEY2005.md),
  especially the public-key layout and verification sections.
- Microsoft, [Certificates and Public Keys](https://learn.microsoft.com/en-us/windows/win32/seccrypto/certificates-and-public-keys),
  for the general distinction between public verification material and
  private signing material.
