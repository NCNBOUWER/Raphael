"""PrintCeptor inverse build decomposition -- SOURCE/CANDIDATE-ONLY, never machine control.

Reverse AND dependency tree and per-component OR manufacturing/sourcing routes.
No absent prices, material qualification or robot functionality may be inferred.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_GRAPH = HERE / "PRINTCEPTOR_INVERSE_BUILD_GRAPH_v0_1.json"
PRIORITIES = {
    "sourcing": ("PRINT", "SALVAGE", "REUSE", "HYBRID", "HAND", "BUY", "ASSEMBLE", "QUALIFY"),
    "simple": ("BUY", "REUSE", "SALVAGE", "HYBRID", "PRINT", "HAND", "ASSEMBLE", "QUALIFY"),
    "learning": ("HAND", "PRINT", "HYBRID", "SALVAGE", "REUSE", "BUY", "ASSEMBLE", "QUALIFY"),
}

def load_graph(path=DEFAULT_GRAPH):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == "cgx.printspace.inverse_build_graph.v0.1"
    ids = [x["id"] for x in data["components"]]
    assert len(ids) == len(set(ids)), "duplicate component IDs"
    lookup = set(ids)
    for part in data["components"]:
        assert part["options"], part["id"]
        assert part["id"] not in part["needs"]
        for dep in part["needs"]:
            assert dep in lookup, (part["id"], dep)
        for option in part["options"]:
            assert option["evidence"] == "CANDIDATE_ONLY"
            assert option["cost_aud"] is None, "cost cannot be synthesized"
    kid = [x["id"] for x in data["starter_kits"]]
    assert len(kid) == len(set(kid))
    return data

def evaluate(data, kit_id="K-FDM", goal="BB-FINAL", priority="sourcing"):
    """Return an auditable route plan; 'candidate' is not 'available/qualified'.

    Salvage paths never imply a device is owned or a removed safety interlock is valid.
    """
    kits = {k["id"]: k for k in data["starter_kits"]}
    nodes = {p["id"]: p for p in data["components"]}
    kit = kits[kit_id]
    caps = set(kit["capabilities"])
    rank = {x: i for i, x in enumerate(PRIORITIES[priority])}
    ordered = []
    route_options = {}
    seen, visiting = set(), set()
    def visit(part_id):
        if part_id in seen:
            return
        if part_id in visiting:
            raise ValueError("dependency cycle: " + part_id)
        visiting.add(part_id)
        part = nodes[part_id]
        for dep in part["needs"]:
            visit(dep)
        variants = []
        for j, route in enumerate(part["options"], 1):
            missing = sorted(set(route["requires"]) - caps)
            variants.append({
                "route": route["mode"], "route_id": f"{part_id}-R{j}",
                "candidate_feasible_given_tool_labels": not missing,
                "missing_capabilities": missing,
                "sourced_seed_components": route["external_seed_components"],
                "physical_qualification": "NOT_VERIFIED",
                "cost_aud": None, "reason": route["technical_note"],
            })
        variants.sort(key=lambda x: (len(x["missing_capabilities"]) > 0,
                     len(x["missing_capabilities"]), rank.get(x["route"], 99),
                     len(x["sourced_seed_components"]), x["route_id"]))
        pick = variants[0]
        route_options[part_id] = {
            "part": part["name"], "group": part["group"], "safety": part["safety"],
            "depends_on": part["needs"], "selected": pick, "all_alternatives": variants,
            "reason_log": "Candidate preference only; no measured lot, fixture, qualified process, purchased stock or cost evidence",
        }
        ordered.append(part_id)
        visiting.remove(part_id)
        seen.add(part_id)
    visit(goal)
    blocked = [n for n in ordered if route_options[n]["selected"]["missing_capabilities"]]
    unverified_sourced = [{
        "node": n,
        "input_components_to_find_test_or_buy": route_options[n]["selected"]["sourced_seed_components"],
        "ownership": "UNKNOWN",
        "technical_equivalence": "NOT_VERIFIED",
    } for n in ordered if route_options[n]["selected"]["sourced_seed_components"]]
    critical_holds = [{
        "node": n,
        "risk_class": route_options[n]["safety"],
        "acceptance": "PHYSICAL_AND_OWNER_EVIDENCE_REQUIRED",
    } for n in ordered if route_options[n]["safety"] in ("CRITICAL", "SECURITY")]
    counts = Counter(route_options[n]["selected"]["route"] for n in ordered)
    known_priced = sum(item["aud"] for item in kit["known_price_observations"])
    acquisition_state = kit.get("acquisition_state", "GENERIC_SCENARIO_ASSUMPTIONS")
    inventory_based = bool(kit.get("inventory_link"))
    return {
        "goal": goal, "kit": kit_id, "priority": priority, "status": "CANDIDATE_ONLY_NO_HARDWARE_PROOF",
        "kit_acquisition_state": acquisition_state,
        "inventory_baseline": kit.get("inventory_link"),
        "post_purchase_capabilities_are_not_currently_installed": acquisition_state.startswith("POST_"),
        "assumed_inventory_is_not_verified": not inventory_based,
        "known_price_excludes_previously_owned_dremel_4300": inventory_based,
        "quoted_tool_items_not_yet_purchased": [q["label"] for q in kit["known_price_observations"]] if acquisition_state.startswith("POST_") else [],

        "single_sealed_session_qualified": False,
        "source_qualified": False,
        "tool_prices_aud_observed_sum_not_total_project_cost": round(known_priced, 2),
        "unpriced_kit_dependencies": kit["unpriced_dependencies"],
        "route_class_counts": dict(counts), "traversal_dependency_first": ordered,
        "unverified_sourced_parts": unverified_sourced,
        "critical_physical_safety_holds": critical_holds,
        "no_missing_capability_label_does_not_mean_build_ready": True,
        "candidate_blockers": [{"node": p, "missing_capabilities": route_options[p]["selected"]["missing_capabilities"]} for p in blocked],
        "decisions": route_options,
        "note": "A route whose capability labels match remains unqualified; no automatic BOM procurement or motion authority.",
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", default=str(DEFAULT_GRAPH))
    parser.add_argument("--kit", default="K-FDM")
    parser.add_argument("--goal", default="BB-FINAL")
    parser.add_argument("--priority", choices=tuple(PRIORITIES), default="sourcing")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args(argv)
    d = load_graph(args.graph)
    r = evaluate(d, args.kit, args.goal, args.priority)
    if args.summary:
        print(json.dumps({k: v for k, v in r.items() if k != "decisions"}, indent=2))
    else:
        print(json.dumps(r, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
