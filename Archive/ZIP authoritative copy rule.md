# ZIP authoritative copy rule

Purpose: define how ZIP files are handled during Achilles archive-data amalgamation.

## Rule

ZIP files are not automatically treated as disposable duplicates. Each ZIP is classified as one of:

1. **Canonical candidate** — may contain the most complete or useful source set.
2. **Archive copy** — preserved for provenance, rollback, or checksum comparison.
3. **Duplicate after extraction** — eligible for approval-gated deletion only after all useful information has been extracted into the canonical fileset.

## Required sequence

1. Inventory all ZIP files with human-readable names, locations, dates, sizes, and known source context.
2. Extract or inspect contents where safe and necessary.
3. Compare against current canonical folders, docs, sheets, code, and package maps.
4. Select one authoritative copy or canonical extracted fileset.
5. Assimilate useful files/content into current canonical/save locations.
6. Move remaining ZIPs to Archive or ZIP Check.
7. Add unresolved or conflicting content to `OPEN_TASKS.csv`.
8. Add only fully extracted duplicates to `Ready to delete after extraction.md`.
9. Weekly owner approval is required before deletion.

## Selection criteria

| Criterion | Meaning |
|---|---|
| Completeness | Contains the broadest intact fileset or latest clean source. |
| Recency | Newer only wins when content is also complete or confirmed. |
| Validation | Contains test output, checksums, or run confirmations. |
| Provenance | Has a clear source, generation context, or commit link. |
| Non-duplication | Adds unique files or context not present elsewhere. |
| Safety | Does not contain unsupported public claims, private material for public routes, or unreviewed destructive instructions. |

## Current operational status

- Duplicate ZIP packages remain archive/checksum candidates.
- No ZIP deletion is approved.
- ZIP material may be canonical only after extraction and comparison.
- The final canonical fileset should be folder/doc/sheet/code based, not ZIP-dependent.

## Register routing

- ZIPs awaiting review: `Archive/Ready to archive.md` and ZIP Check.
- Conflicts or missing extraction: `OPEN_TASKS.csv`.
- Fully extracted duplicates: `Archive/Ready to delete after extraction.md`.
