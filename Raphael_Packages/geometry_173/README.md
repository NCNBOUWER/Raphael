# Raphael / GeoMatrices — 173-position geometry register (review commit)

**Status: research staging, not canonical physics, not a mint authorization.**

This directory is a source-aligned **reference map and candidate geometric model** for the 173 numbered Raphael slots recovered from the 7–9 November 2026 founder/research discussion. It preserves original and corrected assertions alongside their provenance, and maps to existing Raphael/N³/EML#F and CGX interfaces without copying the master workbooks or replacing their equations.

## Primary rule: roles are not unique solids

- `catalogue.json`: **173 slot roles** with source labels, normalized identifiers, draft and reference V/E/F, face inventories, status, proposed Raphael function, atomic correspondence *hypothesis*, golden scaling, geometry-source link and receipt/fingerprint.
- `relations.json`: typed reference graph (geometry identity, role family, geometric succession, speculative atomic map, known alias and limited duality links).
- `model.json`: model-contract semantics for golden scaling, metric tests, ternary/complex representations, proof and release gates.
- `catalogue.csv`: spreadsheet-friendly rendering; JSON is the source for this packet.
- `source_crosswalk.json`: source-interface **pointers only**, not the contents of the 101-sheet master or a new component database.
- `validate.py`: deterministic structural tests; success does **not** mean independent coordinates, a valid common Raphael metric or a physical theory have been proven.
- `index.html`: searchable HTML explorer; panels deliberately use **face-inventory schematics, not manufactured 3D meshes**.

## Fixed numbering

| Slots | Research category | Count |
|---|---|---:|
| 1–13 | Classical Archimedean | 13 |
| 14 | J37 alternative role (same solid as slot 58) | 1 |
| 15–21 | Selected prisms and antiprisms | 7 |
| 22–113 | Johnson J1–J92 | 92 |
| 114–117 | Kepler–Poinsot | 4 |
| 118–130 | Catalan | 13 |
| 131–137 | Unverified Raphael chiral/torsion proposals | 7 |
| 138–172 | Selected standard uniform identifiers U16–U50; draft identities often differ | 35 |
| 173 | Great dirhombicosidodecahedron U75 | 1 |

**Position 174 is not a catalogue row.** It is the intentionally empty, non-mintable DIGITAL-UNIVERSE sentinel with no object ID, person, unknown-object placeholder or geometry.

### Known corrections and distinctness constraints

- Slot 14 and slot 58 both reference established J37; one canonical geometry, two study roles.
- Slots 22–113 preserve the deterministic `J=(slot-21)` assignment; for example slot 96 is J75, slot 99 is J78, slot 105 is J84.
- Slot 173 U75: `V=60`, `E=240`, `F=124`, `χ=-56`, faces `40{3}+60{4}+24{5/2}`. Nonconvex/nonorientable abstract topology is not proof of physical zero flux.
- The 35 U16–U50 positions must not inherit their often-incorrect *draft* names as standardized identities.
- None of the seven Raphael-only candidate frames has an admitted coordinate/incidence proof here.

## Geometry and physics are separate tests

The scale label at slot `j` is `R(j)=R0*phi^(j-1)`, with `phi=(1+sqrt(5))/2`. `R0` and a governing physical selection law are **not supplied**. A curved-metric admissibility proof requires a **single, defined metric** and valid geodesic, incidence, curvature, orientation/holonomy and gluing tests for each claimed shape. Merely changing Euclidean formulas is insufficient. The mathematical constant `pi` remains irrational even when a curved-space circumference/diameter ratio differs from `pi`.

The proposed `Z=j` links are annotations, **not** independent atomic-structure predictions. Chemical elements above Z=118 are not experimentally recognized, and the model-dependent Dirac–Coulomb thresholds near 137 and ~170–173 are not a proof that these shapes are physical elements. Complex/ternary representation is an encoding grammar, not another solid or a derived particle Hamiltonian.

## Source and canonical interface pointers

- Local staging source (not committed): `Raphael_173_Source_Aligned_Staging_2026-11-09.xlsx`; SHA-256 appears in `catalogue.json`.
- Primary research context: [Raphael 101-sheet master V.R.](https://drive.google.com/file/d/1NR9dVMB10VCB3I5ImQUrPHyVXEHTWjNR/view), [Römer Family workbook](https://docs.google.com/spreadsheets/d/1refNFmebTcmPVojCuZsyILJEWaKz-sVzYLfZtqMl8k8/edit), [N³ proof modules](https://github.com/NCNBOUWER/Raphael/tree/main/N%5E3).
- Established model/data references: [exact Johnson solid coordinate/incidence dataset](https://zenodo.org/records/10729583), [Johnson explorer](https://vzome.github.io/johnson-solids/), [uniform polyhedron index](https://en.wikipedia.org/wiki/List_of_uniform_polyhedra), [specialist U75 reference](https://www.dmccooey.com/polyhedra/GreatDirhombicosidodecahedron.html).
- Existing downstream interface IDs: `CGA-*`, `RGS-*`, `MRI4D-*`, `T1K-*`, `WIT-*`, `CGXI-*` (see source crosswalk). **Do not invent parallel component-instance authorities.**

## Validation

Run `python validate.py` from this directory. It confirms 173 contiguous slots, J/U assignment, J37 alias, U75 reference counts and incidence, 174 sentinel semantics, proposed-status preservation, 173 golden exponents, reference graph integrity and no mintable entries. It does **not** validate 173 exact embeddings, a shared curved metric, or a Theory of Everything.

## Release and rights posture

This is a **provisional data/mapping commit for review**. No Raphael master workbook, N³ or EML#F equation source, physical deployment, NFT registry or canonical CGX object has been overwritten. Coordinate datasets are **linked**, not republished under assumed rights. More exact meshes must be brought in only with source provenance and licensing checks.