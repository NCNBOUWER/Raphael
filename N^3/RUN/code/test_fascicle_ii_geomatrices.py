"""Smoke tests for Fascicle II Raphael GeoMatrices utilities."""

from math import isclose
from fascicle_ii_geomatrices import (
    DICE_2D6_COUNTS,
    normalize,
    two_dice_count,
    product_probability_for_2d6_sums,
    obw_polygon_map,
    gamma_interpolate,
    finite_difference,
    covariant_barycentric_derivative,
    mmb_aggregate,
    single_observer_bias_bound,
    validate_fascicle_ii,
    get_project_scope,
    get_fascicle_status,
    get_core_tpw_facts,
    get_raphael_boundary,
    get_eml_boundary,
    get_fascicle_ii_objects,
)


def test_two_dice_counts():
    expected = [1,2,3,4,5,6,5,4,3,2,1]
    got = [two_dice_count(s) for s in range(2,13)]
    assert got == expected
    assert sum(got) == 36
    assert DICE_2D6_COUNTS[7] == 6


def test_tpw_probability_facts():
    assert isclose(product_probability_for_2d6_sums([7,7,7]), 1/216)
    assert isclose(product_probability_for_2d6_sums([2,2,2]), 1/46656)
    assert get_core_tpw_facts()["sum_state_rows"] == 1331
    assert get_core_tpw_facts()["primitive_ordered_outcomes"] == 46656


def test_obw_closure_and_centres():
    assert isclose(sum(normalize([12,5,5])), 1.0)
    c3 = obw_polygon_map([7,7,7])
    c4 = obw_polygon_map([7,7,7,7])
    assert all(abs(v) < 1e-12 for v in c3)
    assert all(abs(v) < 1e-12 for v in c4)


def test_transport_and_covariant_closure():
    a = normalize([12,5,5])
    b = normalize([7,7,7])
    mid = gamma_interpolate(a,b,0.5)
    vel = finite_difference(a,b,1.0)
    assert isclose(sum(mid), 1.0, abs_tol=1e-12)
    assert isclose(sum(vel), 0.0, abs_tol=1e-12)
    D = covariant_barycentric_derivative([1,1,1], [0.2,-0.1,0.05], [0.1,0.0,-0.1])
    assert isclose(sum(D), 0.0, abs_tol=1e-12)


def test_mmb_aggregate_and_bias_bound():
    agg = mmb_aggregate([[7,7,7], [8,6,7], [6,8,7], [7,6,8]])
    assert isclose(sum(agg), 1.0, abs_tol=1e-12)
    assert isclose(single_observer_bias_bound(1.0, 4), 0.25)
    assert isclose(single_observer_bias_bound(1.0, 6), 1/6)


def test_smoke_calls_are_real():
    assert "N^3" in get_project_scope()
    assert get_fascicle_status()["Fascicle II"] == "active build"
    assert "fixed" in get_raphael_boundary()
    assert "EML#F" in get_eml_boundary()
    assert "Omnicompounded Barycentric Well" in get_fascicle_ii_objects()
    report = validate_fascicle_ii()
    assert report["closure_3"]
    assert report["centre3_near_zero"]
    assert report["gamma_closed"]
    assert report["derivative_tangent"]
    assert report["mmb_closed"]


if __name__ == "__main__":
    test_two_dice_counts()
    test_tpw_probability_facts()
    test_obw_closure_and_centres()
    test_transport_and_covariant_closure()
    test_mmb_aggregate_and_bias_bound()
    test_smoke_calls_are_real()
    print("all Fascicle II GeoMatrices tests passed")
