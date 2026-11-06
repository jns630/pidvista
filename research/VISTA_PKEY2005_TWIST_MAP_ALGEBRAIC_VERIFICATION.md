# PKEY2005 Twist-Map Algebraic Verification

## Scope

This is a verification-only check of the public twist/untwist equations. It does not decode product keys, compute pairings, construct signatures, or recover private parameters.

## Public model being checked

The public PKEY2005 write-up gives the tower relation (t^2=-2), defines (d=t^2), and describes the twist curve
[
E': y^2=x^3+d^2ax+d^3b
]
with untwist map
[
(X,Y)=(t^{-2}x,t^{-3}y).
]
The target curve is
[
E: Y^2=X^3+aX+b.
]

Since (d=-2), the twist coefficients are (d^2a=4a) and (d^3b=-8b). Also, (t^{-2}=-1/2) and (t^{-3}=t/4).

## Symbolic identity

Assume (y^2=x^3+d^2ax+d^3b). Then
[
egin{aligned}
Y^2
&=t^{-6}y^2\
&=t^{-6}x^3+t^{-6}d^2ax+t^{-6}d^3b\
&=(t^{-2}x)^3+a(t^{-2}x)+b\
&=X^3+aX+b,
end{aligned}
]
because (d=t^2). Therefore the stated map sends a point satisfying the stated twist equation to a point satisfying the base curve equation.

This proves the equation-level map, not that any particular serialized point is decoded correctly.

## Executable check

Added `vista_pkey2005_twist_map_check.py`. It reuses the documented (K_3/K_6) tower reductions and checks:

- (t^2=-2)
- the computed identities for (t^{-1}), (t^{-2}), and (t^{-3})
- 128 deterministic equation-level checks using sampled (x,a,bin K_3), embedded into (K_6)

The test constructs the twist-curve right-hand side and verifies that multiplying it by (t^{-6}) equals the base-curve right-hand side after applying (X=t^{-2}x). It does not need to find a square root (y), because the identity is an equation-level substitution.

## Result

The script was run locally after creation:

- inverse identities: PASS
- 128 deterministic twist-map equation checks: PASS

## What this does not establish

- It does not validate the byte/limb ordering of any serialized (Q'_i).
- It does not establish that the decoded coordinates lie on the twist curve; that is a separate point-decoding and curve-membership check.
- It does not validate subgroup membership.
- It does not implement or validate the Tate pairing or its normalization.
- It does not test the stored six-coefficient pairing reference.
- It does not establish product-key validity or activation entitlement.

## Sources

- UMSKT, PKEY2005 validation write-up: https://git.enderman.ch/UMSKT/writeups/src/commit/c2f90c6b57e78f8c63e69a4b189b45d556724131/PKEY2005.md
- Public PKey2005Decoder project (field tower and twist-map overview): https://github.com/laomms/PKey2005Decoder
