# Row-level extraction - ACR3 registers - 2026-06-26

Purpose: extract row-level work items from the current visible ACR3 workbook registers into Achilles task, archive, and package-map routing.

## Sources read

| Source workbook | Tabs/ranges read | Use |
|---|---|---|
| `ACR3_Raphael_LightSpeed_Workbook_Finalisation_Register_2026_06_24` | `00_Control`, `01_Workbook_Index`, `02_Finalisation_Order`, `05_Transfer_To_Achilles`, `06_Open_Items` | controlling workbook finalisation register |
| `ACR3_COMP1_Drive_Orchestration_Execution_Register_2026_06_09` | `02_Move_Order`, `03_Unresolved` | drive move/archive and unresolved items |
| `ACR3_Future_Landing_Library_Notebook_Expansion_Register_2026_06_02` | `06_Open_Build_Items` | future landing/library/notebook build queue |

## Control extraction

The controlling register states:

- current staging account: `hotdogg3211@gmail.com`;
- final publishing / agent account: `achilles.romer@gmail.com`;
- Raphael fields include `EML#F / EM#F and N^3` and are excluded from direct Römer temporary assimilation;
- physical Drive moves require a move-capable lane;
- the register should be treated as a compact state carrier for future turns.

## Canonical workbook/source routing

| ID | Workbook / register | Status | Route |
|---|---|---|---|
| WB-001 | `Romer_EMASSC_LinkDrive_DataIndex_Workbook_v0_1` | canonical | Library / Operations + DataSpace |
| WB-002 | `LightSpeed_Web_Shell_Builder_CL3_v0_2` | active build | CYC / LS Web + Logs / LS Web |
| WB-003 | `ACR3_Future_Landing_Library_Notebook_Expansion_Register_2026_06_02` | active | Library / Operations |
| WB-004 | `ACR3_COMP1_Drive_Orchestration_Execution_Register_2026_06_09` | active | Logs / Drive Placement |
| WB-005 | `ACR3_Hotdogg3211_Drive_Alignment_Map_TEMP_TO_ACHILLES_2026_06_24` | active | Logs / Transfer |
| WB-006 | `Paradoxical_Progress.xlsx` | exclude from Römer temp | Raphael / EML#F / N^3 lane |
| WB-007 | `romer_national_commitments_dossier_compact_memory_pack.xlsx` | dossier | Library / National Dossier |
| WB-008 | `romer_national_commitments_dossier_final_elevation_pass.xlsx` | dossier | Library / National Dossier |

## Finalisation order extracted

1. Keep Temporary Drives canonical five-folder structure and approved Library/Google Earth handling.
2. Keep canonical workbook indexes in Library/Operations and Logs/Transfer.
3. Use LightSpeed Web workbook as the manual Squarespace/cross-platform launch map.
4. Keep LightSpeed Go under the private app runtime path and Logs/LS GO.
5. Preserve Raphael workbooks as active development fields; cross-reference only.
6. Track national dossier workbooks under Library/National Dossier or Library/Operations.
7. Transfer to `achilles.romer` only after staging registers, indexes, and source families are aligned.

## Transfer batches extracted

| Batch | Contents | Readiness |
|---|---|---|
| T1 | Control registers and alignment maps | ready after physical placement |
| T2 | LightSpeed Web / Squarespace builder and route proof logs | ready after manual embed tests |
| T3 | LightSpeed Go private app build records | staged; auth review |
| T4 | Raphael references only | reference; do not move field folders |
| T5 | National dossier workbooks | public-safe review required |

## Open items extracted

| Source ID | Item | Routing |
|---|---|---|
| O-001 / U-005 | Physical Drive moves | keep T-036 blocked; manual or move-capable lane required |
| O-002 / U-004 | Workbook duplicates and duplicate ZIP packages | move/archive into ZIP Check; select authoritative copy after checksum |
| O-003 | `achilles.romer` transfer | create transfer/publishing task after Temporary Drives placement pass |
| O-004 | Public deployment / Vercel project | create deployment/import task after build checks |
| U-001 | `Data_Achilles_Dashboard_Code_Block_CL3_v0_1` | classify as public route block or admin/control dashboard |
| U-002 | `Copy of Pantry Sales Tracker 2026.xlsx` | archive/quarantine outside launch root |
| U-003 | Google Earth folder | decide root exception vs Library/Google_Earth placement |

## Move/archive candidates extracted

| Item | Destination / default | Routing |
|---|---|---|
| Duplicate ZIP packages | ZIP Check | add to Ready to archive; checksum pending |
| `Copy of Pantry Sales Tracker 2026.xlsx` | Library/99_Archive_Non_Project or outside Temporary Drives | add to Ready to archive/manual quarantine |
| `SHFF_Staged_Digital_Twin_Display_Rules_CL3_v0_1` | Library/Digital_Twins/SHFF | search required |
| `Raphael_Schema_Seed_Pack_CL3_v0_1` | Library/Schemas_and_Seeds/Raphael | search required |
| Web shell / route deployment logs | CYC and Logs/LS Web | move-ready; not archive |
| Repo bootstrap/finalisation/split handoffs | Agents/Neo or Logs/Repo_Handoff | move-ready; not archive |
| UI/Codex prompts | Agents/Athene, Agents/UI_CoRunner, Agents/Codex | move-ready; not archive |
| National commitments dossier materials | Library/National_Dossier and Agents/Subagent_Execution_Plans | move/mirror; public-safe review required |

## Future build items extracted

| Priority | Build item | Routing |
|---|---|---|
| 1 | Library Master Landing | package-map / Drive file-set task |
| 2 | Notebook Master Landing | package-map / Drive file-set task |
| 3 | Per-system Digital Twin Landing Docs | project-specific publish surfaces |
| 4 | Route Proof Packet Templates | build after COMP-2 pass |
| 5 | Cross-system audit envelope | deferred until Go/Web/Neo/CCC boundaries are stable |

## Applied task routing

- Existing T-036 remains the physical move blocker.
- New tasks should be added for authoritative ZIP selection, dashboard-code classification, pantry archive/quarantine, Google Earth folder placement, `achilles.romer` transfer readiness, Vercel project import/deploy, digital twin landing docs, route proof packet templates, and cross-system audit envelope.
- T-059 can be marked complete after `OPEN_TASKS.csv` and `Ready to archive.md` are updated.

## Boundary

This pass extracts and routes row-level content. It does not mutate the Google Sheets or perform Drive moves/deletions.
