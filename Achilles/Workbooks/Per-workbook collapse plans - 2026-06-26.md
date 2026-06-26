# Per-workbook collapse plans - 2026-06-26

Purpose: record the first metadata-based collapse plan for currently visible workbook/sheet sources.

## Source discovery

The current Drive search surfaced the most relevant current workbook register as `ACR3_Raphael_LightSpeed_Workbook_Finalisation_Register_2026_06_24`, created 26 June 2026 and updated 26 June 2026.

Additional relevant workbook/sheet sources surfaced:

- `ACR3_COMP1_Drive_Orchestration_Execution_Register_2026_06_09`
- `ACR3_Future_Landing_Library_Notebook_Expansion_Register_2026_06_02`
- `Raphael Unified Physics Framework Elements and Theoretical Constructs`
- `Romer_EMASSC_LinkDrive_DataIndex_Workbook_v0_1`
- `Website Logs`

## Plan A - Raphael / LightSpeed workbook finalisation register

Spreadsheet: `ACR3_Raphael_LightSpeed_Workbook_Finalisation_Register_2026_06_24`

Sheets observed:

- `00_Control`
- `01_Workbook_Index`
- `02_Finalisation_Order`
- `03_Raphael_Boundary`
- `04_LightSpeed_Boundary`
- `05_Transfer_To_Achilles`
- `06_Open_Items`

Collapse approach:

1. Treat this as the current controlling register for workbook finalisation.
2. Preserve `00_Control` as the active control page.
3. Use `01_Workbook_Index` as the source list for workbook families.
4. Use `02_Finalisation_Order` as the execution order.
5. Preserve `03_Raphael_Boundary` and `04_LightSpeed_Boundary` as project-boundary guards.
6. Use `05_Transfer_To_Achilles` as the Achilles transfer surface.
7. Convert `06_Open_Items` into `OPEN_TASKS.csv` entries where items are not already present.
8. Add a consolidated log page only after row-level inspection.

Status: ready for row-level inspection.

## Plan B - Drive orchestration execution register

Spreadsheet: `ACR3_COMP1_Drive_Orchestration_Execution_Register_2026_06_09`

Sheets observed:

- `Sheet1`
- `00_Control`
- `01_Current_Root_Files`
- `02_Move_Order`
- `03_Unresolved`
- `04_Return_Protocol`

Collapse approach:

1. Use `00_Control` as the execution gate.
2. Treat `01_Current_Root_Files` as current Drive root file inventory.
3. Treat `02_Move_Order` as source for Ready to archive / manual desktop actions.
4. Transfer `03_Unresolved` into `OPEN_TASKS.csv` where still current.
5. Fold `04_Return_Protocol` into Achilles protocol addendum if it contains recurring standards.
6. Preserve `Sheet1` only if it contains raw or early-version data not represented elsewhere.

Status: ready for row-level inspection.

## Plan C - Future landing / library notebook expansion register

Spreadsheet: `ACR3_Future_Landing_Library_Notebook_Expansion_Register_2026_06_02`

Sheets observed:

- `Sheet1`
- `00_Control`
- `01_Landing_Documents`
- `02_Notebooks`
- `03_Library_Index`
- `04_Project_Routes`
- `05_Source_Authority`
- `06_Open_Build_Items`

Collapse approach:

1. Use `00_Control` as owner/intake gate.
2. Use `01_Landing_Documents` for project-specific Drive file set population.
3. Use `02_Notebooks` for master/internal/public notebook mapping.
4. Use `03_Library_Index` for source/library package map.
5. Use `04_Project_Routes` for project routing and package boundaries.
6. Use `05_Source_Authority` to resolve canonical vs archived source hierarchy.
7. Convert `06_Open_Build_Items` into `OPEN_TASKS.csv` where still current.
8. Preserve `Sheet1` only if it contains early/raw source records.

Status: ready for row-level inspection.

## Plan D - Raphael Unified Physics Framework Elements and Theoretical Constructs

Spreadsheet: `Raphael Unified Physics Framework Elements and Theoretical Constructs`

Sheets observed:

- `Table 1`
- `Source References`

Collapse approach:

1. Treat `Table 1` as a content-source table for Raphael / Raphael_Physics / N^3 boundary checks.
2. Treat `Source References` as source authority and citation map.
3. Do not merge this into EML#F or N^3 without explicit source-boundary review.
4. Use it to update publish/print surfaces and the final holistic package map.

Status: ready for row-level inspection.

## Plan E - LinkDrive data index workbook

Spreadsheet: `Romer_EMASSC_LinkDrive_DataIndex_Workbook_v0_1`

Observed through search as a relevant workbook source. Metadata inspection remains pending.

Collapse approach:

1. Inspect metadata and tabs.
2. Identify whether it is current, archive, or bridge inventory.
3. Route active file entries into package maps.
4. Route unresolved/missing entries into `OPEN_TASKS.csv`.

Status: metadata inspection pending.

## Next actions

1. Read bounded row ranges from Plan A control/index/order/open-items tabs.
2. Extract current tasks into `OPEN_TASKS.csv`.
3. Add archive/move items to `Archive/Ready to archive.md`.
4. Repeat for Plan B and Plan C.
5. Defer destructive cleanup until extraction and approval.

## Boundary

This file is a plan and metadata summary. It does not mutate spreadsheet contents yet.
