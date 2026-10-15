#!/usr/bin/env python3
"""Regresiones F11: resultados offline no equivalen a decisiones CoreRPG."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/validation"))
import f11_career_reference as f11


class F11CareerReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, cls.routes = f11.load_reference_data()
        cls.fixture_path = ROOT / "validation/fixtures/f11/f11_career_scenarios_v0.1.json"
        cls.fixtures = json.loads(cls.fixture_path.read_text(encoding="utf-8"))["scenarios"]
        cls.base = cls.fixtures[0]["profile"]
        cls.offer = cls.fixtures[0]["offer"]

    def profile(self, **changes):
        return {**self.base, **changes}

    def offer_copy(self, **changes):
        return {**self.offer, **changes}

    def check(self, profile=None, offer=None):
        return f11.screen_assignment(
            self.profile() if profile is None else profile,
            self.offer_copy() if offer is None else offer,
            self.catalog, self.routes,
        )

    def review(self, request, profile=None, offer=None):
        return f11.review_career_request(
            self.profile() if profile is None else profile,
            request, offer, self.catalog, self.routes,
        )

    def test_01_all_40_fixture_scenarios(self):
        report = f11.run_scenarios(self.fixture_path)
        self.assertEqual(40, len(report["results"]))
        self.assertTrue(report["all_match"], [r for r in report["results"] if not r["matches_expected"]])

    def test_02_candidate_never_approves(self):
        r = self.check()
        self.assertEqual(f11.CANDIDATE, r["status"])
        self.assertIn("OFFLINE_REFERENCE", r["authority"])

    def test_03_no_mutation_of_inputs(self):
        p, o = self.profile(), self.offer_copy()
        before = copy.deepcopy((p, o))
        self.check(p, o)
        self.assertEqual(before, (p, o))

    def test_04_missing_canonical_class_fails_closed(self):
        self.assertEqual(f11.BLOCKED, self.check(offer=self.offer_copy(class_id="valhalla"))["status"])

    def test_05_bare_future_year_does_not_activate_valhalla(self):
        self.assertEqual(f11.BLOCKED, self.check(self.profile(campaign_year=2480), self.offer_copy(class_id="valhalla"))["status"])

    def test_06_era_is_not_global_ship_unlock(self):
        self.assertEqual(f11.BLOCKED, self.check(self.profile(era_profile="pike", campaign_year=2400), self.offer_copy(class_id="intrepid"))["status"])

    def test_07_unverified_decade_is_conservative(self):
        self.assertFalse(f11.class_temporally_available("galaxy", "tng_ds9_voyager", 2365, self.catalog))

    def test_08_positive_temporal_example(self):
        self.assertTrue(f11.class_temporally_available("galaxy", "tng_ds9_voyager", 2372, self.catalog))

    def test_09_boolean_campaign_year_is_invalid(self):
        self.assertEqual(f11.BLOCKED, self.check(self.profile(campaign_year=True))["status"])
        self.assertEqual(f11.BLOCKED, self.check(self.profile(era_profile=["pike"]))["status"])
        self.assertFalse(f11.class_temporally_available("oberth", ["pike"], 2372, self.catalog))

    def test_10_boolean_vacancy_as_string_is_invalid(self):
        self.assertEqual(f11.BLOCKED, self.check(offer=self.offer_copy(vacancy="true"))["status"])

    def test_11_no_automatic_commission_to_captain(self):
        self.assertEqual(f11.BLOCKED, self.check(offer=self.offer_copy(position_id="ship_captain"))["status"])

    def test_12_player_may_remain_without_progression(self):
        self.assertEqual(f11.NO_CHANGE, self.review({"action": "remain"})["status"])

    def test_13_player_may_decline_promotion(self):
        self.assertEqual(f11.NO_CHANGE, self.review({"action": "decline_promotion"})["status"])

    def test_14_promotions_require_event_evidence(self):
        r = self.review({"action": "promotion", "target_rank": "lieutenant_junior_grade", "evidence_event_ids": []})
        self.assertIn("missing_operational_evidence", r["reasons"])

    def test_15_evidence_never_grants_promotion(self):
        r = self.review({"action": "promotion", "target_rank": "lieutenant_junior_grade", "evidence_event_ids": ["e-1"]})
        self.assertEqual(f11.REVIEW, r["status"])
        self.assertIn("verify_source_events", r["requires"])

    def test_16_skip_ranks_not_allowed(self):
        self.assertEqual(f11.BLOCKED, self.review({"action": "promotion", "target_rank": "commander", "evidence_event_ids": ["e-1"]})["status"])

    def test_17_romance_does_not_grant_promotion(self):
        r = self.review({"action": "promotion", "target_rank": "lieutenant_junior_grade", "romance": "high"})
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_18_permanent_command_requires_rank(self):
        r = self.review({"action": "permanent_command", "evidence_event_ids": ["e-1"]},
                        offer=self.offer_copy(class_id="galaxy", position_id="ship_captain"))
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_19_no_temporary_command_without_order(self):
        r = self.review({"action": "temporary_command", "evidence_event_ids": ["e-1"]},
                        self.profile(rank="commander", command_qualified=True))
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_20_temporary_command_is_not_automatic(self):
        r = self.review({"action": "temporary_command", "evidence_event_ids": ["e-1"],
                         "operational_order_ref": "pending-host-verify"},
                        self.profile(rank="commander", command_qualified=True))
        self.assertEqual(f11.REVIEW, r["status"])

    def test_21_transfer_does_not_change_rank(self):
        r = self.review({"action": "transfer", "evidence_event_ids": ["e-1"]},
                        offer=self.offer_copy(class_id="intrepid"))
        self.assertEqual(f11.REVIEW, r["status"])
        self.assertNotIn("new_rank", r)

    def test_22_specialty_change_requires_training(self):
        r = self.review({"action": "change_specialty", "target_route": "tactical_operations",
                         "bridging_qualification": "cross_training", "evidence_event_ids": ["e-1"]})
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_23_command_qualification_does_not_autofill_vacancy(self):
        r = self.review({"action": "permanent_command", "evidence_event_ids": ["e-1"]},
                        self.profile(rank="captain", command_qualified=True),
                        self.offer_copy(class_id="galaxy", position_id="ship_captain",
                                        accepted_ranks=["captain"], vacancy=False))
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_24_rank_and_command_need_formal_decision(self):
        r = self.review({"action": "permanent_command", "evidence_event_ids": ["e-1"]},
                        self.profile(rank="captain", command_qualified=True),
                        self.offer_copy(class_id="galaxy", position_id="ship_captain",
                                        accepted_ranks=["captain"], required_qualifications=[]))
        self.assertEqual(f11.REVIEW, r["status"])
        self.assertIn("commit_append_only_in_CoreRPG", r["requires"])

    def test_25_stable_digest(self):
        obj = {"z": 1, "a": [1, 2]}
        self.assertEqual(f11.scenario_fingerprint(obj), f11.scenario_fingerprint({"a": [1, 2], "z": 1}))

    def test_26_changes_affect_digest(self):
        self.assertNotEqual(f11.scenario_fingerprint({"x": 1}), f11.scenario_fingerprint({"x": 2}))

    def test_27_unverified_officer_not_allowed_by_unknown_class(self):
        self.assertEqual(f11.BLOCKED, self.check(offer=self.offer_copy(class_id="odyssey"))["status"])

    def test_28_partial_catalog_cannot_authorize(self):
        self.assertEqual(f11.BLOCKED, f11.screen_assignment(self.profile(), self.offer_copy(), {"classes": []}, self.routes)["status"])
        corrupted = copy.deepcopy(self.catalog)
        corrupted["classes"][0]["availability"]["retained_playable_profiles"] = None
        self.assertFalse(f11.class_temporally_available("constitution", "pike", 2260, corrupted))

    def test_29_duplicate_evidence_ids_rejected(self):
        r = self.review({"action": "promotion", "target_rank": "lieutenant_junior_grade",
                         "evidence_event_ids": ["x", "x"]})
        self.assertEqual(f11.BLOCKED, r["status"])

    def test_30_social_history_retained_in_requirements(self):
        r = self.review({"action": "evaluation", "evidence_event_ids": ["x"], "supervisor_id": "npc-1"})
        self.assertIn("preserve_social_history", r["requires"])

    def test_31_no_write_side_effect(self):
        original = self.fixture_path.read_bytes()
        f11.run_scenarios(self.fixture_path)
        self.assertEqual(original, self.fixture_path.read_bytes())

    def test_32_route_is_preference_not_hard_ship_lock(self):
        r = self.check(offer=self.offer_copy(class_id="galaxy"))
        self.assertEqual(f11.CANDIDATE, r["status"])
        self.assertEqual("cross_route_possible", r["route_fit"])

    def test_33_malformed_route_does_not_crash(self):
        self.assertEqual(f11.BLOCKED, self.check(profile=self.profile(route=["science"]))["status"])

    def test_34_malformed_action_does_not_crash(self):
        self.assertEqual(f11.BLOCKED, self.review({"action": ["promotion"]})["status"])

    def test_35_no_payload_authoritative_overrides(self):
        offer = self.offer_copy(vacancy=False, host_approved=True, commander_override=True)
        self.assertEqual(f11.BLOCKED, self.check(offer=offer)["status"])

    def test_36_evaluation_lacks_AI_scoring_authority(self):
        r = self.review({"action": "evaluation", "evidence_event_ids": ["x"], "supervisor_id": "npc",
                         "ai_rating": "perfect"})
        self.assertEqual(f11.REVIEW, r["status"])
        self.assertEqual("OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION", r["authority"])

    def test_37_approved_route_priorities_remain_separated(self):
        routes = self.routes["routes"]
        self.assertEqual(["oberth", "intrepid", "nebula"], routes["science"]["class_priorities"])
        self.assertEqual(["nova"], routes["science"]["class_candidates_to_verify"])
        self.assertEqual(["miranda"], routes["tactical_operations"]["class_priorities"])
        self.assertEqual(["saber", "akira", "steamrunner"], routes["tactical_operations"]["class_candidates_to_verify"])
        self.assertEqual(["galaxy", "sovereign"], routes["exploration_command"]["class_priorities"])
        self.assertEqual(["odyssey", "valhalla"], routes["exploration_command"]["class_candidates_to_verify"])

    def test_38_fixed_career_contracts_still_match_reference_guards(self):
        progression = json.loads((ROOT / "gameplay/careers/starfleet_service/career_progression_rules.json").read_text(encoding="utf-8"))
        promotion = json.loads((ROOT / "gameplay/careers/promotions/promotion_pipeline.json").read_text(encoding="utf-8"))
        assignment = json.loads((ROOT / "gameplay/careers/assignments/assignment_transition.json").read_text(encoding="utf-8"))
        self.assertEqual("foundation_fixed", progression["status"])
        self.assertIn("available_billet", progression["transfer_inputs"])
        self.assertFalse(promotion["xp_directly_promotes"])
        self.assertTrue(promotion["promotion_can_occur_without_transfer"])
        self.assertTrue(promotion["transfer_can_occur_without_promotion"])
        self.assertTrue({"validate_vacancy", "validate_rank", "validate_qualification", "issue_orders"}.issubset(assignment["start_steps"]))


if __name__ == "__main__":
    unittest.main()
