# PKEY2005 public-parameter sanity audit

## Scope and input

This audit ran the read-only public-parameter checker against the supplied
`pkeyconfig(1).xrm-ms` file:

- Size: 620,662 bytes
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Public-key records examined: 14
- Groups: 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166

The check is intentionally limited to public parameters. It does not decode
product keys, recover H1 vectors, solve discrete logarithms, construct
signatures, or verify a Tate pairing.

## Results

All 14 records passed every implemented sanity check. The public field and
curve parameters were identical across the 14 groups.

| Check | Result |
|---|---|
| Base-field modulus probable-prime test | Pass, all groups |
| Curve-order probable-prime test | Pass, all groups |
| H1 radix values below modulus | Pass, all groups |
| Extension polynomial expected degree and nonzero leading coefficient | Pass, all groups |
| Extension polynomial coefficients below modulus | Pass, all groups |
| Elliptic-curve discriminant nonzero modulo p | Pass, all groups |
| Stored max-quotient byte matches documented relation | Pass, all groups |
| Base-curve coefficients are zero | Pass, all groups |
| Required zero byte and serialized point/pairing bounds | Pass, all groups |

The common base-field modulus is:

`0x2bb38c9b1d8a3b820c6524544665`

The common curve order is:

`0x2bb38c9b1d8a3b1846f701ad79ef`

Both are 110-bit values. The stored max-quotient byte is 35, matching
`floor(24^25 / p) - 1`. The curve discriminant
`4a^3 + 27b^2 mod p` is nonzero.

The public write-up defines the base curve as `y^2 = x^3 + ax + b`, and
describes the two extension polynomials as low-to-high coefficient arrays.
The checker verifies their lengths, leading coefficients, and coefficient
ranges; it does not claim an irreducibility proof.

## Important field-name correction

The published ImHex layout names the 32-bit word at field-data relative offset
`0x1f` as `offset_modulus`. It is distinct from `size_modulus`, which
determines the point count. In this supplied data both values happen to be 14.
The checker keeps these fields separate.

## Limits and next test

These results establish basic consistency of the shared public field
parameters, not mathematical validity of the serialized point vector. A
point-membership test requires fully confirmed conventions for the cubic and
quadratic extensions and the twist representation. The UMSKT write-up
describes the point untwist and pairing verification model, while noting
PKEY2005-specific unknowns remain.

The next safe validation step is to independently confirm extension-field
irreducibility and point-decoding conventions, then test public-point
membership without attempting any private-scalar recovery or signature
generation.

## Reproduction

```sh
python vista_pkey2005_public_parameter_sanity.py pkeyconfig.xrm-ms -o parameter-sanity.json
```

The primality checks use fixed-base Miller-Rabin tests. They are probable-prime
checks, not formal primality certificates. Polynomial degree checks do not
prove irreducibility.

## References

- UMSKT, [PKEY2005 Validation](https://git.enderman.ch/UMSKT/writeups/src/commit/5e9c37af411e8a3b5491ff2505c6e79abd3ea8f1/PKEY2005.md),
  especially the public-key field layout and verification sections.
