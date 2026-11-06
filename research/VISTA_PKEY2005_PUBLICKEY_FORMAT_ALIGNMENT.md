# PKEY2005 public-key record: documented field map and Vista blob alignment

## Scope

This note maps the supplied Vista `pkeyconfig.xrm-ms` public-key records
against the public PKEY2005 binary-format description published in the UMSKT
write-up. It is a format/serialization audit only. It does not implement
signature verification, recover private signing material, or generate keys.

Source file:
- Name: `pkeyconfig(1).xrm-ms`
- Size: 620,662 bytes
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

External format reference:
- UMSKT, “PKEY2005 Validation,” Public Key Binary Format:
  https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- The write-up describes an outer public-key header, a field-data structure,
  a vector of elliptic-curve points, and a stored pairing value.

## 1. Observed outer header

All 14 decoded records are 1,579 bytes. The first 12 bytes decode as:

| Offset | Length | Observed value | Interpretation |
|---:|---:|---|---|
| 0 | 4 | `0x44556677` | Public-key record magic |
| 4 | 2 | `0x0100` | Format/version marker |
| 6 | 2 | zero padding | Padding |
| 8 | 4 | `307` (`0x133`) | Field-data byte length |

The field-data block therefore occupies offsets 12–318 inclusive
(307 bytes), and ends at absolute offset 319.

The public format description names the same outer magic, version marker,
and field-data length field.

## 2. Alignment of the 319-byte common prefix

The earlier byte comparison found that offsets 0–318 are byte-for-byte
identical in all 14 group records.

The documented structure explains the boundary:

- 12-byte outer header
- 307-byte field-data block
- Total: 319 bytes

Thus, the common prefix is not merely an unexplained constant header: it
contains the common record header **and the entire serialized field-data
block** described by the public format write-up.

The field-data block carries shared algorithm/domain parameters, including
the base-field modulus, subgroup order, extension-polynomial metadata,
H1 radix vector, and elliptic-curve coefficients. The public write-up also
documents reserved/unused fields. This audit does not assign semantics to
reserved fields beyond the published description.

## 3. Alignment of the 1,260-byte group-specific suffix

The suffix begins at absolute offset 319 and has length 1,260 bytes.

For this supplied file, the public-key records contain 14 point records,
each 84 bytes, followed by one 84-byte pairing-value record:

| Component | Count | Bytes each | Total |
|---|---:|---:|---:|
| Compressed/twist point records | 14 | 84 | 1,176 |
| Stored pairing value | 1 | 84 | 84 |
| **Suffix total** | | | **1,260** |

The arithmetic aligns exactly:

`319 + (14 × 84) + 84 = 1,579`

The public PKEY2005 write-up describes the point vector as `ecpoint_k3`
entries and the final field element as the stored Tate pairing reference.
An 84-byte point is consistent with six 14-byte base-field limbs: three
limbs for x and three for y. The 84-byte pairing value is consistent with
six 14-byte limbs for the degree-six extension field in this file.

This is the structural explanation for the 15 blocks in the previous
comparison: blocks 1–14 correspond to the 14 point records, and block 15
corresponds to the pairing value. The prior 84-byte partition was therefore
not arbitrary for this specific record layout.

## 4. What differs between groups

The empirical comparison across all 14 records found:

- Common prefix (offsets 0–318): identical in all 14.
- Point-vector plus pairing suffix (offsets 319–1578): distinct for every
  group.
- Each of the 15 84-byte blocks has 14 distinct byte sequences across the
  14 groups.
- Pairwise byte-position Hamming distances between full records: 1,246 to
  1,258 across 91 pairs.

The group-specific portion therefore includes differences throughout the
point vector and stored pairing value, rather than a single small group-ID
field. This is a serialization observation, not a claim about how Microsoft
generated or provisioned each key.

## 5. Updated interpretation

The strongest supported interpretation is:

1. All 14 records share one common PKEY2005 field-data/header block in this
   configuration file.
2. Each group has a distinct vector of 14 serialized points and a distinct
   stored pairing reference.
3. The common prefix and group-specific suffix map cleanly onto the public
   PKEY2005 record schema.
4. A group ID selects a complete group-specific public-key record; it is not
   simply an edition or channel label.
5. This does not establish that each group was generated independently,
   that any particular product key is valid, or that a key is entitled to
   activation.

## 6. Validation boundaries

The local Vista PidGenX checker and this structural parser answer different
questions:

- PidGenX result: whether the installed native DLL/configuration pair
  accepted the input for local product-ID processing.
- Structural audit: whether the configuration records parse and align with
  the public binary-format description.
- Full cryptographic verification: a separate mathematical check of the
  PKEY2005 signature/pairing relation. It has not been completed for the
  sample key discussed in this project.
- Activation/entitlement: a separate licensing-server and licensing-state
  question.

Do not report a structural parse or HRESULT 0 as proof of online activation,
ownership, or global validity.

## 7. Reproduction checklist

1. Decode the outer XrML `infoBin` Base64 payload to the embedded XML.
2. Extract each `PublicKeyValue` Base64 blob.
3. Check record length (1,579 bytes) and outer magic/version.
4. Read the 32-bit little-endian field-data length at offset 8.
5. Confirm that `12 + field_data_length = 319` for this supplied file.
6. Confirm the 1,260-byte suffix is exactly 14 × 84-byte point records plus
   one 84-byte pairing-value record.
7. Compare group records by hashes and fixed-size block equality.
8. Preserve the source-file SHA-256 with every audit result.

## 8. Source and attribution

The binary layout and field names above are based on the public UMSKT
PKEY2005 validation write-up. Byte counts, common-prefix equality, group
differences, and the exact alignment to the supplied Vista file are
observations from the supplied `pkeyconfig.xrm-ms` data. Interpretations
beyond those two sources are explicitly identified as inference.
