# Vista PKEY2005 Public-Key Group to Licensing-Configuration Map

## Scope

This report maps the 14 public-key group IDs in the supplied Vista XrML configuration to the `Configuration` and `KeyRange` records that reference them.

It is a metadata linkage audit only. It does not generate, validate, or alter product keys, and it does not infer activation entitlement from configuration metadata.

Input file SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

## Linkage validation

The supplied file contains:

- 211 `Configuration` records;
- 1,120 `KeyRange` records;
- 14 public-key groups: 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164 and 166;
- 791 distinct part-number strings.

Every `KeyRange` reference resolved to a `Configuration` by matching `RefActConfigId` to `ActConfigId`. Every configuration had at least one associated key range.

## Group coverage

| Public-key group | Configurations | Key ranges | Channel classification |
|---:|---:|---:|---|
| 140 | 10 | 10 | Mixed |
| 142 | 23 | 392 | Mixed — 6 types |
| 144 | 7 | 33 | OEM:COA only |
| 146 | 21 | 94 | Mixed |
| 148 | 1 | 5 | OEM:COA only |
| 150 | 32 | 141 | Mixed |
| 152 | 41 | 168 | Mixed |
| 154 | 21 | 50 | Mixed |
| 156 | 8 | 85 | Retail / OEM:NONSLP |
| 158 | 4 | 8 | OEM:COA / OEM:NONSLP |
| 160 | 1 | 5 | OEM:COA only |
| 162 | 1 | 8 | OEM:COA only |
| 164 | 31 | 98 | Mixed |
| 166 | 10 | 23 | OEM:COA / OEM:NONSLP |

The four groups used exclusively by `OEM:COA` configurations are 144, 148, 160 and 162.

Group 156 is used by Retail and `OEM:NONSLP` configurations, but not exclusively by either one. Group 158 and 166 are used by `OEM:COA` and `OEM:NONSLP` configurations.

Group 142 has the largest key-range count (392) and is associated with six channel types. Group 152 has the largest number of configurations (41).

## What the mapping tells us

1. A public-key group is not generally a one-to-one identifier for a single licensing channel. Most groups are classified as mixed.
2. The four `OEM:COA)-only groups are a distinct subset in this configuration file, but this observation alone does not establish a separate signature algorithm or different curve parameters.
3. Group 142 is especially broadly reused in the configuration metadata: 23 configurations and 392 key ranges.
4. The same common mathematical parameter prefix across all 14 public-key records is consistent with the group IDs selecting different public point vectors and pairing references within a shared parameter framework.

## Important interpretation limits

- A channel classification here describes the `Configuration` / `KeyRange` metadata in the supplied file.
- It does not prove that a key is genuine, owned, entitled, installed, or activatable.
- It does not establish that group IDs are interchangeable.
- It does not establish that channel labels correspond to different cryptographic algorithms.
- This is one supplied Vista configuration file; do not generalize the counts to every Vista build or servicing state.

## Recommended follow-on

A useful next metadata-only investigation is to identify the exact `Configuration` identifiers and product descriptions associated with each group, then compare their edition/channel labels. That can show whether group reuse follows edition, channel, product family, or another configuration dimension without attempting to recover any private signing material.
