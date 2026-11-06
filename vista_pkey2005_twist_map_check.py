#!/usr/bin/env python3
"""Verification-only algebraic test of the documented PKEY2005 twist map.

Checks the map from E': y^2=x^3+d^2*a*x+d^3*b to
E: Y^2=X^3+a*X+b over K6, with d=t^2=-2 and t^2=-2.
Uses public field parameters only. It does not parse keys, compute pairings,
create signatures, or recover private data.
"""
from random import Random

P = 886368969471450739924935101400677

def k3_add(a, b):
    return tuple((a[i] + b[i]) % P for i in range(3))

def k3_mul(a, b):
    c = [0] * 5
    for i in range(3):
        for j in range(3):
            c[i+j] += a[i] * b[j]
    for degree in (4, 3):
        value = c[degree] % P
        c[degree] = 0
        if degree == 3:
            c[1] -= value
            c[0] -= 4 * value
        else:
            c[2] -= value
            c[1] -= 4 * value
    return tuple(v % P for v in c[:3])

def k6_add(a, b):
    return tuple((a[i] + b[i]) % P for i in range(6))

def k6_mul(a, b):
    A, B, C, D = a[:3], a[3:], b[:3], b[3:]
    ac, bd = k3_mul(A, C), k3_mul(B, D)
    ad, bc = k3_mul(A, D), k3_mul(B, C)
    return tuple((ac[i] - 2*bd[i]) % P for i in range(3)) + k3_add(ad, bc)

def k6_pow(a, n):
    out = (1, 0, 0, 0, 0, 0)
    while n:
        if n & 1:
            out = k6_mul(out, a)
        a = k6_mul(a, a)
        n >>= 1
    return out

def embed_k3(a):
    return tuple(a) + (0, 0, 0)

def scale_k6(a, scalar):
    return tuple((v * scalar) % P for v in a)

def add_k6(*values):
    out = (0, 0, 0, 0, 0, 0)
    for value in values:
        out = k6_add(out, value)
    return out

def main():
    zero = (0, 0, 0, 0, 0, 0)
    one = (1, 0, 0, 0, 0, 0)
    t = (0, 0, 0, 1, 0, 0)
    t_inv = scale_k6(t, (P - 1) * pow(2, -1, P) % P)
    t_inv2 = scale_k6(one, (P - 1) * pow(2, -1, P) % P)
    t_inv3 = scale_k6(t, pow(4, -1, P))
    check = lambda ok, msg: (_ for _ in ()).throw(AssertionError(msg)) if not ok else None

    check(k6_mul(t, t) == (P-2, 0, 0, 0, 0, 0), "t^2 != -2")
    check(k6_mul(t, t_inv) == one, "computed t inverse is incorrect")
    check(k6_mul(t_inv, t_inv) == t_inv2, "t^-2 identity failed")
    check(k6_mul(t_inv2, t_inv) == t_inv3, "t^-3 identity failed")

    rng = Random(0x5457495354)
    for index in range(128):
        x = embed_k3(tuple(rng.randrange(P) for _ in range(3)))
        a = embed_k3(tuple(rng.randrange(P) for _ in range(3)))
        b = embed_k3(tuple(rng.randrange(P) for _ in range(3)))

        # d=t^2=-2, so d^2=4 and d^3=-8.
        x2 = k6_mul(x, x)
        x3 = k6_mul(x2, x)
        twist_rhs = add_k6(
            x3,
            scale_k6(k6_mul(a, x), 4),
            scale_k6(b, -8 % P),
        )

        # If y^2=twist_rhs, then (t^-3*y)^2=t^-6*twist_rhs.
        mapped_y_squared = k6_mul(k6_pow(t_inv3, 2), twist_rhs)
        mapped_x = k6_mul(t_inv2, x)
        mapped_x2 = k6_mul(mapped_x, mapped_x)
        mapped_x3 = k6_mul(mapped_x2, mapped_x)
        base_rhs = add_k6(mapped_x3, k6_mul(a, mapped_x), b)
        check(mapped_y_squared == base_rhs,
              f"twist-map identity failed on deterministic sample {index}")

    print("PASS: t^2=-2 and computed t^-1, t^-2, t^-3 identities")
    print("PASS: 128 deterministic K3-to-K6 twist-map equation checks")
    print("LIMIT: algebraic map only; no point decoding, pairing, or signature validation.")

if __name__ == "__main__":
    main()
