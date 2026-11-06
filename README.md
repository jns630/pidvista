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

Detailed configuration comparisons:
- [Complete 14-group configuration and public-key fingerprint matrix](research/VISTA_PKEY2005_ALL_GROUP_MATRIX.md)
- [Retail Home Basic PidGenX comparison: group 142 vs group 144](research/VISTA_RETAIL_HOMEBASIC_GROUP142_COMPARISON.md)
- [Group 142 cross-configuration reuse audit](research/VISTA_GROUP142_CROSS_CONFIGURATION_AUDIT.md)

## Public-key binary format alignment

All 14 decoded public-key records are 1,579 bytes. The first 12 bytes are
the outer record header; its little-endian field-data length is 307 bytes.
Thus the complete common prefix is 12 + 307 = **319 bytes**, identical
across all 14 groups.

The remaining 1,260 bytes align with the documented PKEY2005 schema as
14 × 84-byte point records followed by one 84-byte stored pairing value.
This explains the 15 blocks in the earlier byte comparison: 14 point entries
and the final pairing-reference entry. Every one of those blocks differs
across all 14 groups in this supplied configuration.

The field map is based on the public UMSKT PKEY2005 write-up; the byte
alignment and equality results are independently observed from the supplied
Vista configuration file. This does not prove independent key generation,
signature validity, or activation.

Detailed note:
[Vista PKEY2005 public-key format alignment](research/VISTA_PKEY2005_PUBLICKEY_FORMAT_ALIGNMENT.md)

Additional byte-level comparison:
[PKEY2005 public-key byte-structure comparison](research/VISTA_PKEY2005_PUBLICKEY_BYTE_STRUCTURE.md)

## Field-data structural parser

The 307-byte field-data region has been audited against the published PKEY2005
binary layout. The documented members consume 153 bytes; the remaining 154
bytes are zero padding in all 14 supplied records. The parser checks the outer
and inner headers, member bounds, 14 × 84-byte point vector, and 84-byte
pairing-reference boundary.

- Parser: [vista_pkey2005_publickey_inspector.py](vista_pkey2005_publickey_inspector.py)
- Audit: [Field-data structural audit](research/VISTA_PKEY2005_FIELDDATA_STRUCTURAL_AUDIT.md)

Run with `python vista_pkey2005_publickey_inspector.py pkeyconfig.xrm-ms -o inspection.json`.
This is structural inspection only, not product-key or signature validation.

## Public-parameter sanity audit

The read-only [public-parameter sanity checker](vista_pkey2005_public_parameter_sanity.py)
checks field dimensions, probable primality, polynomial coefficient bounds,
and curve non-singularity. Results are documented in the
[public-parameter sanity audit](research/VISTA_PKEY2005_PUBLIC_PARAMETER_SANITY_AUDIT.md).
These checks do not verify points, signatures, pairings, or activation.

## Signature-verification readiness

The public PKEY2005 pairing-verification model and remaining unknowns are
summarized in [Signature-verification readiness](research/VISTA_PKEY2005_SIGNATURE_VERIFICATION_READINESS.md).
The structural inspector is not a signature verifier. Its field map was
corrected to treat field-data offset `0x1f` as `offset_modulus`; the point
count is derived from `size_modulus`.

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
