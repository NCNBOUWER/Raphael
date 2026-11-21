from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATLAS_PATH = ROOT / "CROSS_GREX_PRODUCT_ATLAS_v0_5.json"
PRIMITIVES_PATH = ROOT / "CROSS_GREX_SHARED_PRIMITIVES_v0_5.json"
GAPS_PATH = ROOT / "CROSS_GREX_GAP_REGISTER_v0_5.json"
GRAPH_PATH = ROOT / "SHARED_MODULE_DEPENDENCY_GRAPH_v0_6.json"
PACKETS_PATH = ROOT / "DEMONSTRATOR_GATE_PACKETS_v0_6.json"
TARGET_PRODUCTS = ("FO-01", "FE-04")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_dependency_graph() -> dict:
    atlas = load_json(ATLAS_PATH)
    shared = load_json(PRIMITIVES_PATH)
    products = atlas["products"]
    registered = {row["technology_id"]: row for row in shared["records"]}

    usage: dict[str, list[str]] = defaultdict(list)
    edge_counts: Counter[tuple[str, str]] = Counter()
    edge_products: dict[tuple[str, str], list[str]] = defaultdict(list)

    for product in products:
        product_id = product["product_id"]
        refs = sorted(set(product["component_tech_refs"]))
        for ref in refs:
            usage[ref].append(product_id)
        for a, b in itertools.combinations(refs, 2):
            edge = (a, b)
            edge_counts[edge] += 1
            edge_products[edge].append(product_id)

    if set(usage) != set(registered):
        missing = sorted(set(registered) - set(usage))
        extra = sorted(set(usage) - set(registered))
        raise ValueError(f"primitive coverage mismatch missing={missing} extra={extra}")

    nodes = []
    for technology_id in sorted(registered):
        meta = registered[technology_id]
        product_ids = sorted(usage[technology_id])
        derived_count = len(product_ids)
        registered_count = int(meta["product_reuse_count"])
        if derived_count != registered_count:
            raise ValueError(
                f"reuse mismatch for {technology_id}: derived={derived_count} registered={registered_count}"
            )
        nodes.append(
            {
                "technology_id": technology_id,
                "canonical_function": meta["canonical_function"],
                "product_reuse_count": derived_count,
                "grex_domain_count": meta["grex_domain_count"],
                "grex_groups": meta["grex_groups"],
                "products": product_ids,
                "physical_qualified": bool(meta.get("physical_qualified", False)),
                "rank_basis": "product_reuse_count_only",
            }
        )

    nodes.sort(key=lambda row: (-row["product_reuse_count"], row["technology_id"]))
    for rank, node in enumerate(nodes, start=1):
        node["reuse_rank"] = rank

    edges = [
        {
            "a": a,
            "b": b,
            "product_cooccurrence_count": count,
            "products": sorted(edge_products[(a, b)]),
            "physical_interchangeability_verified": False,
            "meaning": "co-occurrence dependency signal only; not proof of shared geometry, interface or part interchangeability",
        }
        for (a, b), count in edge_counts.items()
    ]
    edges.sort(key=lambda row: (-row["product_cooccurrence_count"], row["a"], row["b"]))
    for rank, edge in enumerate(edges, start=1):
        edge["cooccurrence_rank"] = rank

    return {
        "schema": "cgx.printspace.shared_module_dependency_graph.v0.6",
        "id": "CGX-F4D-SHARED-DEPENDENCY-20261008",
        "status": "DERIVED_ONLY_OWNER_REVIEW",
        "source_atlas": atlas["id"],
        "source_shared_primitives": shared["id"],
        "product_count": len(products),
        "primitive_count": len(nodes),
        "edge_count": len(edges),
        "ranking_rule": "nodes by product reuse count; edges by product co-occurrence count",
        "nodes": nodes,
        "edges": edges,
        "constraints": [
            "Reuse ranking prioritises evidence and interface work; it does not imply physical interchangeability.",
            "All physical qualification flags remain inherited from the source primitive register.",
            "No material property, supplier part, geometry tolerance, process window or production permission is inferred.",
        ],
    }


def build_demonstrator_packets(graph: dict) -> dict:
    atlas = load_json(ATLAS_PATH)
    gap_register = load_json(GAPS_PATH)
    by_product = {row["product_id"]: row for row in atlas["products"]}
    gap_by_product: dict[str, list[dict]] = defaultdict(list)
    for ticket in gap_register["tickets"]:
        gap_by_product[ticket["product_id"]].append(ticket)

    packets = []
    for product_id in TARGET_PRODUCTS:
        product = by_product[product_id]
        stages = product["bottom_up"]["stages"]
        packets.append(
            {
                "product_id": product_id,
                "name": product["name"],
                "category": product["category"],
                "primary_grex": product["primary_grex"],
                "status": "INTEGRATED_DEMONSTRATOR_GATE_PACKET / DIGITAL_ONLY",
                "functional_contract": product["functional_contract"],
                "technology_ids": product["component_tech_refs"],
                "component_functions": product["component_functions"],
                "hybrid_insert_candidates": product["top_down"]["hybrid_required"],
                "system_acceptance_tests": product["top_down"]["system_acceptance_tests"],
                "material_family_path": product["bottom_up"]["material_family_path"],
                "material_seed_refs": product["bottom_up"]["material_seed_refs"],
                "environment_opportunity_ids": product["bottom_up"]["environment_opportunity_ids"],
                "stages": stages,
                "gap_tickets": gap_by_product[product_id],
                "selection_state": {
                    "exact_supplier_parts": [],
                    "supplier_lot_passports": [],
                    "resolved_geometry_tolerances": [],
                    "measured_property_receipts": [],
                    "qualified_machine_cells": [],
                    "cad_revision": None,
                },
                "gates": {
                    "all_stages_design_only": all(
                        stage.get("stage_status") == "DESIGN_ONLY_NOT_RUN" for stage in stages
                    ),
                    "physical_recipe_verified": False,
                    "physical_tested": bool(product.get("physical_tested", False)),
                    "production_approved": bool(product.get("production_approved", False)),
                    "hardware_safety_authority": product.get("hardware_safety_authority"),
                    "owner_review_required": product.get("governance_stage") == "OWNER_REVIEW_REQUIRED",
                },
                "next_independent_proofs": [
                    "Select exact sourced-versus-print-research module choices with part/passport identity.",
                    "Bind one CAD revision and SI geometry/tolerance set.",
                    "Populate only source-traceable or measured material operands with uncertainty.",
                    "Run coupon sequence for each directional interface and cumulative-exposure gate.",
                    "Run system acceptance tests only after component and C0 safety gates pass.",
                ],
            }
        )

    a = set(by_product[TARGET_PRODUCTS[0]]["component_tech_refs"])
    b = set(by_product[TARGET_PRODUCTS[1]]["component_tech_refs"])
    shared_ids = sorted(a & b)
    node_by_id = {row["technology_id"]: row for row in graph["nodes"]}

    return {
        "schema": "cgx.printspace.demonstrator_gate_packets.v0.6",
        "id": "CGX-F4D-DEMONSTRATORS-20261008",
        "status": "DIGITAL_ONLY_OWNER_REVIEW",
        "source_atlas": atlas["id"],
        "source_gap_register": gap_register["id"],
        "dependency_graph": graph["id"],
        "packets": packets,
        "cross_demonstrator_reuse": {
            "products": list(TARGET_PRODUCTS),
            "shared_technology_ids": shared_ids,
            "shared_primitives": [node_by_id[x] for x in shared_ids],
            "physical_interchangeability_verified": False,
        },
        "authority_boundary": {
            "machine_control": False,
            "physical_actuation": False,
            "production_release": False,
            "semantic_authority_transfer": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the two derived JSON artifacts")
    args = parser.parse_args()

    graph = build_dependency_graph()
    packets = build_demonstrator_packets(graph)
    if args.write:
        GRAPH_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        PACKETS_PATH.write_text(json.dumps(packets, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = {
        "product_count": graph["product_count"],
        "primitive_count": graph["primitive_count"],
        "edge_count": graph["edge_count"],
        "top_reuse": [
            {
                "technology_id": row["technology_id"],
                "function": row["canonical_function"],
                "product_reuse_count": row["product_reuse_count"],
            }
            for row in graph["nodes"][:10]
        ],
        "demonstrators": [
            {
                "product_id": row["product_id"],
                "name": row["name"],
                "technology_count": len(row["technology_ids"]),
                "stage_count": len(row["stages"]),
                "gap_count": len(row["gap_tickets"]),
            }
            for row in packets["packets"]
        ],
        "shared_technology_ids": packets["cross_demonstrator_reuse"]["shared_technology_ids"],
        "physical_interchangeability_verified": False,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
