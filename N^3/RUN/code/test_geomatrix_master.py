#!/usr/bin/env python3
"""Minimal validation tests for the N^3 / TPW GeoMatrix harness."""
from __future__ import annotations

import math
from fractions import Fraction

import geomatrix_master as gm


def assert_close(a: float, b: float, eps: float = 1e-12) -> None:
    if abs(a - b) > eps:
        raise AssertionError(f"expected {a} ≈ {b}")


def test_core_validation() -> None:
    v = gm.validate_tpw_core()
    assert v["sum_state_rows"] == 1331
    assert v["primitive_ordered_outcomes"] == 46656
    assert v["probability_sum"] == "1"
    assert v["unique_mode"] is True
    assert v["mode_states"] == [(7, 7, 7)]
    assert v["max_probability"] == "1/216"
    assert v["min_probability"] == "1/46656"
    assert v["min_probability_state_count"] == 8


def test_probability_and_counts() -> None:
    assert gm.two_dice_count(7) == 6
    assert gm.two_dice_count(2) == 1
    assert gm.two_dice_count(12) == 1
    assert gm.joint_probability((7, 7, 7)) == Fraction(1, 216)
    assert gm.joint_probability((2, 2, 2)) == Fraction(1, 46656)


def test_barycentric_closure() -> None:
    b = gm.barycentric_closure([6, 6, 6])
    assert b == (1 / 3, 1 / 3, 1 / 3)
    assert_close(sum(b), 1.0)
    assert gm.state_to_barycentric((7, 7, 7)) == (1 / 3, 1 / 3, 1 / 3)
    assert gm.state_to_barycentric((2, 2, 2)) == (1 / 3, 1 / 3, 1 / 3)


def test_projection_and_gamma() -> None:
    coord = gm.project_to_polygon([1, 1, 1])
    assert_close(coord[0], 0.0)
    assert_close(coord[1], 0.0)
    seq = [(1, 0, 0), (0, 1, 0)]
    path = gm.gamma_interpolate(seq, samples_per_segment=4)
    assert len(path) == 5
    assert path[0] == (1.0, 0.0, 0.0)
    assert path[-1] == (0.0, 1.0, 0.0)
    for point in path:
        assert_close(sum(point), 1.0)
        assert all(x >= 0 for x in point)


def test_velocity() -> None:
    vel = gm.finite_difference_velocity([(1, 0, 0), (0, 1, 0)], h=2.0)
    assert vel == [(-0.5, 0.5, 0.0)]


if __name__ == "__main__":
    test_core_validation()
    test_probability_and_counts()
    test_barycentric_closure()
    test_projection_and_gamma()
    test_velocity()
    print("all geomatrix_master tests passed")
