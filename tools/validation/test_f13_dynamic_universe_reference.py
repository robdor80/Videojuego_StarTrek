#!/usr/bin/env python3
"""Regresiones F13: referencia offline; no prueba CoreRPG, UE5 ni simulación galáctica real."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "validation"))
import f13_dynamic_universe_reference as f13


class TestF13DynamicUniverseReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            (ROOT / "validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json").read_text(encoding="utf-8")
        )

    def setUp(self):
        self.world = copy.deepcopy(self.fixture["world"])
        self.layers = {
            "complete_range": [1, 118],
            "layer_119": "PARTIAL",
            "layer_120": "BLOCKED_RUNTIME",
            "source_refs": [
                "docs/roadmap/procedural_layers_master_plan_v0.1.md",
                "docs/roadmap/procedural_runtime_readiness_v0.1.md",
            ],
        }
        self.states = {str(i): ("COMPLETE" if i <= 3 else "READY_TO_RESUME" if i == 4 else "TODO")
                       for i in range(1, 11)}
        self.trade = {
            "trade_id": "trade_test",
            "buyer_inventory_ref": "inv_naral",
            "seller_inventory_ref": "inv_sb12",
            "resource": "medical_supplies",
            "quantity": 20,
            "route_ref": "route_antares_naral",
            "source_need_ref": "need_medicine",
            "operator_ref": "operator_7",
        }

    def test_fixture_has_44_scenarios(self):
        result = f13.run_scenarios(ROOT / "validation/fixtures/f13/f13_dynamic_universe_scenarios_v0.1.json")
        self.assertEqual(44, result["scenario_count"])
        self.assertEqual(44, result["passed"], result["failed_ids"])

    def test_world_is_consistent(self):
        self.assertTrue(f13.validate_world(self.world))

    def test_world_rejects_negative_stock(self):
        self.world["inventories"]["inv_naral"]["stocks"]["food"] = -1
        with self.assertRaises(ValueError):
            f13.validate_world(self.world)

    def test_world_rejects_uncausal_traffic(self):
        self.world["traffic"]["traffic_med"]["cause_ref"] = ""
        with self.assertRaises(ValueError):
            f13.validate_world(self.world)

    def test_world_rejects_unknown_route_endpoint(self):
        self.world["routes"]["route_sol_antares"]["destination_ref"] = "nowhere"
        with self.assertRaises(ValueError):
            f13.validate_world(self.world)

    def test_layers_do_not_overclaim_runtime(self):
        result = f13.audit_layers(self.layers)
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertEqual([120], result["runtime_blocked_layers"])

    def test_canonical_roadmap_sources_are_the_real_f13_frontier(self):
        result = f13.audit_repository(ROOT)
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertEqual(118, result["complete_layers"])
        self.assertEqual([119], result["partial_layers"])
        self.assertEqual([120], result["runtime_blocked_layers"])
        self.assertEqual(4, result["active_reference_block"])

    def test_layer_119_cannot_be_falsely_closed(self):
        self.layers["layer_119"] = "COMPLETE"
        self.assertEqual(f13.BLOCKED, f13.audit_layers(self.layers)["status"])

    def test_block_4_is_next(self):
        result = f13.gate_dynamic_blocks(self.states, 4)
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertEqual(4, result["active_reference_block"])

    def test_cannot_skip_to_block_9_missions(self):
        result = f13.gate_dynamic_blocks(self.states, 9)
        self.assertEqual(f13.BLOCKED, result["status"])
        self.assertIn("out_of_order_dynamic_block", result["reasons"])

    def test_block_progression_can_advance_after_reference_close(self):
        self.states["4"] = "REFERENCE_COMPLETE"
        self.states["5"] = "IN_PROGRESS"
        self.assertEqual(f13.REVIEW, f13.gate_dynamic_blocks(self.states, 5)["status"])

    def test_trade_is_candidate_not_mutation(self):
        before = copy.deepcopy(self.world)
        result = f13.screen_economic_transfer(self.world, self.trade)
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertIn("NO_WORLD_STATE_MUTATION", result["authority"])
        self.assertEqual(before, self.world)

    def test_trade_requires_live_demand(self):
        self.trade["source_need_ref"] = "need_closed"
        self.assertEqual(f13.BLOCKED, f13.screen_economic_transfer(self.world, self.trade)["status"])

    def test_trade_conserves_stock_in_replay(self):
        evt = {"event_id": "t1", "tick": 1, "event_type": "trade", "cause_refs": ["evt_epidemic_1"],
               "trade": self.trade}
        result = f13.replay_reference(self.world, [evt], 2)
        self.assertEqual(100, result["final_inventories"]["inv_sb12"]["medical_supplies"])
        self.assertEqual(30, result["final_inventories"]["inv_naral"]["medical_supplies"])

    def test_replay_never_mutates_input_world(self):
        before = copy.deepcopy(self.world)
        evt = {"event_id": "p1", "tick": 1, "event_type": "production", "cause_refs": ["factory_shift"],
               "inventory_ref": "inv_naral", "resource": "food", "amount": 5}
        f13.replay_reference(self.world, [evt], 2)
        self.assertEqual(before, self.world)

    def test_replay_rejects_negative_inventory(self):
        evt = {"event_id": "c1", "tick": 1, "event_type": "consumption", "cause_refs": ["usage"],
               "inventory_ref": "inv_naral", "resource": "dilithium", "amount": 99}
        result = f13.replay_reference(self.world, [evt], 2)
        self.assertEqual(f13.BLOCKED, result["status"])

    def test_replay_requires_cause(self):
        evt = {"event_id": "p1", "tick": 1, "event_type": "production", "cause_refs": [],
               "inventory_ref": "inv_naral", "resource": "food", "amount": 1}
        self.assertEqual("event_without_cause", f13.replay_reference(self.world, [evt], 2)["reasons"][0])

    def test_replay_digest_is_deterministic(self):
        evt = {"event_id": "p1", "tick": 1, "event_type": "production", "cause_refs": ["factory_shift"],
               "inventory_ref": "inv_naral", "resource": "food", "amount": 5}
        a = f13.replay_reference(self.world, [evt], 2)
        b = f13.replay_reference(copy.deepcopy(self.world), [copy.deepcopy(evt)], 2)
        self.assertEqual(a["sha256"], b["sha256"])

    def test_disruption_projects_existing_traffic_only(self):
        crisis = {"crisis_id": "cr1", "severity": "high", "cause_event_refs": ["war_evt"],
                  "affected_route_refs": ["route_antares_naral"]}
        result = f13.project_disruption(self.world, crisis)
        self.assertEqual(["traffic_med"], result["affected_traffic"])

    def test_prewarp_formal_contact_warns_but_does_not_fake_hard_block(self):
        req = {"civilization_ref": "vestra_prewarp", "requested_scope": "formal_contact",
               "mission_authority_ref": "order_obs"}
        result = f13.assess_contact(self.world, req)
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertIn("prime_directive_noninterference_warning", result["reasons"])

    def test_prewarp_observation_is_valid_review_path(self):
        req = {"civilization_ref": "vestra_prewarp", "requested_scope": "observe",
               "mission_authority_ref": "order_obs"}
        result = f13.assess_contact(self.world, req)
        self.assertEqual("observe", result["recommended_scope"])

    def test_warp_is_candidate_not_mandatory_contact(self):
        req = {"civilization_ref": "naral_union", "requested_scope": "formal_contact",
               "mission_authority_ref": "order_fc"}
        result = f13.assess_contact(self.world, req)
        self.assertIn("warp_threshold_is_candidate_not_mandatory_contact", result["reasons"])

    def test_mission_comes_from_existing_need(self):
        result = f13.derive_mission_candidate(self.world, "need_medicine", "uss_miranda")
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertEqual("evt_epidemic_1", result["cause_ref"])

    def test_mission_does_not_exist_without_need(self):
        result = f13.derive_mission_candidate(self.world, "missing_need", "uss_miranda")
        self.assertEqual(f13.NO_MISSION, result["status"])

    def test_player_proximity_is_not_needed_to_make_mission_candidate(self):
        result = f13.derive_mission_candidate(self.world, "need_science", "uss_oberth")
        self.assertEqual(f13.REVIEW, result["status"])
        self.assertNotIn("player", json.dumps(result).lower())

    def test_capability_blocks_wrong_ship(self):
        result = f13.derive_mission_candidate(self.world, "need_medicine", "uss_oberth")
        self.assertEqual(f13.NO_MISSION, result["status"])
        self.assertIn("medical", result["missing_capabilities"])

    def test_legal_access_is_not_invented(self):
        result = f13.derive_mission_candidate(self.world, "need_border", "uss_sovereign")
        self.assertEqual(f13.NO_MISSION, result["status"])
        self.assertIn("legal_access_unresolved", result["reasons"])

    def test_new_need_can_yield_candidate_after_causal_event(self):
        evt = {
            "event_id": "n1", "tick": 1, "event_type": "need_open", "cause_refs": ["distress_evt"],
            "need": {"need_id": "need_rescue", "cause_ref": "distress_evt",
                     "required_capabilities": ["medical"], "route_ref": "route_sol_antares",
                     "legal_access_required": False},
        }
        result = f13.replay_reference(self.world, [evt], 2)
        refs = {(x["need_ref"], x["ship_ref"]) for x in result["mission_candidates"]}
        self.assertTrue(any(n == "need_rescue" for n, _ in refs))


if __name__ == "__main__":
    unittest.main()
