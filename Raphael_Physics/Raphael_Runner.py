"""Classic Raphael command-line runner.

Validates the classic simulation core without importing N^3 or EML#F.
"""
from __future__ import annotations

import argparse
import json
from Simulations.simulation_controller import run_simulation
from natural_phenomena.system_interaction import ecosystem_to_climate_feedback
from raphael_equations import calculate_raphael_equations


def run_all() -> dict:
    return {
        "atomic": run_simulation("atomic", num_points=64),
        "cosmic": run_simulation("cosmic", time_step=12, num_points=64),
        "quantum": run_simulation("quantum", time_step=12, num_points=64),
        "feedback": ecosystem_to_climate_feedback(2.0, 0.5, 0.8),
        "helium_surrogate": calculate_raphael_equations(2, 2, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    report = run_all()
    if args.validate:
        assert report["atomic"]["points"] == 64
        assert report["cosmic"]["scale"] > 1.0
        assert report["quantum"]["density_mean"] > 0
        assert report["helium_surrogate"]["Total Energy"] > 0
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
