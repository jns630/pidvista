# Vista PKEY2005 Public Subgroup and Pairing-Reference Audit

## Scope

This report extends the public-data checks for the 14 PKEY2005 public-key groups in the supplied Vista XrML configuration. It checks scalar-order membership of the serialized twist points and target-subgroup membership of the serialized pairing reference.

It does not parse product keys, recover discrete logarithms or private coefficients, reproduce signature generation, or verify a product-key signature.

Input SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

## 1. Point order

The common declared curve order is:

`m = 0x2bb38c9b1d8a3b1846f701ad79ef`

An independent exact primality test reports that (m) is prime.

The preceding point audit found that all 196 serialized points satisfy the documented twist-curve equation and that scalar multiplication by (m) sends every point to infinity. This audit additionally confirmed that none of the serialized affine points is the point at infinity (all have nonzero affine coordinate data).

Because (m) is prime, every non-identity point annihilated by (m) has exact order (m). Therefore all 196 points have exact order (m), not merely order dividing (m).

| Group | Exact-order points |
|---:|---:|
| 140 | 14/14 |
| 142 | 14/14 |
| 144 | 14/14 |
| 146 | 14/14 |
| 148 | 14/14 |
| 150 | 14/14 |
| 152 | 14/14 |
| 154 | 14/14 |
| 156 | 14/14 |
| 158 | 14/14 |
| 160 | 14/14 |
| 162 | 14/14 |
| 164 | 14/14 |
| 166 | 14/14 |
| **Total** | **196/196** |

## 2. Pairing-reference decoding and target subgroup

The public-key format describes the pairing reference as an extension-field element with six base-field coefficients. The extension tower is:

- (K_3=mathbb F_p[u]/(u^3+u+4))
- (K_6=K_3[t]/(t^2+2))

The six serialized 14-byte little-endian limbs were interpreted in the documented coefficient order as:

[
c=(z_0+z_1u+z_2u^2)+(z_3+z_4u+z_5u^2)t.
]

The arithmetic check used (u^3=-u-4) and (t^2=-2), reducing all coefficients modulo (p). For each public-key group it checked:

1. all six coefficients are in the canonical range ([0,p-1]);
2. the decoded element is nonzero;
3. exponentiation by (m) in (K_6) gives the multiplicative identity.

**Result: 14/14 pairing references passed all three checks.**

The earlier inconclusive result was caused by an incorrect coefficient/basis interpretation in the preliminary test. Under the coefficient ordering above, every reference satisfies (c^m=1).

This proves target-subgroup membership for the decoded field element. It does not independently recompute the Tate pairing from the hidden pairing input points (P,S).

## 3. Independence: what can and cannot be concluded

The public PKEY2005 write-up describes the points (Q_i) as generated from one generator (P), with (Q_i=alpha_iP). Under that documented construction, the points are scalar multiples of the same order-(m) generator and therefore are not intended to be linearly independent as a set of 14 points in the (m)-torsion group.

No discrete logarithms (alpha_i) were computed here. The audit makes no claim about their values.

## 4. Consolidated outcome

| Property | Result |
|---|---:|
| Twist-curve equation | 196/196 pass |
| Scalar annihilation ([m]Q_i'=O) | 196/196 pass |
| Exact point order (m) | 196/196 pass |
| Pairing-reference coefficients canonical | 14/14 pass |
| Pairing references nonzero | 14/14 pass |
| Pairing references satisfy (c^m=1) | 14/14 pass |

## 5. Limitations

These checks establish strong mathematical consistency of the public points and stored target-group elements. They do not establish that a product key is valid, entitled, or activatable, and they do not constitute complete PKEY2005 signature verification.

The point scalar-multiplication and pairing-field exponentiation checks were executed locally against the supplied XrML file. The earlier curve-membership result was also independently computed locally. The GitHub copy of the earlier checker was not fetched and rerun during this session.

## Reference

The public format description documents the six-coefficient extension-field serialization, the twist representation, and the stored value (c=e_m(P,S)):

- https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
