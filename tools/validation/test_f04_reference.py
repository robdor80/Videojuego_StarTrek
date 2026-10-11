#!/usr/bin/env python3
"""F04 pure-reference regression checks, no dependency on remote CoreRPG."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "validation"))
from f04_reference import check_roster, check_schedule, evaluate, verify_fixture  # noqa:E402


def context(action, **kw):
    return dict(action=action, actor_active=True, actor_fit=True,
                technical_available=True, safety_interlock="none", **kw)


class F04ReferenceTests(unittest.TestCase):
    def test_all_38_fixture_cases(self):
        path = ROOT / "validation/fixtures/f04/authority_watch_acceptance_v0.1.json"
        fixture = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual((len(fixture["authority_cases"]), len(fixture["roster_cases"]),
                          len(fixture["schedule_cases"])), (25, 7, 6))
        self.assertEqual(verify_fixture(path), [])

    def test_unknown_action_fails_closed(self):
        self.assertEqual(evaluate(context("newly_invented_power"))["code"], "UNKNOWN_ACTION")

    def test_rank_cannot_confer_command(self):
        c = context("change_watch_policy", rank="admiral", staffing_valid=True)
        self.assertEqual(evaluate(c)["decision"], "DENY")

    def test_captain_must_have_appointment(self):
        c = context("change_watch_policy", position="commanding_officer", staffing_valid=True)
        self.assertEqual(evaluate(c)["decision"], "DENY")

    def test_captain_can_reject_engine_preference(self):
        c = context("change_watch_policy", position="commanding_officer",
                    appointment_active=True, staffing_valid=True, control_mode="manual",
                    engine_prefers="three_shift", requested_watch="four_shift")
        self.assertEqual(evaluate(c)["decision"], "ALLOW")

    def test_worse_choice_cannot_break_hard_safety(self):
        c = context("change_watch_policy", position="commanding_officer",
                    appointment_active=True, staffing_valid=True,
                    safety_interlock="non_overrideable")
        self.assertEqual(evaluate(c)["code"], "HARD_INTERLOCK")

    def test_delegate_cannot_extend_origin_permission(self):
        d = dict(from_authorized_commander=False, to_actor=True, domain="watch_policy",
                 status="active", starts_at=10, ends_at=20)
        c = context("change_watch_policy", staffing_valid=True, control_mode="delegated_autonomous",
                    now=11, delegation=d)
        self.assertEqual(evaluate(c)["decision"], "DENY")

    def test_delegate_domain_confined(self):
        d = dict(from_authorized_commander=True, to_actor=True, domain="first_contact_policy",
                 status="active", starts_at=10, ends_at=20)
        c = context("change_watch_policy", staffing_valid=True, control_mode="delegated_autonomous",
                    now=11, delegation=d)
        self.assertEqual(evaluate(c)["decision"], "DENY")

    def test_medical_removal_does_not_grant_command(self):
        c = context("relieve_command_medically", position="chief_medical_officer",
                    professional_qualified=True, medical_judgement_documented=True,
                    target_medically_unfit=True)
        out = evaluate(c)
        self.assertEqual(out["decision"], "ALLOW")
        self.assertIs(out["transfers_command"], False)
        self.assertEqual(out["effect"], "activate_normal_succession")

    def test_prime_directive_review_not_automatic_hard_block(self):
        c = context("first_contact", position="commanding_officer", appointment_active=True,
                    prime_directive_risk=True, contact_authorized=True)
        self.assertEqual(evaluate(c)["decision"], "REVIEW")

    def test_technical_capability_required_for_sensor(self):
        c = context("sensor_scan", station="sensors", on_duty=True,
                    assignment_active=True, qualified=True, technical_available=False)
        self.assertEqual(evaluate(c)["decision"], "DENY")

    def test_two_characters_can_cover_two_slots(self):
        slots = [dict(slot_id="s1", qualification="sensors", continuous=True),
                 dict(slot_id="s2", qualification="ops", continuous=True)]
        people = {k: dict(is_duty_crew=True, aboard=True, fit=True, qualifications=[v])
                  for k, v in [("a", "sensors"), ("b", "ops")]}
        assigns = [dict(slot_id="s1", character_id="a"),
                   dict(slot_id="s2", character_id="b")]
        self.assertEqual(check_roster(slots, people, assigns), [])

    def test_no_unqualified_fallback_spawn(self):
        slots = [dict(slot_id="s", qualification="science", continuous=True)]
        people = {"alice": dict(is_duty_crew=True, aboard=True, fit=True,
                                qualifications=["security"])}
        errors = check_roster(slots, people, [dict(slot_id="s", character_id="alice")])
        self.assertEqual(errors, ["INELIGIBLE_CREW:alice"])

    def test_contiguous_half_open_windows(self):
        a = dict(id="a", character_id="same", start=0, end=10)
        b = dict(id="b", character_id="same", start=10, end=20)
        self.assertEqual(check_schedule([a, b]), [])

    def test_untraced_override_rejected(self):
        a = dict(id="rest", character_id="same", start=0, end=12, preempted_by="emergency")
        b = dict(id="emergency", character_id="same", start=7, end=9, kind="emergency")
        self.assertEqual(check_schedule([a, b]), ["INCOMPATIBLE_OVERLAP:emergency:rest"])

    def test_repository_inputs_match_canonical_semantics(self):
        def read(p):
            return json.loads((ROOT / p).read_text(encoding="utf-8"))
        manifest = read("gameplay/ship_operations/crew_manifest_model.json")
        shifts = read("gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json")
        positions = read("lore/federation/starfleet/positions/positions.json")
        medical = read("lore/federation/starfleet/regulations/medical_authority.json")
        directive = read("lore/federation/starfleet/prime_directive/prime_directive.json")
        self.assertIn("vacancies", manifest["manifest_fields"])
        self.assertIn("three_shift", shifts["starfleet_patterns"])
        self.assertIn("four_shift", shifts["starfleet_patterns"])
        self.assertIn("commanding_officer", [x["id"] for x in positions["positions"]])
        self.assertTrue(medical["can_relieve_commanding_officer"])
        self.assertFalse(medical["transfers_command"])
        self.assertTrue(directive["not_a_hard_action_block"])


if __name__ == "__main__":
    unittest.main()
