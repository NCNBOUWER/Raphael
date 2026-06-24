#!/usr/bin/env python3
"""Safe N^3 / Trinity Probability Well GeoMatrix harness.

Scope:
- finite 2d6 / N-variable probability checks;
- barycentric closure;
- convex polygon projection;
- piecewise-linear continuous trajectory bridge Γ;
- finite-difference velocity calculation.

Non-scope:
- does not prove hydrodynamics;
- does not prove quantum phase dynamics;
- does not prove gravity;
- does not rewrite private Raphael equations.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from fractions import Fraction
from itertools import product
from typing import List, Sequence, Tuple

SUM_SUPPORT = tuple(range(2, 13))
COUNT_BY_SUM = {s: 6 - abs(s - 7) for s in SUM_SUPPORT}


def two_dice_count(s: int) -> int:
    if s not in COUNT_BY_SUM:
        raise ValueError(f"2d6 sum must be in 2..12, got {s}")
    return COUNT_BY_SUM[s]


def joint_probability(state: Sequence[int]) -> Fraction:
    numerator = 1
    for s in state:
        numerator *= two_dice_count(int(s))
    return Fraction(numerator, 36 ** len(state))


def validate_tpw_core() -> dict:
    states = list(product(SUM_SUPPORT, repeat=3))
    probs = [joint_probability(s) for s in states]
    max_p = max(probs)
    min_p = min(probs)
    max_states = [s for s, p in zip(states, probs) if p == max_p]
    min_states = [s for s, p in zip(states, probs) if p == min_p]
    total = sum(probs, Fraction(0, 1))
    return {
        "sum_state_rows": len(states),
        "primitive_ordered_outcomes": 36 ** 3,
        "probability_sum": str(total),
        "probability_sum_float": float(total),
        "unique_mode": max_states == [(7, 7, 7)],
        "mode_states": max_states,
        "max_probability": str(max_p),
        "min_probability": str(min_p),
        "min_probability_state_count": len(min_states),
        "minimum_corner_states": min_states,
    }


def barycentric_closure(weights: Sequence[float]) -> Tuple[float, ...]:
    if not weights:
        raise ValueError("weights cannot be empty")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be nonnegative")
    total = float(sum(weights))
    if total == 0.0:
        raise ValueError("weight sum cannot be zero")
    return tuple(float(w) / total for w in weights)


def state_to_barycentric(state: Sequence[int]) -> Tuple[float, ...]:
    return barycentric_closure([two_dice_count(int(s)) for s in state])


def regular_polygon_vertices(k: int) -> Tuple[Tuple[float, float], ...]:
    if k < 3:
        raise ValueError("polygon requires k >= 3")
    return tuple((math.cos(2 * math.pi * i / k), math.sin(2 * math.pi * i / k)) for i in range(k))


def project_to_polygon(barycentric: Sequence[float]) -> Tuple[float, float]:
    b = barycentric_closure(barycentric)
    vertices = regular_polygon_vertices(len(b))
    x = sum(w * vx for w, (vx, _vy) in zip(b, vertices))
    y = sum(w * vy for w, (_vx, vy) in zip(b, vertices))
    return (x, y)


def gamma_interpolate(sequence: Sequence[Sequence[float]], samples_per_segment: int = 10) -> List[Tuple[float, ...]]:
    """Piecewise-linear Γ bridge over simplex states."""
    if samples_per_segment < 1:
        raise ValueError("samples_per_segment must be >= 1")
    if len(sequence) < 2:
        return [tuple(barycentric_closure(sequence[0]))] if sequence else []
    closed = [barycentric_closure(s) for s in sequence]
    dim = len(closed[0])
    if any(len(s) != dim for s in closed):
        raise ValueError("all states must share dimension")
    out: List[Tuple[float, ...]] = []
    for a, b in zip(closed[:-1], closed[1:]):
        for j in range(samples_per_segment):
            lam = j / samples_per_segment
            out.append(tuple((1 - lam) * a[i] + lam * b[i] for i in range(dim)))
    out.append(closed[-1])
    return out


def finite_difference_velocity(sequence: Sequence[Sequence[float]], h: float = 1.0) -> List[Tuple[float, ...]]:
    if h <= 0:
        raise ValueError("h must be positive")
    closed = [barycentric_closure(s) for s in sequence]
    return [tuple((b[i] - a[i]) / h for i in range(len(a))) for a, b in zip(closed[:-1], closed[1:])]


def random_2d6_sum() -> int:
    return random.randint(1, 6) + random.randint(1, 6)


def random_tpw_state(n: int = 3) -> Tuple[int, ...]:
    return tuple(random_2d6_sum() for _ in range(n))


def demo_sequence(length: int = 5, n: int = 3, seed: int | None = None) -> dict:
    if seed is not None:
        random.seed(seed)
    states = [random_tpw_state(n) for _ in range(length)]
    bary = [state_to_barycentric(s) for s in states]
    coords = [project_to_polygon(b) for b in bary]
    velocities = finite_difference_velocity(bary)
    return {
        "states": states,
        "barycentric": bary,
        "polygon_coordinates": coords,
        "finite_difference_velocities": velocities,
        "notice": "Mathematical simplex trajectory only; physical correspondence layer remains P5/audit pending.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe TPW GeoMatrix validation/demo harness")
    parser.add_argument("--validate", action="store_true", help="run TPW core validation")
    parser.add_argument("--demo", action="store_true", help="run a stochastic trajectory demo")
    parser.add_argument("--length", type=int, default=5, help="demo sequence length")
    parser.add_argument("--dimension", type=int, default=3, help="number of independent 2d6 variables")
    parser.add_argument("--seed", type=int, default=7, help="random seed for demo")
    args = parser.parse_args()

    payload = {}
    if args.validate or not args.demo:
        payload["validation"] = validate_tpw_core()
    if args.demo:
        payload["demo"] = demo_sequence(args.length, args.dimension, args.seed)

    print(json.dumps(payload, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
