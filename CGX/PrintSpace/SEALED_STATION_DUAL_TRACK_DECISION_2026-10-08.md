# PrintSpace sealed-station + motion testbed — founder decision and engineering handoff
**Date / zone:** 2026-10-08, Australia/Brisbane  
**Status:** Founder-approved *parallel research tracks*; layered-envelope concept and vibration targets require detailed modelling and validation. **No physical construction, pressurisation, vacuum, heater, actuator or production release permission granted.**  
**Authority:** PrintSpace PR #6 review lane, referencing the existing Raphael UTP and Post-Mix owners without merging or changing their models.

## Binding scope from transit conversation
- Founder rejected treating **A: sealed multi-process printing station** and **B: minimal motion/kinematics testbed** as exclusive priorities. **Develop both concurrently and hybridise their results into the actual printing station.** The motion testbed is the instrumented precursor/rig for the intended printer, *not* a detached competing product.
- **Continuously sealed session definition** retained: all material and part changes, internal compartment builds, pick/place, rotations and robot/tool operations occur without opening or de-sealing the main controlled enclosure. Pre-staged chips and other sourced components may be retrieved internally; external *digital* commands/telemetry do not break the session, provided the communication penetration maintains environmental integrity.
- Founder suggested a **secondary internal region/layer**, analogous to multi-pane aircraft windows, to manage enclosure/environment fluctuations. Treat as a **design candidate** for a layered pressure/thermal/acoustic/mechanical architecture, not a proven aviation-style recipe or a decision to build an unsafe pressure vessel. The outer airtight boundary and any independent inner process containment must have separately justified functions.
- Founder raised the need to reduce **motion-induced vibration**, dynamic disturbances and their effect on deposition accuracy, sealing, alignment, process interfaces, tooling and camera/metrology. Specific target amplitude/frequency and source mechanisms are not yet known or agreed.

## Parallel design lanes, shared reference frame
### Track A — sealed multi-process station
Conceptual subsystems: outer continuous environmental boundary and door interlocks; designed digital/power/feedthroughs; pre-staged internal shelves/material cartridges; robotic transfer/tool-changer; independently defined inner process zone(s) for hazardous/controlled operations if later permitted; contamination segregation; thermal management; cameras and sensors; accessible recovery only *after* session termination. No opening the main enclosure for reorientation or tooling mid-run.
**Boundary rule:** a window-like double layer alone is not proof of a pressure/vacuum-rated chamber. Cavity pressure, leak paths, differential expansion and failure propagation need explicit analysis and professional sign-off if relevant.

### Track B — motion, reaction-force and alignment testbed
Instrument the same intended machine topology: motion stages, robotic grasp/repositioning, tool access, balanced/isolated reaction paths and flexible service routing. Use low-energy dry-run models and safe instrumented rigs before any deposition or sealed-atmosphere operation.
Record: stage velocity/acceleration/jerk, motor and tooling excitation spectra, displacement vs datum, angular errors, settling time, tool centre-point repeatability, stage/platform natural frequencies, transmissibility, contact/grasp forces and impact/collision states. Use SI units and calibrated sensors for future empirical results; no measurements claimed today.

### Coupled A↔B questions to resolve in CAD/analysis
1. **Load paths:** can an isolation frame support motion actuators without transferring large reaction forces into the precision deposition datum or seals?
2. **Seal versus freedom:** isolate the inner working platform while preserving flexible hoses/cables, gas feedthroughs, door interfaces and hermetic integrity without over-constraining motion.
3. **Cavity coupling:** any dual-pane/double-wall or floating inner enclosure must be tested for its own acoustic and mechanical resonances; an air gap does not inherently suppress all vibration.
4. **Thermal coupling:** model process temperature gradients, expansion mismatch, condensation and material cross-contamination and their effect on positioning and seal lifetime.
5. **Robotic staging:** ensure all tools and purchased-module racks are reachable inside the uninterrupted sealed build; anticipate changing product scale without bespoke Butter Bot-only transfer rails.
6. **Digital supervision:** external electrical/optical communications and software commands allowed across validated boundary penetrations; no assumption of remote permission to actuate hardware.

## Dependency-directed simulation and proof queue
- Define bounding-box envelopes, masses, maximum internal payloads and motion stroke ranges from the actual Butter Bot and broader product families; identify missing values explicitly instead of inventing them.
- Produce CAD interface skeleton: common datum, frame, base, inner zone candidate, actuators, material racks, sensor placements and feedthrough allowances. Parallel kinematic/dynamic free-body and thermal/seal models. Preserve component provenance and process staging by G07.
- Run preliminary modal/reaction-force and source-to-target vibration analyses across motion profiles: step/acceleration, tool change, pick/place and deposition. Include worst-case settling at a defined metrology datum; do not claim tolerances before evidence.
- Investigate enclosure-level pressure/temperature/gas environment as a **founder gate** before selecting inner/outer load bearing shell specifications. High vacuum, pressurised reactive atmospheres and sealed battery formation are not presumed within scope of a benign first rig.
- Qualify tests in order: simulator -> unenergised envelope mock-up -> low-energy dry kinematics -> monitored sealed ambient commissioning (separate owner/safety approval) -> specialised environmental modules only after professional design, facility and operating gates.
- Explicitly separate software/model tests and source-level feasibility from measured print precision, leak rates and actual pressure-vessel compliance.

## Next founder decision requested (OPEN)
**Initial operating-envelope authority:** Should the first station be specified for **sealed, near-ambient-pressure, nonreactive operation**, while allowing future **independently qualified vacuum/controlled-atmosphere modules**; or must an independently engineered vacuum/controlled-pressure inner chamber be a first-generation core requirement?
**Recommendation:** First option. It lets sealed integration, kinematics and vibration isolation progress without unearned pressure-system qualifications and without foreclosing later capable modules.

## Source references
- [Founder BB programme and sealed session definition](BUTTER_BOT_FOUNDER_DECISIONS_2026-10-08.md)
- [Transit decision queue](TRANSIT_DECISION_GATE_QUEUE_2026-10-08.json)
- [In-transit handoff](IN_TRANSIT_CONTINUATION_HANDOFF_2026-10-08.md)

**External engineering context (analogy only):** NASA's spacecraft window technical and standards materials distinguish multiple pane functions, structural pressure barriers, vent/purge loads and verification. Source: https://www.nasa.gov/podcasts/small-steps-giant-leaps/small-steps-giant-leaps-episode-59-spacecraft-window-design/ ; https://standards.nasa.gov/standard/NASA/NASA-STD-5018 . The same structural qualification is **not** asserted for PrintSpace.
