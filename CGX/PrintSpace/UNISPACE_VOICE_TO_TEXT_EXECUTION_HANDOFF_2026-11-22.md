# UniSpace — CGX PrintSpace/Raphael voice-to-text execution handoff
**Snapshot:** 2026-11-22, Australia/Brisbane. **Status:** SOURCE-BOUND REVIEW QUEUE, NOT PRODUCTION RELEASE.

This handoff consolidates the open engineering threads of this conversation so the next ordinary text-chat session can work from one ordered queue. It is a **read-only coordination/index document**. It does not create an alternate root, runtime, DBR receipt service, source catalogue, new agent identity, manufacturing licence, physical machine command or source-authority promotion.

## 0. Authority and product topology

**UniSpace** is the umbrella. **FileSpace** owns individually governed CGX object identity, canonical/portable source, signed roots and selective hydration. **DataSpace** exchanges authenticated peer state/receipts under separate leases and readback. **PrintSpace** is the candidate digital-to-physical manufacturing consumer. **Raphael** owns reference geometry roles/metric research, **LightSpeed** owns the execution/CGX capability/DBR interfaces, and existing specialised domain sources own materials, CAD, machines and rights.

Existing source boundaries:
- [CGX PrintSpace owner review PR #6](https://github.com/NCNBOUWER/Raphael/pull/6) — integration consumer and manufacturing candidate routes; **draft**, not merged.
- [Raphael geometry owner review PR #7](https://github.com/NCNBOUWER/Raphael/pull/7) — 173 geometry role slots, Euclidean mesh reference snapshot and aliases; **draft**, not merged. Regression snapshot pinned at `4ffebc85b1f945b83359c824c2165a98eb036c86`.
- [LightSpeed CGX node exchange](https://github.com/achillesromer-coder/LightSpeed/blob/main/cgx/domain_templates/node_exchange_contract.json) and [agent runtime](https://github.com/achillesromer-coder/LightSpeed/blob/main/cgx/domain_templates/agent_runtime_contract.json) — authentication, execution leases, independent agent/node identities, capabilities, signed roots and DBR/readback.
- [Canonical 411-archetype source workbook](https://docs.google.com/spreadsheets/d/1refNFmebTcmPVojCuZsyILJEWaKz-sVzYLfZtqMl8k8/edit) — original source, not to be replaced by this project; derived census `CGA_411_ARCHETYPE_CENSUS_SOURCE_LINK_v0_1.json`.
- [Current digital regression receipt](CGX_UNISPACE_CONVERGENCE_REGRESSION_2026-11-22.md); static digital software tests **97 passed, 1 skipped, 0 failed** in [GitHub Actions run 44962013660](https://github.com/NCNBOUWER/Raphael/actions/runs/44962013660) at commit `a11ae2cbfd1750f7a5ef6cb021f1cde7920a5062`. Later changes require fresh CI verification.

**Source-of-truth policy:** Resolve existing FileSpace/DBR Object_ID, State Root, DBR Root, owner workbook revision and source hashes at every execution boundary; historical snapshot links above are anchors, not live authority assertions. An ordinary chat transcript does not become canon merely because it describes a design.

## 1. Settled decisions: preserve as invariants

1. **Three-stage representation:** immutable conventional binary source / native CAD / machine-compatible baseline **first**; deterministic, tested reversible ternary interpretation or carrier **second**; indexed, sparse, fractalized T173 CGX geometry/semantic projection **third**. Native physical output is compiled **last**, from a frozen, approved manufacturing IR. The sample base-3 carrier is **not compression**; measure actual cold/warm bytes and costs.
2. **Zero and uncertainty are distinct:** slot **174** is Raphael's `INTENTIONALLY_EMPTY`, nonmintable, zero/sentinel role; **no 174th solid**. A sparse cell may be `EMPTY_INTENTIONAL`, `UNRESOLVED_SOURCE`, `NOT_APPLICABLE`, `CANDIDATE_BINDING`, `BLOCKED_INCOMPATIBLE` or `ADMITTED_DIGITAL`. A slot's lack of mesh does not prove its physical impossibility; a mismatch of process routes does not preclude separately built/assembled components.
3. **Six orthogonal user-facing umbrellas share one T173 source:** do **not** duplicate all 173 geometries six times or equate slots with 411 component types. Make a source-bound sparse `umbrella × T173 role` applicability map; empty cells remain empty unless evidence supports an edge.
4. **Component counts, not claims of printability:** 411 source archetypes / 15 source domains / 22 family labels. Derived six-umbrella totals **121, 111, 95, 49, 28, 7** = 411. Manufacturing-route labels mention printing for 173 archetypes, direct printing for 70 and strict `PRINT-DIRECT` for 46; **none of these classification counts prove physical qualification**.
5. **Geometry review:** 173 nonminted role slots, 131 numeric Euclidean reference meshes plus 9 shared geometric aliases = 140 mesh-backed *roles*; **33** roles without attached reference meshes; reserved 174 absent. 699 typed relation records. The Raphael metric, all-device printability, source licence and physical properties are separate proof gates.
6. **Composites:** incompatible single-process materials may be fabricated through separate toolpaths, intermediate subassemblies, protected transitions or external manufacture, then assembled if their **interface and functional requirements** pass. Do not equate local route incompatibility with functional impossibility.
7. **Decentralized intelligence:** Achilles/SAI/other agents can propose, optimize and maintain scoped digital plans via authenticated DataSpace; offline machine supervision remains a separate bounded, verified local controller. Prepaired authenticated Wi-Fi/LAN/Bluetooth candidates may be warm for failover, but no automatic pairing, no lease transfer by copying, no network-driven live-actuator mutation and no unchecked continuation during outages.
8. **Changes during printing:** DataSpace updates create new immutable revisions and signed receipts; only the verified machine/owner execution envelope can authorize future toolpath changes at controlled safe checkpoints. Completed printed layers stay immutable.
9. **Economics and rights:** base reusable reference library is open only to the extent source rights support; commercial recipes/qualified print entitlements require independent release and price controls. No launch/mint/payment/publication from a software pass.
10. **Traceability:** historical workbooks, prior branches, CAD, instrument files and experimental runs are linked by existing provenance and DBR receipts, not recopied into a newly invented master.

## 2. Source-backed catalogue / hierarchy

One indexed six-sided conceptual interface, **not six separate truths**:

| Functional umbrella (derived, noncanonical) | Source archetype count | Source domains |
|---|---:|---|
| Computation, power and control | 121 | Semiconductor; Electrical; Power/Control; Protection/Switching |
| Sensing, signals and electromagnetic communication | 111 | Sensing; RF/Communications; Electromagnetic |
| Structures, interconnects and actuation | 95 | Electrical/Packaging; Mechanical; Actuation |
| Energy, thermal and fluid systems | 49 | Energy; Fluid/Thermal |
| Optical, photonic and acoustic systems | 28 | Optical/Display; Acoustic/Ultrasonic |
| Chemical and electrochemical systems | 7 | Electrochemical/Chemical |
| **Total** | **411** | **15 source domains; 22 family labels** |

**Orthogonal filter facets** (not extra counted archetypes): spatial scale, dimensions/units, position/frame, 2D vector, mesh, B-rep/implicit solid, T173 role/alias, material/lot, porosity/lattice, atomic/molecular model *if independently physically justified*, interfaces/contacts, deposition order, directional A→B compatibility, environmental dose, surface finish/roughness, plating, encapsulation, electronics/sensors, rights, source/version, uncertainty and evidence state. A Euclidean polyhedron is **not** automatically an atom, molecule, functional battery or fluid phase. Such cross-domain mappings require the correct physical model and dimensional parameters.

## 3. Target sparse hydration model — proposed for implementation, not yet accepted

- **H0 minimal index:** stable Object_ID; owner/source revision; rights; coarse functional umbrella; geometry applicability flags including intentional zero vs unresolved.
- **H1 geometry identity:** exact source role/alias, available unitful native vector/solid/mesh hash, local transformations, incidence/manifold checks and coordinate reference; no invented solid for an unknown.
- **H2 interface and material:** oriented faces/surfaces, candidate A→B contacts, roughness, thermal/chemical/electrical property passports, lot/uncertainty and evidence, layer-contact topology.
- **H3 process and stack:** typed operation DAG, print sequencing, atmosphere/vacuum barriers, deposition/postprocess damage budget, encapsulation, external process or first-build tool alternatives, machine capability dependencies.
- **H4 coupled assembly and digital experiment:** shared simulation state, explicit physics solver and boundary assumptions, 4D stimulus and material responses, qualified source inputs, versioned run receipt; deterministic emulation is not empirical proof.
- **H5 optional sparse compound projection:** content-addressed repeat blocks/variants, instance transforms, dependencies, source hashes and receipt roots for e.g. 40 z layers × 7 xy configurations; payloads hydrate on demand. This is an **instance DAG/index**, not a new T173 geometry role or claim of compression.

A hypothetical 40-layer print with seven XY configurations yields 280 *layer-configuration placements*, not necessarily 280 unique geometries. Deduplicate by source hash and transform; compare total serialized bytes, retrieval latency, computation cost, cache misses and a bit-exact binary fallback. H4/H5 cannot increase physical evidence or authorization.

## 4. Open-thread execution queue (text-chat owner-review lane)

**P0 — exact source sync and regression**
- Read existing PR #6 head, PR #7 geometry head, LightSpeed CGX schema/DBR currentness, owner workbook revision, and capture evidence hashes without copying source bytes as canon.
- Run all existing route, inverse-build, component-geometry, material, node/lease and convergence CI on source-pinned revisions; classify FAIL vs expected HOLD vs optional SKIP.
- **Acceptance:** reproducible URL/commit/test receipt; no outstanding unclassified failure; no illegal source-master write.

**P1 — 411 × 173 × six derived sparse crosswalk**
- For each of 411 source archetypes, resolve domain/family, source row, interface descriptions, current vector/solid/mesh refs, reference T173 roles or `UNRESOLVED_SOURCE`.
- For each six-umbrella × T173 role, store **only supported edges**, typed applicability status and evidence ref; preserve no-evidence blanks; `174` is sentinel, excluded from geometry array/minting.
- **Acceptance:** 411 preserved unique IDs; 15/22 and 6 sums exact; 173 role identities stable; no fabricated CAD or atomic mapping; all edges have a cited source/ref or are explicitly hypothetical.

**P2 — geometry/math and simulation bench**
- Validate 131 source mesh incidences and 9 aliases at scale/units, classify 33 unmatched source roles, compare 2D boundary/mesh/B-rep/implicit representations where actual assets exist; preserve 174 empty.
- Introduce material/physics laws appropriate to object scale: atomistic/electronic modelling distinct from continuum fluid or mechanical mesh and electromechanical circuits; no universal T173 physics assertion.
- **Acceptance:** every numerical solver reports input source, units, assumptions, deterministic seed if needed, convergence, meaningful residuals and epistemic state; no fake experiment receipts.

**P3 — directed interface and multimaterial sequencing**
- Integrate existing 72 directed material candidate routes, 196 family ordering candidates, and build dependencies; verify source label vs real test.
- Support contact surface textures and coatings, interface gradients, atmosphere transitions, protection/barrier checks, heat/chemical exposure budgets, porous interfaces, sacrificial supports and postprocessing.
- **Acceptance:** A→B independent of B→A; missing data stays HOLD; composite decomposition can route around *local* process conflicts only when full assembly requirements pass.

**P4 — in-process Achilles pet digital exemplar**
- Model functional shell, sensor(s), conductor paths, actuator and power unit, connectors, software/AI hosting, protective encapsulation, test points and separation between printed form, externally sourced parts and embedded compute.
- Compile source → ternary → T173 references → H0–H5 hydration → candidate print DAG → dry-run digital receipts, keeping user-requested changes as proposed future-layer revisions only.
- **Acceptance:** no motion or real-time controller implied; explicit unsupported/missing source and build/tool requirements; rights and device safety gates; source-pinned model.

**P5 — decentralized/nearby warm-link fallbacks**
- Extend existing CGX node-exchange and runtime (not a new transport server) with registered Bluetooth/Wi-Fi peer capability, pairing/identity attestation, lease epoch fencing, stale/replay prevention, split-brain holds, signed packet/readback, failover thresholds, local bounded controller policy.
- **Acceptance:** actual second-node signed tests and measured failover with disconnected network; until then status is *simulated policy only*, not live transparent handover.

**P6 — hardware qualification and release (blocked)**
- Machine identity and calibration, coupon/interface chemistry, electrical/safety isolations, dimensional/material metrology, closed-loop telemetry, environmental tests, DBR native receipts, independent owner release.
- **Acceptance:** physical evidence, independent safety review, rights and owner approvals. None are implied by the digital staging branch.

## 5. Already implemented on this draft review branch

- `cgx_printspace_shell.py`: conventional bytes, reversible 6-trit-per-byte illustrative converter, safe geometry lookup, candidate dependency/capability/rights plan, review-only in-print revision proposal.
- `cgx_printspace_t173_projection.py`: pinned PR #7 Euclidean mesh role/alias crosswalk; does not clone 131 meshes or admit geometry for production.
- `cgx_unispace_link_policy.py`: deterministic *read-only* link preference, trusted-adapter receipt and safe-offline recommendation; no actual Bluetooth transport.
- `test_cgx_convergence_regression.py` and existing PrintSpace tests; last independently read CI result above (97 pass, 1 skip). Re-run after subsequent branch changes.
- `CGA_411_ARCHETYPE_CENSUS_SOURCE_LINK_v0_1.json`: original-owner-source linked 411 / 15 / 22 census with additive six-umbrella rollup. **Derived classification only.**

## 6. Decisions/gates requiring owner or empirical input

- Confirm exact current source workbook and licences where newer revisions conflict; never elevate a stale local hash by guesswork.
- Choose a demonstrable first **physical** material/process/coupon class only once machine instrumentation, operator control and safety plan are available.
- Distinguish conceptually **zero (H0 EMPTY)**, **unknown**, **not applicable**, **blocked** and **valid compound** in the viewer. An intentionally empty slot can be serialized for simulation but never minted or executed as a mesh.
- Review hardware/network transfer implementation before live pairing or printing; keep PC01 proposals and stylized geometry distinct from actual calibration.
- Leave PR #6 and PR #7 **draft and unmerged** until the existing source-owner acceptance and DBR release gate passes.

## 7. First execution action in ordinary text chat

Start with **P0 and P1 together**: reconcile live source heads, verify the existing CI and source hashes, then populate **only independently justified source-linked** archetype→geometry applicability edges (including truly blank/unknown cells). Deliver a machine-readable sparse crosswalk, counts and per-entry evidence flags; do not generate 1,038 speculative geometry claims merely to fill a 6×173 matrix. Then run focused geometry and build-graph tests. This is the continuation point; no need to reopen the whole conversation.
