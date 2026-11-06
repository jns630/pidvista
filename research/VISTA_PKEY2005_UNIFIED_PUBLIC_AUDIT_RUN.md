# Unified Vista PKEY2005 Public-Data Audit — Run Record

## Input

- File: supplied `pkeyconfig.xrm-ms`
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Size: 620,662 bytes

## Results from local execution

The unified public-data audit algorithm was executed locally against the supplied file.

| Check | Result |
|---|---:|
| Public-key groups parsed | 14 |
| Serialized points | 196 |
| Points with canonical coordinates | 196/196 |
| Points on documented twisted curve | 196/196 |
| Points for which ([m]Q=O) | 196/196 |
| Groups with identical field-data bytes | 14/14 |

Every group ID (140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166) passed all point-coordinate, curve-membership and scalar-annihilation checks.

The field-data prefix was byte-identical across all 14 records.

## Pairing-reference status

For each record, the six serialized coefficient limbs were checked to be below (p), and the decoded coefficient vector was nonzero.

**No pairing-reference order test is claimed.** In particular, this run record does not claim (c^m=1), and it does not recompute the Tate pairing. The field-basis/serialization interpretation must be independently settled before that test is added.

## Reproduction

The committed script is:

`vista_pkey2005_unified_public_audit.py`

Run:

```sh
python vista_pkey2005_unified_public_audit.py pkeyconfig.xrm-ms -o public-audit.json
```

The local run used the same documented field tower and twist-curve model as the committed script. The output JSON was generated locally; this report records its aggregate results.

## Interpretation limits

- Fixed-base probable-prime tests are probable-prime checks, not formal primality certificates.
- ([m]Q=O) plus a prime (m) and non-identity affine coordinates implies exact order (m), conditional on the curve model and arithmetic being correct. This report records the scalar-annihilation test, not a separate proof certificate.
- These are public-parameter consistency checks, not product-key signature verification.
- No product key is generated or modified; no private signing material is recovered.
- No ownership, entitlement, online activation or transferability conclusion follows.
