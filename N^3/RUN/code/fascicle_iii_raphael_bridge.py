"""Fascicle III Raphael integration utilities.

This module exposes the crosswalk, fidelity, equation registry, and disproof-method checks used by Fascicle III. It does not build Raphael Lite and does not implement EML#F.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

FIDELITY_LEVELS = {
    100: "mathematically proof-locked within stated assumptions",
    110: "proof-locked plus corroborating internal proof path",
    200: "empirically validated",
    250: "second independent empirical validation method",
}

EQUATIONS = {
    "EQ-CL-001": "S=sum X_n; p_n=X_n/S; sum p_n=1.0",
    "EQ-DER-001": "D_mu p_n = partial_mu p_n + [A_mu^n + T_mu_nu partial^nu v_n] p_n",
    "EQ-LOG-001": "L(p)=log10(P_joint+10^-5)",
    "EQ-LAP-001": "nabla^2 L(r)=-4 alpha near centroid",
    "EQ-TOE-001": "Psi_ToE = integral_over_simplex((nabla^d Psi_in) exp(i integral g_QG dt')) dV_4",
}

CLAIM_CROSSWALK = {
    "closure_constraint": {
        "supports": ["Fascicle I normalization", "Fascicle II OBW containment"],
        "equations": ["EQ-CL-001"],
        "status": "internally_validated",
        "fidelity": 110,
        "fail_if": "mapped state fails closure",
    },
    "centrality_selector": {
        "supports": ["Fascicle I unique product mode", "Fascicle II regular polygon centre"],
        "equations": ["EQ-LOG-001"],
        "status": "internally_supported",
        "fidelity": 110,
        "fail_if": "equal-centroid states are confused with product-probability modes",
    },
    "transport_covariance": {
        "supports": ["Gamma bridge", "covariant derivative tangent condition"],
        "equations": ["EQ-DER-001"],
        "status": "internally_supported",
        "fidelity": 110,
        "fail_if": "projected derivative violates tangent closure",
    },
    "cross_domain_manifest": {
        "supports": ["closure grammar", "OBW/MMB grammar", "falsification routes"],
        "equations": ["EQ-TOE-001"],
        "status": "ToE_candidate_framework",
        "fidelity": 110,
        "fail_if": "target domain cannot define closure, geometry, residual, or evidence pathway",
    },
}

DOMAIN_REQUIREMENTS = [
    "finite_or_normalisable_components",
    "closure_or_conservation_rule",
    "coordinate_or_history_sequence",
    "residual_or_failure_condition",
    "domain_relevance",
]


def get_fascicle_iii_status() -> Dict[str, str]:
    return {
        "Fascicle I": "imported mathematical foundation",
        "Fascicle II": "imported architectural/classical foundation",
        "Fascicle III": "Raphael integration and disproof-method layer",
        "Raphael Lite": "deferred",
        "EML#F": "external source/library pointer",
    }


def get_equation_registry() -> Dict[str, str]:
    return dict(EQUATIONS)


def evaluate_claim_status(claim_key: str) -> Dict[str, object]:
    if claim_key not in CLAIM_CROSSWALK:
        raise KeyError(f"unknown claim key: {claim_key}")
    return dict(CLAIM_CROSSWALK[claim_key])


def evaluate_domain_admissibility(features: Dict[str, bool]) -> Tuple[bool, List[str]]:
    missing = [name for name in DOMAIN_REQUIREMENTS if not features.get(name, False)]
    return (len(missing) == 0, missing)


def inherited_fidelity(*support_levels: int) -> int:
    """Return internal inherited fidelity.

    If all dependencies are >=100 and at least two independent proof paths are supplied,
    the assembled support reaches 110. A single >=120 dependency may carry its own level.
    Empirical thresholds are not manufactured here.
    """
    if not support_levels:
        return 0
    if len(support_levels) == 1:
        return support_levels[0]
    if all(level >= 100 for level in support_levels):
        return max(110, min(max(support_levels), 250))
    return min(support_levels)


def get_raphael_suite_calls() -> List[str]:
    return [
        "get_raphael_equations",
        "map_to_closure",
        "map_to_obw",
        "map_to_mmb",
        "map_to_raphael_term",
        "evaluate_claim_status",
        "get_fidelity",
        "get_eml_reference",
    ]


def get_eml_reference() -> str:
    return "See EML#F for the external EML Function derivation-library/catalogue; do not import it as native GeoMatrices."


def validate_fascicle_iii() -> Dict[str, object]:
    admissible, missing = evaluate_domain_admissibility({k: True for k in DOMAIN_REQUIREMENTS})
    partial_admissible, partial_missing = evaluate_domain_admissibility({"closure_or_conservation_rule": True})
    return {
        "equation_count": len(EQUATIONS),
        "claim_count": len(CLAIM_CROSSWALK),
        "closure_status": evaluate_claim_status("closure_constraint")["status"],
        "transport_equation": evaluate_claim_status("transport_covariance")["equations"][0],
        "domain_full_admissible": admissible,
        "domain_full_missing": missing,
        "domain_partial_admissible": partial_admissible,
        "domain_partial_missing_count": len(partial_missing),
        "fidelity_100_100": inherited_fidelity(100, 100),
        "fidelity_120_single": inherited_fidelity(120),
        "raphael_lite": get_fascicle_iii_status()["Raphael Lite"],
        "eml_boundary": get_eml_reference(),
        "suite_call_count": len(get_raphael_suite_calls()),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(validate_fascicle_iii(), indent=2, sort_keys=True))
