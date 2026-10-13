# CGX-F4D | PrintSpace Capability-First Interface Doctrine
Document ID: CGX-F4D-CAP-20261008
Version: 0.1 | Date: 2026-10-08 | Status: PROPOSED / OWNER REVIEW
Scope: conceptual manufacturing ontology and crosswalk for CGX PrintSpace, Raphael, Filespace, Dataspace and LightSpeed. Not a validated printer, recipe or deployed adapter.
Non-overwrite rule: Raphael_Physics, N^3, EML#F and existing LightSpeed capability registry remain distinct and authoritative in their respective lanes.

## Directive
1. Evaluate a dissimilar material, atmosphere, field, geometry or process transition **first as an exploitable candidate interaction**, not merely an incompatibility.
2. Return CAN[function] IF[environment + materials + geometry + process sequence + equipment + safety + measurement + authority]. Record capability maturity independently of interface discovery.
3. Failed process route does not invalidate the desired function; re-route through isolation, sequencing, graded transitions, inserted components or an alternative material while preserving observations.
4. Keep scientific conservation laws, credible hazards, actual machine limitations and verified test conditions explicit. Capability-first does not mean unqualified success claims.
5. Preserve identities, lineage, owner gates, observations and receipts. Do not silently migrate or override the existing LightSpeed routing states.

## Definitions and functional vocabulary
| Term | Meaning and function |
| --- | --- |
| 2D / 3D / CGX-4D | CGX shorthand: planar pattern / volumetric structure / volumetric integrated function. The pre-existing academic meaning of 4D printing includes stimulus/time-responsive materials; do not conflate. |
| PrintSpace | Physical fabrication plane: cells, chambers, recipes, transformations, inspections and production receipts. |
| Filespace | Versioned source CAD, recipes, evidence files, firmware and hashes. |
| Dataspace | Typed and provenanced material properties, physical claims, relations, operating windows, units, uncertainties and capability state. |
| Functional contract | Required task, input/output, payload, operating envelope, lifecycle and acceptance tests for a manufactured object. |
| Dissimilar interface | Region where mechanical, chemical, optical, electrical, magnetic or thermal properties differ. |
| Interface leverage | Intentional use of such differences for adhesion, modulation, conversion, protection, sensing, actuation or separation. |
| FGM/graded interface | Spatially variable composition, phase, microstructure or stiffness replacing an abrupt boundary. |
| Process window | Measurable parameter region where a process can yield a specified acceptable feature. |
| Functional window | Conditions in which the finished feature meets its required behaviour and tolerance. |
| Opportunity window | Conditions and time period in which a resource, field or environmental state provides a useful function or production advantage. |
| Environment profile | Pressure, oxygen partial pressure, humidity, temperature, gravity vector, acceleration, chemical environment, fields, radiation and contamination profile with measurements. |
| Vacuum | Reduced gas pressure, not zero reactants; recipe-specific pressure/contamination criterion required. |
| Inert atmosphere | Controlled low-reactivity environment qualified for the chosen material and temperature. |
| Oxidation | Electron-transfer chemistry, potentially avoided for conductor preservation or induced deliberately to form functional layers. |
| Hermetic seal | Enclosure demonstrated to meet gas/fluid leak and lifetime acceptance targets; a closed printed shape alone is not a verified seal. |
| Process cell | Isolated/managed fabrication zone with qualified tool, atmosphere, feedstock and sensing capacity. |
| Process transition | Purge, cure, sinter, cool, shield, encapsulate, transfer, magnetise or test between operations. |
| Selective activation | Localised temperature, electric/magnetic field, illumination or chemical treatment to transform only selected regions. |
| Feedstock passport | Source, composition, hazards, storage, preparation, uncertainty and lot identity. |
| Variable-feedstock synthesis | Metered combination of qualified material streams under mass/species balance, followed by kinetics and microstructure qualification. |
| Interface passport | Neighbouring material identities, spatial relation, intended interaction, process windows, failure modes and measured result. |
| Process passport | Actual machine, operator, calibration, environment traces, recipe, transitions, metrology and disposition. |
| Functional void | Internal volume allocated to structural, energy, cooling, optical, acoustic, service, movement, recovery or reserve purpose. |
| Spare print area | Unoccupied compatible build envelope, distinct from internal void and idle machine capacity. |
| Redundancy | Independent alternative functionality quantified for common-mode dependencies and lifetime. |
| Metrology | Traceable dimensional, mechanical, electrical, chemical, thermal and environmental measurement with uncertainty. |
| Coupon | Representative small sample qualifying an interface/process before scaling to a complete system. |
| Receipt | Timestamped immutable action/evidence record with actor, source hash, parameters, outcome and references. |
| Handshake | Typed interface through which one CGX lane declares actual capability, conditions, authority, limits, observations and next action to another. |

## Physical and optimisation relations (SI units)
- Conditional predicate: CAN(F | E,M,G,P,S,Q,A). F function; E environment; M material; G geometry; P process sequence; S machine/system; Q physical qualification; A action authority.
- Candidate route exists if a route r satisfies all physical, safety and resource predicates C_i(r)<=0. Label verified CAN-1 only after required physical acceptance tests V_j(r)=pass.
- Spatial composition c_k(x,y,z,t) must be nonnegative and sum to 1 across species fractions at every material point. A spatial gradient may be intentionally functional.
- Feedstock mass: m_out=sum(m_in)+m_generated-m_consumed, accounting for reaction and waste rather than treating output properties as linear averages.
- Idealised examples needing correct regimes and constitutive laws: heat flux q=-k grad(T); Fick diffusion J=-D grad(c); locally Ohmic current j=sigma E. Use coupled thermal/electromagnetic/chemical/structural equations and boundary conditions as applicable.
- Intentional contrast: output=f(delta temperature, delta chemical potential, delta voltage, strain, magnetic flux, geometry, process time). Each delta is a candidate mechanism, not an automatic benefit.
- Battery usable energy E=integral[V(t) I(t) dt] over the qualified discharge profile; allocate voids only after structural, environmental and safety needs.
- Marginal production objective: minimize weighted time + financial cost + consumed energy + waste + risk + assembly, subject to mandatory quality and containment requirements. Weights and units must be declared; never score safety as a tradable preference.
- Energy harvesting: measured useful output must not exceed physically available input after accounting for conversion losses. No net energy claim from geometric pattern alone.

## Capability maturity, separate from LightSpeed tool route availability
CAN-1 Demonstrated: specified function physically passed tests under stated environment and duration.
CAN-2 Engineered: known equipment/process + engineering design, but integrated test incomplete.
CAN-3 Conditional: executable route requires atmosphere, equipment, material, integration or safety provisions.
CAN-4 Investigational: scientific mechanism/hypothesis exists; method or performance unverified.
CAN-5 Alternative Route: this specific route failed; preserve target, failure evidence and propose bounded alternatives.
DO NOT replace the existing LightSpeed tool states available/workflow/gated/assisted/registered_unwrapped/missing. A tool can be available while a physical manufacturing ability remains CAN-4.

## Interface x environmental capability atlas
| Interaction | CAN output / mechanism | Executable conditions | Evidence gate |
| --- | --- | --- | --- |
| Oxygen-reactive conductor | High retained conductivity | Vacuum or qualified inert gas deposit -> temperature-compatible process -> complete encapsulation and seals before atmospheric re-exposure | O2 trace, electrical, material-state, leak and service cycling |
| Intentional oxidation | Dielectric, passivation, chemical sensor | Spatially controlled oxidation with target chemistry and thickness | XPS/other chemistry, thickness, breakdown, ageing |
| Metal + polymer | Flexible wiring, shielding, joined chassis | Local low-T deposition/sinter or hybrid placement and encapsulation | Four-wire resistance, isolation, peel, cyclic bending |
| Metal + metal | Gradient hardness, thermal path, electrical junction | Controlled feed/phase history, interface heat input and graded transition | Grain/phase profile, fatigue, corrosion |
| Different thermal expansion | Actuation, controlled curvature/preload | Layer architecture, thermal schedule and service temperature | Shape response, stress, hysteresis |
| Compressive/tensile residual stress | Prestress, shape programming | Tune deposition direction and cure/cool history | Stress and displacement cycling |
| Conductor + dielectric | Capacitor, antenna, sensor, insulated buses | Deposited layers, spacing, RF and voltage design | Capacitance, leakage, ESR, impedance, dielectric breakdown |
| Electrochemical potential | Plating, sensor, rechargeable function | Electrodes/electrolyte/containment, current and contamination control | Capacity, reaction products, cycles, protection |
| Magnetic/nonmagnetic | Inductor, motor, magnetic switch | Coils, aligned particles, qualified magnetisation and mechanical gaps | Field mapping, force, losses |
| Optical contrast | Waveguide, filtering, imaging paths | Transparency, geometry, wavelength-specific curing and clean surfaces | Spectrum, scattering, alignment |
| Surface roughness | Mechanical interlock, adhesion or release | Engineered contact texture/chemistry | Shear, friction, wear |
| Acoustic impedance | Damping/resonator | Modulated density, geometry and stiffness | Spectrum, damping loss |
| Temperature gradient | Thermal switching, thermoelectric harvesting | Sustained heat source and heat sink | Gradient, watts, efficiency |
| Light field | Photovoltaic/photochemical transformation | Spectral match and qualified absorber | Irradiance, I-V, photostability |
| RF field | Communication and limited energy harvesting | Antenna tune and real available external field | Spectrum, DC output and duty cycle |
| Mechanical vibration | Strain sensing / limited harvesting | Coupled resonant geometry | Power, frequency curve, fatigue |
| Humidity | Hydrogels, humidity sensors | Controlled water activity and protective assembly | Swelling, hysteresis, service cycles |
| Earth gravity | Gravity-assisted deposition, infiltration, drainage | Qualified orientation, acceleration and fluid regime | Flow, dimensional accuracy, pores |
| Microgravity | Different scaffold, deposition, capillary and on-demand assembly regime | Closed material containment and microgravity-qualified transport | Droplet/debris control, reproducibility |
| Vacuum/pressure | Degassing, select reactive-surface protection | Material-specific deposition and chamber configuration | Pressure and gas traces, chemistry |
| Radiation | Shielding, sensing, material response | Qualified exposure and material prescription | Measured dose attenuation/degradation |

## Worked route: protected oxygen-sensitive feature
Goal: print an oxygen-sensitive electronic or metallic feature that survives exposure to air.
1. Define desired electrical/chemical performance and exposure lifetime.
2. Determine material-specific oxygen/humidity/temperature sensitivity empirically.
3. Select verified vacuum or inert-gas atmosphere; measure residual partial pressures, outgassing and substrate state.
4. Print and post-process in the protected environment, confirming deposition tool suitability there.
5. Complete a validated barrier/seal over all functional surfaces and penetrations before returning chamber to ambient atmosphere.
6. Verify seal leak rate/permeation, then atmospheric, pressure, thermal and humidity cycling.
7. Measure conductivity, surface chemistry and task function.
8. If a method fails, retain function and test alternatives: a deposited multilayer barrier, independent sealed insert, protective chemistry, another atmosphere or another chamber.
Airtight CAD geometry is not equivalent to a hermetic physical part; chamber oxygen suppression alone does not guarantee permanent protection.

## Earth and in-situ microgravity: parallel CAN routes
- Earth: gravity aids flow, settling, loading and orientation-controlled production; gravity's influence is included in the calibrated manufacturing envelope.
- Orbit: microgravity enables alternative low-sag and material-arrangement regimes and on-demand assembly; the process must positively provide containment, feed and thermal handling. These are two branches of one functional contract, not two negative constraints.
- Space station, terrestrial factory, home, and micro/nano cells share typed passports and acceptance terminology, not necessarily the same machine.

## Handoff rules and execution sequence
Functional request -> functional contract -> interface discovery -> compatible route enumeration -> Raphael/conventional comparative physics -> equipment/environment match -> sequence protected transitions -> manufacture -> metrology -> evidence grade -> recorded CAN state -> owner gate -> CGX receipt.
Prioritise existing proven tools, then safe sequencing and isolation, then hybrid integration, then novel coupons and microstructure studies. Prefer process-specific adaptive cells over claims of one universal simultaneous environment.
For batch scheduling distinguish bed nesting, useful internal geometry, and temporal machine utilisation; each needs noninterference and net-benefit tests.

## Minimum handoff object
Required IDs/fields: contract_id, function, desired_output, target_units, route_id, interface_id, environment_profile_id, chamber_cell_id, feedstock_ids, geometry_hash, process_recipe_id, process_transition_ids, acceptance_test_ids, observations, uncertainty, CAN_state, existing_runtime_tool_state, safety_gate, action_authority, evidence_uris, timestamps, reviewer, disposition, next_route.

## Benchmarks and proof queue
PS-001: inspect current CGX capability registry and map onto existing keys; do not rewrite it.
PS-002: conductor/dielectric coupon, with resistance, isolation and interface adhesion.
PS-003: protected-metal coupon with atmosphere and verified leak test.
PS-004: graded-compliance interface coupon with fatigue and stress measurement.
PS-005: BB01 hybrid Butter Bot functional contract and qualified insert mapping.
PS-006: PrintSpace process scheduler only after measured machine/material availability.
PS-007: dual 1g/microgravity route equivalence and divergence review.
PS-008: independent review of Raphael solver assumptions, units and falsification tests.
Unresolved are work items, not blanket impossibility labels.

## Sources and qualification boundaries
- ISO/ASTM 52920:2023 qualification principles (industrial AM): https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/07/69/76911.html
- ISO/ASTM 52953:2025 monitoring-data registration, currently scoped to metal PBF-LB: https://www.iso.org/standard/84117.html
- Metal/polymer heterogeneous interfaces and methods (2025): https://www.nature.com/articles/s44334-025-00045-w
- Functionally graded interface structures and mechanical consequences (2025): https://www.sciencedirect.com/science/article/pii/S0921509325010457
- ISS National Lab Additive Manufacturing Facility: https://issnationallab.org/facilities/additive-manufacturing-facility/
- NASA microgravity bioprinting: https://www.nasa.gov/missions/station/iss-research/3d-bioprinting/

## Change log
2026-10-08: Owner-directed capability-first ontology, oxidisation control via protected print and pre-refill encapsulation, gravity-route parity, physical evidence gates, executable process alternatives. Doc-only proposed specification; no printer tests, no deployed CGX adapter, no alteration to existing external lanes.
