# Bootstrap 4D Printer → expandable printer-family doctrine
**Founder decision date:** 2026-10-08, Australia/Brisbane
**Authority:** PrintSpace PR #6, review-only engineering doctrine. Does not override Raphael/UTP, Post-Mix, RootAuthority, Römer safety or production ownership. Nothing described here is physically built, commissioned, certified or deployed.

## Founder-approved decisions
1. **Bootstrap 4D Printer** is the simple designation for the first, function-first manufacturing machine (formerly "Printer-1"). Its primary purpose is to establish and iterate *all defining capabilities of the intended CGX 4D-printing system* and use them to make the next, visually refined printer and a wider family. Its cosmetic finish may be secondary, but safety is never optional.
2. **All 4D-defining features are mandatory architectural research requirements from generation one.** If a feature is immature or causes build difficulty, retain its target, explicit interface, provisional method, risk and qualification plan instead of silently omitting it or declaring completion. Experimental failures supply evidence; they do not excuse unsafe operation. A simulation/placeholder is not an operational implementation.
3. **Self-bootstrapping capability:** Deliver only the minimum *operable and safely contained* hardware required for a seed printer to manufacture additional modules/structural components and expand its own utility, where supported by demonstrable tool/material capability. The bootstrap system must have a complete and auditable expansion path; do not assume the first seed can produce pressure vessels, semiconductor dies, qualified motors, or its own firmware/electronics.
4. **Refined next generation:** The printer manufactured using the Bootstrap 4D Printer must be more aesthetically refined and production-aware. Appearance requirements do not outrank qualified vacuum/positive-pressure/gas containment, safeguarding, electrical requirements or functional equivalence.
5. **Product family:** Later printers differ by **scale**, **application**, **function** and optionally **colour-coded identification**. The single-user personal unit is not necessarily the commercial/industrial unit. Preserve an explicit mandatory 4D-capability baseline versus transparent application-dependent modules and safety qualifications. Colour coding is a candidate identification system, not a licence to remove mandatory features.
6. **Channels/tiers:** Low-price **DIY expandable 4D kit**, an assembled general-purpose printer, and high-end **industry-specific, custom-scoped/custom-priced printers**. These are design and commercial intents, not costed price commitments or approved market claims.
7. **Materials:** For high-mass/high-throughput fabrication, evaluate deliberate **starter surplus / material reserve**, alternative cartridges and modular refill/replenishment strategies scaled to each model. More material is not automatically better: explicit mass budget, safe storage, depletion alarms, scrap/recovery and provision for high-demand parts are required. Where direct self-printing/assembly is not feasible, a manufactured assembly kit is an acceptable *alternative path*, documented as an assembly kit rather than fully autonomous self-replication.
8. **Redundancy & safety:** Design for contained failure, emergency stop, instrumentation, leak detection, energy isolation and qualified protections where applicable, including fallback and service/recovery procedures. Redundancy to be allocated from hazard analysis and measured reliability, not asserted as universally available.

## Candidate 4D capability-completeness ledger (not an asserted industry-wide definition)
**Terminology:** Conventional "4D printing" generally denotes printed parts that transform function/form over time with defined stimuli. Here the founder also specifies a *broader CGX 4D manufacturing station* with multimaterial function and process-state control. Do not conflate the two; preserve both criteria and define engineering acceptance explicitly.

| Proposed capability target | Minimum documentation for Bootstrap design | Evidence still required |
|---|---|---|
| Stimulus/time-dependent printed response | Stimulus → constitutive state → response → repeatability and recovery contract | Matched measured coupon response and ageing |
| Multi-feed and graded composition | Feedstock passport, mass/energy balance, spatial concentration profile; link to canonical Post-Mix, not a substitute | Characterised feedstock/processing measurements |
| Multimaterial directional interfaces | Explicit X→Y vs Y→X process path and thermal/chemical contamination rules | Bidirectional transition coupons |
| Multi-axis access and internal reposition | Envelope/robot sweep, reachable tool and component staging, pose/datum transforms | Metrology and collision-safe tests |
| Continuous sealed-session integration | No opening/de-sealing main boundary; robotic handling of internal tools/materials and pre-staged inserts | Seal integrity plus complete process readback |
| Environmental controls | Vacuum, positive pressure, independently qualified gases and safe transitions | Rated system design, gas selection, validated interlocks |
| Process conditioning and temporal staging | Cure/solidification/anneal/activation sequencing with cumulative history and incompatibility checks | Process model and measured coupon outcomes |
| Embedded multifunctional components | Structures, conductors, insulation, magnets, sensors, actuators, active electronic and energy-storage pathways (unknowns retained) | Individual component qualification; source-tagged inserted controls |
| Closed-loop sensing and process correction | Temperature, position, chamber state, feed consumption and error correction traces | Calibrated evidence, safety and repeatability |
| Recursive modular self-expansion | BOM/SBOM, expansion sockets, dimensioned fit/interface tolerances, assembly accessibility | Verified seed → fabricated expansion → independently functional upgraded station |

**No shortcut:** A feature may start as a separately testable module or bounded research stub **only if identified as not yet implemented**. Do not record architectural placeholders as operational 4D completeness. Safety-critical environmental controls cannot be substituted by untested mockups for physical operation.

## Build and expansion contracts
- **Seed BOM:** distinguish (A) externally supplied safety-rated or otherwise qualified components, (B) printed or printable components with validated parameters, (C) research-only component candidates and (D) consumables. A complete original seed may need external electronics, gas/vacuum hardware and conventional instrumentation.
- **Expansion ledger:** for each target subassembly, identify needed build volume and tooling, material type and quantity, human vs automated assembly operations, time, waste, orientation, postprocessing and whether the seed can actually fabricate it. Put impossible routes on a formal unresolved list; do not claim self-replication.
- **Material budget:** per build, define \(m_{required}=m_{final}+m_{support}+m_{purge}+m_{scrap}+m_{process\_loss}\), with quantities in kg and evidence-backed uncertainties. Initial stock per feed should cover selected jobs plus a justified reserve where storage and environmental constraints allow. The sufficiency test is by part and feedstock, not generic surplus mass.
- **Scaling:** report useful build envelope in m³ (and axis strokes in m), maximum deposited mass, feedstock compatibility, production rate, energy use, floor space, chamber/pressure ratings, lifecycle/service budget and mission-critical reliability **when data exist**.
- **Class comparator:** Personal/DIY seed; general-purpose assembled; large-capacity/heavy-material; industry-qualified/custom. Each shares the functional 4D requirements, while maximum envelope, throughput, specialty tools, redundant channels, user skills, certifications and service model can vary. Identify which architectures require redesigned rated chambers rather than merely scaled copies.
- **Safety:** chemical/thermal/electrical/pressure hazards, fire, oxygen-displacement and implosion/overpressure are independently engineered, regulated and licensed when required. Colour codes and software cannot replace engineered containment; remote operation and production activation remain held.
- **Marketing evidence:** "fully 4D-capable," "self-printing printer" and "certified for vacuum/pressure/gas" are withheld until individual end-to-end acceptance and regulatory evidence exist.

## Princeception — founder-defined printer family
**Approved direction:** Princeception is the informal name for a printer making a printer, including its supporting printable parts and recursive modules. Full non-software component printability is a research ambition, not a validated current capability. Qualified purchased parts remain permitted during prototyping.

Initial private offerings: **Everyday**, a basic expandable unit, and **Pro**, a fuller-capability unit with a mini-printer inside the primary printer so components can be fabricated concurrently. A larger outer chamber could contain multiple smaller printers; five was illustrative, not a specified unit count.

Classification dimensions are independent: fixed/in-situ or traversing machine movement; chambered, non-chambered or removable process arrangement; terrestrial or specialised environment; personal or tailored scale/application. An enclosed nested print process still follows the single-session rule: do not open the outer boundary during manufacture.

Validate shared staging, coordinate frames, concurrent scheduling, vibration, access and material budgets; no nested machine or self-replication proof is yet claimed.

**Founder-confirmed nested-process architecture (2026-10-08):** Pro and larger printers should be designed with **separately controlled internal process chambers** as well as common-atmosphere printing where compatible. The primary chamber remains sealed during the whole single-session job; independent inner gas controls need segregated supply, sensing, purge, pressure protection and verified isolation before physical use.

- **Supply/part trays:** Reusable and replenishable staging trays may contain sourced chips, gyroscopes, actuators or other complex devices. The printer selects direct fabrication versus sourced placement on comparative performance, energy, time, effort, safety and qualification. Trays can be replaced or repurposed; provenance and supplier test data travel with each component.
- **Printer kinds:** Fixed in-situ deposition units, small independent micro-printers and traversing/roving machines have different scale, reachable area, toolsets and atmospheres. They can coexist in the outer unit; avoid presuming a universal apparatus or one uniform gas space.
- **One concurrent session:** The large printer may fabricate one feature while a local micro-printer produces LEDs or other subcomponents within its own environment, later transferring products through controlled interfaces for integration. Printing a graphene capacitor in the outer volume at the same time is a *candidate scheduling example*, not a proven chemistry, qualified device or safe atmosphere pairing.
- **Coupled integration:** Reserve slots, datum references, pick-and-place reach, feed transfer and process-isolation allowances. Evaluate chemical cross-contamination, heat transfer, pressure/vacuum loads, vibration, motion envelopes, electrical isolation and concurrent power budgets. A semi-permeable wall does not automatically provide gas containment or safe species separation.
- **Evidence:** Compare multi-printer yield/time/cost with a single build head. Keep printed and sourced provenance separately recorded. No actual multi-zone environment, LED print or energy-storage print is claimed.

**Founder correction — individual designs:** A shared physical dock is not compulsory. Each purchased skeleton can be customised by function, appearance and equipment. Actual compatibility is assessed per device and module. Reference design ancestry may inform variants without requiring identical products.

**Approved offline core:** Every printer has its own local CGX device identity, deterministic controller and startup capability handshake. Classical printing requires neither AI assistance nor cloud access. Roving units, nested micro-printers, specialised tools, AI and online services remain selectable. A minimal skeleton may be sold for safe incremental expansion; a fully assembled configuration is also available as a product direction. Safety controls and permitted operating modes remain local and independent of remote services.

**CGX discoverable skeleton — founder direction (2026-10-08):** Each printer and kit starts with a lightweight, discoverable CGX definition of its model/identity, label, capacity, installed functions and desired expansions. It does not require Windows, a heavyweight application OS, network, or AI. Initial provisioning supplies a model-level name and purpose; setup permits optional user renaming, feature and build-path choices. A firmware/embedded-control layer still performs physical machine control and local interlocks; a passive description file cannot replace that runtime.

**Shared information substrate:** Model printers and parts using CGX-linked identities and relationships (parent, child, sibling/variant, assembly membership and upgrades), with versioned links into workspaces, dataspaces and filespaces. The objective is compatibility of *information and reasoning*, not compulsory uniform hardware, appearance, connectors or feature packages. A printer lacking AI, roaming or a specialised module retains a defined upgrade pathway.

**Identity granularity — next founder gate:** Should each manufactured/installed component have a persistent CGX lineage record, with unique unit IDs where practicable and batch/lot identity where individual tracking is unnecessary, without requiring electronics on passive parts? This would support recovery, upgrades, provenance and cross-printer learning.

**Unanswered separately:** Default local ownership/storage versus opt-in cloud synchronisation has not yet been expressly approved; preserve as a separate data-governance question.

## Approved kit details
Use appropriately qualified sourced items where direct printing is not proven, and include necessary protective hardware for supported functions. A per-component startup handshake reports supported capabilities and bounded modes. A guided educational journey is optional; custom variants remain valid when they operate within demonstrated limits. Unverified high-risk modes remain unavailable until qualified.

## Source links
- [2026-10-08 station/enclosure decision](SEALED_STATION_DUAL_TRACK_DECISION_2026-10-08.md)
- [2026-10-08 founder Butter Bot scope](BUTTER_BOT_FOUNDER_DECISIONS_2026-10-08.md)
- [Transit queue](TRANSIT_DECISION_GATE_QUEUE_2026-10-08.json)
