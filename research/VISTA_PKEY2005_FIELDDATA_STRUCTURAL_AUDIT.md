# Vista PKEY2005 field-data structural audit

## Scope

This audit parses the serialized public-key records embedded in the supplied
Vista `pkeyconfig.xrm-ms`. It checks container framing and documented
public-parameter boundaries only. It does not accept product keys, generate
keys, calculate H1, recover private material, or verify a signature/pairing.

## Input and repeatability

Input examined: `pkeyconfig(1).xrm-ms`

- File size: 620,662 bytes
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Public-key records found: 14
- Group IDs: 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166

## Observed outer framing

Each decoded public-key blob is 1,579 bytes:

| Absolute offset | Length | Meaning | Observed |
|---:|---:|---|---:|
| 0 | 4 | Outer magic, little-endian | `0x44556677` |
| 4 | 2 | Format version | `0x0100` |
| 6 | 2 | Padding | preserved |
| 8 | 4 | Field-data size, little-endian | 307 (`0x133`) |
| 12 | 307 | Field-data region | ends at offset 319 |

The 319-byte prefix (outer header plus declared field-data region) is identical
across all 14 records.

## Field-data schema alignment

The published UMSKT PKEY2005 binary-format description gives the following
field-data prefix. The parser follows that documented order and verifies that
each variable-length member remains inside the declared 307-byte region.

| Field-data relative offset | Absolute offset | Member | Observed size/value |
|---:|---:|---|---:|
| 0 | 12 | Field magic | `0x00112233` |
| 4 | 16 | Field version | `0x0100` |
| 8 | 20 | must_be_0 | 0 |
| 9 | 21 | size_modulus / size_bignum | 14 |
| 10 | 22 | size_order | 14 |
| 11 | 23 | ext_deg1 | 3 |
| 15 | 27 | ext_deg2 | 2 |
| 19, 23, 27 | 31, 35, 39 | documented unused words | retained as raw integers |
| 31 | 43 | num_elements | 14 |
| 35, 39, 43 | 47, 51, 55 | documented unused words | retained as raw integers |
| 47 | 59 | max_quotient byte | 35 |
| 48 | 60 | H1 radix vector | 14 bytes |
| 62 | 74 | modulus | 14 bytes |
| 76 | 88 | order | 14 bytes |
| 90 | 102 | extension polynomial 1 | 4 bytes |
| 94 | 106 | extension polynomial 2 | 3 bytes |
| 97 | 109 | base-curve coefficient a | 14 bytes |
| 111 | 123 | base-curve coefficient b | 14 bytes |
| 125 | 137 | curve coefficient a | 14 bytes |
| 139 | 151 | curve coefficient b | 14 bytes |

The documented members consume 153 bytes of the field-data region. The
remaining 154 bytes (field-data relative offsets 153 through 306) are zero
padding in every one of the 14 records examined. The outer record declares a
307-byte field-data region, and the public format description pads the field
structure to that declared boundary before the point vector begins.

The six words labelled unused are reported without assigning additional
semantics. Their values are preserved in the JSON report.

## Point-vector and pairing boundaries

Each point consists of three little-endian bignum limbs for x and three for y.
With 14-byte bignums, each point occupies 6 × 14 = 84 bytes.

- Point vector begins at absolute offset 319.
- 14 points occupy 14 × 84 = 1,176 bytes.
- Point vector ends at absolute offset 1,495 (exclusive).
- Pairing reference has ext_deg1 × ext_deg2 = 3 × 2 = 6 limbs.
- Pairing reference occupies 6 × 14 = 84 bytes, offsets 1,495–1,578.
- End of pairing reference is offset 1,579, exactly the record length.

Thus the 1,260-byte suffix is exactly 14 point blocks plus one pairing-reference
block. The parser verifies these arithmetic boundaries for every record.

## Parser

`vista_pkey2005_publickey_inspector.py` reads the XrML `infoBin`, extracts
each `PublicKeyValue`, performs the structural checks above, and emits JSON.

Example:

```sh
python vista_pkey2005_publickey_inspector.py pkeyconfig.xrm-ms -o inspection.json
```

The JSON includes each group ID, record hash, observed header values, field
member offsets, trailing-padding status, point/pairing ranges, and check
results. It fails on malformed lengths or inconsistent record boundaries.

## Interpretation and limits

The successful parse establishes that the supplied records are internally
consistent with this documented serialization layout. It does not establish
that any product key is valid, that any signature passes pairing verification,
that a key is entitled to a licence, or that Windows will activate.

## Reference

- UMSKT, [PKEY2005 public-key binary format and validation notes](https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md).
