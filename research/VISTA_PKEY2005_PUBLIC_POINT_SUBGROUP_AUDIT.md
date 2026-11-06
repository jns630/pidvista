# Vista PKEY2005 Public-Point Subgroup Membership Audit

## Scope

This audit checks only public parameters serialized in the supplied Vista PKEY configuration file. It does not inspect product keys, derive private signing material, recover H1 coefficients, or generate signatures.

Input file SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The three supplied XrML copies were byte-identical.

## Method

The public-key records provide the base-field modulus (p), the declared curve order (m), the cubic extension polynomial (u^3+u+4), the quadratic extension polynomial (t^2+2), the base curve coefficients (a,b), and 14 serialized points per group.

The stored points are documented as points on the quadratic twist over (K_3). With (d=t^2=-2), the twist equation used was:

[
y'^2=x'^3+d^2ax'+d^3b.
]

For each point, the checker performed two distinct tests:

1. Verify the twist-curve equation in (K_3=mathbb F_p[u]/(u^3+u+4)).
2. Compute scalar multiplication ([m]Q'_i) on that twist curve using Jacobian coordinates and check whether the result is the point at infinity.

The second test checks that each point is annihilated by the declared order (m). It is a public-data group-membership check, not a signature verification.

## Results

| Public-key group | Curve equation | ([m]Q'_i=O) |
|---:|---:|---:|
| 140 | 14/14 | 14/14 |
| 142 | 14/14 | 14/14 |
| 144 | 14/14 | 14/14 |
| 146 | 14/14 | 14/14 |
| 148 | 14/14 | 14/14 |
| 150 | 14/14 | 14/14 |
| 152 | 14/14 | 14/14 |
| 154 | 14/14 | 14/14 |
| 156 | 14/14 | 14/14 |
| 158 | 14/14 | 14/14 |
| 160 | 14/14 | 14/14 |
| 162 | 14/14 | 14/14 |
| 164 | 14/14 | 14/14 |
| 166 | 14/14 | 14/14 |
| **Total** | **196/196** | **196/196** |

All 196 points passed both tests. The scalar multiplication result was infinity for every point.

## Pairing-reference inspection: unresolved

The serialized pairing-reference region is 84 bytes per public-key record, corresponding to six 14-byte base-field coefficients under the documented extension-field serialization. For all 14 records:

- all six coefficients were less than (p);
- the decoded value was nonzero;
- the decoded value was not the multiplicative identity.

A preliminary exponentiation test using the natural (K_6=K_3[t]/(t^2+2)) coefficient interpretation did **not** establish (c^m=1) for any record. This is an unresolved result. It may indicate an incorrect interpretation of the pairing-field basis, a field-arithmetic or serialization assumption that needs further confirmation, or another detail not captured by the public write-up. It is not evidence that the stored references are invalid.

No claim of pairing-reference validity is made in this audit.

## Interpretation and limitations

The results establish that, for this input file and the documented twist equation, every serialized public point lies on the twist curve and is annihilated by the declared scalar (m).

They do not establish:

- that each point has exact order (m), rather than an order dividing (m);
- that the points are independent or form a particular basis;
- that the pairing references are correctly decoded or valid;
- that any product key is valid, entitled, or activatable;
- that the complete PKEY2005 signature-verification procedure has been reproduced.

The computation was executed locally against the supplied XrML file. The committed point-curve checker was not fetched and rerun from GitHub during this audit session; the subgroup calculation was an additional local computation.

## External technical reference

The UMSKT PKEY2005 write-up documents the public-key layout, extension-field coefficient serialization, twist representation, and the stored Tate-pairing reference:

- https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md

This report is a structural and mathematical consistency audit of public data only.
