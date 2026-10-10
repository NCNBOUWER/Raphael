# CGX-F4D | Multi-stage route planner and evidence gate
Document ID: CGX-F4D-MULTISTAGE-20261008 | v0.2 | PROPOSED / OWNER REVIEW

## Relationship to existing work
Extends `PAIRWISE_SEQUENCE_ROUTES_v0_1.json` (14 manufacturing families, 196 ordered pair records) without rewriting it, the Raphael Physics catalog, the CGX root, or any deployed capability router. No hardware actions are performed.

## Four distinct checks
1. **Dependencies:** stages form a directed acyclic graph (DAG); the bounded enumerator returns candidate topological orders.
2. **Adjacent transition:** each consecutive material-family change resolves its directional X→Y class P/S/T/M/R from the existing matrix. Managed transition and module routes require an explicitly named strategy. A code does not equate to production authorisation.
3. **Non-adjacent survival:** every stage after a feature's creation accounts for its declared cumulative exposure channels. Missing exposure is UNKNOWN, not zero. Explicitly additive channels only; validated physical models must first convert nonlinear histories to a well-defined damage metric.
4. **Process gates:** dependencies such as enclosure completion and leak integrity testing precede environment refill. Gate assertions in examples are only symbolic planner contracts, not measured evidence receipts.

## Software run and scope
```sh
cd CGX/PrintSpace
python multistage_route_planner.py
python -m unittest -v test_multistage_route_planner.py
```
Input fixtures: `MULTISTAGE_ROUTE_TEST_CASES_v0_2.json`. Outputs: `CANDIDATE_ONLY`, `NEEDS_EVIDENCE`, or `REJECT_CANDIDATE` — none indicate tested physical safety. The `bounded_search_truncated` flag reports possible omitted orders.

## Representation: feature, stage, exposure
- A **feature** has `family`, `created_by` and optional named cumulative `budgets` by exposure channel.
- A **stage** identifies `family` (or null for inspection/atmosphere operations), `after` dependencies, new `creates` IDs, per-feature `exposures`, and required/produced **planning** gates.
- An **exposure channel** has explicit units and aggregation model; this prototype only supports additive accumulation of precomputed nonnegative values. Real thermal, electrochemical, diffusion or stress damage requires qualified non-linear process models and measured records upstream.
- An **environmental transition** such as refill must follow required encapsulation and integrity gate stages; future versions should require actual evidence IDs/hashes before they are considered satisfied, distinguish declared vs completed states, and model measured pressure/oxygen/temperature trajectories.
- A **physical manufacturing licence** and action-authority handshake are deliberately excluded.

## Worked cases
1. `VACUUM_CONDUCTOR_SEAL_REFILL`: candidate route: protected conductor → barrier deposition → symbolic integrity gate → atmosphere refill. Does NOT claim a printed barrier is hermetic.
2. `THERMAL_POSTPROCESS_UNSAFE`: synthetic accumulated damage exceeds budget; route rejected and must be reordered or reengineered.
3. `MISSING_EXPOSURE_REQUIRES_DATA`: missing dose remains UNKNOWN; no inference of safety.
4. `BUTTER_BOT_HYBRID_SEQUENCE`: chassis → traces → insulation → processor insert → power module → test. All values synthetic.

## Handoff for production integration
- Map family aliases to actual feedstock passports and verified machine capabilities; reject unmapped chemistry.
- Replace synthetic additive doses with validated temperature/time/pressure/chemical/field histories, including spatial dose fields and distinct model uncertainties.
- Treat all `produces_gates` as planned until backed by immutable machine/meter/test receipts, calibration and operator authority.
- Resolve non-adjacent interface topology, contamination, staged seal verification, thermomechanical fatigue, unsupported exposed edges, and access for disassembly.
- Add multi-object bed nesting, cell calendars, purge overhead, tool collision, recycling and lifecycle costs only *after* safety feasibility.
- Preserve lineage IDs, separate proposed capability from verified CAN-1, and never promote these fixtures into a machine command queue.

## Directional process examples to instantiate as material-specific records
- MT→TP: hot-process metal, cool, prepare surface, polymer deposition. TP→MT: selective metallisation, reverse order or isolate and mechanically insert.
- TP→CI→DE: chassis cavities, local deposition, electrical isolation and continuity testing.
- CI→DE→EC→DE: insulated conductors, chemistry-specific electrode sequence, protective seal and leak tests; no claimed cell qualification.
- FL→TP→FL: sacrificial fluidic template, enclosure, remove sacrificial core prior to sealing and validate flow.
- CR→OP→TP: fired ceramic, optical deposition or insert, low-energy enclosure.
- TP→BV: complete high-energy processing first, decontaminate by qualified process, isolate biological stage and test viability.
- Earth→microgravity: retain function and schemas, requalify flow/particle capture/cooling under target equipment and gravity conditions.

Status: deterministic **software demonstrator**, not physical, process, safety or release certification.
