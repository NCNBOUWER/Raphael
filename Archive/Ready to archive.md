# Ready to archive

Purpose: list files and folders that should be moved into Archive during the desktop/manual consolidation pass.

Rule: preserve these items. Move them into Archive first, then run archive-data amalgamation.

## Current candidates

| Human-readable name | Current ID / path | Reason | Status |
|---|---|---|---|
| Archived duplicate - Raphael adapter folder - 2026-06-25 0158 | `1ia0wnQDOBa1Ind7-MEGRIRdo0HFvhKyk` | Older duplicate Raphael adapter folder. Connector move blocked by file authorization. | Ready for desktop archive move |
| Archived duplicate - Raphael folder - 2026-06-25 0157 | `1mUIyR38XtYg9WwfjeqY5rqCqqfiAIM-u` | Older duplicate Raphael folder. | Ready for desktop archive move |
| Archived duplicate - Raphael folder - 2026-06-24 | `1ovk0wYtHzgMXIVsxDAqTT2fUsXqSjAha` | Older duplicate Raphael folder. | Ready for desktop archive move |
| Old Raphael Physics | `1QNB1rGd631KQwqksuSnQbXEnvFWYWCQD` | Old classic Raphael Physics folder already under Archive. | Extraction pending |
| Duplicate ZIP packages | `ZIP Check / duplicate package copies` | Workbook registers direct duplicate packages into ZIP Check for checksum and authoritative-copy selection. | Classify under `Archive/ZIP authoritative copy rule.md`; checksum/extraction pending |
| Copy of Pantry Sales Tracker 2026.xlsx | `Copy of Pantry Sales Tracker 2026.xlsx` | Non-core launch file; should not remain in launch root or Temporary Drives root. | Ready for archive/quarantine outside launch root |

## Move-ready but not archive candidates

These are not archive candidates yet. They should be moved to their active destinations during the desktop/manual pass:

- LightSpeed web shell builder and route deployment logs to CYC / Logs LS Web.
- Repo bootstrap/finalisation/split handoffs to Agents/Neo or Logs/Repo_Handoff.
- Terminal Codex Validation Prompt to Agents/Neo or Agents/Codex.
- UI Build CoRunner Prompt to Agents/Athene or Agents/UI_CoRunner.
- National commitments dossier materials to Library/National_Dossier and relevant agent execution plan folders.
- Google Earth materials to Investor folder, not Operations, because they support tailoring, excavation, build, and investor-facing spatial context.

## Search-required candidates

These need location/search before archive or canonical placement:

- `SHFF_Staged_Digital_Twin_Display_Rules_CL3_v0_1`
- `Raphael_Schema_Seed_Pack_CL3_v0_1`

## Intake rule

When Achilles finds a stale version, duplicate folder, old chat export, old workbook copy, or superseded package, append it here with a human-readable name, ID/path, reason, extraction state, and required owner action.

## ZIP rule

ZIPs are handled under `Archive/ZIP authoritative copy rule.md`. They may be canonical candidates, archive copies, or duplicates after extraction. No ZIP is deleted until extracted, compared, routed into the canonical fileset, and approved in the weekly deletion review.

## Desktop action

1. Open the active Raphael folder.
2. Open Archive.
3. Move the candidates above into Archive where needed.
4. Rename them using the human-readable names.
5. Leave contents intact for archive-data amalgamation.
6. Do not delete anything unless it is later listed in `Ready to delete after extraction.md` and approved.
