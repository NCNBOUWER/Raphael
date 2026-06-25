"""Classic Raphael simulation controller."""
from __future__ import annotations

from natural_phenomena.fractal_expansion import generate_fractal_3d
from natural_phenomena.time_dynamics import cosmic_expansion, evolve_quantum_state


def run_simulation(kind: str, time_step: int = 1, num_points: int = 100) -> dict:
    if kind == "quantum":
        x, y, z, density = evolve_quantum_state(time_step, num_points)
        return {"kind": kind, "points": len(x), "density_mean": sum(density) / len(density)}
    if kind == "cosmic":
        x, y, z, scale = cosmic_expansion(time_step, num_points)
        return {"kind": kind, "points": len(x), "scale": scale}
    if kind in {"atomic", "galactic", "stellar", "fractal"}:
        x, y, z = generate_fractal_3d(levels=3, num_points=num_points)
        return {"kind": kind, "points": len(x), "z_min": min(z), "z_max": max(z)}
    raise ValueError(f"unknown simulation kind: {kind}")
