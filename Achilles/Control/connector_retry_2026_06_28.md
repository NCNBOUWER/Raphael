# Achilles connector retry — 2026-06-28

Status: connector retry pass complete.

Scope checked:
- Google Drive
- GitHub
- Files / Library
- Slack public channel surface
- Supabase
- Neon Postgres
- Automations

Deferred Z stack: untouched.

## Findings

Google Drive: active Achilles and LightSpeed control documents and workbooks are discoverable. Drive remains the current authority surface for task registers, source maps, archive extraction, delete-candidate policy, and web-shell/workbook staging.

GitHub: installed repository search exposes `NCNBOUWER/Raphael`. Standalone LightSpeed, Achilles, Romer, and Link-Drive repositories were not visible through the current GitHub installation during this run. Within `NCNBOUWER/Raphael`, Achilles task/control/workbook paths are discoverable.

Slack: public channel search found the all-Romer channel. Public channel history had no extractable project content beyond the channel join event.

Supabase: connector is enabled but returned no accessible projects.

Neon Postgres: connector is enabled and organization access exists, but returned no accessible projects.

Automations: the Achilles Daily Consolidation automation was updated to request all currently enabled connector surfaces on future runs.

## OPEN_TASKS delta

- ACT-CONN-001: confirm GitHub connector installation covers the required project repositories.
- ACT-CONN-002: identify or create the selected database deployment target before backend consolidation.
- ACT-CONN-003: keep connector-inclusive daily consolidation enabled.
- ACT-CONN-004: merge this connector retry note into the current Achilles task/control lane.

## Blockers

- Drive physical moves and document/sheet writes remain outside this connector run.
- GitHub access is limited to the visible installed repository set.
- Supabase and Neon have no current projects to inspect.
- Slack public surface currently has no extractable project messages.
- ZIP inventory and checksum work remains pending until archives are materialized/exportable.
