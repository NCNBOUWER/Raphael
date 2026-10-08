"""Referential and evidence-state regression tests for PrintSpace v0.3 seed datasets.

No physical data verification or production qualification is implied.
"""
import json
import csv
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

def data(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

class TestPrintSpacePopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.families = data("PAIRWISE_SEQUENCE_ROUTES_v0_1.json")
        cls.materials = data("MATERIAL_CANDIDATE_PASSPORTS_v0_3.json")
        cls.routes = data("MATERIAL_DIRECTIONAL_ROUTES_v0_3.json")
        cls.crosswalk = data("TECHNOLOGY_MATERIAL_CROSSWALK_v0_3.json")
        cls.opportunities = data("FUNCTIONAL_OPPORTUNITY_WINDOWS_v0_3.json")
        cls.geometries = data("PARAMETRIC_GEOMETRY_FUNCTION_SEEDS_v0_3.json")
        cls.coupons = data("COUPON_QUALIFICATION_QUEUE_v0_3.json")
        cls.handshake = data("PRINTSPACE_RUNTIME_HANDSHAKE_PROPOSAL_v0_2.json")

    def test_full_family_coverage_and_candidate_evidence(self):
        fams = {f["id"] for f in self.families["families"]}
        mats = self.materials["materials"]
        self.assertEqual(len(fams), 14)
        self.assertEqual(len(mats), 59)
        self.assertEqual({m["planning_family"] for m in mats}, fams)
        self.assertEqual(len({m["material_id"] for m in mats}), len(mats))
        for m in mats:
            self.assertIsNone(m["process_window"])
            self.assertEqual(m["measured_material_properties"], [])
            self.assertEqual(m["state"], "CANDIDATE_ONLY_NOT_A_RECIPE")
            self.assertTrue(m["candidate_environments"])

    def test_directional_route_traceability(self):
        mat = {m["material_id"]:m for m in self.materials["materials"]}
        pairs = {(x["from"],x["to"]):x for x in self.families["pairs"]}
        routes = self.routes["routes"]
        self.assertEqual(len(routes), 72)
        self.assertEqual(len({r["route_id"] for r in routes}), len(routes))
        indexes = {(r["first"],r["second"]) for r in routes}
        self.assertEqual(len(indexes),len(routes))
        self.assertEqual(indexes,{(b,a) for (a,b) in indexes})
        for r in routes:
            self.assertIn(r["first"],mat)
            self.assertIn(r["second"],mat)
            key=(mat[r["first"]]["planning_family"], mat[r["second"]]["planning_family"])
            self.assertEqual(r["pair_catalog_id"],pairs[key]["pair_id"])
            self.assertEqual(r["provisional_class"],pairs[key]["route_class"])
            self.assertIn("CAN", r["route_id"].replace("PS-MR","CAN-PS-MR"))
            self.assertEqual(r["production_approved"],False)
            self.assertEqual(r["evidence_state"], "NO_MATERIAL_PAIR_PHYSICAL_QUALIFICATION")
            self.assertTrue(r["can_if"])
            self.assertGreaterEqual(len(r["acceptance_tests"]),1)

    def test_all_upstream_technology_ids_are_bound(self):
        cw=self.crosswalk["records"]
        self.assertEqual(len(cw),70)
        self.assertEqual({c["tech_id"] for c in cw},{f"PT-{n:03d}" for n in range(1,71)})
        mats={m["material_id"] for m in self.materials["materials"]}
        for item in cw:
            self.assertTrue(set(item["material_seed_ids"])<=mats)
            self.assertTrue(item["geometry_seed"])
            self.assertEqual(item["evidence_state"],"CANDIDATE_BINDING_NOT_PRODUCTION_APPROVAL")

    def test_opportunity_and_geometry_coverage(self):
        records=self.opportunities["records"]
        geo=self.geometries["geometries"]
        self.assertEqual(len(records),26)
        self.assertEqual(len(geo),30)
        allowed={"ENV-0","ENV-1","ENV-2","ENV-3","ENV-4"}
        for x in records:
            self.assertTrue(set(x["candidate_utp_environment_ids"])<=allowed)
            self.assertFalse(x["production_approved"])
            self.assertTrue(x["required_measurements"])
        for x in geo:
            self.assertTrue(x["parameters"])
            self.assertFalse(x["machine_ready"])

    def test_coupons_cover_every_direction_without_approval(self):
        coupons=self.coupons["coupons"]
        route_ids={r["route_id"] for r in self.routes["routes"]}
        self.assertEqual(len(coupons),72)
        self.assertEqual({c["material_route_id"] for c in coupons}, route_ids)
        self.assertEqual(len({c["coupon_id"] for c in coupons}),72)
        self.assertEqual(self.coupons["counts"]["p1"],12)
        self.assertEqual(self.coupons["counts"]["p2"]+self.coupons["counts"]["p3"],60)
        for x in coupons:
            self.assertIsNone(x["threshold_values"])
            self.assertFalse(x["physical_tested"])
            self.assertFalse(x["production_approved"])
            self.assertEqual(x["status"],"DESIGNED_NOT_EXECUTED")


    def test_complete_material_level_directional_index(self):
        with (HERE / "MATERIAL_PAIRWISE_INDEX_v0_3.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            rows=list(csv.DictReader(handle))
        mats={m["material_id"]:m for m in self.materials["materials"]}
        fams={(p["from"], p["to"]):p for p in self.families["pairs"]}
        curated={(r["first"],r["second"]):r for r in self.routes["routes"]}
        self.assertEqual(len(rows),59 * 59)
        self.assertEqual(len({(r["material_from"],r["material_to"]) for r in rows}),59 * 59)
        self.assertEqual(sum(bool(r["curated_directional_route_id"]) for r in rows),72)
        for row in rows:
            a=mats[row["material_from"]]
            b=mats[row["material_to"]]
            p=fams[(a["planning_family"],b["planning_family"])]
            self.assertEqual(row["inherited_family_route_class"],p["route_class"])
            self.assertEqual(row["family_pair_id"],p["pair_id"])
            self.assertEqual(row["production_approved"],"false")
            self.assertEqual(row["physical_test_status"],"NOT_TESTED")
            cr=curated.get((a["material_id"],b["material_id"]))
            self.assertEqual(row["curated_directional_route_id"],cr["route_id"] if cr else "")
            if cr is None:
                self.assertEqual(row["candidate_status"],"FAMILY_CLASS_INHERITED")
            else:
                self.assertEqual(row["candidate_status"],"ROUTE_SEED_ONLY")

    def test_handshake_fail_closed(self):
        h=self.handshake
        self.assertFalse(h["physical_actuation"])
        self.assertFalse(h["installed_in_local_runtime"])
        self.assertFalse(h["live_registry_modified"])
        self.assertIn("missing_measurements",h["state_handshake"]["fail_closed_conditions"])
        self.assertIn("machine.start",h["prohibited_capabilities"])

if __name__=="__main__":
    unittest.main()
