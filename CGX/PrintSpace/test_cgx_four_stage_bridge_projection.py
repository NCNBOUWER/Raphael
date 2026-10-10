"""Static checks for the non-authoritative CGX File/Data/Print/Type I bridge.
No runtime, network, UI deployment, manufacturing or legal release is exercised.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

RECORD = json.loads(
    (Path(__file__).parent / "CGX_FILESPACE_DATASPACE_PRINTSPACE_TYPE1_BRIDGE_2026-10-10.json")
    .read_text(encoding="utf-8")
)


class FourStageIntegrationProjectionTests(unittest.TestCase):
    def test_noncanonical_and_distinct_stages(self):
        self.assertIn("REVIEW_ONLY", RECORD["state"])
        self.assertTrue(RECORD["execution_contract"]["no_new_master"])
        stages = RECORD["vision"]
        self.assertEqual([v["id"] for v in stages], ["S1", "S2", "S3", "S4"])
        self.assertTrue(all(v["outcome"].strip() for v in stages))

    def test_interface_integrity_and_gates(self):
        records = RECORD["interfaces"]
        ids = [v["id"] for v in records]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(records), 14)
        for edge in records:
            with self.subTest(edge=edge["id"]):
                for key in ("edge", "owner", "state", "missing", "mutation", "proof", "parent_gate"):
                    self.assertTrue(edge[key].strip(), key)
                self.assertIn("G", edge["parent_gate"])

    def test_one_owner_not_separate_families_stores(self):
        families = RECORD["families"]
        ids = [f["id"] for f in families]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({"Cognigrex", "Romer-Grex", "Eco-Grex", "EMASSC", "LightSpeed", "Achilles P.A.", "CCC/CYC"}.issubset(set(ids)))
        self.assertTrue(all(f["authority"] for f in families))

    def test_inputs_and_minimum_hydration_profiles(self):
        ec = RECORD["execution_contract"]
        self.assertEqual(ec["hydrate_levels"], ["SHELL", "SPARSE", "PROJECT_DEEP", "CROSS_DOMAIN_BOUNDED"])
        self.assertIn("lease", ec["input"])
        self.assertIn("Owner/operator approve", " ".join(ec["path"]))
        self.assertIn("Read back", " ".join(ec["path"]))
        for example in RECORD["example_work"].values():
            self.assertIn(example["profile"], ec["hydrate_levels"])

    def test_compatible_native_providers_and_no_unsupported_release(self):
        providers = [p["provider"] for p in RECORD["native_suites"]]
        self.assertTrue(any("Windows" in p for p in providers))
        self.assertTrue(any("GitHub" in p for p in providers))
        self.assertTrue(any("Google Drive" in p for p in providers))
        self.assertIn("Documents excluded", RECORD["native_suites"][0]["gate"])
        self.assertIn("no new", RECORD["status_note"].lower())
        self.assertIn("No public release", RECORD["safety_and_release"]["approval"])

    def test_physical_evidence_and_live_currentness_are_not_promoted(self):
        recorded = RECORD["source_snapshots"]
        self.assertNotEqual(recorded["lightspeed_host_canonical"], recorded["lightspeed_github_main"])
        self.assertIn("one fast-forward commit", recorded["lightspeed_provider_delta"])
        self.assertIn("16 x 3840", recorded["private_review_artwork"])
        self.assertIn("simulation != empirical test", RECORD["execution_contract"]["no_evidence_escalation"])
        self.assertIn("current", RECORD["safety_and_release"]["always_current"])


if __name__ == "__main__":
    unittest.main()
