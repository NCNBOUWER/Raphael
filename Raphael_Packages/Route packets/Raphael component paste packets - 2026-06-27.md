# Raphael component paste packets - 2026-06-27

Purpose: define static-first component paste packets for the Raphael route set. These packets are additive planning artifacts only; they do not authorise deployment, deletion, archive movement, or public release.

Source authority:

- `Achilles/Web/route_proof_packet_templates.json`
- `Raphael_Packages/Raphael static interactive elements.md`
- `Raphael_Packages/Route packets/Raphael route packet set - 2026-06-27.md`
- `Raphael_Packages/Route packets/Raphael source tables - 2026-06-27.md`

Global paste rules:

- Static fallback is required before interaction.
- Scripts are optional and must not hide source/status content.
- External dependencies must be declared before paste.
- Rollback instruction is mandatory for every route component.
- No empirical, validation, release, or unification claim may bypass claim gate review.
- EML#F remains external.
- Raphael Lite remains deferred.
- N^3 is GeoMatrices.
- Google Earth material remains Investor-scoped.

## `/raphael` overview components

| Component | Route target | Static fallback | Scripts required | External dependencies | Manual paste notes | Rollback instruction |
|---|---|---|---|---|---|---|
| Package status cards | `/raphael` | table/card list with status and blocker text | no | none | Paste above boundary cards | Remove component block and retain source table |
| Boundary cards | `/raphael` | plain cards for Raphael_Physics, GeoMatrices, EML#F, Raphael Lite | no | none | Include external/deferred badges | Remove component block; do not merge boundaries |
| Function rollup | `/raphael` | static list grouped by route | optional filter only | none | Filter must not be required to read content | Remove filter script; keep static list |
| Source table | `/raphael` | markdown/HTML table | no | source tables file | Must include unresolved state for missing source verification | Remove source table component if stale; route back to source file |
| Open tasks panel | `/raphael` | static list of task IDs/statuses | optional filter only | current OPEN_TASKS register | Do not paste unless current register is verified | Remove panel if register freshness is uncertain |

## `/raphael/equations` components

| Component | Route target | Static fallback | Scripts required | External dependencies | Manual paste notes | Rollback instruction |
|---|---|---|---|---|---|---|
| Equation/function cards | `/raphael/equations` | plain formula cards with source placeholder | no | verified equation source documents | No validation text without citation/evidence class | Remove cards lacking source trace |
| Source trace drawer | `/raphael/equations` | visible source line under each card | optional disclosure only | claim gate packet | Disclosure must default to source-visible fallback | Remove disclosure script; keep visible source line |
| Proof badges | `/raphael/equations` | text badge: unresolved / source-linked / reviewed | no | claim gate state | Default unresolved until verified | Revert badges to unresolved |
| Term detail cards | `/raphael/equations` | static glossary table | optional filter only | equation source documents | Terms must remain source-bound | Remove unsourced term entries |

## `/raphael/natural-phenomena` components

| Component | Route target | Static fallback | Scripts required | External dependencies | Manual paste notes | Rollback instruction |
|---|---|---|---|---|---|---|
| Phenomena lens cards | `/raphael/natural-phenomena` | static cards by phenomenon/lens | no | Raphael_Physics boundary verification | Mark simulation-only unless evidence attached | Remove cards or badge as unresolved |
| Classic package link | `/raphael/natural-phenomena` | visible link/text block | no | Raphael_Physics source path | Keep separate from N^3 and EML#F | Remove link if boundary unresolved |
| Simulation badge | `/raphael/natural-phenomena` | text badge | no | claim gate state | Default simulation-only | Revert to simulation-only |
| Source trace table | `/raphael/natural-phenomena` | static source table | no | source tables file | No empirical claim without evidence class | Remove unsourced rows |

## `/raphael/geomatrices` components

| Component | Route target | Static fallback | Scripts required | External dependencies | Manual paste notes | Rollback instruction |
|---|---|---|---|---|---|---|
| GeoMatrices status panel | `/raphael/geomatrices` | static status and blocker list | no | N^3 / GeoMatrices folder verification | Use GeoMatrices as canonical naming | Remove panel if source status stale |
| Fascicle map | `/raphael/geomatrices` | table/card map | optional graph only | verified GeoMatrices source | Graph cannot replace static table | Remove graph; retain table |
| Proof map | `/raphael/geomatrices` | static proof table | optional filter only | verified proof source | No validation language without claim gate | Remove unverified proof rows |
| Validation report placeholder | `/raphael/geomatrices` | unresolved/reviewed badge | no | validation report source | Default unresolved | Revert to unresolved |
| Release gate banner | `/raphael/geomatrices` | static blocked/review state | no | route packet set | Must show unresolved folder verification if still open | Remove release banner only after owner sign-off update |

## `/raphael/emlf` components

| Component | Route target | Static fallback | Scripts required | External dependencies | Manual paste notes | Rollback instruction |
|---|---|---|---|---|---|---|
| External source marker | `/raphael/emlf` | static label and boundary note | no | EML#F external source verification | Must remain visible | Remove route component if marker cannot be shown |
| Operator identity card | `/raphael/emlf` | static identity/source card | no | EML#F source | Do not internalise into Raphael core | Remove card if source unresolved |
| Candidate grammar table | `/raphael/emlf` | static table | optional filter only | EML#F source material | Mark candidate/unverified by default | Remove or mark unresolved |
| Validation run placeholder | `/raphael/emlf` | static unresolved/reviewed badge | no | validation run source | No validation claim unless evidenced | Revert to unresolved |
| Separation rule banner | `/raphael/emlf` | static banner | no | route packet guardrails | Must remain visible | Remove component paste if banner cannot be retained |

## Escalations

| Escalation | Target |
|---|---|
| Current OPEN_TASKS verification before task panels | OPEN_TASKS / task delta |
| Equation source attachment before equation cards | documents queue / claim gate |
| Raphael_Physics boundary verification before natural phenomena route | OPEN_TASKS / route queue |
| N^3 / GeoMatrices source verification before fascicle/proof map release | OPEN_TASKS / route queue |
| EML#F source verification before external function route release | OPEN_TASKS / route queue |
| Owner sign-off before public deployment | deployment readiness packet |

## Archive/deletion posture

No deletion candidate is created. Any older notes, exports, ZIPs, or route drafts discovered while implementing these components must be extracted into canonical route packets, source tables, task deltas, extension queues, or archive/delete registers before owner approval is requested.