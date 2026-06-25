"""Classic Raphael time-dynamics utilities.

No N^3 or EML#F imports.
"""
from __future__ import annotations

import math
from typing import List, Tuple


def evolve_quantum_state(time_step: int = 1, num_points: int = 100) -> Tuple[List[float], List[float], List[float], List[float]]:
    if num_points <= 0:
        raise ValueError("num_points must be positive")
    x, y, z, density = [], [], [], []
    phase = time_step * 0.05
    for i in range(num_points):
        u = i / max(1, num_points - 1)
        angle = 2 * math.pi * u + phase
        radius = 0.5 + 0.5 * math.sin(3 * angle)
        x.append(radius * math.cos(angle))
        y.append(radius * math.sin(angle))
        z.append(math.sin(angle + phase) * 0.25)
        density.append(radius * radius)
    return x, y, z, density


def cosmic_expansion(time_step: int = 1, num_points: int = 100) -> Tuple[List[float], List[float], List[float], float]:
    if num_points <= 0:
        raise ValueError("num_points must be positive")
    scale = 1.0 + 0.01 * time_step
    x, y, z = [], [], []
    for i in range(num_points):
        u = (i + 0.5) / num_points
        theta = 2 * math.pi * u
        phi = math.acos(1 - 2 * u)
        x.append(scale * math.sin(phi) * math.cos(theta))
        y.append(scale * math.sin(phi) * math.sin(theta))
        z.append(scale * math.cos(phi))
    return x, y, z, scale
