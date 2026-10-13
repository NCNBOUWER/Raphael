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
            "motion_candidate":_motion_candidate(v),"parts":parts,"frames":frames,
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
