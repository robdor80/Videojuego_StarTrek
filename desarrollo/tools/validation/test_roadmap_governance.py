#!/usr/bin/env python3
"""Regresiones R0: el validador ha de permitir progreso real y rechazar evidencias falsas."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "desarrollo/tools/validation"))
from validate_roadmap_state import PLAN, STATE, validate  # noqa: E402


class RoadmapGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(STATE.read_text(encoding="utf-8"))
        cls.plan = PLAN.read_text(encoding="utf-8")

    def fresh(self) -> dict:
        return copy.deepcopy(self.baseline)

    def run_checks(self, state: dict, plan: str | None = None) -> list[str]:
        return validate(state, self.plan if plan is None else plan, ROOT)

    def test_actual_snapshot_passes(self):
        self.assertEqual(self.run_checks(self.fresh()), [])

    def test_parallel_active_workstreams_are_allowed(self):
        s = self.fresh()
        phase = next(p for p in s["phases"] if p["id"] == "F11")
        phase["status"] = "EN_CURSO"
        # El foco F05 sigue teniendo prioridad. Dos frentes no falsean el gobierno.
        updated = self.plan.replace("| **EN_REVISION** | UE5_JUGABLE |", "| **EN_CURSO** | UE5_JUGABLE |", 1)
        self.assertEqual(self.run_checks(s, updated), [])

    def test_phase_closed_without_acta_is_rejected(self):
        s = self.fresh()
        phase = next(p for p in s["phases"] if p["id"] == "F05")
        phase["status"] = "CERRADA"
        self.assertTrue(any("F05: " in e for e in self.run_checks(s)))

    def test_draft_cannot_be_faked_as_merged(self):
        s = self.fresh()
        pr = next(pr for pr in s["tracked_pull_requests"] if pr["number"] == 91)
        pr["status"] = "FUSIONADA"
        self.assertTrue(any("PR #91" in e for e in self.run_checks(s)))

    def test_unmerged_pr_cannot_contain_merge_receipt(self):
        s = self.fresh()
        pr = next(pr for pr in s["tracked_pull_requests"] if pr["number"] == 97)
        pr["merge_commit_sha"] = "a" * 40
        self.assertTrue(any("PR #97" in e for e in self.run_checks(s)))

    def test_ue5_claim_without_build_msi_and_acta_is_rejected(self):
        s = self.fresh()
        next(p for p in s["phases"] if p["id"] == "F07")["achieved_maturity"] = "UE5_JUGABLE"
        self.assertTrue(any("UE5/aceptación" in e for e in self.run_checks(s)))

    def test_closure_evidence_must_survive(self):
        s = self.fresh()
        next(p for p in s["phases"] if p["id"] == "F04")["closure"]["evidence_refs"] = []
        self.assertTrue(any("F04: CERRADA sin acta" in e for e in self.run_checks(s)))

    def test_eighty_steps_and_structure_are_fixed(self):
        s = self.fresh()
        next(p for p in s["phases"] if p["id"] == "F13")["steps"]["P06"] = "PLANIFICADA"
        self.assertTrue(any("F13: cinco pasos" in e for e in self.run_checks(s)))

    def test_last_contiguous_closed_is_derived(self):
        s = self.fresh()
        s["completed_management_phase"] = "F03"
        self.assertTrue(any("completed_management_phase" in e for e in self.run_checks(s)))

    def test_master_plan_must_track_status(self):
        s = self.fresh()
        self.assertTrue(any("F05: tabla" in e for e in self.run_checks(s, self.plan.replace(
            "| **EN_CURSO** | CORE_INTEGRADO |", "| **CERRADA** | CORE_INTEGRADO |", 1,
        ))))

    def test_legacy_governance_history_is_not_discarded(self):
        s = self.fresh()
        s["governance_review"]["merged_prs"] = []
        self.assertTrue(any("evidencia histórica" in e for e in self.run_checks(s)))


if __name__ == "__main__":
    unittest.main()
