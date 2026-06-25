# Classical transport and covariant bridge

## Purpose

This module converts Fascicle I's Gamma bridge into Fascicle II transport language without claiming physical field equivalence.

## Discrete transport

Given a closed state sequence:

```text
p(t_0), p(t_1), ..., p(t_T)
```

where each `p(t)` lies in the simplex, define the finite-difference transport vector:

```text
V(t_i) = [p(t_{i+1}) - p(t_i)] / Δt.
```

Because both endpoint states are closed:

```text
sum_j V_j(t_i) = [sum_j p_j(t_{i+1}) - sum_j p_j(t_i)] / Δt = 0.
```

So transport is tangent to the closure surface.

## Gamma interpolation

For `τ` between `t_i` and `t_{i+1}`:

```text
Γ(τ) = (1-λ)p(t_i) + λp(t_{i+1}),    0 <= λ <= 1.
```

Because the simplex is convex, `Γ(τ)` remains closed and bounded.

## Gauge-corrected barycentric derivative

For a normalised state `p`, raw local change `r`, and connection contribution `c`, define:

```text
raw_i = r_i + c_i p_i
D_i = raw_i - p_i sum_j raw_j
```

Then:

```text
sum_i D_i = sum_i raw_i - (sum_i p_i)(sum_j raw_j) = 0.
```

This is the discrete closure-preserving analogue of a covariant derivative. It allows local vertex, metric, observer, or boundary changes to be included without violating the closure constraint.

## Irregular geometry derivative

When vertices vary with an external coordinate `x^mu`, the map is:

```text
X = sum_i p_i v_i(x^mu)
```

and the derivative splits into:

```text
dX = sum_i dp_i v_i + sum_i p_i dv_i.
```

The first term tracks redistribution of weights. The second tracks boundary deformation. This is the formal separation behind regular boundary / irregular distribution and irregular boundary / regularised distribution.

## Proof boundary

This module proves closure and transport consistency. It does not prove general relativity, quantum gravity, or Raphael's physical equations. It prepares the mathematical language for later Fascicle III crosswalks.
