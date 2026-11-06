# Vista PKEY2005 Configuration-Level Group Analysis

## Input and scope

Extracted from the supplied `pkeyconfig.xrm-ms` file (SHA-256 `792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`). This is a metadata-only analysis of `Configuration` and linked `KeyRange` records.

## Complete group summary

| Group | Configurations | Key ranges | Distinct EditionIds | ProductKeyTypes |
|---:|---:|---:|---:|---|
| 140 | 10 | 10 | 2 | OEM:COA, OEM:NONSLP, OEM:SLP, Retail |
| 142 | 23 | 392 | 14 | OEM:COA, OEM:NONSLP, Retail, Volume:CSVLK, Volume:GVLK, Volume:MAK |
| 144 | 7 | 33 | 7 | OEM:COA |
| 146 | 21 | 94 | 8 | OEM:NONSLP, OEM:SLP, Retail |
| 148 | 1 | 5 | 1 | OEM:COA |
| 150 | 32 | 141 | 15 | OEM:COA, OEM:NONSLP, OEM:SLP, Retail |
| 152 | 41 | 168 | 27 | OEM:COA, Retail, Volume:CSVLK, Volume:GVLK, Volume:MAK |
| 154 | 21 | 50 | 10 | OEM:COA, OEM:SLP, Retail, Volume:CSVLK, Volume:MAK |
| 156 | 8 | 85 | 7 | OEM:NONSLP, Retail |
| 158 | 4 | 8 | 4 | OEM:COA, OEM:NONSLP |
| 160 | 1 | 5 | 1 | OEM:COA |
| 162 | 1 | 8 | 1 | OEM:COA |
| 164 | 31 | 98 | 12 | OEM:COA, OEM:NONSLP, OEM:SLP, Retail |
| 166 | 10 | 23 | 6 | OEM:COA, OEM:NONSLP |

## Exact Vista edition/configuration examples

These examples are exact rows from the supplied file. The identifier is the `ActConfigId`; range counts refer to KeyRange rows linked by `RefActConfigId`.

| Group | Edition | ProductKeyType | ActConfigId | Ranges | ProductDescription |
|---:|---|---|---|---:|---|
| 142 | Ultimate | Retail | `{30fab9cc-8614-4339-989f-7ce61fb7a5c4}` | 112 | Windows Vista Ultimate Retail |
| 142 | Business | Retail | `{9de9abe2-d01d-4538-af84-4498bdbc2ba3}` | 73 | Windows Vista Business Retail |
| 142 | HomeBasic | Retail | `{95c6e80a-0ff8-4bd0-95f2-c4a39b79d09e}` | 61 | Windows Vista Home Basic Retail |
| 142 | HomePremium | Retail | `{9e042223-03bf-49ae-808f-ff37f128d40d}` | 69 | Windows Vista Home Premium Retail |
| 144 | HomePremium | OEM:COA | `{a4eec485-e375-48b4-8f51-80d13a4086b6}` | 4 | Windows Vista Home Premium - OEM:COA |
| 144 | HomeBasic | OEM:COA | `{91dbad68-4713-4f9c-b351-6e77a8361741}` | 12 | Windows Vista Home Basic - OEM:COA |
| 146 | Business | OEM:NONSLP | `{177df7ed-709f-454a-91bd-947ec8a1e668}` | 11 | Windows Vista Business - OEM:NONSLP |
| 146 | HomeBasic | OEM:NONSLP | `{bb4c2c10-dc0d-4ce6-8824-ee71ddb63c07}` | 12 | Windows Vista Home Basic - OEM:NONSLP |
| 150 | Business | OEM:NONSLP | `{86e0a073-040b-4e10-aaf1-55f75482b5a4}` | 4 | Windows Vista SP1 Business OEM:NONSLP |
| 152 | HomeBasic | OEM:COA | `{f23dba60-517a-4184-bd26-066d9e3c19a9}` | 1 | Windows Vista SP2 Home Basic OEM:COA |
| 154 | Business | OEM:COA | `{0101b69a-85c8-4344-8196-7a16a7790bb5}` | 3 | Windows Vista Business - OEM:COA |
| 156 | Business | OEM:NONSLP | `{093e8e65-b6ab-4526-ab64-ae4e8269b656}` | 10 | Windows Vista Business - OEM:NONSLP |
| 158 | HomePremium | OEM:COA | `{da0483a8-c443-45fd-9b52-2bba9b2ee8ab}` | 1 | Windows Vista SP2 Home Premium OEM:COA |
| 160 | HomeBasic | OEM:COA | `{b4b150d0-ec09-4f74-910d-371ed161b2ac}` | 5 | Windows Vista Home Basic - OEM:COA |
| 162 | Business | OEM:COA | `{b13b0123-8661-4ee2-afb7-05c37481686b}` | 8 | Windows Vista Business - OEM:COA |
| 164 | HomePremium | OEM:COA | `{e05164a4-fb9a-471f-8c3a-6959b4cf1b72}` | 8 | Windows Vista SP2 Home Premium OEM:COA |
| 166 | HomeBasic | OEM:NONSLP | `{657fd7f1-652f-4a7f-9cef-e45e60f8b4c7}` | 4 | Windows Vista SP2 Home Basic OEM:NONSLP |

## Findings

1. **Group 142 is the main Vista retail/volume convergence group in this file.** It includes the large retail ranges for Ultimate, Business, Home Basic and Home Premium, plus configurations labelled GVLK, MAK and CSVLK. Its 392 linked ranges are the highest group total.
2. **Group 144 is a clean OEM:COA-only subset.** It contains seven configurations covering Business, Business N, Home Basic, Home Basic N, Home Premium, Starter and Ultimate.
3. **Group 146 is predominantly OEM service-channel material**, with OEM:SLP and OEM:NONSLP entries, D-OEM variants, plus a small number of Retail-labeled SP2 configurations.
4. **Group 152 is the broadest configuration family by count** (41 configurations and 27 distinct EditionIds). Its configuration records span Vista and Windows Server product families and include OEM:COA, Retail and volume types.
5. **Group 150 is strongly server-oriented** in the configuration records, including Windows Server 2008, Small Business Server, HPC and related server products, alongside one Vista Business SP1 OEM:NONSLP entry.
6. **Group 164 is also server-heavy**, including Medium Business Server and Storage Server editions, plus several Vista SP2 OEM configurations.
7. **Groups 148, 160 and 162 are narrow COA-specific groupings** in this file: one configuration each. Group 148 maps Home Premium, 160 Home Basic, and 162 Business.
8. **Groups 156 and 166 are OEM:NONSLP/OEM:COA mixed families**, with group 156 containing mostly OEM:NONSLP and one Retail configuration, and group 166 containing SP2 OEM:COA and OEM:NONSLP records.

## Extraction checks and caveats

- 211 Configuration records and 1,120 KeyRange records were parsed.
- All KeyRange `RefActConfigId` values resolved to a Configuration `ActConfigId`.
- Every Configuration had at least one linked KeyRange.
- `ProductKeyType` is the configuration's declared channel/type; `EulaType` is a separate property on each linked KeyRange. They should not be conflated.
- The supplied configuration file's metadata does not prove that a product key is genuine, owned, entitled, accepted by online activation, or transferable.
- These counts describe only the file identified by the SHA-256 above; do not generalize them to every Vista configuration release.
