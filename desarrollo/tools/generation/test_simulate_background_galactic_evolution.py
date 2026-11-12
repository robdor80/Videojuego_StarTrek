#!/usr/bin/env python3
"""Adversarial P2-B10 offline scheduling tests; never attest CoreRPG runtime."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "desarrollo/tools/generation/simulate_background_galactic_evolution.py"
FIXTURE = ROOT / "desarrollo/validation/fixtures/background_galactic_evolution/verified_npc_offscreen_catchup_v0.1.json"
spec = importlib.util.spec_from_file_location("p2b10", SCRIPT)
b10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b10)


class BackgroundGalacticEvolutionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.initial = copy.deepcopy(self.fixture["state"])

    def run_0_3(self, state=None):
        return b10.advance(self.initial if state is None else state, 3, "clock_0_3")

    def run_full(self):
        return b10.run_fixture(copy.deepcopy(self.fixture))

    def test_01_fixture_is_synthetic_and_initial_valid(self):
        self.assertEqual("SYNTHETIC_NONCANONICAL", self.fixture["kind"])
        self.assertTrue(b10.validate(self.initial))

    def test_02_fixture_has_six_real_external_tasks(self):
        self.assertEqual(6, len(self.initial["tasks"]))
        self.assertTrue(all(x["intent_ref"] in self.initial["facts"]
                            for x in self.initial["tasks"].values()))

    def test_03_fixture_runs_without_mutating_original(self):
        before = copy.deepcopy(self.fixture)
        result = self.run_full()
        self.assertTrue(result["initial_unchanged"])
        self.assertEqual(before, self.fixture)

    def test_04_all_six_tasks_dispatch_without_player(self):
        result = self.run_full()
        self.assertEqual(6, len(result["dispatches"]))
        self.assertEqual("OFFLINE_REFERENCE_ONLY", result["authority"])
        self.assertTrue(all(x["authority"] == "PROPOSAL_ONLY"
                            for x in result["dispatches"]))

    def test_05_virtual_clock_advances_three_bounded_batches(self):
        result = self.run_full()
        self.assertEqual(8, result["final_tick"])
        self.assertEqual(4, result["journal_entries"])

    def test_06_priority_and_domain_quota_bound_first_tick(self):
        state = self.run_0_3()
        first = [x for x in state["outbox"] if x["tick"] == 1]
        self.assertEqual(["t_b04", "t_b08"], [x["task_id"] for x in first])
        self.assertEqual(2, len(first))

    def test_07_fifo_and_delayed_lower_priority_tasks(self):
        state = self.run_0_3()
        self.assertEqual(["t_b06", "t_b02"], [x["task_id"] for x in state["outbox"] if x["tick"] == 2])
        self.assertEqual(["t_b09", "t_b05"], [x["task_id"] for x in state["outbox"] if x["tick"] == 3])

    def test_08_deterministic_hash_and_schedule_replay(self):
        self.assertEqual(self.run_full(), self.run_full())

    def test_09_replay_with_json_serialization_is_stable(self):
        data = json.loads(json.dumps(self.fixture))
        self.assertEqual(self.run_full()["snapshot_sha256"],
                         b10.run_fixture(data)["snapshot_sha256"])

    def test_10_no_automatic_world_effects_or_hidden_state(self):
        state = self.run_0_3()
        self.assertEqual(b10.STATE_FIELDS, set(state))
        self.assertFalse(any(key in state for key in ("world_delta", "economy",
                         "galactic_population", "missions", "war_state", "rng")))

    def test_11_player_lod_injection_forbidden(self):
        state = copy.deepcopy(self.initial)
        state["lod"] = "full"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_12_player_presence_in_task_forbidden(self):
        state = copy.deepcopy(self.initial)
        state["tasks"]["t_b09"]["player_present"] = True
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_13_camera_distance_not_valid_clock(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["clock_0_3"]["issuer_ref"] = "camera"
        with self.assertRaises(ValueError):
            b10.advance(state, 3, "clock_0_3")

    def test_14_advance_requires_exact_clock_proof(self):
        with self.assertRaises(ValueError):
            b10.advance(self.initial, 3, "intent_b04")

    def test_15_wrong_clock_authority_is_blocked(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["clock_0_3"]["end_tick"] = 4
        with self.assertRaises(ValueError):
            b10.advance(state, 3, "clock_0_3")

    def test_16_wallclock_does_not_advance_anything(self):
        self.assertEqual(0, self.initial["tick"])
        self.assertEqual([], self.initial["outbox"])

    def test_17_negative_and_float_ticks_rejected(self):
        for value in (-1, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                b10.advance(self.initial, value, "clock_0_3")

    def test_18_oversized_catchup_is_rejected(self):
        with self.assertRaises(ValueError):
            b10.advance(self.initial, 8, "clock_0_3")

    def test_19_clock_reversal_is_rejected(self):
        with self.assertRaises(ValueError):
            b10.advance(self.run_0_3(), 1, "clock_0_3")

    def test_20_clock_ref_cannot_be_reused(self):
        with self.assertRaises(ValueError):
            b10.advance(self.run_0_3(), 6, "clock_0_3")

    def test_21_unaccepted_intent_is_rejected(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["intent_b04"]["status"] = "proposed"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_22_foreign_campaign_fact_rejected(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["intent_b04"]["campaign_id"] = "another"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_23_revision_mismatch_rejected(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["intent_b04"]["world_revision"] = "stale"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_24_causal_source_ref_must_exist(self):
        state = copy.deepcopy(self.initial)
        state["tasks"]["t_b04"]["source_refs"] = ["forged", "intent_b04"]
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_25_external_domain_ownership_is_enforced(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["intent_b04"]["owner_ref"] = "B09"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_26_future_intent_cannot_be_dispatched(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["intent_b04"]["tick"] = 5
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_27_b09_needs_independently_accepted_need(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["need_med"]["status"] = "projection"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_28_b09_cannot_use_risk_instead_of_need(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["need_med"]["kind"] = "domain_intent"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_29_conflicting_duplicate_task_identity_rejected(self):
        state = copy.deepcopy(self.initial)
        state["tasks"]["t_b04"]["source_refs"] = ["intent_b04", "intent_b04"]
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_30_budget_must_be_positive_integer(self):
        state = copy.deepcopy(self.initial)
        state["config"]["budget_per_tick"] = 0
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_31_per_domain_limit_cannot_exceed_budget(self):
        state = copy.deepcopy(self.initial)
        state["config"]["per_domain_quota"] = 3
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_32_backpressure_preserves_unprocessed_tasks(self):
        state = copy.deepcopy(self.initial)
        state["config"]["max_pending_outbox"] = 2
        after = b10.advance(state, 3, "clock_0_3")
        self.assertEqual(2, len(after["outbox"]))
        self.assertEqual(6, len(after["tasks"]))

    def test_33_accepted_external_receipt_is_recorded_not_executed(self):
        state = self.run_0_3()
        state = b10.acknowledge(state, "p2b10:demo-2383:t_b04", "receipt_b04")
        self.assertEqual(1, len(state["receipts"]))
        self.assertEqual("accepted", state["facts"]["receipt_b04"]["result"])
        self.assertFalse("world_delta" in state)

    def test_34_duplicate_exact_ack_is_idempotent(self):
        state = self.run_0_3()
        state = b10.acknowledge(state, "p2b10:demo-2383:t_b04", "receipt_b04")
        self.assertEqual(state, b10.acknowledge(state, "p2b10:demo-2383:t_b04", "receipt_b04"))

    def test_35_ack_before_dispatch_is_rejected(self):
        with self.assertRaises(ValueError):
            b10.acknowledge(self.initial, "p2b10:demo-2383:t_b04", "receipt_b04")

    def test_36_wrong_receipt_fails_atomically(self):
        state = self.run_0_3()
        before = copy.deepcopy(state)
        with self.assertRaises(ValueError):
            b10.acknowledge(state, "p2b10:demo-2383:t_b04", "intent_b04")
        self.assertEqual(before, state)

    def test_37_ack_future_fact_rejected(self):
        state = self.run_0_3()
        state["facts"]["receipt_b04"]["tick"] = 20
        with self.assertRaises(ValueError):
            b10.acknowledge(state, "p2b10:demo-2383:t_b04", "receipt_b04")

    def test_38_tampered_journal_digest_rejected(self):
        state = self.run_0_3()
        state["journal"][0]["digest"] = "bad"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_39_tampered_head_rejected(self):
        state = self.run_0_3()
        state["trace_head"] = "forged"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_40_tampered_outbox_rejected(self):
        state = self.run_0_3()
        state["outbox"][0]["authority"] = "WORLD_WRITER"
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_41_duplicate_dispatch_is_rejected(self):
        state = self.run_0_3()
        state["outbox"].append(copy.deepcopy(state["outbox"][0]))
        with self.assertRaises(ValueError):
            b10.validate(state)

    def test_42_late_delivered_news_only_visible_after_arrival(self):
        state = self.run_0_3()
        self.assertEqual([], b10.view(state, "captain", 3)["delivered"])
        state = b10.acknowledge(state, "p2b10:demo-2383:t_b04", "receipt_b04")
        state = b10.advance(state, 6, "clock_3_6")
        self.assertEqual([], b10.view(state, "captain", 6)["delivered"])
        state = b10.advance(state, 8, "clock_6_8")
        self.assertEqual(["t_b09"], [x["task_id"] for x in b10.view(state, "captain", 8)["delivered"]])

    def test_43_observer_has_no_implicit_omniscience(self):
        self.assertEqual([], self.run_full()["views"]["observer"]["delivered"])
        self.assertEqual([], self.run_full()["views"]["agency"]["delivered"])

    def test_44_invalid_observer_is_rejected(self):
        with self.assertRaises(ValueError):
            b10.view(self.initial, "nobody", 0)

    def test_45_public_clearance_cannot_read_restricted_even_with_delivery(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["delivery_cap"]["recipient_ref"] = "observer"
        state = b10.advance(state, 3, "clock_0_3")
        state = b10.advance(state, 6, "clock_3_6")
        state = b10.advance(state, 8, "clock_6_8")
        self.assertEqual([], b10.view(state, "observer", 8)["delivered"])

    def test_46_renaming_task_changes_stable_dispatch_id(self):
        state = copy.deepcopy(self.initial)
        task = state["tasks"].pop("t_b04")
        state["tasks"]["t_alt"] = task
        state["facts"]["receipt_b04"]["dispatch_id"] = "p2b10:demo-2383:t_alt"
        changed = b10.advance(state, 3, "clock_0_3")
        self.assertIn("p2b10:demo-2383:t_alt",
                      {x["dispatch_id"] for x in changed["outbox"]})

    def test_47_zero_length_clock_request_rejected_without_new_work(self):
        with self.assertRaises(ValueError):
            b10.advance(self.initial, 0, "clock_0_3")
        self.assertEqual([], self.initial["journal"])

    def test_48_false_canon_fixture_is_rejected(self):
        fixture = copy.deepcopy(self.fixture)
        fixture["kind"] = "CANONICAL_WORLDSTATE"
        with self.assertRaises(ValueError):
            b10.run_fixture(fixture)

    def test_49_nonexistent_receipt_ref_cannot_ack(self):
        with self.assertRaises(ValueError):
            b10.acknowledge(self.run_0_3(), "p2b10:demo-2383:t_b04", "missing")

    def test_50_read_only_views_do_not_mutate_source(self):
        state = self.run_0_3()
        before = copy.deepcopy(state)
        b10.view(state, "observer", 3)
        self.assertEqual(before, state)


    def test_51_duplicate_external_intent_cannot_be_dispatched_twice(self):
        state = copy.deepcopy(self.initial)
        state["tasks"]["t_alias"] = copy.deepcopy(state["tasks"]["t_b04"])
        with self.assertRaisesRegex(ValueError, "duplicate_external_intent"):
            b10.validate(state)

    def test_52_delivery_cannot_precede_the_external_message_fact(self):
        state = copy.deepcopy(self.initial)
        state["facts"]["delivery_cap"]["arrival_tick"] = 2
        with self.assertRaisesRegex(ValueError, "premature_delivery"):
            b10.validate(state)

    def test_53_priority_aging_gives_old_background_work_a_fair_turn(self):
        old = {"priority": "background", "due_tick": 0}
        urgent = {"priority": "urgent", "due_tick": 7}
        self.assertLess(b10.priority_key("old", old, 7, 2),
                        b10.priority_key("new", urgent, 7, 2))

    def test_54_hard_config_bound_prevents_unbounded_catchup(self):
        state = copy.deepcopy(self.initial)
        state["config"]["max_batch_ticks"] = 500000
        with self.assertRaisesRegex(ValueError, "configuration_hard_limit"):
            b10.validate(state)


if __name__ == "__main__":
    unittest.main()
