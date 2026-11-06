# PKEY2005 public-key record byte-structure comparison

## Scope and source

This audit compares the 14 `PublicKeyValue` blobs in the supplied Vista
`pkeyconfig.xrm-ms` file. It is a byte-level structural comparison only.
It does not attempt to derive signing secrets, generate product keys, or
validate a product-key signature.

Source file SHA-256:

`792455ee1f192dd77ec6dec882742ddabfa873f222b2456e152f9263b557de10`

All 14 records declare:

`msft:rm/algorithm/pkey/2005`

Each Base64-decoded record is 1,579 bytes.

## 1. Identical header and group-specific tail

A byte-for-byte comparison of all 14 records finds:

| Region | Offset interval (end exclusive) | Length | Observation |
|---|---:|---:|---|
| Common prefix | 0–319 | 319 bytes | Identical across all 14 records |
| Group-specific tail | 319–1579 | 1,260 bytes | All 14 tails are distinct |

Every byte position in the first 319 bytes is identical across the records.
The 1,260-byte suffix differs for every group.

This is a stronger structural observation than comparing whole-record
fingerprints alone: it localizes the variation to the suffix while showing
that the prefix is shared.

## 2. Fixed-width block comparison

For descriptive comparison, the 1,260-byte suffix can be divided into
15 consecutive blocks of 84 bytes:

| Block | Start offset | End offset (exclusive) | Distinct block values across groups |
|---:|---:|---:|---:|
| 1 | 319 | 403 | 14 |
| 2 | 403 | 487 | 14 |
| 3 | 487 | 571 | 14 |
| 4 | 571 | 655 | 14 |
| 5 | 655 | 739 | 14 |
| 6 | 739 | 823 | 14 |
| 7 | 823 | 907 | 14 |
| 8 | 907 | 991 | 14 |
| 9 | 991 | 1075 | 14 |
| 10 | 1075 | 1159 | 14 |
| 11 | 1159 | 1243 | 14 |
| 12 | 1243 | 1327 | 14 |
| 13 | 1327 | 1411 | 14 |
| 14 | 1411 | 1495 | 14 |
| 15 | 1495 | 1579 | 14 |

Each 84-byte block has 14 distinct byte strings across the 14 groups.
The block partition is an observational aid; this table does not assign
cryptographic meaning to individual blocks.

## 3. Pairwise byte differences

There are 91 unordered pairs among 14 records. Across those pairs, the
number of byte positions that differ ranges from **1,246 to 1,258** out of
1,579 bytes.

The small common prefix accounts for the large shared portion of each pair.
The rest is highly group-specific at the byte level.

## 4. Interpretation

The evidence supports these limited conclusions:

1. All 14 records use the same declared PKEY2005 algorithm identifier.
2. All records share an identical 319-byte prefix.
3. Every group has a distinct 1,260-byte suffix.
4. Under the descriptive 84-byte partition, every suffix block differs
   across all 14 groups.
5. The serialized public-key records are therefore not merely copies with
   a small group-ID field changed.

The earlier configuration audit found shared mathematical-domain
parameters across the groups. Together, these observations are consistent
with a common PKEY2005 format/domain and group-specific public-key material.

They do **not** prove that every group has an independently generated
signing key, identify the semantic meaning of every byte range, or establish
signature validity for any product key. A distinct public-key record hash
is not a signature-verification result.

## 5. Reproduction

1. Parse the outer XrML and Base64-decode the `infoBin` element.
2. Locate each `PublicKey` element and read `GroupId`,
   `AlgorithmId`, and `PublicKeyValue`.
3. Base64-decode `PublicKeyValue` into bytes.
4. Confirm each record length is 1,579 bytes.
5. Compare bytes 0–318 across all records.
6. Compare bytes 319–1578 across all records.
7. For a descriptive fixed-width view, partition the suffix into 15
   consecutive 84-byte blocks and compare each block across groups.
8. Compute pairwise Hamming distances over byte positions (not bit
   positions) for all 91 record pairs.

## 6. Safety and validation boundary

This repository's investigation remains limited to configuration parsing,
public-record fingerprints, and structural consistency. No private signing
material was recovered, no signing coefficients were searched for, and no
key-generation or signature-forging operation was performed.

The local PidGenX HRESULT observations recorded elsewhere in this repository
are separate native DLL/configuration acceptance results. They should not
be conflated with a complete independent PKEY2005 mathematical signature
verification or with online activation and licence entitlement.
