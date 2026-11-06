# Vista Retail Home Basic PidGenX comparison: group 142 vs group 144

## Scope

This note records the comparison of the user's second locally run Vista
PidGenX test (Home Basic, Retail / MSDN) against the supplied
`pkeyconfig.xrm-ms` file, and compares it with the earlier Home Premium
OEM:COA test.

The source configuration file was 620,662 bytes with SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The complete product key and machine-specific identifiers are intentionally
not reproduced here.

## 1. Native PidGenX observation from screenshot

The second screenshot reports:

| Field | Observed value |
|---|---|
| PidGenX HRESULT | `0x0` |
| Local result | Accepted by installed DLL/config pair |
| Edition type | Home Basic |
| Edition ID | `X13-04106` |
| ProductKeyType | Retail |
| EULA | MSDN |
| Activation ID | `95c6e80a-0ff8-4bd0-95f2-c4a39b79d09e` |

This is an offline local PidGenX/configuration acceptance result. It does not
prove licence ownership, online activation, transferability, or global
validity.

## 2. Exact Activation ID match in the supplied configuration

The Activation ID matches exactly one `Configuration` entry in the supplied
embedded XML (case-insensitive GUID comparison, braces ignored).

| Configuration field | Matched value |
|---|---|
| EditionId | `HomeBasic` |
| ProductDescription | `Windows Vista Home Basic Retail` |
| ProductKeyType | `Retail` |
| RefGroupId | `142` |
| IsRandomized | `false` |

The key's displayed Edition ID `X13-04106` is also present as a
`PartNumber` in one of the ranges attached to this configuration.

## 3. Key ranges attached to this Retail configuration

The Activation ID has **61** associated `KeyRange` records in this file.
They cover **35** distinct part-number strings:

- 60 ranges have `EulaType=Retail`.
- 1 range has `EulaType=MSDN`.
- All 61 have `IsValid=true`.
- The MSDN-labelled range is part number `X13-04106`, matching the
  Edition ID printed in the PidGenX screenshot.

This is a concrete example of why `ProductKeyType` and `EulaType` must be
kept separate: the parent configuration is Retail, while one attached range
has an MSDN EULA label. It does not change the parent's ProductKeyType.

## 4. Comparison with the earlier Home Premium OEM:COA test

The earlier PidGenX screenshot reported the Home Premium Activation ID
`a4eec485-e375-48b4-8f51-80d13a4086b6`. That ID matches this configuration
entry:

| Configuration field | Home Premium test |
|---|---|
| EditionId | `HomePremium` |
| ProductDescription | `Windows Vista Home Premium - OEM:COA` |
| ProductKeyType | `OEM:COA` |
| RefGroupId | `144` |
| IsRandomized | `false` |
| Attached KeyRange records | 4 |
| Distinct part numbers | 3 |
| EULA labels | OEM (all 4) |

The two tests therefore map to different configuration entries and different
public-key groups:

| Property | Home Basic test | Home Premium test |
|---|---:|---:|
| Edition | Home Basic | Home Premium |
| ProductKeyType | Retail | OEM:COA |
| Group ID | **142** | **144** |
| Range records for exact Activation ID | 61 | 4 |
| EULA labels | Retail (60), MSDN (1) | OEM (4) |
| PidGenX HRESULT | 0x0 | 0x0 |

## 5. Group-level usage

The group-level counts are broader than the exact Activation ID counts above:

| Group | Configurations referencing group | Key ranges across those configurations | ProductKeyType distribution |
|---|---:|---:|---|
| 142 | 23 | 392 | Retail 13; Volume:CSVLK 1; Volume:MAK 1; Volume:GVLK 4; OEM:NONSLP 2; OEM:COA 2 |
| 144 | 7 | 33 | OEM:COA 7 |

Group 142 is shared by several product-key types. Group 144 is associated
only with OEM:COA configurations in this particular file. A group ID is
therefore not itself an edition or channel label.

## 6. Public-key record comparison

Both group records identify the same algorithm:

`msft:rm/algorithm/pkey/2005`

Both decoded records are 1,579 bytes. Their SHA-256 fingerprints differ:

| Fingerprint | Group 142 | Group 144 |
|---|---|---|
| Complete public-key record SHA-256 | `255befbd0b7207d59f03ee472880a0ae611c419387f59c290c0060fdd3b1c1e7` | `10f913219d9c4c81d7eb22f40a34fb8179a08b99e3dddef2d71c1e8f8352d0c6` |
| Pairing-reference field SHA-256 | `1eedb5fdc5b2dc734b3bca2c410d579eec9c058f5a61b8ebdb2a0467dd1a8c9e` | `4fb2ff20dbcc399d580a7e5ba2fa264396eaf5965d84a60d25b3697a174a0c28` |

The earlier public-parameter audit found that all 14 groups in this file
share the same recovered field modulus, subgroup order, and curve
coefficients, while their complete public-key records and pairing-reference
fields differ.

For these two groups, the hash comparison confirms that the stored records
are not byte-identical. It does not, by itself, establish whether the groups
represent independently generated signing keys, nor does it constitute a
PKEY2005 signature/pairing verification of either screenshot's key.

## 7. Conclusions

1. The Retail Home Basic Activation ID from the screenshot exactly matches
   a configuration with `EditionId=HomeBasic`, `ProductKeyType=Retail`,
   and `RefGroupId=142`.
2. Its displayed Edition ID `X13-04106` matches the part number on the
   one MSDN-labelled range attached to that configuration.
3. The earlier Home Premium OEM:COA test maps to group 144, not group 142.
4. Both local PidGenX tests returned HRESULT 0, but they exercised different
   configuration entries and different group-specific public-key records.
5. The two groups use the same named PKEY2005 algorithm and common
   mathematical domain from the earlier audit, but their serialized public
   records and pairing-reference fingerprints differ.
6. None of these observations proves online activation, licence ownership,
   or global validity. No private signing material was recovered and no
   product-key generation was attempted.

## 8. Reproduction method

1. Decode the outer XrML `infoBin` Base64 payload to the embedded XML.
2. Find the `Configuration` whose `ActConfigId` equals the screenshot's
   Activation ID, ignoring GUID braces and letter case.
3. Read `EditionId`, `ProductDescription`, `ProductKeyType`,
   `RefGroupId`, and `IsRandomized`.
4. Select `KeyRange` entries whose `RefActConfigId` matches that
   `ActConfigId`.
5. Select the `PublicKey` record with the matched `RefGroupId`; compare
   record hashes rather than publishing key material.
6. Keep the screenshot-derived PidGenX outcome separate from XML-derived
   metadata and from any online activation status.

Source: supplied `pkeyconfig.xrm-ms` file and user-provided PidGenX
screenshots. External format references: the PKEY configuration record
model and PidGenX's use of a matching configuration file are described in
the cited public references in the project discussion.
