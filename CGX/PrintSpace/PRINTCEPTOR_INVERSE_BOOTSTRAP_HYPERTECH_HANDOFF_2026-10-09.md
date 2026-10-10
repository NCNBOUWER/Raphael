# PrintCeptor — backward substitution, Printception and Hyper-Tech CGX interfaces
**Status:** candidate engineering design and bounded provider price observations, 2026-10-09 Australia/Brisbane. **Do not** use this as an order, physical operating licence, robotics acceptance or autonomous hazard-control plan.

## Goal-first inverse engineering
Instead of adding every imaginable printer function to generation 0, decompose the **completed output** into `required function → component/part → process/interface → qualified tool/environment → physical seed requirements`. Retain an **AND** edge for all mandatory subcomponents, and **OR** route choices PRINT, REUSE, BUY, HYBRID, HAND, ASSEMBLE and QUALIFY. Every alternative remains in the source graph even if lower-ranked or unqualified. Log causal reasons, external assumptions and missing physical evidence with DBR when real work commences.

### Reverse targets and source-of-truth
1. **Butter Bot** (first complete integrated print article, not first physical object): shell, tracks/geartrain, neck/cable/pulley, arms/claws, 5 actuator elements, power, MCU/drivers, audio/LED and fitted assembly. `BB-FINAL` requires source geometry/rights plus a qualified uninterrupted sealed assembly and safe in-chamber functional test.
2. **PrintCeptor-0 bootstrap**: mechanically stable skeleton, two planned articulated arms, tool exchange, offline motion/safety control, metrology, feed cavity. Qualification progresses from safe manually assembled seed and noncritical self-printed upgrades, not purchase of an entire universal lab on day one.
3. **PrintCeptor 4D G1 full programme**: required 17 UTP functionality targets and independent graded multi-material, responsive/time-state and controlled-atmosphere acceptance; still unresolved and not commissioned.
4. **Hyper-Tech**: optional add-on that makes an existing device or manual fixture **more observable, individually described or functionally capable only to its verified extent**, without taking over the host's control system.

**Graph implementation:** [Inverse source graph](PRINTCEPTOR_INVERSE_BUILD_GRAPH_v0_1.json) + [deterministic inverse compiler](printceptor_inverse_compiler.py) + [tests](test_printceptor_inverse_compiler_v0_1.py). All outputs `CANDIDATE_ONLY`. The selectable starting tools, actual component dependencies and original negative routes are retained for future owner-scoped CGX/DBR traceability.

## Node-tree examples
`Butter Bot complete` → AND shell, tracks, neck, two arms, motor set, controller/drives, protected electrical power, optional audio/LED and sealed-session assembly.
`Shell` → OR FDM print / hand-pen deposition / buy.
`Tracked mechanism` → OR FDM gear/sprocket + sourced shafts/bearings/track / fully bought component.
`Neck` → OR printed pulley housing + sourced tensile cable/pin/bearing / machined source.
`Motor` → OR sourced new / recovered tested; printing the motor itself is **not** an eligible present route.
`Active control` → OR verified sourced MCU, motor driver and firmware / verified reclaimed compatible board, not printer-manufactured microchip by declaration.
`Power` → sourced protected battery or qualified regulator; no untested DIY printed cell.
`One sealed session` → requires a **physically commissioned** outer enclosure, robotic automatic handling and safe test, and therefore is **not met by pen/FDM/rotary**.

`PrintCeptor skeleton` → AND datum frame, arm cradle, joint/servo/control, automated tool interface, metrology and feed cavity. `PrintCeptor fully controlled 4D` further → tested barriers + primary rated enclosure + qualified gas/vacuum plant + applicable fine and subtractive processes + 17 source G1 test gates.

## Starter substitution and actual cost provenance
| Option | Verified public example prices (AUD) | What becomes candidate-printable | What is still sourced or unknown |
|---|---:|---|---|
| S0 — pen + low-cost rotary + modular kit | Pen 79.95 + rotary 54.98 = **134.93 before optional materials/kit** | Manual noncritical polymer sample, grips, mockups and trials | Automated repeatability, precision, electronics, joint motors, safe enclosure and sealed one-run mechanism |
| S1 — affordable FDM + rotary | Creality Ender-3 V3 SE **259** + rotary **54.98** = **313.98 before filament and all other parts** | More repeatable low-temperature polymer housings, shell segments, brackets, sort-trays, grippers, aligned jigs | Actuator, shafts, certified electric/power, inspection, assembler and chamber |
| S2 — FDM/rotary + MCU/servos/camera | Same two prices; all control/power/sensing **unpriced** | Candidate automated motion fixtures or supervised assembly aids after mechanical/C0 tests | Certified pressure boundary, multi-material qualified process, robust dual-arm precision and self-session proof |
| S3 — full PrintCeptor 0 | No verified total BOM price or possession | Candidate after physical commissioning and expanded process evidence | Full G1 function acceptance and actual end-to-end Butter Bot test remain OPEN |

Observed vendor listings: [Creality official Australia](https://store.creality.com/au/products/ender-3-v3-se-3d-printer), [Jaycar high-temp PLA pen](https://www.jaycar.com.au/high-temp-pla-3d-pen-kit/p/TL4582), [Bunnings rotary tool category](https://www.bunnings.com.au/products/tools/tool-accessories/woodworking-rotary/rotary-tools/corded-rotary-tools). These are **tool snapshots**, not total machine cost estimates, stock guarantees or vendor procurement endorsements. Higher-cost routes remain in the graph; none removed by default.

For each alternative compute separately, as actual inputs become available: `C_total = capital + tools + materials + energy + assembly labour + scrap/rework + maintenance + safety/qualification + amortization`. Unknown terms remain `null`, not zero. Rank Pareto candidates on total cost, independence, lead time, certified margin, performance, reliability, environmental/circular impacts and repeatability **after hard safety/IP constraints**.

## Future process and reversible platform ladder
- S0 learn/repair/print a low-energy grip or kit joint.
- S1 use FDM to produce fixtures/shells/gear drafts, with sourced actuators/control and hand construction.
- S2 print **the tools to build PrintCeptor**, e.g. gripper shells/couplers/feed guides and robot supports; attach rated actuators, measuring instruments and manual-safe electronic controller. Machine may print some of its own parts, but is not yet autonomous or universal.
- S3 commission sealed outer chamber, isolated tool/material handoffs, process safety, anti-collision and deterministic C0; no physically hazardous gas/vacuum commissioning without qualified engineering.
- S4 first complete **Butter Bot** in one sealed session with inserted sourced chips/motors/battery permitted and separately DBR-labelled; verify externally observable function and safe electrical response before breaking seal.
- S5 compare measured physical result to CGX atlas/UTP/PMX model and share **only authorised** data with collaborators, then create refined PrintCeptor A and subsequent state library/university/industrial pilot facilities.
- S6 later prove G1/Printer-μ child reproduction independently; post proof, expand specialist/industrial/in-situ/space manufacturing.

## Hyper-Tech — device modernisation without duplicating the original
[20-device retrofit archetype catalogue](HYPER_TECH_CGX_RETROFIT_FAMILY_v0_1.json) uses four explicit information/physical planes:
- **FileSpace:** Original CAD, firmware and manual references, object instance/type, ports, capability ranges, source and licence.
- **DataSpace:** Sensor evidence, source/revision roots, DBRs, conditions, uncertain/missing readings and selected history; owner-family network rules.
- **PrintSpace:** Printed housing, fixture, jig, tools or mechanical interface plus externally sourced active ICs/motors, verified upgrade and service/rollback evidence.
- **WorkSpace:** Bounded physical zone, responsible human/tech participants, permissions, authorised tasks, operator opt-in, and local fail-safe constraints.

**Not a second CGX root.** Existing `CGX-IR/0.1`, `CGX-UNIVERSAL-OBJECT-EXTENSION/0.1`, `CGX-CROSS-DOMAIN-BRIDGE-REGISTRY/0.1`, `CGX-NODE-EXCHANGE-CONTRACT/0.1`, `CGX-VIEW-SELECTION-POLICY/0.1` and `CGX-TECHNOLOGY-STACK/0.1` remain source/owner controls. One installed item may gain new interfaces without a new root identity. Passive tools are parent-owned children, with independent global type/reference records; a powered self-governed adapter may have its own CGX individual when technically warranted.

### Worked Hyper-Tech routes
- **Regular PC:** Print a USB enclosure/mount, supply authorised compliant USB bridge/dongle where necessary, install an owner-approved signed companion runtime if the host permits, agree to identity/permission handshake; retain host OS/network authority. *USB insertion by itself must NOT expose a PC remotely or obtain privileged access.*
- **Coffee machine:** Prefer vendor-supported network/API; if unavailable, a safe removable external mechanical button actuator + bounded optical/readback sensor can interact with existing control UI under human consent. Do not bypass temperature, pressure, electrical or food-safety protections; no unsupported unsupervised scalding operation.
- **Workshop jig:** Print a fit-for-purpose holder and attach optional QR/NFC tag. It is useful without electronics; an authorised camera/tracker can reveal it to a CGX workbench; tags do not make it aware or autonomous.
- **Wireless charging:** Print the mount around certified compatible receiver/regulation circuitry and verify power/heat/EMC. This is not a universal replacement for existing mains power, battery or an energy source.
- **Room-scale workshop:** Compose commissioned identities, tool holders, material storage, safe cameras, robots and user permissions in a WorkSpace. A single scope graph can coordinate several machines, but consequential actions are still gated by each individual's physical controller.
- **Mobile/wearable:** Print geometry and program source-tagged radio/power interfaces; battery-free and complete functional smartphone are separately measured hard goals, not included as present manufacturing capability.

### Product/service delivery classes
1. **Downloadable CGX recipe/adapter:** Authorised file and source-provenance packet, conditional local manufacture.
2. **Licensed DIY Build Kit:** Printed parts and sourced tested electronics, operator-assembled.
3. **Printed Finished Upgrade:** Generated/certified components with material/geometry/test DBR and installation rules.
4. **Hyper-Tech Retrofit Service:** Qualified onsite assessment and installation for supported nonhazardous systems.
5. **PrintCeptor/child printer network service:** Local library/university/business shared machine time, training, consumed materials, conditional versioned upload permissions.
6. **Industrial/Mark/Luke/eco specialisation:** Owner-controlled application and qualification; source research remains distinct.

A printable kit's useful function does **not** require independent intelligence. CGX names and records its capability, and optional embedded adapters improve sensing/actuation only where a real benefit is demonstrated.

## Public design sharing / LEGO-specific legal risk
Founder's brick-compatible construction prototype is an **in-house generic construction interface**, not automatically licensed LEGO IP nor a public LEGO-compatible commercial SKU. [LEGO Ideas Terms (16 Dec 2025)](https://ideas.lego.com/agree_policies) currently say submitted product ideas **cannot be AI-authored or AI-assisted**, submissions assign extensive rights to LEGO, and independent sale of items derived from ideas submitted there is restricted. **Do not submit this AI-assisted design to LEGO Ideas or imply an approved partnership**. A separately authorised business-to-business licensing discussion or a genuinely independent human-origin proposal is a possible, separately reviewed path; consult EMASSC IP/legal owners first.

Likewise, [djnugent/ButterBot](https://github.com/djnugent/ButterBot) public CAD/README may be inspected as a reference, but public source visibility alone does not confirm commercial/redistribution rights. Preserve independently designed prototype derivations and attribution/specific source agreement, and do not auto-upload models upstream.

## Build pipeline and authority gates
```
Intent / selected CGX family -> reverse goal DAG -> inventory kit/capability handshake
-> qualified source alternatives -> candidate route with missing evidence
-> geometry + PMX + UTP process simulation -> C0 hardware/environmental safety
-> PRINT/BUY/REUSE/HYBRID work order (after owner confirmation)
-> inspected assembled part -> CGX installed part/parent child identity
-> measured function and DBR -> optional CCC/CYC signed release/download
```
Existing owner contracts: `C0` hard realtime safety, `C1` optional local AI, `C2` optional network. Existing CGX node exchange requires sha256/size readback before source removal. Owner/community licence/distribution is not implied by a content receipt. No local machine, pressure vessel, powered robotics or source-authoritative CGX carrier is changed by this document.

## Remaining concrete evidence tasks (same G-gate queue, not a second dispatch authority)
- `G06` **actual inventory**: owned/missing FDM/pen/rotary, measured motors/controller/kit parts, energy/tool/environment ratings, quote list in AUD and equipment condition.
- `G06` **route coupons**: accessible low-load gripper and fixture with force/thermal tests; FDM-to-motor/servo integration, repeatable datum and safe tool exchange.
- `G07` Butter Bot physical CAD rights, exact dimensions, COG/5-actuator budget, wiring, track materials, geometrical decomposition, one-sealed-session tool reach and internal safe preopening function tests.
- `G02/G14` bind 28 inverse component nodes and 20 Hyper-Tech patterns to CGX atlas part types and source owner's object IDs, retaining exact version and original source authority.
- `G06/G15` Hyper-Tech PC dongle signing/host consent, appliance OEM API/physical button risk, safe WorkSpace zone rules, network permissions and DBR receipt exchange.
- `G15` EMASSC + CCC/CYC publication licence and external LEGO/ButterBot permissions, no automatic third-party distribution.
- `G15` partner ROI/service model for accessible local printers in public libraries/universities/industry before general commercial launch.

**Physical status:** every planned route candidate; no pre-existing actual paid purchase, printer build, calibrated motion, Butter Bot closed print or commercial rights is demonstrated.
