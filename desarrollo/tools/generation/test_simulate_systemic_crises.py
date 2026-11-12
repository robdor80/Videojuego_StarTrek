#!/usr/bin/env python3
"""Adversarial tests for P2-B08. Fictional facts are NOT trusted CoreRPG records."""
import copy
import json
import unittest
from pathlib import Path

import simulate_systemic_crises as b8

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "validation/fixtures/systemic_crises/systemic_crisis_galactic_chain_v0.1.json"
REF = "p2b08:demo-2383:shock_subspace"


class SystemicCrisisReferenceTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.state = self.case["state"]
        self.events = self.case["events"]

    def at(self, count):
        return b8.replay(self.state, self.events[:count])

    def event(self, kind, at=15, **fields):
        return dict(event_id="test_" + kind, kind=kind, actor_ref="agency",
                    tick=at, trigger="world", crisis_ref=REF, **fields)

    def rejects(self, state, event):
        original = copy.deepcopy(state)
        with self.assertRaises(ValueError):
            b8.apply_event(state, event)
        self.assertEqual(original, state)

    def test_fixture_is_valid_before_simulation(self):
        self.assertTrue(b8.validate(self.state))

    def test_entire_fixture_replays(self):
        final = self.at(len(self.events))
        self.assertEqual(11, len(final["events"]))
        self.assertEqual("resolved", final["crises"][REF]["state"])

    def test_input_snapshot_is_immutable(self):
        initial = copy.deepcopy(self.state)
        self.at(11)
        self.assertEqual(initial, self.state)

    def test_crisis_is_campaign_scoped_and_shock_anchored(self):
        self.assertEqual(REF, b8.crisis_id("demo-2383", "shock_subspace"))

    def test_no_external_world_state_mutation(self):
        final = self.at(11)
        self.assertEqual(self.state["networks"], final["networks"])
        self.assertEqual(self.state["regions"], final["regions"])
        self.assertEqual(self.state["facts"], final["facts"])

    def test_initial_shock_propagates_across_regions(self):
        p = self.at(1)["crises"][REF]["projection"]
        self.assertEqual(8000, p["network_stress_bps"]["orion_subspace"])
        self.assertEqual(7200, p["network_stress_bps"]["lyra_supply"])
        self.assertEqual(5760, p["network_stress_bps"]["beltran_medical"])
        self.assertEqual(4, p["scope"])

    def test_severity_derived_from_network_not_event_label(self):
        self.assertEqual("high", self.at(1)["crises"][REF]["projection"]["severity"])

    def test_secondary_shock_is_causal_and_does_not_reroll(self):
        self.assertEqual(2, len(self.at(3)["crises"][REF]["shock_refs"]))
        self.assertEqual("shock_beltran", self.at(3)["crises"][REF]["shock_refs"][1])

    def test_projections_are_non_authoritative(self):
        p = self.at(4)["crises"][REF]["projection"]
        self.assertIn("candidate-only", p["note"])
        self.assertNotIn("inventory_delta", p)

    def test_accepted_mitigation_reduces_primary_stress(self):
        p = self.at(5)["crises"][REF]["projection"]
        self.assertEqual(1000, p["network_stress_bps"]["orion_subspace"])

    def test_containment_requires_low_remaining_pressure(self):
        self.assertEqual("contained", self.at(7)["crises"][REF]["state"])

    def test_resolution_requires_zero_remaining_stress(self):
        self.assertFalse(self.at(9)["crises"][REF]["projection"]["network_stress_bps"])

    def test_delayed_communication_only_after_arrival(self):
        self.assertEqual([], b8.view_for(self.at(2), "captain"))
        self.assertEqual(1, len(b8.view_for(self.at(8), "captain")))
        self.assertEqual(2, len(b8.view_for(self.at(11), "captain")))

    def test_uninformed_observer_stays_uninformed(self):
        self.assertEqual([], b8.view_for(self.at(11), "observer"))

    def test_message_is_snapshot_not_telepathic_update(self):
        captain = b8.view_for(self.at(11), "captain")
        self.assertGreater(captain[0]["projection"]["max_pressure_bps"], 0)
        self.assertEqual(0, captain[1]["projection"]["max_pressure_bps"])

    def test_replay_is_deterministic(self):
        self.assertEqual(b8.digest(self.at(11)), b8.digest(self.at(11)))

    def test_same_event_replay_is_idempotent(self):
        snapshot = self.at(1)
        self.assertEqual(snapshot, b8.apply_event(snapshot, self.events[0]))

    def test_same_event_id_changed_payload_is_rejected(self):
        snapshot = self.at(1)
        wrong = dict(self.events[0], tick=20)
        self.rejects(snapshot, wrong)

    def test_rejects_unaccepted_fact(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["status"] = "pending"
        self.rejects(s, self.events[0])

    def test_rejects_foreign_campaign_fact(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["campaign_id"] = "other_campaign"
        self.rejects(s, self.events[0])

    def test_rejects_shock_before_source_time(self):
        e = dict(self.events[0], tick=0)
        self.rejects(self.state, e)

    def test_rejects_open_without_existing_shock(self):
        e = dict(self.events[0], shock_ref="future_fake")
        self.rejects(self.state, e)

    def test_rejects_duplicate_open(self):
        s = self.at(1)
        e = dict(self.events[0], event_id="another_open", tick=3)
        self.rejects(s, e)

    def test_rejects_phantom_shock_network(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["network_ref"] = "invented_route"
        self.rejects(s, self.events[0])

    def test_rejects_unrecognized_shock_family(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["family"] = "omega"
        self.rejects(s, self.events[0])

    def test_rejects_loss_beyond_bps_range(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["loss_bps"] = 12000
        self.rejects(s, self.events[0])

    def test_rejects_boolean_as_bps(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["loss_bps"] = True
        self.rejects(s, self.events[0])

    def test_rejects_player_proximity_trigger(self):
        e = dict(self.events[0], trigger="player")
        self.rejects(self.state, e)

    def test_rejects_player_distance_parameter(self):
        e = dict(self.events[0], player_distance=5)
        self.rejects(self.state, e)

    def test_rejects_inventory_delta_in_event(self):
        e = dict(self.events[0], inventory_delta={"fuel": -10})
        self.rejects(self.state, e)

    def test_rejects_mission_creation_field(self):
        e = dict(self.events[0], mission_id="rescue_001")
        self.rejects(self.state, e)

    def test_rejects_retroactive_history(self):
        s = self.at(1)
        e = self.event("assess", 1)
        self.rejects(s, e)

    def test_rejects_unauthorized_actor_action(self):
        e = dict(self.events[0], actor_ref="captain")
        self.rejects(self.state, e)

    def test_rejects_canonical_collision(self):
        s = copy.deepcopy(self.state)
        s["reserved_ids"].append(REF)
        self.rejects(s, self.events[0])

    def test_rejects_unknown_dependency(self):
        s = copy.deepcopy(self.state)
        s["networks"]["lyra_supply"]["dependencies"][0]["network_ref"] = "not_real"
        self.rejects(s, self.events[0])

    def test_rejects_duplicate_dependency(self):
        s = copy.deepcopy(self.state)
        s["networks"]["lyra_supply"]["dependencies"].append(
            {"network_ref": "orion_subspace", "weight_bps": 100})
        self.rejects(s, self.events[0])

    def test_dependency_cycle_is_bounded_and_deterministic(self):
        s = copy.deepcopy(self.state)
        s["networks"]["orion_subspace"]["dependencies"] = [
            {"network_ref": "lyra_supply", "weight_bps": 10000}]
        a = b8.apply_event(s, self.events[0])
        b = b8.apply_event(copy.deepcopy(s), self.events[0])
        self.assertEqual(a["crises"][REF]["projection"], b["crises"][REF]["projection"])

    def test_rejects_tampered_event_digest(self):
        s = self.at(1)
        s["events"][0]["digest"] = "wrong"
        self.rejects(s, self.events[1])

    def test_rejects_tampered_event_request(self):
        s = self.at(1)
        s["events"][0]["request"]["tick"] = 900
        self.rejects(s, self.events[1])

    def test_rejects_duplicate_shock(self):
        s = self.at(3)
        e = self.event("add_shock", 12, shock_ref="shock_beltran")
        self.rejects(s, e)

    def test_rejects_mitigation_without_authorization(self):
        s = self.at(4)
        e = self.event("mitigate", 6, mitigation_ref="mit_orion_a",
                       authorization_ref="missing")
        self.rejects(s, e)

    def test_rejects_mitigation_by_different_actor(self):
        s = self.at(4)
        e = self.event("mitigate", 6, mitigation_ref="mit_orion_a",
                       authorization_ref="auth_orion")
        e["actor_ref"] = "captain"
        self.rejects(s, e)

    def test_rejects_duplicate_mitigation(self):
        s = self.at(5)
        e = self.event("mitigate", 7, mitigation_ref="mit_orion_a",
                       authorization_ref="auth_orion")
        self.rejects(s, e)

    def test_rejects_early_containment(self):
        s = self.at(4)
        e = self.event("contain", 7, report_ref="report_contained")
        self.rejects(s, e)

    def test_rejects_early_resolution(self):
        s = self.at(4)
        e = self.event("resolve", 9, report_ref="report_restored")
        self.rejects(s, e)

    def test_rejects_resolution_while_stress_remains(self):
        s = self.at(7)
        e = self.event("resolve", 9, report_ref="report_restored")
        self.rejects(s, e)

    def test_rejects_unattested_recovery(self):
        s = self.at(8)
        e = self.event("resolve", 9, report_ref="missing")
        self.rejects(s, e)

    def test_rejects_reactivation_after_resolution(self):
        s = self.at(11)
        e = self.event("add_shock", 13, shock_ref="shock_beltran")
        self.rejects(s, e)

    def test_rejects_classification_leak(self):
        s = self.at(1)
        e = self.event("communicate", 3, recipient_ref="observer",
                       classification="classified", arrival_tick=5)
        self.rejects(s, e)

    def test_rejects_unknown_recipient(self):
        s = self.at(1)
        e = self.event("communicate", 3, recipient_ref="phantom",
                       classification="public", arrival_tick=4)
        self.rejects(s, e)

    def test_rejects_backward_delivery(self):
        s = self.at(1)
        e = self.event("communicate", 3, recipient_ref="captain",
                       classification="public", arrival_tick=2)
        self.rejects(s, e)

    def test_prewarp_intervention_requires_policy_exception(self):
        s = copy.deepcopy(self.state)
        p = "p2b08:demo-2383:shock_primitive"
        s["facts"]["shock_primitive"] = {"kind":"shock","status":"accepted","campaign_id":"demo-2383",
            "tick":1,"network_ref":"primitive_comms","family":"epidemic","loss_bps":7000}
        s["facts"]["mit_primitive"] = {"kind":"mitigation","status":"accepted",
            "campaign_id":"demo-2383","tick":3,"actor_ref":"agency",
            "crisis_ref":p,"network_ref":"primitive_comms","relief_bps":3000}
        s["facts"]["auth_primitive"] = {"kind":"authorization","status":"accepted",
            "campaign_id":"demo-2383","tick":3,"actor_ref":"agency","crisis_ref":p,
            "region_ref":"primitive_world","scope":"intervene"}
        opened = b8.apply_event(s, dict(self.events[0], shock_ref="shock_primitive"))
        e = self.event("mitigate", 3, crisis_ref=p, mitigation_ref="mit_primitive",
                       authorization_ref="auth_primitive")
        self.rejects(opened, e)
        opened["facts"]["review_primitive"] = {
            "kind":"policy_review","status":"accepted","campaign_id":"demo-2383","tick":3,
            "crisis_ref":p,"region_ref":"primitive_world","decision":"approved_exception"}
        e["policy_review_ref"] = "review_primitive"
        self.assertIn("mit_primitive", b8.apply_event(opened, e)["crises"][p]["mitigation_refs"])

    def test_prewarp_policy_cannot_be_implicit(self):
        self.assertTrue(self.state["regions"]["primitive_world"]["prewarp"])
        self.assertNotIn("policy_review_ref", self.events[4])

    def test_cannot_force_direct_network_state_in_event(self):
        s = self.at(1)
        e = self.event("assess", 3, route_creation="wormhole")
        self.rejects(s, e)

    def test_empty_shock_does_not_generate_crisis(self):
        s = copy.deepcopy(self.state)
        s["facts"]["shock_subspace"]["loss_bps"] = 0
        self.rejects(s, self.events[0])

    def test_cross_campaign_snapshots_are_not_interchangeable(self):
        s = copy.deepcopy(self.state)
        s["campaign_id"] = "other"
        self.rejects(s, self.events[0])


if __name__ == "__main__":
    unittest.main()
