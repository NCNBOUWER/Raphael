"""Fascicle II Raphael GeoMatrices utilities.

Concrete, smoke-testable functions for OBW, MMB, irregular geometry and
closure-preserving transport. This module intentionally avoids Raphael Lite and
does not implement external EML#F.
"""

from __future__ import annotations

from math import cos, sin, pi, isclose, log10
from typing import List, Sequence, Tuple, Dict

Vector = Tuple[float, ...]

DICE_2D6_COUNTS: Dict[int, int] = {s: 6 - abs(7 - s) for s in range(2, 13)}


def two_dice_count(total: int, sides: int = 6) -> int:
    """Return the number of ordered outcomes for a two-dice sum."""
    if sides < 2:
        raise ValueError("sides must be >= 2")
    if total < 2 or total > 2 * sides:
        return 0
    return min(total - 1, 2 * sides + 1 - total)


def normalize(weights: Sequence[float]) -> List[float]:
    """Normalize non-negative weights to a closed composition."""
    if not weights:
        raise ValueError("at least one weight is required")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    total = float(sum(weights))
    if total <= 0:
        raise ValueError("sum(weights) must be > 0")
    return [float(w) / total for w in weights]


def regular_polygon_vertices(k: int, radius: float = 1.0, phase: float = pi / 2) -> List[Vector]:
    """Return centred regular K-gon vertices in R^2."""
    if k < 3:
        raise ValueError("k must be >= 3")
    return [
        (radius * cos(phase + 2 * pi * i / k), radius * sin(phase + 2 * pi * i / k))
        for i in range(k)
    ]


def weighted_map(weights: Sequence[float], vertices: Sequence[Sequence[float]]) -> Vector:
    """Map weights to the convex hull of supplied vertices."""
    if len(weights) != len(vertices):
        raise ValueError("weights and vertices must have the same length")
    if not vertices:
        raise ValueError("vertices are required")
    dim = len(vertices[0])
    if any(len(v) != dim for v in vertices):
        raise ValueError("all vertices must share dimension")
    p = normalize(weights)
    return tuple(sum(p_i * float(v[j]) for p_i, v in zip(p, vertices)) for j in range(dim))


def obw_polygon_map(weights: Sequence[float], phase: float = pi / 2) -> Vector:
    """Map K weights into a regular K-gon OBW."""
    return weighted_map(weights, regular_polygon_vertices(len(weights), phase=phase))


def product_probability_for_2d6_sums(sums: Sequence[int], sides: int = 6) -> float:
    """Joint probability for independent two-dice sum variables."""
    denom = (sides * sides) ** len(sums)
    num = 1
    for s in sums:
        num *= two_dice_count(int(s), sides=sides)
    return num / denom


def log_probability(sums: Sequence[int], epsilon: float = 1e-5) -> float:
    """Base-10 log probability with regularising epsilon."""
    return log10(product_probability_for_2d6_sums(sums) + epsilon)


def gamma_interpolate(a: Sequence[float], b: Sequence[float], lam: float) -> List[float]:
    """Piecewise-linear interpolation between closed states."""
    if len(a) != len(b):
        raise ValueError("states must have the same length")
    if not 0 <= lam <= 1:
        raise ValueError("lam must be in [0,1]")
    return [(1 - lam) * float(x) + lam * float(y) for x, y in zip(a, b)]


def finite_difference(a: Sequence[float], b: Sequence[float], dt: float = 1.0) -> List[float]:
    """Finite-difference transport vector between states."""
    if dt == 0:
        raise ValueError("dt must be non-zero")
    if len(a) != len(b):
        raise ValueError("states must have the same length")
    return [(float(y) - float(x)) / dt for x, y in zip(a, b)]


def covariant_barycentric_derivative(p: Sequence[float], raw_change: Sequence[float], connection: Sequence[float] | None = None) -> List[float]:
    """Return a closure-preserving derivative.

    raw_i = raw_change_i + connection_i*p_i
    D_i = raw_i - p_i*sum(raw)
    Therefore sum(D)=0 when sum(p)=1.
    """
    if len(p) != len(raw_change):
        raise ValueError("p and raw_change must have the same length")
    p_norm = normalize(p)
    if connection is None:
        connection = [0.0] * len(p_norm)
    if len(connection) != len(p_norm):
        raise ValueError("connection must match p length")
    raw = [float(r) + float(c) * p_i for p_i, r, c in zip(p_norm, raw_change, connection)]
    total_raw = sum(raw)
    return [r - p_i * total_raw for p_i, r in zip(p_norm, raw)]


def mmb_aggregate(observer_maps: Sequence[Sequence[float]], weights: Sequence[float] | None = None) -> List[float]:
    """Aggregate closed observer maps into a closed MMB state."""
    if not observer_maps:
        raise ValueError("observer maps are required")
    width = len(observer_maps[0])
    if any(len(m) != width for m in observer_maps):
        raise ValueError("observer maps must have equal length")
    closed_maps = [normalize(m) for m in observer_maps]
    if weights is None:
        weights = [1.0] * len(observer_maps)
    w = normalize(weights)
    return [sum(w_i * m[j] for w_i, m in zip(w, closed_maps)) for j in range(width)]


def single_observer_bias_bound(bias_magnitude: float, observer_count: int) -> float:
    """Equal-weight bound for one observer's unilateral bias contribution."""
    if observer_count <= 0:
        raise ValueError("observer_count must be positive")
    return abs(float(bias_magnitude)) / observer_count


PLATONIC_VERTEX_MATRIX = {
    "Tetrahedron": {"vertices": 4, "dice_pairs": 4, "total_dice": 8},
    "Octahedron": {"vertices": 6, "dice_pairs": 6, "total_dice": 12},
    "Cube": {"vertices": 8, "dice_pairs": 8, "total_dice": 16},
    "Icosahedron": {"vertices": 12, "dice_pairs": 12, "total_dice": 24},
    "Dodecahedron": {"vertices": 20, "dice_pairs": 20, "total_dice": 40},
}


def get_project_scope() -> str:
    return "N^3 = Fascicles I-III; GeoMatrices = future unified merge."


def get_fascicle_status() -> Dict[str, str]:
    return {"Fascicle I": "built", "Fascicle II": "active build", "Fascicle III": "deferred"}


def get_core_tpw_facts() -> Dict[str, object]:
    return {
        "sum_state_rows": 11 ** 3,
        "primitive_ordered_outcomes": 36 ** 3,
        "mode": (7, 7, 7),
        "max_probability": product_probability_for_2d6_sums([7, 7, 7]),
        "min_probability": product_probability_for_2d6_sums([2, 2, 2]),
    }


def get_fascicle_ii_objects() -> List[str]:
    return [
        "Omnicompounded Barycentric Well",
        "Multi-Observer Multi-Function Breakdown",
        "bounded container",
        "observer decomposition",
        "classical correspondence",
        "covariant transport",
        "irregular geometry",
    ]


def get_raphael_boundary() -> str:
    return "Raphael equations are fixed; N^3 crosswalks, supports, constrains, or disproves only."


def get_eml_boundary() -> str:
    return "EML#F is separate third-party source/library; not EMFF/RFS and not proof of Raphael."


def validate_fascicle_ii() -> Dict[str, object]:
    """Return deterministic validation checks for smoke tests."""
    centre3 = obw_polygon_map([7, 7, 7])
    centre4 = obw_polygon_map([7, 7, 7, 7])
    p_a = normalize([12, 5, 5])
    p_b = normalize([7, 7, 7])
    mid = gamma_interpolate(p_a, p_b, 0.5)
    derivative = covariant_barycentric_derivative([1, 1, 1], [0.2, -0.1, 0.05], [0.1, 0.0, -0.1])
    mmb = mmb_aggregate([[7, 7, 7], [8, 6, 7], [6, 8, 7], [7, 6, 8]])
    return {
        "closure_3": isclose(sum(normalize([12, 5, 5])), 1.0, abs_tol=1e-12),
        "centre3_near_zero": all(abs(v) < 1e-12 for v in centre3),
        "centre4_near_zero": all(abs(v) < 1e-12 for v in centre4),
        "gamma_closed": isclose(sum(mid), 1.0, abs_tol=1e-12),
        "derivative_tangent": isclose(sum(derivative), 0.0, abs_tol=1e-12),
        "mmb_closed": isclose(sum(mmb), 1.0, abs_tol=1e-12),
        "bias_bound_6": single_observer_bias_bound(1.0, 6),
        "mode_probability": product_probability_for_2d6_sums([7, 7, 7]),
        "platonic_vertex_matrix": PLATONIC_VERTEX_MATRIX,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(validate_fascicle_ii(), indent=2, sort_keys=True))
