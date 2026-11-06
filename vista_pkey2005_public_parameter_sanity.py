#!/usr/bin/env python3
"""Read-only sanity checks for public PKEY2005 field and curve parameters.

Checks serialized dimensions, probable primality of the base-field modulus and
curve order, polynomial coefficient ranges/leading terms, H1 radix bounds,
the documented max-quotient relation, and non-singularity of the base curve.
It does not decode product keys, recover H1 vectors, solve discrete logs,
construct signatures, or perform signature/pairing verification.
"""
import argparse, base64, hashlib, json, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

MAGIC, FIELD_MAGIC, VERSION = 0x44556677, 0x00112233, 0x0100

def local(tag): return tag.rsplit("}", 1)[-1]
def u16(b, o): return struct.unpack_from("<H", b, o)[0]
def u32(b, o): return struct.unpack_from("<I", b, o)[0]
def le(b): return int.from_bytes(b, "little")

def probable_prime(n, rounds=32):
    if n < 2: return False
    small = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47)
    for q in small:
        if n == q: return True
        if n % q == 0: return False
    d, s = n-1, 0
    while d % 2 == 0: s += 1; d //= 2
    bases = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,
             59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131)
    for a in bases[:rounds]:
        if a >= n-1: continue
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1: break
        else: return False
    return True

def inspect(blob, gid):
    if len(blob) < 12 or u32(blob,0) != MAGIC or u16(blob,4) != VERSION:
        raise ValueError(f"group {gid}: invalid outer header")
    fs = u32(blob,8); f = blob[12:12+fs]
    if len(f) != fs or u32(f,0) != FIELD_MAGIC or u16(f,4) != VERSION:
        raise ValueError(f"group {gid}: invalid field header/bounds")
    bn, must_zero = blob[0x15], f[8]
    sm, so = f[9], f[10]
    d1, d2 = u32(f,11), u32(f,15)
    offset_modulus = u32(f,31)
    if bn != sm or not sm or not so or not d1 or not d2:
        raise ValueError(f"group {gid}: inconsistent public dimensions")
    # Published layout: point count is size_modulus; offset_modulus is a
    # separate 32-bit field at relative offset 0x1f.
    cur = 48
    radices = list(f[cur:cur+sm]); cur += sm
    p = le(f[cur:cur+sm]); cur += sm
    order = le(f[cur:cur+so]); cur += so
    poly1 = list(f[cur:cur+d1+1]); cur += d1+1
    poly2 = list(f[cur:cur+d2+1]); cur += d2+1
    base_a = le(f[cur:cur+bn]); cur += bn
    base_b = le(f[cur:cur+bn]); cur += bn
    a = le(f[cur:cur+bn]); cur += bn
    b = le(f[cur:cur+bn]); cur += bn
    if cur > len(f): raise ValueError(f"group {gid}: field members exceed field data")
    disc = (4*pow(a,3,p) + 27*pow(b,2,p)) % p if p > 1 else 0
    checks = {
      "field_modulus_probable_prime": probable_prime(p),
      "curve_order_probable_prime": probable_prime(order),
      "h1_radices_below_modulus": all(0 <= x < p for x in radices),
      "extension_polynomial_1_has_expected_degree": len(poly1)==d1+1 and poly1[-1]!=0,
      "extension_polynomial_2_has_expected_degree": len(poly2)==d2+1 and poly2[-1]!=0,
      "extension_polynomial_coefficients_below_modulus": all(x < p for x in poly1+poly2),
      "curve_discriminant_nonzero_mod_p": disc != 0,
      "max_quotient_matches_documented_relation": f[47] == (24**25//p)-1,
      "base_curve_coefficients_zero_as_documented_unused_curve": base_a==0 and base_b==0,
      "must_be_zero_field_byte": must_zero==0,
      "offset_modulus_equals_observed_size_modulus": offset_modulus==sm,
    }
    points_end = 12+fs+sm*6*bn
    pairing_end = points_end+d1*d2*bn
    checks["point_and_pairing_regions_end_at_record_boundary"] = pairing_end==len(blob)
    return {
      "group_id":gid, "record_sha256":hashlib.sha256(blob).hexdigest(),
      "base_field_modulus_hex":hex(p), "base_field_bits":p.bit_length(),
      "curve_order_hex":hex(order), "curve_order_bits":order.bit_length(),
      "extension_polynomial_1_coefficients_low_to_high":poly1,
      "extension_polynomial_2_coefficients_low_to_high":poly2,
      "curve_a_hex":hex(a), "curve_b_hex":hex(b),
      "curve_discriminant_mod_p_hex":hex(disc), "h1_radices":radices,
      "max_quotient_byte":f[47], "offset_modulus":offset_modulus,
      "size_modulus":sm, "checks":checks,
      "all_checks_pass":all(checks.values())
    }

def parse(path):
    root=ET.parse(path).getroot()
    info=next((x for x in root.iter() if local(x.tag)=="infoBin"),None)
    if info is None: raise ValueError("missing infoBin")
    inner=ET.fromstring(base64.b64decode("".join((info.text or "").split()),validate=True))
    out=[]
    for g in inner.iter():
        if local(g.tag)!="PublicKey": continue
        gid=next((x.text or "" for x in g.iter() if local(x.tag)=="GroupId"),"")
        val=next((x.text for x in g.iter() if local(x.tag)=="PublicKeyValue"),None)
        if val: out.append(inspect(base64.b64decode("".join(val.split()),validate=True),gid))
    if not out: raise ValueError("no public key records")
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xrm_ms",type=Path)
    ap.add_argument("-o","--output",type=Path)
    args=ap.parse_args()
    try:
        rows=parse(args.xrm_ms)
        report={
          "input":args.xrm_ms.name, "public_key_count":len(rows),
          "all_groups_pass":all(x["all_checks_pass"] for x in rows),
          "common_parameters":len({(x["base_field_modulus_hex"],x["curve_order_hex"],x["curve_a_hex"],x["curve_b_hex"]) for x in rows})==1,
          "records":rows,
          "limitations":[
            "Probable-prime tests are not formal primality certificates.",
            "Polynomial degree/coefficient checks do not prove irreducibility.",
            "No public-point curve-membership test is claimed: twist and extension-field conventions require additional independent confirmation.",
            "No product-key, signature, pairing, entitlement, or activation result is produced."
          ]
        }
        rendered=json.dumps(report,indent=2)+"\\n"
        if args.output: args.output.write_text(rendered,encoding="utf-8")
        else: print(rendered,end="")
        return 0 if report["all_groups_pass"] else 1
    except Exception as exc:
        print("ERROR:",exc,file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
