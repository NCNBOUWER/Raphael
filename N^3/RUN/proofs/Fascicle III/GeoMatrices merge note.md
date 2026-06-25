# GeoMatrices merge note

Decision: `N^3` itself becomes the GeoMatrices folder after the three fascicles are complete.

## Final merge posture

The fascicles are build logs. The final live system should be minimal, navigable, and front-facing. After Fascicle III completion:

```text
N^3/
├─ WELCOME.md
├─ START.html
├─ RUN/
├─ INTERNAL/
├─ Publications/
└─ Archive/
   └─ Fascicles/
      ├─ Fascicle I/
      ├─ Fascicle II/
      └─ Fascicle III/
```

## Merge principle

Small similar files should be merged. Repeated definitions should collapse into `Terms.md`, `OPEN_TASKS.csv`, proof packs, and one public explanation surface. Fascicle-specific files should remain only where they carry distinct proof, audit, or build-history value.

## Do not do yet

- Do not collapse the fascicles before Fascicle III owner review.
- Do not build Raphael Lite during the merge.
- Do not merge EML#F into N^3.
- Do not update canonical workbooks until the post-fascicle pipeline is ready.
