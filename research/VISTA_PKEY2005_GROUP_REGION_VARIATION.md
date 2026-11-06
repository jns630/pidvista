# PKEY2005 public-key group region variation

## Method

The 14 `PublicKeyValue` Base64 blobs were extracted from the embedded XrML
`infoBin` in `pkeyconfig(1).xrm-ms`. The input file SHA-256 is:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

Each decoded record is 1,579 bytes. The comparison was performed at each byte
offset across all 14 group records, then independently by region and by each
84-byte point block. This is a descriptive byte comparison only.

## Region-level result

| Region | Offsets (end exclusive) | Length | Varying byte positions | Unique region hashes |
|---|---:|---:|---:|---:|
| Outer header | 0–12 | 12 | 0 | 1 |
| Field data | 12–319 | 307 | 0 | 1 |
| Point vector | 319–1495 | 1,176 | 1,176 | 14 |
| Pairing reference | 1495–1579 | 84 | 84 | 14 |

Therefore, the complete 319-byte prefix is byte-identical across all 14 groups.
Every byte position in the point vector and pairing-reference region differs
between at least two groups. Both suffix regions have 14 unique region hashes.

## Per-point result

All 14 point blocks are 84 bytes. For every point index 0 through 13:

- all 84 byte positions vary across the 14 groups;
- all 14 groups have a unique 84-byte block at that index.

The point offsets are contiguous:
`319 + (point_index × 84)`, ending at offset 1,495 exclusive.

## What this establishes

The records share a common serialization header and field-data parameter block,
but their serialized point vectors and stored pairing-reference values are
group-specific in this supplied file. The comparison does not establish why
they differ, whether their underlying mathematical points are independent,
whether any signatures are valid, or whether any key is entitled to activation.

The pairing-reference value is treated as an opaque serialized public-data
region here. No private-key derivation, H1 recovery, signature forgery, or
pairing verification is attempted.

## Reproduction

Run the structural parser first:

```sh
python vista_pkey2005_publickey_inspector.py pkeyconfig.xrm-ms -o inspection.json
```

The accompanying CSV `vista_pkey2005_group_region_variation.csv` contains
region and per-point counts and offsets. The JSON report contains the same
findings in machine-readable form.
