"""UniSpace DataSpace rolling handover policy, source-only, never live transport.

This projection consumes capability/authentication receipts from a registered
transport adapter. It does not discover, pair, open a radio, transfer a lease,
operate a printer, or establish cryptographic trust by itself.
"""
from __future__ import annotations
import hashlib
import json

SCHEMA = "cgx.unispace.dataspace.rolling_link.review.v0.1"
TRANSPORTS = ("ethernet", "wifi_lan", "wifi_direct", "bluetooth_classic", "ble_gatt")
LOW_BANDWIDTH = frozenset(("bluetooth_classic", "ble_gatt"))
MAX_OBSERVATION_AGE_MS = 5000


def _require(value, message):
    if not value:
        raise ValueError(message)


def _integer(value):
    return type(value) is int and value >= 0


def _hash(payload):
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def evaluate_handover(machine, observed_links, now_ms):
    """Return a nonexecuting link recommendation and explicit rejection reasons.

    All timestamps are assumed from an adapter-provided *single monotonic clock*.
    A link's authentication/readback booleans are assertions by a trusted adapter,
    not evidence this module itself authenticated a device.
    """
    _require(type(machine) is dict and type(observed_links) is list,
             "machine and link inventory required")
    _require(_integer(now_ms), "monotonic now_ms required")
    for field in ("machine_node_id", "machine_object_id", "state_root",
                  "dbr_root", "lease_id"):
        _require(type(machine.get(field)) is str and machine[field],
                 "missing " + field)
    _require(_integer(machine.get("lease_epoch")) and
             _integer(machine.get("lease_valid_until_ms")),
             "invalid lease timing")
    peers = machine.get("allowed_peers")
    _require(type(peers) is dict, "allowed peer registry required")
    _require(len(observed_links) <= 64, "unbounded link input")
    candidates, rejected = [], []
    unique = set()
    for link in observed_links:
        _require(type(link) is dict, "invalid link entry")
        pid = link.get("peer_node_id")
        proto = link.get("transport")
        ident = (pid, proto)
        _require(ident not in unique, "duplicate peer/transport observations")
        unique.add(ident)
        problems = []
        profile = peers.get(pid)
        if not isinstance(pid, str) or not isinstance(profile, dict):
            problems.append("PEER_NOT_ALLOWLISTED")
        if pid == machine["machine_node_id"]:
            problems.append("SELF_LINK")
        if proto not in TRANSPORTS:
            problems.append("TRANSPORT_UNSUPPORTED")
        last = link.get("observed_ms")
        if not _integer(last) or last > now_ms or now_ms - last > MAX_OBSERVATION_AGE_MS:
            problems.append("LINK_STALE")
        seq = link.get("readback_counter")
        if not _integer(seq) or (isinstance(profile, dict) and
            seq <= profile.get("last_accepted_counter", -1)):
            problems.append("REPLAY_OR_MISSING_READBACK")
        if (link.get("pre_paired") is not True or
            link.get("authenticated") is not True or
            link.get("capability_readback_verified") is not True):
            problems.append("HANDSHAKE_NOT_AUTHENTICATED")
        if isinstance(profile, dict) and link.get("peer_key_id") != profile.get("peer_key_id"):
            problems.append("PEER_KEY_MISMATCH")
        if link.get("protocol_compatible") is not True:
            problems.append("PROTOCOL_INCOMPATIBLE")
        if link.get("channel_ready") is not True:
            problems.append("CHANNEL_NOT_READY")
        if link.get("lease_epoch") != machine["lease_epoch"]:
            problems.append("LEASE_EPOCH_MISMATCH")
        if machine["lease_valid_until_ms"] <= now_ms:
            problems.append("LEASE_EXPIRED")
        if problems:
            rejected.append({"peer_node_id": pid, "transport": proto, "reasons": problems})
            continue
        candidates.append({
            "peer_node_id": pid,
            "transport": proto,
            "readback_counter": seq,
            "candidate_role": "CONTROL_AND_SMALL_RECEIPT_ONLY" if proto in LOW_BANDWIDTH
                              else "BOUNDED_DATA_AND_RECEIPT",
            "data_capacity_unverified": True,
            "priority": TRANSPORTS.index(proto),
        })
    candidates.sort(key=lambda x: (x["priority"], x["peer_node_id"]))
    chosen = dict(candidates[0]) if candidates else None
    if chosen:
        chosen.pop("priority", None)
    for c in candidates:
        c.pop("priority", None)
    remote_required = machine.get("job_requires_remote_compute", True) is True
    local_plan = all(machine.get(k) is True for k in (
        "local_signed_plan_loaded", "local_safety_interlocks_verified",
        "local_controller_verified", "local_execution_lease_scoped"))
    if chosen is not None:
        operation = "LINK_HANDOVER_CANDIDATE_ONLY"
    elif local_plan and not remote_required and machine["lease_valid_until_ms"] > now_ms:
        operation = "LOCAL_AUTONOMY_REQUIRES_SEPARATE_CONTROLLER_DECISION"
    else:
        operation = "PAUSE_AT_SAFE_BOUNDARY_AND_HOLD"
    return {
        "schema": SCHEMA, "umbrella": "UniSpace",
        "subsystem": "DataSpace", "machine_object_id": machine["machine_object_id"],
        "machine_node_id": machine["machine_node_id"], "state_root": machine["state_root"],
        "dbr_root": machine["dbr_root"], "lease_id": machine["lease_id"],
        "lease_epoch": machine["lease_epoch"], "preferred_link": chosen,
        "candidate_links": candidates, "rejected_links": rejected,
        "operational_recommendation": operation,
        "link_policy_sha256": _hash({"machine": machine, "links": observed_links,
                                     "now_ms": now_ms}),
        "transport_switched": False, "lease_transferred": False,
        "machine_actuated": False, "new_peer_paired": False,
        "boundary": "Trusted peer and signed lease verification belong to existing CGX runtime adapters",
    }
