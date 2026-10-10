import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CROSSWALK = ROOT / "CGX" / "PrintSpace" / "TYPE1_UTP150_MATURATION_CROSSWALK_v0_1.json"


def test_utp150_crosswalk_binds_existing_printspace_source_families_without_physical_uplift():
    data = json.loads(CROSSWALK.read_text(encoding="utf-8-sig"))
    accepted = set(data["accepted_ingest_classes"])
    bindings = data["source_family_bindings"]

    assert data["artifact_id"] == "RAPHAEL-PRINTSPACE-UTP150-XWALK-001"
    assert "PHYSICAL_NOT_RUN" in data["status"]
    assert len(bindings) >= 9
    assert all(item["ingest_class"] in accepted for item in bindings)
    assert all((ROOT / item["path"]).exists() for item in bindings)
    assert all(item["primary_axes"] for item in bindings)
    assert all(item["expected_dependents"] for item in bindings)

    boundaries = " ".join(data["hard_boundaries"]).lower()
    assert "no physical execution" in boundaries
    assert "no second master" in boundaries
    assert "unknown or unsupported coupling remains hold" in boundaries
    assert "physical execution remains separate" in data["next_proof"].lower()


def test_crosswalk_preserves_directional_and_measurement_fail_closed_rules():
    data = json.loads(CROSSWALK.read_text(encoding="utf-8-sig"))
    by_name = {Path(item["path"]).name: item for item in data["source_family_bindings"]}

    directional = by_name["MATERIAL_DIRECTIONAL_ROUTES_v0_3.json"]
    assert "X→Y does not imply Y→X" in directional["evidence_rule"]

    measurements = by_name["MATERIAL_PROPERTY_MEASUREMENT_REGISTER_v0_3.csv"]
    assert measurements["ingest_class"] == "RAW_MEASUREMENT"
    assert "SYMBOLIC or HOLD" in measurements["evidence_rule"]

    coupons = by_name["COUPON_QUALIFICATION_QUEUE_v0_3.json"]
    assert "cannot advance physical_evidence" in coupons["evidence_rule"]
