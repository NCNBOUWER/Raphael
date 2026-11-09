# Raphael / CGX — 173-slot Geometry Research Studio v0.5

**Status:** Draft research review, not geometry canon or mint authorization.

## Bounded completion accomplished

- All **173 Raphael positions** remain unique role IDs. Position **174 is an intentionally empty, non-mintable DIGITAL-UNIVERSE sentinel** and is never serialized as an object.
- All **92 Johnson solids, J1–J92** at Raphael slots 22–113 have explicit numeric Euclidean vertex and polygon-face coordinates. The constructions are checked for counts, regular edges, exactly two face incidences per abstract edge and convex Euler characteristic 2. Several are distinguished by colour-preserving face/vertex incidence graph tests.
- 131 distinct numeric Euclidean reference mesh payloads; 9 alias slots reuse an existing geometry identity. Total 140/173 slots mesh-backed.
- Four Kepler–Poinsot star polyhedra (slots 114–117) were reconstructed from the icosahedron's neighbour graphs and duality; star faces are treated as ordered self-crossing polygons, **not** filled convex hulls.
- Snub dodecahedron (slot 13) reconstructed from its icosahedral rotation orbit; its Catalan polar dual (slot 130) likewise. Slot 151 correctly reuses slot 13; U34/U35 roles at 156–157 reuse their canonical Kepler mesh identities.
- The viewer has working Vertices/Edges/Faces controls cycling ascending → descending → Raphael order, including navigation and a sequence graph that now respects sorting order.
- A compact unsigned CGX composite preview can reference geometry identities without minting objects or duplicating geometry payloads.

## Files

- `build_v05.py` — reproducible mathematical construction of the new references, with original formulas and source attributions. The complete local source package also includes the prerequisite `build_expansion.py` from the previous v0.3 stage; both must be present for a full clean rebuild.
- `render_studio_v05.py` — regenerates a self-contained standalone studio while preserving the original v0.4 interaction model.
- `qa_v05.py` — structural/face-incidence/numeric hashing and preservation tests.
- `test_browser_v05.py` — automated 9-transition sorting and star-face interface smoke tests.
- `Raphael_Packages/geometry_173/showcase/analytic_reference_meshes_v05.json` — 131 numeric meshes; 9 deduplicated role aliases.
- `.../showcase/showcase_data_v05.json` — all 173 source-governed role records, with mesh-grade, sources and candidate applications.
- `.../showcase/proof_queue_v05.json` — exact remaining geometry blockers for 33 positions (26 known non-convex and 7 Raphael-specific undefined candidates).
- `.../showcase/geometry_signatures_v05.json` — reproducible topology and hash diagnostics.
- `.../showcase/showcase_v05.html` — standalone interactive viewer.
- `.../showcase/qa_v05_full.json` — machine-readable result.

## Scientific and legal qualification

**Numeric regular-faced Euclidean construction is not a Raphael curved-spacetime admissibility proof.** A common Raphael metric, coordinates inside that metric, geodesic edges, field dynamics, topological boundary specifications, empirical validation, and object/mint authority remain open.

The model re-evaluates **mathematical coordinate formulas** from publicly documented constructions, not downloaded third-party mesh files. Mathematical derivations and source citations are retained. Reuse of an external downloadable polygon mesh requires separate license review. No local OS/CGX runtime, permission authority or digital signature is implied.

### Known references used

- Johnson catalogue and counts: https://www.orchidpalms.com/polyhedra/johnson/johnson.html
- J84–J92 algebraic geometry: https://www.qfbox.info/4d/johnson
- Snub dodecahedron rotation-group coordinates: https://en.wikipedia.org/wiki/Snub_dodecahedron
- Uniform/non-convex classification: https://mathworld.wolfram.com/UniformPolyhedron.html
- Kepler–Poinsot canonical types: https://mathworld.wolfram.com/Kepler-PoinsotSolid.html

## Review gates

**33 slots remain without exact mesh embeddings:** U16–U21, U30–U33, U36–U50, U75; and Raphael-specific slots 131–137. Their pending proofs are listed individually. They must remain research slots, not asserted novel solid identities or physical particles. The existing master, family workbooks, original PR#7 source files and mint registry remain separate authoritative systems.