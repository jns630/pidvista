# Vista PKEY Configuration Release Comparison: Candidate Discovery

## Executive result

A second, clearly identified Vista operating-system `pkeyconfig.xrm-ms` file suitable for a like-for-like comparison was **not located** in the public references checked during this pass.

The supplied file remains identified by:

- Size: 620,662 bytes
- SHA-256: `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`
- Catalogue date: 2009-04-11

A third-party file catalogue lists this same size, date and SHA-256 for its Windows Vista entry. This independently corroborates the identity of the supplied file, but does not establish that no other Vista servicing versions exist.

## Candidate discovered: Microsoft VAMT ESU configuration

Microsoft's Download Center lists a separate file named `pkconfig_vista.xrm-ms`:

- Published: 2024-07-15
- Listed size: 656.8 KB
- Purpose: VAMT configuration update
- Microsoft says it enables VAMT to deploy and activate keys for Windows Server 2008 (alongside a separate Windows 7 configuration for Windows Server 2008 R2 / Windows 7 SP1 ESU).

Official listing:
https://www.microsoft.com/en-us/download/details.aspx?id=100304

**Important:** despite the `vista` filename, Microsoft's page identifies this file as the configuration for **Windows Server 2008** in the VAMT tool's configuration directory. It is not identified as a replacement or servicing revision of the Windows Vista operating-system file at `%windir%\\ServiceProfiles\\NetworkService\\AppData\\Roaming\\Microsoft\\SoftwareProtectionPlatform\\` or the Vista system licensing configuration location. It must not be treated as a second Vista OS release without inspecting its contents and context.

## Other catalogue evidence

A public Microsoft-file catalogue indexes separate configuration files for Windows 7 / Server 2008 R2, Windows 8 / Server 2012, and Windows 8.1 / Server 2012 R2. Its current index also lists separate product-specific game configurations such as Flight Simulator X, Flight Simulator X Acceleration, Gears of War, Halo 2 for Windows Vista, and Shadowrun. These are distinct product configurations, not evidence of alternate Vista OS servicing releases.

A public technical reference describes the Vista development transition: early builds used `pkeyconfig.xml`, renamed to `pkeyconfig.xrm-ms` in build 5259; early builds 5048 and 5071 used a different structure and PKey986, while later builds from 5098 adopted the later structure. This suggests beta-era files could be a separate historical comparison target, but they are not directly interchangeable with a 2009 Vista RTM/SP2-era configuration.

## What is and is not established

Established:

1. The supplied 620,662-byte file matches the independently catalogued Vista file hash.
2. Microsoft publishes a later VAMT file called `pkconfig_vista.xrm-ms`, but describes it as the Windows Server 2008 VAMT configuration.
3. Other Windows and game-specific PKeyConfig files exist in the public archive index.

Not established:

1. That the 656.8 KB VAMT file is a Vista OS pkeyconfig release.
2. That the supplied 2009 file is the only Vista OS pkeyconfig version.
3. That the VAMT file shares the same inner schema, public-key groups, or signing parameters.
4. Any cross-release change to Vista's 14 public-key groups.

## Required next input for a valid byte-level comparison

To complete a defensible cross-release diff, obtain one additional file with its provenance recorded, ideally one of:

- a Vista RTM / SP1 / SP2 system copy of `pkeyconfig.xrm-ms` from a documented build;
- a Vista beta-era `pkeyconfig.xml` / `.xrm-ms` file, clearly labelled with its build number (an intentionally separate historical schema comparison); or
- the Microsoft VAMT `pkconfig_vista.xrm-ms` file, if the research goal is broadened to compare the Server 2008 VAMT config with the Vista public format.

Record source URL, original path, file size, SHA-256, OS/build and whether it came from an installed system or a deployment tool. Then compare the outer wrapper, embedded infoBin XML, configuration and key-range counts, public-key group IDs, shared field-data bytes, point-vector bytes, pairing-reference bytes, and signature metadata.

## Sources

- Microsoft Download Center, VAMT ESU Configuration: https://www.microsoft.com/en-us/download/details.aspx?id=100304
- Vista pkeyconfig file metadata and SHA-256 listing: https://www.winpcware.com/extension/xrm-ms/pkeyconfig-xrm-ms
- Microsoft file catalogue: https://files.rg-adguard.net/
- PKeyMaster technical documentation on Vista build history: https://github.com/ntriver-org/ntriver-org-site/blob/main/docs/pkeymaster/docs/key-checker.mdx

This report deliberately records the candidate as unverified for Vista OS comparison rather than assuming equivalence from its filename.
