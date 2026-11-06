# Vista PKEY2005 group 142: cross-configuration reuse audit

## Scope and source

This audit examines every `Configuration` entry in the supplied Vista
`pkeyconfig.xrm-ms` that references `RefGroupId=142`, then joins its
`KeyRange` entries by `KeyRange.RefActConfigId` to
`Configuration.ActConfigId`.

Source file SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

The source contains 211 configurations, 1,120 key ranges, and 14 public-key
groups. The 1,120 range-to-configuration references matched in the earlier
full-file audit.

## 1. Group 142 aggregate

| Metric | Result |
|---|---:|
| Configurations referencing group 142 | 23 |
| KeyRange records attached to those configurations | 392 |
| ProductKeyType categories | 6 |
| Configurations with IsRandomized=false | 23 |
| Configurations with IsRandomized=true | 0 |

### Distribution by ProductKeyType

| ProductKeyType | Configurations | KeyRange records |
|---|---:|---:|
| Retail | 13 | 377 |
| Volume:CSVLK | 1 | 1 |
| Volume:MAK | 1 | 2 |
| Volume:GVLK | 4 | 8 |
| OEM:NONSLP | 2 | 2 |
| OEM:COA | 2 | 2 |
| **Total** | **23** | **392** |

This establishes that group 142 is not a one-channel or one-edition label in
this configuration file.

## 2. Retail configurations using group 142

| EditionId | Product description | Key ranges | Distinct part numbers |
|---|---|---:|---:|
| Ultimate | Windows Vista Ultimate Retail | 112 | 70 |
| Business | Windows Vista Business Retail | 73 | 48 |
| BusinessN | Windows Vista Business N Retail | 19 | 13 |
| HomeBasic | Windows Vista Home Basic Retail | 61 | 35 |
| HomeBasicN | Windows Vista Home Basic N Retail | 9 | 7 |
| HomePremium | Windows Vista Home Premium Retail | 69 | 42 |
| Enterprise | Windows Vista Enterprise Retail | 2 | 2 |
| OCUR | Windows Vista OCUR add-on Retail | 3 | 2 |
| UltimateN | Windows Vista Ultimate N Retail | 13 | 8 |
| Starter | Windows Vista Starter Retail | 4 | 4 |
| HomePremiumN | Windows Vista Home Premium N Retail | 10 | 6 |
| CodecPack | Windows Vista CODEC add-on Retail | 1 | 1 |
| EnterpriseN | Windows Vista EnterpriseN Retail | 1 | 1 |
| **Total** | | **377** | |

The 13 Retail configuration entries span core Vista editions, N editions,
Starter, Enterprise, and add-on configurations. The group assignment alone
does not imply that these products are interchangeable.

## 3. Non-Retail configurations using group 142

| ProductKeyType | EditionId | Product description | Key ranges |
|---|---|---|---:|
| Volume:CSVLK | n/a | Windows Vista ALL Volume SKUs - CSVLK | 1 |
| Volume:MAK | n/a | Windows Vista ALL Volume SKUs - MAK | 2 |
| Volume:GVLK | Business | Windows Vista Business - GVLK | 2 |
| Volume:GVLK | BusinessN | Windows Vista Business N - GVLK | 2 |
| Volume:GVLK | Enterprise | Windows Vista Enterprise - GVLK | 2 |
| Volume:GVLK | EnterpriseN | Windows Vista EnterpriseN GVLK | 2 |
| OEM:NONSLP | Starter | Windows Vista SP2 Starter OEM:NONSLP | 1 |
| OEM:NONSLP | Ultimate | Windows Vista SP2 Ultimate OEM:NONSLP | 1 |
| OEM:COA | HomeBasic | Windows Vista SP2 Home Basic OEM:COA | 1 |
| OEM:COA | Business | Windows Vista SP2 Business OEM:COA | 1 |

The four GVLK configurations contribute eight ranges. The CSVLK, MAK,
OEM:NONSLP, and OEM:COA entries account for the remaining non-Retail ranges.

## 4. What group reuse means

The PKEY configuration schema associates each configuration with a
`RefGroupId`, and public-key records are indexed by `GroupId`. Therefore,
all 23 configurations that reference group 142 resolve to the same
group-142 public-key record in this file. They do not each have a separate
public-key record merely because their editions or ProductKeyType values
differ.

This is a configuration-indexing observation. It does **not** establish that
all 23 configurations accept the same product key, that keys are
interchangeable, or that a key accepted for one edition is valid for another.
The individual key-range metadata and native product configuration remain
relevant.

The public-key record for group 142 is distinct from the record for group
144. The earlier audit found that the 14 records share the same recovered
PKEY2005 mathematical domain parameters, while their serialized records
and pairing-reference fields differ. Those structural facts do not constitute
a full signature/pairing verification of any key.

## 5. Connection to the two observed PidGenX tests

The user's Retail Home Basic screenshot maps to the group-142
`HomeBasic` / `Retail` configuration. The earlier Home Premium OEM:COA
screenshot maps to group 144.

| Observation | Home Basic test | Home Premium test |
|---|---|---|
| ProductKeyType | Retail | OEM:COA |
| Group ID | 142 | 144 |
| PidGenX HRESULT | 0x0 | 0x0 |
| Local PidGenX result | Accepted | Accepted |

These results show that the installed PidGenX/configuration pair returned
success for those two particular inputs. They do not test every configuration
that references group 142, and do not prove entitlement, ownership, online
activation, or global validity.

## 6. Conclusions

1. Group 142 is referenced by 23 configurations and 392 key ranges in the
   supplied configuration file.
2. It is reused across six ProductKeyType categories, including Retail,
   Volume, OEM:NONSLP, and OEM:COA.
3. Thirteen Retail entries cover multiple Vista editions and add-on products.
4. All 23 configurations have `IsRandomized=false` in this file.
5. Because the public-key table is keyed by GroupId, all these configurations
   reference the same group-142 public-key record.
6. Group reuse is not evidence that keys are interchangeable or that every
   configuration has been independently tested.
7. The two screenshot-based PidGenX results remain local offline observations,
   not proof of activation or licensing entitlement.

## 7. Reproduction outline

1. Decode the outer XrML `infoBin` Base64 payload to embedded XML.
2. Select all `Configuration` elements where `RefGroupId` equals `142`.
3. For each selected configuration, collect `KeyRange` elements whose
   `RefActConfigId` equals its `ActConfigId`.
4. Aggregate by `ProductKeyType`, `EditionId`, and `ProductDescription`.
5. Compare the selected group ID to the `PublicKey/GroupId` index.
6. Keep XML-derived configuration metadata separate from screenshot-derived
   native PidGenX results and from online activation status.

## References

- PKEY configuration record structure and field meanings:
  https://github.com/awuctl/licensing-stuff/blob/main/docs/details.md
- Example parser showing configuration, range, and public-key joins:
  https://github.com/awuctl/licensing-stuff/blob/main/pkeyconfig.py
- PidGenX and matching Vista configuration usage:
  https://ntriver.org/pkeymaster/docs/key-checker

Source data: user-supplied Vista `pkeyconfig.xrm-ms` file and PidGenX
screenshots. This report records metadata analysis only; it does not generate
product keys, recover private signing material, or bypass activation.
