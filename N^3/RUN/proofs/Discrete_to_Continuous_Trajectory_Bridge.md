# Discrete-to-continuous trajectory bridge

## Purpose

This file addresses the reviewer-risk that a finite dice/probability system is discrete while Raphael-side field language may be continuous.

The bridge is intentionally modest: it proves a continuous interpolation of normalized discrete simplex states. It does not prove any physical continuous field equation by itself.

## Simplex state sequence

Let each discrete state be a normalized simplex point

```text
x_t ∈ Δ^{K-1}.
```

For consecutive states `x_t` and `x_{t+1}`, define the trajectory bridge

```text
Γ_h[x](τ) = (1-λ)x_t + λx_{t+1},
λ = (τ-th)/h,
τ ∈ [th,(t+1)h].
```

## Closure proof

The simplex is convex. Therefore every convex combination of two simplex points remains inside the simplex.

Because `0≤λ≤1` and both endpoints satisfy nonnegativity and unit-sum closure,

```text
Γ_h[x](τ) ∈ Δ^{K-1}.
```

## Velocity proxy

A finite-difference velocity can be defined as

```text
v_t = (x_{t+1}-x_t)/h.
```

This is a mathematical path-analysis tool. It is not a physical force law.

## Claim boundary

Safe:

```text
Discrete TPW states can be embedded as continuous piecewise-linear paths inside the simplex.
```

Unsafe without separate proof:

```text
TPW paths prove hydrodynamics, quantum phase dynamics, gravity, space logistics, or Raphael field equations.
```
