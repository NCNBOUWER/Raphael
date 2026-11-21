"""CGX PrintSpace convergence shell — binary → ternary → T173, review only.

Additive reference consumer of existing Raphael geometry and PrintSpace sources.
No mint, DataSpace transport, machine driver, payment gateway or safety approval.
"""
from __future__ import annotations
import hashlib
import json
from copy import deepcopy

SCHEMA = "cgx.printspace.convergence_shell.v0.1"
BRAND = "UniSpace / CGX PrintSpace"
STATES = ("UNKNOWN", "CANDIDATE", "QUALIFIED", "FAILED")
PROCESS_CAPABILITIES = {
    "STRUCTURE": "polymer_deposition",
    "SURFACE_TEXTURE": "microtexture_tool",
    "CONDUCTOR": "conductive_deposition",
    "ELECTROPLATE": "electroplating",
    "SENSOR": "sensor_integration",
    "ENCAPSULATE": "barrier_deposition",
    "VALIDATE": "metrology",
}
GEOMETRY_REF = (
    "NCNBOUWER/Raphael:Raphael_Packages/geometry_173/"
    "showcase/analytic_reference_meshes_v05.json"
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_binary(value):
    """Standard JSON UTF-8 baseline; no NaN or ambiguous serialization."""
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def bytes_to_ternary(binary):
    """Six unsigned base-3 digits per byte: a LOSSLESS illustrative codec.

    This is not compression and must not be confused with three-valued logic.
    """
    _require(isinstance(binary, bytes), "binary bytes required")
    result = []
    for byte in binary:
        digits = [0] * 6
        for i in range(5, -1, -1):
            digits[i] = byte % 3
            byte //= 3
        result.extend(digits)
    return tuple(result)


def ternary_to_bytes(trits):
    _require(isinstance(trits, (list, tuple)) and len(trits) % 6 == 0,
             "trits must be a multiple of six")
    output = bytearray()
    for start in range(0, len(trits), 6):
        value = 0
        for digit in trits[start:start + 6]:
            _require(type(digit) is int and 0 <= digit <= 2,
                     "ternary digit must be 0, 1 or 2")
            value = value * 3 + digit
        _require(value <= 255, "non-byte ternary group")
        output.append(value)
    return bytes(output)


def binary_ternary_receipt(value):
    raw = canonical_binary(value)
    trits = bytes_to_ternary(raw)
    _require(ternary_to_bytes(trits) == raw, "lossless round trip failed")
    return {
        "binary_sha256": hashlib.sha256(raw).hexdigest(),
        "binary_bytes": len(raw),
        "ternary_digits": len(trits),
        "trit_codec": "UNSIGNED_BASE3_6_PER_BYTE_NOT_COMPRESSION",
        "roundtrip": "PASS",
        "separate_semantic_states": list(STATES),
        "measured_savings": None,
    }


def resolve_t173(slot, source):
    """Bind a role, not a new canonical mesh, to an independently sourced record.

    source is a caller-supplied, trusted and revision-pinned projection of the
    Raphael PR7 geometry record. This function does not authenticate that caller.
    """
    _require(type(slot) is int and 1 <= slot <= 173,
             "invalid or reserved T173 slot")
    _require(type(source) is dict, "geometry source must be a dictionary")
    record = source.get(str(slot))
    if record is None:
        return {"slot": slot, "state": "UNKNOWN", "source": GEOMETRY_REF,
                "mesh": None, "reason": "SOURCE_SLOT_UNRESOLVED"}
    _require(type(record) is dict, "invalid geometry record")
    alias = record.get("alias_of")
    if alias is not None:
        _require(type(alias) is int and 1 <= alias <= 173 and alias != slot,
                 "invalid alias target")
        target = source.get(str(alias))
        _require(type(target) is dict and target.get("alias_of") is None,
                 "missing alias target or alias chain")
        record = target
    sha = record.get("mesh_sha256")
    _require(isinstance(sha, str) and len(sha) == 64
             and all(c in "0123456789abcdef" for c in sha),
             "geometry requires a source-bound SHA256")
    _require(record.get("evidence") in ("REFERENCE_EUCLIDEAN", "QUALIFIED_CAD"),
             "geometry must declare bounded evidence")
    return {
        "slot": slot,
        "state": "CANDIDATE",  # physical suitability is NOT inferred
        "geometry_role": record.get("role_id"),
        "source": record.get("source", GEOMETRY_REF),
        "mesh_sha256": sha,
        "mesh_role": alias if alias is not None else slot,
        "evidence": record["evidence"],
        "unit": record.get("unit"),
        "physical_qualified": False,
        "Raphael_metric_qualified": False,
    }


def compile_plan(request, geometry_source, printer, routes):
    """Produce a source-linked *candidate* plan without scheduling or actuation.

    Each feature has id, operation and optional after (dependencies) and
    directional_route_id. Tool fabrication is an alternative path, not proof
    the tool exists or is safe for use.
    """
    _require(type(request) is dict and type(printer) is dict and
             type(routes) is dict, "invalid argument")
    _require(isinstance(request.get("object_id"), str) and request["object_id"],
             "object_id required")
    shape = resolve_t173(request.get("t173_slot"), geometry_source)
    features = request.get("features")
    _require(isinstance(features, list) and 0 < len(features) <= 256,
             "features must be a bounded list")
    ids = [f.get("id") for f in features]
    _require(all(isinstance(i, str) and i for i in ids) and
             len(ids) == len(set(ids)), "duplicate/invalid feature ID")
    feature_by_id = {f["id"]: f for f in features}
    for feature in features:
        _require(feature.get("operation") in PROCESS_CAPABILITIES,
                 "unrecognized operation")
        deps = feature.get("after", [])
        _require(isinstance(deps, list) and len(deps) == len(set(deps))
                 and all(dep in feature_by_id and dep != feature["id"]
                         for dep in deps), "invalid dependency")
    order, pending, done = [], set(ids), set()
    while pending:
        eligible = sorted(i for i in pending
                          if set(feature_by_id[i].get("after", [])) <= done)
        _require(bool(eligible), "dependency cycle")
        for i in eligible:
            pending.remove(i)
            done.add(i)
            order.append(i)
    caps = set(printer.get("verified_capabilities", []))
    buildable = printer.get("candidate_tool_builds", {})
    _require(isinstance(buildable, dict), "invalid tool catalogue")
    _require(request.get("license_state") in ("OPEN", "PAID", "RESTRICTED", "UNKNOWN"),
             "rights state required")
    required = []
    unmet = []
    for feature_id in order:
        f = feature_by_id[feature_id]
        cap = PROCESS_CAPABILITIES[f["operation"]]
        if cap in caps:
            path = "PRESENT_CAPABILITY"
        elif cap in buildable:
            path = "MAKE_TOOL_FIRST_CANDIDATE"
            unmet.append({"feature": feature_id, "missing": cap,
                          "next": "TOOL_BUILD_AND_INDEPENDENT_QUALIFICATION"})
        else:
            path = "EXTERNAL_OR_NEW_CAPABILITY"
            unmet.append({"feature": feature_id, "missing": cap,
                          "next": "QUALIFY_OR_SOURCE_CAPABILITY"})
        rid = f.get("directional_route_id")
        route = routes.get(rid) if rid else None
        if rid is not None and (not isinstance(route, dict) or
                                route.get("production_approved") is not True):
            unmet.append({"feature": feature_id, "missing": rid,
                          "next": "DIRECTIONAL_INTERFACE_COUPON_AND_REVIEW"})
        required.append({
            "feature": feature_id, "operation": f["operation"],
            "after": f.get("after", []), "capability": cap,
            "route": path, "directional_route_id": rid,
            "surface": deepcopy(f.get("surface", {})),
        })
    if shape["state"] == "UNKNOWN":
        unmet.append({"missing": "T173_MESH", "next": "SOURCE_AND_GEOMETRY_ADMISSION"})
    if request["license_state"] in ("UNKNOWN", "RESTRICTED"):
        unmet.append({"missing": "RIGHTS", "next": "OWNER_LICENSE_REVIEW"})
    if request["license_state"] == "PAID" and request.get("price_aud") is None:
        unmet.append({"missing": "PRICE", "next": "PUBLISHER_APPROVAL"})
    if not printer.get("authenticated_machine_profile", False):
        unmet.append({"missing": "MACHINE_HANDSHAKE", "next": "AUTHENTICATE_AND_CALIBRATE"})
    if not printer.get("verified_safety_envelope", False):
        unmet.append({"missing": "SAFETY_ENVELOPE", "next": "ENGINEERING_ASSESSMENT"})
    document = {
        "schema": SCHEMA, "brand": BRAND, "parent": "Cognigrex.cgx",
        "family": "PrintSpace", "object_id": request["object_id"],
        "variant": request.get("variant", "candidate"),
        "geometry": shape, "features": required,
        "owner": request.get("owner"), "agent": request.get("agent"),
        "rights": request["license_state"],
        "price_aud_candidate": request.get("price_aud"),
        "unresolved": unmet,
        "source_state": "REVIEW_ONLY_UNMINTED",
        "production_approved": False, "machine_commands": [],
        "next_execution": "OPERATOR_AND_CAPABILITY_REVIEW",
    }
    return {"plan": document, "representation": binary_ternary_receipt(document)}


def propose_checkpoint(current, update):
    """Assess an in-print DataSpace revision; never accept or execute it.

    Trusted adapters must verify the receipt and hardware state independently.
    The printer must atomically approve a signed, versioned plan at a safe
    boundary; no direct live DataSpace→actuator connection is provided here.
    """
    _require(type(current) is dict and type(update) is dict,
             "invalid checkpoint request")
    reasons = []
    if update.get("object_id") != current.get("object_id"):
        reasons.append("OBJECT_ID_MISMATCH")
    if update.get("expected_state_root") != current.get("state_root"):
        reasons.append("STALE_SOURCE_ROOT")
    if type(update.get("sequence")) is not int or update["sequence"] != current.get("sequence", 0) + 1:
        reasons.append("INVALID_SEQUENCE")
    if update.get("upstream_receipt_state") != "UPSTREAM_VERIFIED":
        reasons.append("RECEIPT_NOT_VERIFIED_BY_TRUSTED_ADAPTER")
    if current.get("checkpoint_state") != "PAUSED_SAFE_BOUNDARY":
        reasons.append("NO_SAFE_CHECKPOINT")
    if update.get("modifies_completed_layers") is not False:
        reasons.append("COMPLETED_LAYERS_IMMUTABLE")
    if update.get("safety_envelope_unchanged") is not True:
        reasons.append("SAFETY_REQUALIFICATION_REQUIRED")
    if update.get("remaining_plan_qualified") is not True:
        reasons.append("REMAINING_PROCESS_UNQUALIFIED")
    if not isinstance(update.get("new_state_root"), str) or len(update["new_state_root"]) != 64:
        reasons.append("NEW_STATE_ROOT_MISSING")
    return {
        "schema": "cgx.printspace.dataspace_revision_proposal.v0.1",
        "object_id": current.get("object_id"),
        "review_state": "HOLD" if reasons else "CANDIDATE_FOR_INDEPENDENT_OPERATOR_AND_MACHINE_REVIEW",
        "reasons": reasons,
        "old_state_root": current.get("state_root"),
        "proposed_state_root": update.get("new_state_root"),
        "can_commit": False, "can_actuate": False,
        "mutated_file": False, "sent_to_printer": False,
        "note": "Upstream receipt marker is not verified cryptographically by this module.",
    }
