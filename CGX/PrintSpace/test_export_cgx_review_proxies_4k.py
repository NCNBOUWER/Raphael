"""Offline 4K proxy renderer contract tests. Browser render is operator-local, not CI."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import export_cgx_review_proxies_4k as source


class ReviewProxyFourKTests(unittest.TestCase):
    def test_dimensions_and_watermark(self):
        self.assertEqual((source.WIDTH, source.HEIGHT), (3840, 2160))
        document = source.wrapper("mark_iii", "../assets/mark_iii.svg")
        self.assertIn("INTERACTION PROXY", document)
        self.assertIn("NOT DIMENSIONED CAD", document)
        self.assertIn("connect-src 'none'", document)
        self.assertIn("../assets/mark_iii.svg", document)

    def test_injection_rejected(self):
        with self.assertRaises(ValueError):
            source.wrapper('bad"><script>', "../assets/x.svg")

    def test_receipt_and_sources_must_be_exact(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            assets = root / "assets"
            assets.mkdir()
            for name in source.ALLOWED:
                (assets / (name + ".svg")).write_text(
                    '<svg data-representation-class="INTERACTION_PROXY" '
                    'data-dimension-authority="NONE" data-release-eligible="false"></svg>',
                    encoding="utf-8",
                )
            receipt = {
                "schema": source.EXPECTED_SCHEMA,
                "artifact": "OFFLINE_LOCAL_REVIEW_ONLY",
                "item_total": 605,
                "source_heads": {"LightSpeed": "a", "PrintSpace": "b"},
                "files": {"assets/" + name + ".svg": source.sha256(assets / (name + ".svg"))
                          for name in source.ALLOWED},
            }
            (root / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            _, rows = source.validate_receipt(root)
            self.assertEqual(len(rows), 16)
            (assets / "mark_iii.svg").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "drift"):
                source.validate_receipt(root)

    def test_unqualified_svg_is_held(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            assets = root / "assets"
            assets.mkdir()
            for name in source.ALLOWED:
                (assets / (name + ".svg")).write_text("<svg/>", encoding="utf-8")
            receipt = {
                "schema": source.EXPECTED_SCHEMA, "artifact": "OFFLINE_LOCAL_REVIEW_ONLY",
                "item_total": 605,
                "files": {"assets/" + name + ".svg": source.sha256(assets / (name + ".svg"))
                          for name in source.ALLOWED},
            }
            (root / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Not a declared"):
                source.validate_receipt(root)


if __name__ == "__main__":
    unittest.main()
