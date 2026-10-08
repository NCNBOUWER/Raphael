# CGX PrintSpace — Capability-First Functional Manufacturing (Review Branch)

Status: **PROPOSED / OWNER REVIEW**. Read-only modelling and data/QA package. No machine control or qualified print recipe.

## Current founder build/release ordering (2026-10-09)
The latest accepted physical sequence is **Bootstrap PrintCeptor manual seed assembly → safe internally fabricated upgrades → Butter Bot as first complete sealed-session integrated print and internal functional test → collaborator validation → PrintCeptor A → proposed state library/university/SQE pilots → broader commercial rollout**. Digital UTP/PMX development may remain concurrent; this does **not** impose a prior Printer-μ reproduction test before the initial Butter Bot. Main chamber defaults to one open print volume with job-created/reused secondary partitions. See [authoritative latest founder decision overlay](PRINTCEPTOR_FOUNDER_PHASE_ORDER_AND_CCC_CYC_HANDOFF_2026-10-09.md) and [current decision queue](TRANSIT_DECISION_GATE_QUEUE_2026-10-08.json). All steps are **planned**, not hardware completion.

## Entry points by responsibility
- **Capability doctrine:** [CAPABILITY_FIRST_INTERFACE_ONTOLOGY_2026-10-08.md](CAPABILITY_FIRST_INTERFACE_ONTOLOGY_2026-10-08.md) — CAN IF philosophy and process opportunities.
- **Directional process ontology:** [CROSS_DOMAIN_SEQUENCING_MATRIX_2026-10-08.md](CROSS_DOMAIN_SEQUENCING_MATRIX_2026-10-08.md) and [PAIRWISE_SEQUENCE_ROUTES_v0_1.json](PAIRWISE_SEQUENCE_ROUTES_v0_1.json) — 14×14 family pairs.
- **Material population:** [MATERIAL_CANDIDATE_PASSPORTS_v0_3.json](MATERIAL_CANDIDATE_PASSPORTS_v0_3.json) — 59 material/module/void archetypes; [MATERIAL_PAIRWISE_INDEX_v0_3.csv](MATERIAL_PAIRWISE_INDEX_v0_3.csv) — 3,481 directed material-index records (only 72 curated routes).
- **Function and geometry:** [TECHNOLOGY_MATERIAL_CROSSWALK_v0_3.json](TECHNOLOGY_MATERIAL_CROSSWALK_v0_3.json) — all 70 existing PT IDs; [PARAMETRIC_GEOMETRY_FUNCTION_SEEDS_v0_3.json](PARAMETRIC_GEOMETRY_FUNCTION_SEEDS_v0_3.json) — 30 geometries; [FUNCTIONAL_OPPORTUNITY_WINDOWS_v0_3.json](FUNCTIONAL_OPPORTUNITY_WINDOWS_v0_3.json) — 26 environment/interactions.
- **Process validation queue:** [COUPON_QUALIFICATION_QUEUE_v0_3.json](COUPON_QUALIFICATION_QUEUE_v0_3.json) — 72 proposed coupon plans; [MATERIAL_PROPERTY_MEASUREMENT_REGISTER_v0_3.csv](MATERIAL_PROPERTY_MEASUREMENT_REGISTER_v0_3.csv) — 531 currently blank material measurement slots.
- **Equations:** [PHYSICAL_EQUATION_CATALOGUE_v0_4.json](PHYSICAL_EQUATION_CATALOGUE_v0_4.json) — 59 dimensioned analytic models and UTP kernel references.
- **Equation relationships:** [PHYSICS_FUNCTION_CROSSWALK_v0_4.json](PHYSICS_FUNCTION_CROSSWALK_v0_4.json) — 70 functional types, 30 geometries, 26 environmental opportunities and 72 material routes linked to analytic screens and scale regimes.
- **Operand provenance:** [PHYSICS_OPERAND_PROVENANCE_BLUEPRINT_v0_4.json](PHYSICS_OPERAND_PROVENANCE_BLUEPRINT_v0_4.json) — 172 named input requirements, no synthetic material measurements.
- **Explanations:** [PHYSICS_FORMALISATION_AND_VALIDATION_2026-10-08.md](PHYSICS_FORMALISATION_AND_VALIDATION_2026-10-08.md) — core equations, interface calculus, continuum vs simple approximations, scope and evidence gates.
- **Implementation bridge:** [PRINTSPACE_RUNTIME_CROSSWALK_2026-10-08.md](PRINTSPACE_RUNTIME_CROSSWALK_2026-10-08.md); [PRINTSPACE_RUNTIME_HANDSHAKE_PROPOSAL_v0_2.json](PRINTSPACE_RUNTIME_HANDSHAKE_PROPOSAL_v0_2.json).
- **Lineage:** [PRINTSPACE_DATASET_LINEAGE_v0_3.json](PRINTSPACE_DATASET_LINEAGE_v0_3.json) — cross references to upstream UTP PR #5, Post-Mix PR #11, local CGX root. No authority transfer.

## Execute synthetic verification only
From this directory (standard Python, no external dependencies):
```sh
python -m unittest -v test_multistage_route_planner.py test_printspace_population_v0_3.py test_dimensioned_equation_engine_v0_4.py
python dimensioned_equation_engine.py --equation PS-EQ-001 --inputs-json '{"resistivity":1.7e-8,"length":1.0,"area":1e-6}'
python multistage_route_planner.py --case BUTTER_BOT_HYBRID_SEQUENCE
```
This runs only read-only mathematical tests; neither command drives machinery or populates true material values. GitHub Action: `.github/workflows/printspace-data-tests.yml`.

## Scientific and governance limits
- Source authority: UTP kernel registry in Raphael PR #5. All analytic equations are screening models with stated constitutive assumptions; they do not replace coupled Maxwell/FEM/CFD/semiconductor/chemical kinetics.
- All unknown or unmeasured material properties remain null; missing evidence cannot be inferred as 0 or safe.
- Candidate print compatibility is **directional**: X→Y != Y→X. Stage ordering must preserve the full processing history of earlier regions.
- For environment opportunity: specify actual controllable atmosphere, temperature, pressure, gravity regime and measured dose; protect and qualify sensitive structures before subsequent transitions.
- Production remains off: every new data record and calculation has `production_approved=false`, with no physical machine-control connector.
- Prefer human/owner review through the existing CGX and LightSpeed C0/C1/C2 governance and audit gate, not unreviewed binary carrier modification.

## Next evidence intake
Load exact supplier lot passports, resolved geometry/tolerances, qualified machine cells and measured property uncertainty, then run X→Y and X→Y→Z comparative coupons. Capture independently verifiable receipt IDs for every stage and inspect predicted-vs-measured residuals before promoting a route beyond candidate-only.
