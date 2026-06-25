"""Classic Raphael equation placeholders.

These remain classic/current simulation helpers and intentionally do not import N^3 or EML#F.
The force functions are labelled surrogate utilities, not final physical proofs.
"""
from __future__ import annotations


def calculate_raphael_equations(protons: float, neutrons: float, electrons: float) -> dict:
    if protons < 0 or neutrons < 0 or electrons < 0:
        raise ValueError("particle counts must be non-negative")
    strong = 0.8 * protons * neutrons / (protons + neutrons) if (protons + neutrons) else 0.0
    weak = 0.2 * protons * electrons / (protons + electrons) if (protons + electrons) else 0.0
    return {"Strong Force": strong, "Weak Force": weak, "Total Energy": strong + weak}


if __name__ == "__main__":
    print(calculate_raphael_equations(2, 2, 2))
