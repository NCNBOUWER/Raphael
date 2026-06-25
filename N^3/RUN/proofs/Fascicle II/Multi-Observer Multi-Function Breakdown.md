# Multi-Observer Multi-Function Breakdown

## Definition

The **Multi-Observer Multi-Function Breakdown** (MMB) is the face-projection counterpart to OBW.

OBW binds variables to vertices. MMB binds observers/functions to faces or projection windows.

An observer `m` supplies a local map:

```text
F_m(x) -> y_m
```

where `y_m` is a normalised vector or coordinate projection. The internal MMB state is the weighted observer aggregate:

```text
Y_MMB = sum_m w_m y_m,      w_m >= 0,      sum_m w_m = 1.
```

## Theorem 1 — Observer aggregate closure

If every observer output is closed and observer weights are closed, then the aggregate is closed.

```text
sum_j Y_j = sum_j sum_m w_m y_{m,j}
          = sum_m w_m sum_j y_{m,j}
          = sum_m w_m
          = 1.
```

Proof class: **P1 / PR-1**.

## Theorem 2 — Single-observer bias decay

Let one observer introduce bias vector `b`, while `M-1` observers are unbiased and weights are equal.

```text
Y_biased = Y_true + b/M
||Y_biased - Y_true|| <= ||b|| / M.
```

As `M` increases, one observer's unilateral influence decays toward zero.

Proof class: **P1** for the bound; **P2** when verified computationally.

## Functional use

MMB is separated from corner-variable expansion to prevent bleed:

- Do not use MMB to add new variables at 3D corners.
- Use MMB to compare face/window/observer projections of the same or related event.
- Use OBW for variable containment.
- Use MMB for observation decomposition.

## Non-locality visualisation boundary

MMB can visualise the failure of purely local single-observer sufficiency: the internally aggregated state is not equal to any one face projection except in special cases.

This is a **structural visualisation and correspondence**, not an experimental proof of quantum non-locality by itself. Formal Bell-test claims remain Fascicle III or external physics territory.

## Polyhedral observer decks

| Container | Observer/faces use | Recommended role |
|---|---:|---|
| Tetrahedron | 4 faces | Minimal 3D MMB. |
| Cube | 6 faces | Preferred 4-6 observer deck. |
| Octahedron | 8 faces | Dense observer cross-checking. |
| Dodecahedron | 12 faces | High-resolution observation mesh. |
| Icosahedron | 20 faces | High-density face decomposition. |

## Hollow projection interpretation

The hollow interior is the shared reconciliation space. It displays local observer projections, cross-face contradictions, bias cancellation, and convergence toward a shared aggregate coordinate. The internal MMB aggregate can be used as a sanity check against any one-function overfit.
