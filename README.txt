VistaPidGenXCheck — cloud build package
=======================================

This package builds a 64-bit Windows console EXE using GitHub Actions. It is
configured with a Windows Vista (6.00) PE subsystem target and static MSVC CRT
linking (/MT). The source calls the local Vista PidGenX DLL/config only; it does
not install a key, activate Windows, or make network requests at runtime.

BUILD STEPS (phone-friendly)
----------------------------
1. Sign in to https://github.com/ and create a NEW empty repository.
2. Upload the files/folders from this package, preserving this structure:
     VistaPidGenXCheck.cpp
     README.txt
     .github/workflows/build.yml
3. Open the repository's Actions tab.
4. Select “Build VistaPidGenXCheck” in the left panel.
5. Press “Run workflow”, then the green “Run workflow” button.
6. Wait for the run to finish successfully.
7. Open that completed run. At the bottom, under Artifacts, download
   “VistaPidGenXCheck-x64”. It is a ZIP containing the EXE and build headers.
8. Extract the ZIP and copy VistaPidGenXCheck.exe to the Vista x64 computer.

IMPORTANT COMPATIBILITY NOTE
----------------------------
The executable is built as x64 and marked with Windows subsystem version 6.00.
The build uses /MT to avoid a separate Visual C++ runtime installation. This
is a Vista-targeted build configuration, but final runtime compatibility still
needs testing on the actual Vista SP2 machine. Do not run it on a production
machine if Windows reports a missing DLL or unsupported entry point; report
that exact message so the build can be adjusted.

SECURITY
--------
The GitHub workflow compiles source code only. It does not receive a product
key. Enter your key only into the locally run program on your Vista computer.
Do not commit or upload any product key, PID, CID, or personal license data.

The program's PidGenX output is an offline local result, not proof of genuine
licensing, ownership, transferability, or activation.
