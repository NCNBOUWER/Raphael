# CGX-F4D | Population expansion, lineage and acceptance handoff (v0.3)
Document ID: CGX-F4D-POPULATION-20261008. State: PROPOSED, unmerged owner review.

## Why this is an extension rather than a second catalogue
Raphael UTP PR #5 already contains **70** PT umbrella technology classes, feedstock families, environment classes, interaction hypergraph, multiphysics kernels, printer identities and a C0/C1/C2 handshake. The separate Post-Mix Data PR #11 already contains a variable-feedstock mass-balance control plan and stable PMX IDs. This proposal does not edit those branches or any promoted CGX carrier. It adds directly connected material/formulation seeds and candidate directional routes in the existing PrintSpace PR #6 only.

## Coverage
- 14 manufacturing-family identities and all 196 ordered class-level candidate transitions remain in existing v0.1 assets.
- 59 named material, chemical, void or module *archetypes*, one or more in every family; no numeric AM process properties are invented.
- 3,481 (59×59) unique ordered archetype-level combinations in `MATERIAL_PAIRWISE_INDEX_v0_3.csv`. Precisely 72 link to curated candidate route designs; the remaining 3,409 inherit only an unqualified broad-family P/S/T/M/R routing suggestion, not an actual material compatibility claim.
- 72 directional material-level route seeds covering 36 selected pairs in both directions, each with process staging, candidate environment, unknowns, alternative and test measurements.
- 70/70 existing UTP functional technology classes linked to candidate material passports and preliminary parametric geometry.
- 26 environmental and interface opportunities, including deliberately induced oxidation, low-oxygen deposition, internal hermetic volumes, low energy activation and independent Earth/microgravity routes.
- 30 parametric geometry archetypes covering printed circuits, RF, batteries, interfaces, optics, thermal/flow and robotic motion.
- 72 coupon qualification plans, one per candidate directional material route; 12 initially flagged for priority study. *No experimental coupons are claimed to have been manufactured or measured*.

## Source/physical evidence doctrine
NIST documents how AM material properties can vary with feedstock, build equipment and processing environment. A NIST Materials Data Repository listing is a discovery location, **not** automatic evidence that a particular recipe is qualified. ISO/ASTM 52920:2023 is a general AM process/site qualification standard; ISO/ASTM 52953:2025 is specifically scoped to registering process-monitoring NDT data for laser-based metal powder bed fusion, with methods adaptable beyond its normative scope. This work neither accesses paywalled full standards nor claims compliance.

A material record without a measured process window is explicitly **null**, not zero or an assumed generic melting temperature. A candidate X→Y→Z remains unapproved until a real machine, material lot and process path meet quantified physical acceptance criteria. Non-adjacent effects, higher-order hyperedges and environmental transitions remain open, as described by UTP-HYPERGRAPH-001.

## Integration map
1. Resolve UTP PT ID from the canonical upstream PR #5 catalogue, not an independently authored replacement.
2. Select listed candidate material IDs, then fetch their planned family P/S/T/M/R transitions from the v0.1 196-pair catalogue.
3. Match the requested component geometry parameters and operating environment to qualified process assets; reject missing or source-unsound property assumptions.
4. Search common-window, sequential, transition, modular and investigational routes; preserve X→Y != Y→X.
5. Execute synthetic-only v0.2 scheduler to find chronological errors and unknown non-adjacent doses; treat symbolic gate names as *planned*, never an instrument receipt.
6. Create coupon records and resolve into tested evidence only with exact feed lot, machine, instrument, operator, calibration, raw files, uncertainty, acceptance and source hash.
7. Use existing PMX-MAT-001 material post-mix solver via a future independently reviewed adapter; never substitute additive rules for reactive mixing/phase evolution.
8. Promote upstream-consumed records through the actual CGX root/domain governance process and readback verification. Do not mutate promoted S92 carriers in place.

## Missing data made explicit
- 59/59 named archetypes still require measured or supplier-proven physical property passports and qualified lot-specific manufacturing envelopes.
- 72/72 directional material route seeds require stage-level experimental evidence and both-direction comparisons.
- 70/70 technology bindings are planning matches, not complete design dossiers or validated functional component products.
- Environmental control profiles use opportunity mechanisms and required sensors, not manufactured capability claims.
- Fabrication-stage printable 4D integrated systems remain a research/prototyping programme.

## Run validation
From `CGX/PrintSpace`:
```
python -m unittest -v test_multistage_route_planner.py test_printspace_population_v0_3.py
python multistage_route_planner.py --case BUTTER_BOT_HYBRID_SEQUENCE
```
No hardware command, source-branch merge, autonomous printer actuation, modified local root/Drive workbook, or production-authorised recipe is performed.

## Recommended targeted work gates
P1: coupons for PETG/PLA electronics, conductor/dielectric transitions, soluble channel templates, insulated cores, and protected module insertion, sorted by local available instrumentation. Hazardous energetic battery chemistry, live biological material and semiconductor formation remain specialist-lab routes and are *not* maker bench instructions. Coordinate those through C0 safety governance and explicit qualified operator authorisation.
