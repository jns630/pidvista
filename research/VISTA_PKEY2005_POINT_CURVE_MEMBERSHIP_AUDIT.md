# PKEY2005 public-point twisted-curve membership audit

## Scope

This audit tests whether each serialized public point satisfies the
documented quadratic-twist curve equation over the cubic extension field.
It uses only public parameters and public-key records from the supplied
Vista configuration. It does not parse product keys, recover H1, solve
private discrete logarithms, generate signatures, or verify Tate pairings.

Input:
- File: `pkeyconfig(1).xrm-ms`
- Size: 620,662 bytes
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Groups: 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166

## Extension-field model

The signed low-to-high polynomial coefficients in the first record are:

- `F1 = [4, 1, 0, 1]`, i.e. (u^3 + u + 4)
- `F2 = [2, 0, 1]`, i.e. (t^2 + 2)

Thus:
- (K_3 = mathbb{F}_p[u]/(u^3+u+4))
- (K_6 = K_3[t]/(t^2+2))
- (t^2 = d = -2)

The cubic is irreducible over the base field: a cubic is reducible over a
field exactly when it has a root, and the polynomial gcd test for
(gcd(u^3+u+4,u^p-u)) has degree zero beyond constants (equivalently,
the cubic is coprime to (u^p-u)). The quadratic is irreducible over
(K_3): (p equiv 5 pmod 8), so (-2) is a nonsquare in (mathbb F_p);
because the extension degree (3) is odd, it remains a nonsquare in
(mathbb F_{p^3}).

The source describes the public points as points on the twisted curve and
gives the untwist map ((x,y) mapsto (t^{-2}x,t^{-3}y)). The corresponding
twisted-curve equation is:

[
y'^2 = x'^3 + d^2 a x' + d^3 b,qquad d=-2.
]

All coordinates are interpreted as three little-endian base-field
coefficients in the basis (1,u,u^2), with multiplication reduced modulo
(u^3+u+4).

## Results

All **196 of 196** serialized public points (14 per group, across 14 groups)
satisfy the twisted-curve equation. Every coordinate limb is within the
base-field range.

| Group | Points checked | Points satisfying curve equation |
|---:|---:|---:|
| 140 | 14 | 14 |
| 142 | 14 | 14 |
| 144 | 14 | 14 |
| 146 | 14 | 14 |
| 148 | 14 | 14 |
| 150 | 14 | 14 |
| 152 | 14 | 14 |
| 154 | 14 | 14 |
| 156 | 14 | 14 |
| 158 | 14 | 14 |
| 160 | 14 | 14 |
| 162 | 14 | 14 |
| 164 | 14 | 14 |
| 166 | 14 | 14 |
| **Total** | **196** | **196** |

This result is a strong internal-consistency check: the stored point coordinates,
the extension polynomial, and the documented twist relation agree across
every group in the supplied configuration.

## Reproduction

Run:

```sh
python vista_pkey2005_point_curve_check.py pkeyconfig.xrm-ms -o point-check.json
```

The checker performs public-point equation checks and extension-polynomial
sanity checks. Its output is diagnostic only.

## Limitations

Curve membership does not prove that a point has the required subgroup
order, that the stored pairing reference is correct, or that a product-key
signature verifies. It also does not establish entitlement or activation.
The next cryptographic stage would require a separately validated pairing
implementation and a trusted test vector; no such result is claimed here.

## Reference

- UMSKT, [PKEY2005 public-key format and untwist mapping](https://git.enderman.ch/UMSKT/writeups/src/commit/5e9c37af411e8a3b5491ff2505c6e79abd3ea8f1/PKEY2005.md),
  particularly the extension-field serialization and untwist description.
