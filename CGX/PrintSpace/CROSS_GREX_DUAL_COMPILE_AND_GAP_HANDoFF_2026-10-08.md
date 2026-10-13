# CGX-F4D | Cross-Grex Product Atlas and Dual Manufacturing Compiler
Document ID: CGX-F4D-PORTFOLIO-20261008 | v0.5 | DRAFT / OWNER REVIEW

## Purpose
Connect the existing 70 functional technology classes and 14 directional material families to 80 named product and project archetypes spanning wearables (7), usable personal electronics (11), operable robotics/automation (10), backend/SAI (10), Eco-Grex (9), Römer/EMASSC (13), Socie-Civil infrastructure (7), PrintSpace/Raphael research (9), and community/operations (4).

## Deliverables
- `PRODUCT_ATLAS_TAXONOMY_v0_5.json` — Grex lanes and 17 non-qualified process family templates.
- `PRODUCT_ATLAS_SEEDS_A_v0_5.json`, `B`, `C` — explicit product contracts, PT IDs, intended functions, hybrid modules, gaps and tests.
- `CROSS_GREX_PRODUCT_ATLAS_v0_5.json` — 80 expanded dual-compile records, 586 PT references spanning **all 70** existing UTP technology IDs, 475 conceptual process stages and 395 directional stage transitions. All production flags false.
- `CROSS_GREX_SHARED_PRIMITIVES_v0_5.json` — 70 shared PT classes sorted by how many archetypes reuse them; reusable designs do **not** imply physical interchangeability.
- `CROSS_GREX_GAP_REGISTER_v0_5.json` — 220 open owner-review gaps with heuristic discipline classification, no fabricated closure.
- `cross_grex_atlas_compiler.py` — read-only compiler with `--product <ID>`, `--mode top|bottom|both`, and `--compare ID1 ID2`.
- `test_cross_grex_product_atlas_v0_5.py` — coverage/integrity and energy-last sequence checks.

## Dual direction contracts
**Top-down:** Intended product output → PT technology composition → geometric/physical modules → hybrid parts (not print-equivalent) → system acceptance tests.
**Bottom-up:** Material/feedstock IDs → directional X→Y candidate process family → controlled environment and stage transitions → cumulative exposure/previous feature survival → coupon evidence → subsystem/function verification.
**Reconciliation:** use stable UTP PT IDs, CGX material/passport IDs and capability/readback receipts. If the printed system and top-down function are not jointly met, emit a quantified gap and preserve alternative routes.

## Example group links and device gates
- Wearables: watch/ring/glasses/neckline, skin safety, RF tuning, power, thermal and optical comfort.
- Usables: a complete phone-like **hybrid** product can integrate printed enclosure, antenna, mechanical, conductive and optical components while the SoC/memory/camera/display remain qualified modules. This is not a claim of fully printed smartphone semiconductor fabrication.
- Operables: Butter Bot, coffee machine, arm, rover, inspection and assistive devices; interlocks for human contact, heat, food safety, force, motion and fail-safe authority.
- Backend: home host, router, CGX node, SAI public/private/government/defensive infrastructure, LightSpeed GO. Access and data authority are not hardware printing equivalence.
- Eco-Grex: acoustic surrogate/faux habitat, nests, bioacoustic sensors, water/soil, circular feed, EcoX and fauna-safe remediation; permits, ethical baselines and toxicity qualification are mandatory before deployment.
- Römer: Mark 1P, III/V, Solar Hull, Free Flow, RFS/EMFF, Luke II/IV, InterSol, asteroid/ISRU, space service and Mission 1 interfaces. Flight and novel-physics readiness remain **unproven**; independent mission/physics gates remain mandatory.
- Socie-Civil: SEQLD M1 raised deck/river nodes, acoustic and transport surfaces, water misting, sensor and resilience infrastructure. No structural safety claims without certified engineering.
- PrintSpace R&D: Printer-1, Printer-micro, roaming printer, gas cell/plasma, photonic/semiconductor, fluidics, electrochemistry, post-mix and ISRU qualification programmes.
- Operations: Riverlee Rose tool/kits, educational maker kits, consultancy repair and public environmental monitoring.

## Candidate architecture constraints
1. **Never** fabricate a supposedly qualified numerical property. The 531 material-property slots remain evidence-empty until measured or source-traceably populated.
2. Process pair codes S/T/M/P/R inherited from the generic family matrix represent route *search hints*, not production.
3. Active electronics and protected battery modules are placed late. The robot path was corrected to `MT→TP→EL→CI→DE→MG→SC→BT` as a safe *planning order*; actual compatibility requires additional proof.
4. When a stage requires a different environment, search common-window, sequential, isolated chamber, qualified interlayer and modular alternatives rather than defaulting to impossibility.
5. Earlier layers must survive all later thermal, field, chemical and mechanical exposures. Planned tests do not replace observed evidence.
6. C0 owner/operator/machine physical safety is separate from C1/C2 orchestration; human sign-off and actual coupons are prerequisites for actuation or released hardware.
7. Grex owner maps are proposed responsibility references and do not transfer control of another branch, company or existing source.
8. Do not mutate the promoted Cognigrex S92 recovery carriers or conflate this PR with merged production state.

## Worked CLI
```sh
cd CGX/PrintSpace
python cross_grex_atlas_compiler.py --product FU-01 --mode both
python cross_grex_atlas_compiler.py --product FO-01 --mode bottom
python cross_grex_atlas_compiler.py --compare FU-01 FB-01
python -m unittest -v test_cross_grex_product_atlas_v0_5.py
```

## Source of truth and handoff
This branch extends Raphael PR #6. Upstream UTP technology/component ontology and owner process remain in Raphael PR #5. Post-Mix composition data remain in `achillesromer-coder/Data` PR #11. The interactive in-chat Visualize is a view of these plans, not the canonical execution environment.

## Next qualification
Generate a ranked shared-module dependency graph from `CROSS_GREX_SHARED_PRIMITIVES_v0_5.json`, resolve real component supply/print/insert trade-offs, and design one full integrated demonstrator (Butter Bot or local CGX sensor) with CAD, verified bills of material, quantified power/force/thermal models and authorised fabrication coupons before expanding to fully printed semiconductors, batteries, spacecraft or infrastructure.
