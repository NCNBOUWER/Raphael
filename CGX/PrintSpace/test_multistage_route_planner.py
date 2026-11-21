"""Stdlib tests for the CGX-F4D candidate-only multi-stage planner."""
import unittest
from pathlib import Path
from multistage_route_planner import read_json, validate_catalog, evaluate_contract, enumerate_orders

HERE = Path(__file__).resolve().parent
CATALOG = read_json(HERE / "PAIRWISE_SEQUENCE_ROUTES_v0_1.json")
CASES = {c["id"]: c for c in read_json(HERE / "MULTISTAGE_ROUTE_TEST_CASES_v0_2.json")["cases"]}


class MultiStageRouteTests(unittest.TestCase):
    def test_directional_coverage(self):
        families, pairs = validate_catalog(CATALOG)
        self.assertEqual((len(families), len(pairs)), (14, 196))
        self.assertIn(("TP", "MT"), pairs)
        self.assertIn(("MT", "TP"), pairs)

    def test_encapsulation_before_atmosphere_refill(self):
        result = evaluate_contract(CATALOG, CASES["VACUUM_CONDUCTOR_SEAL_REFILL"])
        self.assertEqual(result["best_candidates"][0]["status"], "CANDIDATE_ONLY")
        order = result["best_candidates"][0]["order"]
        self.assertLess(order.index("seal"), order.index("refill"))
        self.assertLess(order.index("inspect_seal"), order.index("refill"))
        self.assertFalse(result["production_approved"])

    def test_cumulative_damage_rejects_route(self):
        result = evaluate_contract(CATALOG, CASES["THERMAL_POSTPROCESS_UNSAFE"])
        self.assertEqual(result["best_candidates"][0]["status"], "REJECT_CANDIDATE")
        self.assertIn("exceeds budget", " ".join(result["best_candidates"][0]["violations"]))

    def test_absent_dose_is_not_assumed_zero(self):
        result = evaluate_contract(CATALOG, CASES["MISSING_EXPOSURE_REQUIRES_DATA"])
        self.assertEqual(result["best_candidates"][0]["status"], "NEEDS_EVIDENCE")
        self.assertIn("missing demo_damage_index", " ".join(result["best_candidates"][0]["unknowns"]))

    def test_robot_hybrid_route_no_production_approval(self):
        result = evaluate_contract(CATALOG, CASES["BUTTER_BOT_HYBRID_SEQUENCE"])
        self.assertEqual(result["best_candidates"][0]["status"], "CANDIDATE_ONLY")
        self.assertFalse(result["physical_tested"])

    def test_cycle_is_rejected(self):
        stages = {"a":{"after":["b"]},"b":{"after":["a"]}}
        with self.assertRaises(ValueError):
            enumerate_orders(stages)

    def test_gate_sequence_is_required(self):
        import copy
        case = copy.deepcopy(CASES["VACUUM_CONDUCTOR_SEAL_REFILL"])
        case["stages"] = [s for s in case["stages"] if s["id"] != "inspect_seal"]
        case["stages"][-1]["after"] = ["seal"]
        result = evaluate_contract(CATALOG, case)
        self.assertEqual(result["best_candidates"][0]["status"], "REJECT_CANDIDATE")


if __name__ == "__main__":
    unittest.main()
