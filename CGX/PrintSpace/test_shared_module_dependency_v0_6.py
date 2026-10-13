from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPH = json.loads((ROOT / "SHARED_MODULE_DEPENDENCY_GRAPH_v0_6.json").read_text(encoding="utf-8"))
PACKETS = json.loads((ROOT / "DEMONSTRATOR_GATE_PACKETS_v0_6.json").read_text(encoding="utf-8"))
SHARED = json.loads((ROOT / "CROSS_GREX_SHARED_PRIMITIVES_v0_5.json").read_text(encoding="utf-8"))


class SharedModuleDependencyTests(unittest.TestCase):
    def test_graph_covers_all_primitives_and_products(self):
        self.assertEqual(GRAPH["primitive_count"], 70)
        self.assertEqual(GRAPH["product_count"], 80)
        self.assertEqual(len(GRAPH["nodes"]), 70)
        self.assertGreater(GRAPH["edge_count"], 0)
        self.assertEqual(GRAPH["edge_count"], len(GRAPH["edges"]))

    def test_reuse_counts_match_registered_source(self):
        registered = {row["technology_id"]: row["product_reuse_count"] for row in SHARED["records"]}
        derived = {row["technology_id"]: row["product_reuse_count"] for row in GRAPH["nodes"]}
        self.assertEqual(derived, registered)

    def test_graph_is_fail_closed_on_physical_equivalence(self):
        self.assertTrue(all(not row["physical_qualified"] for row in GRAPH["nodes"]))
        self.assertTrue(
            all(not edge["physical_interchangeability_verified"] for edge in GRAPH["edges"])
        )

    def test_target_demonstrators_are_exact_and_unreleased(self):
        by_id = {row["product_id"]: row for row in PACKETS["packets"]}
        self.assertEqual(set(by_id), {"FO-01", "FE-04"})
        self.assertEqual(len(by_id["FO-01"]["stages"]), 8)
        self.assertEqual(len(by_id["FE-04"]["stages"]), 6)
        self.assertEqual(len(by_id["FO-01"]["gap_tickets"]), 4)
        self.assertEqual(len(by_id["FE-04"]["gap_tickets"]), 3)
        for packet in by_id.values():
            self.assertTrue(packet["gates"]["all_stages_design_only"])
            self.assertFalse(packet["gates"]["physical_recipe_verified"])
            self.assertFalse(packet["gates"]["physical_tested"])
            self.assertFalse(packet["gates"]["production_approved"])
            self.assertEqual(packet["selection_state"]["exact_supplier_parts"], [])
            self.assertEqual(packet["selection_state"]["measured_property_receipts"], [])

    def test_cross_demonstrator_shared_primitives_are_bounded(self):
        cross = PACKETS["cross_demonstrator_reuse"]
        self.assertEqual(cross["shared_technology_ids"], ["PT-018", "PT-043"])
        self.assertFalse(cross["physical_interchangeability_verified"])


if __name__ == "__main__":
    unittest.main()
