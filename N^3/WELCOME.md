# Welcome

## Trinity Probability Well / Raphael Support Layer

This repository is the clean public-facing control surface for the N^3 workstream.

It provides a standalone Trinity Probability Well package that can be reviewed, run, audited, and later connected back into the broader private Raphael codebase. It does **not** rewrite, repair, replace, or re-derive the privately completed Raphael Equations.

## Start here

1. Open `START.html` for the human-readable entry point.
2. Run `RUN/code/geomatrix_master.py --validate` to reproduce the finite probability checks.
3. Read `RUN/proofs/Core_Proof_Pack.md` and the proof appendices in `RUN/proofs/`.
4. Use `INTERNAL/audit/` for Raphael-side crosswalks and audit controls.
5. Use `INTERNAL/registers/OPEN_TASKS.xlsx` for open tasks; when a task is completed, update the workbook or return it for controlled update.

## Proof-safe position

The Trinity Probability Well proves a finite, normalized, probability-geometric centrality structure.

- `(7,7,7)` is the unique three-variable product-probability mode.
- `(7,...,7)` is the unique finite N-variable product-measure mode for independent 2d6 sum variables.
- Barycentric centroid selection and product-probability modal selection are distinct.
- The continuous trajectory bridge is a valid piecewise-linear interpolation of discrete simplex states.
- The trajectory bridge is **not** a proof of hydrodynamics, quantum dynamics, gravity, or the private Raphael physical equations.

## Fidelity rating convention

This repository uses an internal fidelity rating rather than unsupported physical certainty language.

| Rating | Meaning |
|---:|---|
| `0–99%` | Incomplete, unverified, or partially controlled. |
| `100%` | Mathematically proven within the stated finite model. |
| `110%` | Mathematically proven and corroborated by at least two independent proof/check paths inside the package. |
| `200%` | Empirically validated against an external dataset or physical measurement regime. |
| `250%` | Empirically validated by two independent empirical methods, with supporting proof structure retained. |

Current package rating:

| Layer | Rating | Reason |
|---|---:|---|
| TPW finite probability core | `110%` | Enumeration, product-PMF proof, validation code, and independent theorem cross-checks agree. |
| N-variable finite product extension | `110%` | Direct product-measure proof and code-constrained formulation. |
| Barycentric/simplex mapping | `110%` | Normalization proof, closure proof, projection checks. |
| Continuous trajectory bridge | `100%` | Piecewise-linear interpolation is mathematically valid in the convex simplex. |
| Raphael physical correspondence | `P5 / audit-pending` | Support/crosswalk/falsification layer only; empirical and dimensional sign-off not included here. |

## Repository layout

```text
/
├─ WELCOME.md
├─ START.html
├─ RUN/
│  ├─ code/
│  ├─ data/
│  ├─ validation/
│  ├─ proofs/
│  └─ Raphael/
├─ INTERNAL/
│  ├─ audit/
│  └─ registers/
├─ Publications/
└─ Archive/
```

## Publication rule

Use this repository as an academic tool and clean front door. Do not promote correspondence-layer statements into physical proof claims unless they are separately proven, dimensionally audited, empirically validated, and signed off.
