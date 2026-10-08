#!/usr/bin/env python3
"""CGX-F4D multi-stage route demonstrator v0.2.

Candidate route analysis only. No hardware control, simulation engine,
physical qualification, or production authorisation is implemented.
All numerical fixture doses are synthetic software-test values.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def read_json(path):
    with open(path, "r", encoding="utf-8") as stream:
        return json.load(stream)


def validate_catalog(catalog):
    families = {f["id"] for f in catalog["families"]}
    pairs = {(p["from"], p["to"]): p for p in catalog["pairs"]}
    if len(families) != 14 or len(pairs) != 196:
        raise ValueError("Expected 14 distinct families and 196 directional pairs")
    if set(pairs) != {(a, b) for a in families for b in families}:
        raise ValueError("Pair catalog does not cover the ordered Cartesian product")
    return families, pairs


def validate_contract(contract, families):
    if contract.get("production_approved") is not False:
        raise ValueError("Demonstrator only accepts production_approved=false")
    stages = contract.get("stages", [])
    features = contract.get("features", [])
    ids = [s["id"] for s in stages]
    fids = [f["id"] for f in features]
    if len(ids) != len(set(ids)) or len(fids) != len(set(fids)):
        raise ValueError("Duplicate stage or feature identifier")
    if not stages or len(stages) > 14:
        raise ValueError("Stage count must be between 1 and 14")
    for s in stages:
        if s.get("family") is not None and s["family"] not in families:
            raise ValueError("Unknown family: " + str(s.get("family")))
        if any(d not in ids or d == s["id"] for d in s.get("after", [])):
            raise ValueError("Invalid dependency in " + s["id"])
        for fid, channel_doses in s.get("exposures", {}).items():
            if fid not in fids:
                raise ValueError("Unknown exposed feature " + fid)
            for value in channel_doses.values():
                if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                    raise ValueError("Exposure dose must be finite, numeric and nonnegative")
    created = []
    for f in features:
        if f["family"] not in families or f["created_by"] not in ids:
            raise ValueError("Invalid feature source or family")
        if f["id"] not in next(s for s in stages if s["id"] == f["created_by"]).get("creates", []):
            raise ValueError("Feature creation contract mismatch: " + f["id"])
        created.append(f["id"])
        for channel, budget in f.get("budgets", {}).items():
            if channel not in contract.get("channels", {}):
                raise ValueError("Unregistered exposure channel: " + channel)
            if contract["channels"][channel].get("aggregation") != "additive":
                raise ValueError("Only explicitly additive exposure channels are supported")
            if not isinstance(budget, (int, float)) or not math.isfinite(budget) or budget < 0:
                raise ValueError("Invalid budget for " + f["id"])
    for s in stages:
        for fid in s.get("creates", []):
            if fid not in created:
                raise ValueError("Undeclared created feature: " + fid)
    return {s["id"]: s for s in stages}, {f["id"]: f for f in features}


def enumerate_orders(stages, max_orders=128):
    """Enumerate bounded topological orders; does not silently assert exhaustiveness."""
    ids = sorted(stages)
    orders = []
    def visit(prefix, completed):
        if len(orders) >= max_orders:
            return
        if len(prefix) == len(ids):
            orders.append(list(prefix))
            return
        for stage_id in ids:
            if stage_id not in completed and set(stages[stage_id].get("after", [])) <= completed:
                visit(prefix + [stage_id], completed | {stage_id})
    visit([], set())
    if not orders:
        raise ValueError("Dependency graph has a cycle or cannot be scheduled")
    truncated = len(orders) == max_orders
    return orders, truncated


def evaluate_order(contract, stages, features, pairs, order):
    active = {}
    cumulative = {}
    gates = set()
    previous_family = None
    pair_edges = []
    violations = []
    unknowns = []
    for stage_id in order:
        step = stages[stage_id]
        for required in step.get("requires_gates", []):
            if required not in gates:
                violations.append(f"{stage_id}: required gate {required} not established by an earlier stage")
        if step.get("operation") == "atmosphere_refill":
            for fid, feature in active.items():
                if feature.get("protected_atmosphere_required"):
                    for mandatory in ("barrier_closed", "barrier_integrity_checked"):
                        if mandatory not in gates:
                            violations.append(f"{stage_id}: {fid} unprotected; missing {mandatory}")
        for fid, feature in active.items():
            doses = step.get("exposures", {}).get(fid, {})
            for channel, budget in feature.get("budgets", {}).items():
                if channel not in doses:
                    unknowns.append(f"{stage_id}: missing {channel} exposure for {fid}")
                    continue
                cumulative[fid][channel] += doses[channel]
                if cumulative[fid][channel] > budget + 1e-12:
                    violations.append(
                        f"{stage_id}: {fid}/{channel} dose {cumulative[fid][channel]:g} exceeds budget {budget:g}"
                    )
        family = step.get("family")
        if family and previous_family:
            pair = pairs[(previous_family, family)]
            route_class = pair["route_class"]
            pair_edges.append({
                "from": previous_family, "to": family,
                "pair_id": pair["pair_id"], "route_class": route_class,
                "transition": step.get("transition"),
            })
            if route_class in {"T", "M", "R"} and not step.get("transition"):
                unknowns.append(f"{stage_id}: {route_class} transition strategy not specified")
            if route_class == "R":
                unknowns.append(f"{stage_id}: research-class route requires independent feasibility proof")
        if family:
            previous_family = family
        for fid in step.get("creates", []):
            active[fid] = features[fid]
            cumulative[fid] = {channel: 0.0 for channel in features[fid].get("budgets", {})}
        gates.update(step.get("produces_gates", []))
    if violations:
        status = "REJECT_CANDIDATE"
    elif unknowns:
        status = "NEEDS_EVIDENCE"
    else:
        status = "CANDIDATE_ONLY"
    return {
        "order": order, "status": status, "violations": sorted(set(violations)),
        "unknowns": sorted(set(unknowns)), "pair_edges": pair_edges,
        "cumulative_exposure": cumulative,
        "production_approved": False,
    }


def evaluate_contract(catalog, contract, max_orders=128):
    families, pairs = validate_catalog(catalog)
    stages, features = validate_contract(contract, families)
    orders, truncated = enumerate_orders(stages, max_orders=max_orders)
    results = [evaluate_order(contract, stages, features, pairs, order) for order in orders]
    priority = {"CANDIDATE_ONLY": 0, "NEEDS_EVIDENCE": 1, "REJECT_CANDIDATE": 2}
    results.sort(key=lambda x: (priority[x["status"]], len(x["unknowns"]), len(x["violations"]), x["order"]))
    return {
        "schema": "cgx.printspace.multistage_route_evaluation.v0.2",
        "contract_id": contract["id"],
        "evaluated_orders": len(orders),
        "bounded_search_truncated": truncated,
        "best_candidates": results[:min(5, len(results))],
        "status_counts": {name: sum(r["status"] == name for r in results)
                          for name in ("CANDIDATE_ONLY", "NEEDS_EVIDENCE", "REJECT_CANDIDATE")},
        "physical_tested": False,
        "production_approved": False,
        "note": "Graph and synthetic exposure accounting only: not constitutive modelling or machine authorisation",
    }


def main():
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=str(folder / "PAIRWISE_SEQUENCE_ROUTES_v0_1.json"))
    parser.add_argument("--cases", default=str(folder / "MULTISTAGE_ROUTE_TEST_CASES_v0_2.json"))
    parser.add_argument("--case", help="optional contract ID")
    parser.add_argument("--max-orders", type=int, default=128)
    args = parser.parse_args()
    if args.max_orders < 1:
        parser.error("--max-orders must be positive")
    catalog = read_json(args.catalog)
    cases = read_json(args.cases)["cases"]
    report = [
        evaluate_contract(catalog, item, args.max_orders)
        for item in cases if not args.case or item["id"] == args.case
    ]
    if args.case and not report:
        parser.error("Unknown case ID")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
