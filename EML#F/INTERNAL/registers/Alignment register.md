# Alignment register

## Canonical role

EML#F is an external-source derivation grammar for candidate equations and compact reduced models.

## Imported source claims

| Source element | Use in EML#F | Status |
|---|---|---|
| `eml(x,y)=exp(x)-ln(y)` | binary operator implementation | implemented |
| `M1(R)=eml(alpha ln R, exp(beta R))` | activation-suppression module | implemented |
| EML expression trees | future catalogue grammar | registered |
| cascade basis | reduced temporal basis demonstration | implemented as deterministic utility |
| PKA-R / Rho / 50-state examples | source-paper validation contexts | referenced only |

## Boundaries

- Do not treat EML as a new physical force.
- Do not merge EML#F into N^3.
- Do not use EML#F to validate Raphael physical claims without data.
- Do not use EML#F as a replacement for mechanistic domain models.

## Test conditions

A valid EML#F implementation must pass:

1. operator identity check;
2. M1 expanded-form equivalence;
3. internal optimum check for non-monotone response;
4. EML-vs-Hill non-monotone fit comparison;
5. cascade-basis finite-value check.
