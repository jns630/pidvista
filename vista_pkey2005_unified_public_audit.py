#!/usr/bin/env python3
"""Reproducible public-data PKEY2005 audit. No key generation or signature work.

Checks public record boundaries, common field data, probable primality,
extension-polynomial irreducibility, twist-curve membership, and [m]Q=O for
each serialized public point. Pairing references are only checked for six
canonical, nonzero base-field coefficients; their field/order test is
intentionally not claimed until the encoding is independently settled.
"""
import argparse, base64, hashlib, json, struct, sys
import xml.etree.ElementTree as ET
from pathlib import Path

MAGIC, FMAGIC, VERSION = 0x44556677, 0x00112233, 0x0100
def local(t): return t.rsplit("}", 1)[-1]
def u16(b,o): return struct.unpack_from("<H",b,o)[0]
def u32(b,o): return struct.unpack_from("<I",b,o)[0]
def le(b): return int.from_bytes(b,"little")

def probable_prime(n):
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47):
        if n == q: return True
        if n % q == 0: return False
    d,s=n-1,0
    while d%2 == 0: s+=1; d//=2
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131):
        if a >= n-1: continue
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def cubic_irreducible(p, coeff):
    # For a cubic f over Fp: irreducible iff gcd(f, X^p-X)=1.
    f=[v%p for v in coeff]
    def trim(a):
        while len(a)>1 and a[-1]%p==0: a.pop()
        return a
    def rem(a,b):
        a=trim(a[:]); b=trim(b[:]); inv=pow(b[-1],-1,p)
        while len(a)>=len(b) and not(len(a)==1 and a[0]==0):
            k=len(a)-len(b); q=a[-1]*inv%p
            for i,v in enumerate(b): a[k+i]=(a[k+i]-q*v)%p
            trim(a)
        return a
    def mulmod(a,b):
        z=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): z[i+j]=(z[i+j]+x*y)%p
        return rem(z,f)
    def powmod(a,e):
        z=[1]
        while e:
            if e&1: z=mulmod(z,a)
            a=mulmod(a,a); e>>=1
        return z
    def gcd(a,b):
        while not(len(b)==1 and b[0]==0): a,b=b,rem(a,b)
        iv=pow(a[-1],-1,p)
        return [(v*iv)%p for v in a]
    xp=powmod([0,1],p)
    diff=rem([(xp[i] if i<len(xp) else 0)-(1 if i==1 else 0)
              for i in range(max(2,len(xp)))],f)
    return len(gcd(f,diff))==1

def field_ops(p, poly):
    c=[v%p for v in poly[:3]]
    zero=(0,0,0); one=(1,0,0)
    def add(x,y): return tuple((x[i]+y[i])%p for i in range(3))
    def neg(x): return tuple((-v)%p for v in x)
    def sub(x,y): return add(x,neg(y))
    def mul(x,y):
        z=[0]*5
        for i in range(3):
            for j in range(3): z[i+j]=(z[i+j]+x[i]*y[j])%p
        for k in (4,3):
            v=z[k]
            for j in range(3): z[k-3+j]=(z[k-3+j]-v*c[j])%p
        return tuple(z[:3])
    def sq(x): return mul(x,x)
    def cube(x): return mul(sq(x),x)
    return zero,one,add,sub,mul,sq,cube

def scalar_mul_is_infinity(k, P, A, ops):
    # Jacobian arithmetic for y^2=x^3+A*x+B over K3.
    zero,one,add,sub,mul,sq,cube=ops
    O=(zero,one,zero)
    def dbl(Q):
        X,Y,Z=Q
        if Z==zero or Y==zero: return O
        yy=sq(Y); yyyy=sq(yy); zz=sq(Z)
        S=mul((4,0,0),mul(X,yy))
        M=add(mul((3,0,0),sq(X)),mul(A,sq(zz)))
        X3=sub(sq(M),mul((2,0,0),S))
        Y3=sub(mul(M,sub(S,X3)),mul((8,0,0),yyyy))
        Z3=mul((2,0,0),mul(Y,Z))
        return X3,Y3,Z3
    def plus(P1,P2):
        X1,Y1,Z1=P1; X2,Y2,Z2=P2
        if Z1==zero: return P2
        if Z2==zero: return P1
        z1=sq(Z1); z2=sq(Z2)
        U1=mul(X1,z2); U2=mul(X2,z1)
        S1=mul(Y1,mul(Z2,z2)); S2=mul(Y2,mul(Z1,z1))
        if U1==U2: return dbl(P1) if S1==S2 else O
        H=sub(U2,U1); I=sq(mul((2,0,0),H)); J=mul(H,I)
        r=mul((2,0,0),sub(S2,S1)); V=mul(U1,I)
        X3=sub(sub(sq(r),J),mul((2,0,0),V))
        Y3=sub(mul(r,sub(V,X3)),mul((2,0,0),mul(S1,J)))
        Z3=mul(sub(sub(sq(add(Z1,Z2)),z1),z2),H)
        return X3,Y3,Z3
    R=O; Q=P
    while k:
        if k&1: R=plus(R,Q)
        Q=dbl(Q); k >>= 1
    return R[2]==zero

def parse(path):
    root=ET.parse(path).getroot()
    info=next((x for x in root.iter() if local(x.tag)=="infoBin"),None)
    if info is None: raise ValueError("missing infoBin")
    inner=ET.fromstring(base64.b64decode("".join((info.text or "").split()),validate=True))
    rows=[]
    for g in inner.iter():
        if local(g.tag)!="PublicKey": continue
        gid=next((x.text or "" for x in g.iter() if local(x.tag)=="GroupId"),"")
        value=next((x.text for x in g.iter() if local(x.tag)=="PublicKeyValue"),None)
        if value: rows.append((gid,base64.b64decode("".join(value.split()),validate=True)))
    if not rows: raise ValueError("no PublicKeyValue records found")
    return rows

def inspect(gid, blob):
    if len(blob)<12 or u32(blob,0)!=MAGIC or u16(blob,4)!=VERSION:
        raise ValueError(f"{gid}: invalid outer header")
    fs=u32(blob,8); f=blob[12:12+fs]
    if len(f)!=fs or u32(f,0)!=FMAGIC or u16(f,4)!=VERSION:
        raise ValueError(f"{gid}: invalid field header")
    bn,sm,so=f[9],f[9],f[10]; d1,d2=u32(f,11),u32(f,15)
    if (fs,bn,sm,so,d1,d2)!=(307,14,14,14,3,2):
        raise ValueError(f"{gid}: unexpected field dimensions")
    pos=48; rad=list(f[pos:pos+sm]); pos+=sm
    p=le(f[pos:pos+bn]); pos+=bn; m=le(f[pos:pos+so]); pos+=so
    poly1=[v if v<128 else v-256 for v in f[pos:pos+d1+1]]; pos+=d1+1
    poly2=[v if v<128 else v-256 for v in f[pos:pos+d2+1]]; pos+=d2+1
    base_a=le(f[pos:pos+bn]); pos+=bn; base_b=le(f[pos:pos+bn]); pos+=bn
    a=le(f[pos:pos+bn]); pos+=bn; b=le(f[pos:pos+bn]); pos+=bn
    if poly1!=[4,1,0,1] or poly2!=[2,0,1] or base_a or base_b:
        raise ValueError(f"{gid}: unsupported field polynomial/base coefficients")
    point_start=12+fs; point_size=6*bn; pair_start=point_start+sm*point_size
    if pair_start+d1*d2*bn!=len(blob): raise ValueError(f"{gid}: record boundary mismatch")
    ops=field_ops(p,poly1); zero,one,add,sub,mul,sq,cube=ops
    d=(-2%p,0,0); d2v=mul(d,d); d3=mul(d2v,d)
    A=mul(d2v,(a,0,0)); B=mul(d3,(b,0,0))
    coord_ok=curve_ok=order_ok=0
    for i in range(sm):
        q=blob[point_start+i*point_size:point_start+(i+1)*point_size]
        x=tuple(le(q[j*bn:(j+1)*bn]) for j in range(3))
        y=tuple(le(q[(3+j)*bn:(4+j)*bn]) for j in range(3))
        if any(v>=p for v in x+y): continue
        coord_ok+=1
        if sq(y)==add(add(cube(x),mul(A,x)),B):
            curve_ok+=1
            if scalar_mul_is_infinity(m,(x,y,one),A,ops): order_ok+=1
    pairing=blob[pair_start:]
    coeff=[le(pairing[i*bn:(i+1)*bn]) for i in range(6)]
    return {
      "group_id":gid,"record_sha256":hashlib.sha256(blob).hexdigest(),
      "point_count":sm,"canonical_point_coordinates":coord_ok,
      "points_on_twist_curve":curve_ok,"points_annihilated_by_m":order_ok,
      "point_checks_pass":coord_ok==curve_ok==order_ok==sm,
      "p_probable_prime":probable_prime(p),"m_probable_prime":probable_prime(m),
      "cubic_extension_irreducible":cubic_irreducible(p,poly1),
      "quadratic_extension_irreducible_over_K3":pow((-2)%p,(p-1)//2,p)==p-1,
      "radices_below_p":all(v<p for v in rad),
      "pairing_coefficients_canonical":len(coeff)==6 and all(v<p for v in coeff),
      "pairing_reference_nonzero":any(coeff),
      "pairing_reference_order_test":"NOT PERFORMED; encoding/basis still requires independent confirmation",
      "field_data_sha256":hashlib.sha256(f).hexdigest()
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("xrm_ms",type=Path); ap.add_argument("-o","--output",type=Path)
    args=ap.parse_args()
    rows=[inspect(g,b) for g,b in parse(args.xrm_ms)]
    report={
      "input":args.xrm_ms.name,"input_sha256":hashlib.sha256(args.xrm_ms.read_bytes()).hexdigest(),
      "public_key_groups":len(rows),"total_points":sum(x["point_count"] for x in rows),
      "points_on_twist_curve":sum(x["points_on_twist_curve"] for x in rows),
      "points_annihilated_by_m":sum(x["points_annihilated_by_m"] for x in rows),
      "all_point_checks_pass":all(x["point_checks_pass"] for x in rows),
      "common_field_data":len({x["field_data_sha256"] for x in rows})==1,
      "pairing_reference_order_test":"NOT PERFORMED; no c^m=1 claim",
      "records":rows,
      "limitations":["Probable-prime checks are fixed-base probable-prime tests, not formal certificates.",
        "Pairing references are checked only for coefficient bounds and nonzero value.",
        "No Tate pairing is recomputed and no product-key signature is verified.",
        "No key generation, private signing material recovery, or activation is performed."]
    }
    output=json.dumps(report,indent=2)+"\n"
    if args.output: args.output.write_text(output,encoding="utf-8")
    else: print(output,end="")
    return 0 if report["all_point_checks_pass"] and report["common_field_data"] else 1
if __name__=="__main__": raise SystemExit(main())
