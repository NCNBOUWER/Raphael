# Symbol Governance Table

## Purpose

This file fixes symbol meanings for the standalone TPW package and prevents accidental reuse across private Raphael contexts.

| Symbol | Public meaning in this repo | Domain | Status |
|---|---|---|---|
| `s` | one 2d6 sum value | `{2,...,12}` | fixed |
| `n(s)` | count of ordered 2d6 outcomes giving sum `s` | integer count | fixed |
| `X_i` | independent 2d6 sum variable | finite random variable | fixed |
| `P_N(x)` | N-variable product probability | rational probability | fixed |
| `b` | barycentric/simplex coordinate | normalized vector | fixed |
| `Γ` | piecewise-linear trajectory interpolation operator | simplex path | fixed |
| `h` | time-step parameter for interpolation/finite difference | positive scalar | fixed |
| `v_t` | finite-difference velocity proxy | vector difference per step | fixed |
| `Ψ`, `Φ`, `g_QG`, `R` | private Raphael-side symbols | external/private | reference only |

## Rule

Private Raphael symbols are not redefined here. They may be referenced as private IDs or audit targets only.
