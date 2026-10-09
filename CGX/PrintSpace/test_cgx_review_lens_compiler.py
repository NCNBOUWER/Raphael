"""Offline CGX object review-lens invariants (no physical/source mutation)."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cgx_review_lens_compiler as module

class OfflineCGXReviewTests(unittest.TestCase):
    def test_distinct_layers(self):
        self.assertEqual(module.GROUPS, ("component", "technology", "product", "printer", "twin"))
        self.assertEqual(len(module.TWINS), 16)
        self.assertEqual(len(set(x[0] for x in module.TWINS)), 16)

    def test_no_hidden_authorisation(self):
        self.assertIn("NOT_APPROVED", module.HTML)
        self.assertIn("This interface cannot approve", module.HTML)

    def test_local_only_csp(self):
        self.assertIn("connect-src 'none'", module.HTML)
        self.assertIn("default-src 'none'", module.HTML)
        self.assertIn("img-src 'self' data:", module.HTML)
        self.assertNotIn('http://127.0.0.1:4173', module.HTML)
        self.assertIn("REVIEW_SELECTION_DRAFT", module.HTML)

    def test_provenance_source_per_item(self):
        e = module.entry("component", "CGA-TEST", "test resistor", "electrical",
            "sets resistance", "cgx/path.json", "achillesromer-coder/LightSpeed", "a"*40,
            "CANDIDATE", "Physical qualification pending")
        self.assertIn("LightSpeed/blob/", e["source_url"])
        self.assertIn("/cgx/path.json", e["source_url"])
        self.assertIn("Physical qualification pending", e["hold"])

    def test_missing_source_fails_closed(self):
        with TemporaryDirectory() as a, TemporaryDirectory() as b:
            with self.assertRaises(FileNotFoundError):
                module.compile_data(Path(a), Path(b))

    def test_no_fake_twin_geometry(self):
        self.assertIn("No verified graphic is linked", module.HTML)

if __name__ == "__main__":
    unittest.main()
