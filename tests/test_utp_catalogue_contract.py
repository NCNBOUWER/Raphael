import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "Raphael_Packages" / "Universal_Tech_Printer"

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class UTPCatalogueContractTests(unittest.TestCase):
    def test_catalogue_has_broad_unique_coverage(self):
        c = load("printable_technology_catalogue_v0_1.json")
        items = c["items"]
        self.assertGreaterEqual(len(items), 60)
        ids = [x["id"] for x in items]
        self.assertEqual(len(ids), len(set(ids)))
        allowed_evidence = {"E0","E1","E2","E3","E4","E5"}
        for x in items:
            for key in ("category","name","functions","ops","feeds","env","geometry","diy","horizons","evidence","status","links"):
                self.assertIn(key, x, x["id"])
            self.assertIn(x["evidence"], allowed_evidence)
            self.assertTrue(x["functions"])
            self.assertTrue(x["ops"])
            self.assertTrue(x["env"])

    def test_required_universal_functions_are_represented(self):
        c = load("printable_technology_catalogue_v0_1.json")
        names = " ".join(x["name"].lower() for x in c["items"])
        for term in (
            "conductor","capacitor","inductor","battery","rgb","sensor",
            "actuator","antenna","transistor","printer","pressure"
        ):
            self.assertIn(term, names)

    def test_cgx_identity_is_federated_not_master_replacement(self):
        d = load("cgx_printer_identity_v0_1.json")
        self.assertIn("cgx:root:cognigrex", d["semantic_model"]["parents"])
        self.assertIn("cgx:domain:romer", d["semantic_model"]["parents"])
        self.assertIn("not a replacement master", d["semantic_model"]["rule"])
        self.assertEqual([x["id"] for x in d["compute_layers"]], ["C0-RT","C1-EDGE","C2-NETWORK"])
        self.assertIn("must remain locally executable", d["compute_layers"][0]["constraint"])

    def test_phone_equivalence_does_not_claim_soc_parity(self):
        d = load("cgx_printer_identity_v0_1.json")
        b = d["smartphone_equivalence_boundary"]
        self.assertIn("Functional equivalence", b["statement"])
        self.assertIn("not implied", b["constraint"])

    def test_horizons_expose_local_only_dependency(self):
        d = load("local_horizon_self_organization_v0_1.json")
        ids = [x["id"] for x in d["profiles"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("H-TERR-SITE", ids)
        self.assertIn("H-ORBIT", ids)
        self.assertIn("H-LUNAR", ids)
        self.assertIn("H-MARS", ids)
        self.assertIn("H-ASTEROID", ids)
        self.assertIn("H-INTERSTELLAR", ids)
        self.assertIn("not an assumed capability", d["local_only_mode"]["hard_rule"])

    def test_universal_triplet_is_exactly_three_layers(self):
        d = load("universal_triplet_v0_1.json")
        ids = [x["id"] for x in d["layers"]]
        self.assertEqual(ids, ["U-FILESPACE","U-DATASPACE","U-SOLIDSTATE"])
        self.assertIn("still evolving", d["working_term"]["status"])

    def test_circular_feed_has_decontamination_gate(self):
        d = load("eco_circular_materials_binding_v0_1.json")
        poly = next(x for x in d["streams"] if x["id"] == "ECO-POLY")
        chain = " ".join(poly["chain"]).lower()
        self.assertIn("wash", chain)
        self.assertIn("coupon test", chain)
        graphene = next(x for x in d["streams"] if x["id"] == "ECO-GRAPHENE")
        self.assertIn("does not itself become graphene", graphene["constraint"])

    def test_ai_helper_never_owns_hard_interlocks(self):
        d = load("ai_build_helper_interface_v0_1.json")
        self.assertTrue(any("hard machine interlocks" in x for x in d["AI_boundary"]))

    def test_frontier_scenario_does_not_replace_mission_baseline(self):
        d = load("portfolio_triplet_convergence_v0_1.json")
        self.assertIn("does not supersede", d["frontier_scenario"]["status"])

if __name__ == "__main__":
    unittest.main()
