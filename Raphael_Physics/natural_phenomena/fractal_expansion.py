"""Classic Raphael fractal expansion utilities.

This module is classic Raphael simulation support. It does not import N^3 or EML#F.
"""
from __future__ import annotations

import random
from typing import List, Tuple


def generate_fractal_3d(levels: int = 3, num_points: int = 1000, seed: int | None = 7) -> Tuple[List[float], List[float], List[float]]:
    if levels <= 0 or num_points <= 0:
        raise ValueError("levels and num_points must be positive")
    rng = random.Random(seed)
    x, y, z = [], [], []
    for level in range(levels):
        scale = 1.0 / (level + 1)
        count = num_points // levels + (1 if level < num_points % levels else 0)
        for _ in range(count):
            x.append(rng.uniform(-1, 1) * scale)
            y.append(rng.uniform(-1, 1) * scale)
            z.append(rng.uniform(-1, 1) * scale)
    return x, y, z


def mandelbrot_escape_counts(width: int, height: int, zoom: float = 1.0, max_iter: int = 50) -> list[list[int]]:
    if width <= 0 or height <= 0 or zoom <= 0 or max_iter <= 0:
        raise ValueError("width, height, zoom, and max_iter must be positive")
    rows = []
    for j in range(height):
        row = []
        y = (j / max(1, height - 1) * 4.0 - 2.0) / zoom
        for i in range(width):
            x = (i / max(1, width - 1) * 4.0 - 2.0) / zoom
            z = 0j
            c = complex(x, y)
            count = max_iter
            for k in range(max_iter):
                if abs(z) > 2.0:
                    count = k
                    break
                z = z * z + c
            row.append(count)
        rows.append(row)
    return rows
