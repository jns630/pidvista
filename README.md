# pidvista — Windows Vista PKEY2005 research and local validation

This repository contains read-only research tools for examining Vista licensing
configuration data and asking the **installed Windows Vista PidGenX implementation**
to process a product key locally. It is not a key generator or activation bypass.

## Current validation tool

- Source: [VistaPidGenXCheck.cpp](VistaPidGenXCheck.cpp)
- Build workflow: [.github/workflows/c-cpp.yml](.github/workflows/c-cpp.yml)
- Artifact name: `VistaPidGenXCheck-x64`
- Target: x64 Windows Vista (subsystem version 6.00), built with the static MSVC CRT.

The checker loads the installed Vista `pidgenx.dll` and matching
`pkeyconfig.xrm-ms`, prompts for a key locally, and does not save or transmit
the key. Keep keys and machine-specific licensing identifiers out of source
control, CI logs, and public screenshots.

### Interpreting the result

- **HRESULT 0:** the local PidGenX DLL/configuration pair accepted the input
  for local product-ID processing.
- **Nonzero HRESULT:** PidGenX did not accept/process the input. Check the
  installed configuration, product edition, channel, and exact HRESULT.
- Neither result proves ownership, transferability, genuine entitlement,
  or activation. Activation is a separate licensing state.

## Supplied Vista configuration inventory

The supplied configuration files examined during this research were identical:

- Size: **620,662 bytes**
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Embedded XML: **211 Configuration entries**, **1,120 KeyRange entries**
- Public-key groups: **14** (IDs 140 through 166, even numbers)
- Decoded public-key records: **1,579 bytes** each
- Algorithm: `msft:rm/algorithm/pkey/2005`

All 1,120 key-range references matched a configuration entry. All 211
configurations had at least one range. All 211 had `IsRandomized=false` in
this particular file. There were 791 distinct part-number strings.

## Native PidGenX observations

Two user-run offline PidGenX tests have been documented, with complete keys
and machine-specific identifiers omitted:

| Test | Edition | ProductKeyType | EULA | Group ID | HRESULT |
|---|---|---|---|---:|---|
| A | Vista Home Premium | OEM:COA | OEM | 144 | `0x0` |
| B | Vista Home Basic | Retail | MSDN | 142 | `0x0` |

Test B's Activation ID matched the Home Basic Retail configuration in the
supplied XML. Its Edition ID `X13-04106` matched the part number on the
single MSDN-labelled range attached to that configuration. The parent
configuration still has `ProductKeyType=Retail`; EULA and ProductKeyType
are distinct fields.

Group 142 is referenced by **23 configurations and 392 key ranges** across
six ProductKeyType categories. Group 144 is used only by OEM:COA
configurations in this file. The two screenshot observations resolve to
different groups and different serialized public-key records.

Detailed comparisons:
- [Complete 14-group configuration and public-key fingerprint matrix](research/VISTA_PKEY2005_ALL_GROUP_MATRIX.md)
- [Retail Home Basic PidGenX comparison: group 142 vs group 144](research/VISTA_RETAIL_HOMEBASIC_GROUP142_COMPARISON.md)
- [Group 142 cross-configuration reuse audit](research/VISTA_GROUP142_CROSS_CONFIGURATION_AUDIT.md)
- [PKEY2005 public-key byte-structure comparison](research/VISTA_PKEY2005_PUBLICKEY_BYTE_STRUCTURE.md)

## Public-key byte-structure findings

All 14 decoded public-key records are 1,579 bytes. Bytes 0–318 (319 bytes)
are identical across all groups. Bytes 319–1578 (1,260 bytes) are group
specific, with 14 distinct suffixes. Partitioning the suffix into 15
consecutive 84-byte blocks for descriptive comparison shows 14 distinct
values in every block. Across the 91 record pairs, byte-position Hamming
distances range from 1,246 to 1,258.

This establishes a common serialized prefix and extensive group-specific
suffix variation. The 84-byte partition is descriptive, not a semantic
field map. These byte differences do not prove independently generated
signing keys or constitute signature verification.

## Randomization and Product ID limitations

All 211 configurations in the supplied file have `IsRandomized=false`.
The XML does not contain an explicit Product ID template, Advanced PID
template, or PID-generation algorithm. See:
[Randomization and PID-field audit](research/VISTA_PKEYCONFIG_RANDOMIZATION_AND_PID.md).

## Sample-key cryptographic status

Preliminary Base24 and curve-point checks were structurally consistent, but
the complete PKEY2005 signature/pairing comparison was not performed. The
offline arithmetic result must therefore be described as **unverified**,
not confirmed valid or invalid. A local PidGenX acceptance result is a
separate native observation, not a substitute for online activation or
licence ownership.

## Research scripts

- `vista_pkey2005_research.py` — XML/configuration structure inspector.
- `vista_pkey2005_crypto_audit.py` — public parameter and record audit.
- `vista_pkey2005_public_arithmetic_audit.py` — public arithmetic consistency audit.
- `VistaPidGenXCheck.cpp` — local native PidGenX diagnostic.

The project is limited to read-only configuration inspection, public-parameter
consistency checks, and local validation through Microsoft's installed
licensing component. It does not generate keys, recover private signing
material, patch licensing binaries, bypass validation, or activate Windows.
