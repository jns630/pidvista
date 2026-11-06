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

The 14 public-key records share the same recovered field modulus, subgroup
order, and curve coefficients in the prior public-parameter audit, but their
serialized records and pairing-reference fields have distinct hashes.
These structural checks are not the final PKEY2005 signature/pairing
verification for a product key.

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
six ProductKeyType categories: Retail, Volume:CSVLK, Volume:MAK,
Volume:GVLK, OEM:NONSLP, and OEM:COA. Its 13 Retail configurations span
multiple Vista editions and add-on products. Because the public-key table is
indexed by GroupId, all 23 configurations resolve to the same group-142
public-key record. This does not make their product keys interchangeable.

The Home Premium OEM:COA configuration references group 144, which is used
only by OEM:COA configurations in this file. Its public-key record differs
from group 142. This does not establish independently generated signing keys
or prove signature validity.

Detailed comparisons:
- [Complete 14-group configuration and public-key fingerprint matrix](research/VISTA_PKEY2005_ALL_GROUP_MATRIX.md)
- [Retail Home Basic PidGenX comparison: group 142 vs group 144](research/VISTA_RETAIL_HOMEBASIC_GROUP142_COMPARISON.md)
- [Group 142 cross-configuration reuse audit](research/VISTA_GROUP142_CROSS_CONFIGURATION_AUDIT.md)

The complete matrix shows that group 144 is OEM:COA-only in this supplied
configuration file (7 configurations, 33 ranges). Groups 148, 160, and 162
are also OEM:COA-only, each with one configuration. Group 142 is the broadest
mixed-channel group (23 configurations, 392 ranges), while group 152 has the
largest configuration count (41). All 14 records use the PKEY2005 algorithm
and have distinct complete-record and pairing-reference hashes. These are
configuration/fingerprint findings, not signature-verification results.

Machine-readable snapshots generated from the same source file:
- `vista_pkey2005_all_group_matrix.csv`
- `vista_pkey2005_all_group_matrix.json`

## Randomization and Product ID limitations

The XML contains configuration IDs, group references, edition IDs,
descriptions, key types, the randomization flag, and key-range metadata.
It does **not** contain an explicit Product ID template, Advanced PID
template, or PID-generation algorithm. PID generation therefore cannot be
reconstructed from these XML fields alone.

Full methodology:
[Vista PKEY configuration: randomization and PID-field audit](research/VISTA_PKEYCONFIG_RANDOMIZATION_AND_PID.md)

## Sample-key cryptographic status

Preliminary Base24 and curve-point checks were structurally consistent, but
the complete PKEY2005 signature/pairing comparison was not performed. The
offline arithmetic result must therefore be described as **unverified**,
not confirmed valid or invalid. A local PidGenX acceptance result is a
separate native observation, not a substitute for claiming online activation
or licence ownership.

## Research scripts

- `vista_pkey2005_research.py` — XML/configuration structure inspector.
- `vista_pkey2005_crypto_audit.py` — public parameter and record audit.
- `vista_pkey2005_public_arithmetic_audit.py` — public arithmetic consistency audit.
- `VistaPidGenXCheck.cpp` — local native PidGenX diagnostic.

The project is limited to read-only configuration inspection, public-parameter
consistency checks, and local validation through Microsoft's installed
licensing component. It does not generate keys, recover private signing
material, patch licensing binaries, bypass validation, or activate Windows.
