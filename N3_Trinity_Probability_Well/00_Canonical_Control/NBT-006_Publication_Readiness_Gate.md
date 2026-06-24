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
| Git cleanup | Temporary README replaced and old root binary ZIP removed from final branch | PASS |
| Drive Folder 2 staging | Final folder/index prepared | PASS-STAGED |
| Citation lock | Exact page/section mapping completed | HUMAN SIGN-OFF REQUIRED |
| Dimensional audit | Raphael-side dimensional interpretations checked | HUMAN SIGN-OFF REQUIRED |
| Coefficient audit | Coefficient origin and scaling assumptions checked | HUMAN SIGN-OFF REQUIRED |
| Boundary conditions | Explicit assumptions registered | HUMAN SIGN-OFF REQUIRED |
| Publish sign-off | Final proof-lock completed | PENDING HUMAN SIGN-OFF |

## Decision rule

This v1.5 build may be staged to GitHub and Drive as the final pre-publish candidate. It should not be represented as a completed public scientific release until the HUMAN SIGN-OFF REQUIRED gates are either closed or explicitly excluded from the release scope.

## v1.5 final-prepublish update

Final Git/Drive staging is permitted after README replacement, source ZIP creation, validation test pass, and Folder 2 Drive isolation. Public/scientific publication still requires final human sign-off on citations and Raphael-side audit references.
