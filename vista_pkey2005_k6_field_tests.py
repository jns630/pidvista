#!/usr/bin/env python3
"""Verification-only tests for the documented PKEY2005 field tower.

This tool tests finite-field arithmetic and coefficient serialization only.
It does not parse product keys, compute pairings, create signatures, or activate
Windows. No private parameters are used.
"""
from random import Random

P = 886368969471450739924935101400677
M = int("2bb38c9b1d8a3b1846f701ad79ef", 16)
K3_POLY = (4, 1, 0, 1)  # u^3 + u + 4
K6_POLY = (2, 0, 1)     # t^2 + 2


def k3_add(a, b):
    return tuple((a[i] + b[i]) % P for i in range(3))


def k3_mul(a, b):
    c = [0] * 5
    for i in range(3):
        for j in range(3):
            c[i + j] += a[i] * b[j]
    # u^3 = -u - 4; u^4 = -u^2 - 4u
    for degree in (4, 3):
        value = c[degree] % P
        c[degree] = 0
        if degree == 3:
            c[1] -= value
            c[0] -= 4 * value
        else:
            c[2] -= value
            c[1] -= 4 * value
    return tuple(value % P for value in c[:3])


def k6_add(a, b):
    return tuple((a[i] + b[i]) % P for i in range(6))


def k6_mul(a, b):
    # a=A+B*t, b=C+D*t, t^2=-2
    A, B, C, D = a[:3], a[3:], b[:3], b[3:]
    ac, bd = k3_mul(A, C), k3_mul(B, D)
    ad, bc = k3_mul(A, D), k3_mul(B, C)
    real = tuple((ac[i] - 2 * bd[i]) % P for i in range(3))
    return real + k3_add(ad, bc)


def k6_pow(a, exponent):
    result = (1, 0, 0, 0, 0, 0)
    while exponent:
        if exponent & 1:
            result = k6_mul(result, a)
        a = k6_mul(a, a)
        exponent >>= 1
    return result


def poly_trim(a):
    while len(a) > 1 and a[-1] % P == 0:
        a.pop()
    return [value % P for value in a]


def poly_sub(a, b):
    result = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        result[i] += value
    for i, value in enumerate(b):
        result[i] -= value
    return poly_trim(result)


def poly_mulmod(a, b, modulus):
    result = [0] * (len(a) + len(b) - 1)
    degree = len(modulus) - 1
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            result[i + j] = (result[i + j] + av * bv) % P
    for d in range(len(result) - 1, degree - 1, -1):
        value = result[d] % P
        for j in range(degree):
            result[d - degree + j] = (
                result[d - degree + j] - value * modulus[j]
            ) % P
    return poly_trim(result[:degree])


def poly_powmod(a, exponent, modulus):
    result = [1]
    while exponent:
        if exponent & 1:
            result = poly_mulmod(result, a, modulus)
        a = poly_mulmod(a, a, modulus)
        exponent >>= 1
    return result


def poly_gcd(a, b):
    a, b = poly_trim(a[:]), poly_trim(b[:])
    while not (len(b) == 1 and b[0] == 0):
        while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
            quotient = a[-1] * pow(b[-1], -1, P) % P
            shift = len(a) - len(b)
            for i in range(len(b)):
                a[i + shift] = (a[i + shift] - quotient * b[i]) % P
            a = poly_trim(a)
        a, b = b, a
    inverse = pow(a[-1], -1, P)
    return [(value * inverse) % P for value in a]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    zero = (0,) * 6
    one = (1, 0, 0, 0, 0, 0)
    check(P % 2 == 1, "base modulus is not odd")
    check(pow(P - 2, (P - 1) // 2, P) == P - 1,
          "-2 is not a nonsquare in Fp")

    # Rabin criterion for an irreducible cubic over Fp.
    x = [0, 1]
    xp = poly_powmod(x, P, list(K3_POLY))
    check(poly_gcd(list(K3_POLY), poly_sub(xp, x)) == [1],
          "cubic polynomial has a linear factor")
    check(poly_powmod(x, P ** 3, list(K3_POLY)) == x,
          "cubic polynomial fails Frobenius criterion")

    rng = Random(0x2005)
    samples = [tuple(rng.randrange(P) for _ in range(6)) for _ in range(8)]
    for a in samples:
        check(k6_mul(a, one) == a and k6_mul(one, a) == a,
              "multiplicative identity failure")
        check(k6_add(a, zero) == a, "additive identity failure")
        if a != zero:
            inverse = k6_pow(a, P ** 6 - 2)
            check(k6_mul(a, inverse) == one, "inverse failure")
            check(k6_pow(a, P ** 6 - 1) == one, "Fermat exponent failure")

    for a, b, c in zip(samples, samples[1:] + samples[:1],
                       samples[2:] + samples[:2]):
        check(k6_mul(a, b) == k6_mul(b, a), "commutativity failure")
        check(k6_mul(k6_mul(a, b), c) == k6_mul(a, k6_mul(b, c)),
              "associativity failure")
        check(k6_mul(a, k6_add(b, c)) ==
              k6_add(k6_mul(a, b), k6_mul(a, c)), "distributivity failure")

    u = (0, 1, 0, 0, 0, 0)
    t = (0, 0, 0, 1, 0, 0)
    check(k6_mul(k6_mul(u, u), u) == (P - 4, P - 1, 0, 0, 0, 0),
          "u^3 = -u - 4 relation failure")
    check(k6_mul(t, t) == (P - 2, 0, 0, 0, 0, 0),
          "t^2 = -2 relation failure")

    print("PASS: base-field nonsquare test and cubic irreducibility criterion")
    print("PASS: K6 identities, inverses, Fermat, commutativity,")
    print("      associativity, distributivity, and both tower relations")
    print(f"p_bits={P.bit_length()} m_bits={M.bit_length()} samples={len(samples)}")
    print("LIMIT: this does not test stored pairing references or signatures.")


if __name__ == "__main__":
    main()
