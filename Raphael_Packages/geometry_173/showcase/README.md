# RAPHAEL / GEO-MATRICES · 173 Geometry-to-CGX Studio (v0.2 review)

**Authority:** research preview connected to [Raphael PR #7](https://github.com/NCNBOUWER/Raphael/pull/7). No master equation changes, mint, signature, public product launch, or change to 174 sentinel.

## Output and operation

- `showcase.html` — standalone offline HTML with **173 selectable roles**, full names/identities and source-linked descriptions. It carries its own data and 20 independently constructed Euclidean reference meshes; **open directly in a browser without running a server**.
- `showcase_data.json` — derived UI cache, 173 distinct role IDs, proposed domain/function tags, original labels, evidence gates, source pointer and typed relation links. **Not a new canonical database.** The authoritative source remains `geometry_173/catalogue.json` / `relations.json`.
- `analytic_reference_meshes.json` — 20 original Euclidean coordinate/facet constructions, tested for face-edge incidences (two uses per edge), equal-edge-length tolerance, counts and Euler characteristic. No copied third-party mesh coordinates.
- `build_analytic.py` — deterministic construction from polyhedron mathematical formulas; requires `numpy` and `scipy` only for rebuilding. The HTML viewer does not require either library.
- `metric_sandbox.py`, `metric_test_results.json` — illustrative Euclidean/log-radial/hyperbolic/spherical comparison. **No Raphael metric is inferred**; all candidate metrics remain unapproved.
- `validate_showcase.py`, `showcase_qa.json` — verifies 173 slots, source hash, Johnson and uniform mappings, 20 geometric seeds, non-minting and the intentionally empty position 174.
- `composite_preview.py` — CLI for generating a source-identified, unsigned composite-role manifest with alias deduplication.

## User interface

Sequence: 173 family-coloured nodes, draggable index, keyboard left/right, auto-play. Catalogue: search/filter by exact mesh and zone. Geometry: pointer-rotated 3D meshes where validated, and clearly marked schematic representations otherwise. Model inspector: counts, source identity, old/draft label, currently proposed interdomain role, associated interface *families*, evidence restrictions and external source links. Network view: sequence graph, not a physical coupling graph. CGX preview: up to eight proposed role references, coalesced canonical geometry IDs, local unsigned JSON export.

## Known proof boundary

- 173 **research positions** are not 173 unique and complete mathematical solids.
- 20 **Euclidean reference meshes**, not 20 proven shapes under Raphael spacetime.
- All 173 supposed atom/element interactions remain **hypothesis**, never derived by source workbook.
- `R_j=R_0*φ^(j−1)` is a scale-index transform; source `R_0` and physically selected `φ` are not established.
- U75 topology is source-referenced `V=60, E=240, F=124`, `χ=-56`; no global horizon conservation proof follows.
- `π` remains irrational even though geodesic circle ratios can be rational in specified curved metrics.
- Geometry identity and research role are distinct: e.g. slot 14 and 58 both reference J37.
- Composite is **not** a minted asset, token, signed provenance receipt, rights transfer or 1:1 physical proof.

## Installation & test

Open `showcase.html` directly, or serve this folder with `python -m http.server`. To re-run independent numerical generation, in an environment with NumPy and SciPy:

```bash
python build_analytic.py
python metric_sandbox.py
python validate_showcase.py
python composite_preview.py 14 58 173 --out sample_composite.json
```

The console should report 20 validated Euclidean reference shapes. It does not report 173 verified 3D solids.

## Source and rights

The user-owned Raphael workbook and PR #7 are the provenance source for this staging UI. Independently derived reference meshes are newly constructed formulas in `build_analytic.py`; the app does not redistribute the George W. Hart noncommercial mesh dataset or Zenodo exact Johnson files. Future imports must respect original coordinate dataset licences and source identity.

Existing canonical workbooks / family interfaces are **linked, not cloned**: `CGA-*`, `RGS-*`, `MRI4D-*`, `T1K-*`, `WIT-*`; per-slot binding remains provisional. Live `main`, canonical Google Sheets, mint registries, source IDs and executive authority remain unchanged.