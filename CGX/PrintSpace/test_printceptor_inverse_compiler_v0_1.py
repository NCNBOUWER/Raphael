"""Source-only checks of PrintCeptor reverse build data; not physical machine tests."""
import unittest
from printceptor_inverse_compiler import load_graph, evaluate

class InverseTreeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = load_graph()

    def test_node_ids_and_dependency_dag(self):
        self.assertGreaterEqual(len(self.d["components"]), 25)
        allids = {x["id"] for x in self.d["components"]}
        for x in self.d["components"]:
            self.assertTrue(set(x["needs"]).issubset(allids))
            self.assertNotIn(x["id"], x["needs"])
        for goal in ("BB-FINAL", "PC0-SEED", "PC0-4D", "HT-WORKSPACE"):
            out = evaluate(self.d, "K-FDM", goal)
            self.assertEqual(len(out["traversal_dependency_first"]),
                             len(set(out["traversal_dependency_first"])))

    def test_all_alternatives_are_retained(self):
        a = evaluate(self.d, "K-FDM", "BB-FINAL")
        for decision in a["decisions"].values():
            self.assertGreaterEqual(len(decision["all_alternatives"]), 1)
            self.assertEqual(decision["selected"]["physical_qualification"], "NOT_VERIFIED")
            for route in decision["all_alternatives"]:
                self.assertIsNone(route["cost_aud"])

    def test_pen_manual_shell_not_autonomous(self):
        a = evaluate(self.d, "K-PEN", "BB-FINAL", "learning")
        self.assertEqual(a["decisions"]["BB-SHELL"]["selected"]["route"], "HAND")
        self.assertFalse(a["single_sealed_session_qualified"])
        self.assertIn("BB-FINAL", [x["node"] for x in a["candidate_blockers"]])

    def test_fdm_has_print_route_but_cannot_complete_sealed(self):
        a = evaluate(self.d, "K-FDM", "BB-FINAL")
        self.assertEqual(a["decisions"]["BB-SHELL"]["selected"]["route"], "PRINT")
        self.assertIn("BB-FINAL", [x["node"] for x in a["candidate_blockers"]])
        self.assertFalse(a["single_sealed_session_qualified"])

    def test_robot_tools_still_need_qualified_chamber(self):
        a = evaluate(self.d, "K-ROBOT", "BB-FINAL")
        self.assertIn("BB-FINAL", [x["node"] for x in a["candidate_blockers"]])
        self.assertFalse(a["source_qualified"])

    def test_conceptual_pc0_not_promoted(self):
        a = evaluate(self.d, "K-PC0", "BB-FINAL")
        self.assertEqual(a["status"], "CANDIDATE_ONLY_NO_HARDWARE_PROOF")
        self.assertFalse(a["single_sealed_session_qualified"])
        self.assertFalse(a["source_qualified"])

    def test_safety_parts_not_directly_print_eligible(self):
        nodes = {x["id"]: x for x in self.d["components"]}
        for id in ("PC-C0", "PC-CHAMBER", "PC-GAS", "BB-ACT", "BB-ENERGY"):
            self.assertNotIn("PRINT", [o["mode"] for o in nodes[id]["options"]])

    def test_kit_pricing_is_partial_and_aud(self):
        r = evaluate(self.d, "K-FDM", "BB-FINAL")
        self.assertGreater(r["tool_prices_aud_observed_sum_not_total_project_cost"], 250)
        self.assertGreater(len(r["unpriced_kit_dependencies"]), 0)

    def test_first_arm_and_pen_can_be_considered_but_not_qualified(self):
        kit = next(k for k in self.d["starter_kits"] if k["id"] == "K-FDM-PEN-ARM")
        self.assertIn("FDM_POLYMER", kit["capabilities"])
        self.assertNotIn("SERVO_MOTION", kit["capabilities"])
        a = evaluate(self.d, "K-FDM-PEN-ARM", "PC-ARM-PEN-DEMO")
        self.assertIn("PC-ARM-ONE", a["decisions"])
        self.assertIn("PC-PEN-HEAD", a["decisions"])
        self.assertEqual(a["decisions"]["PC-PEN-HEAD"]["selected"]["route"], "SALVAGE")
        self.assertFalse(a["single_sealed_session_qualified"])
        self.assertFalse(a["source_qualified"])

    def test_no_capability_label_blockers_does_not_hide_sourcing_or_safety(self):
        a = evaluate(self.d, "K-FDM-PEN-ARM", "PC-ARM-PEN-DEMO")
        self.assertTrue(a["no_missing_capability_label_does_not_mean_build_ready"])
        self.assertTrue(a["unverified_sourced_parts"])
        self.assertTrue(a["critical_physical_safety_holds"])
        self.assertFalse(a["source_qualified"])
        self.assertFalse(a["single_sealed_session_qualified"])

    def test_donor_hardware_and_non_equivalent_nozzles_are_unverified(self):
        nodes = {x["id"]: x for x in self.d["components"]}
        self.assertEqual(
            set(o["mode"] for o in nodes["PC-GEAR-DONOR"]["options"]), {"BUY", "SALVAGE"}
        )
        self.assertIn("medical", self.d["first_purchase_salvage_lens_v0_2"]["industrial_context_equivalence"]["non_equivalence"].lower())
        self.assertTrue(all(o["cost_aud"] is None for x in nodes.values() for o in x["options"]))

    def test_repair_alternatives_not_deleted(self):
        a = evaluate(self.d, "K-FDM", "BB-TRACKS")
        self.assertEqual(len(a["decisions"]["BB-TRACKS"]["all_alternatives"]), 2)
        b = evaluate(self.d, "K-FDM", "BB-TRACKS", "simple")
        self.assertNotEqual(a["decisions"]["BB-TRACKS"]["selected"]["route"],
                            b["decisions"]["BB-TRACKS"]["selected"]["route"])

if __name__ == "__main__":
    unittest.main()
