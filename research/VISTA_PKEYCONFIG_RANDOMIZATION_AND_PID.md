# Vista PKEY configuration: randomization and PID-field audit

## Scope and source

This note records a read-only inspection of the supplied Vista
`pkeyconfig.xrm-ms` configuration. The exact source file SHA-256 was:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The embedded XML contains 211 `Configuration` elements and 1,120
`KeyRange` elements. Each key range was joined to its parent configuration
through `KeyRange.RefActConfigId` -> `Configuration.ActConfigId`; all
1,120 references matched, and all 211 configurations had at least one range.

## 1. IsRandomized result

Every one of the 211 configuration entries has:

`IsRandomized = false`

| ProductKeyType | Configurations | IsRandomized=true | IsRandomized=false |
|---|---:|---:|---:|
| Retail | 64 | 0 | 64 |
| OEM:NONSLP | 52 | 0 | 52 |
| OEM:COA | 37 | 0 | 37 |
| OEM:SLP | 34 | 0 | 34 |
| Volume:GVLK | 13 | 0 | 13 |
| Volume:MAK | 6 | 0 | 6 |
| Volume:CSVLK | 5 | 0 | 5 |
| **Total** | **211** | **0** | **211** |

There is no channel or group correlation to test within this file because
the flag has no variation. This does not prove that other Vista configuration
versions or other Microsoft licensing products never use a true value.

## 2. Key-range and EULA metadata

The 1,120 joined key ranges contain 791 distinct part-number strings.
The range counts by parent configuration ProductKeyType are:

| ProductKeyType | Key ranges |
|---|---:|
| Retail | 548 |
| OEM:NONSLP | 287 |
| OEM:COA | 107 |
| OEM:SLP | 58 |
| Volume:MAK | 94 |
| Volume:GVLK | 17 |
| Volume:CSVLK | 9 |
| **Total** | **1,120** |

EULA metadata is not a one-to-one alias for ProductKeyType. For example,
some Retail configuration ranges carry an MSDN or Windows Anytime Upgrade
EULA label, while the parent configuration remains `Retail`. Preserve both
fields when analyzing a range; do not replace one with the other.

## 3. PID and Advanced PID findings

The embedded XML schema in this supplied file contains these configuration
fields:

- `ActConfigId`
- `RefGroupId`
- `EditionId`
- `ProductDescription`
- `ProductKeyType`
- `IsRandomized`

Each `KeyRange` contains:

- `RefActConfigId`
- `PartNumber`
- `EulaType`
- `IsValid`
- `Start`
- `End`

There is no explicit Product ID template, Advanced PID template, or PID
generation algorithm in this XML. Therefore the Product ID and Advanced PID
returned by the local PidGenX diagnostic cannot be derived from these fields
alone. Their generation should be treated as behavior of the native
PidGenX/licensing implementation unless a separate authoritative format
specification is obtained.

The successful local PidGenX test reported a Home Premium / OEM:COA mapping.
The separate `slmgr /dlv` screenshot reported the currently installed system
as Home Basic / OEM_COA_SLP with License Status `Licensed`. The screenshots
show different product identities and a different partial product key; they
do not establish that the tested Home Premium key was installed or activated.
Sensitive IDs and complete product keys are intentionally omitted here.

## 4. Interpretation and limitations

- `IsRandomized=false` is an observed configuration flag, not evidence that
  product IDs are deterministic in every respect.
- Key-range boundaries and part numbers are metadata used to describe key
  ranges; this audit does not provide a procedure for constructing keys.
- The channel label, EULA label, and SLMGR Description string are distinct
  fields from different layers. They should not be assumed interchangeable.
- These findings do not establish key ownership, transferability, online
  activation, or global validity.
- No private signing material was recovered, and no key-generation process
  was attempted.

## 5. Reproducibility

The companion audit files are:

- `vista_pkeyconfig_randomization_audit.csv`: one row per configuration.
- `vista_pkeyconfig_randomization_audit.json`: aggregate counts and schema
  conclusions.

Source file hash should be checked before comparing results from another
configuration release.
