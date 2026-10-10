"""UTP multiphysics interaction/compiler utilities.

Architecture and bookkeeping helpers only. This module does not implement a
general CFD, plasma, semiconductor, chemistry, FEM or quantum solver. It
selects and composes domain kernels and tests interaction-order assumptions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, isfinite
from typing import Dict, Iterable, List, Mapping, Sequence, Set


def normalize_nonnegative(values: Mapping[str, float]) -> Dict[str, float]:
    if not values:
        raise ValueError("values cannot be empty")
    if any(float(v) < 0 for v in values.values()):
        raise ValueError("values must be non-negative")
    total = float(sum(values.values()))
    if total <= 0:
        raise ValueError("sum(values) must be positive")
    return {k: float(v) / total for k, v in values.items()}


def boltzmann_weights(
    free_energies_j_per_mol: Mapping[str, float],
    temperature_k: float,
    gas_constant_j_per_mol_k: float = 8.31446261815324,
) -> Dict[str, float]:
    """Normalize Gibbs/free-energy candidates into thermodynamic weights.

    Intended for regimes where a Boltzmann/Gibbs equilibrium weighting is
    physically justified. It is not a replacement for kinetic/path models.
    """
    if temperature_k <= 0:
        raise ValueError("temperature_k must be positive")
    if gas_constant_j_per_mol_k <= 0:
        raise ValueError("gas constant must be positive")
    if not free_energies_j_per_mol:
        raise ValueError("at least one state is required")
    minimum = min(float(v) for v in free_energies_j_per_mol.values())
    raw = {
        k: exp(-(float(g) - minimum) / (gas_constant_j_per_mol_k * temperature_k))
        for k, g in free_energies_j_per_mol.items()
    }
    return normalize_nonnegative(raw)


def relative_residual(observed: Sequence[float], predicted: Sequence[float], eps: float = 1e-12) -> float:
    """L2 relative residual used to decide whether pair order is adequate."""
    if len(observed) != len(predicted) or not observed:
        raise ValueError("observed and predicted must be non-empty and equal length")
    num = sum((float(a) - float(b)) ** 2 for a, b in zip(observed, predicted)) ** 0.5
    den = max(sum(float(a) ** 2 for a in observed) ** 0.5, eps)
    return num / den


def interaction_order_gate(
    observed: Sequence[float],
    pair_prediction: Sequence[float],
    threshold: float,
) -> str:
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    r = relative_residual(observed, pair_prediction)
    return "PASS_PAIR" if r <= threshold else "PROMOTE_HIGHER_ORDER"


def pair_reconstruction(
    baseline: Sequence[float],
    self_effects: Iterable[Sequence[float]],
    pair_effects: Iterable[Sequence[float]],
) -> List[float]:
    """Additive reconstruction used only to *test* the pairwise hypothesis."""
    out = [float(x) for x in baseline]
    for effect in list(self_effects) + list(pair_effects):
        if len(effect) != len(out):
            raise ValueError("effect vector width mismatch")
        out = [a + float(b) for a, b in zip(out, effect)]
    return out


def dimensionless_groups(
    *,
    rho: float | None = None,
    velocity: float | None = None,
    length: float | None = None,
    viscosity: float | None = None,
    diffusivity: float | None = None,
    reaction_rate: float | None = None,
    surface_tension: float | None = None,
    mean_free_path: float | None = None,
) -> Dict[str, float]:
    """Compute only dimensionless groups supported by supplied inputs."""
    out: Dict[str, float] = {}
    if rho is not None and velocity is not None and length is not None and viscosity:
        out["Re"] = rho * velocity * length / viscosity
    if velocity is not None and length is not None and diffusivity:
        out["Pe"] = velocity * length / diffusivity
    if reaction_rate is not None and length is not None and velocity:
        out["Da_advective"] = reaction_rate * length / velocity
    if rho is not None and velocity is not None and length is not None and surface_tension:
        out["We"] = rho * velocity * velocity * length / surface_tension
    if viscosity is not None and velocity is not None and surface_tension:
        out["Ca"] = viscosity * velocity / surface_tension
    if mean_free_path is not None and length:
        out["Kn"] = mean_free_path / length
    if any(not isfinite(v) for v in out.values()):
        raise ValueError("non-finite dimensionless group")
    return out


KERNEL_BY_FEATURE = {
    "flow": {"K-FLUID-MASS", "K-FLUID-MOM", "K-ENERGY"},
    "species": {"K-SPECIES"},
    "reaction": {"K-SPECIES", "K-FREEENERGY"},
    "electric": {"K-MAXWELL"},
    "magnetic": {"K-MAXWELL"},
    "ionic": {"K-NP", "K-MAXWELL", "K-SPECIES"},
    "faradaic": {"K-NP", "K-BV", "K-MAXWELL", "K-SPECIES"},
    "phase_change": {"K-FREEENERGY", "K-CH", "K-AC", "K-ENERGY"},
    "mechanical": {"K-MECH"},
    "semiconductor": {"K-SEMI", "K-MAXWELL", "K-ENERGY"},
    "plasma": {"K-PLASMA", "K-MAXWELL", "K-ENERGY", "K-SPECIES"},
    "radiation": {"K-RADIATION"},
    "raphael_compare": {"K-CLOSURE", "K-RAPHAEL-OBW"},
}


def select_kernels(features: Iterable[str]) -> List[str]:
    selected: Set[str] = set()
    for feature in features:
        if feature not in KERNEL_BY_FEATURE:
            raise KeyError(f"unknown feature: {feature}")
        selected.update(KERNEL_BY_FEATURE[feature])
    return sorted(selected)


ENVIRONMENT_CAPABILITIES = {
    "ENV-0": {"ambient", "structural", "machining", "inspection", "cold_placement"},
    "ENV-1": {"ambient", "structural", "machining", "inspection", "cold_placement", "local_inert", "low_oxygen", "local_thermal", "solvent_capture"},
    "ENV-2": {"sealed_gas", "controlled_pressure", "low_pressure", "vacuum_after_evacuation", "electrochemical_sealing", "microplasma"},
    "ENV-3": {"macro_atmosphere", "macro_pressure", "macro_thermal"},
    "ENV-4": {"mobile_local_inert", "mobile_local_thermal", "mobile_feed", "mobile_metrology"},
}


def environment_supports(environment: str, requirements: Iterable[str]) -> bool:
    if environment not in ENVIRONMENT_CAPABILITIES:
        raise KeyError(f"unknown environment: {environment}")
    return set(requirements).issubset(ENVIRONMENT_CAPABILITIES[environment])


@dataclass
class BuildNode:
    node_id: str
    scale: str
    environment: str
    features: List[str] = field(default_factory=list)
    children: List["BuildNode"] = field(default_factory=list)

    def compile_kernel_map(self) -> Dict[str, List[str]]:
        out = {self.node_id: select_kernels(self.features)}
        for child in self.children:
            out.update(child.compile_kernel_map())
        return out

    def all_ids(self) -> List[str]:
        ids = [self.node_id]
        for child in self.children:
            ids.extend(child.all_ids())
        if len(ids) != len(set(ids)):
            raise ValueError("recursive build graph contains duplicate node ids")
        return ids


def compare_traditional_hybrid(
    traditional: Mapping[str, float],
    hybrid: Mapping[str, float],
    lower_is_better: Iterable[str],
) -> Dict[str, float]:
    """Return signed fractional improvement where positive means better.

    Metric definitions/weights belong to the caller; this function deliberately
    refuses to collapse unlike metrics into one universal score.
    """
    lower = set(lower_is_better)
    keys = set(traditional) & set(hybrid)
    out: Dict[str, float] = {}
    for k in sorted(keys):
        t = float(traditional[k])
        h = float(hybrid[k])
        if t == 0:
            raise ValueError(f"traditional baseline for {k} is zero")
        out[k] = (t - h) / abs(t) if k in lower else (h - t) / abs(t)
    return out
