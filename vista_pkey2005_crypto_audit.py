#!/usr/bin/env python3
"""Public-parameter audit for Vista PKEY2005 config; not a key verifier."""
import argparse, base64, hashlib, json, sys
from pathlib import Path
import xml.etree.ElementTree as ET

MAGIC = 0x44556677
FIELD_MAGIC = 0x00112233
RADIX = [1, 3, 8, 15, 15, 15, 31, 3, 3, 3, 3, 3, 7, 63]
BASES = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53)

def lname(tag):
    return tag.rsplit("}", 1)[-1]

def child_text(el, name):
    for c in el:
        if lname(c.tag) == name:
            return (c.text or "").strip()
    return ""

def le(b, o, n):
    return int.from_bytes(b[o:o+n], "little")

def probable_prime(n):
    if n < 2:
        return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n-1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
        if a >= n-1:
            continue
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        for unused in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def extract(path):
    outer = ET.fromstring(path.read_bytes())
    for e in outer.iter():
        if lname(e.tag) == "infoBin" and (e.text or "").strip():
            return ET.fromstring(base64.b64decode("".join(e.text.split())))
    raise ValueError("No embedded infoBin XML found")

def main():
    ap = argparse.ArgumentParser(description="Audit public Vista PKEY2005 arithmetic parameters")
    ap.add_argument("config")
    ap.add_argument("-o", "--output", default="vista-pkey-crypto-audit.json")
    args = ap.parse_args()
    path = Path(args.config)
    inner = extract(path)
    records = []
    for e in inner.iter():
        if lname(e.tag) != "PublicKey":
            continue
        encoded = child_text(e, "PublicKeyValue")
        if not encoded:
            continue
        b = base64.b64decode("".join(encoded.split()), validate=True)
        if len(b) != 1579 or le(b,0,4) != MAGIC or le(b,4,2) != 0x100:
            raise ValueError("Unexpected public-key record header or size")
        if le(b,12,4) != FIELD_MAGIC or le(b,16,2) != 0x100:
            raise ValueError("Unexpected field-data header")
        p = le(b,74,14)
        n = le(b,88,14)
        a = le(b,137,14)
        curve_b = le(b,151,14)
        discriminant = (4*pow(a,3,p) + 27*pow(curve_b,2,p)) % p if p else 0
        radix = list(b[60:74])
        records.append({
            "size":len(b),
            "sha256":hashlib.sha256(b).hexdigest(),
            "group_id":child_text(e,"GroupId") or None,
            "modulus_probable_prime":probable_prime(p),
            "order_probable_prime":probable_prime(n),
            "short_weierstrass_discriminant_nonzero":discriminant != 0,
            "h1_radix_matches_expected":radix == RADIX,
            "h1_radix":radix
        })
    raw = path.read_bytes()
    report = {
        "scope":"public parameter arithmetic audit only; not signature verification or key generation",
        "source_size":len(raw),
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "records_found":len(records),
        "records":records
    }
    Path(args.output).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print("Public records audited:",len(records))
    print("Report written to:",args.output)
    print("This is not PKEY2005 signature verification.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR:",exc,file=sys.stderr)
        sys.exit(2)
