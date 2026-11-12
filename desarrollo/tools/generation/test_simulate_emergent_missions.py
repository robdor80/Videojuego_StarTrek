#!/usr/bin/env python3
"""Pruebas adversariales B09: referencia offline, no prueba de misiones en UE5/CoreRPG."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "desarrollo/tools/generation"))
import simulate_emergent_missions as m

FIXTURE = ROOT / "desarrollo/validation/fixtures/emergent_missions/verified_unmet_need_npc_response_v0.1.json"
MED = "p2b09:demo-2383:need_med:npc_medical"
PRE = "p2b09:demo-2383:need_prewarp:npc_science"


class B09Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def setUp(self):
        self.s = copy.deepcopy(self.fixture["state"])
        self.events = copy.deepcopy(self.fixture["events"])

    def after(self, count):
        for ev in self.events[:count]:
            self.s = m.apply(self.s, ev)
        return self.s

    def expect_rejected(self, event, reason=None):
        before = copy.deepcopy(self.s)
        with self.assertRaises(ValueError) as cm:
            m.apply(self.s, event)
        if reason is not None:
            self.assertIn(reason, str(cm.exception))
        self.assertEqual(before, self.s)

    def test_01_fixture_is_synthetic(self):
        self.assertEqual("SYNTHETIC_NONCANONICAL", self.fixture["kind"])

    def test_02_state_valid(self):
        self.assertTrue(m.validate(self.s))

    def test_03_same_input_same_hash(self):
        a = m.run_fixture(self.fixture)
        b = m.run_fixture(copy.deepcopy(self.fixture))
        self.assertEqual(a["state_sha256"], b["state_sha256"])

    def test_04_final_npc_mission_and_separate_prewarp_proposal(self):
        summary = m.run_fixture(self.fixture)
        self.assertEqual(6, summary["event_count"])
        self.assertEqual("completed", summary["mission_states"][MED])
        self.assertEqual("proposed", summary["mission_states"][PRE])
        self.assertTrue(summary["initial_unchanged"])

    def test_05_no_need_no_mission(self):
        self.assertEqual("NO_MISSION", m.can_screen(self.s, "agency", "unknown", "npc_medical", 4)["status"])

    def test_06_preaccepted_future_need_not_exposed(self):
        self.assertIn("no_accepted_need", m.can_screen(self.s, "agency", "need_med", "npc_medical", 1)["reasons"])

    def test_07_external_consequence_required(self):
        self.s["facts"]["need_med"]["cause_ref"] = "unproven"
        self.expect_rejected(self.events[1], "invalid_need")

    def test_08_projection_not_a_consequence(self):
        self.s["facts"]["incident_medical"]["kind"] = "risk_projection"
        self.expect_rejected(self.events[1], "invalid_fact_kind")

    def test_09_foreign_campaign_fact_denied(self):
        self.s["facts"]["need_med"]["campaign_id"] = "other"
        self.expect_rejected(self.events[1], "unaccepted_or_foreign_fact")

    def test_10_unaccepted_need_denied(self):
        self.s["facts"]["need_med"]["status"] = "proposed"
        self.expect_rejected(self.events[1], "unaccepted_or_foreign_fact")

    def test_11_needs_are_not_player_events(self):
        req = copy.deepcopy(self.events[1])
        req["trigger"] = "player"
        self.expect_rejected(req, "player_or_script")

    def test_12_distance_field_forbidden(self):
        req = copy.deepcopy(self.events[1])
        req["player_distance"] = 9
        self.expect_rejected(req, "invalid_event_fields")

    def test_13_need_unknown_to_captain_before_delivery(self):
        self.assertIn("need_not_known", m.can_screen(self.s, "captain", "need_med", "enterprise_d", 3)["reasons"])

    def test_14_clearance_blocks_unauthorized_actor(self):
        self.s["actors"]["agency"]["clearance"] = "public"
        self.assertIn("insufficient_clearance", m.can_screen(self.s, "agency", "need_med", "npc_medical", 4)["reasons"])

    def test_15_missing_capability(self):
        self.assertIn("missing_capabilities", m.can_screen(self.s, "agency", "need_med", "npc_science", 4)["reasons"])

    def test_16_unavailable_asset(self):
        self.s["assets"]["npc_medical"]["available"] = False
        self.assertIn("asset_unavailable", m.can_screen(self.s, "agency", "need_med", "npc_medical", 4)["reasons"])

    def test_17_route_closed_does_not_create_new_route(self):
        self.s["routes"]["route_lyra"]["status"] = "closed"
        self.assertIn("existing_route_closed", m.can_screen(self.s, "agency", "need_med", "npc_medical", 4)["reasons"])

    def test_18_route_must_reach_need(self):
        self.s["facts"]["need_med"]["route_ref"] = "route_delta"
        self.expect_rejected(self.events[1], "need_route_destination_mismatch")

    def test_19_proposal_cannot_use_protected_id(self):
        self.s["reserved_ids"].append(MED)
        self.expect_rejected(self.events[1], "reserved_mission_identity")

    def test_20_proposal_id_stable(self):
        self.assertEqual(MED, m.mission_id("demo-2383", "need_med", "npc_medical"))

    def test_21_identical_event_idempotent_even_after_time_advances(self):
        self.after(4)
        before = copy.deepcopy(self.s)
        again = m.apply(self.s, self.events[0])
        self.assertEqual(before, again)
        self.assertEqual(before, self.s)

    def test_22_changed_id_payload_is_rejected(self):
        self.after(2)
        req = copy.deepcopy(self.events[1])
        req["asset_ref"] = "enterprise_d"
        self.expect_rejected(req, "event_id_payload_conflict")

    def test_23_retroactive_new_event_denied(self):
        self.after(2)
        req = copy.deepcopy(self.events[1])
        req["event_id"] = "new_in_past"
        req["tick"] = 3
        self.expect_rejected(req, "retroactive_event")

    def test_24_unknown_actor_does_not_get_proposal_power(self):
        req = copy.deepcopy(self.events[1])
        req["actor_ref"] = "observer"
        self.expect_rejected(req, "actor_scope_denied")

    def test_25_authorize_requires_independent_order(self):
        self.after(2)
        req = copy.deepcopy(self.events[2])
        req["order_ref"] = "missing"
        self.expect_rejected(req, "missing_or_future_order")

    def test_26_authorize_rejects_future_order(self):
        self.after(2)
        req = copy.deepcopy(self.events[2])
        req["tick"] = 4
        self.expect_rejected(req, "missing_or_future_order")

    def test_27_order_must_cover_correct_asset(self):
        self.after(2)
        self.s["facts"]["auth_med"]["asset_ref"] = "enterprise_d"
        self.expect_rejected(self.events[2], "order_scope_or_subject_mismatch")

    def test_28_independent_issuer_not_self_granted(self):
        self.after(2)
        self.s["facts"]["auth_med"]["approved_by_ref"] = "agency"
        self.expect_rejected(self.events[2], "no_independent_order_issuer")

    def test_29_wrong_jurisdiction_blocks(self):
        self.after(2)
        self.s["facts"]["auth_med"]["jurisdiction_ref"] = "delta_sovereign"
        self.expect_rejected(self.events[2], "wrong_jurisdiction")

    def test_30_prewarp_blocks_unreviewed_authorization(self):
        self.after(6)
        req = {"event_id": "pre_auth", "kind": "authorize", "actor_ref": "agency",
               "tick": 10, "trigger": "world", "mission_ref": PRE,
               "order_ref": "auth_prewarp", "policy_ref": None}
        self.expect_rejected(req, "prime_directive_exception_required")

    def test_31_prewarp_only_with_accepted_exception(self):
        self.after(6)
        req = {"event_id": "pre_auth", "kind": "authorize", "actor_ref": "agency",
               "tick": 10, "trigger": "world", "mission_ref": PRE,
               "order_ref": "auth_prewarp", "policy_ref": "policy_prewarp"}
        result = m.apply(self.s, req)
        self.assertEqual("authorized", result["missions"][PRE]["state"])
        self.assertEqual("proposed", self.s["missions"][PRE]["state"])

    def test_32_fake_prewarp_exception_rejected(self):
        self.after(6)
        self.s["facts"]["policy_prewarp"]["decision"] = "denied"
        req = {"event_id": "pre_auth", "kind": "authorize", "actor_ref": "agency",
               "tick": 10, "trigger": "world", "mission_ref": PRE,
               "order_ref": "auth_prewarp", "policy_ref": "policy_prewarp"}
        self.expect_rejected(req, "prime_directive_not_approved")

    def test_33_assignment_requires_order_and_reservation(self):
        self.after(3)
        req = copy.deepcopy(self.events[3])
        req["reservation_ref"] = "missing"
        self.expect_rejected(req, "missing_or_future_reservation")

    def test_34_assignment_uses_matching_existing_reservation(self):
        self.after(3)
        self.s["facts"]["reservation_med"]["asset_ref"] = "enterprise_d"
        self.expect_rejected(self.events[3], "invalid_external_reservation")

    def test_35_assignment_route_may_close(self):
        self.after(3)
        self.s["routes"]["route_lyra"]["status"] = "closed"
        self.expect_rejected(self.events[3], "route_closed")

    def test_36_assignment_does_not_consume_or_relocate_asset(self):
        self.after(3)
        before = copy.deepcopy(self.s["assets"])
        after = m.apply(self.s, self.events[3])
        self.assertEqual(before, after["assets"])

    def test_37_completion_requires_verified_external_outcome(self):
        self.after(4)
        self.s["facts"]["outcome_med"]["result"] = "unknown"
        self.expect_rejected(self.events[4], "unverified_completion")

    def test_38_completion_requires_accepted_need_resolution(self):
        self.after(4)
        req = copy.deepcopy(self.events[4])
        req["resolution_ref"] = "missing"
        self.expect_rejected(req, "missing_or_future_need_resolved")

    def test_39_completion_not_player_success_button(self):
        self.after(4)
        req = copy.deepcopy(self.events[4])
        req["trigger"] = "quest"
        self.expect_rejected(req, "player_or_script_trigger")

    def test_40_closed_need_not_reissued_to_enterprise(self):
        self.after(5)
        verdict = m.can_screen(self.s, "agency", "need_med", "enterprise_d", 9)
        self.assertEqual("NO_MISSION", verdict["status"])
        self.assertIn("need_already_resolved", verdict["reasons"])

    def test_41_no_telepathic_knowledge_before_arrival(self):
        self.after(6)
        self.assertEqual([], m.view(self.s, "captain", 8)["delivered"])
        self.assertEqual("need_med", m.view(self.s, "captain", 9)["delivered"][0]["need_ref"])

    def test_42_delayed_news_is_stale_not_world_truth(self):
        self.after(6)
        notice = m.view(self.s, "captain", 9)["delivered"][0]
        self.assertTrue(notice["reported_open"])
        self.assertEqual(3, notice["as_of_tick"])
        self.assertFalse(m.open_need(self.s, "need_med", 9))

    def test_43_observer_keeps_no_secret_knowledge(self):
        self.after(6)
        self.assertEqual([], m.view(self.s, "observer", 9)["delivered"])

    def test_44_confidentiality_rejects_downgrade(self):
        req = copy.deepcopy(self.events[0])
        req["classification"] = "public"
        self.expect_rejected(req, "confidentiality_violation")

    def test_45_no_future_message_arrives_in_past(self):
        req = copy.deepcopy(self.events[0])
        req["arrival_tick"] = 2
        self.expect_rejected(req, "negative_delivery_delay")

    def test_46_cannot_send_secret_to_low_clearance(self):
        req = copy.deepcopy(self.events[0])
        req["recipient_ref"] = "observer"
        self.expect_rejected(req, "confidentiality_violation")

    def test_47_tampered_event_digest_rejected(self):
        self.after(2)
        self.s["events"][0]["digest"] = "bad"
        with self.assertRaisesRegex(ValueError, "tampered_history"):
            m.validate(self.s)

    def test_48_tampered_mission_id_rejected(self):
        self.after(2)
        self.s["missions"][MED]["mission_id"] = "fake"
        with self.assertRaisesRegex(ValueError, "invalid_mission"):
            m.validate(self.s)

    def test_49_double_proposal_of_same_identity_denied(self):
        self.after(2)
        req = copy.deepcopy(self.events[1])
        req["event_id"] = "new"
        req["tick"] = 5
        self.expect_rejected(req, "mission_already_exists")

    def test_50_reject_mission_created_by_player_to_fix_no_need(self):
        req = copy.deepcopy(self.events[1])
        req["need_ref"] = "invented_by_player"
        self.expect_rejected(req, "candidate_blocked")

    def test_51_invalid_canonical_campaign_reference_blocked(self):
        self.s["facts"]["incident_medical"]["campaign_id"] = "other"
        self.expect_rejected(self.events[1], "unaccepted_or_foreign_fact")

    def test_52_wrong_lifecycle_order(self):
        self.after(2)
        self.expect_rejected(self.events[3], "wrong_lifecycle_state")

    def test_53_completed_mission_cannot_be_authorized_again(self):
        self.after(5)
        req = copy.deepcopy(self.events[2])
        req["event_id"] = "wrong_again"
        req["tick"] = 9
        self.expect_rejected(req, "wrong_lifecycle_state")

    def test_54_replay_invariant_no_world_side_effects(self):
        world = copy.deepcopy(self.fixture["state"])
        m.run_fixture(self.fixture)
        self.assertEqual(world, self.fixture["state"])

    def test_55_closed_need_before_first_offer_blocks(self):
        self.s["facts"]["resolution_med"]["tick"] = 3
        self.assertIn("need_already_resolved",
                      m.can_screen(self.s, "agency", "need_med", "npc_medical", 4)["reasons"])

    def test_56_missions_are_npc_operable_without_player(self):
        report = m.run_fixture(self.fixture)
        self.assertEqual("completed", report["mission_states"][MED])
        self.assertNotIn("player", json.dumps(report).lower())

    def test_57_reference_refuses_live_classification(self):
        bogus = copy.deepcopy(self.fixture)
        bogus["kind"] = "CORE_LIVE"
        with self.assertRaisesRegex(ValueError, "real_world_claim"):
            m.run_fixture(bogus)


    def test_58_route_requires_existing_origin(self):
        del self.s["routes"]["route_lyra"]["origin_ref"]
        self.expect_rejected(self.events[1], "invalid_route")

    def test_59_asset_must_be_at_route_origin(self):
        self.s["assets"]["npc_medical"]["location_ref"] = "lyra_colony"
        self.assertIn("asset_not_on_route_origin",
                      m.can_screen(self.s, "agency", "need_med", "npc_medical", 4)["reasons"])

    def test_60_assignment_rechecks_route_origin(self):
        self.after(3)
        self.s["assets"]["npc_medical"]["location_ref"] = "lyra_colony"
        self.expect_rejected(self.events[3], "asset_not_on_route_origin")

    def test_61_view_cannot_advance_world_clock(self):
        self.after(1)
        with self.assertRaisesRegex(ValueError, "future_view_forbidden"):
            m.view(self.s, "captain", 9)

    def test_62_assigned_need_suppresses_competing_offer(self):
        self.after(4)
        verdict = m.can_screen(self.s, "agency", "need_med", "enterprise_d", 6)
        self.assertEqual("NO_MISSION", verdict["status"])
        self.assertIn("need_already_assigned", verdict["reasons"])

    def test_63_no_parallel_assignment_to_same_need(self):
        self.after(4)
        other = m.mission_id("demo-2383", "need_med", "enterprise_d")
        self.s["missions"][other] = {"mission_id": other, "need_ref": "need_med",
                                      "asset_ref": "enterprise_d", "originator_ref": "agency",
                                      "opened_tick": 4, "state": "authorized"}
        self.s["facts"]["order_second"] = {"kind": "order", "status": "accepted",
            "campaign_id": "demo-2383", "tick": 7, "purpose": "assign",
            "mission_ref": other, "need_ref": "need_med", "asset_ref": "enterprise_d",
            "actor_ref": "agency", "approved": True, "approved_by_ref": "admiralty",
            "jurisdiction_ref": "federation_lyra"}
        self.s["facts"]["reservation_second"] = {"kind": "reservation", "status": "accepted",
            "campaign_id": "demo-2383", "tick": 7, "purpose": "mission_assignment",
            "mission_ref": other, "asset_ref": "enterprise_d", "granted_by_ref": "admiralty"}
        req = {"event_id": "second_dispatch", "kind": "assign", "actor_ref": "agency",
               "tick": 7, "trigger": "world", "mission_ref": other,
               "order_ref": "order_second", "reservation_ref": "reservation_second",
               "policy_ref": None}
        self.expect_rejected(req, "need_already_assigned")

    def test_64_consequence_cannot_postdate_need(self):
        self.s["facts"]["incident_medical"]["tick"] = 3
        self.expect_rejected(self.events[1], "invalid_need")

    def test_65_external_reservation_must_have_independent_grant(self):
        self.after(3)
        self.s["facts"]["reservation_med"]["granted_by_ref"] = "agency"
        self.expect_rejected(self.events[3], "invalid_external_reservation")

if __name__ == "__main__":
    unittest.main()
