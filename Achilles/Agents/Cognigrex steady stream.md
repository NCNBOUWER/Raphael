# Cognigrex steady stream

Purpose: define the current steady-stream control surface for Cognigrex-style distributed consolidation.

## Role

Cognigrex is the distributed processing layer for distinct task streams that retain their own identity while feeding shared state back into Achilles.

## Current state

This is a setup scaffold only. It does not start the deferred Z stack.

## Stream lanes

| Lane | Function | Current status |
|---|---|---|
| Archive stream | inspect older files and extract useful context | pending |
| Workbook stream | collapse versioned sheets into final unversioned pages | pending |
| Drive stream | map current folders and manual desktop actions | active |
| Git stream | update protocols, registers, maps, and reports | active |
| Publish stream | prepare project-specific file sets and print surfaces | pending |
| Agent stream | maintain Achilles Assistant Agent and task execution cadence | active |

## Retained-state rule

Each stream should report:

- last completed action;
- next safe action;
- blocker;
- canonical file updated;
- unresolved items added to OPEN_TASKS.

## Recovery rule

After interruption, resume from the last valid state. Use a soft retained-state summary and continue with the next safe action.

## Exclusions

- No secondary Z stack automation yet.
- No unsupervised deletion.
- No uncited factual claims.
