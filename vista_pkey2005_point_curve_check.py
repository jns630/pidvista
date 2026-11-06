#!/usr/bin/env python3
"""Verify public PKEY2005 point records against the documented K3 twist curve.

Read-only checks only: parses public configuration parameters, constructs K3
using the published cubic polynomial, confirms the quadratic twist t^2=-2,
and checks y'^2 = x'^3 + d^2*a*x' + d^3*b for each serialized Q' point.
No product-key parsing, H1 recovery, private-scalar work, signature creation,
or Tate-pairing verification is performed.
"""
import argparse, base64, hashlib, json, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

OUTER_MAGIC, FIELD_MAGIC, VERSION = 0x44556677, 0x00112233, 0x0100

def local(tag): return tag.rsplit("}", 1)[-1]
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
def le(b): return int.from_bytes(b,"little")
def signed_coeffs(raw):
    return [x if x < 128 else x-256 for x in raw]

def probable_prime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        if n == q: return True
        if n % q == 0: return False
    d,s=n-1,0
    while d%2==0: s+=1; d//=2
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,
              59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131):
        if a >= n-1: continue
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=pow(x,2,n)
            if x==n-1: break
        else: return False
    return True

def parse_record(blob,gid):
    if len(blob)<12 or u32(blob,0)!=OUTER_MAGIC or u16(blob,4)!=VERSION:
        raise ValueError(f"group {gid}: invalid outer header")
    size=u32(blob,8); f=blob[12:12+size]
    if len(f)!=size or u32(f,0)!=FIELD_MAGIC or u16(f,4)!=VERSION:
        raise ValueError(f"group {gid}: invalid field-data header")
    bn,sm,so=f[9],f[9],f[10]
    d1,d2=u32(f,11),u32(f,15)
    if not bn or bn!=sm or not so or d1!=3 or d2!=2:
        raise ValueError(f"group {gid}: unsupported/inconsistent dimensions")
    pos=48
    radices=list(f[pos:pos+sm]); pos+=sm
    p=le(f[pos:pos+bn]); pos+=bn
    order=le(f[pos:pos+so]); pos+=so
    poly1=signed_coeffs(f[pos:pos+d1+1]); pos+=d1+1
    poly2=signed_coeffs(f[pos:pos+d2+1]); pos+=d2+1
    base_a=le(f[pos:pos+bn]); pos+=bn
    base_b=le(f[pos:pos+bn]); pos+=bn
    a=le(f[pos:pos+bn]); pos+=bn
    b=le(f[pos:pos+bn]); pos+=bn
    if pos>len(f): raise ValueError(f"group {gid}: field data truncated")
    if poly1 != [4,1,0,1] or poly2 != [2,0,1]:
        raise ValueError(f"group {gid}: polynomial differs from independently documented model")
    if base_a or base_b:
        raise ValueError(f"group {gid}: unexpected base-curve coefficients")
    if not probable_prime(p) or not probable_prime(order):
        raise ValueError(f"group {gid}: modulus/order failed probable-prime test")
    if any(x<0 or x>=p for x in radices):
        raise ValueError(f"group {gid}: H1 radix outside base field")
    point_size=6*bn
    start=12+size
    end=start+sm*point_size
    pair_end=end+d1*d2*bn
    if pair_end!=len(blob):
        raise ValueError(f"group {gid}: point/pairing boundaries do not match record")
    return dict(gid=gid,p=p,bn=bn,sm=sm,poly1=poly1,poly2=poly2,a=a,b=b,
                points_start=start,point_size=point_size)

def field_ops(p,poly):
    # K3 = Fp[u]/(u^3 + c2*u^2 + c1*u + c0)
    c=[x%p for x in poly[:3]]
    def add(x,y): return tuple((x[i]+y[i])%p for i in range(3))
    def mul(x,y):
        z=[0]*5
        for i in range(3):
            for j in range(3): z[i+j]=(z[i+j]+x[i]*y[j])%p
        for k in (4,3):
            v=z[k]
            if v:
                for j in range(3): z[k-3+j]=(z[k-3+j]-v*c[j])%p
        return tuple(z[:3])
    def sq(x): return mul(x,x)
    def cube(x): return mul(sq(x),x)
    return add,mul,sq,cube

def has_root_cubic(p,poly):
    # A cubic over a field is reducible iff it has a root in that field.
    # Exhaustive root testing is infeasible for 110-bit p; use gcd(X^p-X,f).
    # Polynomial arithmetic is over Fp, low coefficient first.
    f=[x%p for x in poly]
    def trim(a):
        while len(a)>1 and a[-1]%p==0: a.pop()
        return a
    def rem(a,b):
        a=trim(a[:]); b=trim(b[:])
        inv=pow(b[-1],-1,p)
        while len(a)>=len(b) and not (len(a)==1 and a[0]==0):
            k=len(a)-len(b); q=a[-1]*inv%p
            for i in range(len(b)): a[k+i]=(a[k+i]-q*b[i])%p
            trim(a)
        return a
    def mulmod(a,b,m):
        z=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): z[i+j]=(z[i+j]+x*y)%p
        return rem(z,m)
    def powmod(a,e,m):
        out=[1]
        while e:
            if e&1: out=mulmod(out,a,m)
            a=mulmod(a,a,m); e>>=1
        return out
    def gcd(a,b):
        while not (len(b)==1 and b[0]==0): a,b=b,rem(a,b)
        inv=pow(a[-1],-1,p); return [(x*inv)%p for x in a]
    xp=powmod([0,1],p,f)
    diff=rem([(xp[i] if i<len(xp) else 0)-(1 if i==1 else 0) for i in range(max(len(xp),2))],f)
    return len(gcd(f,diff))>1

def inspect(path):
    root=ET.parse(path).getroot()
    info=next((x for x in root.iter() if local(x.tag)=="infoBin"),None)
    if info is None: raise ValueError("missing infoBin")
    inner=ET.fromstring(base64.b64decode("".join((info.text or "").split()),validate=True))
    rows=[]
    for group in inner.iter():
        if local(group.tag)!="PublicKey": continue
        gid=next((x.text or "" for x in group.iter() if local(x.tag)=="GroupId"),"")
        val=next((x.text for x in group.iter() if local(x.tag)=="PublicKeyValue"),None)
        if val: rows.append((gid,base64.b64decode("".join(val.split()),validate=True)))
    results=[]
    for gid,blob in rows:
        r=parse_record(blob,gid); p=r["p"]
        add,mul,sq,cube=field_ops(p,r["poly1"])
        # F2 = t^2 + 2, hence d=t^2=-2 in the base subfield.
        d=(-2%p,0,0); d2=mul(d,d); d3=mul(d2,d)
        A=mul(d2,(r["a"],0,0)); B=mul(d3,(r["b"],0,0))
        valid=[]; invalid=[]
        for i in range(r["sm"]):
            off=r["points_start"]+i*r["point_size"]
            q=blob[off:off+r["point_size"]]; n=r["bn"]
            x=tuple(le(q[j*n:(j+1)*n]) for j in range(3))
            y=tuple(le(q[(3+j)*n:(4+j)*n]) for j in range(3))
            if any(v>=p for v in x+y):
                invalid.append(i); continue
            lhs=sq(y)
            rhs=add(add(cube(x),mul(A,x)),B)
            (valid if lhs==rhs else invalid).append(i)
        cubic_irreducible=not has_root_cubic(p,r["poly1"])
        # Legendre(-2,p)=-1 and [K3:Fp]=3, so -2 remains nonsquare in K3.
        quadratic_irreducible=pow((-2)%p,(p-1)//2,p)==p-1
        results.append({
          "group_id":gid,"record_sha256":hashlib.sha256(blob).hexdigest(),
          "point_count":r["sm"],"points_on_twisted_curve":len(valid),
          "invalid_point_indices":invalid,
          "all_coordinate_limbs_below_p":len(invalid)==0,
          "cubic_extension_polynomial_irreducible":cubic_irreducible,
          "quadratic_extension_polynomial_irreducible_over_K3":quadratic_irreducible,
          "twist_parameter_d_hex":hex(p-2),
          "twisted_curve_A_hex":[hex(v) for v in A],
          "twisted_curve_B_hex":[hex(v) for v in B],
          "all_checks_pass":len(valid)==r["sm"] and not invalid and cubic_irreducible and quadratic_irreducible
        })
    if not results: raise ValueError("no public key records found")
    return {"input":path.name,"public_key_count":len(results),
            "total_points":sum(x["point_count"] for x in results),
            "total_points_on_twisted_curve":sum(x["points_on_twisted_curve"] for x in results),
            "all_groups_pass":all(x["all_checks_pass"] for x in results),
            "extension_model":"K3 = Fp[u]/(u^3+u+4); K6 = K3[t]/(t^2+2); d=t^2=-2",
            "curve_checked":"y'^2 = x'^3 + d^2*a*x' + d^3*b over K3",
            "records":results,
            "limitations":["This is public-point consistency, not product-key signature verification.",
              "It does not calculate H1, H2, a Tate pairing, or activation status."]}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xrm_ms",type=Path); ap.add_argument("-o","--output",type=Path)
    args=ap.parse_args()
    try:
        report=inspect(args.xrm_ms); data=json.dumps(report,indent=2)+"\n"
        if args.output: args.output.write_text(data,encoding="utf-8")
        else: print(data,end="")
        return 0 if report["all_groups_pass"] else 1
    except Exception as e:
        print("ERROR:",e,file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
