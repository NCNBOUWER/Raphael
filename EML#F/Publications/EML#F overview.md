# EML#F overview

EML#F aligns the EML Function paper with the broader Raphael build as an external derivation-library and expression-catalogue component.

## Source basis

The EML paper defines the operator:

```text
eml(x, y) = exp(x) - ln(y)
```

and uses it as a structured grammar for reduced nonlinear ODEs. The paper treats EML as syntax and candidate-equation generation rather than a standalone physical or biological interaction law.

## Alignment role

EML#F supplies:

- binary-expression grammar;
- activation-suppression module handling;
- non-monotone response candidate generation;
- cascade / reduced-basis catalogue logic;
- future symbolic-regression interface for Raphael and GeoMatrices work.

## Non-embedding rule

EML#F remains its own folder. N^3 / GeoMatrices points outward to EML#F where EML-style binary derivation language is required.

## Fidelity rule

EML#F validation is empirical-method dependent. The folder can provide internal mathematical checks for the EML operator and module identities, but real domain elevation requires source data, null models, held-out validation, and expert review.
