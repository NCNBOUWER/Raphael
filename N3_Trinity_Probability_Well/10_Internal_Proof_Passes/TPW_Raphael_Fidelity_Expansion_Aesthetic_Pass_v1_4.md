# TPW / Raphael Fidelity, Expansion + Aesthetic Pass v1.4

## Pass type

Internal update/fidelity pass with product-cleanliness and reviewer-risk reduction.

## Inputs considered

- v1.3 update/fidelity package.
- Latest clarification: use TPW as side-channel support, not Raphael equation rewriting.
- Latest pasted risk note: discrete-to-continuous bridge and falsification requirements.

## Accepted expansions

### 1. Product-probability centrality

For one 2d6 sum variable:

```text
n(s) = 6 - |s - 7|
```

For `N` independent variables:

```text
P(s_1,...,s_N) = ∏ n(s_i) / 36^N
```

Because `n(s)` is uniquely maximized at `s=7`, the product is uniquely maximized at:

```text
(7,...,7)
```

Status: `P1`.

### 2. Barycentric centroid distinction

All equal triples map to the barycentric centroid. Product probability selects `(7,7,7)` from that equal-triple family.

Status: `P1/P2`.

### 3. Continuous trajectory bridge

Discrete simplex states can be embedded into continuous paths by piecewise-linear interpolation:

```text
Γ_h[x](τ) = (1−λ)x_t + λx_{t+1}
```

The bridge is valid geometry and finite-difference analysis. It does not independently prove continuous physical field equations.

Status: `P3/P4`, not `P1` physics.

### 4. Raphael relationship rule

TPW may support, constrain, classify, or falsify relationships to Raphael claims. It must not rewrite or retrofit Raphael equations.

Status: governance locked.

## Reviewer-risk reduction

The main overreach risk is claiming that finite dice/probability geometry proves continuous physical equations. v1.4 blocks that move and replaces it with a trajectory-bridge claim.

## Publication status

Not yet publication-ready. Citation, dimensional, coefficient, and boundary-condition gates remain open.
