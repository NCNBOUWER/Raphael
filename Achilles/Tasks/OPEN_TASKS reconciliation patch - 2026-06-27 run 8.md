# OPEN_TASKS reconciliation patch - 2026-06-27 run 8

Purpose: preserve the current canonical OPEN_TASKS register without risky full-file overwrite while recording task rows that should be appended or reconciled in the next safe register mutation pass.

## Source state reviewed

- `N^3/INTERNAL/registers/OPEN_TASKS.csv` exists in Git and currently exposes T-001 through T-078 in the fetched register state.
- `Achilles/Tasks/Task delta - canonical handoff and Neo scaffold.md` queued T-079 through T-086.
- `Achilles/Tasks/Task delta - Raphael source and component packets - 2026-06-27.md` records that Raphael source tables and component paste packets were created and should be reconciled into OPEN_TASKS.
- Drive search surfaced active Achilles current task, archive extraction, delete candidate, canonical source map, ZIP Check, and handoff documents.

## Rows to append or reconcile

```csv
T-079,Archive,Inventory and classify ZIP candidates,Pending,High,Joint,ZIP Check + Archive/ZIP authoritative copy rule.md,ZIPs are inspected compared and classified as canonical candidate archive copy or duplicate-after-extraction,No deletion; ZIPs remain candidates until extraction/classification
T-080,Dashboards,Apply dashboard classification to workbook collapse plans,Pending,High,Assistant,Achilles/Dashboards/dashboard_classification.json + Achilles/Workbooks/Workbook collapse controller.md,Workbook collapse plans identify control data function project investor or archive dashboard landing types,Preserve logs at back and keep dashboards functional
T-081,Branding,Prepare durable brand asset placement,Pending,High,Joint,Achilles/Brand/brand_asset_manifest.json + Achilles/Brand/logo_policy.json,Project-specific assets have durable Git or Drive placement and dashboard family binding,Binary movement still requires Drive/Git materialisation path
T-082,Investor,Create Investor dashboard route for Google Earth material,Pending,Medium,Assistant,Achilles/Dashboards/dashboard_classification.json + Drive Google Earth folder,Google Earth is routed into Investor dashboard context rather than Operations,Drive search confirms Google Earth exists in Temporary Drives root plan
T-083,Dashboards,Apply field-specific assets across dashboard configs,Pending,High,Assistant,Achilles/Brand/brand_asset_manifest.json + Achilles/Web configs,Dashboard configs use field-specific branding and avoid universal wordmark overreach,Follow dashboard visual consistency policy
T-084,Automation,Resolve Neo independent automation slot,Blocked,Medium,Owner,Neo/Neo launch scaffold.md,Either an active slot is freed or Neo remains folded into Achilles prompts,Do not activate secondary Z stack operators
T-085,Routes,Generate remaining route proof packets,Complete,Medium,Assistant,Achilles/Web/Route proof packets,Intake claim gate component paste deployment readiness and post-publish audit packet files exist,Completed in prior route proof packet pass; reconcile status in master register
T-086,Raphael,Generate Raphael route packet set from static interactive elements plan,Complete,High,Assistant,Raphael_Packages/Route packets/Raphael route packet set - 2026-06-27.md,Raphael route packet set exists for /raphael /raphael/equations /raphael/natural-phenomena /raphael/geomatrices /raphael/emlf,Completed in prior Raphael route packet pass
T-087,Raphael,Reconcile Raphael source tables and component paste packets into OPEN_TASKS,Pending,High,Assistant,Raphael_Packages/Route packets/Raphael source tables - 2026-06-27.md + Raphael component paste packets,Master task register reflects created source/component packets and remaining route deployment readiness work,Created as safe reconciliation patch instead of overwriting register
T-088,Raphael,Generate per-route deployment readiness instances,Pending,High,Assistant,Achilles/Web/Route proof packets/deployment_readiness_packet.md + Raphael route packets,Each Raphael route has deployment readiness instance with source table claim gate and preview checks,Requires source authority verification before public copy
```

## Drive-derived open items to retain

| Item | Status | Routing |
|---|---|---|
| Achilles Current Task Register ACT-001 onward | Active | Reconcile with Git OPEN_TASKS during safe register mutation |
| Achilles Archive Extraction Register Current | Active / preservation-first | Archive queue |
| Achilles Delete Candidate Register Current | Empty / owner approval required | Delete register; no deletion promoted |
| ZIP Check folder | Active folder found | Archive queue; checksum/authority pass pending |
| ACR3 Chat Closure Handoff to Neo and Achilles | Current closure-carrier | Documents queue and agent handoff queue |
| ACR3 Drive Alignment Map | Active staging/transfer map | Drive/archive/workbook queues |

## Guardrails preserved

- Preserve source truth.
- No deletion or archive move performed.
- Archive before deletion.
- Extract useful material before disposal.
- EML#F remains external.
- Raphael Lite remains deferred.
- N^3 remains GeoMatrices.
- Google Earth remains Investor-scoped.
- ZIPs remain canonical candidates/archive copies until extracted and classified.
- Field-specific dashboard branding remains required.
- Secondary Z stack operators remain inactive.

## Next safe mutation

When a safe full-file register edit is available, append or reconcile the rows above into `N^3/INTERNAL/registers/OPEN_TASKS.csv`, then mark this patch as absorbed in a later task delta.
