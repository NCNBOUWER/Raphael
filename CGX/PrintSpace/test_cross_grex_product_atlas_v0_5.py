"""Read-only integrity checks for cross-Grex candidate product atlas."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def get(name):
    return json.loads((ROOT/name).read_text(encoding="utf-8"))
class PortfolioCoverage(unittest.TestCase):
    def setUp(self):
        self.p = get("CROSS_GREX_PRODUCT_ATLAS_v0_5.json")
        self.t = get("TECHNOLOGY_MATERIAL_CROSSWALK_v0_3.json")
        self.m = get("MATERIAL_CANDIDATE_PASSPORTS_v0_3.json")
        self.r = get("PAIRWISE_SEQUENCE_ROUTES_v0_1.json")
    def test_full_class_coverage(self):
        ps = self.p["products"]
        tech = {x["tech_id"] for x in self.t["records"]}
        used = {t for p in ps for t in p["component_tech_refs"]}
        self.assertEqual(len(ps), 80)
        self.assertEqual(len({p["product_id"] for p in ps}), 80)
        self.assertEqual(tech, used)
        self.assertEqual(len(used),70)
        self.assertEqual(len({p["category"] for p in ps}),9)
    def test_links_and_stages(self):
        materials={x["material_id"] for x in self.m["materials"]}
        pairs={(x["from"],x["to"]):x for x in self.r["pairs"]}
        total=0
        for p in self.p["products"]:
            self.assertTrue(set(p["bottom_up"]["material_seed_refs"])<=materials)
            stages=p["bottom_up"]["stages"]
            self.assertEqual(len(stages),len(p["bottom_up"]["material_family_path"]))
            for i,s in enumerate(stages):
                self.assertEqual(i+1,s["step"])
                self.assertEqual(s["stage_status"],"DESIGN_ONLY_NOT_RUN")
                if i:
                    pair=pairs[(stages[i-1]["family"],s["family"])]
                    self.assertEqual(pair["pair_id"],s["process_pair_id"])
                    self.assertEqual(pair["route_class"],s["transition_class"])
                    total+=1
            if "BT" in p["bottom_up"]["material_family_path"]:
                self.assertEqual(stages[-1]["family"],"BT")
            self.assertFalse(p["production_approved"])
            self.assertFalse(p["physical_tested"])
        self.assertEqual(total,395)
    def test_gap_and_reuse_registers(self):
        gaps=get("CROSS_GREX_GAP_REGISTER_v0_5.json")["tickets"]
        reuse=get("CROSS_GREX_SHARED_PRIMITIVES_v0_5.json")["records"]
        self.assertEqual(len(gaps),220)
        self.assertEqual(len(reuse),70)
        self.assertEqual(sum(x["product_reuse_count"] for x in reuse),586)
        self.assertFalse(any(x["production_approved"] for x in gaps))
    def test_environment_opportunities(self):
        ids={x["id"] for x in get("FUNCTIONAL_OPPORTUNITY_WINDOWS_v0_3.json")["records"]}
        for p in self.p["products"]:
            self.assertTrue(set(p["bottom_up"]["environment_opportunity_ids"])<=ids)
    def test_butterbot_and_phone(self):
        byid={p["product_id"]:p for p in self.p["products"]}
        self.assertIn("PT-043",byid["FU-01"]["component_tech_refs"])
        self.assertIn("PT-053",byid["FO-01"]["component_tech_refs"])
        self.assertIn("PT-068",byid["FR-02"]["component_tech_refs"])
        self.assertIn("PT-036",byid["FD-04"]["component_tech_refs"])
if __name__=="__main__":
    unittest.main()
