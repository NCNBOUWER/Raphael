import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UTP = ROOT / "Raphael_Packages" / "Universal_Tech_Printer"


def load(name):
    return json.loads((UTP / name).read_text(encoding="utf-8-sig"))


def test_source_candidate_matrix_advances_only_at_source_evidence_ceiling():
    matrix = load("printer_mu_source_candidate_matrix_v0_1.json")
    dag = load("printer_mu_dependency_dag_v0_1.json")

    assert matrix["artifact_id"] == "UTP-PRINTER-MU-SOURCE-CANDIDATES-001"
    assert "NO PHYSICAL QUALIFICATION" in matrix["state"]
    assert matrix["dag_advancement"]["physical_qualification"] == "NOT_RUN"
    assert matrix["dag_advancement"]["C0_state"].startswith("PARTIAL CANDIDATE STACK ONLY")

    by_id = {node["id"]: node for node in dag["nodes"]}
    expected = {"MU-001", "MU-002", "MU-004", "MU-013", "MU-017", "MU-019"}
    actual = {node_id for node_id, node in by_id.items() if node["selection_state"] == "CANDIDATE"}

    assert actual == expected
    assert all(by_id[node_id]["evidence_state"] == "SOURCE_ONLY" for node_id in expected)
    assert all(by_id[node_id].get("candidate_refs") for node_id in expected)
    assert not any(node["selection_state"] == "SELECTED_WITH_EVIDENCE" for node in dag["nodes"])


def test_all_candidate_refs_resolve_and_c0_remains_incomplete():
    matrix = load("printer_mu_source_candidate_matrix_v0_1.json")
    dag = load("printer_mu_dependency_dag_v0_1.json")

    candidates = {item["candidate_id"]: item for item in matrix["candidates"]}
    assert len(candidates) == 7
    assert all(item["official_source"].startswith("https://") for item in candidates.values())

    for node in dag["nodes"]:
        for ref in node.get("candidate_refs", []):
            assert ref in candidates

    c0 = next(node for node in dag["nodes"] if node["id"] == "MU-017")
    assert set(c0["candidate_refs"]) == {"PMU-CAND-DRIVER-001", "PMU-CAND-SAFETY-001"}
    note = dag["dependency_closure"]["c0_partial_candidate_note"].lower()
    assert "deterministic motion controller" in note
    assert "remain unresolved" in note

    safety = candidates["PMU-CAND-SAFETY-001"]
    assert "not the complete C0 controller" in safety["role"]
    driver = candidates["PMU-CAND-DRIVER-001"]
    assert "not a safety controller" in driver["role"]
