# NBT-006 — Publication Readiness Gate

## Purpose

This gate prevents internal proof artifacts from being published before they satisfy citation, theorem-fidelity, and correspondence-control requirements.

## Required pass criteria

| Gate | Required condition | Status |
|---|---|---|
| Scope lock | TPW side-channel only; Raphael equations not rewritten | PASS |
| TPW enumeration | `1331` sum-state triples and `46656` primitive outcomes verified | PASS |
| Product mode | `(7,7,7)` uniquely maximizes product probability | PASS |
| Entropy distinction | Barycentric centroid is non-unique; product probability selects `(7,7,7)` | PASS |
| N-variable product extension | `(7,...,7)` is unique finite product-measure mode | PASS |
| Trajectory bridge | Continuous interpolation treated as bridge, not physics proof | PASS |
| Raphael equation integrity | Raphael equations are external/completed; TPW does not modify them | PASS |
| Citation lock | Exact page/section mapping completed | OPEN |
| Dimensional audit | Raphael-side dimensional interpretations checked | OPEN |
| Coefficient audit | Coefficient origin and scaling assumptions checked | OPEN |
| Boundary conditions | Explicit assumptions registered | OPEN |
| Publish sign-off | Final proof-lock completed | OPEN |

## Decision rule

A release may move from internal fidelity branch to publication branch only when all OPEN gates are closed or explicitly marked as excluded from release scope.
