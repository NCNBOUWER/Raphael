# Merge readiness checklist

Purpose: convert T-030 owner review into a clear go/no-go decision before the N^3 cleanup and GeoMatrices merge pass.

## Current phase

```text
T-030 = owner review before merge
T-033 = future merge/cleanup task after owner approval
```

## Must pass before T-033

| Check | Required result | Status |
|---|---|---|
| Three fascicles present | Fascicle I, II, III files exist and are readable | ready for owner review |
| Validation present | Fascicle I-II-III validation reports exist | ready for owner review |
| EML boundary | EML#F remains external | ready for owner review |
| Raphael Lite boundary | Raphael Lite deferred | ready for owner review |
| Equations exposure | exact equations allowed in Git and source-governed | ready for owner review |
| Claims posture | ToE candidate/falsification framework, not unsupported empirical proof | ready for owner review |
| Workbooks | no current workbooks touched in this phase | ready for owner review |
| Merge target | N^3 becomes GeoMatrices live folder | ready for owner review |

## Merge actions after approval

1. Create `Archive/Fascicles/`.
2. Move or copy fascicle-specific build logs into archive.
3. Collapse duplicate concepts into `Terms.md`.
4. Keep `WELCOME.md`, `START.html`, `RUN/`, `INTERNAL/`, `Publications/`, and `Archive/` minimal.
5. Preserve proof packs, validation files, code harnesses, and audit matrices.
6. Create final GeoMatrices public overview.
7. Create final internal proof/audit index.
8. Update `OPEN_TASKS.csv` after merge.

## Do not do during T-030

- Do not merge yet.
- Do not touch workbooks.
- Do not build EML#F yet.
- Do not build Raphael Lite yet.
- Do not delete fascicle-specific files until owner review is complete.

## Owner review commands

Use one of these next:

```text
Approve T-30
Approve T-30 with edits: ...
Hold T-30 because: ...
```

If approved, the next build command is:

```text
Proceed with T-33 GeoMatrices merge cleanup
```
