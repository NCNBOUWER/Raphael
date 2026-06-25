# Full run confirmation

Date: 25 June 2026

## Status

Completed.

## Git additions in this pass

- `N^3/Publications/GeoMatrices overview.md`
- `N^3/INTERNAL/registers/Proof audit index.md`
- `N^3/Archive/Fascicles/Fascicle I.md`
- `N^3/Archive/Fascicles/Fascicle II.md`
- `N^3/Archive/Fascicles/Fascicle III.md`
- `N^3/Archive/Merge note.md`
- `N^3/INTERNAL/registers/Review approved.md`

## Actual validation run

The local combined N^3 build was assembled from the clean source plus Fascicle II and Fascicle III source packages.

Commands run:

```bash
python3 -m py_compile geomatrix_master.py test_geomatrix_master.py fascicle_ii_geomatrices.py test_fascicle_ii_geomatrices.py fascicle_iii_raphael_bridge.py test_fascicle_iii_raphael_bridge.py
python3 test_geomatrix_master.py
python3 test_fascicle_ii_geomatrices.py
python3 test_fascicle_iii_raphael_bridge.py
python3 geomatrix_master.py --validate
python3 fascicle_ii_geomatrices.py
python3 fascicle_iii_raphael_bridge.py
```

Results:

- Fascicle I tests passed.
- Fascicle II tests passed.
- Fascicle III tests passed.
- `geomatrix_master --validate` returned 1331 sum-state rows and 46656 ordered outcomes.
- The unique mode remained `(7,7,7)`.
- Maximum probability remained `1/216`.
- Minimum probability remained `1/46656` with 8 minimum corner states.
- Fascicle II returned closure, centre, Gamma, derivative, and MMB checks as true.
- Fascicle III returned 5 equations, 4 claim families, `100 + 100 -> 110` inherited fidelity, single 120 support retained as 120, Raphael Lite deferred, and EML#F external.

## Raphael adjunct source check

- `raphael_equations.py` compiled and ran its example.
- `fractal_expansion.py` compiled and `generate_fractal_3d` returned coordinate arrays.
- `Raphael_Runner.py` compiled, but direct import is blocked in the local uploaded bundle by the missing dependency module `time_dynamics`.

## Drive note

A Google Drive document named `GeoMatrices run confirmation` was created and moved into the active N^3 Drive folder.

## Remaining next phase

- Build EML#F as a separate source folder.
- Update workbook pipeline in place after EML#F alignment.
- Align final Drive-facing package.
- Defer Raphael Lite until the later Raphael_Physics phase.
