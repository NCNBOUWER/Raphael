"""Read-only Raphael T173 → PrintSpace reference projection.

Imports PR7 reviewed *source data* by file/commit, without owning mesh bytes,
creating a geometry master, asserting scale-invariant physical meaning, minting,
or granting machine operations. CI pins PR7 source commit independently.
"""
from __future__ import annotations
import json
from pathlib import Path

SOURCE_REVIEW_COMMIT = "4ffebc85b1f945b83359c824c2165a98eb036c86"
SOURCE_PATH = "Raphael_Packages/geometry_173/showcase/analytic_reference_meshes_v05.json"


def _require(ok, reason):
    if not ok:
        raise ValueError(reason)


def project_t173(catalogue, source_meshes, *, source_commit=SOURCE_REVIEW_COMMIT):
    _require(type(catalogue) is dict and type(source_meshes) is dict, "invalid source")
    _require(source_commit == SOURCE_REVIEW_COMMIT, "unreviewed source commit")
    entries = catalogue.get("entries")
    _require(type(entries) is list and len(entries) == 173, "173 slot roles required")
    slots = [row.get("slot") for row in entries]
    _require(slots == list(range(1, 174)), "missing/duplicated/misordered slots")
    sentinel = catalogue.get("position_174", {})
    _require(sentinel.get("mintable") is False and sentinel.get("record") is False,
             "174 must stay nonmintable")
    meshes = source_meshes.get("meshes")
    aliases = source_meshes.get("aliases")
    _require(type(meshes) is dict and type(aliases) is dict, "mesh index required")
    _require(set(meshes).isdisjoint(aliases), "alias and mesh collision")
    _require(all(str(k).isdigit() and 1 <= int(k) <= 173 for k in meshes), "unknown mesh slot")
    _require(all(str(k).isdigit() and 1 <= int(k) <= 173 for k in aliases), "unknown alias slot")
    projection = {}
    for row in entries:
        slot = row["slot"]
        own = meshes.get(str(slot))
        target = aliases.get(str(slot))
        if target is not None:
            _require(type(target) is int and str(target) in meshes,
                     "alias points to missing or unreviewed mesh")
            own = meshes[str(target)]
        if own is None:
            continue
        _require(own.get("verified_euclidean_reference") is True,
                 "mesh is not a reviewed Euclidean reference")
        mhash = own.get("numerical_geometry_hash_sha256")
        _require(type(mhash) is str and len(mhash) == 64 and
                 all(c in "0123456789abcdef" for c in mhash),
                 "source geometry fingerprint missing")
        mesh_slot = target if target is not None else slot
        _require(type(own.get("vertices")) is list and
                 type(own.get("faces")) is list, "mesh vertices/faces missing")
        counts = own.get("counts", {})
        _require(len(own["vertices"]) == counts.get("V")
                 and len(own["faces"]) == counts.get("F"),
                 "source mesh count discrepancy")
        _require(own.get("Raphael_metric_admissibility") in ("UNTESTED", "NOT_TESTED"),
                 "metric assertion needs independent review")
        projection[str(slot)] = {
            "role_id": row["role_id"],
            "alias_of": target,
            "mesh_sha256": mhash,
            "source": ("NCNBOUWER/Raphael@" + source_commit + ":" + SOURCE_PATH),
            "unit": "normalised Euclidean reference (NOT manufacturing dimensions)",
            "evidence": "REFERENCE_EUCLIDEAN",
            "physical_qualification": False,
            "metric_qualification": False,
            "source_authentication": "CALLER_MUST_VERIFY_GIT_COMMIT_AND_BLOB",
            "geometry_role_id": row.get("canonical_geometry_id"),
            "mesh_slot": mesh_slot,
        }
    missing = [slot for slot in range(1, 174) if str(slot) not in projection]
    return {
        "schema": "cgx.printspace.t173_review_crosswalk.v0.1",
        "state": "DERIVED_REVIEW_ONLY_NOT_MACHINE_READY",
        "source_commit": source_commit,
        "source_roles": 173, "physical_qualified": 0,
        "mesh_reference_records": len(meshes),
        "shared_aliases": len(aliases), "mesh_backed_roles": len(projection),
        "unresolved_slots": missing, "projection": projection,
        "source_authentication": "TRUSTED_FETCH_ADAPTER_REQUIRED",
        "note": "One role per slot, aliases reuse source geometry; no Raphael metric or manufacturing proof",
    }


def load_t173_review_source(directory):
    """Load read-only local files supplied by independently verified checkout."""
    folder = Path(directory)
    cat = json.loads((folder / "catalogue.json").read_text(encoding="utf-8"))
    mesh = json.loads((folder / "showcase" /
                       "analytic_reference_meshes_v05.json").read_text(encoding="utf-8"))
    return project_t173(cat, mesh)
