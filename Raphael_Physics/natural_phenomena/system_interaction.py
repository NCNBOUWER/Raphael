"""Classic Raphael system interaction helpers."""
from __future__ import annotations


def ecosystem_to_climate_feedback(biomass: float, heat: float, moisture: float) -> dict:
    if biomass < 0 or moisture < 0:
        raise ValueError("biomass and moisture must be non-negative")
    coherence = biomass * moisture / (1.0 + abs(heat))
    turbulence = abs(heat) / (1.0 + biomass + moisture)
    return {
        "coherence": coherence,
        "turbulence": turbulence,
        "net_feedback": coherence - turbulence,
    }
