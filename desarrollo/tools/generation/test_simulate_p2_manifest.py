#!/usr/bin/env python3
"""P2-H17/H18: normalized view must track source manifests without rewriting them."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROADMAP = ROOT / "proyecto/docs/roadmap"
VIEW = ROADMAP / "P2_B01_B10_MADUREZ_NORMALIZADA_20261119.json"


class P2ReferenceMaturityTests(unittest.TestCase):
    def test_ten_reference_blocks_match_177_historical_packages(self):
        view = json.loads(VIEW.read_text(encoding="utf-8"))
        self.assertEqual(view["total_blocks"], 10)
        self.assertEqual((view["total_packages"], view["total_reference_packages"]), (177, 177))
        self.assertFalse(view["f13_runtime_implemented"])
        self.assertEqual(sorted(view["blocks"]), [f"B{x:02d}" for x in range(1, 11)])
        amount = 0
        for block, record in view["blocks"].items():
            with self.subTest(block=block):
                raw = json.loads((ROOT / record["source_manifest"]).read_text(encoding="utf-8"))
                self.assertEqual(record["historical_packages_total"], raw["summary"]["total_packages"])
                completed = (raw["summary"].get("certified_reference") or
                             raw["summary"].get("complete_reference") or
                             raw["summary"].get("complete"))
                self.assertEqual(record["historical_packages_complete"], completed)
                self.assertEqual(record["source_status"], raw.get("status", "COMPLETE"))
                self.assertEqual(record["reference_status"], "REFERENCE_COMPLETE_HISTORICAL")
                self.assertFalse(record["runtime_implemented"])
                self.assertEqual(len(raw["packages"]), completed)
                amount += completed
        self.assertEqual(amount, 177)

    def test_historical_master_plan_has_current_banner(self):
        content = (ROADMAP / "procedural_dynamic_universe_10_block_plan_v0.1.md").read_text(encoding="utf-8")
        self.assertIn("ESTADO VIGENTE — 19/11/2026", content)
        self.assertIn("P2_B01_B10_MADUREZ_NORMALIZADA_20261119.json", content)


if __name__ == "__main__":
    unittest.main()
