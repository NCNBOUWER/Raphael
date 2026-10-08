# CGX-F4D | Interdisciplinary Directional Print Sequence Matrix
Document ID: CGX-F4D-SEQ-20261008 | Version 0.1 | 2026-10-08
Status: PROPOSED / OWNER REVIEW. Appends to CGX-F4D-CAP-20261008 in this PR; no deployed scheduler, production approval or experimentally qualified pairings are claimed.

## Goal and semantics
Enumerate every ordered X→Y family transition and discover route(s) using co-processing, sequencing, controlled atmosphere, interlayers, sacrificial stages, separate fabrication and modular placement. X→Y is distinct from Y→X. Neither implies contact, mixing or adhesion unless the geometry contract requires it. A material-family row is a *candidate planning class*, not a recipe; actual chemistry, orientation, process, machine and lifecycle conditions dominate.

## Route legend
| Code | Meaning | Default action |
|---|---|---|
| C | Shared-window candidate; same family is NOT automatically qualified | Find overlapping environment/feed/process and test coupons |
| S | Sequential candidate in one compatible process family | Cure/cool/clean X; then deposit Y and qualify interface |
| T | Transition needed (process, material interlayer, atmosphere or spatial isolation) | Compare interlayer, purge, local activation, stage split or chamber move |
| M | Modular integration | Print/obtain module separately and insert/overmould within module limits |
| R | Direct X→Y research route; do not release | Seek alternate process, reverse order, isolation or replaceable module |

Every cell is unqualified until a process passport, material passports, coupon, equipment authority and acceptance tests pass. Incompatibility of one *process route* does not imply inability to execute the *functional contract*.

## 14 material/function families
| ID | Family | Typical process | Interactions requiring qualification |
|---|---|---|---|
| MT | High-temperature metals | melt/sinter/DED | thermal, oxidation, metallurgy |
| CR | Ceramics and glasses | fire/sinter/convert | thermal, shrinkage, cracking |
| TP | Thermoplastics | melt extrusion / fusion | melt, adhesion, creep |
| RS | Photocured resin / thermoset | photocure or chemical cure | cure depth, exotherm, residuals |
| EL | Elastomers / flexibles | extrusion / low-temp cure | fatigue, adhesion, seal |
| CI | Conductive inks / traces | direct write / sinter / plate | resistivity, adhesion, current |
| DE | Dielectric / insulating inks | coat / extrude / cure | breakdown, pinholes, isolation |
| MG | Magnetic composites | deposit / align / magnetise | coercivity, field, contamination |
| OP | Optical / photonic layers | precision print / coat | transmission, finish, alignment |
| FL | Microfluidic / sacrificial channels | template / flush / seal | flow, extraction, leak |
| EC | Electrochemical active layers | wet process / seal | electrolyte, reactions, corrosion |
| SC | Semiconductor / precision modules | qualified pick-and-place | ESD, heat, precision, packaging |
| BT | Battery / power modules | insert / connect / protect | separation, safety, replacement |
| BV | Biological / bioactive layers | sterile low-energy print | viability, sterility, contamination |

## Directional cross-compatibility matrix — all 196 ordered family pairs
| X first ↓ / Y second → |MT|CR|TP|RS|EL|CI|DE|MG|OP|FL|EC|SC|BT|BV|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**MT**|C|T|T|T|T|T|T|T|T|T|T|M|M|M|
|**CR**|T|C|T|T|T|T|T|T|T|T|T|M|M|M|
|**TP**|T|T|C|S|S|S|S|S|T|S|T|M|M|T|
|**RS**|T|T|S|C|S|S|S|S|S|S|T|M|M|T|
|**EL**|T|T|S|S|C|S|S|S|T|S|T|M|M|T|
|**CI**|T|T|S|S|S|C|S|S|S|S|T|M|M|T|
|**DE**|T|T|S|S|S|S|C|S|S|S|T|M|M|T|
|**MG**|T|T|S|S|S|S|S|C|T|S|T|M|M|T|
|**OP**|T|T|T|S|T|S|S|T|C|T|T|M|M|T|
|**FL**|T|T|S|S|S|S|S|S|T|C|T|M|M|T|
|**EC**|R|R|T|T|T|T|T|T|T|T|C|M|M|T|
|**SC**|R|R|T|T|T|T|T|T|M|T|M|C|M|M|
|**BT**|R|R|M|M|M|M|M|M|M|M|M|M|C|M|
|**BV**|R|R|T|T|T|T|T|T|T|T|T|M|M|C|

**Interpretation:** Read a row as X already processed, then the column as Y next. Codes are proposed routing defaults only; e.g. TP→MT is T and often better reversed or separated because of thermal history, whereas MT→TP is also T but may be achieved via heat-first/cool-then-polymer. Specific composition and thermal history may change either classification. The full machine-readable ordered-pair catalog is `PAIRWISE_SEQUENCE_ROUTES_v0_1.json`.

## Interdisciplinary sequence examples and qualified-work candidates
| Intended function | Sequence | Class | Proposed operations and evidence |
|---|---|---|---|
| Structural metal → conductive polymer | MT→CI | T | Complete heat-intensive metal first; cool; passivate/condition or roughen locally; direct-write conductive feature; low-energy sinter; overcoat; verify resistance, adhesion, expansion cycles. |
| Polymer → high-temp metal | TP→MT | T | Consider selective low-energy metallisation or plating; otherwise reverse metal-first order or independently manufacture metal insert; never apply full metal-melt heat to unqualified polymer. |
| Ceramic → conductor | CR→CI | T | Fire or densify ceramic; clean/activate; deposit conductor; local sinter/plate; dielectric and bond tests. |
| Conductor → dielectric | CI→DE | S | Deposit and stabilise conductor; clean; dielectric print/cure; breakdown, pinhole, leakage and capacitance tests. |
| Dielectric → conductor | DE→CI | S | Cure dielectric, check moisture/surface energy; add conductor with compatible thermal budget; continuity and isolation tests. |
| Conductor → magnetic composite | CI→MG | S | Form coil/traces, protect interturn insulation; deposit magnetic composite; field-align or magnetise where compatible; flux and loss tests. |
| Resin → elastomer joint | RS→EL | S | Print rigid body; maintain join-ready surface; deposit flexible joint; cure; assess adhesion and fatigue. |
| Elastomer → resin | EL→RS | S | Stabilise elastomer and use interface primer/mechanical interlock if needed; deposit low-exotherm resin; peel and bend tests. |
| Polymer → plated conductor → polymer | TP→CI→TP | T/S | Print cavity, prepare plating seed, selective electroless/electroplate or low-T print, rinse/dry/inspect, resume compatible polymer overprint; assess trapped fluid and shorts. |
| Fluidic sacrificial → enclosure | FL→TP | S | Print sacrificial path and surrounding structure, remove/flush path before final sealing; validate unobstructed flow, extractables and leak. |
| Optical layer → housing | OP→TP | T | Protect optical surface/geometry; low-temperature enclosure or separate optic insert; wavelength response and stray-light test. |
| Wet electrode → sealed electrochemical compartment | EC→DE | T | Deposit chemistry under compatible atmosphere, include separator/isolation, activate and seal; corrosion, leakage, capacity and abuse tests as applicable. |
| Chassis → processor module → cover | TP→SC→TP | M/T | Print cavity and pads; cool; ESD-safe placement; route interconnect; functional-test; low-energy enclosure within package's temperature envelope. |
| Chassis → battery module → cover | TP→BT→TP | M | Print protected service bay; insert certified module late, add fused/protected connection, inspect, preserve replacement access; no energetic post-processing on battery. |
| Inert metal → airtight seal → atmosphere refill | MT→DE/RS | T | Qualify low-oxygen chamber; deposit sensitive feature; complete barrier/seals before refill; verify leak/permeation, electrical and cycling data. |
| Machine substrate → living bioactive layer | TP→BV | T | Complete heat-intensive/nonsterile manufacturing first, decontaminate by compatible means, transfer to controlled biological cell, deposit and protect biological material, verify viability/contamination. |
| Biological layer → high-temperature ceramic | BV→CR | R | No general directly qualified high-temperature deposition on living layer. Search alternative low-temperature ceramic precursors, spatial isolation, reversal or separate module; viability gate remains mandatory. |
| Metal → graded metal | MT→MT | C | Meter composition path; check phase stability and thermal expansion, control thermal history; perform composition, crack, residual-stress and fatigue tests. |
| Earth print → orbital print | ANY→ANY | T | Keep functional contract; requalify feed, gravity-dependent flow, particle capture, cooling and environmental safety for in-situ equipment. |
| Power module → wet electrochemistry | BT→EC | M | Keep sealed power module isolated, route chemistry through replaceable controlled cartridge, prevent short/corrosion, verify compartment seals. |

## Minimum process staging
0. FUNCTION CONTRACT: target function, outputs, loads, environmental service, replaceability and end-of-life.
1. FEEDSTOCK/TOOL PASSPORT: exact chemistry/lot, purity, storage, rheology, cure/sinter, machine/calibration/cleanliness, uncertainty.
2. TOPOLOGY & INTERFACE: touching / embedded / bonded / insulated / free-moving / graded / optically coupled / fluidically connected; each relation differs.
3. WINDOW SEARCH: shared-window C; then low-impact sequential S; then environmental/interface transition T; then module M; investigation R. Do not prioritise a route over safety.
4. DIRECTED PROCESS GRAPH: evaluate every order X→Y and Y→X, dependencies, support removals, chamber transitions and head-clearance limits; include nonadjacent cumulative damage.
5. PROCESS EXECUTION: atmosphere, thermal budget, purge/dry/cure, protective sealing, selective activation, tool changes, contamination-controlled handovers.
6. IN-PROCESS TESTS: dimension, conductivity, insulation, adhesion, porosity, phase, humidity, leak, particle/bio containment and process telemetry where relevant.
7. INTEGRATION/FINAL TESTS: energy and fluid connections, functionality, lifecycle, failure modes, service and hazard testing; owner-controlled release.

## Route physics and algorithms (engineering definitions, not material data)
- **Thermal survival:** For each already-deposited feature i, cumulative exposure is represented by a time-temperature history `T_i(t)` and material-specific damage law `D_i = integral(k_i(T_i(t), environment, stress) dt)`; the acceptable limit is experimentally determined, never globally assumed.
- **Chemical dose:** For each reactive pair, integrate measured activity/exposure over transport history; diffusion and cure depend on validated constitutive and kinetic parameters.
- **Mechanics:** Resolve residual stress and strain including time/temperature history, mismatch expansion, gradients, bond geometry and fatigue.
- **Electrics:** Verify conductor `R = integral(rho(x)/A(x) dx)` only in regimes supporting lumped approximation, and separately model dielectric breakdown, contact resistance, EMI and current-carrying temperature.
- **Flows:** Enforce continuity/species conservation, rheology, pressure drop, cure/swelling and waste/removal pathways through inaccessible voids.
- **Electrochemical/bio:** Require chemistry-specific charge/mass balance, thermal/pressure/chemical isolation and reaction/viability evidence.
- **Scheduling:** Construct a directed acyclic process graph of stages; search routes under mandatory process and safety predicates. The best path is multiobjective cost/energy/time/waste/service optimisation *after* feasibility gates; store rejected routes with reasons and fallback.

## Conditional capability acceptance
`CAN(function) IF exact_materials AND route AND measured_window AND calibrated_equipment AND safe_transition AND metrology_pass AND owner_authority`.
Never upgrade `CAN-3/CAN-4` to `CAN-1` on an untested matrix cell. Runtime tool availability remains separate from physical qualification.

## Proof queue and measurement setup
- SEQ-001: 14×14 class catalog baseline; reconcile material schema and identifiers against actual CGX repository canonical keys.
- SEQ-002: verify order-dependent CI→DE and DE→CI insulation/adherence on common substrate coupons.
- SEQ-003: TP→CI→TP pause/plate/rinse/dry/resume printed conductor coupons.
- SEQ-004: metal-first vs polymer-first selective metal interface coupons; measure adhesion, thermal dose and cycling.
- SEQ-005: protected reactive metal print + barrier before atmospheric refill, with leak/permeation/oxidation checks.
- SEQ-006: FL sacrificial channel removal and pressure-tested encapsulation.
- SEQ-007: rigid/flexible joints with fatigue coupons and graded transition candidates.
- SEQ-008: integrated SC and BT module placement with functional and safety checks (no novel battery chemistry inside first robot).
- SEQ-009: prospective orbital/microgravity transition using verified local equipment/environment data.
- SEQ-010: add test outcome/uncertainty and evidence URL to specific pair instance; re-evaluate scheduler class.

## Provenance and scope
- ISO/ASTM 52920:2023: manufacturing process planning, sequence, qualification and traceability: https://www.iso.org/standard/76911.html
- ISO/ASTM 52953:2025: metal AM process-monitoring data registration (not general qualification of every polymer/bio system): https://www.iso.org/standard/84117.html
- Metal/polymer hybrid review (2025): https://www.nature.com/articles/s44334-025-00045-w
- Microfluidic multimaterial review (2026): https://link.springer.com/article/10.1007/s40964-026-01847-w
- Hybrid printed electronics with pick-and-place (2017): https://doi.org/10.1002/adma.201703817
- In-situ copper plating through stop-and-go extrusion (2026): https://doi.org/10.1002/admt.202502555
- Dissimilar-metal interface review (2026): https://link.springer.com/article/10.1007/s40964-026-01888-1

This matrix is a *comprehensive cross of the 14 defined high-level process families*, not a claim of having tested every pair of real materials. Each physical implementation must instantiate a pair or longer sequence with exact material identifiers and evidence.
