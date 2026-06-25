"""EML#F alignment utilities.

This module implements the EML operator as an external-source derivation grammar.
It is not an N^3 proof module and is not a Raphael-Lite runtime.
"""
from __future__ import annotations

from math import exp, log, isfinite
from typing import Iterable, List, Sequence, Tuple


def eml(x: float, y: float) -> float:
    """Return exp(x) - ln(y)."""
    if y <= 0:
        raise ValueError("EML second argument must be positive for ln(y).")
    return exp(x) - log(y)


def activation_suppression(r: float, alpha: float, beta: float) -> float:
    """M1(R) = eml(alpha ln R, exp(beta R)) = R**alpha - beta*R."""
    if r <= 0:
        raise ValueError("R must be positive for ln(R).")
    return eml(alpha * log(r), exp(beta * r))


def activation_suppression_expanded(r: float, alpha: float, beta: float) -> float:
    if r <= 0:
        raise ValueError("R must be positive.")
    return (r ** alpha) - beta * r


def optimum_r(alpha: float, beta: float) -> float:
    if not (0 < alpha < 1):
        raise ValueError("Internal optimum requires 0 < alpha < 1.")
    if beta <= 0:
        raise ValueError("beta must be positive.")
    return (beta / alpha) ** (1.0 / (alpha - 1.0))


def hill_response(r: float, vmax: float, k: float, n: float) -> float:
    if r < 0 or vmax < 0 or k <= 0 or n <= 0:
        raise ValueError("Invalid Hill parameters.")
    rn = r ** n
    return vmax * rn / (k ** n + rn)


def rmse(predicted: Sequence[float], observed: Sequence[float]) -> float:
    if len(predicted) != len(observed) or not predicted:
        raise ValueError("RMSE inputs must be same non-zero length.")
    return (sum((p - o) ** 2 for p, o in zip(predicted, observed)) / len(predicted)) ** 0.5


def fit_eml_grid(x: Sequence[float], y: Sequence[float], alphas: Iterable[float], betas: Iterable[float]) -> Tuple[float, float, float]:
    best = None
    for a in alphas:
        for b in betas:
            pred = [activation_suppression_expanded(v, a, b) for v in x]
            score = rmse(pred, y)
            if best is None or score < best[2]:
                best = (a, b, score)
    if best is None:
        raise RuntimeError("No valid EML fit candidates.")
    return best


def fit_hill_grid(x: Sequence[float], y: Sequence[float], vmaxs: Iterable[float], ks: Iterable[float], ns: Iterable[float]) -> Tuple[float, float, float, float]:
    best = None
    for vmax in vmaxs:
        for k in ks:
            for n in ns:
                pred = [hill_response(v, vmax, k, n) for v in x]
                score = rmse(pred, y)
                if best is None or score < best[3]:
                    best = (vmax, k, n, score)
    if best is None:
        raise RuntimeError("No valid Hill fit candidates.")
    return best


def cascade_basis(t: Sequence[float], depth: int, tau: float = 1.0) -> List[List[float]]:
    if depth <= 0 or tau <= 0:
        raise ValueError("depth and tau must be positive.")
    basis = []
    for k in range(depth):
        row = []
        for value in t:
            if value < 0:
                raise ValueError("time values must be non-negative.")
            row.append((value ** k) * exp(-value / tau))
        basis.append(row)
    return basis


def validate_emlf() -> dict:
    xs = [0.2, 0.4, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0, 5.0]
    ys = [activation_suppression_expanded(x, 0.55, 0.32) for x in xs]
    eml_fit = fit_eml_grid(xs, ys, [i / 100 for i in range(35, 76, 2)], [i / 100 for i in range(18, 51, 2)])
    hill_fit = fit_hill_grid(xs, ys, [i / 10 for i in range(1, 21)], [i / 10 for i in range(1, 31)], [0.5, 1.0, 2.0, 3.0])
    basis = cascade_basis([0, 1, 2, 3], 3, tau=2.0)
    return {
        "operator_identity_value": eml(2.0, exp(3.0)),
        "operator_identity_expected": exp(2.0) - 3.0,
        "m1_operator_value": activation_suppression(2.0, 0.55, 0.32),
        "m1_expanded_value": activation_suppression_expanded(2.0, 0.55, 0.32),
        "optimum_r": optimum_r(0.55, 0.32),
        "eml_fit_alpha": eml_fit[0],
        "eml_fit_beta": eml_fit[1],
        "eml_fit_rmse": eml_fit[2],
        "hill_fit_rmse": hill_fit[3],
        "eml_beats_hill_on_nonmonotone_data": eml_fit[2] < hill_fit[3],
        "cascade_depth": len(basis),
        "cascade_time_points": len(basis[0]),
        "all_values_finite": all(isfinite(v) for row in basis for v in row),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(validate_emlf(), indent=2, sort_keys=True))
