# Task 01 — Strong vs. Weak Scaling Foundations

## Amdahl (1967): fixed-size ("strong") scaling
* Assumption: the **problem size W is constant**. A fraction `s` of the *serial* runtime is inherently sequential, `1−s` is perfectly parallelisable.
* `T(P) = T(1)·(s + (1−s)/P)`  ⇒  `S_A(P) = 1 / (s + (1−s)/P)`.
* As P → ∞ the per-processor slice `W/P → 0`; the parallel part vanishes and `S_A → 1/s`. Problem dimension stays **N = const**.
* Why "fixed-size": the numerator (work) is frozen; adding processors only *shortens the time* of the same job.
* Physical reading: cores are a tool to finish a given job faster; the sequential part is a hard wall (s = 5% ⇒ max 20×).

## Gustafson–Barsis (1988): fixed-time ("weak") scaling
* Assumption: the **wall-clock time is constant** (a user budget: "the forecast must be ready in 1 h"). The problem is enlarged to use the machine: parallel work `W_par(P) = P·W_par(1)`, serial work stays fixed.
* `S_G(P) = (s + pP)/(s + p) = P − α(P−1)` with `s + p = 1` measured on the parallel run.
* As P → ∞ the problem dimension grows without bound (N ∝ P in work, e.g. N ∝ P^{1/3} per side in 3-D); `S_G` grows **linearly** with slope `1−α`; there is no ceiling.
* Why "fixed-time": the denominator (parallel time) is frozen; adding processors lets you do *more work* in the same time.

## The divergence
| | Amdahl | Gustafson |
|---|---|---|
| Held constant | problem size | execution time |
| What grows with P | nothing (time shrinks) | problem size (work) |
| Serial part | fixed **fraction** of fixed work → absolute time stays, fraction of *parallel run* grows | fixed **absolute time**, fraction of the scaled work shrinks |
| Limit | `1/s` | unbounded, slope `1−α` |
| Question answered | "how fast can this job finish?" | "how big a job can I finish in this time?" |

**Philosophical divergence:** Amdahl asks what to do with a *given* problem and finds a pessimistic ceiling; Gustafson observes that practitioners do not keep the problem fixed — they spend extra capacity on resolution, accuracy and fidelity — so the serial *fraction* is not a constant of nature but a function of problem size. Both are algebraically consistent: they are the same time model evaluated under different constraints (see Task 03 for the conversion `s_A = α / (α + (1−α)P)`).
