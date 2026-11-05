# Task 02 — Derivation of Gustafson's Scaled Speedup

**Setup.** Run on P processors. Normalise the *parallel* wall time to 1:

(1) `s + p = 1`, where `s` = time spent in serial code, `p` = time spent in the parallel region (all P processors busy). Define `α ≡ s`.

**Step 1 — Work done.** In the parallel region each of P processors performs `p` units of work, in total `P·p`. The serial region performs `s`. Total work (in units of "one processor-second"):

(2) `W = s + P·p`.

**Step 2 — Same job on one processor.** One processor must execute all work sequentially (assuming the larger problem fits and the work per unit is identical):

(3) `T(1) = s + P·p`.

**Step 3 — Scaled speedup** = time of the scaled job on 1 CPU / time on P CPUs:

(4) `S(P) = T(1)/T(P) = (s + P·p)/(s + p) = s + P·p`   (using (1)).

**Step 4 — Eliminate p.** From (1), `p = 1 − s = 1 − α`:

(5) `S(P) = α + P(1 − α) = P − α(P − 1)`.  ∎

Line check: P=1 ⇒ S = 1 ✓; α=0 ⇒ S = P ✓; α=1 ⇒ S = 1 ✓.

**Consequences.** `dS/dP = 1 − α` (constant slope) and `E(P) = S/P = 1 − α(P−1)/P`.
Caveat: the derivation assumes (i) serial time independent of P, (ii) the parallel work scales exactly ×P and (iii) no communication cost — Tasks 11–13 relax these.
