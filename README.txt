pidvista — Windows Vista PKEY2005 research and local validation
=================================================================

The repository contains read-only Vista PKEY2005 configuration research and a
local diagnostic that calls the PidGenX export from the installed Vista system.
It does not generate keys, modify licensing state, bypass validation, or
activate Windows.

LOCAL VALIDATOR
---------------
Source: VistaPidGenXCheck.cpp
Workflow: .github/workflows/c-cpp.yml
Artifact: VistaPidGenXCheck-x64

The x64 checker loads:
  C:\Windows\System32\pidgenx.dll
  C:\Windows\System32\licensing\pkeyconfig\pkeyconfig.xrm-ms

To build:
1. Open the private repository's Actions tab.
2. Select "Build VistaPidGenXCheck".
3. Select "Run workflow".
4. Download the VistaPidGenXCheck-x64 artifact.
5. Copy the EXE to Vista SP2 x64 and run it locally.
6. Enter the test key only at the local prompt.

The workflow compiles and checks the PE architecture/subsystem. It cannot run
Vista's PidGenX DLL on the hosted runner. Actual PidGenX testing must occur on
the Vista computer. The key is not sent by this program; never put keys in
workflow inputs, repository files, logs, or issues.

Interpretation:
- HRESULT 0 means the installed local PidGenX/config pair accepted the input
  for local product-ID processing.
- A nonzero HRESULT means local processing failed; inspect the exact HRESULT,
  edition/channel, and local configuration version.
- This is not an activation result or proof of licence ownership or transfer.

PUBLIC CONFIGURATION FINDINGS
-----------------------------
Three supplied configuration copies were identical:
  Size:   620,662 bytes
  SHA256: 792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10

Decoded structure:
  211 Configuration entries
  1,120 KeyRange entries
  14 public-key groups: 140, 142, 144, 146, 148, 150, 152, 154,
                        156, 158, 160, 162, 164, 166
  1,579 bytes per decoded public-key record
  Algorithm: msft:rm/algorithm/pkey/2005

Public parameters recovered by the audit:
  p = 886368969471450739924935101400677
  n = 886368969471450710152985728350703
  K3 polynomial: u^3 + u + 4
  K6/K3 polynomial: t^2 + 2

The arithmetic audit checks public record structure, probable-prime
consistency, extension-field operations, twist points, and the stored pairing
element's subgroup relation. It is not a complete product-key signature test.

SAMPLE-KEY STATUS
-----------------
The sample key examined offline decoded to a 112-bit Base24 integer. Its
quotient on division by p was 4 and passed the preliminary quotient-bound
check. Its x-coordinate admitted candidate y coordinates on the reconstructed
base curve. These checks are only preliminary structural plausibility checks.

FINAL VERDICT: UNVERIFIED. The complete PKEY2005 signature/pairing comparison
was not performed. Do not label the sample key valid or invalid from these
partial checks. Test it with the local Vista PidGenX checker.

RESEARCH UTILITIES
------------------
vista_pkey2005_research.py
  XML/configuration structure inspector.

vista_pkey2005_crypto_audit.py
  Public record and parameter audit.

vista_pkey2005_public_arithmetic_audit.py
  Extension-field, twist-point, and pairing-subgroup consistency audit.

VistaPidGenXCheck.cpp
  Local PidGenX diagnostic; Vista x64 paths are currently hard-coded.

Self-test:
  python vista_pkey2005_public_arithmetic_audit.py --self-test

Config audits:
  python vista_pkey2005_public_arithmetic_audit.py pkeyconfig.xrm-ms -o arithmetic-report.json
  python vista_pkey2005_crypto_audit.py pkeyconfig.xrm-ms -o crypto-report.json
  python vista_pkey2005_research.py pkeyconfig.xrm-ms -o config-report.json

SCOPE
-----
Read-only research and local validation only. No key generation, private
signing-material recovery, licensing-binary patching, validation bypass, or
activation. Do not commit product keys, PIDs, IIDs, CIDs, or personal license
data.
