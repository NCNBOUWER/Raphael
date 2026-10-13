"""PrintSpace temporal geometric preview from owner-seeded parametric primitives.

This is an R2/R3 schematic sequence for offline CGX review, not a physical
kinematic, thermo-chemical or semiconductor simulation. Phase index != seconds.
The existing Raphael directional-material planner remains process authority.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = HERE / "FUNCTIONAL_TIME_PREVIEW_SEEDS_v0_1.json"
SCHEMA = "cgx.printspace.functional_time_preview_compiled.v0.1"
PRIMITIVES = frozenset(("box", "cylinder", "link"))
STAGE_TYPES = frozenset((
    "FDM_DEPOSITION", "SOURCED_COMPONENT_PLACEMENT",
    "UV_CURE_CANDIDATE", "IN_PROCESS_UV_PATTERN_CANDIDATE",
    "MASKED_PHOTOLITHOGRAPHY_CANDIDATE", "LASER_DIRECT_WRITE_CANDIDATE",
    "INSPECT_AND_FUNCTIONAL_SIM",
))


def source_sha(path=SEEDS):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _finite_number(value, *, positive=False):
    if type(value) not in (float, int) or not math.isfinite(value):
        raise ValueError("dimension/coordinate must be finite numerical value")
    if abs(value) > 100000:
        raise ValueError("unbounded millimetre geometry")
    if positive and value <= 0:
        raise ValueError("size requires positive millimetres")
    return float(value)


def _sorted_stages(stages):
    """Deterministic dependency order, not an estimated deposition time."""
    ids = [s["id"] for s in stages]
    if len(ids) != len(set(ids)) or not ids or len(ids) > 128:
        raise ValueError("stage IDs must be unique, bounded and nonempty")
    index = {s["id"]: s for s in stages}
    for stage in stages:
        deps = stage.get("depends_on")
        if not isinstance(deps, list) or len(deps) != len(set(deps)):
            raise ValueError("stage dependency graph malformed")
        if set(deps) - set(index) or stage["id"] in deps:
            raise ValueError("stage dependency references unknown or self")
    output, complete = [], set()
    while len(output) < len(stages):
        ready = [s for s in stages
                 if s["id"] not in complete and set(s["depends_on"]) <= complete]
        if not ready:
            raise ValueError("stage dependency cycle")
        selected = ready[0]
        output.append(selected)
        complete.add(selected["id"])
    return output


def validate_seed(source):
    if source.get("schema") != "cgx.printspace.functional_time_preview_seeds.v0.1":
        raise ValueError("unregistered PrintSpace preview schema")
    if source.get("hardware_control_enabled") is not False:
        raise ValueError("simulation cannot authorize hardware")
    contracts = source.get("process_contracts", {})
    if set(contracts) != STAGE_TYPES:
        raise ValueError("missing or unknown process capability type")
    if any(c.get("can_run_physically") is not False for c in contracts.values()):
        raise ValueError("physical capability must remain unqualified")
    variants = source.get("product_variants", [])
    if not 1 <= len(variants) <= 16:
        raise ValueError("product variants not bounded")
    ids = [v["id"] for v in variants]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate variant identity")
    for v in variants:
        if v.get("aesthetic", {}).get("gendered") is not False:
            raise ValueError("watch/finish is design choice, not gender")
        envelope = v["design_envelope_mm"]
        if len(envelope) != 3 or any(_finite_number(n, positive=True) <= 0 for n in envelope):
            raise ValueError("invalid geometry envelope")
        parts = v.get("parts", [])
        if not 1 <= len(parts) <= 64 or len(set(p["id"] for p in parts)) != len(parts):
            raise ValueError("invalid or duplicate parts")
        stages = _sorted_stages(v.get("stages", []))
        stage_ids = {s["id"] for s in stages}
        part_ids = {p["id"] for p in parts}
        referenced = set()
        for p in parts:
            if p.get("primitive") not in PRIMITIVES or p.get("stage") not in stage_ids:
                raise ValueError("unregistered primitive or part stage")
            center, size = p.get("center_mm"), p.get("size_mm")
            if not isinstance(center, list) or not isinstance(size, list) or len(center) != 3 or len(size) != 3:
                raise ValueError("every 3D part needs centre/size vectors")
            for n in center: _finite_number(n)
            for n in size: _finite_number(n, positive=True)
            # This only bounds the nominal prototype in a reference envelope,
            # not swept robot motion or thermal distortion.
            for axis in range(3):
                if axis < 2 and abs(center[axis]) + size[axis]/2 > envelope[axis] * 0.8 + 1e-9:
                    raise ValueError("part outside illustrative planar envelope")
                if axis == 2 and (center[axis] - size[axis]/2 < -1e-9 or
                                   center[axis] + size[axis]/2 > envelope[axis] + 1e-9):
                    raise ValueError("part outside illustrative Z envelope")
        for stage in stages:
            if stage.get("process") not in STAGE_TYPES or stage.get("part_ids") is None:
                raise ValueError("unknown stage process/parts")
            if len(stage["part_ids"]) != len(set(stage["part_ids"])):
                raise ValueError("duplicated stage part")
            for part_id in stage["part_ids"]:
                if part_id not in part_ids or part_id in referenced:
                    raise ValueError("unknown or re-used part in stage")
                referenced.add(part_id)
                if next(p for p in parts if p["id"] == part_id)["stage"] != stage["id"]:
                    raise ValueError("part/stage binding mismatch")
        if referenced != part_ids:
            raise ValueError("parts not assigned exactly once")
        if v["parameters"].get("battery_capacity_wh") is not None or v["parameters"].get("compute_capacity_n") is not None:
            raise ValueError("battery/compute values require separate source measurement")
    return True


def _display_area(variant):
    p=variant["parameters"]
    if "display_width_mm" in p:
        return round(_finite_number(p["display_width_mm"],positive=True) *
                     _finite_number(p["display_height_mm"],positive=True), 5)
    if "display_diameter_mm" in p:
        d = _finite_number(p["display_diameter_mm"],positive=True)
        return round(math.pi * d*d/4, 5)
    return None


def _motion_candidate(variant):
    # Function intent / visual sweep samples only, no inferred torque, dynamics,
    # collisions, control firmware, power consumption or motion authorization.
    p=variant["parameters"]
    tracks=p.get("drive_track_count")
    if tracks is None:
        return None
    return {"meaning":"SCHEMATIC_KINEMATIC_ENVELOPE_NOT_VALIDATED",
            "track_count_candidate":tracks,
            "left_arm_degrees":p.get("arm_left_degrees"),
            "right_arm_degrees":p.get("arm_right_degrees"),
            "torque_nm":p.get("mechanism_torque_nm"),
            "torque_verified":False}



def _source_dependency_coverage(variant: dict) -> dict | None:
    """Reference owner-owned inverse DAG IDs; does not infer printed function."""
    goal = variant.get("source_goal_node")
    refs = [p["source_dependency_node_ref"] for p in variant["parts"]
            if "source_dependency_node_ref" in p]
    if goal is None:
        if refs:
            raise ValueError("source node refs require registered inverse goal")
        return None
    if type(goal) is not str or not goal or type(refs) is not list:
        raise ValueError("unregistered source inverse goal")
    graph_file = HERE / "PRINTCEPTOR_INVERSE_BUILD_GRAPH_v0_1.json"
    graph = json.loads(graph_file.read_text(encoding="utf-8"))
    if graph.get("schema") != "cgx.printspace.inverse_build_graph.v0.1":
        raise ValueError("unregistered inverse source graph")
    index = {c["id"]: c for c in graph["components"]}
    if len(index) != len(graph["components"]) or goal not in index:
        raise ValueError("missing or duplicate inverse source identity")
    needed = set(index[goal].get("needs", []))
    if not needed or len(needed) > 64 or any(x not in index for x in needed):
        raise ValueError("inverse goal missing verified dependency closure")
    if any(type(ref) is not str or ref not in needed for ref in refs):
        raise ValueError("preview references foreign or unregistered source dependency")
    represented = set(refs)
    return {
        "graph_sha256": source_sha(graph_file),
        "owner_goal_id": goal,
        "required_node_ids": sorted(needed),
        "referenced_node_ids": sorted(represented),
        "not_geometrically_represented": sorted(needed-represented),
        "reference_count": len(refs),
        "inference": "SEMANTIC_MOUNTING_POINT_NOT_PHYSICALLY_IMPLEMENTED",
        "physical_functional_coverage_verified": False,
        "electrical_control_safety_verified": False,
        "qualified_fabrication": False,
    }




I3_TRACK_PLAN = HERE / "BUTTERBOT_I3_TRACK_CLOSURE_PLAN_v0_1.json"
I3_ROUTE_SCHEMA = "cgx.printspace.butterbot_i3_track_closure_compiled.v0.1"


def compile_i3_track_closure_plan(path=I3_TRACK_PLAN):
    """Resolve ordered tool travel and mechanism prerequisites without a machine.

    An ordered symbolic station route can be independently reviewed and
    sampled without commanding either arm. Positions, collision free-space,
    tension force and the Intel Core i3 SKU remain explicit unknowns.
    """
    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema") != "cgx.printspace.butterbot_i3_core_track_closure.v0.1":
        raise ValueError("unregistered Intel i3 track-closure schema")
    if (raw.get("status") != "SOURCE_CANDIDATE_NO_HARDWARE_CONTROL" or
            raw.get("safety", {}).get("physical_process_approved") is not False or
            raw.get("safety", {}).get("armed_tool_action_allowed") is not False):
        raise ValueError("unqualified manufacturing authority")
    source = raw.get("host_i3_seed", {})
    if (source.get("core_family") != "Intel Core i3" or
            source.get("exact_sku") is not None or
            source.get("safety_control") != "SEPARATE_DETERMINISTIC_MCU"):
        raise ValueError("Intel i3 SKU/independent safety role must remain unresolved")
    if source.get("implementation") != "SOURCED_COMPUTE_MODULE_BOARD_COOLING_STORAGE_MEMORY":
        raise ValueError("CPU silicon cannot be printed by this route")

    components = raw.get("source_components", [])
    if not isinstance(components, list) or not 1 <= len(components) <= 128:
        raise ValueError("invalid component registry")
    ids = [c["id"] for c in components]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate component identity")
    registry = {c["id"]: c for c in components}
    for c in components:
        if not isinstance(c.get("required"), list) or not c["required"]:
            raise ValueError("component lacks passport/functional requirements")
        if c.get("kind") == "SOURCED" and c.get("can_print") is not False:
            raise ValueError("fabricating an unprintable sourced component")
    for required in ("i3_module", "motor_left", "motor_right", "battery_pack",
                     "safety_MCU", "motor_drivers", "servo_pack",
                     "speaker_and_LEDs", "sensors", "track_links",
                     "join_pins", "wheel_bearings", "idler_axles"):
        if required not in registry:
            raise ValueError("mechanical/electrical BOM missing " + required)

    stations = raw.get("stations", {})
    if not isinstance(stations, dict) or len(stations) < 12:
        raise ValueError("unregistered machine stations")
    if any(x.get("physical_position_mm") is not None for x in stations.values()):
        raise ValueError("machine travel positions cannot be asserted before calibration")
    steps = _sorted_stages(raw.get("steps", []))
    if not 15 <= len(steps) <= 128:
        raise ValueError("unbounded staged build")
    named = {s["id"]: s for s in steps}
    index = {s["id"]: idx for idx, s in enumerate(steps)}

    for stage in steps:
        if (stage.get("source_station") not in stations or
                stage.get("target_station") not in stations):
            raise ValueError("stage origin/destination station unresolved")
        if stage.get("motion_path_proven") is not False or stage.get("physical_execution_approved") is not False:
            raise ValueError("unsafe machine motion authority")
        if not isinstance(stage.get("evidence_required"), list) or not stage["evidence_required"]:
            raise ValueError("operation requires explicit proof list")
        parts = stage.get("component_ids")
        if not isinstance(parts, list) or len(parts) != len(set(parts)) or any(p not in registry for p in parts):
            raise ValueError("stage uses unregistered source component")
        role = stage.get("tool_role")
        if type(role) is not str or not role.startswith(("ARM_", "CAMERA_", "ISOLATED_")):
            raise ValueError("tool role unregistered")
        if stage.get("allowance_fraction") is not None:
            if stage["id"] not in ("S02_LOWER_TRACK_LEFT_10PCT",
                                  "S03_LOWER_TRACK_RIGHT_10PCT") or \
                    stage["allowance_fraction"] != 0.1:
                raise ValueError("10 percent allowance cannot be applied to tension")

    expected = (
        "S00_CORE_BASIS", "S02_LOWER_TRACK_LEFT_10PCT",
        "S03_LOWER_TRACK_RIGHT_10PCT", "S04_PRINT_CHASSIS_AND_CRADLE",
        "S06_INSTALL_BEARINGS_AXLES", "S07_INSTALL_TRACK_DRIVE_MOTORS",
        "S08_CHECK_TRACK_OPEN_ROUTE", "S13_INSTALL_I3_MODULE",
        "S14_BATTERY_AND_REGULATORS", "S17_VOICE_LED",
        "S18_DRY_ASSEMBLY_INSPECTION", "S19_MEASURE_FINAL_TRACK_ROUTE",
        "S20_PREP_LEFT_TRACK", "S21_CLOSE_LEFT_TRACK",
        "S22_LEFT_COOL_RELAX_INSPECT", "S23_PREP_RIGHT_TRACK",
        "S24_CLOSE_RIGHT_TRACK", "S25_RIGHT_COOL_RELAX_INSPECT",
        "S26_FINAL_C0_TEST", "S27_FINISH_AND_PARK",
    )
    if any(x not in index for x in expected):
        raise ValueError("closure dependency stage missing")
    if sorted(index[x] for x in expected) != [index[x] for x in expected]:
        raise ValueError("closure order/dependency violation")

    before_electronics = ("S10_PRINT_ARM_AND_NECK", "S16_HEAD_SHELL")
    if any(index[x] >= index["S13_INSTALL_I3_MODULE"] for x in before_electronics):
        raise ValueError("hot structural printing after sourced electronics")
    if index["S16_HEAD_SHELL"] >= index["S14_BATTERY_AND_REGULATORS"]:
        raise ValueError("heated shell work after battery insertion")
    for sid in ("S21_CLOSE_LEFT_TRACK", "S24_CLOSE_RIGHT_TRACK"):
        stage = named[sid]
        if "NO_UNQUALIFIED_HOT_WELD" not in stage.get("temperature_guard", ""):
            raise ValueError("closure must hold hot welding near sourced electronics")
        if stage.get("toolhead_conflict_guard") is not True:
            raise ValueError("closure lacks tool collision guard")
    left = named["S21_CLOSE_LEFT_TRACK"]
    right = named["S24_CLOSE_RIGHT_TRACK"]
    if ((left.get("tension_arm"), left.get("joining_arm")) != ("ARM_A", "ARM_B") or
            (right.get("tension_arm"), right.get("joining_arm")) != ("ARM_B", "ARM_A")):
        raise ValueError("two-arm handoff/alternation contract violated")
    if (named["S20_PREP_LEFT_TRACK"].get("tension_arm") != "ARM_A" or
            named["S23_PREP_RIGHT_TRACK"].get("tension_arm") != "ARM_B"):
        raise ValueError("fixture handoff does not match closure")
    p = raw.get("track_plan", {})
    if (p.get("allowance", {}).get("value") != 0.10 or
            p["allowance"].get("applies_to") !=
            "RAW_UNTRIMMED_LOWER_STOCK_OR_PRINTED_FIT_TABS_ONLY" or
            "BELT_OPERATING_STRAIN" not in p["allowance"].get("applies_not_to", [])):
        raise ValueError("track allowance incorrectly assumed final strain")
    if (p.get("force_target_n") is not None or
            p.get("closed_loop_tension_validated") is not False or
            p.get("safety_default", "").split(";")[0] !=
            "MECHANICAL_PIN_AND_IDLER"):
        raise ValueError("unqualified track tension or thermal joining")
    modes = p.get("closure_modes", [])
    if not modes or sum(m.get("default") is True for m in modes) != 1 or \
            any(m.get("physical_ready") is not False for m in modes):
        raise ValueError("closure mode wrongly qualified")
    if raw.get("access_contract", {}).get("all_axes_calibration_and_collision_sweeps_required") is not True:
        raise ValueError("machine collision/clearance acceptance missing")

    # The parser cannot infer actual path distance, joint servo torque, speed,
    # friction or loaded deformation from symbolic station identifiers.
    seen = set()
    visible = set()
    frames = []
    render_parts = {
        "S02_LOWER_TRACK_LEFT_10PCT": ("left_track",),
        "S03_LOWER_TRACK_RIGHT_10PCT": ("right_track",),
        "S04_PRINT_CHASSIS_AND_CRADLE": ("chassis",),
        "S10_PRINT_ARM_AND_NECK": ("neck", "left_arm", "right_arm"),
        "S13_INSTALL_I3_MODULE": ("compute_bay",),
        "S14_BATTERY_AND_REGULATORS": ("battery_cavity",),
        "S16_HEAD_SHELL": ("head",),
        "S17_VOICE_LED": ("face",),
    }
    for idx, stage in enumerate(steps):
        if not set(stage["depends_on"]) <= seen:
            raise ValueError("unsatisfied step dependency")
        seen.add(stage["id"])
        visible.update(render_parts.get(stage["id"], ()))
        is_closure = stage["operation"] == "LAST_TRACK_CLOSURE"
        frames.append({
            "step": idx + 1,
            "progress_fraction": round((idx + 1) / len(steps), 6),
            "stage_id": stage["id"],
            "operation": stage["operation"],
            "from_station": stage["source_station"],
            "to_station": stage["target_station"],
            "travel_mm": None,
            "cartesian_path": None,
            "tool_role": stage["tool_role"],
            "tension_arm": stage.get("tension_arm"),
            "joining_arm": stage.get("joining_arm"),
            "force_target_n": None,
            "force_measured_n": None,
            "workpiece_temperature_c": None,
            "time_s": None,
            "visible_part_ids": sorted(visible),
            "closure_side": "LEFT" if stage["id"] == "S21_CLOSE_LEFT_TRACK"
                            else "RIGHT" if stage["id"] == "S24_CLOSE_RIGHT_TRACK" else None,
            "track_left_closed_candidate": index["S21_CLOSE_LEFT_TRACK"] <= idx,
            "track_right_closed_candidate": index["S24_CLOSE_RIGHT_TRACK"] <= idx,
            "operation_evidence": stage["evidence_required"],
            "output_state_candidate": stage["output_state"],
            "source_component_ids": stage["component_ids"],
            "tool_reachability_verified": False,
            "joint_strength_verified": False,
            "tension_verified": False,
            "physical_execution_approved": False,
        })

    return {
        "schema": I3_ROUTE_SCHEMA,
        "source_sha256": source_sha(path),
        "root": "BB-FINAL",
        "cpu": source,
        "source_components": components,
        "station_metadata": stations,
        "track": p,
        "ordered_stages": [s["id"] for s in steps],
        "frames": frames,
        "stage_count": len(frames),
        "physical_machine_motion_simulated": False,
        "full_functional_butterbot_simulation": False,
        "electrical_source_verified": False,
        "authentic_original_CAD_verified": False,
        "finished_article_printed": False,
        "factory_production_authorized": False,
        "holds": raw.get("known_limits", []),
    }



def compile_preview(source, *, source_hash=None):
    validate_seed(source)
    routes = []
    for v in source["product_variants"]:
        stages = _sorted_stages(v["stages"])
        stage_index = {s["id"]: i for i, s in enumerate(stages)}
        parts = [{**p, "first_visible_frame":stage_index[p["stage"]] + 1,
                  "evidence":"SCHEMATIC_NOT_SOURCE_CAD"} for p in v["parts"]]
        frames=[]
        for i, stage in enumerate(stages):
            completed = {s["id"] for s in stages[:i+1]}
            visible = [p["id"] for p in parts if p["stage"] in completed]
            contract = source["process_contracts"][stage["process"]]
            frames.append({
                "step":i+1,"progress_fraction":round((i+1)/len(stages),6),
                "stage_id":stage["id"],"process":stage["process"],
                "visible_part_ids":visible,
                "added_part_ids":stage["part_ids"],
                "process_required_evidence":contract["needs"],
                "process_status":stage["status"],
                "claimed_elapsed_seconds":None,"measured_temperature_c":None,
                "measured_energy_j":None,"qualified_process":False,
                "observed_substrate_state":None,"stage_process_window_verified":False,
            })
        routes.append({
            "id":v["id"],"name":v["name"],"kind":v["kind"],"family":v["family"],
            "source_evidence":"PARAMETRIC_SEED_NOT_ORIGINAL_CAD",
            "envelope_mm":v["design_envelope_mm"],"aesthetic":v["aesthetic"],
            "parameters":v["parameters"],"display_area_mm2_candidate":_display_area(v),
            "battery_capacity_wh":None,"compute_capacity_n":None,
            "motion_candidate":_motion_candidate(v),
            "inverse_source_coverage":_source_dependency_coverage(v),
            "i3_track_build_route":(compile_i3_track_closure_plan()
                                    if v["id"]=="BB-SOURCE-DEMO" else None),
            "parts":parts,"frames":frames,
            "unknowns":v["source_caveats"],
            "qualified_fabrication":False,"production_approved":False,
        })
    return {
        "schema":SCHEMA,"source_sha256":source_hash,
        "units":"mm","timeline":"NORMALIZED_ORDER_NO_MEASURED_SECONDS",
        "process_catalog":source["process_contracts"],
        "directional_material_catalog_sha256": source_sha(
            HERE / "PAIRWISE_SEQUENCE_ROUTES_v0_1.json"),
        "process_window_profiles": {
            process: {
                state: assess_process_window(
                    process,substrate_state=state,
                    process_contracts=source["process_contracts"])
                for state in sorted(SUBSTRATE_STATES)
            } for process in sorted(STAGE_TYPES)
        },
        "physical_or_calibrated_simulation":False,
        "source_cad_ownership_verified":False,
        "public_release_authorized":False,"machine_control_enabled":False,
        "products":routes,
    }


def load_and_compile(path=SEEDS):
    path=Path(path)
    return compile_preview(json.loads(path.read_text(encoding="utf-8")),
                           source_hash=source_sha(path))



def assess_functional_device_requirements(
    product: dict, *,
    arm_angle_deg=None, arm_length_mm=None, payload_mass_kg=None,
    required_screen_area_mm2=None,
    battery_capacity_wh=None, average_power_w=None,
    compute_target_n=None, compute_metric=None,
) -> dict:
    """Bounded first-order requirement comparisons; NOT a device qualification.

    Geometry can be exactly resolved from admitted candidate parameters.
    Torque below is only a static gravity contribution; motor startup,
    inertia, gearing, holding current and losses are intentionally excluded.
    Battery runtime is an ideal arithmetic upper-bound estimate, not a
    certified runtime; no supplied compute metric is silently converted to W.
    """
    if not isinstance(product, dict) or product.get("source_evidence") != "PARAMETRIC_SEED_NOT_ORIGINAL_CAD":
        raise ValueError("unrecognized source-bound functional candidate")
    def optional(value, name, *, strict_positive=False):
        if value is None:
            return None
        if type(value) not in (int, float) or not math.isfinite(value) or abs(value) > 1e9:
            raise ValueError(name + " must be finite bounded numeric")
        if value < 0 or (strict_positive and value == 0):
            raise ValueError(name + " must be nonnegative (strictly positive when required)")
        return float(value)

    if arm_angle_deg is not None:
        if type(arm_angle_deg) not in (int, float) or not math.isfinite(arm_angle_deg) or abs(arm_angle_deg) > 180:
            raise ValueError("arm angle must be finite within -180..180 degrees")
        angle = float(arm_angle_deg)
    else:
        angle = None
    length = optional(arm_length_mm,"arm_length_mm",strict_positive=True)
    mass = optional(payload_mass_kg,"payload_mass_kg")
    display = optional(required_screen_area_mm2,"required_screen_area_mm2",strict_positive=True)
    wh = optional(battery_capacity_wh,"battery_capacity_wh")
    watts = optional(average_power_w,"average_power_w",strict_positive=True)
    target = optional(compute_target_n,"compute_target_n")
    if target is not None and (not isinstance(compute_metric,str) or
                               not 1 <= len(compute_metric) <= 64):
        raise ValueError("compute_n requires declared metric and units")
    if angle is not None and product.get("kind") != "tracked_robot":
        raise ValueError("arm angle not applicable to this article")

    holds = []
    results = {
        "schema":"cgx.printspace.functional_requirements_candidate.v0.1",
        "product_id":product["id"],
        "evidence":"USER_PARAMETER_MATH_ONLY_NOT_AS_BUILT",
        "measured_or_qualified":False,
        "source_rights_verified":False,
        "hardware_control":False,
        "required_screen_area_mm2": display,
        "available_display_area_mm2_schematic":product["display_area_mm2_candidate"],
        "display_fit_comparison":None,
        "arm_angle_deg_requested": angle,
        "arm_tip_horizontal_offset_mm":None,
        "arm_tip_vertical_rise_mm":None,
        "static_gravity_torque_nm_candidate":None,
        "battery_wh_user_candidate":wh,
        "average_power_w_user_candidate":watts,
        "ideal_arithmetic_runtime_h":None,
        "compute_n_user_candidate":target,
        "compute_metric":compute_metric if target is not None else None,
        "unresolved":[]
    }
    if display is not None:
        maxarea=product["display_area_mm2_candidate"]
        results["display_fit_comparison"] = (
            "UNRESOLVED_AVAILABLE_DISPLAY" if maxarea is None else
            "AREA_ONLY_FITS" if display <= maxarea else "AREA_EXCEEDS_SCHEMATIC_APERTURE"
        )
        if maxarea is None or display > maxarea:holds.append("screen area/electro-optical packaging")
        # Same area does not prove that rectangular vs circular panel can fit.
        holds.append("screen outline, thickness, radii, electrical/optical interfaces and sealing")
    if angle is not None:
        if length is None:holds.append("arm length/datum/kinematic calibration")
        else:
            rad=math.radians(angle)
            results["arm_tip_horizontal_offset_mm"]=round(length*math.sin(rad),6)
            results["arm_tip_vertical_rise_mm"]=round(length*math.cos(rad),6)
        if mass is not None and length is not None:
            results["static_gravity_torque_nm_candidate"]=round(
                mass*9.80665*length/1000*math.sin(math.radians(angle)),8)
        holds.append("joint limits, bearings, full dynamic loads, motor curves, safety and collision sweep")
    if wh is not None or watts is not None:
        if wh is not None and watts is not None:
            results["ideal_arithmetic_runtime_h"]=round(wh/watts,6)
        holds.append("battery chemistry/discharge curve, thermal protection, power conversion and actual duty cycle")
    if target is not None:
        holds.append("compute workload benchmark, power performance, firmware and measured throughput")
    results["unresolved"] = sorted(set(holds))
    return results




# Temporal substrate state is a requested process condition, not a material
# property measured by this preview.
SUBSTRATE_STATES = frozenset((
    "UNKNOWN", "WET_FLOWABLE", "GREEN_PARTIALLY_CURED", "STABILIZED"
))
ENVIRONMENT_STATES = frozenset((
    "UNKNOWN", "OPEN", "LOCAL_SHROUD", "SEALED_MICROCHAMBER", "MACRO_CHAMBER"
))
OPTICAL_PROCESSES = frozenset((
    "UV_CURE_CANDIDATE", "IN_PROCESS_UV_PATTERN_CANDIDATE",
    "MASKED_PHOTOLITHOGRAPHY_CANDIDATE", "LASER_DIRECT_WRITE_CANDIDATE"
))
PATTERN_PROCESSES = frozenset((
    "IN_PROCESS_UV_PATTERN_CANDIDATE",
    "MASKED_PHOTOLITHOGRAPHY_CANDIDATE",
    "LASER_DIRECT_WRITE_CANDIDATE",
))


def assess_process_window(
    process: str, *, substrate_state: str = "UNKNOWN",
    environment: str = "UNKNOWN",
    source_lot_ref: str | None = None,
    substrate_temperature_c: float | None = None,
    exposure_dose_j_cm2: float | None = None,
    focus_or_alignment_um: float | None = None,
    process_contracts: dict | None = None,
) -> dict:
    """CAN-IF process selector; no machine approval or inferred chemistry.

    Missing independent calibration/coupon evidence cannot be filled by a
    user-entered temperature/dose/lot label. A WET state is neither
    universally prohibited nor implicitly safe for laser or lithography.
    """
    if type(process) is not str or process not in STAGE_TYPES:
        raise ValueError("unregistered PrintSpace process")
    if substrate_state not in SUBSTRATE_STATES:
        raise ValueError("unregistered substrate state")
    if environment not in ENVIRONMENT_STATES:
        raise ValueError("unregistered processing environment")
    if source_lot_ref is not None and (
        type(source_lot_ref) is not str or
        not 1 <= len(source_lot_ref) <= 128 or
        any(ord(ch) < 32 for ch in source_lot_ref)
    ):
        raise ValueError("source lot must be a bounded non-secret reference")
    for name, value, positive in (
        ("substrate_temperature_c", substrate_temperature_c, False),
        ("exposure_dose_j_cm2", exposure_dose_j_cm2, True),
        ("focus_or_alignment_um", focus_or_alignment_um, True),
    ):
        if value is None:
            continue
        if type(value) not in (float, int) or not math.isfinite(value) or abs(value) > 1000000:
            raise ValueError(name + " must be finite bounded numeric")
        if positive and value <= 0:
            raise ValueError(name + " must be positive")
    contracts = process_contracts
    if contracts is None:
        # Existing source-owned registry, not a second local process master.
        contracts = json.loads(SEEDS.read_text(encoding="utf-8"))["process_contracts"]
    if process not in contracts or contracts[process].get("can_run_physically") is not False:
        raise ValueError("unregistered or unqualified process contract")

    needs = list(contracts[process].get("needs", []))
    if not needs or len(needs) != len(set(needs)):
        raise ValueError("missing, duplicated or invalid source requirements")
    holds = list(needs)
    if substrate_state == "UNKNOWN":
        holds.append("actual substrate cure/rheology and temperature state")
    if environment == "UNKNOWN":
        holds.append("actual local atmosphere, pressure and process shielding")
    if source_lot_ref is None:
        holds.append("exact material lot and chemistry passport")
    if substrate_temperature_c is None:
        holds.append("measured substrate temperature and thermal history")
    if process in OPTICAL_PROCESSES and exposure_dose_j_cm2 is None:
        holds.append("calibrated dose/fluence and optical material response")
    if process in PATTERN_PROCESSES and focus_or_alignment_um is None:
        holds.append("feature registration/spot metrology and actual resolution")
    if substrate_state in ("WET_FLOWABLE", "GREEN_PARTIALLY_CURED") and process in OPTICAL_PROCESSES:
        holds.append("time-dependent viscosity, swelling/shrinkage, focus and chemical selectivity coupon")
        holds.append("survivability of all earlier deposited material and features")
    if process == "MASKED_PHOTOLITHOGRAPHY_CANDIDATE":
        holds.append("photoresist application, mask, development, rinse and compatible etch/lift-off")
        if substrate_state == "WET_FLOWABLE":
            holds.append("wet resist/mask adhesion and fiducial stability under flow")
    if process == "LASER_DIRECT_WRITE_CANDIDATE":
        holds.append("independent laser-rated enclosure, electrical interlock, extraction and optical isolation")
        if environment == "OPEN":
            holds.append("open laser process not authorized without validated local enclosure")
    if process in ("SOURCED_COMPONENT_PLACEMENT",):
        holds.append("actual manufacturer component passport, ESD, alignment and thermal exposure")

    if process in OPTICAL_PROCESSES and substrate_state == "UNKNOWN":
        disposition = "HOLD_SUBSTRATE_STATE_UNRESOLVED"
    elif process == "LASER_DIRECT_WRITE_CANDIDATE" and environment == "OPEN":
        disposition = "HOLD_LASER_ENCLOSURE_NOT_QUALIFIED"
    elif process == "MASKED_PHOTOLITHOGRAPHY_CANDIDATE" and substrate_state == "WET_FLOWABLE":
        disposition = "CAN_IF_WET_CHEMISTRY_FOCUS_AND_MASK_COUPONS_VALIDATED"
    elif process in OPTICAL_PROCESSES and substrate_state in ("WET_FLOWABLE", "GREEN_PARTIALLY_CURED"):
        disposition = "CAN_IF_TRANSIENT_STATE_EXPOSURE_AND_DAMAGE_VALIDATED"
    else:
        disposition = "CAN_IF_SOURCE_REQUIREMENTS_INDEPENDENTLY_QUALIFIED"

    return {
        "schema": "cgx.printspace.temporal_process_window_candidate.v0.1",
        "process": process, "substrate_state": substrate_state,
        "environment": environment,
        "source_lot_ref_user_candidate": source_lot_ref,
        "substrate_temperature_c_user_candidate": substrate_temperature_c,
        "exposure_dose_j_cm2_user_candidate": exposure_dose_j_cm2,
        "focus_or_alignment_um_user_candidate": focus_or_alignment_um,
        "disposition": disposition,
        "requires_independent_evidence": sorted(set(holds)),
        "physical_process_verified": False,
        "material_compatibility_verified": False,
        "safety_interlocks_verified": False,
        "claim_time_seconds": None,
        "hardware_command": None,
        "production_approved": False,
    }


def review_directional_material_transition(
    from_family: str, to_family: str, *,
    catalog_path: Path | None = None,
) -> dict:
    """Return exact owner pair record without treating the reverse as equal."""
    source = (HERE / "PAIRWISE_SEQUENCE_ROUTES_v0_1.json") if catalog_path is None else Path(catalog_path)
    catalog = json.loads(source.read_text(encoding="utf-8"))
    families = {item["id"] for item in catalog["families"]}
    pairs = catalog["pairs"]
    if len(families) != 14 or len(pairs) != 196 or len(set((p["from"], p["to"]) for p in pairs)) != 196:
        raise ValueError("directional Raphael catalog incomplete")
    if from_family not in families or to_family not in families:
        raise ValueError("unregistered material family transition")
    match = next(p for p in pairs if p["from"] == from_family and p["to"] == to_family)
    reverse = next(p for p in pairs if p["from"] == to_family and p["to"] == from_family)
    if match.get("production_approved") is not False or not match.get("directional"):
        raise ValueError("unqualified directional pair wrongly promoted")
    return {
        "schema": "cgx.printspace.directional_transition_review.v0.1",
        "from": from_family, "to": to_family,
        "source_catalog_sha256": source_sha(source),
        "pair_id": match["pair_id"], "route_class": match["route_class"],
        "route_label": match["route_label"],
        "stage_controls": match["stage_controls"],
        "fallback_routes": match["fallback_routes"],
        "reverse_pair_id": reverse["pair_id"],
        "reverse_is_separate_contract": from_family != to_family,
        "recipe_and_coupon_evidence": match["physical_evidence"],
        "production_approved": False, "actual_tool_route_available": False,
    }




ADAPTIVE_SEED_POLICY = HERE / "BUTTERBOT_ADAPTIVE_SEED_THRESHOLDS_v0_1.json"
ADAPTIVE_SCENARIO_FIXTURE = HERE / "BUTTERBOT_ADAPTIVE_THREE_SCENARIOS_v0_1.json"
ADAPTIVE_SOLUTION_SCHEMA = "cgx.printspace.butterbot_adaptive_three_solutions.v0.1"
TIER_ORDER = ("BOOTSTRAP_EVERYDAY", "PRO_BALANCED", "INDUSTRIAL_CIRCULAR")


def _bounded_number(value, name, *, positive=False):
    """Allow finite nonnegative numeric scenario values, never bool or NaN."""
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or value > 100000000:
        raise ValueError(name + " must be finite and nonnegative")
    if positive and value == 0:
        raise ValueError(name + " must be positive")
    return float(value)


def _validate_adaptive_seed_data(policy, fixture, base):
    if policy.get("schema") != "cgx.printspace.butterbot_adaptive_seed_thresholds.v0.1":
        raise ValueError("unregistered adaptive threshold policy")
    if fixture.get("schema") != "cgx.printspace.butterbot_adaptive_scenario_fixture.v0.1":
        raise ValueError("unregistered adaptive scenario fixture")
    if (fixture.get("status") != "SYNTHETIC_SCENARIO_ONLY_NO_LIVE_SOURCE_ATTESTATION" or
            policy.get("status") != "SOURCE_REVIEW_ONLY_NOT_PRODUCTION" or
            policy.get("source_policy", {}).get("hardware_control") is not False):
        raise ValueError("adaptive scenario cannot authorize manufacture")
    tiers = policy.get("tiers", [])
    if [t.get("id") for t in tiers] != list(TIER_ORDER):
        raise ValueError("exact three separate tier policies required")
    if base["schema"] != I3_ROUTE_SCHEMA or base.get("factory_production_authorized") is not False:
        raise ValueError("source 28-stage plan must remain unqualified")
    base_stage_ids = {f["stage_id"] for f in base["frames"]}
    all_stages = set(base_stage_ids)
    for tier in tiers:
        weights = tier.get("weights", {})
        if set(weights) != {"cost", "runtime", "compute", "thermal", "printability"}:
            raise ValueError("tier must declare all five optimization weights")
        if abs(sum(_bounded_number(x, "weight") for x in weights.values()) - 1.0) > 1e-8:
            raise ValueError("multi-objective tier weights must sum to one")
        if tier.get("sealed_session_mandatory") is not True or \
                tier.get("allowed_cpu_families") != ["i3", "i5"]:
            raise ValueError("cpu substitutions and sealed session are mandatory")
        _bounded_number(tier["required_workload_n"], "required_workload", positive=True)
        _bounded_number(tier["min_ideal_runtime_h"], "min_runtime", positive=True)
        _bounded_number(tier["min_i5_gain_ratio"], "min_i5_gain_ratio", positive=True)
        _bounded_number(tier["preferred_print_fraction"], "print_target", positive=True)
        if not 0 < tier["preferred_print_fraction"] <= 1:
            raise ValueError("invalid printable fraction target")
        inserts = tier.get("stage_insertions", [])
        if len(inserts) > 8:
            raise ValueError("too many conditional tier process insertions")
        for item in inserts:
            if item["after"] not in base_stage_ids or item["id"] in all_stages:
                raise ValueError("unregistered or conflicting inserted stage")
            if item.get("qualified") is not False or \
                    item.get("kind") != "SCHEMATIC_REVIEW_ONLY":
                raise ValueError("unqualified inserted manufacturing authority")
            all_stages.add(item["id"])

    candidates = fixture.get("candidates", [])
    if not 1 <= len(candidates) <= 24:
        raise ValueError("unbounded CPU candidate inventory")
    if len({c["id"] for c in candidates}) != len(candidates):
        raise ValueError("duplicate CPU candidate")
    for c in candidates:
        if c.get("family") not in ("i3", "i5") or \
                c.get("source_type") != "SYNTHETIC_ONLY_NO_PURCHASING_CLAIM" or \
                c.get("exact_cpu_sku") is not None or \
                c.get("board_and_cooler_passport_verified") is not False:
            raise ValueError("CPU donor scenario must remain unverified")
        for key in ("cost_aud","peak_thermal_w","cooling_capacity_w",
                    "average_system_w","workload_score_n"):
            _bounded_number(c.get(key), "cpu "+key, positive=key!="cost_aud")
        xyz=c.get("module_xyz_mm", [])
        if len(xyz)!=3 or any(_bounded_number(v,"module xyz",positive=True)<=0 for v in xyz):
            raise ValueError("CPU mechanical envelope not bounded")
    snapshots=fixture.get("tier_snapshots", [])
    if [s.get("tier_id") for s in snapshots] != list(TIER_ORDER):
        raise ValueError("exact matching three inventory snapshots required")
    for s in snapshots:
        for k in ("max_spend_aud","battery_wh"):
            _bounded_number(s.get(k),k,positive=True)
        xyz=s.get("provisional_internal_envelope_mm",[])
        if len(xyz)!=3 or any(_bounded_number(v,"body xyz",positive=True)<=0 for v in xyz):
            raise ValueError("unbounded target enclosure")
        if len(set(s.get("assumed_process_cells",[]))) != len(s.get("assumed_process_cells",[])):
            raise ValueError("duplicated process capability")
        if s.get("internally_preloaded_sourced_trays") is not True or \
                s.get("real_sealed_session_witness") is not False or \
                s.get("measured_machine_cell_readiness") is not False:
            raise ValueError("sealed session evidence erroneously promoted")
    margins=fixture.get("margin_mm",[])
    if len(margins)!=3 or any(_bounded_number(v,"edge margin")>100 for v in margins):
        raise ValueError("invalid CPU margin")
    if fixture.get("benchmark_units") != "ABSTRACT_SYNTHETIC_WORKLOAD_N":
        raise ValueError("unadmitted real workload benchmark")
    return True


def _seed_candidate_scores(tier, snapshot, fixture, print_candidate_fraction):
    candidates=fixture["candidates"]
    i3_benchmark=max((c["workload_score_n"] for c in candidates if c["family"]=="i3"),default=None)
    available=min(_bounded_number(snapshot["max_spend_aud"],"budget",positive=True),
                  _bounded_number(tier["max_incremental_cost_aud"],"tier cap",positive=True)
                  if tier.get("max_incremental_cost_aud") is not None
                  else _bounded_number(snapshot["max_spend_aud"],"budget",positive=True))
    margins=fixture["margin_mm"]
    outcomes=[]
    for c in candidates:
        rejects=[]
        cost=float(c["cost_aud"])
        power=float(c["peak_thermal_w"])
        cooling=float(c["cooling_capacity_w"])
        work=float(c["workload_score_n"])
        runtime=float(snapshot["battery_wh"])/float(c["average_system_w"])
        if c["family"] not in tier["allowed_cpu_families"]:
            rejects.append("CPU_FAMILY_NOT_ALLOWED")
        if work < tier["required_workload_n"]:
            rejects.append("WORKLOAD_BELOW_TIER_MINIMUM")
        if runtime < tier["min_ideal_runtime_h"]:
            rejects.append("IDEAL_RUNTIME_BELOW_TIER_MINIMUM")
        if power > cooling:
            rejects.append("PEAK_THERMAL_LOAD_EXCEEDS_ASSUMED_COOLING")
        if cost > available:
            rejects.append("ACQUISITION_COST_EXCEEDS_ASSUMED_AVAILABLE_BUDGET")
        if any(c["module_xyz_mm"][i]+2*margins[i] >
               snapshot["provisional_internal_envelope_mm"][i] for i in range(3)):
            rejects.append("COMPLETE_MODULE_EXCEEDS_PROVISIONAL_ENVELOPE")
        missing_cells=sorted(set(tier["minimum_cells"]) -
                             set(snapshot["assumed_process_cells"]))
        if missing_cells:
            rejects.append("STATED_MACHINE_PROCESS_CELLS_MISSING")
        if c["family"]=="i5" and i3_benchmark is not None and \
                work < i3_benchmark*tier["min_i5_gain_ratio"]:
            rejects.append("I5_WORKLOAD_GAIN_DOES_NOT_CLEAR_THRESHOLD")
        costs=1-min(1,cost/available)
        ideal=min(1,runtime/(2*tier["min_ideal_runtime_h"]))
        compute=min(1,work/(2*tier["required_workload_n"]))
        thermal=min(1,max(0,(cooling-power)/power))
        printable=min(1,print_candidate_fraction/tier["preferred_print_fraction"])
        metrics={"cost":costs,"runtime":ideal,"compute":compute,
                 "thermal":thermal,"printability":printable}
        score=round(100*sum(float(tier["weights"][k])*metrics[k]
                            for k in tier["weights"]),6)
        outcomes.append({
            "id":c["id"],"family":c["family"],"sku":None,
            "scenario_cost_aud":cost,
            "scenario_workload_n":work,
            "scenario_peak_w":power,
            "scenario_cooling_capacity_w":cooling,
            "ideal_arithmetic_runtime_h":round(runtime,4),
            "hypothetical_module_xyz_mm":c["module_xyz_mm"],
            "rejected_thresholds":sorted(rejects),
            "scenario_eligible":not rejects,
            "weighted_score_scenario_only":score,
            "metrics_dimensionless":{k:round(v,4) for k,v in metrics.items()},
            "actual_hardware_verified":False,
        })
    outcomes.sort(key=lambda c:(not c["scenario_eligible"],-c["weighted_score_scenario_only"],c["id"]))
    return outcomes


def _insert_tier_review_stages(base_frames, tier):
    insert_after={}
    for x in tier["stage_insertions"]:
        insert_after.setdefault(x["after"],[]).append(x)
    output=[]
    for frame in base_frames:
        copy=dict(frame)
        copy["mode"]="BASE_28_STAGE_ROUTE"
        output.append(copy)
        for item in insert_after.get(frame["stage_id"],[]):
            overlay=dict(frame)
            overlay.update({
                "stage_id":item["id"],
                "operation":"OPTIONAL_TIER_CAPABILITY_HOLD",
                "source_component_ids":[],
                "tool_role":"REVIEW_ONLY_NON_ACTUATING",
                "from_station":frame["to_station"],
                "to_station":frame["to_station"],
                "travel_mm":None,
                "cartesian_path":None,
                "tension_arm":None,
                "joining_arm":None,
                "force_target_n":None,
                "force_measured_n":None,
                "workpiece_temperature_c":None,
                "time_s":None,
                "tool_reachability_verified":False,
                "joint_strength_verified":False,
                "tension_verified":False,
                "physical_execution_approved":False,
                "track_left_closed_candidate":frame["track_left_closed_candidate"],
                "track_right_closed_candidate":frame["track_right_closed_candidate"],
                "mode":"OPTIONAL_REVIEW_HOLD_NOT_HARDWARE_OPERATION",
                "operation_evidence":["machine cells: "+",".join(item["required_cells"]),
                                      "source-specific independent process coupon and controller witness"],
                "required_cells":item["required_cells"],
                "qualified":False
            })
            output.append(overlay)
    for i,frame in enumerate(output):
        frame["step"]=i+1
        frame["progress_fraction"]=round((i+1)/len(output),6)
    return output


def simulate_adaptive_seed_alternatives(
    policy_path=ADAPTIVE_SEED_POLICY, scenario_path=ADAPTIVE_SCENARIO_FIXTURE,
    *,
    base_route=None,
):
    """Select the best hypothetical component route for each of three tiers.

    No real score is returned: the published scenario inventory explicitly
    contains invented CPU energy, cost and performance examples, while each
    output retains source, rights, machine, interlock and part qualification HOLD.
    """
    policy_path=Path(policy_path)
    scenario_path=Path(scenario_path)
    policy=json.loads(policy_path.read_text(encoding="utf-8"))
    fixture=json.loads(scenario_path.read_text(encoding="utf-8"))
    base=compile_i3_track_closure_plan() if base_route is None else base_route
    _validate_adaptive_seed_data(policy,fixture,base)
    raw=json.loads(I3_TRACK_PLAN.read_text(encoding="utf-8"))
    classes=raw["source_components"]
    printable=sum(c["kind"]=="PRINT_CANDIDATE" for c in classes)
    fraction=printable/len(classes)
    if len(classes)!=19:
        raise ValueError("source-owned 19-class component registry has changed")
    outputs=[]
    for tier,snapshot in zip(policy["tiers"],fixture["tier_snapshots"]):
        results=_seed_candidate_scores(tier,snapshot,fixture,fraction)
        selected=next((x for x in results if x["scenario_eligible"]),None)
        frames=_insert_tier_review_stages(base["frames"],tier)
        outputs.append({
            "tier_id":tier["id"],
            "display_name":tier["display_name"],
            "machine_level_candidate":tier["pc_gate"],
            "objective":tier["candidate_process_policy"],
            "selection":selected,
            "alternatives":results[:3],
            "candidate_pool_size":len(results),
            "required_workload_n_synthetic":tier["required_workload_n"],
            "budget_aud_synthetic":snapshot["max_spend_aud"],
            "battery_wh_synthetic":snapshot["battery_wh"],
            "internally_preloaded_trays_hypothesized":True,
            "stage_count":len(frames),
            "frames":frames,
            "source_component_class_count":len(classes),
            "print_candidate_class_count":printable,
            "candidate_print_class_fraction":round(fraction,6),
            "target_print_fraction":tier["preferred_print_fraction"],
            "unknown_physical_print_fraction":True,
            "fully_printable":False,
            "all_component_printable_target_gate":"HOLD_UNTIL_SOURCED_CHIPS_BATTERY_MOTORS_PRECISION_CLAIM_QUALIFIED",
            "tension_force_validated":False,
            "actual_device_selection_approved":False,
            "real_battery_runtime_verified":False,
            "actual_sealed_session_verified":False,
            "toolpaths_and_simulated_physics_verified":False,
            "actual_CPU_SKU":None,
            "release_status":"DIGITAL_SCENARIO_ONLY_NO_PURCHASING_OR_HARDWARE_AUTHORITY",
            "unresolved":[
                "real processor SKU and board+cooler passport",
                "real price, workload benchmark and module power",
                "measured body fit, center of mass and dynamic drive torque",
                "printer calibration, automatic internal trays and safety C0",
                "material lot, print/wear/thermal/cure coupons and as-built scan",
                "real source rights and no mid-session manual chamber opening",
            ]
        })
    return {
        "schema":ADAPTIVE_SOLUTION_SCHEMA,
        "policy_sha256":source_sha(policy_path),
        "scenario_sha256":source_sha(scenario_path),
        "base_route_sha256":base["source_sha256"],
        "scenario_only":True,
        "tier_count":len(outputs),
        "selection_semantics":"ONE_BEST_HYPOTHETICAL_CPU_PER_TIER_NOT_CROSS_TIER_PRICE_RANKING",
        "computer_architecture":"SOURCED_CPU_AND_ELECTRONICS_RETAINED",
        "physical_process_qualified":False,
        "printed_entire_device":False,
        "closed_chamber_fabrication_accepted":False,
        "results":outputs,
    }



def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=Path,default=SEEDS)
    parser.add_argument("--product",default=None)
    args=parser.parse_args(argv)
    output=load_and_compile(args.seed)
    if args.product:
        output["products"]=[p for p in output["products"] if p["id"]==args.product]
        if not output["products"]:parser.error("unknown product")
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
