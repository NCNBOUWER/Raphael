# NBT-008 — Final Proof-Lock Gate

## Purpose

This gate records what is proof-locked, what is publish-candidate, and what remains restricted to correspondence/audit-pending status.

## Proof-locked items

| Item | Status | Proof class |
|---|---|---|
| 2d6 count vector `n(s)=6-|s-7|` | LOCKED | P0/P1 |
| Three-variable state count `11^3=1331` | LOCKED | P0 |
| Primitive ordered outcome count `36^3=46656` | LOCKED | P0 |
| Product PMF `P(a,b,c)=n(a)n(b)n(c)/36^3` | LOCKED | P1 |
| Probability normalization | LOCKED | P1/P2 |
| Unique product-probability mode `(7,7,7)` | LOCKED | P1/P2 |
| Barycentric centroid non-uniqueness | LOCKED | P1/P2 |
| Modal-centroid selector theorem | LOCKED | P1 |
| Finite N-variable product-measure mode `(7,...,7)` | LOCKED | P1 |
| Convex simplex trajectory bridge `Γ` | LOCKED as geometry | P1/P3 |

## Restricted items

| Item | Status | Reason |
|---|---|---|
| Raphael physical equation proof | RESTRICTED | External equation set; not rewritten or re-derived here |
| Gravity equivalence | P5 | Requires independent field/energy/boundary proof |
| Quantum phase proof | P5 | Requires independent operator and empirical validation |
| Mechanical N-body dynamics | P5 | Probability product-measure result is not Hamiltonian mechanics |
| Theory-of-Everything interpretation | BLOCKED from this release | Outside TPW proof scope |
| Continuous field-equation proof from dice | BLOCKED as stated | Γ is interpolation support, not field-law derivation |

## Decision

This build is ready for final Git/Drive staging. Public/scientific publication remains conditional on external citation completion and final human sign-off.
