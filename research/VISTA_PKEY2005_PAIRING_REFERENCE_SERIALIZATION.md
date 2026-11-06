# PKEY2005 Pairing-Reference Serialization: What Is Established

## Purpose

This note resolves the documented byte-to-field-element serialization convention for the stored pairing reference, while separating that result from the still-unresolved target-subgroup arithmetic test.

This is a public-format analysis only. It does not recover private signing data, derive signatures, or generate product keys.

## Public format facts

The PKEY2005 public-key layout declares the final region as:

`pairing_val[ext_deg1 * ext_deg2]`

Each entry is a little-endian base-field bignum of `size_bignum` bytes. In the supplied Vista configuration:

- `ext_deg1 = 3`
- `ext_deg2 = 2`
- `size_bignum = 14`
- the pairing-reference region is therefore (3\times2\times14=84) bytes.

The public write-up states that extension-field elements are serialized as base-field coefficients in polynomial-basis order:
[
z_0+z_1u+z_2u^2+\cdots+z_{n-1}u^{n-1}.
]

The supplied field tower is:
[
K_3=\mathbb F_p[u]/(u^3+u+4),\qquad
K_6=K_3[t]/(t^2+2).
]

Consequently, the documented six-coefficient interpretation is:
[
c=(z_0+z_1u+z_2u^2)+(z_3+z_4u+z_5u^2)t.
]

The coefficient sequence is therefore ((z_0,z_1,z_2,z_3,z_4,z_5)), each encoded as a 14-byte little-endian integer.

## What this resolves

The serialization convention is supported by the public format description. It is not appropriate to treat the six 14-byte values as an arbitrary unordered collection or reverse their order without evidence.

For the supplied file, earlier local inspection established that all six limbs in each of the 14 pairing-reference records are canonical base-field values ((0\le z_i<p)) and that no decoded six-limb vector is all zero.

## What remains unresolved

A prior preliminary implementation of the exponentiation test (c^m=1), using the natural tower basis above, did not pass. The public write-up's serialization statement alone does not explain that discrepancy.

Before asserting target-subgroup membership, an independent implementation must validate all of the following against known field identities and test vectors:

1. The cubic reduction relation (u^3=-u-4).
2. The quadratic reduction relation (t^2=-2).
3. The mapping of the six serialized limbs to the six basis elements shown above.
4. Multiplication and exponentiation in (K_6), including reduction at both extension levels.
5. The expected target-group order and the exact pairing convention used by the implementation.

Until those checks are independently reproduced, the result of (c^m=1) is **unresolved**. Do not cite the earlier unverified claim that all 14 pairing references passed this test.

## Safe next validation work

A standalone field-arithmetic test suite can validate the tower implementation without using product keys or attempting signature generation. Useful tests include:

- additive and multiplicative identities;
- commutativity and associativity on deterministic sample elements;
- distributivity;
- (t^2=-2);
- (u^3=-u-4);
- coefficient round-trip serialization;
- Fermat identity (x^{p^6-1}=1) for sampled nonzero (x\in K_6), once the extension is established as a field.

These tests validate the arithmetic engine, not the correctness of a stored pairing reference. A final target-subgroup check should only be reported after the field arithmetic and target-group assumptions have independent test coverage.

## References

- UMSKT PKEY2005 public-key format and extension-field serialization: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- UMSKT PKEY2005 verification overview: https://git.enderman.ch/UMSKT/writeups/src/commit/edb97ef881826bc2fa5715d06568abff11222e32/PKEY2005.md

This note records what the public documentation supports and deliberately leaves the failed exponentiation check open.
