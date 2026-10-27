#!/usr/bin/env python3
"""Pruebas de regresión F12: fixtures sin autenticación, no gameplay UE5."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'desarrollo/tools' / "validation"))
import f12_shipboard_reference as f12


class TestF12ShipboardReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            (ROOT / "desarrollo/validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json").read_text(encoding="utf-8")
        )

    def setUp(self):
        self.world = copy.deepcopy(self.fixture["world"])
        self.meal = dict(activity_id="meal-12", ship_id="miranda", location_id="mess",
                         activity_type="social_meal", start=1200, end=1250,
                         participants=["alex", "bea"], accepted_participants=["alex", "bea"])
        self.social = dict(event_id="e-f12", event_type="successful_collaboration",
                           minute=2000, participants=["alex", "bea"],
                           shared_location_ref="mess", cause_event_ref="mission/log/12",
                           witnesses=[])

    def test_fixture_scenarios(self):
        result = f12.run_scenarios(ROOT / "desarrollo/validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json")
        self.assertEqual(45, result["scenario_count"])
        self.assertEqual(45, result["passed"], result["failed_ids"])

    def test_world_has_identity_and_valid_rest(self):
        self.assertTrue(f12.validate_world(self.world))

    def test_world_detects_duplicate_overlapping_schedule(self):
        self.world["characters"]["alex"]["blocks"].append(
            {"start": 900, "end": 1100, "family": "recreation"})
        with self.assertRaises(ValueError):
            f12.validate_world(self.world)

    def test_world_rejects_boolean_minute(self):
        self.world["characters"]["alex"]["blocks"][0]["start"] = True
        with self.assertRaises(ValueError):
            f12.validate_world(self.world)

    def test_activity_is_not_authorized(self):
        result = f12.screen_activity(self.world, self.meal)
        self.assertEqual(f12.REVIEW, result["status"])
        self.assertIn("NO_MUTATION", result["authority"])

    def test_duty_not_preempted_by_player_request(self):
        self.meal.update(start=900, end=920)
        self.assertEqual("schedule_conflict", f12.screen_activity(self.world, self.meal)["reasons"][0])

    def test_no_fabricated_holodeck(self):
        self.meal["activity_type"] = "holodeck"
        self.assertEqual(f12.BLOCKED, f12.screen_activity(self.world, self.meal)["status"])

    def test_social_acceptance_is_explicit(self):
        self.meal["accepted_participants"] = ["alex"]
        self.assertEqual("missing_explicit_participant_acceptance",
                         f12.screen_activity(self.world, self.meal)["reasons"][0])

    def test_acceptance_cannot_be_stolen(self):
        self.meal["accepted_participants"] = ["alex", "cla"]
        self.assertEqual(f12.BLOCKED, f12.screen_activity(self.world, self.meal)["status"])

    def test_no_teleportation_from_another_ship(self):
        self.meal["participants"] = ["alex", "cla"]
        self.meal["accepted_participants"] = ["alex", "cla"]
        self.assertEqual("participant_not_on_ship", f12.screen_activity(self.world, self.meal)["reasons"][0])

    def test_does_not_change_world(self):
        before = copy.deepcopy(self.world)
        f12.screen_activity(self.world, self.meal)
        f12.screen_social_event(self.world, self.social)
        f12.render_lod_plan(self.world, "miranda", "mess", 1)
        self.assertEqual(before, self.world)

    def test_proximity_is_not_friendship(self):
        result = f12.screen_social_event(self.world, self.social)
        self.assertEqual(["professional_respect"], result["candidate_dimensions"])
        self.assertNotIn("friendship", result["candidate_dimensions"])

    def test_no_cause_no_relationship_update(self):
        self.social["cause_event_ref"] = ""
        self.assertEqual(f12.BLOCKED, f12.screen_social_event(self.world, self.social)["status"])

    def test_same_ship_event_requires_real_shared_location_or_contact_evidence(self):
        self.world["characters"]["bea"]["location_id"] = "bridge"
        result = f12.screen_social_event(self.world, self.social)
        self.assertEqual(f12.BLOCKED, result["status"])
        self.assertIn("contact_not_plausible", result["reasons"])
        self.social["travel_or_contact_ref"] = "comms:verified-1"
        self.assertEqual(f12.REVIEW, f12.screen_social_event(self.world, self.social)["status"])

    def test_unknown_shared_location_is_rejected(self):
        self.social["shared_location_ref"] = "invented-room"
        result = f12.screen_social_event(self.world, self.social)
        self.assertEqual(f12.BLOCKED, result["status"])
        self.assertIn("unknown_shared_location", result["reasons"])

    def test_romance_only_with_age_evidence(self):
        self.social["event_type"] = "romantic_expression"
        self.social["participants"] = ["alex", "eli"]
        self.assertEqual("adults_only", f12.screen_social_event(self.world, self.social)["reasons"][0])

    def test_romance_project_canon_and_no_social_filter(self):
        self.social["event_type"] = "romantic_expression"
        self.social["participants"] = ["alex", "far"]
        self.assertEqual(f12.BLOCKED, f12.screen_social_event(self.world, self.social)["status"])
        self.social["event_type"] = "social_activity"
        self.assertEqual(f12.REVIEW, f12.screen_social_event(self.world, self.social)["status"])

    def test_player_romantic_interest_never_inferred(self):
        self.social["event_type"] = "romantic_expression"
        self.social["participants"] = ["alex", "dina"]
        self.assertEqual("missing_player_action", f12.screen_social_event(self.world, self.social)["reasons"][0])
        self.social["explicit_player_action_ids"] = ["dina"]
        self.assertEqual(f12.REVIEW, f12.screen_social_event(self.world, self.social)["status"])

    def test_consent_requires_both_not_just_rank(self):
        self.social["event_type"] = "consensual_intimacy"
        self.social["explicit_consent_ids"] = ["alex"]
        self.assertEqual(f12.BLOCKED, f12.screen_social_event(self.world, self.social)["status"])

    def test_rejection_does_not_infer_hostility(self):
        self.social["event_type"] = "romantic_rejection"
        self.assertEqual([], f12.screen_social_event(self.world, self.social)["candidate_dimensions"])

    def test_witness_does_not_learn_private_conversation(self):
        evt = {**self.social, "witnesses": ["far"], "private_content": "only-participants"}
        self.assertEqual("interaction_occurred",
                         f12.project_event_for_npc(evt, "far")["known_event_type"])
        self.assertNotIn("private_content", f12.project_event_for_npc(evt, "far"))

    def test_no_omniscient_outsider(self):
        self.assertIsNone(f12.project_event_for_npc(self.social, "cla"))

    def test_replay_persists_identity_and_directional_edges(self):
        before = copy.deepcopy(self.world)
        result = f12.replay_reference(self.world, [self.social], months=3)
        self.assertEqual(f12.REVIEW, result["status"])
        self.assertEqual(sorted(before["characters"]), result["identities"])
        self.assertIn("alex->bea", result["relationship_evidence"])
        self.assertIn("bea->alex", result["relationship_evidence"])
        self.assertEqual(before, self.world)

    def test_replay_without_events_does_not_create_relationships(self):
        result = f12.replay_reference(self.world, [], months=5)
        self.assertEqual({}, result["relationship_evidence"])
        self.assertEqual(0, result["processed_events"])

    def test_replay_digest_is_deterministic(self):
        a = f12.replay_reference(self.world, [self.social], months=3)
        b = f12.replay_reference(copy.deepcopy(self.world), [copy.deepcopy(self.social)], months=3)
        self.assertEqual(a["sha256"], b["sha256"])
        self.assertEqual(64, len(a["sha256"]))

    def test_transfer_keeps_identity_and_history(self):
        transfer = dict(event_id="transfer1", event_type="transfer", minute=50000,
                        cause_event_ref="order/42", character_id="bea",
                        new_ship_id="intrepid", new_location_id="mess")
        result = f12.replay_reference(self.world, [self.social, transfer], months=4)
        self.assertEqual("intrepid", result["assignments"]["bea"])
        self.assertIn("alex->bea", result["relationship_evidence"])
        self.assertIn("bea", result["memories_by_owner"])

    def test_transfer_does_not_invent_contact(self):
        transfer = dict(event_id="transfer1", event_type="transfer", minute=50000,
                        cause_event_ref="order/42", character_id="bea",
                        new_ship_id="intrepid", new_location_id="mess")
        later = {**self.social, "event_id": "e-later", "minute": 75000}
        result = f12.replay_reference(self.world, [self.social, transfer, later], months=4)
        self.assertEqual(f12.BLOCKED, result["status"])

    def test_lod_limits_actors_not_population(self):
        result = f12.render_lod_plan(self.world, "miranda", "mess", 2)
        self.assertEqual(["bea", "dina"], result["actors"])
        self.assertEqual(len(self.world["characters"]), result["persistent_population"])
        self.assertNotIn("cla", result["actors"])

    def test_invalid_render_budget_fails_closed(self):
        self.assertEqual(f12.BLOCKED, f12.render_lod_plan(self.world, "miranda", "mess", True)["status"])


if __name__ == "__main__":
    unittest.main()
