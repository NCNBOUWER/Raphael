"""Static contract checks for the PrintCeptor consumer hydration projection.

These checks validate review-only fixture invariants, NOT runtime hydration,
machine authority, CAD, material physics, access control or physical tests.
"""
import json
import unittest
from pathlib import Path

POLICY = json.loads(
    (Path(__file__).parent / "PRINTCEPTOR_CGX_FRONTIER_HYDRATION_PROJECTION_v0_1.json").read_text(encoding="utf-8")
)


class PrintCeptorFrontierProjectionTests(unittest.TestCase):
    def test_consumer_only_no_root_promotion(self):
        self.assertIn("NON_AUTHORITATIVE", POLICY["state"])
        self.assertIn("no CGX root mutation", POLICY["namespace_scope"])
        self.assertIn("without creating a new cgx schema", POLICY["purpose"].lower())

    def test_hydration_profiles_distinct_and_bounded(self):
        profiles = POLICY["query_contract"]["profiles"]
        names = [p["id"] for p in profiles]
        self.assertEqual(names, POLICY["query_contract"]["profile_order"])
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(POLICY["query_contract"]["default_profile"], "SPARSE")
        for profile in profiles:
            self.assertTrue(profile["forbidden"], profile["id"])
            self.assertIn("primary_view", profile)

    def test_cases_select_declared_profiles(self):
        ids = {p["id"] for p in POLICY["query_contract"]["profiles"]}
        cases = POLICY["task_cases"]
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        for case in cases:
            self.assertIn(case["profile"], ids)
            self.assertTrue(case["owner_lanes"], case["id"])
            self.assertTrue(case["excluded_by_default"], case["id"])

    def test_child_printer_distinct_from_bay(self):
        self.assertIn("not itself", POLICY["identities"]["bay"])
        self.assertIn("child Object_ID", POLICY["identities"]["child_printer"])

    def test_memory_separation(self):
        memory = POLICY["memory_classes"]
        self.assertEqual(set(memory), {"semantic", "episodic", "temporary", "private", "co_running_chat"})
        self.assertIn("not canonical", memory["co_running_chat"])
        self.assertIn("not auto-imported", memory["private"])

    def test_owner_frontier_still_open_and_source_freshness_required(self):
        frontier = POLICY["frontier_records"]
        self.assertEqual(len(frontier), len({f["id"] for f in frontier}))
        self.assertGreaterEqual(len(frontier), 6)
        self.assertEqual(POLICY["state_observations"]["root_pointer_state"], "STALE_POINTER_OBSERVED_NOT_CORRECTED")
        self.assertTrue(POLICY["state_observations"]["provider_snapshot_only"])
        self.assertIn("reread", POLICY["state_observations"]["refresh_rule"].lower())
        for gate in frontier:
            self.assertNotEqual(gate["state"], "CLOSED")
            self.assertIn("owner", gate)
            self.assertIn("acceptance", gate)

    def test_source_identity_and_evidence_not_unconditionally_promoted(self):
        self.assertIn("PMX", POLICY["source_refs"]["post_mix"])
        self.assertIn("PR6", POLICY["source_refs"]["printspace"])
        self.assertIn("411", POLICY["source_refs"]["cgx_atlas"])
        self.assertIn("Only proven/readback/committed", POLICY["query_contract"]["evidence_rules"])
        self.assertIn("independent owner review", POLICY["promotion"])


if __name__ == "__main__":
    unittest.main()
