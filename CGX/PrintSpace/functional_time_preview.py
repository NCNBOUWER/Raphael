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
        "physical_or_calibrated_simulation":False,
        "source_cad_ownership_verified":False,
        "public_release_authorized":False,"machine_control_enabled":False,
        "products":routes,
    }


def load_and_compile(path=SEEDS):
    path=Path(path)
    return compile_preview(json.loads(path.read_text(encoding="utf-8")),
                           source_hash=source_sha(path))


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
