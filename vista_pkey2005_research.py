#!/usr/bin/env python3
"""Inspect public Vista PKEY2005 configuration records; no key generation."""
import argparse, base64, hashlib, json, sys
from pathlib import Path
import xml.etree.ElementTree as ET

def lname(tag):
    return tag.rsplit("}", 1)[-1]

def text_child(el, name):
    for child in el:
        if lname(child.tag) == name:
            return (child.text or "").strip()
    return ""

def read_le(data, offset, width):
    return int.from_bytes(data[offset:offset+width], "little")

def main():
    ap = argparse.ArgumentParser(description="Inspect Vista pkeyconfig.xrm-ms public records")
    ap.add_argument("config", help="Path to pkeyconfig.xrm-ms")
    ap.add_argument("-o", "--output", default="vista-pkey-report.json")
    ap.add_argument("--edition", help="Only include entries whose text contains this value")
    args = ap.parse_args()
    raw = Path(args.config).read_bytes()
    outer = ET.fromstring(raw)
    inner = None
    for node in outer.iter():
        if lname(node.tag) == "infoBin" and (node.text or "").strip():
            inner = ET.fromstring(base64.b64decode("".join(node.text.split())))
            break
    if inner is None:
        raise ValueError("No embedded infoBin XML found")
    records, entries = [], []
    for node in inner.iter():
        if lname(node.tag) == "PublicKey":
            encoded = text_child(node, "PublicKeyValue")
            if encoded:
                data = base64.b64decode("".join(encoded.split()), validate=True)
                record = {
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "magic": "0x%08X" % read_le(data, 0, 4) if len(data) >= 4 else None,
                    "version": read_le(data, 4, 2) if len(data) >= 6 else None,
                    "group_id": text_child(node, "GroupId") or None,
                    "structural_size_ok": len(data) == 1579,
                }
                records.append(record)
        if lname(node.tag) in ("Configuration", "ProductKey"):
            row = {}
            for child in node:
                value = (child.text or "").strip()
                if value:
                    row[lname(child.tag)] = value
            if row:
                entries.append(row)
    if args.edition:
        entries = [e for e in entries if args.edition.lower() in json.dumps(e).lower()]
    report = {
        "tool": "Vista PKEY2005 public configuration inspector",
        "scope": "structural inspection only; not cryptographic signature verification",
        "source_file": str(Path(args.config).name),
        "source_size": len(raw),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "configuration_entries_found": len(entries),
        "public_key_records_found": len(records),
        "public_key_records": records,
        "configuration_entries": entries,
    }
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Configuration bytes:", len(raw))
    print("Configuration entries:", len(entries))
    print("Public-key records:", len(records))
    print("Records with expected 1579-byte size:", sum(1 for r in records if r["structural_size_ok"]))
    print("Report written to:", args.output)
    print("Note: structural checks are not PKEY2005 signature verification.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(2)
