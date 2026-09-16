# Solved-key pattern analysis (83 published secrets)

Keys analyzed: 83  |  bit-width range: 1..135

## Top nibble (bits n-4..n-1), n >= 4

- 0x8: 7
- 0x9: 9
- 0xa: 12
- 0xb: 12
- 0xc: 6
- 0xd: 17
- 0xe: 10
- 0xf: 7

## Last nibble (k mod 16)

- 0x0: 6
- 0x1: 6
- 0x2: 3
- 0x3: 8
- 0x4: 10
- 0x5: 5
- 0x6: 5
- 0x7: 4
- 0x8: 5
- 0x9: 2
- 0xa: 1
- 0xb: 3
- 0xc: 7
- 0xd: 3
- 0xe: 7
- 0xf: 8

## Relative position inside interval (deciles)

- 0-10%: 7
- 10-20%: 7
- 20-30%: 7
- 30-40%: 10
- 40-50%: 10
- 50-60%: 5
- 60-70%: 14
- 70-80%: 8
- 80-90%: 6
- 90-100%: 9

## Bits set (hamming weight) as fraction of bit-width

- mean: 0.516 (expected ~0.500)
- count: 83

## Verdict

- uniform top nibble ~= expected under random keys in [2^(n-1), 2^n)
- uniform last nibble: no mod-16 residue is favoured by the generator
- relative position uniform: solved keys are not biased toward any part of the interval (no positional shortcut)
- hamming weight ~ n/2 as expected for uniform independent bits

_Nothing here suggests structure worth exploiting: the published secrets behave like uniform random integers within their interval._
