# Vista PKEY2005 Cross-Group Public-Parameter Comparison

## Scope and input

This comparison examines the 14 serialized PKEY2005 public-key records embedded in the supplied Vista `pkeyconfig.xrm-ms` file. It compares only public serialized material; it does not derive private coefficients, discrete logarithms, signatures, or product keys.

Input SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The three supplied XrML copies were byte-identical.

## Result at a glance

The 14 records have a common 319-byte prefix and group-specific suffixes:

| Region | Offset | Length | Across 14 groups |
|---|---:|---:|---|
| Outer header + field data | 0–318 | 319 bytes | Identical |
| Point vector | 319–1494 | 1,176 bytes | Different in every group |
| Pairing reference | 1495–1578 | 84 bytes | Different in every group |

All 14 records are 1,579 bytes. Every field-data region is 307 bytes and byte-identical. The point vector contains 14 points of 84 bytes each.

This matches the documented format: common field parameters and H1 radix vector, followed by the group-specific point vector and stored pairing reference. The public format description identifies these regions as the field parameters/radices, points (Q_i'), and pairing reference (c=e_m(P,S)). See the UMSKT PKEY2005 write-up: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md

## Shared field parameters

Every one of the following serialized fields is identical across all 14 groups:

| Field | Serialized value (hex, little-endian where numeric) | Interpretation |
|---|---|---|
| H1 radix vector | `0103080f0f0f1f0303030303073f` | 14 radix bytes |
| Base-field modulus (p) | `65465424650c823b8a1d9b8cb32b` | 14-byte little-endian integer |
| Curve order (m) | `ef79ad01f746183b8a1d9b8cb32b` | 14-byte little-endian integer |
| First extension polynomial | `04 01 00 01` | (u^3+u+4), low-degree coefficient first |
| Second extension polynomial | `02 00 01` | (t^2+2), low-degree coefficient first |
| Base-curve (a) | 14 zero bytes | Unused base-curve coefficient |
| Base-curve (b) | 14 zero bytes | Unused base-curve coefficient |
| Curve (a) | `da14d4df6e6d04a4c03fd31f4d01` | 14-byte little-endian integer |
| Curve (b) | `4de6c02220717598fe0c26685b12` | 14-byte little-endian integer |

The format prefix also agrees across groups on the magic values, format versions, extension degrees (3 and 2), field-data size (307), point count (14), and maximum-quotient byte (35).

The shared field parameters imply that the groups use the same represented base field, curve, extension tower, and radix vector in this particular configuration file. This is a statement about the supplied file, not every Vista/Windows 7 configuration ever published.

## Group-specific material

Each group has a distinct 1,176-byte point-vector region and a distinct 84-byte pairing-reference region. The following SHA-256 prefixes are fingerprints of those exact serialized regions; they are useful for reproducibility and detecting accidental changes, not cryptographic interpretations of the underlying points.

| Group ID | Point-vector SHA-256 prefix | Pairing-reference SHA-256 prefix |
|---:|---|---|
| 140 | `a20b11eaa47c` | `0f7358959818` |
| 142 | `37e383a4c716` | `1eedb5fdc5b2` |
| 144 | `cc8aea8eabf7` | `4fb2ff20dbcc` |
| 146 | `998b27e0f6c3` | `d24808256256` |
| 148 | `857d309a0afd` | `663c7cc50da9` |
| 150 | `d79689fb13a3` | `bf04fd8f49b7` |
| 152 | `1394c1006ad9` | `de7d6ce92f75` |
| 154 | `262269f94905` | `43e250b6b3b5` |
| 156 | `462b331cb08a` | `36b6fb7edf4e` |
| 158 | `74b06f2e89b1` | `c87b1ffa36dd` |
| 160 | `e478f4829b3a` | `fa2b459cb8d8` |
| 162 | `4a5debd10c3a` | `f31e7fd9967a` |
| 164 | `f53c5277795a` | `ed1ac33a897c` |
| 166 | `c6aeae6a2eff` | `341ee6b17b05` |

All 14 point-vector fingerprints are distinct, and all 14 pairing-reference fingerprints are distinct.

## Interpretation

The simplest structural conclusion is:

- **Shared across groups:** serialization format, field parameters, curve coefficients, extension polynomials, H1 radix vector, and dimensions.
- **Specific to each group:** the serialized (Q_i') point vector and the stored pairing reference (c).

This is consistent with one common mathematical parameter set being reused for multiple product-key groups, while each group carries its own public point vector and target pairing value.

The comparison does not reveal how the group-specific points were generated, does not establish relationships between their discrete logarithms, and does not recover any private signing vector. It also does not prove that a product key belongs to a given group or is valid.

## Reproducibility

The comparison was computed locally by extracting each `PublicKeyValue` blob from the embedded `infoBin` XML, then hashing and comparing the exact byte slices at the offsets listed above. All 14 records were 1,579 bytes long and shared the exact first 319 bytes.

The region hashes are abbreviated to 12 hexadecimal characters in the table. The full input file SHA-256 is recorded above.
