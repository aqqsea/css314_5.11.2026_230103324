# Task 07 — Maximum Tolerable Serial Fraction

Given P = 8192, requirement `S(P) ≥ 7500`.

`P − α(P−1) ≥ 7500`  
`α(P−1) ≤ P − 7500`  
`α ≤ (P − 7500)/(P − 1) = 692/8191`  

**α_max = 692/8191 ≈ 0.084483 (≈ 8.45 %)**

Check: `S = 8192 − 0.084483·8191 = 8192 − 692.0 = 7500.0` ✓. Equivalent efficiency target `E ≥ 7500/8192 = 0.9155`, i.e. `α ≤ (1−E)·P/(P−1)`.
Under Amdahl the same S would require `s ≤ (P/S − 1)/(P − 1) = (1.09227−1)/8191 ≈ 1.13·10⁻⁵` — a 7500× tighter bound; the target is realistic only in the weak-scaling frame.
