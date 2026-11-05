#!/usr/bin/env python
"""Independent public-parameter arithmetic audit for Vista PKEY2005 records.

Checks the documented record layout, K3/K6 extension polynomials, every
compressed point on the quadratic twist over K3, and the stored pairing
element's subgroup-order relation in K6. Python 3.7+, standard library only.

This is NOT a product-key signature verifier, activation checker, or key
generator. It does not process product keys or recover private material.
"""
from __future__ import print_function
import argparse, base64, hashlib, json, sys
from pathlib import Path
import xml.etree.ElementTree as ET

MAGIC, FIELD_MAGIC, VERSION = 0x44556677, 0x00112233, 0x0100
RADICES = [1,3,8,15,15,15,31,3,3,3,3,3,7,63]
RECORD_SIZE, POINT_COUNT = 1579, 14
Z3, O3 = (0,0,0), (1,0,0)
Z6, O6 = (Z3,Z3), (O3,Z3)

class AuditError(Exception): pass

def lname(tag): return tag.rsplit('}',1)[-1]
def child_text(el,name):
    for c in el:
        if lname(c.tag)==name: return (c.text or '').strip()
    return ''
def uint(b,o,n):
    if o<0 or n<=0 or o+n>len(b): raise AuditError("truncated integer at %d"%o)
    return int.from_bytes(b[o:o+n],'little')

def probable_prime(n):
    if n<2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n==q: return True
        if n%q==0: return False
    d,s=n-1,0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53):
        if a>=n-1: continue
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def add3(x,y,p): return tuple((x[i]+y[i])%p for i in range(3))
def scale3(k,x,p): return tuple(k*v%p for v in x)
def mul3(x,y,p):
    # K3 = Fp[u]/(u^3+u+4), hence u^3=-u-4.
    c=[0]*5
    for i in range(3):
        for j in range(3): c[i+j]=(c[i+j]+x[i]*y[j])%p
    v=c[4]; c[1]=(c[1]-4*v)%p; c[2]=(c[2]-v)%p
    v=c[3]; c[0]=(c[0]-4*v)%p; c[1]=(c[1]-v)%p
    return tuple(c[:3])
def mul6(x,y,p):
    # K6 = K3[t]/(t^2+2), hence t^2=-2.
    ac=mul3(x[0],y[0],p); bd=mul3(x[1],y[1],p)
    ad=mul3(x[0],y[1],p); bc=mul3(x[1],y[0],p)
    return (add3(ac,scale3(-2,bd,p),p),add3(ad,bc,p))
def pow6(x,n,p):
    out=O6
    while n:
        if n&1: out=mul6(out,x,p)
        x=mul6(x,x,p); n>>=1
    return out

def parse_record(b):
    if len(b)!=RECORD_SIZE: raise AuditError("record length != 1579")
    if uint(b,0,4)!=MAGIC or uint(b,4,2)!=VERSION: raise AuditError("public header mismatch")
    if uint(b,8,4)!=307 or uint(b,12,4)!=FIELD_MAGIC or uint(b,16,2)!=VERSION:
        raise AuditError("field-data header mismatch")
    if b[20]!=0: raise AuditError("reserved field flag is nonzero")
    width,ow= b[21],b[22]
    d1,d2=uint(b,23,4),uint(b,27,4)
    count=uint(b,43,4)
    if (width,ow,d1,d2,count)!=(14,14,3,2,14): raise AuditError("unsupported field dimensions")
    if list(b[60:74])!=RADICES: raise AuditError("H1 radix mismatch")
    p,n=uint(b,74,14),uint(b,88,14)
    # Signed, low-degree-first polynomial coefficients.
    poly1=[int.from_bytes(b[i:i+1],'little',signed=True) for i in range(102,106)]
    poly2=[int.from_bytes(b[i:i+1],'little',signed=True) for i in range(106,109)]
    if poly1!=[4,1,0,1] or poly2!=[2,0,1]:
        raise AuditError("extension polynomial mismatch")
    a,curve_b=uint(b,137,14),uint(b,151,14)
    if not p or not n or a>=p or curve_b>=p: raise AuditError("base-field parameter out of range")
    if not probable_prime(p): raise AuditError("base modulus failed Miller-Rabin")
    if not probable_prime(n): raise AuditError("subgroup order failed Miller-Rabin")
    if (4*pow(a,3,p)+27*pow(curve_b,2,p))%p==0: raise AuditError("base curve singular")
    # The quadratic twist uses d=t^2=-2: a'=d^2*a=4a; b'=d^3*b=-8b.
    d=(p-2,0,0)
    ta=mul3(mul3(d,d,p),(a,0,0),p)
    tb=mul3(mul3(mul3(d,d,p),d,p),(curve_b,0,0),p)
    for j in range(POINT_COUNT):
        off=319+j*84
        x=tuple(uint(b,off+i*14,14) for i in range(3))
        y=tuple(uint(b,off+42+i*14,14) for i in range(3))
        if any(v>=p for v in x+y): raise AuditError("point %d coordinate >= p"%j)
        lhs=mul3(y,y,p)
        rhs=add3(add3(mul3(mul3(x,x,p),x,p),mul3(ta,x,p),p),tb,p)
        if lhs!=rhs: raise AuditError("point %d fails twist-curve equation"%j)
    coeff=[uint(b,1495+i*14,14) for i in range(6)]
    if any(v>=p for v in coeff): raise AuditError("pairing coefficient >= p")
    pairing=(tuple(coeff[:3]),tuple(coeff[3:]))
    if pairing==Z6: raise AuditError("pairing value is zero")
    if pow6(pairing,n,p)!=O6: raise AuditError("pairing value fails c^n=1")
    return {
      "sha256":hashlib.sha256(b).hexdigest(),"p_bits":p.bit_length(),"n_bits":n.bit_length(),
      "probable_prime_checks":"PASS (Miller-Rabin, 16 fixed bases; not a formal certificate)",
      "base_curve_nonsingular":"PASS",
      "K3_polynomial":"u^3+u+4","K6_over_K3_polynomial":"t^2+2",
      "twist_curve_equation":"y^2=x^3+4*a*x-8*b over K3",
      "twist_points_valid":14,"pairing_nonzero":"PASS","pairing_c_to_n_equals_one":"PASS",
      "H1_radices":"PASS"
    }

def audit_config(path):
    raw=path.read_bytes()
    try: outer=ET.fromstring(raw)
    except ET.ParseError as e: raise AuditError("outer XML parse failed: %s"%e)
    inner=None
    for el in outer.iter():
        if lname(el.tag)=="infoBin" and (el.text or "").strip():
            try: inner=ET.fromstring(base64.b64decode(''.join(el.text.split())))
            except Exception as e: raise AuditError("embedded XML decode failed: %s"%e)
            break
    if inner is None: raise AuditError("pkeyConfigData infoBin not found")
    records=[]
    for el in inner.iter():
        if lname(el.tag)!="PublicKey": continue
        value=child_text(el,"PublicKeyValue")
        if not value: continue
        try: blob=base64.b64decode(''.join(value.split()),validate=True)
        except Exception as e: raise AuditError("bad public-key base64: %s"%e)
        item=parse_record(blob)
        item["group_id"]=child_text(el,"GroupId")
        item["algorithm"]=child_text(el,"AlgorithmId")
        records.append(item)
    if not records: raise AuditError("no public-key records")
    return {
      "file":path.name,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
      "record_count":len(records),"records":records,
      "result":"PASS",
      "scope":"Public parameter arithmetic only; not product-key signature verification or activation."
    }

def self_test():
    p=11; x=(1,2,3); y=(4,5,6); z=(7,8,9)
    assert mul3(x,O3,p)==x
    assert mul3(mul3(x,y,p),z,p)==mul3(x,mul3(y,z,p),p)
    q=((1,2,3),(4,5,6))
    assert mul6(q,O6,p)==q and mul6(q,Z6,p)==Z6
    t=(Z3,O3)
    assert mul6(t,t,p)==((p-2,0,0),Z3)
    assert probable_prime(11) and not probable_prime(15)
    print("PASS: K3 field identities and associativity")
    print("PASS: K6 field identities and t^2=-2")
    print("PASS: Miller-Rabin positive and negative controls")

def main():
    ap=argparse.ArgumentParser(description="Audit Vista PKEY2005 public parameter arithmetic")
    ap.add_argument("config",nargs="?",type=Path)
    ap.add_argument("-o","--output",type=Path)
    ap.add_argument("--self-test",action="store_true")
    a=ap.parse_args()
    if a.self_test: self_test()
    if a.config:
        report=audit_config(a.config)
        out=json.dumps(report,indent=2)
        if a.output: a.output.write_text(out+"\n",encoding="utf-8")
        print(out)
    elif not a.self_test: ap.error("provide a config file or --self-test")
    return 0
if __name__=="__main__":
    try: sys.exit(main())
    except Exception as e:
        print("AUDIT ERROR: %s"%e,file=sys.stderr); sys.exit(2)
