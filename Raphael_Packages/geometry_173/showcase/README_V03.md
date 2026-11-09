# Raphael 173 · Sequence-Sort Geometry Studio v0.3

Status: **research preview**. This package extends the existing `NCNBOUWER/Raphael` draft PR #7. It does not merge to main, mint CGX assets, modify source-governed equations, or assert that the Raphael metric/ToE is established.

## Interactive behaviour

- The **Vertices / Edges / Faces** buttons each cycle `ascending ↑ → descending ↓ → Raphael 001..173` across successive clicks on the same metric. Clicking another metric begins that metric in ascending order. Ties resolve by original Raphael position; unavailable values are last.
- The filtered list, complete sequence strip, sequence network view, previous/next and range control use the active sort order. The position identity and golden exponent remain attached to the original slot.
- The model viewer rotates formula-derived 3D polygons in orbit mode; unsupported positions receive clearly marked schematic/functional visualisation. Composite previews deduplicate equivalent identity pointers, are unsigned and never mintable.

## Mesh and identity coverage

- 173 original position roles are preserved.
- 104 distinct role-target Euclidean meshes were generated with analytic formulas and verified computationally for finite coordinates, convex-hull face polygons, edge count, exactly two faces per edge, Euler characteristic 2 and equal edge lengths where applicable. The 13 selected Catalan duals may have unequal edge lengths by definition (duality geometry).
- 6 role aliases reuse an existing mesh: slot 14 → 58 (J37), and selected U24–U28 mappings to original Archimedean slots; the full alias table in the JSON is authoritative, not this prose summary.
- 110/173 positions therefore show coordinate meshes; 63/173 need a qualified source and/or mathematical definition.
- A particularly important correction was choosing cupola phase orientations that reproduce both J65 and J67 published V/E/F and polygonal-face inventories. Generated J62, J63 and J64 also match these external combinatorial references.
- **Caution:** These checks are necessary but not sufficient to prove that every Johnson name is globally graph-isomorphic to the conventional Johnson identifier; remaining distinct-identity comparisons need oriented incidence / geometric symmetry or canonical catalogue matching. No non-convex/imaginary/curved-Raphael embedding is claimed to be validated by the Euclidean convex-hull routine.

## Reproduce

Requires Python 3, `numpy`, `scipy`, `playwright` + Chromium for the optional UI test.

From the extracted package root:

```bash
python build_expansion.py
python patch_studio.py
python qa_v03.py
python test_v03_browser.py
```

Outputs: `Raphael_Packages/geometry_173/showcase/analytic_reference_meshes_v03.json`, `showcase_data_v03.json`, `showcase_v03.html`, and the standalone HTML at the package root.

## Source reconciliation and rights

The catalogues and links remain source-governed from PR #7. Published Johnson-solid face inventories used in checks: https://www.orchidpalms.com/polyhedra/johnson/johnson.html ; https://paulohscwb.github.io/polyhedra/johnson3/ . Additional classifications: https://mathworld.wolfram.com/JohnsonSolid.html . Coordinate-generation formulas for conventional solids are mathematical formulas; no third-party mesh archive was copied. The GitHub assets are strictly research previews, not licences to mint a third-party model.

Position 174 remains an **empty, non-mintable DIGITAL-UNIVERSE sentinel**, not a geometric asset.