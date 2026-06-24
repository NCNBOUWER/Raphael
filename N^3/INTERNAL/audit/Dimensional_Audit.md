# Dimensional Audit

## Public TPW layer

| Item | Dimensional class | Result |
|---|---|---|
| `n(s)` | count | dimensionless integer |
| `P(a,b,c)` | probability | dimensionless rational |
| `b` | normalized coordinate | dimensionless vector |
| `Γ` | simplex interpolation | dimensionless path unless external time scale is supplied |
| `v_t` | finite difference | dimensionless per step, or dimensionless per external time unit if `h` is specified |

The public TPW layer is dimensionally closed because all probabilities, counts, and normalized coordinates are dimensionless.

## Raphael-side layer

Private Raphael equations and physical variables require their own dimensional, coefficient, and boundary-condition audit. This repository does not alter those equations and does not claim their dimensional closure.
