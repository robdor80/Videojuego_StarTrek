#!/usr/bin/env python3
"""Acceptance tests for F10 OFFLINE reference. Not UE5 or Core integration tests."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from f10_academy_continuity import (
    ROOT, apply, new_candidate, replay, restore, seal, _module
)
from f10_academy_reference import evaluate

FIXTURE = ROOT / "validation/fixtures/f10/f10_academy_lifecycle_offline_v0.1.json"
DATA = json.loads(FIXTURE.read_text(encoding="utf-8"))


def candidate():
    return new_candidate("cadet:alpha", "profile:alpha")


def host(**updates):
    return {
        "trusted_origin": "CORE_HOST_VERIFIED",
        "character_ref": "cadet:alpha",
        "effective_date": "2370-01-01",
        **updates
    }


def admission():
    return apply(candidate(), {"action": "admit", "event_ref": "adm:1"},
                 host(admission_authorized=True))


def command(action, ref, **fields):
    return {"action": action, "event_ref": ref, **fields}


def year_review(year):
    return host(
        authorized_academic_review=True,
        explicit_player_choice=True,
        consolidated_evidence={
            "period_complete": True, "failed_required_modules": 0,
            "remediation_open": 0, "practical_requirements_complete": True,
            "conduct_status": "good"
        },
        verified_evidence_refs=[f"ev:y{year}"]
    )


class AcademyContinuityTests(unittest.TestCase):
    def test_full_four_year_career_from_fixture(self):
        end = restore(replay(DATA))
        self.assertEqual(end["academic_year"], 4)
        self.assertEqual(end["academy_status"], "graduated")
        self.assertEqual(end["year_results"], [1, 2, 3, 4])
        self.assertEqual(end["specialization"], "science_sensors")
        self.assertTrue(end["commissioned"])
        self.assertEqual(end["rank"], "ensign")
        self.assertEqual(end["first_assignment"]["orders_ref"], "order:starfleet-001")
        self.assertEqual(len(end["event_log"]), 16)
        self.assertEqual(len(end["record_events"]), 10)
        self.assertEqual(len(end["lesson_trace"]), 4)
        self.assertEqual(len(end["practice_trace"]), 2)
        self.assertEqual(len(end["social_trace"]), 1)
        self.assertEqual(end["relationship_refs"], [])
        self.assertEqual(end["mentor_refs"], [])
        self.assertEqual(end["disciplinary_refs"], [])
        self.assertEqual(end["scope"], "offline_qa_only_not_a_core_save")

    def test_record_step19_reused_with_source_families(self):
        end = restore(replay(DATA))
        families = [e["source_family"] for e in end["record_events"]]
        self.assertEqual(families.count("academy_admission"), 1)
        self.assertEqual(families.count("practical_evaluation"), 2)
        self.assertEqual(families.count("academy_year_progression"), 4)
        self.assertEqual(families.count("specialization_selected"), 1)
        self.assertEqual(families.count("academy_graduation"), 1)
        self.assertEqual(families.count("commission"), 1)
        self.assertEqual(len({r["record_event_id"] for r in end["record_events"]}), 10)

    def test_determinism_and_roundtrip(self):
        self.assertEqual(replay(DATA), replay(copy.deepcopy(DATA)))
        envelope = json.loads(json.dumps(replay(DATA)))
        self.assertEqual(restore(envelope), envelope["snapshot"])

    def test_mutated_save_is_rejected(self):
        envelope = replay(DATA)
        envelope["snapshot"]["rank"] = "captain"
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            restore(envelope)

    def test_invalid_year_order_even_with_rehashed_save(self):
        end = restore(replay(DATA))
        end["year_results"] = [1, 3, 4]
        with self.assertRaisesRegex(ValueError, "year order"):
            restore(seal(end))

    def test_replay_does_not_mutate_input(self):
        frozen = copy.deepcopy(DATA)
        replay(DATA)
        self.assertEqual(DATA, frozen)

    def test_no_promotion_on_admission(self):
        admitted = admission()
        self.assertEqual(admitted["academy_status"], "cadet_year_1")
        self.assertEqual(admitted["rank"], None)
        self.assertEqual(admitted["record_events"][0]["source_family"], "academy_admission")

    def test_untrusted_host_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "stub"):
            apply(candidate(), command("admit", "adm:1"),
                  host(trusted_origin="WEB", admission_authorized=True))

    def test_character_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            apply(candidate(), command("admit", "adm:1"),
                  host(character_ref="other:cadet", admission_authorized=True))

    def test_unverified_admission_rejected(self):
        with self.assertRaisesRegex(ValueError, "not authorized"):
            apply(candidate(), command("admit", "adm:1"), host())

    def test_extra_grade_field_rejected(self):
        with self.assertRaisesRegex(ValueError, "extra command fields"):
            apply(admission(), command("lesson", "l:1", subject_id="STF-401",
                                      stage="theory", grade=100),
                  host(attendance_confirmed=True))

    def test_invalid_course_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            apply(admission(), command("lesson", "l:1", subject_id="BRN-101",
                                      stage="theory"), host(attendance_confirmed=True))

    def test_lesson_no_automatic_grade(self):
        s = apply(admission(), command("lesson", "l:1", subject_id="STF-401",
                                      stage="theory"), host(attendance_confirmed=True))
        self.assertEqual(len(s["record_events"]), 1)
        self.assertEqual(s["lesson_trace"][0]["result"], "attendance_only")

    def test_practice_denied_without_core_resolution(self):
        with self.assertRaisesRegex(ValueError, "unverified practical"):
            apply(admission(), command("practice", "p:1", scenario_id="sensors_training",
                                      evidence_ref="sensor:1"),
                  host(practical_evaluation_confirmed=True,
                       verified_evidence_refs=["sensor:1"]))

    def test_capstone_only_in_year_four(self):
        with self.assertRaisesRegex(ValueError, "capstone window"):
            apply(admission(), command("practice", "p:km", scenario_id="kobayashi_maru",
                                      evidence_ref="km:1"),
                  host(simulation_resolved_in_core=True, practical_evaluation_confirmed=True,
                       verified_evidence_refs=["km:1"]))

    def test_new_external_study_evidence_reviewed_not_granted(self):
        result = evaluate({"action": "import_study_evidence", "evidence_ref": "web:new-003"},
                          {"trusted_origin": "CORE_HOST_VERIFIED", "character_ref": "cadet:alpha",
                           "academic_year": 2, "academy_status": "cadet_year_2",
                           "known_evidence_refs": []})
        self.assertEqual(result["decision"], "REQUIRES_CORE_REVIEW")
        self.assertFalse(result["grade_awarded"])

    def test_no_year_advance_without_verified_evidence(self):
        with self.assertRaisesRegex(ValueError, "not verified"):
            apply(admission(), command("complete_year", "year:1", evidence_ref="ev:y1"),
                  host(authorized_academic_review=True, consolidated_evidence={
                      "period_complete": True
                  }))

    def test_failed_modules_block_progression(self):
        review = year_review(1)
        review["consolidated_evidence"]["failed_required_modules"] = 8
        with self.assertRaisesRegex(ValueError, "requirements not passed"):
            apply(admission(), command("complete_year", "year:1", evidence_ref="ev:y1"), review)

    def test_year_two_needs_player_choice(self):
        s = apply(admission(), command("complete_year", "year:1", evidence_ref="ev:y1"), year_review(1))
        with self.assertRaisesRegex(ValueError, "player choice"):
            apply(s, command("complete_year", "year:2", evidence_ref="ev:y2"), year_review(2))

    def test_instructor_cannot_choose_player_specialty(self):
        s = apply(admission(), command("complete_year", "year:1", evidence_ref="ev:y1"), year_review(1))
        with self.assertRaisesRegex(ValueError, "not a player choice"):
            apply(s, command("choose_specialization", "s:2",
                             specialization_id="science_sensors"),
                  host(selection_window_open=True, explicit_player_choice=False))

    def test_graduation_and_commission_are_separate(self):
        partial = copy.deepcopy(DATA)
        partial["steps"] = partial["steps"][:14]
        graduated = restore(replay(partial))
        self.assertEqual(graduated["academy_status"], "graduated")
        self.assertFalse(graduated["commissioned"])
        self.assertIsNone(graduated["rank"])
        self.assertIsNone(graduated["first_assignment"])

    def test_no_first_assignment_before_commission(self):
        partial = copy.deepcopy(DATA)
        partial["steps"] = partial["steps"][:14]
        state = restore(replay(partial))
        with self.assertRaisesRegex(ValueError, "prerequisites"):
            apply(state, command("assign_first_post", "posting:premature"),
                  host(posting_authorized=True, vacancy_confirmed=True,
                       confirmed_orders_ref="order:1", confirmed_position_ref="slot:1"))

    def test_orders_and_vacancy_required(self):
        partial = copy.deepcopy(DATA)
        partial["steps"] = partial["steps"][:15]
        state = restore(replay(partial))
        with self.assertRaisesRegex(ValueError, "vacancy and orders"):
            apply(state, command("assign_first_post", "posting:1"),
                  host(posting_authorized=True, vacancy_confirmed=False,
                       confirmed_orders_ref="order:1", confirmed_position_ref="slot:1"))

    def test_duplicate_event_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate event_ref"):
            apply(admission(), command("lesson", "adm:1",
                                       subject_id="STF-401", stage="theory"),
                  host(attendance_confirmed=True))

    def test_social_trace_does_not_invent_relationships(self):
        s = apply(admission(), command("social", "social:1", npc_ref="npc:academy-cadet"),
                  host(social_event_confirmed=True))
        self.assertEqual(s["relationship_refs"], [])
        self.assertEqual(s["social_trace"][0]["relation_effect"], "none_by_default")

    def test_existing_schedule_resolver_reused(self):
        scheduler = _module("tools/generation/generate_academy_schedule_step5.py", "f10_schedule")
        fixture = {
            "campaign_seed": 17, "cadets": [{"population_slot_ref": "cadet:alpha"}],
            "day_indices": [0], "shared_commitments": [
                {"commitment_id": "class:1", "member_slot_refs": ["cadet:alpha"],
                 "entry_type": "class", "day_index": 0, "start_minute": 480,
                 "end_minute": 540, "location_ref": "academy:classroom"},
                {"commitment_id": "practice:1", "member_slot_refs": ["cadet:alpha"],
                 "entry_type": "practical", "day_index": 0, "start_minute": 600,
                 "end_minute": 660, "location_ref": "academy:classroom"}
            ]
        }
        out = scheduler.build_schedules(fixture)
        self.assertEqual(out["schedule_conflicts"], [])
        self.assertEqual(len(out["schedules"]["cadet:alpha"]), 2)
        self.assertEqual(out["schedule_truth_semantics"], "expected_not_actual_presence")

    def test_existing_instructor_resolver_cannot_award_grades(self):
        mentors = _module("tools/generation/resolve_academy_mentors_instructors_step12.py",
                          "f10_instructors")
        outcome = mentors.resolve({
            "instructors": [{"instructor_id": "prof:1", "subject_ids": ["STF-401"],
                             "active": True, "mentee_capacity": 1,
                             "mentor_scopes": ["science"], "authority_scope": []}],
            "cadets": [{"population_slot_ref": "cadet:alpha", "is_player": True}],
            "teaching_assignments": [
                {"instructor_id": "prof:1", "subject_id": "STF-401"}
            ],
            "travel_edges": [], "locations": []
        })
        self.assertEqual(outcome["teaching_assignments"][0]["assignment_state"], "active")
        self.assertEqual(outcome["automatic_grade_awards"], [])
        self.assertEqual(outcome["automatic_qualification_awards"], [])


if __name__ == "__main__":
    unittest.main()
