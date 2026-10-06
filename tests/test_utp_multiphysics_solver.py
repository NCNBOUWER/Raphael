import math
import unittest

from Raphael_Packages.Universal_Tech_Printer.utp_multiphysics_solver import (
    BuildNode,
    boltzmann_weights,
    compare_traditional_hybrid,
    dimensionless_groups,
    environment_supports,
    interaction_order_gate,
    pair_reconstruction,
    select_kernels,
)


class UTPMultiphysicsTests(unittest.TestCase):
    def test_boltzmann_weights_close(self):
        p = boltzmann_weights({"a": 0.0, "b": 1000.0}, 300.0)
        self.assertTrue(math.isclose(sum(p.values()), 1.0, abs_tol=1e-12))
        self.assertGreater(p["a"], p["b"])

    def test_pair_gate_promotes_only_on_residual(self):
        pred = pair_reconstruction([1.0, 1.0], [[0.1, 0.0]], [[0.0, 0.2]])
        self.assertEqual(interaction_order_gate(pred, pred, 1e-9), "PASS_PAIR")
        self.assertEqual(interaction_order_gate([2.0, 2.0], pred, 0.1), "PROMOTE_HIGHER_ORDER")

    def test_dimensionless_groups(self):
        g = dimensionless_groups(
            rho=1000.0, velocity=1.0, length=0.01, viscosity=0.001,
            diffusivity=1e-9, surface_tension=0.07, mean_free_path=1e-7
        )
        self.assertTrue(math.isclose(g["Re"], 10000.0))
        self.assertTrue(g["Pe"] > 0)
        self.assertTrue(g["Kn"] > 0)

    def test_kernel_selection(self):
        k = select_kernels(["plasma", "raphael_compare"])
        self.assertIn("K-PLASMA", k)
        self.assertIn("K-RAPHAEL-OBW", k)
        self.assertIn("K-MAXWELL", k)

    def test_open_environment_is_limited_not_empty(self):
        self.assertTrue(environment_supports("ENV-0", ["structural", "inspection"]))
        self.assertFalse(environment_supports("ENV-0", ["microplasma"]))

    def test_recursive_ir(self):
        child = BuildNode("pixel", "micro", "ENV-2", ["plasma", "electric"])
        root = BuildNode("screen", "meso", "ENV-1", ["mechanical"], [child])
        m = root.compile_kernel_map()
        self.assertIn("K-MECH", m["screen"])
        self.assertIn("K-PLASMA", m["pixel"])
        self.assertEqual(root.all_ids(), ["screen", "pixel"])

    def test_hybrid_comparator_does_not_make_universal_score(self):
        out = compare_traditional_hybrid(
            {"parts": 10, "repairability": 2},
            {"parts": 5, "repairability": 3},
            lower_is_better=["parts"],
        )
        self.assertTrue(math.isclose(out["parts"], 0.5))
        self.assertTrue(math.isclose(out["repairability"], 0.5))


if __name__ == "__main__":
    unittest.main()
