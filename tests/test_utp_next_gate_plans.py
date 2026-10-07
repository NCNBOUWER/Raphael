import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "Raphael_Packages" / "Universal_Tech_Printer"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class UTPNextGatePlanTests(unittest.TestCase):
    def test_sh01_plan_keeps_execution_open(self):
        d = load("build_packets/sh01_cgx_identity_coupon_plan_v0_1.json")
        self.assertIn("NOT_RUN", d["state"])
        self.assertEqual(set(d["three_planes"]), {"filespace", "dataspace", "solid_state"})
        self.assertIn("READ_IDENTITY", d["process_sequence"])
        self.assertIn("READBACK_RECEIPT", d["process_sequence"])
        self.assertEqual(d["selection"]["selected_route_id"], "SH01-ID-A")
        self.assertIn("NOT_EXECUTED", d["selection"]["status"])
        self.assertIn("energized electrical measurement", d["selection"]["measurement_schema"]["excluded_for_first_route"])

    def test_printer_mu_dag_covers_declared_basis(self):
        d = load("printer_mu_dependency_dag_v0_1.json")
        mapped = set()
        for node in d["nodes"]:
            mapped.update(node["function_basis"])
            self.assertEqual(node["evidence_state"], "ARCHITECTURE")
            self.assertEqual(node["selection_state"], "UNSELECTED")
            self.assertTrue(node["qualification_limit"])
        self.assertEqual(set(d["universal_function_basis"]) - mapped, set())

    def test_child_commissioning_gate_requires_parent_evidence(self):
        d = load("printer_mu_dependency_dag_v0_1.json")
        gate = " ".join(d["dependency_closure"]["child_commissioning_gate"]).lower()
        self.assertIn("printer-1 physically exists", gate)
        self.assertIn("calibrated", gate)
        self.assertIn("cross-calibrated", gate)

if __name__ == "__main__":
    unittest.main()
