#!/usr/bin/env python3
"""QA de referencia F10; sin juego UE5, Core, Firestore o perfiles reales."""
from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from f10_academy_reference import (
    ROOT, audit_sources, evaluate,
    DECISION_DENY, DECISION_READ, DECISION_REVIEW
)

FIXTURE = ROOT / "validation/fixtures/f10/f10_academy_scenarios_v0.1.json"


def context(patch=None):
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return {**fixture["base_trusted_context"], **(patch or {})}


class AcademyReferenceTests(unittest.TestCase):
    def test_curriculum_source_audit(self):
        report = audit_sources()
        self.assertEqual(
            (report["years"], report["trimesters"], report["main_courses"], report["specializations"]),
            (4, 12, 60, 7)
        )
        self.assertEqual((report["branch_stages"], report["designed_units"]), (35, 501))
        self.assertFalse(report["core_runtime_checked"])
        self.assertFalse(report["unreal_checked"])
        self.assertFalse(report["external_runtime_checked"])

    def test_all_scenarios(self):
        doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(doc["schema_version"], "0.1.0")
        self.assertGreaterEqual(len(doc["cases"]), 30)
        ids = [c["id"] for c in doc["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        for case in doc["cases"]:
            with self.subTest(case=case["id"]):
                input_context = {**doc["base_trusted_context"], **case["context_patch"]}
                proposal_before = copy.deepcopy(case["proposal"])
                context_before = copy.deepcopy(input_context)
                outcome = evaluate(case["proposal"], input_context)
                self.assertEqual(outcome["decision"], case["expected_decision"])
                self.assertEqual(case["proposal"], proposal_before)
                self.assertEqual(input_context, context_before)
                self.assertFalse(outcome["effects_applied"])
                self.assertFalse(outcome["world_state_mutated"])
                self.assertFalse(outcome["grade_awarded"])
                self.assertFalse(outcome["rank_awarded"])
                self.assertFalse(outcome["posting_awarded"])

    def test_no_automatic_web_authority(self):
        result = evaluate({"action": "import_study_evidence", "evidence_ref": "web:theory-1"}, context())
        self.assertEqual(result["decision"], DECISION_REVIEW)
        self.assertFalse(result["grade_awarded"])

    def test_local_study_does_not_need_game(self):
        result = evaluate({"action": "study_progress", "subject_id": "STF-401"})
        self.assertEqual(result["decision"], DECISION_READ)

    def test_cannot_inject_grades(self):
        candidate = {"action": "import_study_evidence", "evidence_ref": "web:theory-1", "passed": True}
        self.assertEqual(evaluate(candidate, context())["decision"], DECISION_DENY)

    def test_cannot_assign_player_specialization_from_instructor(self):
        candidate = {"action": "choose_specialization", "specialization_id": "medical"}
        self.assertEqual(evaluate(candidate, context({"explicit_player_choice": False}))["decision"], DECISION_DENY)

    def test_end_of_fourth_year_never_awards_rank(self):
        candidate = {"action": "advance_year", "evidence_ref": "event:y2"}
        ctx = context({"academic_year": 4, "academy_status": "cadet_year_4"})
        output = evaluate(candidate, ctx)
        self.assertEqual(output["decision"], DECISION_DENY)
        self.assertFalse(output["rank_awarded"])

    def test_graduation_does_not_commission(self):
        candidate = {"action": "confirm_graduation", "evidence_ref": "event:grad-1"}
        ctx = context({"academic_year": 4, "academy_status": "graduation_pending", "graduation_eligible": True})
        out = evaluate(candidate, ctx)
        self.assertEqual(out["decision"], DECISION_REVIEW)
        self.assertFalse(out["rank_awarded"])

    def test_commission_not_first_assignment(self):
        candidate = {"action": "commission", "evidence_ref": "event:grad-1"}
        ctx = context({"academic_year": 4, "academy_status": "graduated", "commission_authorized": True,
                       "confirmed_graduation_event_ref": "event:grad-1"})
        out = evaluate(candidate, ctx)
        self.assertEqual(out["decision"], DECISION_REVIEW)
        self.assertFalse(out["posting_awarded"])

    def test_simulation_does_not_auto_grade(self):
        candidate = {"action": "review_simulation", "scenario_id": "kobayashi_maru", "evidence_ref": "sim:km-1"}
        out = evaluate(candidate, context())
        self.assertEqual(out["decision"], DECISION_REVIEW)
        self.assertFalse(out["grade_awarded"])

    def test_invalid_candidate_input(self):
        for value in (None, [], "advance_year", 123, True):
            with self.subTest(value=value):
                self.assertEqual(evaluate(value, context())["decision"], DECISION_DENY)

    def test_invalid_context_is_rejected(self):
        p = {"action": "advance_year", "evidence_ref": "event:y2"}
        for value in (None, [], "trusted", {}, {"trusted_origin": "CORE_HOST_VERIFIED"}):
            with self.subTest(value=value):
                self.assertEqual(evaluate(p, value)["decision"], DECISION_DENY)

    def test_bool_does_not_count_as_year(self):
        p = {"action": "advance_year", "evidence_ref": "event:y2"}
        for y in (True, False, 2.0, "2", None, 0, 5):
            with self.subTest(year=y):
                self.assertEqual(evaluate(p, context({"academic_year": y}))["decision"], DECISION_DENY)

    def test_duplicate_evidence_is_rejected(self):
        p = {"action": "advance_year", "evidence_ref": "event:y2"}
        self.assertEqual(
            evaluate(p, context({"known_evidence_refs": ["event:y2", "event:y2"]}))["decision"],
            DECISION_DENY
        )

    def test_candidate_fails_closed(self):
        for p in (
            {"action": "unknown"},
            {"action": "advance_year", "evidence_ref": "event:y2", "rank": "captain"},
            {"action": "advance_year", "evidence_ref": 123},
            {"action": "study_progress", "subject_id": ""},
        ):
            with self.subTest(candidate=p):
                self.assertEqual(evaluate(p, context())["decision"], DECISION_DENY)

    def test_audit_detects_manifest_drift(self):
        # Copia exclusivamente los contratos consultados: nada del material multimedia.
        rels = [
            "curriculum/curriculum_manifest_v1_0.json",
            "academic_year_trimester_model.json", "curriculum_structure.json",
            "specializations.json", "external_study_profile_contract.json",
            "academy_state.json", "cadet_progression.json", "graduation_model.json",
            "life/academy_record_integration_contract_v0.1.json",
            "first_assignment_model.json", "simulation_model.json",
        ]
        base = Path("gameplay/careers/academy_path")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in rels:
                src = ROOT / base / rel
                dst = root / base / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            curriculum = json.loads((ROOT / base / rels[0]).read_text(encoding="utf-8"))
            for y in curriculum["years"]:
                rel = Path("curriculum") / y["manifest_ref"]
                dst = root / base / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text("{}", encoding="utf-8")
            audit_sources(root)
            target = root / base / rels[0]
            manifest = json.loads(target.read_text(encoding="utf-8"))
            manifest["main_course_components"] = 59
            target.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "60 asignaturas"):
                audit_sources(root)


if __name__ == "__main__":
    unittest.main()
