import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "Raphael_Packages" / "Universal_Tech_Printer"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class UTPObjectPortfolioExtensionTests(unittest.TestCase):
    def test_physical_object_identity_preserves_triplet_and_compute_boundary(self):
        d = load("cgx_physical_object_identity_v0_1.json")
        self.assertEqual(set(d["three_planes"]), {"filespace","dataspace","solid_state"})
        ids = [x["id"] for x in d["compute_profiles"]]
        self.assertEqual(ids, ["CP0-PASSIVE","CP1-TINY","CP2-EDGE","CP3-FEDERATED"])
        self.assertIn("does not create missing physical compute", d["equivalence_rule"])
        self.assertEqual(
            d["minimal_handshake"],
            ["HELLO","CAPABILITY","HORIZON","STATE","TASK_OFFER","PLAN_RECEIPT","EXEC_RECEIPT","VERIFY","DBR_COMMIT","HANDOFF"]
        )

    def test_new_neutrals_cover_required_interface_roles(self):
        d = load("new_neutrals_layer_taxonomy_v0_1.json")
        ids = {x["id"] for x in d["classes"]}
        for expected in (
            "N-POWER-REF","N-DIEL","N-EMI","N-MAG","N-THERM-SPREAD","N-THERM-BREAK",
            "N-CHEM","N-GALV","N-COMPLY","N-HERM","N-OPT","N-FLUID"
        ):
            self.assertIn(expected, ids)
        self.assertIn("not physically inert", d["definition"])

    def test_catalogue_projection_keeps_single_evidence_graph(self):
        d = load("catalogue_projection_contract_v0_1.json")
        self.assertIn("one underlying evidence-bearing catalogue", d["principle"])
        self.assertIn("DIY/school", d["audiences"])
        self.assertIn("government/infrastructure", d["audiences"])
        self.assertIn("remote/outpost", d["audiences"])
        self.assertIn("Eco-Grex", d["portfolio_domains"])
        self.assertIn("Type-2 frontier", d["portfolio_domains"])

    def test_eco_packet_does_not_label_cleanup_carbon_as_graphene(self):
        d = load("build_packets/eco_circular_sensor_heater_v0_1.json")
        self.assertIn("not labelled graphene", d["graphene_boundary"])
        self.assertIn("coupon", " ".join(d["workflow"]).lower())

    def test_surface_packet_keeps_frontier_mechanism_gate(self):
        d = load("build_packets/gov_functional_surface_pilot_v0_1.json")
        self.assertIn("sensor input", d["geospatial_biofeedback_boundary"])
        self.assertIn("falsification test", d["geospatial_biofeedback_boundary"])

    def test_diy_packet_excludes_hazardous_routes(self):
        d = load("build_packets/diy_cgx_identity_starter_v0_1.json")
        b = " ".join(d["boundaries"]).lower()
        self.assertIn("no high-voltage plasma", b)
        self.assertIn("no reactive/toxic semiconductor", b)

if __name__ == "__main__":
    unittest.main()
