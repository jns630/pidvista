# pidvista — Windows Vista PKEY2005 research and local validation

This repository contains read-only research tools for examining Vista licensing
configuration data and asking the **installed Windows Vista PidGenX implementation**
to process a product key locally. It is not a key generator or activation bypass.

## Current validation tool

- Source: [VistaPidGenXCheck.cpp](VistaPidGenXCheck.cpp)
- Build workflow: [.github/workflows/c-cpp.yml](.github/workflows/c-cpp.yml)
- Artifact name: `VistaPidGenXCheck-x64`
- Target: x64 Windows Vista (subsystem version 6.00), built with the static MSVC CRT.

The checker loads:

- `C:\\Windows\\System32\\pidgenx.dll`
- `C:\\Windows\\System32\\licensing\\pkeyconfig\\pkeyconfig.xrm-ms`

It prompts for a key on the Vista computer and calls the local `PidGenX` export.
The key is not written to a file or transmitted by this program. The program
wipes its in-memory input buffer after the call. Do not paste keys into GitHub
issues, workflow inputs, logs, commits, or this README.

### Build and test

1. Open the repository's **Actions** tab.
2. Select **Build VistaPidGenXCheck**.
3. Choose **Run workflow**.
4. Download the `VistaPidGenXCheck-x64` artifact from the completed run.
5. Extract it and copy `VistaPidGenXCheck.exe` to a Windows Vista SP2 x64
   installation that has its normal licensing components.
6. Run it locally from Command Prompt and enter the test key at its prompt.

The workflow only compiles and checks the executable's architecture/subsystem.
It cannot run Vista's PidGenX DLL on the hosted Windows runner. The actual
validation step must be performed on the Vista machine. This build target is
not proof of runtime compatibility; report any missing DLL, entry-point, or
runtime error exactly as displayed.

### Interpreting the result

- **HRESULT 0:** the local PidGenX DLL/configuration pair accepted the input
  for local product-ID processing. This is a positive local validation result
  for that installed configuration.
- **Nonzero HRESULT:** PidGenX did not accept/process the input. It is not, by
  itself, proof that a key is globally invalid; check edition, channel,
  configuration-file version, and the exact HRESULT.
- Neither result proves licence ownership, transferability, genuine status,
  or that Windows is activated. Activation is a separate licensing state.

The checker is currently hard-coded for the Vista x64 system paths. Do not use
it as an XP/Windows 7 checker or assume that an arbitrary copied
`pkeyconfig.xrm-ms` is interchangeable with the configuration installed on
the target machine.

## Public Vista PKEY2005 configuration findings

The supplied configuration files examined during this research were byte-for-byte
identical:

- Size: **620,662 bytes**
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Embedded configuration: **211 Configuration entries**, **1,120 KeyRange entries**
- Public-key groups: **14**, with IDs **140, 142, 144, 146, 148, 150, 152, 154,
  156, 158, 160, 162, 164, 166**
- Each decoded public-key record: **1,579 bytes**
- Algorithm identifier: `msft:rm/algorithm/pkey/2005`

The public-parameter audit scripts in this repository inspect the XML structure,
record sizes and hashes, field parameters, extension-field arithmetic, curve
points, and stored pairing-element subgroup consistency. The independent
arithmetic audit uses:

- Base field modulus:
  `886368969471450739924935101400677`
- Subgroup order:
  `886368969471450710152985728350703`
- Cubic extension relation: `u^3 + u + 4 = 0`
- Quadratic extension relation: `t^2 + 2 = 0`
- The stored point records are checked against the documented quadratic-twist
  curve equation over the cubic extension field.
- The audit checks the stored pairing element's nonzero value and
  `c^n = 1` subgroup relation.

These are public-parameter consistency checks. They are not the final
PKEY2005 signature/pairing comparison for a product key.

## Sample-key investigation status

A sample Vista key was examined offline during the conversation; its literal
value is intentionally omitted from the repository.

Established preliminary observations:

- Base24 decoding with the Windows product-key alphabet produced a 112-bit
  integer.
- The quotient on division by the recovered field modulus was **4**. This
  passed the preliminary quotient-bound check discussed in the public
  PKEY2005 research.
- The decoded x-coordinate admitted curve y-coordinate candidates on the
  reconstructed base curve.
- These checks establish structural plausibility only.

**Final cryptographic verdict: UNVERIFIED.** The complete PKEY2005 signature
verification/pairing comparison was not performed. Therefore the sample key
must not be described as confirmed valid or confirmed invalid based on these
offline calculations. The local Vista PidGenX test above is the next
independent validation step.

## Research scripts

- `vista_pkey2005_research.py` — XML/configuration structure inspector.
- `vista_pkey2005_crypto_audit.py` — public parameter and record audit.
- `vista_pkey2005_public_arithmetic_audit.py` — independent extension-field,
  twist-point, and pairing-subgroup consistency audit.
- `VistaPidGenXCheck.cpp` — local native PidGenX diagnostic.

Run the arithmetic self-tests with:

```sh
python vista_pkey2005_public_arithmetic_audit.py --self-test
```

Run an audit against a configuration file with:

```sh
python vista_pkey2005_public_arithmetic_audit.py pkeyconfig.xrm-ms -o arithmetic-report.json
python vista_pkey2005_crypto_audit.py pkeyconfig.xrm-ms -o crypto-report.json
python vista_pkey2005_research.py pkeyconfig.xrm-ms -o config-report.json
```

## Scope and safety

This project is limited to read-only inspection, public-parameter consistency
checks, and local validation using Microsoft's installed licensing component.
It does not generate product keys, recover or derive Microsoft's private
signing material, patch licensing binaries, alter validation results, or
activate Windows. Keep product keys, installation IDs, confirmation IDs, and
personal licensing data out of source control and CI logs.
