#!/usr/bin/env python3
"""Guard the historical Academy hand-off while the dynamic universe advances."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "desarrollo/tools/generation/validate_academy_life_final_step20.py"
spec = importlib.util.spec_from_file_location("academy_gate", MODULE_PATH)
academy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(academy)


def plan_for(states):
    rows = ["| Block | Scope | Status |", "|---|---|---|"]
    rows.extend(f"| {block} | synthetic block {block} | {states[block]} |"
                for block in range(1, 11))
    return "\n".join(rows)


def base_states():
    return {i: ("COMPLETE" if i <= 3 else "TODO") for i in range(1, 11)}


class AcademyDynamicFrontierBridgeTests(unittest.TestCase):
    def test_01_historical_ready_b04_is_valid(self):
        s = base_states()
        s[4] = "READY_TO_RESUME"
        self.assertEqual(4, academy.dynamic_reference_frontier(plan_for(s)))

    def test_02_current_b08_frontier_is_valid(self):
        s = base_states()
        for i in (4, 5, 6, 7):
            s[i] = "REFERENCE_COMPLETE"
        self.assertEqual(8, academy.dynamic_reference_frontier(plan_for(s)))

    def test_03_cannot_skip_block(self):
        s = base_states()
        s[5] = "REFERENCE_COMPLETE"
        self.assertIsNone(academy.dynamic_reference_frontier(plan_for(s)))

    def test_04_earlier_baseline_must_be_complete(self):
        s = base_states()
        s[2] = "TODO"
        self.assertIsNone(academy.dynamic_reference_frontier(plan_for(s)))

    def test_05_missing_or_duplicate_row_rejected(self):
        s = plan_for(base_states())
        self.assertIsNone(academy.dynamic_reference_frontier(s.replace(
            "| 10 | synthetic block 10 | TODO |", "")))
        self.assertIsNone(academy.dynamic_reference_frontier(s + "\n| 4 | duplicate | TODO |"))

    def test_06_out_of_order_in_progress_rejected(self):
        s = base_states()
        s[6] = "IN_PROGRESS"
        self.assertIsNone(academy.dynamic_reference_frontier(plan_for(s)))

    def test_07_full_reference_completion_can_be_recognized(self):
        s = base_states()
        for i in range(4, 11):
            s[i] = "REFERENCE_COMPLETE"
        self.assertEqual(11, academy.dynamic_reference_frontier(plan_for(s)))

    def test_08_real_current_references_are_valid(self):
        source = (ROOT / "proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md").read_text(encoding="utf-8")
        self.assertEqual(10, academy.dynamic_reference_frontier(source))
        status = json.loads((ROOT / "proyecto/docs/roadmap/academy_life_social_simulation_status_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual("READY_TO_RESUME", status["deferred_after_step_20"]["status"])

    def test_09_full_academy_repository_audit_passes(self):
        report = academy.audit_repo(ROOT)
        self.assertTrue(report["dynamic_universe_gate_ok"], report["errors"])
        self.assertTrue(report["ok"], report["errors"])


if __name__ == "__main__":
    unittest.main()
