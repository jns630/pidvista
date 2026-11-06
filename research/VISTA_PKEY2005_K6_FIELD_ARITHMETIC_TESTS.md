# PKEY2005 K6 Field-Arithmetic Test Report

## Scope

An independent, verification-only arithmetic test was added for the public field tower described in the PKEY2005 write-up. It uses only public field parameters:

- (p=886368969471450739924935101400677)
- (m=\texttt{0x2bb38c9b1d8a3b1846f701ad79ef})
- (K_3=\mathbb F_p[u]/(u^3+u+4))
- (K_6=K_3[t]/(t^2+2))

The test code does not parse product keys, compute a Tate pairing, generate signatures, recover private parameters, or activate Windows.

## Test outcome

The reproducible script completed successfully after correcting two implementation mistakes found during development.

- The base-field test confirms that (-2) is a nonsquare in (mathbb F_p).
- The cubic polynomial (u^3+u+4) passes the degree-three Rabin irreducibility criterion.
- The tower relations (u^3=-u-4) and (t^2=-2) pass.
- Eight deterministic sample elements passed multiplicative identity, inverse, and (x^{p^6-1}=1) checks.
- Deterministic samples passed commutativity, associativity, and distributivity checks.

Command:

```sh
python vista_pkey2005_k6_field_tests.py
```

Expected output begins with:

```
PASS: base-field nonsquare test and cubic irreducibility criterion
PASS: K6 identities, inverses, Fermat, commutativity,
      associativity, distributivity, and both tower relations
```

## Development corrections recorded

The initial local implementation contained two sign/coefficient placement errors when reducing (u^3) and (u^4). The explicit generator-relation test caught the first issue; inverse tests then exposed the remaining reduction error. Both were corrected before the successful run. This is why the generator identities and inverse tests are retained in the script.

## Interpretation and limits

This validates the tested arithmetic implementation for the documented tower, subject to the public parameters and test coverage described above. It does **not** prove that any of the 14 serialized pairing references has order (m), that a pairing value was serialized with a different convention, or that a product key or signature is valid.

The next safe validation step is a separately sourced, independently checkable test vector for the extension-field representation or pairing output. Without such a vector, any pairing-reference order result should remain labelled unverified.

## Source

The public PKEY2005 write-up describes little-endian bignums, the extension-field polynomial basis, the field tower, and the stored pairing reference: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
