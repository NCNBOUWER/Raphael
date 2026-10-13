"""Offline CGX object review-lens invariants (no physical/source mutation)."""
from __future__ import annotations
import sys
import unittest
import os
import re
import shutil
import subprocess
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

    def test_same_offline_atlas_embeds_replay_controls_without_machine_execution(self):
        self.assertIn('id="printTimeline"', module.HTML)
        self.assertIn('id="printCanvas"', module.HTML)
        self.assertIn('id="printPhase"', module.HTML)
        self.assertIn('id="printRate"', module.HTML)
        self.assertIn('id="printPalette"', module.HTML)
        self.assertIn("sceneRender()", module.HTML)
        self.assertIn("time_previews", module.HTML)
        self.assertTrue(callable(module.load_and_compile))
        self.assertIn("connect-src 'none'", module.HTML)
        self.assertIn("not verified CAD", module.HTML)

    def test_standalone_print_demo_is_playable_source_only_and_exclusive(self):
        with TemporaryDirectory() as base:
            target=Path(base)/"build-preview"
            receipt=module.build_print_demo(target)
            markup=(target/"index.html").read_text(encoding="utf-8")
            self.assertEqual(receipt["status"],"VIEWER_CREATED_NO_PHYSICAL_OR_CAD_PROOF")
            self.assertFalse(receipt["public_release_authorized"])
            self.assertFalse(receipt["device_control_enabled"])
            self.assertEqual(len(receipt["source_seed_sha256"]),64)
            self.assertIn('id="printCanvas"',markup)
            self.assertIn('id="printProcedure"',markup)
            self.assertIn('id="printBattery"',markup)
            self.assertIn('id="printArm"',markup)
            self.assertIn('id="printPlay"',markup)
            self.assertIn('id="printSubstrate"',markup)
            self.assertIn("process_window_profiles",markup)
            self.assertIn("CAN_IF_WET_CHEMISTRY_FOCUS_AND_MASK_COUPONS_VALIDATED",markup)
            self.assertIn("HOLD_SUBSTRATE_STATE_UNRESOLVED",markup)
            self.assertIn("safety_interlocks_verified",markup)
            self.assertIn('"BB-SOURCE-DEMO"',markup)
            self.assertIn('"WATCH-ROUND"',markup)
            self.assertIn('"WATCH-SQUARE"',markup)
            self.assertIn("connect-src 'none'",markup)
            self.assertNotIn("private_canonical_root",markup)
            self.assertTrue((target/"receipt.json").exists())
            with self.assertRaisesRegex(ValueError,"occupied"):
                module.build_print_demo(target)
            script=re.search(r"<script>\s*(.*?)</script>",markup,re.S)
            self.assertIsNotNone(script)
            node=shutil.which("node")
            if node:
                result=subprocess.run([node,"--check"],input=script.group(1),
                                      encoding="utf-8",capture_output=True,timeout=8)
                self.assertEqual(result.returncode,0,result.stderr)

    def test_real_source_metadata_if_roots_supplied(self):
        """Optional integration smoke test; intentionally absent on unmounted CI."""
        light = os.environ.get("CGX_LIGHTSPEED_ROOT")
        printspace = os.environ.get("CGX_PRINTSPACE_ROOT")
        if not light or not printspace:
            self.skipTest("Set CGX_LIGHTSPEED_ROOT/CGX_PRINTSPACE_ROOT for full source smoke")
        meta, rows = module.compile_data(Path(light), Path(printspace))
        self.assertIsInstance(meta, dict)
        self.assertIsInstance(rows, list)
        self.assertEqual(meta["counts"], {
            "component": 411,
            "technology": 81,
            "product": 80,
            "printer": 17,
            "twin": 16,
        })
        self.assertEqual(len(rows), 605)
        self.assertEqual(set(meta["source_heads"]), {"LightSpeed", "PrintSpace"})

    def test_guided_review_paths_preserve_one_source_graph(self):
        self.assertEqual(len(module.TOURS), 4)
        ids = [tour["id"] for tour in module.TOURS]
        self.assertEqual(len(ids), len(set(ids)))
        for tour in module.TOURS:
            self.assertGreaterEqual(len(tour["steps"]), 4)
            self.assertEqual(len(set(tour["steps"])), len(tour["steps"]))
            self.assertTrue(all(kind in module.GROUPS for kind, _id in tour["steps"]))
        self.assertIn('id="tour"', module.HTML)
        self.assertIn('function jumpRoute', module.HTML)
        self.assertIn('source review only', module.HTML)

if __name__ == "__main__":
    unittest.main()
