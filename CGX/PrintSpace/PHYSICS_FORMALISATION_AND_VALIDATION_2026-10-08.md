# CGX-F4D | Quantitative Physics and Capability Formalisation
Document ID: CGX-F4D-PHYSICS-20261008 | Version: 0.4 | Status: PROPOSED / OWNER REVIEW
Scope: SI-dimensional analytical screening, process regime classification and traceable links to the pre-existing Universal Tech Printer physics kernels. These files do NOT assert installed physical printing capability.

## 1. Canonical authorities and non-overwrite rule
- UTP physics owner: `NCNBOUWER/Raphael` PR #5, `UTP-KERNELS-001`, `UTP-HYPERGRAPH-001`, `UTP-CATALOGUE-001`, `UTP-ENV-001`.
- PrintSpace PR #6 owns only the candidate computation layer (dimensioned formulae + prototype crosswalk + test cases).
- Post-Mix PMX owner: `achillesromer-coder/Data` PR #11 `PMX-MAT-001`. Formula PS-EQ-035 is nonreactive mass accounting only and **does not** replace reaction kinetics or the PMX solver.
- Existing N^3, EML#F, Raphael_Physics_Classic, Raphael Lite, promoted `.cgx` carriers and LightSpeed source remain distinct.
- Never label a candidate equation result as a qualified component. Software CI asserts mathematical/unit consistency, not physical predictive accuracy.

## 2. Three model levels
**Level A — Analytic identity or approximation (implemented):** 59 separately dimensioned, read-only scalar relations in `PHYSICAL_EQUATION_CATALOGUE_v0_4.json`. Evaluated by `dimensioned_equation_engine.py` with explicit SI inputs, a restricted expression grammar, domain guards and named assumptions.
**Level B — Coupled physical continuum/device model (external UTP authority):** Maxwell and charge continuity; fluid momentum/mass/energy, species and reaction transport; Nernst–Planck/Butler–Volmer electrochemistry; phase fields; solid deformation; semiconductor carrier equations; optical/plasma radiation.
**Level C — Instrument and product validation (future evidence):** material/geometry-specific parameter calibration, test coupon results, measurement uncertainty, multi-stage survival, end-of-life and owner-authorised machine profile. An analytic result does not establish Level C.

## 3. Physical state and conservation framework
State vector per spatial region and process history may include composition, phase, deformation, charge, pressure, temperature, velocity, gas content, exposure and geometry:
`s(x,t) = [c_k, eta_k, u, p, T, phi, E, B, sigma, epsilon, g, ...]`.
- Mass: `partial_t(rho) + div(rho*v) = S_m`, where S_m must have a verified material source or sink.
- Species: `partial_t(c_k) + div(c_k*v + J_k) = R_k`; Fick/Nernst–Planck requires region-appropriate material laws.
- Charge: `partial_t(rho_q) + div(J) = 0`; no source-free perpetual charging claims.
- Energy: resolved net heat, electrical work, mechanical work, chemical energy and radiative terms must balance at selected control-volume boundaries.
- Momentum: `partial_t(rho*v) + div(rho*v⊗v) = div(sigma) + rho*g + f_EM + ...`; moving solids and fluids use domain-appropriate constitutive laws.
- Interfaces impose flux and traction continuity or specified jumps, reaction rates, transport barriers, insulation, optical coupling or adhesion; all depend on actual topology.
- The CGX capability-first doctrine treats environmental and interfacial differences as candidate functions, **not** as automatically beneficial or physically unconstrained.

## 4. Transition calculus
For materials or functions X and Y, and a route `r`:
`CAN_IF(X→Y,r) := route_exists AND valid_environment(r) AND validated_prior_survival(r) AND required_observations_present(r) AND operator_authority(r)`.
The family P/S/T/M/R classification is a search hint; route selection must be material/lot/machine/geometry-specific.
- P: direct shared-window co-process candidate.
- S: sequential with validated prior-layer survival.
- T: environment, chemistry, process, interlayer or chamber transition.
- M: separated/inserted qualified module.
- R: investigative route, not physically authorised.
When `W_X ∩ W_Y = empty` for direct co-processing, CGX searches *temporally sequential* windows `W_X at t1` and `W_Y at t2`, protective encapsulation, bonded graded interfaces or modular paths. An empty simultaneous process-window intersection is **not** proof of functional impossibility.
Cumulative material survival is non-local in the stage graph: evaluate damage and uncertainty for each feature after every later process step, not merely at adjacent interfaces.

## 5. Scale, environment, gravity and nondimensional similarities
12 additions to the screening catalogue extend the original 47 relations to 59. They calculate Pe, Ca, We, Fo, Bi, Kn, Da, magnetic Reynolds, Hartmann, Debye/geometric ratio, thermal diffusivity and electromagnetic skin depth.
- `Bo = Δρ g L²/γ` compares body forces with surface tension. On Earth `g` is site-specific; orbital microgravity uses measured residual acceleration, *not* a universal exact zero.
- `Ca = μU/γ`, `We = ρU²L/γ`, `Pe = UL/D`, `Kn = λ_mfp/L` identify fluid and gas regimes. At molecular scales, continuum assumptions can cease to hold; promote to an appropriate model rather than extrapolate blindly.
- `Bi = hL/k` and `Fo = αt/L²` help assess whether lumped or distributed transient heating is appropriate.
- `Rm` and `Ha` inform magnetic-fluid coupling, not printable motor torque directly.
- `PS-EQ-046` capillary length diverges in the zero-g idealisation; zero-g is rejected *for that formula*, while alternate capillarity models remain available.

## 6. Worked illustrative engineering calculations (NOT device ratings)
1. Copper-like reference trace (illustrative resistivity `1.7e-8 Ohm*m`), length `1 m`, section `1e-6 m²`: `R=0.017 Ohm`; at `2 A`, `P=0.068 W`. Values are numerical fixtures, NOT a claim about particular printed inks or measured copper stock.
2. Dielectric parallel plate: `eps_r=2`, `A=0.01 m²`, `d=0.001 m`: `C≈1.77e-10 F` when the ideal plate assumption holds, not a realistic routed PCB without fringing.
3. Gravity-capillary example: `Δρ=1000 kg/m³`, `g=9.81 m/s²`, `L=1 mm`, `γ=0.072 N/m`: `Bo≈0.13625`, indicating capillarity should not be neglected. This does not itself establish a qualified orbital print process.
4. Ideal nonreacting mix: `2 kg at 10% species A` and `1 kg at 40%` yields `20% mass fraction` if no reaction, phase partition or loss.
5. Protective chamber: ideal gas pV/nRT may bound internal gas state; molar permeation `Ndot=P*A*Δp/L` estimates only a validated homogeneous solution-diffusion route and does not certify hermetic sealing or ageing.
6. Thermal mismatch: `abs(alpha_A - alpha_B)*ΔT*L` predicts a **free** differential expansion, not the bonded residual stress field.

## 7. Equation-to-production data dependency
A material property slot must record SI units, actual numerical value, uncertainty, temperature/pressure/strain/frequency/chemistry regime, exact feedstock lot and specimen identity, method, equipment calibration, instrument ID, source ID, date, and measurement authority.
A feature must record geometry/surface topology, tolerances, applied service loads, service environment and stress/corrosion/fatigue histories.
The calculation must emit model ID, equation version, operands with unit+provenance, output, validity checks, estimated uncertainty, alternate model candidates and test receipt links.
The v0.4 engine intentionally **does not** infer material properties from the 531 empty measurement slots.

## 8. Known incomplete subsystems — route rather than falsely certify
- Semiconductor logic and transistor fabrication: K-SEMI full bands/carrier transport/defects required; PS-EQ-001/004 alone do not model active digital logic.
- Lithium battery: K-NP and K-BV with separators, kinetics and thermal runaway safety; PS-EQ-026 only screened electrical energy.
- Complete magnetic motors: field saturation, winding heating, eddy current, mechanical load, control and tolerance; long-solenoid closed form is not a motor solver.
- Hermetic systems: actual seal interface leak/permeation and lifetime cycling measurements required.
- Living bioinks: material-specific sterile controls, viability, waste isolation and regulatory safeguards.
- RF harvesting: Friis is an ideal far-field link estimate, NOT proof of useful ambient energy or unrestricted spectral operation.
- Nano/micro manufacturing: feature scale and Kn/Da/Pe regimes determine when continuum scalings must be replaced by specialised micro/nanoscale fabrication models.
- Radiation shielding and plasma: dedicated transport kernels remain necessary.
- Multi-material post-mix: PS-EQ-035/036 assumes nonreactive mixing and additive volumes; apply PMX chemistry-specific nonlinear physical validation separately.

## 9. Evidence and qualification lanes
1. SI/parser validation + synthetic benchmarks + negative tests by GitHub Actions.
2. Source-specific material-property population (no interpolated or invented lot data).
3. Device regime selection + uncertainty budget; distinguish epistemic gaps from known variability.
4. Coupons: X→Y and Y→X, plus X→Y→Z nonadjacent thermal/chemical/field exposure.
5. Controlled PrintSpace machine-specific execution/acceptance in isolated equipment after owner review; compare actual sensor traces to predicted bounds.
6. Versioned corpus and lifecycle evidence via existing CGX identity and DBR process; no mutation of promoted S92 carriers without audited promotion.

## References (method and constants, not generic process recipe endorsements)
- NIST/CODATA: https://www.nist.gov/publications/codata-recommended-values-fundamental-physical-constants-2022
- NIST AM metadata acquisition: https://www.nist.gov/publications/additive-manufacturing-data-and-metadata-acquisition-general-practice
- NIST AM dataset registration + uncertainty: https://www.nist.gov/publications/fully-registered-situ-and-ex-situ-dataset-metal-powder-fusion-additive
- NIST AM-Bench: https://www.nist.gov/programs-projects/metrology-am-model-validation

All formula results and datasets are **non-actuating** candidate analyses. `production_approved=false` is required across v0.4.
