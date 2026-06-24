# NBT-007 — Aesthetic and Product Cleanliness Pass

## Objective

Produce a clean, navigable, version-controlled research package suitable for internal review, Drive mirroring, and later publication preparation.

## Cleanliness decisions

- Binary archive storage is excluded from Git where possible.
- Python cache directories are excluded.
- README now acts as the front-door governance index.
- Proof claims are separated from correspondence hypotheses.
- The package distinguishes three layers:
  1. **Proven finite mathematics**;
  2. **Geometric/trajectory support layer**;
  3. **Raphael correspondence / audit-pending layer**.

## Aesthetic conventions

- Use short section titles.
- Use tables for gates, metrics, and statuses.
- Use `P0–P5/PX` proof status everywhere.
- Do not use physical-unification language unless the claim is explicitly marked as hypothesis or correspondence.
- Keep source code in `05_Code/` and proof appendices in `02_Proof_Appendices/`.

## Final packaging rule

Main branch should contain normal text/data/source files. ZIP files may be used for transfer or release assets, but should not be used as the primary repository structure.
