#!/usr/bin/env python3
"""Structural-only inspector for Vista PKEY2005 public-key records.

Parses XrML infoBin and checks documented serialized field/point boundaries.
It does not accept product keys, generate keys, calculate H1, recover secrets,
or verify signatures/pairings.
"""
import argparse, base64, hashlib, json, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

OUTER_MAGIC, FIELD_MAGIC, VERSION = 0x44556677, 0x00112233, 0x0100

def local(tag):
    return tag.rsplit("}", 1)[-1]

def u16(b, o):
    return struct.unpack_from("<H", b, o)[0]

def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]

def inspect(blob, group_id=""):
    if len(blob) < 12:
        raise ValueError("record shorter than outer header")
    magic, version, field_size = u32(blob, 0), u16(blob, 4), u32(blob, 8)
    if magic != OUTER_MAGIC or version != VERSION:
        raise ValueError("outer magic/version mismatch")
    fs, fe = 12, 12 + field_size
    if fe > len(blob) or field_size < 48:
        raise ValueError("invalid field-data bounds")
    f = blob[fs:fe]
    if u32(f, 0) != FIELD_MAGIC or u16(f, 4) != VERSION:
        raise ValueError("field magic/version mismatch")
    size_bn = blob[0x15]
    must_zero, size_mod, size_order = f[8], f[9], f[10]
    d1, d2 = u32(f, 11), u32(f, 15)
    unused = {hex(o): u32(f, o) for o in (19, 23, 27, 35, 39, 43)}
    offset_modulus = u32(f, 31)
    point_count, maxq = size_mod, f[47]
    if not size_bn or size_mod != size_bn or not size_order or not d1 or not d2 or not point_count:
        raise ValueError("invalid zero or inconsistent dimensions")
    if point_count > 1024 or d1*d2 > 4096:
        raise ValueError("implausible dimensions")
    cur = 48
    def take(n, name):
        nonlocal cur
        a, z = cur, cur+n
        if z > len(f):
            raise ValueError(name + " exceeds field-data region")
        cur = z
        return [fs+a, fs+z]
    h1 = take(size_mod, "H1 radix vector")
    modulus = take(size_mod, "modulus")
    order = take(size_order, "order")
    poly1 = take(d1+1, "extension polynomial 1")
    poly2 = take(d2+1, "extension polynomial 2")
    base_a = take(size_bn, "base curve a")
    base_b = take(size_bn, "base curve b")
    curve_a = take(size_bn, "curve a")
    curve_b = take(size_bn, "curve b")
    padding = f[cur:]
    point_size = 6*size_bn
    p0, p1 = fe, fe+point_count*point_size
    pairing_size = d1*d2*size_bn
    q1 = p1+pairing_size
    if q1 != len(blob):
        raise ValueError("computed point/pairing end differs from record length")
    return {
        "group_id": group_id, "record_length": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "outer_magic": hex(magic), "format_version": hex(version),
        "field_data_size": field_size, "field_data_bounds": [fs, fe],
        "field_magic": hex(u32(f, 0)), "field_version": hex(u16(f, 4)),
        "size_bignum": size_bn, "must_be_zero": must_zero,
        "size_modulus": size_mod, "size_order": size_order,
        "extension_degree_1": d1, "extension_degree_2": d2,
        "documented_unused_words": unused, "offset_modulus": offset_modulus,
        "point_count_from_size_modulus": point_count,
        "max_quotient_byte": maxq, "h1_radix_vector_bounds": h1,
        "modulus_bounds": modulus, "order_bounds": order,
        "extension_polynomial_1_bounds": poly1, "extension_polynomial_2_bounds": poly2,
        "base_curve_a_bounds": base_a, "base_curve_b_bounds": base_b,
        "curve_a_bounds": curve_a, "curve_b_bounds": curve_b,
        "field_data_schema_bytes_consumed": cur,
        "field_data_trailing_padding_bytes": len(padding),
        "field_data_trailing_padding_all_zero": all(x == 0 for x in padding),
        "point_block_size": point_size, "points_bounds": [p0, p1],
        "pairing_reference_size": pairing_size, "pairing_reference_bounds": [p1, q1],
        "checks": {"outer_header": True, "field_header": True,
                   "field_members_in_bounds": True, "point_vector_in_bounds": True,
                   "pairing_reference_in_bounds": True, "record_ends_after_pairing": True}
    }

def parse(path):
    root = ET.parse(path).getroot()
    info = next((e for e in root.iter() if local(e.tag) == "infoBin"), None)
    if info is None or not (info.text or "").strip():
        raise ValueError("missing XrML infoBin")
    inner = ET.fromstring(base64.b64decode("".join(info.text.split()), validate=True))
    rows = []
    for group in inner.iter():
        if local(group.tag) != "PublicKey":
            continue
        gid = next((e.text for e in group.iter() if local(e.tag) == "GroupId"), "") or ""
        val = next((e.text for e in group.iter() if local(e.tag) == "PublicKeyValue"), None)
        if val:
            rows.append(inspect(base64.b64decode("".join(val.split()), validate=True), gid))
    if not rows:
        raise ValueError("no PublicKeyValue records found")
    return rows

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xrm_ms", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    try:
        rows = parse(args.xrm_ms)
        report = {"input": args.xrm_ms.name, "public_key_count": len(rows),
                  "field_data_sizes": sorted(set(r["field_data_size"] for r in rows)),
                  "all_common_prefix_layouts_equal": len(set(
                      tuple((k, str(v)) for k,v in r.items()
                            if k not in ("group_id", "sha256", "record_length", "checks"))
                      for r in rows)) == 1,
                  "records": rows,
                  "scope": "Structural only; no product-key validation, signature verification, key generation, or secret recovery."}
        output = json.dumps(report, indent=2) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
        return 0
    except (OSError, ValueError, ET.ParseError, struct.error) as e:
        print("ERROR:", e, file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
