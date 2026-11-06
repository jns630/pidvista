#!/usr/bin/env python3
"""Known-answer arithmetic fixture from Ben Lynn's Stanford dissertation.

Checks the published toy Tate-pairing example over F_59[i], i^2 = -1.
This is a generic arithmetic regression test, not a PKEY2005 verifier.
"""
P = 59


def add(a, b):
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def mul(a, b):
    return ((a[0] * b[0] - a[1] * b[1]) % P,
            (a[0] * b[1] + a[1] * b[0]) % P)


def inv(a):
    norm = (a[0] * a[0] + a[1] * a[1]) % P
    ni = pow(norm, -1, P)
    return (a[0] * ni % P, -a[1] * ni % P)


def div(a, b):
    return mul(a, inv(b))


def power(a, n):
    result = (1, 0)
    while n:
        if n & 1:
            result = mul(result, a)
        a = mul(a, a)
        n >>= 1
    return result


def check(actual, expected, label):
    if actual != expected:
        raise AssertionError(f"{label}: got {actual}, expected {expected}")
    print(f"PASS: {label} = {actual[0]} + {actual[1]}i")


def main():
    # Stanford thesis, Section 3.10.2:
    # E: y^2 = x^3 + x over F_59
    # P=(25,30), Q=(-25,30i), subgroup order r=5.
    # i^2=-1, so F_59[i] is F_(59^2).
    check(mul((0, 1), (0, 1)), (58, 0), "extension relation i^2=-1")

    # Published Miller steps:
    # f_2(Q) = (19+30i)/58
    f2 = div((19, 30), (58, 0))
    check(f2, (40, 29), "Miller intermediate f_2(Q)")

    # f_4(Q) = f_2(Q)^2 * (34+30i)/9
    f4 = div(mul(mul(f2, f2), (34, 30)), (9, 0))
    check(f4, (31, 32), "Miller intermediate f_4(Q)")

    # f_5(Q) = 9*f_4(Q), as the last line is vertical.
    f5 = mul((9, 0), f4)
    check(f5, (43, 52), "raw Miller value f_5(Q)")

    # Final exponent (59^2-1)/5 = 696.
    result = power(f5, (P * P - 1) // 5)
    check(result, (42, 40), "normalized Tate pairing")

    check(power(result, 5), (1, 0), "pairing output has fifth power one")
    print("LIMIT: this fixture validates only the published toy example.")
    print("LIMIT: it does not test Vista/PKEY2005 field or pairing conventions.")


if __name__ == "__main__":
    main()
