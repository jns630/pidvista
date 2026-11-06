# Independent Tate-Pairing Known-Answer Test

## Source fixture

Ben Lynn, *On the Implementation of Pairing-Based Cryptosystems*, Stanford University dissertation (June 2007), Section 3.10.2, provides a fully worked Tate-pairing example.

The source specifies:

- Curve: (E:y^2=x^3+x) over (mathbb F_{59})
- Extension: (mathbb F_{59^2}=mathbb F_{59}[i]), with (i^2=-1)
- Subgroup order: (r=5)
- First input: (P=(25,30))
- Second input: (Q=(-25,30i))
- Raw Miller value: (f_5(Q)=43+52i)
- Final exponent: ((59^2-1)/5=696)
- Normalized pairing: (42+40i)
- The source confirms ((42+40i)^5=1).

The source also publishes intermediate Miller calculations:
- (f_2(Q)=40+29i)
- (f_4(Q)=31+32i)

## Reproduction

The script `tate_pairing_stanford_2007_kat.py` implements arithmetic in (mathbb F_{59}[i]) and checks each published intermediate and final value.

Run:

```sh
python tate_pairing_stanford_2007_kat.py
```

The script is deliberately a compact known-answer arithmetic regression test. It verifies the published line-evaluation sequence and final exponentiation; it is not a general-purpose pairing library.

## Result

All intermediate values, the raw Miller result, normalized pairing output, and fifth-root-of-unity check reproduce the Stanford dissertation's values.

## Relevance and limits for PKEY2005

This is the independent known-answer fixture that was missing for generic extension-field arithmetic and the textbook Tate-pairing evaluation sequence.

It does **not** establish that the PKEY2005 implementation uses this exact pairing convention. In particular, it does not validate:

- PKEY2005's (mathbb F_{p^6}) tower or its twist mapping;
- PKEY2005's point decoding or lift/sign conventions;
- the exact pairing argument order, divisor normalization, or final exponent in PKEY2005;
- whether any of the 14 stored PKEY2005 references has order (m).

Those remain separate questions requiring a PKEY2005-specific independent fixture.

## Reference

Ben Lynn, *On the Implementation of Pairing-Based Cryptosystems*, Stanford University, June 2007, Section 3.10.2, pp. 40–42:
https://crypto.stanford.edu/pbc/thesis.pdf

The dissertation's worked example gives the curve, points, Miller intermediates, raw value, final exponentiation, and normalized output.
