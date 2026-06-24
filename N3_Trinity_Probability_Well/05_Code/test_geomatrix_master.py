#!/usr/bin/env python3
"""Regression tests for geomatrix_master.py."""

from fractions import Fraction
from geomatrix_master import (
    barycentric_closure,
    finite_difference_velocity,
    gamma_interpolate,
    joint_probability,
    project_to_polygon,
    state_to_barycentric,
    validate_tpw_core,
)


def test_tpw_core():
    result = validate_tpw_core()
    assert result["sum_state_rows"] == 1331
    assert result["primitive_ordered_outcomes"] == 46656
    assert result["probability_sum"] == "1"
    assert result["unique_mode"] is True
    assert result["max_probability"] == "1/216"
    assert result["min_probability"] == "1/46656"
    assert result["min_probability_state_count"] == 8


def test_mode_probability():
    assert joint_probability((7, 7, 7)) == Fraction(1, 216)
    assert joint_probability((6, 7, 7)) < joint_probability((7, 7, 7))


def test_centroid_nonunique_and_selector():
    assert state_to_barycentric((2, 2, 2)) == (1/3, 1/3, 1/3)
    assert state_to_barycentric((7, 7, 7)) == (1/3, 1/3, 1/3)
    assert joint_probability((7, 7, 7)) > joint_probability((2, 2, 2))


def test_barycentric_projection_closure():
    b = barycentric_closure([1, 2, 3])
    assert abs(sum(b) - 1.0) < 1e-12
    x, y = project_to_polygon(b)
    assert -1.0 <= x <= 1.0
    assert -1.0 <= y <= 1.0


def test_gamma_closure():
    seq = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    interp = gamma_interpolate(seq, samples_per_segment=4)
    for state in interp:
        assert abs(sum(state) - 1.0) < 1e-12
        assert all(v >= -1e-12 for v in state)
    vel = finite_difference_velocity(seq)
    assert len(vel) == 2


if __name__ == "__main__":
    test_tpw_core()
    test_mode_probability()
    test_centroid_nonunique_and_selector()
    test_barycentric_projection_closure()
    test_gamma_closure()
    print("all geomatrix_master tests passed")
