# Proof audit index

Purpose: minimal drill-down map for the post-review GeoMatrices live surface.

## Primary chain

| Area | File / folder | Function |
|---|---|---|
| Terms | `INTERNAL/registers/Terms.md` | names, proof classes, fidelity ladder, smoke-test call surface |
| Open tasks | `INTERNAL/registers/OPEN_TASKS.csv` | live action register |
| Equation exposure | `INTERNAL/registers/Equation exposure register.md` | source-governed Git-visible equations |
| Decisions | `INTERNAL/registers/Fascicle III decisions.md` | locked owner build decisions |
| Support matrix | `INTERNAL/audit/Fascicle III support and falsification matrix.md` | support, constraint, and test-status matrix |
| Suite calls | `RUN/Raphael/Raphael Suite call surface.md` | future call registry, not Raphael Lite |

## Proof chain

| Layer | File / folder | Use |
|---|---|---|
| Fascicle I | `RUN/proofs/Core_Proof_Pack.md` | TPW probability foundation |
| Fascicle II | `RUN/proofs/Fascicle II/` | OBW, MMB, transport, irregular geometry |
| Fascicle III | `RUN/proofs/Fascicle III/` | Raphael integration, crosswalk, manifest, merge note |

## Validation chain

| Validation surface | Expected result |
|---|---|
| `RUN/validation/Core_Validation_Report.json` | finite probability checks |
| `RUN/validation/Fascicle II validation report.json` | OBW, MMB, and transport checks |
| `RUN/validation/Fascicle III validation report.json` | equation registry, claim crosswalk, fidelity, domain admissibility |

## Accuracy rules

1. Candidate domain claims need data before empirical status.
2. Keep 100/110 internal fidelity separate from 200/250 empirical fidelity.
3. Keep Raphael equations source-governed.
4. Keep EML#F external.
5. Keep Raphael Lite deferred.
6. Preserve explicit test conditions for elevated claims.
