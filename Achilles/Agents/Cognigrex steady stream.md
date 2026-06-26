# Cognigrex steady stream

Purpose: define the current steady-stream control surface for Cognigrex-style distributed consolidation.

## Role

Cognigrex is the distributed processing layer for distinct task streams that retain their own identity while feeding shared state back into Achilles.

## Current state

This is an active setup scaffold. It does not start the deferred Z stack.

## Source-informed stream lanes

| Lane | Historical anchor | Function | Current status |
|---|---|---|---|
| W1 archive/source stream | Deposit Analysis | inspect old files, classify source value, extract missing context | pending |
| W2 task execution stream | Luke II Catch / Hold | active tasks, blocked tasks, queued work, recent completions | active |
| W3 technical stream | RFS & EMFF | historical technical stream; keep separate from EML#F naming | review |
| W4 dependency stream | Supply Chain & Trajectory | handoffs, routing, dependency maps, throughput | pending |
| W5 scheduling stream | Mission Planning GMAT | run windows, cadence, validation sequencing | active |
| W6 dataspace stream | Asset Library Dataspace | source registry, normalization, QA, publish, pass-off packs | active |
| Workbook stream | Sheets | collapse versioned pages into final unversioned pages and logs | pending |
| Publish stream | Public/master/internal surfaces | project-specific file sets and print/publish outputs | pending |
| Agent stream | Achilles AI | assistant-agent control cards, task execution cadence, retained state | active |

## Retained-state rule

Each stream should report:

- last completed action;
- next safe action;
- blocker;
- canonical file updated;
- unresolved items added to OPEN_TASKS.

## Register discipline

Every stream must prefer register output over memory. Use:

- `OPEN_TASKS.csv` for unresolved work;
- `Ready to archive.md` for items that need preservation/move;
- `Ready to delete after extraction.md` only after extraction is complete;
- package maps for final current/canonical locations;
- workbook logs for consolidated sheet histories.

## Recovery rule

After interruption, resume from the last valid state. Use a soft retained-state summary and continue with the next safe action.

## Exclusions

- No secondary Z stack automation yet.
- No unsupervised deletion.
- No uncited factual claims.
- Do not merge W3 RFS/EMFF terminology into EML#F.
