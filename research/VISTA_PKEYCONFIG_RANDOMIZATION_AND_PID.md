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

### 3.1 Native PidGenX test observations

The following results were transcribed from user-supplied screenshots.
Complete product keys, full Product IDs, Advanced PIDs, Activation IDs,
Installation IDs, and other machine-specific identifiers are deliberately
excluded.

| Test | Edition | PidGenX HRESULT | Local result | ProductKeyType | EULA |
|---|---|---|---|---|---|
| A | Vista Home Premium | `0x0` | Accepted by installed DLL/config pair | OEM:COA | OEM |
| B | Vista Home Basic | `0x0` | Accepted by installed DLL/config pair | Retail | MSDN |

Test B is a distinct Retail-channel example. Its screenshot reports
Home Basic, Edition ID `X13-04106`, ProductKeyType `Retail`, and EULA
`MSDN`. The exact key and licensing identifiers are not retained.

These are offline PidGenX/configuration acceptance observations. They do
not prove entitlement, ownership, online activation, or that either key
was installed on the computer. In particular, the separately supplied
`slmgr /dlv` screenshot reports the currently installed system as
Home Basic / `OEM_COA_SLP` with License Status `Licensed`; it does not
show that Test A or Test B was installed.

The new Retail example demonstrates that the same native PidGenX diagnostic
can return an accepted result for a Retail configuration as well as the
earlier OEM:COA configuration. It does not by itself establish the full
mathematical signature-verification path or generalize to all Retail keys.

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

The audit can be reproduced by parsing the Base64 `infoBin` payload, counting
`Configuration` entries by `IsRandomized`, then joining each
`KeyRange.RefActConfigId` to `Configuration.ActConfigId`. Check the source
file hash before comparing results from another configuration release.

A downloadable CSV and JSON snapshot were generated during this research
session; the repository's Markdown note is the committed record of the
findings.
