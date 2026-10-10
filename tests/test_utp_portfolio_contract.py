import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "Raphael_Packages" / "Universal_Tech_Printer"

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class UTPPortfolioContractTests(unittest.TestCase):
    def test_dbr_contract_has_full_transition_chain(self):
        d = load("cgx_snapshot_dbr_handshake_contract_v0_1.json")
        steps = [x["step"] for x in d["handshake"]]
        self.assertEqual(
            steps,
            ["HELLO","CAPABILITY","HORIZON","STATE","TASK_OFFER","PLAN_RECEIPT",
             "EXEC_RECEIPT","VERIFY","DBR_COMMIT","HANDOFF"]
        )
        snaps = [x["id"] for x in d["snapshot_types"]]
        for expected in ("SNAP-INTENT","SNAP-PLAN","SNAP-EXEC","SNAP-ASBUILT","SNAP-SERVICE","SNAP-HANDOFF"):
            self.assertIn(expected, snaps)
        self.assertIn("does not by itself certify physical performance", d["dbr_record"]["rule"])

    def test_delivery_catalogue_covers_major_audiences(self):
        d = load("portfolio_delivery_catalogue_v0_1.json")
        audiences = {x["audience"] for x in d["offerings"]}
        for expected in (
            "individual/maker/school","small business","cleanup/nonprofit/community",
            "government/municipal/infrastructure","university/lab",
            "internal Römer/EMASSC/InterSol","remote/space outpost"
        ):
            self.assertIn(expected, audiences)
        self.assertIn("GOVERNMENT", d["AI_rendering"])
        self.assertIn("OUTPOST", d["AI_rendering"])

    def test_ruvr_is_explicit_source_gap(self):
        d = load("civilization_health_metrics_v0_1.json")
        self.assertEqual(d["source_gap"]["alias"], "RUVR")
        self.assertIn("NO EXACT SOURCE FOUND", d["source_gap"]["search_state"])
        self.assertIn("Do not invent", d["source_gap"]["rule"])
        ids = [x["id"] for x in d["metrics"]]
        self.assertEqual(len(ids), len(set(ids)))
        for required in ("M-CAP","M-SEED","M-ECO","M-PUBLIC","M-EVID","M-SAFE","M-EXP"):
            self.assertIn(required, ids)

    def test_showcase_keeps_claim_boundaries(self):
        d = load("solid_state_showcase_ladder_v0_1.json")
        items = d["showcases"]
        self.assertGreaterEqual(len(items), 10)
        phone = next(x for x in items if x["id"] == "SH-02")
        self.assertIn("not iPhone SoC density", phone["boundary"])
        mark = next(x for x in items if x["id"] == "SH-11")
        self.assertIn("representative subsystem", mark["boundary"])

if __name__ == "__main__":
    unittest.main()
