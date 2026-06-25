from math import exp, isclose
from emlf_operator import (
    eml,
    activation_suppression,
    activation_suppression_expanded,
    optimum_r,
    cascade_basis,
    validate_emlf,
)


def test_operator_identity():
    assert isclose(eml(2.0, exp(3.0)), exp(2.0) - 3.0, rel_tol=1e-12)


def test_m1_expansion():
    assert isclose(
        activation_suppression(2.0, 0.55, 0.32),
        activation_suppression_expanded(2.0, 0.55, 0.32),
        rel_tol=1e-12,
    )


def test_internal_optimum():
    r0 = optimum_r(0.55, 0.32)
    left = activation_suppression_expanded(r0 * 0.98, 0.55, 0.32)
    mid = activation_suppression_expanded(r0, 0.55, 0.32)
    right = activation_suppression_expanded(r0 * 1.02, 0.55, 0.32)
    assert mid >= left
    assert mid >= right


def test_cascade_basis_shape():
    basis = cascade_basis([0, 1, 2, 3], depth=3, tau=2.0)
    assert len(basis) == 3
    assert all(len(row) == 4 for row in basis)


def test_non_smoke_validation():
    report = validate_emlf()
    assert report["eml_beats_hill_on_nonmonotone_data"] is True
    assert report["cascade_depth"] == 3
    assert report["cascade_time_points"] == 4
    assert report["all_values_finite"] is True


if __name__ == "__main__":
    test_operator_identity()
    test_m1_expansion()
    test_internal_optimum()
    test_cascade_basis_shape()
    test_non_smoke_validation()
    print("all EML#F validation tests passed")
