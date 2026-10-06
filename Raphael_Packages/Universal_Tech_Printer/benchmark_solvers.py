"""Closed-form benchmark solvers for UTP regression.

These are deliberately narrow analytic comparators, not general-purpose CFD,
FEM, electromagnetics or materials solvers.
"""
from __future__ import annotations

from math import pi

MU0 = 4e-7 * pi


def hagen_poiseuille_delta_p(mu_pa_s: float, length_m: float, flow_m3_s: float, radius_m: float) -> float:
    if mu_pa_s <= 0 or length_m <= 0 or radius_m <= 0:
        raise ValueError("mu, length and radius must be positive")
    return 8.0 * mu_pa_s * length_m * flow_m3_s / (pi * radius_m ** 4)


def steady_conduction_heat_rate(k_w_mk: float, area_m2: float, delta_t_k: float, length_m: float) -> float:
    if k_w_mk <= 0 or area_m2 <= 0 or length_m <= 0:
        raise ValueError("k, area and length must be positive")
    return k_w_mk * area_m2 * delta_t_k / length_m


def thermal_resistance(k_w_mk: float, area_m2: float, length_m: float) -> float:
    if k_w_mk <= 0 or area_m2 <= 0 or length_m <= 0:
        raise ValueError("k, area and length must be positive")
    return length_m / (k_w_mk * area_m2)


def parallel_plate_capacitance(permittivity_f_m: float, area_m2: float, gap_m: float) -> float:
    if permittivity_f_m <= 0 or area_m2 <= 0 or gap_m <= 0:
        raise ValueError("permittivity, area and gap must be positive")
    return permittivity_f_m * area_m2 / gap_m


def capacitor_energy_j(capacitance_f: float, voltage_v: float) -> float:
    if capacitance_f < 0:
        raise ValueError("capacitance must be non-negative")
    return 0.5 * capacitance_f * voltage_v * voltage_v


def ideal_long_solenoid_b_t(turns_per_m: float, current_a: float, relative_permeability: float = 1.0) -> float:
    if turns_per_m < 0 or relative_permeability <= 0:
        raise ValueError("turns_per_m must be non-negative and relative_permeability positive")
    return MU0 * relative_permeability * turns_per_m * current_a


def steady_fick_flux_mol_m2_s(diffusivity_m2_s: float, concentration_drop_mol_m3: float, length_m: float) -> float:
    if diffusivity_m2_s < 0 or length_m <= 0:
        raise ValueError("diffusivity must be non-negative and length positive")
    return diffusivity_m2_s * concentration_drop_mol_m3 / length_m
