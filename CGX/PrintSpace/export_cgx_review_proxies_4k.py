#!/usr/bin/env python3
"""Render already-owned Type-I SVG interaction proxies to private 3840x2160 review images.

This is a derived *presentation* export, NOT 3D CAD, a physical simulation,
a new renderer/geometry source, or an owner approval. Refuses changed source
hashes and input directories without the existing read-only 605-object receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

WIDTH, HEIGHT = 3840, 2160
SLUG = re.compile(r"^[a-z][a-z0-9_]{1,70}$")
EXPECTED_SCHEMA = "CGX-REVIEW-LENS-OFFLINE/0.1"
CLASSIFICATIONS = {
    ("INTERACTION_PROXY", "NONE", "NONE_PROXY_ONLY"),
    ("SOURCE_DERIVED_GEOMETRY", "DERIVED_MODEL_ENVELOPE_ONLY", "COMMITTED_DERIVATION_RECEIPT"),
    ("SOURCE_DERIVED_PARTIAL", "PARTIAL_DERIVED_MODEL_ENVELOPE_ONLY", "PARTIAL_DERIVATION_RECEIPT"),
}
EVIDENCE = "REVIEW_ONLY_NOT_VALIDATED_AS_BUILT_CAD"
ALLOWED = (
    "solar_hull", "free_flow_batteries", "free_flow_capacitors",
    "free_flow_solenoid_stack", "rfs_emff", "mark_1p", "mark_i",
    "mark_iii", "luke_family", "maglev_luke_iv", "embedded_bio_blocks",
    "second_cycle", "watchtower", "intersol", "m1_elevated_bypass",
    "romer_spaceport",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def svg_evidence(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    def attribute(name: str) -> str:
        value = re.search(r'\\b' + name + r'="([^"]*)"', raw)
        return value.group(1) if value else ""
    rec = {
        "representation_class": attribute("data-representation-class"),
        "dimension_authority": attribute("data-dimension-authority"),
        "source_binding_state": attribute("data-source-binding-state"),
        "release_eligible": attribute("data-release-eligible"),
    }
    triple = (rec["representation_class"], rec["dimension_authority"], rec["source_binding_state"])
    if triple not in CLASSIFICATIONS or rec["release_eligible"] != "false":
        raise ValueError(f"Not an accepted non-releasable engineering review asset: {path.name}")
    return rec


def validate_receipt(root: Path) -> tuple[dict, list[tuple[str, Path, dict[str, str]]]]:
    receipt = json.loads((root / "receipt.json").read_text(encoding="utf-8"))
    if receipt.get("schema") != EXPECTED_SCHEMA or receipt.get("item_total") != 605:
        raise ValueError("Required source-linked 605-object review receipt unavailable")
    if receipt.get("artifact") != "OFFLINE_LOCAL_REVIEW_ONLY":
        raise ValueError("Not an offline review-only package")
    out = []
    for slug in ALLOWED:
        if not SLUG.fullmatch(slug):
            raise ValueError("Unexpected SVG slug")
        file = root / "assets" / f"{slug}.svg"
        if not file.is_file():
            raise FileNotFoundError(file)
        relative = f"assets/{slug}.svg"
        stored = receipt["files"].get(relative, receipt["files"].get(relative.replace("/", "\\")))
        if stored != sha256(file):
            raise ValueError(f"SVG source drift: {slug}")
        evidence = svg_evidence(file)
        out.append((slug, file, evidence))
    return receipt, out


def wrapper(slug: str, relative_svg: str, evidence: dict | None = None) -> str:
    if not SLUG.fullmatch(slug):
        raise ValueError("Unsafe slug")
    label = slug.replace("_", " ").title()
    evidence = evidence or {
        "representation_class": "INTERACTION_PROXY", "dimension_authority": "NONE"
    }
    declared = evidence.get("representation_class", "UNKNOWN")
    dimensional = evidence.get("dimension_authority", "UNKNOWN")
    caution = " / ".join((declared.replace("_", " "), dimensional.replace("_", " ")))
    image_ref = html.escape(relative_svg, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; connect-src 'none'">
<style>
*{{box-sizing:border-box}}html,body{{margin:0;width:{WIDTH}px;height:{HEIGHT}px;overflow:hidden}}
body{{color:#eaf1f0;background:linear-gradient(135deg,#090f14,#111e24);font:44px 'Segoe UI',Arial,sans-serif}}
header{{height:212px;padding:44px 110px;display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid #e57e29}}
.brand{{font-size:44px;letter-spacing:9px;color:#f1ae69;font-weight:800}}.id{{font-size:30px;color:#aab6b9}}
main{{height:1780px;display:flex;align-items:center;justify-content:center;padding:48px 70px}}
.panel{{width:100%;height:100%;border:2px solid #39505b;border-radius:34px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#07141a}}
.panel img{{object-fit:contain;width:100%;height:100%}}
footer{{height:168px;display:flex;align-items:center;justify-content:space-between;padding:20px 110px;border-top:2px solid #39505b}}
.name{{font-weight:700;font-size:51px}}.hold{{font-size:28px;color:#ffc28f;max-width:70%;text-align:right}}
</style></head><body><header><div class="brand">CGX / RÖMER / PRINTSPACE</div><div class="id">SOURCE-DERIVED VISUAL · 3840 × 2160</div></header>
<main><section class="panel"><img src="{image_ref}" alt="Historical engineering interaction proxy for {html.escape(label,quote=True)}"></section></main>
<footer><span class="name">{html.escape(label)}</span><span class="hold">{html.escape(caution)} — NOT VERIFIED AS-BUILT CAD OR PERFORMANCE</span></footer></body></html>"""


def render(root: Path, executable: Path, *, limit: int | None = None) -> dict:
    if not executable.is_file():
        raise FileNotFoundError(f"Browser executable missing: {executable}")
    source_receipt, pairs = validate_receipt(root)
    if limit is not None:
        if limit < 1 or limit > len(pairs):
            raise ValueError("Limit outside existing asset set")
        pairs = pairs[:limit]
    dest = root / "review_4k"
    dest.mkdir(exist_ok=True)
    snapshots = []
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow required for output geometry verification") from exc
    for slug, source, evidence in pairs:
        page = dest / f"{slug}.html"
        image = dest / f"{slug}.png"
        if page.exists() or image.exists():
            raise FileExistsError(f"Existing derived render held (no overwrites): {slug}")
        page.write_text(wrapper(slug, f"../assets/{slug}.svg", evidence), encoding="utf-8")
        result = subprocess.run(
            [
                str(executable), "--headless", "--disable-extensions",
                "--disable-background-networking", "--hide-scrollbars",
                "--no-first-run", "--force-device-scale-factor=1",
                f"--window-size={WIDTH},{HEIGHT}",
                f"--screenshot={image}", page.resolve().as_uri(),
            ],
            capture_output=True, text=True, timeout=75, check=False,
        )
        if result.returncode != 0 or not image.is_file():
            raise RuntimeError(f"Browser render failed for {slug}: {result.returncode}")
        with Image.open(image) as im:
            size = im.size
        if size != (WIDTH, HEIGHT):
            raise RuntimeError(f"Unexpected image dimensions {slug} {size}, expected {(WIDTH,HEIGHT)}")
        snapshots.append({
            "slug": slug, "source_svg_sha256": sha256(source),
            "image": f"review_4k/{slug}.png",
            "image_sha256": sha256(image),
            "width_px": WIDTH, "height_px": HEIGHT,
            "evidence_ceiling": EVIDENCE,
            **evidence,
        })
    manifest = {
        "schema": "CGX-REVIEW-PROXY-4K/0.1",
        "state": "PRIVATE_PRESENTATION_DERIVATIVE_NOT_CAD",
        "source_receipt_sha256": sha256(root / "receipt.json"),
        "source_heads": source_receipt["source_heads"],
        "source_object_count": source_receipt["item_total"],
        "rendered_count": len(snapshots),
        "watermark": EVIDENCE,
        "items": snapshots,
        "holds": ["No fabricated geometry", "No DBR approval",
                  "No physical material/process validation", "No public posting"],
    }
    (dest / "receipt.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {"status": "RENDERED_PRIVATE_PROXIES", "count": len(snapshots),
            "receipt": str(dest / "receipt.json")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-root", type=Path, required=True)
    parser.add_argument("--browser", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        receipt, pairs = validate_receipt(args.review_root)
        print(json.dumps({"status": "SOURCE_PROXIES_VERIFIED",
                          "count": len(pairs), "source_heads": receipt["source_heads"]}, indent=2))
        return
    print(json.dumps(render(args.review_root, args.browser, limit=args.limit), indent=2))


if __name__ == "__main__":
    main()
