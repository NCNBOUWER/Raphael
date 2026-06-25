"""Smoke tests for Fascicle III Raphael integration utilities."""

from fascicle_iii_raphael_bridge import (
    get_fascicle_iii_status,
    get_equation_registry,
    evaluate_claim_status,
    evaluate_domain_admissibility,
    inherited_fidelity,
    get_raphael_suite_calls,
    get_eml_reference,
    validate_fascicle_iii,
)


def test_status_boundaries():
    status = get_fascicle_iii_status()
    assert status["Fascicle III"] == "Raphael integration and disproof-method layer"
    assert status["Raphael Lite"] == "deferred"
    assert "external" in status["EML#F"]


def test_equation_registry_real():
    eqs = get_equation_registry()
    assert len(eqs) == 5
    assert "sum p_n=1.0" in eqs["EQ-CL-001"]
    assert "D_mu" in eqs["EQ-DER-001"]
    assert "Psi_ToE" in eqs["EQ-TOE-001"]


def test_claim_crosswalk_real():
    closure = evaluate_claim_status("closure_constraint")
    assert closure["status"] == "internally_validated"
    assert closure["fidelity"] == 110
    assert "EQ-CL-001" in closure["equations"]


def test_domain_admissibility():
    full = {
        "finite_or_normalisable_components": True,
        "closure_or_conservation_rule": True,
        "coordinate_or_history_sequence": True,
        "residual_or_failure_condition": True,
        "domain_relevance": True,
    }
    ok, missing = evaluate_domain_admissibility(full)
    assert ok and missing == []
    ok2, missing2 = evaluate_domain_admissibility({"closure_or_conservation_rule": True})
    assert not ok2
    assert "finite_or_normalisable_components" in missing2


def test_fidelity_logic():
    assert inherited_fidelity(100) == 100
    assert inherited_fidelity(100, 100) == 110
    assert inherited_fidelity(120) == 120
    assert inherited_fidelity(120, 100) == 120
    assert inherited_fidelity(90, 100) == 90


def test_suite_and_eml_boundaries():
    calls = get_raphael_suite_calls()
    assert "map_to_raphael_term" in calls
    assert "evaluate_claim_status" in calls
    assert "EML#F" in get_eml_reference()


def test_validation_payload():
    report = validate_fascicle_iii()
    assert report["equation_count"] == 5
    assert report["claim_count"] == 4
    assert report["domain_full_admissible"] is True
    assert report["domain_partial_admissible"] is False
    assert report["fidelity_100_100"] == 110
    assert report["raphael_lite"] == "deferred"


if __name__ == "__main__":
    test_status_boundaries()
    test_equation_registry_real()
    test_claim_crosswalk_real()
    test_domain_admissibility()
    test_fidelity_logic()
    test_suite_and_eml_boundaries()
    test_validation_payload()
    print("all Fascicle III Raphael integration tests passed")
