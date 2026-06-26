# Workbook collapse controller

Date: 26 June 2026

Purpose: control the workbook consolidation pass without destroying version history.

## Scope

Collapse versioned workbook pages into final unversioned pages, while retaining consolidated logs at the back of each workbook.

Current target families:

- Public dossier.
- Master release.
- Internal notebook.
- Paradoxical Progress.
- Any project-specific workbook or sheet surfaced during archive-data amalgamation.

## Owner direction captured

- Collapse every versioned sheet into a final unversioned page.
- Keep the back-of-workbook log structure.
- Consolidate old logs, current logs, notes, and unresolved items.
- Use Drive, sheets, open chats/strings, Git, and archives as sources.
- Add unresolved or missing items to `OPEN_TASKS.csv`.
- Do not delete without extraction and approval.

## Method

For each workbook:

1. Identify all versioned tabs/pages.
2. Group versions by final intended page.
3. Start from the earliest version.
4. Read forward through every later version.
5. Carry forward all current substance.
6. Preserve useful superseded context in the log.
7. Convert unresolved notes into open tasks.
8. Produce a final unversioned page.
9. Produce or update a consolidated log page.
10. Validate formulas, references, links, and naming.
11. Record the result in the workbook alignment report.

## Sheet naming rule

| Versioned examples | Final page |
|---|---|
| `GeoMatrices v1`, `GeoMatrices v2`, `GeoMatrices Final` | `GeoMatrices` |
| `Pipeline old`, `Pipeline v2`, `Pipeline new` | `Pipeline` |
| `Tasks`, `Tasks v2`, `Tasks final` | `Tasks` |

The exact tab names must be inspected before write actions.

## Logs

Each workbook should have a consolidated log section or tab containing:

- source versions inspected;
- carried-forward changes;
- superseded notes;
- unresolved items moved to `OPEN_TASKS.csv`;
- validation status;
- date and pass name.

## Current blocker

Actual spreadsheet mutation requires a spreadsheet execution pass against the target workbook files. Until that pass starts, this controller is the canonical plan.

## Next safe execution

1. Inspect target workbook metadata and tab names.
2. Create a per-workbook collapse plan.
3. Execute the least-risk workbook first.
4. Validate formulas and tab references.
5. Repeat across remaining workbook families.

## Exclusions

- Do not start the deferred Z stack.
- Do not build Raphael Lite during this pass.
- Do not delete source/version tabs until extraction is recorded and owner approval is given.
