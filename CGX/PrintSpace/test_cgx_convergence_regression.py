"""Regression suite for a nonexecuting UniSpace/PrintSpace convergence candidate."""
from __future__ import annotations
import json
import os
import unittest
from pathlib import Path

from cgx_printspace_shell import (
    canonical_binary, bytes_to_ternary, ternary_to_bytes,
    binary_ternary_receipt, resolve_t173, compile_plan, propose_checkpoint,
)
from cgx_unispace_link_policy import evaluate_handover
from cgx_printspace_t173_projection import load_t173_review_source

HERE = Path(__file__).resolve().parent


def machine():
    return {
        "machine_node_id": "pc0-node",
        "machine_object_id": "CGX-DEVICE-SYNTHETIC-PC0",
        "state_root": "a" * 64, "dbr_root": "b" * 64,
        "lease_id": "synthetic-lease",
        "lease_epoch": 3,
        "lease_valid_until_ms": 20000,
        "allowed_peers": {
            "companion-node": {"peer_key_id": "test-key",
                               "last_accepted_counter": 4}
        },
        "job_requires_remote_compute": True,
    }


def link(protocol="wifi_lan"):
    return {
        "peer_node_id": "companion-node", "peer_key_id": "test-key",
        "transport": protocol, "observed_ms": 9500,
        "readback_counter": 5, "pre_paired": True,
        "authenticated": True, "capability_readback_verified": True,
        "protocol_compatible": True, "channel_ready": True,
        "lease_epoch": 3,
    }


def mesh_source():
    return {"1": {"role_id": "RAP-SLOT-001", "mesh_sha256": "1" * 64,
                  "evidence": "REFERENCE_EUCLIDEAN",
                  "unit": "normalised Euclidean reference"}}


def pet_request():
    return {
        "object_id": "CGX-SYNTHETIC-ACHILLES-LAB-PET",
        "owner": "EXAMPLE_ONLY", "agent": "Achilles",
        "t173_slot": 1, "license_state": "OPEN",
        "features": [
            {"id": "shell", "operation": "STRUCTURE"},
            {"id": "texture", "operation": "SURFACE_TEXTURE", "after": ["shell"],
             "surface": {"topology": "roughened-candidate",
                         "requires_roughness_metrology": True}},
            {"id": "sensor", "operation": "SENSOR", "after": ["shell"]},
            {"id": "seal", "operation": "ENCAPSULATE",
             "after": ["sensor", "texture"]},
            {"id": "inspection", "operation": "VALIDATE", "after": ["seal"]},
        ],
    }


class ConvergenceTests(unittest.TestCase):
    def test_binary_to_ternary_lossless_all_bytes(self):
        raw = bytes(range(256))
        trits = bytes_to_ternary(raw)
        self.assertEqual(len(trits), 1536)
        self.assertEqual(ternary_to_bytes(trits), raw)
        self.assertEqual(ternary_to_bytes(bytes_to_ternary(b"")), b"")
        with self.assertRaises(ValueError):
            ternary_to_bytes([0, 1, 2])
        with self.assertRaises(ValueError):
            ternary_to_bytes([True, 0, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            ternary_to_bytes([2] * 6)
        # Ternary radix conversion is not storage compression.
        r = binary_ternary_receipt({"test": "UTF-8 α", "status": None})
        self.assertEqual(r["roundtrip"], "PASS")
        self.assertEqual(r["ternary_digits"], 6 * len(canonical_binary({"test": "UTF-8 α", "status": None})))
        self.assertIsNone(r["measured_savings"])

    def test_t173_reserved_and_unknown(self):
        for value in (0, 174, -1, True, 1.0, "1"):
            with self.assertRaises(ValueError):
                resolve_t173(value, mesh_source())
        result = resolve_t173(173, mesh_source())
        self.assertEqual(result["state"], "UNKNOWN")
        self.assertEqual(result["reason"], "SOURCE_SLOT_UNRESOLVED")
        self.assertFalse(resolve_t173(1, mesh_source())["physical_qualified"])

    def test_explicit_alias_and_missing_target(self):
        source = mesh_source()
        source["14"] = {"alias_of": 1}
        self.assertEqual(resolve_t173(14, source)["mesh_role"], 1)
        with self.assertRaises(ValueError):
            resolve_t173(14, {"14": {"alias_of": 58}})

    def test_dependency_order_surface_and_capability_delta(self):
        printer = {
            "verified_capabilities": ["polymer_deposition", "metrology"],
            "candidate_tool_builds": {
                "microtexture_tool": {"requires": ["polymer_deposition"]},
                "sensor_integration": {"requires": ["microtexture_tool"]},
            },
            "authenticated_machine_profile": False,
            "verified_safety_envelope": False,
        }
        result = compile_plan(pet_request(), mesh_source(), printer, {})
        plan = result["plan"]
        order = [f["feature"] for f in plan["features"]]
        self.assertLess(order.index("shell"), order.index("texture"))
        self.assertLess(order.index("texture"), order.index("seal"))
        self.assertLess(order.index("sensor"), order.index("seal"))
        self.assertIn("MAKE_TOOL_FIRST_CANDIDATE",
                      {x["route"] for x in plan["features"]})
        self.assertIn("EXTERNAL_OR_NEW_CAPABILITY",
                      {x["route"] for x in plan["features"]})
        self.assertIn("MACHINE_HANDSHAKE", {u["missing"] for u in plan["unresolved"]})
        self.assertIn("SAFETY_ENVELOPE", {u["missing"] for u in plan["unresolved"]})
        self.assertFalse(plan["production_approved"])
        self.assertEqual(plan["machine_commands"], [])
        self.assertEqual(result["representation"]["roundtrip"], "PASS")

    def test_dependency_cycle_rejected(self):
        req = pet_request()
        req["features"][0]["after"] = ["inspection"]
        with self.assertRaisesRegex(ValueError, "cycle"):
            compile_plan(req, mesh_source(), {}, {})

    def test_rights_and_directionality_not_auto_promoted(self):
        req = pet_request()
        req["license_state"] = "PAID"
        req["features"][1]["directional_route_id"] = "A_TO_B"
        res = compile_plan(req, mesh_source(), {
            "verified_capabilities": ["polymer_deposition"],
            "authenticated_machine_profile": True,
            "verified_safety_envelope": True,
        }, {"B_TO_A": {"production_approved": True}})
        missing = {u["missing"] for u in res["plan"]["unresolved"]}
        self.assertIn("A_TO_B", missing)
        self.assertIn("PRICE", missing)
        self.assertFalse(res["plan"]["production_approved"])

    def test_checkpoint_stays_nonexecuting(self):
        current = {"object_id": "part", "state_root": "a" * 64,
                   "sequence": 9, "checkpoint_state": "PAUSED_SAFE_BOUNDARY"}
        update = {"object_id": "part", "expected_state_root": "a" * 64,
                  "new_state_root": "b" * 64, "sequence": 10,
                  "upstream_receipt_state": "UPSTREAM_VERIFIED",
                  "modifies_completed_layers": False,
                  "safety_envelope_unchanged": True,
                  "remaining_plan_qualified": True}
        proposal = propose_checkpoint(current, update)
        self.assertEqual(proposal["review_state"], "CANDIDATE_FOR_INDEPENDENT_OPERATOR_AND_MACHINE_REVIEW")
        self.assertFalse(proposal["can_commit"])
        self.assertFalse(proposal["can_actuate"])
        current["checkpoint_state"] = "DEPOSITING"
        self.assertIn("NO_SAFE_CHECKPOINT", propose_checkpoint(current, update)["reasons"])
        update["sequence"] = 9
        self.assertIn("INVALID_SEQUENCE", propose_checkpoint(current, update)["reasons"])

    def test_always_no_canonical_source_promotion(self):
        req = pet_request()
        req["license_state"] = "UNKNOWN"
        plan = compile_plan(req, {}, {}, {})["plan"]
        self.assertEqual(plan["geometry"]["state"], "UNKNOWN")
        self.assertIn("RIGHTS", {item["missing"] for item in plan["unresolved"]})
        self.assertIn("T173_MESH", {item["missing"] for item in plan["unresolved"]})


class RollingTransportTests(unittest.TestCase):
    def test_authenticated_prefers_lan_but_can_select_prepaired_bluetooth(self):
        wifi = link("wifi_lan")
        bt = link("bluetooth_classic")
        result = evaluate_handover(machine(), [bt, wifi], 10000)
        self.assertEqual(result["preferred_link"]["transport"], "wifi_lan")
        self.assertFalse(result["transport_switched"])
        bt_result = evaluate_handover(machine(), [bt], 10000)
        self.assertEqual(bt_result["preferred_link"]["transport"], "bluetooth_classic")
        self.assertEqual(bt_result["preferred_link"]["candidate_role"],
                         "CONTROL_AND_SMALL_RECEIPT_ONLY")
        self.assertFalse(bt_result["lease_transferred"])

    def test_unpaired_or_stale_or_replay_never_selected(self):
        unpaired = link("bluetooth_classic")
        unpaired["pre_paired"] = False
        stale = link("wifi_lan")
        stale["observed_ms"] = 0
        replay = link("ble_gatt")
        replay["readback_counter"] = 4
        out = evaluate_handover(machine(), [unpaired, stale, replay], 10000)
        self.assertIsNone(out["preferred_link"])
        codes = {r for item in out["rejected_links"] for r in item["reasons"]}
        self.assertIn("HANDSHAKE_NOT_AUTHENTICATED", codes)
        self.assertIn("LINK_STALE", codes)
        self.assertIn("REPLAY_OR_MISSING_READBACK", codes)
        self.assertEqual(out["operational_recommendation"], "PAUSE_AT_SAFE_BOUNDARY_AND_HOLD")
        self.assertFalse(out["new_peer_paired"])

    def test_offline_safe_pause_and_bounded_local_mode(self):
        self.assertEqual(evaluate_handover(machine(), [], 10000)["operational_recommendation"],
                         "PAUSE_AT_SAFE_BOUNDARY_AND_HOLD")
        m = machine()
        m.update({"job_requires_remote_compute": False,
                  "local_signed_plan_loaded": True,
                  "local_safety_interlocks_verified": True,
                  "local_controller_verified": True,
                  "local_execution_lease_scoped": True})
        result = evaluate_handover(m, [], 10000)
        self.assertEqual(result["operational_recommendation"],
                         "LOCAL_AUTONOMY_REQUIRES_SEPARATE_CONTROLLER_DECISION")
        self.assertFalse(result["machine_actuated"])

    def test_expired_lease_rejects_transport_and_autonomy(self):
        m = machine()
        m["lease_valid_until_ms"] = 10000
        self.assertIsNone(evaluate_handover(m, [link()], 10000)["preferred_link"])


class SourceBoundReviewTests(unittest.TestCase):
    def test_printspace_materials_are_unapproved(self):
        directory = HERE
        pair = json.loads((directory / "PAIRWISE_SEQUENCE_ROUTES_v0_1.json").read_text())
        material = json.loads((directory / "MATERIAL_DIRECTIONAL_ROUTES_v0_3.json").read_text())
        geometry = json.loads((directory / "PARAMETRIC_GEOMETRY_FUNCTION_SEEDS_v0_3.json").read_text())
        self.assertEqual(len(pair["families"]), 14)
        self.assertEqual(len(pair["pairs"]), 196)
        self.assertEqual(len(material["routes"]), 72)
        self.assertEqual(len(geometry["geometries"]), 30)
        self.assertTrue(all(x["production_approved"] is False for x in material["routes"]))
        self.assertTrue(all(x["machine_ready"] is False for x in geometry["geometries"]))

    @unittest.skipUnless(os.environ.get("CGX_GEOMETRY_173_PATH"), "PR7 checkout not supplied")
    def test_pinned_raphael_geometry_coverage_and_unresolved(self):
        data = load_t173_review_source(os.environ["CGX_GEOMETRY_173_PATH"])
        self.assertEqual(data["source_roles"], 173)
        self.assertEqual(data["mesh_reference_records"], 131)
        self.assertEqual(data["shared_aliases"], 9)
        self.assertEqual(data["mesh_backed_roles"], 140)
        self.assertEqual(len(data["unresolved_slots"]), 33)
        self.assertEqual(data["unresolved_slots"][:7], [131, 132, 133, 134, 135, 136, 137])
        self.assertIn(173, data["unresolved_slots"])
        self.assertEqual(data["physical_qualified"], 0)
        projection = data["projection"]
        self.assertEqual(resolve_t173(14, projection)["mesh_role"], 58)
        self.assertEqual(resolve_t173(1, projection)["state"], "CANDIDATE")
        self.assertEqual(resolve_t173(173, projection)["state"], "UNKNOWN")
        self.assertNotIn("174", projection)


if __name__ == "__main__":
    unittest.main()
