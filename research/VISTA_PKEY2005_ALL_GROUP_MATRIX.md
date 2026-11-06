# Vista PKEY2005: complete public-key group/configuration matrix

## Scope and source

This audit parses the embedded XML in the supplied Vista `pkeyconfig.xrm-ms`.
Source file size: 620,662 bytes. SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The XML contains 211 `Configuration` entries, 1,120 `KeyRange` entries,
and 14 `PublicKey` records. All key ranges were joined to configurations by
`KeyRange.RefActConfigId` -> `Configuration.ActConfigId`. All 1,120 references
matched. Each of the 14 groups has a public-key record.

This report summarizes configuration metadata and cryptographic-record
fingerprints. It does not publish private material, generate product keys,
or claim signature verification.

## 1. Complete group matrix

| Group | Configurations | Key ranges | ProductKeyType distribution |
|---:|---:|---:|---|
| 140 | 10 | 10 | OEM:COA 2; OEM:NONSLP 2; OEM:SLP 2; Retail 4 |
| 142 | 23 | 392 | OEM:COA 2; OEM:NONSLP 2; Retail 13; Volume:CSVLK 1; Volume:GVLK 4; Volume:MAK 1 |
| 144 | 7 | 33 | OEM:COA 7 |
| 146 | 21 | 94 | OEM:NONSLP 10; OEM:SLP 8; Retail 3 |
| 148 | 1 | 5 | OEM:COA 1 |
| 150 | 32 | 141 | OEM:COA 1; OEM:NONSLP 14; OEM:SLP 13; Retail 4 |
| 152 | 41 | 168 | OEM:COA 1; Retail 25; Volume:CSVLK 3; Volume:GVLK 9; Volume:MAK 3 |
| 154 | 21 | 50 | OEM:COA 7; OEM:SLP 4; Retail 7; Volume:CSVLK 1; Volume:MAK 2 |
| 156 | 8 | 85 | OEM:NONSLP 7; Retail 1 |
| 158 | 4 | 8 | OEM:COA 3; OEM:NONSLP 1 |
| 160 | 1 | 5 | OEM:COA 1 |
| 162 | 1 | 8 | OEM:COA 1 |
| 164 | 31 | 98 | OEM:COA 5; OEM:NONSLP 12; OEM:SLP 7; Retail 7 |
| 166 | 10 | 23 | OEM:COA 6; OEM:NONSLP 4 |
| **Total** | **211** | **1,120** | |

## 2. Group 144 is OEM:COA-only in this file

Group 144 has seven configurations and 33 key ranges. All seven
configurations have `ProductKeyType=OEM:COA`. Their editions are:

- Business
- Business N
- Home Basic
- Home Basic N
- Home Premium
- Starter
- Ultimate

All 33 ranges have `EulaType=OEM`. This supports the precise statement
that group 144 is assigned only to OEM:COA configurations in this supplied
configuration file. It does not establish that every Vista release or every
other pkeyconfig revision has the same assignment.

Group 144 is not the only group with OEM:COA-only assignment: groups 148,
160, and 162 are also exclusively OEM:COA in this file. Group 144 is
distinguished by having seven configurations rather than one.

## 3. Other notable group patterns

- Group 142 is the broadest mixed-channel group: 23 configurations and
  six ProductKeyType categories.
- Group 152 has the largest configuration count: 41. It includes Retail,
  Volume, and one OEM:COA configuration.
- Group 150 has 32 configurations, dominated by OEM:NONSLP and OEM:SLP
  entries, with some Retail and one OEM:COA entry.
- Group 164 has 31 configurations and spans OEM:COA, OEM:NONSLP, OEM:SLP,
  and Retail.
- Groups 148, 160, and 162 each have one OEM:COA configuration.
- Group 140 includes ServerHomePremium and ServerHomeStandard configuration
  entries, as well as Retail and OEM types. Group counts are not simple
  edition or channel identifiers.

## 4. Public-key record fingerprints

All 14 public-key records report algorithm
`msft:rm/algorithm/pkey/2005` and are 1,579 bytes after decoding.
Their complete-record and pairing-reference SHA-256 fingerprints are:

| Group | Complete record SHA-256 | Pairing-reference SHA-256 |
|---:|---|---|
| 140 | `85fee45dbf403458c482d5658d5311d64c0c3ba5c1c413d311b7054427a1efd5` | `0f73589598180bb700f5c2a11d2569b00ef1168c67ad325887bc9ad9f8a1b519` |
| 142 | `255befbd0b7207d59f03ee472880a0ae611c419387f59c290c0060fdd3b1c1e7` | `1eedb5fdc5b2dc734b3bca2c410d579eec9c058f5a61b8ebdb2a0467dd1a8c9e` |
| 144 | `10f913219d9c4c81d7eb22f40a34fb8179a08b99e3dddef2d71c1e8f8352d0c6` | `4fb2ff20dbcc399d580a7e5ba2fa264396eaf5965d84a60d25b3697a174a0c28` |
| 146 | `a0b40167a5d6e012c0351c395d29ebde67b8fe0ccfe6345b8fd8d16f7024f192` | `d24808256256ebd9865d113cae54e9302fb201151ad488a8b7eeb10b1b445440` |
| 148 | `ab6c6d662863736e58c5573bc27d5ebce22215efcf294320c3a7652e56a2488b` | `663c7cc50da92117d19ae3f0b840eecf268a5ae9fa8c98eeb815b439dcba3a3c` |
| 150 | `b6761c19f799d37769ab8625cf11d209587ab67c4411b8ff830299d7c49e17b2` | `bf04fd8f49b77253b8c7da68c78411a8a7c3555ecb674240eb0a2d33c086bbec` |
| 152 | `664d462c8f9c9e3e570bd124fa166538e5649312221dd55d0e364a63ff29f85c` | `de7d6ce92f753adc954353c7d145208c8e33c32e6d11ff12dbcc9b9cafa39c53` |
| 154 | `8acee341879c189134cf764fbf8c2ecd89ef1b696243991a63bbd2611959c8d6` | `43e250b6b3b56032a23a1544034fb5bd1386e1235336a3e8b42bd24e5ff60067` |
| 156 | `89321511dc57b087e2d48449cf3338c830368a5a5725add5d3df1400045ffcfc` | `36b6fb7edf4e272683c79fe390d1d96b2aa91829c9a9a6a66b1befe7f841cb8a` |
| 158 | `1006660c96c45a59e592404f6fa6c70a8c8281198d3d56620d8740cf1e7bfe99` | `c87b1ffa36dda0981b9d57bff6b4b4af24bf3652574c571c8fadbf023bc7eaa2` |
| 160 | `6d7a17c12c1df64f30de2eef5908f1bda87c29c0a06f979344ad6056bf8b3269` | `fa2b459cb8d81fcaa792bea1edfe4c24fa372189ee724defb372ea048e6bddcc` |
| 162 | `1eefdda48a648a7d03f43d78839c4654e8bfd6870da0d022576e5e039b69582c` | `f31e7fd9967ad18b6a6fbe860dcc00c96e50798dd0110b5b955c1d69e6392c1f` |
| 164 | `be2b9980f3406313167ccfbc6e7615239e1520b784cc65c9506e4cf49218b929` | `ed1ac33a897c4565c50fecbd5c991c9b2dc69255939aaf8188668dc30763e252` |
| 166 | `fa6f7d143f2e7d0c8f8004109488913c020dd41a9bc5c3cc6f3f88a0f2bb624a` | `341ee6b17b0530834bfbf49d146d88fa3345fc30060ce05dff7df0232f1f77a7` |

All complete-record hashes and all pairing-reference hashes are distinct.
The previous public-parameter audit found common field modulus, subgroup
order, and curve coefficients across the 14 records. Together these
observations show a common PKEY2005 mathematical domain with group-specific
serialized public-key records and pairing-reference data. Hash differences
alone do not prove independently generated signing keys, and this audit
does not perform the final PKEY2005 signature/pairing test.

## 5. Cross-check against the two local PidGenX observations

The two user-run screenshots previously recorded map to:

| Screenshot observation | Activation configuration | Group | ProductKeyType |
|---|---|---:|---|
| Home Basic, Edition ID X13-04106 | HomeBasic Retail | 142 | Retail |
| Home Premium OEM:COA | HomePremium OEM:COA | 144 | OEM:COA |

Both screenshots showed PidGenX HRESULT `0x0`. This means the installed
local DLL/configuration pair accepted the inputs for local processing. It
does not prove licence ownership, entitlement, transferability, or online
activation. The group mapping is derived from the Activation ID match in
the supplied XML, not inferred from the screenshot's edition name alone.

## 6. Interpretation and limitations

1. A group ID is a reference to a public-key record, not a synonym for an
   edition or channel.
2. Multiple configurations can reference the same group, including
   configurations with different ProductKeyType values.
3. Group 144's OEM:COA-only distribution is a property of this exact
   configuration file, not a universal claim about all Vista builds.
4. Distinct public-key record hashes establish byte-level differences only.
5. The audit is structural. It does not recover private signing material,
   generate keys, bypass licensing, or establish cryptographic validity.
6. PidGenX offline acceptance and Windows activation/licensing status are
   separate observations.

## 7. Reproduction

1. Decode the XrML `infoBin` Base64 value to embedded XML.
2. Parse every `Configuration` and `KeyRange`.
3. Join `KeyRange.RefActConfigId` to `Configuration.ActConfigId`,
   normalizing GUID braces and case.
4. Group configurations by `RefGroupId`.
5. Aggregate configuration count, key-range count, ProductKeyType and
   EditionId distributions.
6. Decode each `PublicKeyValue`, compute SHA-256 over the complete record,
   and separately fingerprint the 84-byte pairing-reference segment at
   offset 1495, as used in the prior parser audit.
7. Verify the input file SHA-256 before comparing output with this report.

Machine-readable snapshots: `vista_pkey2005_all_group_matrix.csv` and
`vista_pkey2005_all_group_matrix.json`.
