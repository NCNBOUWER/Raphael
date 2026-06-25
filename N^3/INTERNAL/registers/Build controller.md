# Build controller

Name: **Fascicle II wake-up controller**

Purpose: lightweight interaction and tracking surface for the next N^3 build phase. This controller keeps the build in scope, avoids placeholder smoke-test responses, and records the six smart tasks used to drive the next pass.

## Loading bar

```text
Fascicle II wake-up controller
[██████░░░░] 60% prepared
```

Prepared means: project memory assimilated, EML correction locked, terms registry created, open tasks updated, and build boundaries confirmed. Remaining work is the actual Fascicle II build execution.

## Six smart tasks

| # | Task | Status | Function |
|---:|---|---|---|
| 1 | Confirm scope | Complete | Keep Fascicle I as math/probability, Fascicle II as classical analysis, Fascicle III as Raphael. |
| 2 | Lock terminology | Complete | Use Terms.md for OBW, MMB, EML#F, Raphael Suite, proof classes, and fidelity scale. |
| 3 | Protect boundaries | Complete | Do not build Raphael Lite yet; do not merge EML into N^3 yet; do not rewrite Raphael equations. |
| 4 | Update open tasks | Complete | Track Fascicle II build work in OPEN_TASKS.csv. |
| 5 | Build Fascicle II | Next | Create OBW/MMB/classical transport proof modules, minimal code, and smoke tests. |
| 6 | Verify and merge path | Pending | Ensure the future GeoMatrices merge can absorb all three fascicles cleanly. |

## Controller features

| Feature | Description |
|---|---|
| Scope lock | Maintains the three-fascicle architecture. |
| Term registry | Calls Terms.md for canonical names and definitions. |
| Placeholder killer | Smoke tests must call real facts, terms, proof classes, and boundaries. |
| Open-task sync | OPEN_TASKS.csv is the live action register. |
| Boundary firewall | Prevents EML/Raphael/physics category leakage. |
| Fidelity ladder | Uses 100 / 110 / 200 / 250 scale. |
| Build mode | No more staging language unless explicitly requested. |
| Future merge | Keeps Fascicle II minimal and future-mergeable into GeoMatrices. |

## Standard response hooks

Use these hooks in future prompts to reactivate the controller.

| Hook | Expected assistant behaviour |
|---|---|
| `Wake Fascicle II` | Load Terms.md and OPEN_TASKS.csv, then continue the six smart tasks. |
| `Show controller` | Print the loading bar, task table, and next concrete action. |
| `Run build mode` | Begin Fascicle II file/code/proof execution. |
| `Check boundary` | Check Raphael, EML, and physical-claim leakage. |
| `Smoke test terms` | Confirm terms registry calls return concrete values. |
| `Update tasks` | Edit OPEN_TASKS.csv with completed/new tasks. |

## Current next action

Begin Fascicle II build mode with:

1. Omnicompounded Barycentric Well proof module.
2. Multi-Observer Multi-Function Breakdown proof module.
3. Classical transport / covariant bridge module.
4. Minimal code harness reading Terms.md.
5. Smoke tests for OBW, MMB, proof classes, fidelity scale, Raphael boundary, and EML boundary.

## Hard build constraints

- EML Function is third-party source work in EML#F.
- EML is not EM Function, EMFF, or RFS.
- Raphael Lite is deferred until all fascicles are complete.
- Raphael equations are fixed and source-governed.
- Fascicle II builds classical analysis and GeoMatrices objects, not Fascicle III Raphael claims.
- File names should be plain and clean, without version strings in front-facing names.
