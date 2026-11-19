#!/usr/bin/env python3
"""P2 2026-11-19 audit regression: adversarial R1/R2 and causal bridges.
Offline synthetic evidence only; no assertion of CoreRPG execution or signatures.
"""
import copy
import json
import unittest
from pathlib import Path

import simulate_civilization_evolution as b01
import simulate_colonization_expansion as b02
import simulate_conflict_war as b03
import simulate_living_economy as b04
import simulate_procedural_history as b05

ROOT = Path(__file__).resolve().parents[3]
FIX = ROOT / "desarrollo/validation/fixtures"


def fixture(domain, name):
    return json.loads((FIX / domain / name).read_text(encoding="utf-8"))


def civ():
    return fixture("civilization_evolution", "post_contact_divided_world_5y_v0.1.json")["input"]


def colony():
    return fixture("colonization_expansion", "viable_colony_25y_v0.1.json")["input"]


def fleet():
    return fixture("conflict_war", "strategic_operation_v0.1.json")["input"]


def war():
    return fixture("conflict_war", "war_lifecycle_v0.1.json")


def economy():
    return fixture("living_economy", "living_economy_frontier_supply_v0.1.json")["initial_state"]


def historian():
    return fixture("procedural_history", "procedural_history_reconstruction_v0.1.json")


class AuditR1DefectRegression(unittest.TestCase):
    def test_h01_bypass_prewarp_atomic(self):
        for changes in (
            {"inhabited_state": "protected_prewarp"},
            {"inhabited_state": "inhabited_sovereign", "settlement_rights": "none"},
            {"reachable": False}, {"hazard_prohibited": True},
        ):
            i = colony()
            i["years"] = 0
            i["initial"]["settlement_decision"]["candidate"].update(changes)
            before = copy.deepcopy(i)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                b02.simulate_project(**i)
            self.assertEqual(i, before)

    def test_h01_wrong_campaign_target_or_revision(self):
        for field, value in (("campaign_seed", "other"), ("project_id", "other"),
                             ("target_location_id", "other"), ("world_revision", None)):
            i = colony()
            i["years"] = 0
            i["initial"]["settlement_decision"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                b02.simulate_project(**i)

    def test_h02_untyped_population_delta_rejected(self):
        i = civ()
        i["years"] = 1
        i["scheduled_events"] = [{"year": 1, "event_id": "evt:illicit",
                                  "cause_refs": ["fixture:claim"],
                                  "effects": {"population_delta": 1000}}]
        with self.assertRaisesRegex(ValueError, "typed population_change"):
            b01.simulate(**i)

    def test_h02_migration_double_entry_and_replay(self):
        i = civ()
        i["years"] = 1
        ident = i["civilization_id"]
        i["initial"]["accepted_population_facts"] = {
            "fact:migrants": {"status": "accepted", "campaign_seed": i["campaign_seed"],
                              "kind": "migration", "year": 1,
                              "source_ref": "civ:origin", "destination_ref": ident,
                              "amount": 1000, "source_debit": -1000,
                              "destination_credit": 1000, "delta": 1000}}
        event = {"year": 1, "event_id": "evt:transfer", "cause_refs": ["fact:migrants"],
                 "effects": {"population_delta": 1000, "population_change": {
                     "kind": "migration", "accepted_fact_ref": "fact:migrants"}}}
        i["scheduled_events"] = [event]
        result = b01.simulate(**i)
        self.assertEqual(result["final_state"]["population"] -
                         result["snapshots"][0]["population"] >= 1000, True)
        i["scheduled_events"] = [event, dict(event, event_id="evt:duplicate")]
        with self.assertRaisesRegex(ValueError, "already consumed"):
            b01.simulate(**i)
        i["scheduled_events"] = [event]
        i["initial"]["accepted_population_facts"]["fact:migrants"]["source_debit"] = 0
        with self.assertRaisesRegex(ValueError, "unbalanced migration"):
            b01.simulate(**i)

    def test_h02_unverified_catastrophic_loss_rejected(self):
        i = fixture("civilization_evolution", "causal_extinction_v0.1.json")["input"]
        i["scheduled_events"][0]["effects"].pop("accepted_population_loss_fact_ref")
        with self.assertRaisesRegex(ValueError, "unverified catastrophic"):
            b01.simulate(**i)

    def test_h06_b01_no_independent_war_declaration(self):
        i = civ()
        i["years"] = 1
        target = i["initial"]["external_relations"][0]["party_ref"]
        e = {"year": 1, "event_id": "evt:war", "cause_refs": ["incident:contact"],
             "effects": {"relation_target_ref": target, "war_declared": True}}
        i["scheduled_events"] = [e]
        with self.assertRaisesRegex(ValueError, "cannot autonomously"):
            b01.simulate(**i)
        i["initial"]["accepted_conflict_facts"] = {"fact:war": {
            "status": "accepted", "source_domain": "B03/CoreRPG",
            "campaign_seed": i["campaign_seed"],
            "civilization_id": i["civilization_id"], "party_ref": target, "year": 1}}
        e["effects"]["accepted_war_fact_ref"] = "fact:war"
        result = b01.simulate(**i)
        self.assertEqual(result["final_state"]["external_relations"][0]["relation_state"], "war")

    def test_h07_independence_requires_resolution_and_jurisdiction(self):
        i = colony()
        i["years"] = 1
        i["scheduled_events"] = [{"year": 1, "event_id": "evt:illicit",
                                  "cause_refs": ["fixture:assertion"],
                                  "effects": {"independence_recognized": True,
                                              "new_polity_ref": "polity:illicit"}}]
        with self.assertRaisesRegex(ValueError, "accepted jurisdictional"):
            b02.simulate_project(**i)

    def test_h03_repeated_military_unit_rejected(self):
        i = fleet()
        i["attacker"]["units"].append(copy.deepcopy(i["attacker"]["units"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate military"):
            b03.resolve_operation(**i)
        i = fleet()
        i["defender"]["units"][0]["unit_id"] = i["attacker"]["units"][0]["unit_id"]
        with self.assertRaisesRegex(ValueError, "both sides"):
            b03.resolve_operation(**i)

    def test_h03_unowned_or_other_campaign_units_rejected(self):
        i = fleet()
        i["attacker"]["owner_ref"] = "polity:impostor"
        with self.assertRaisesRegex(ValueError, "absent from accepted"):
            b03.resolve_operation(**i)
        i = fleet()
        i["inventory_snapshot"]["campaign_id"] = "other"
        with self.assertRaisesRegex(ValueError, "not accepted"):
            b03.resolve_operation(**i)

    def test_h04_integrity_reduces_second_operation_power(self):
        i = fleet()
        first = b03.resolve_operation(**i)
        self.assertLess(b03.effective_force(first["attacker_after"]),
                        b03.effective_force(i["attacker"]))
        self.assertLess(b03.effective_force(first["defender_after"]),
                        b03.effective_force(i["defender"]))
        i["attacker"], i["defender"] = first["attacker_after"], first["defender_after"]
        second = b03.resolve_operation(**i)
        self.assertEqual(b03.validate_operation(second), [])
        self.assertLessEqual(b03.effective_force(second["attacker_after"]),
                             b03.effective_force(first["attacker_after"]))

    def test_h05_war_without_attestation_and_premature_peace(self):
        f = war()
        bad = copy.deepcopy(f["events"][0])
        bad.pop("accepted_decision_ref")
        with self.assertRaisesRegex(ValueError, "accepted legal"):
            b03.apply_conflict_event(f["initial_state"], bad)
        with self.assertRaisesRegex(ValueError, "illegal conflict transition"):
            b03.apply_conflict_event(f["initial_state"], f["events"][-1])

    def test_h05_state_machine_idempotence_preserves_war_cost(self):
        f = war()
        s = copy.deepcopy(f["initial_state"])
        s["casualties_total"] = 73
        s["reparations_due"] = 50
        for e in f["events"]:
            before = copy.deepcopy(s)
            s = b03.apply_conflict_event(s, e)
            self.assertEqual(b03.apply_conflict_event(s, e), s)
            self.assertEqual(before["casualties_total"], s["casualties_total"])
        self.assertEqual(s["conflict_state"], "peace")
        self.assertEqual(s["reparations_due"], 50)

    def test_h02_b02_negative_migration_cannot_increase_origin(self):
        i = colony()
        i["initial"]["annual_migrants"] = -100
        with self.assertRaisesRegex(ValueError, "negative migration"):
            b02.simulate_project(**i)


class AuditR2TrustRegression(unittest.TestCase):
    def trade(self, **overrides):
        e = {"kind": "trade", "event_id": "audit:trade", "tick": 1,
             "authority_ref": "authorized_actor", "expected_world_revision": 1,
             "seller_store": "colony_merchant", "buyer_store": "colony_customer",
             "seller_acceptance_ref": "sale_offer", "buyer_acceptance_ref": "sale_accepted",
             "item": "ration", "quantity": 1,
             "consideration": {"mode": "latinum", "unit": "latinum_strip",
                               "amount": 1, "buyer_wallet": "customer_wallet",
                               "seller_wallet": "merchant_wallet"}}
        e.update(overrides)
        return e

    def test_h08_third_party_wallet_cannot_pay(self):
        s = economy()
        e = self.trade()
        e["consideration"]["buyer_wallet"] = "merchant_wallet"
        e["consideration"]["seller_wallet"] = "customer_wallet"
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, "wallet ownership"):
            b04.apply_event(s, e)
        self.assertEqual(s, before)

    def test_h08_forced_consent_and_stale_snapshot_fail(self):
        for overrides, reason in (
            ({"buyer_acceptance_ref": "fake_agreement"}, "consent not verified"),
            ({"authority_ref": "unknown_actor"}, "owner delegation"),
            ({"expected_world_revision": 0}, "stale world revision"),
        ):
            s = economy()
            with self.subTest(overrides=overrides), self.assertRaisesRegex(ValueError, reason):
                b04.apply_event(s, self.trade(**overrides))

    def test_h08_owner_reassignment_revokes_consent(self):
        s = economy()
        s["stores"]["colony_customer"]["owner_ref"] = "third_party"
        with self.assertRaisesRegex(ValueError, "owner delegation"):
            b04.apply_event(s, self.trade())

    def test_h09_known_id_not_a_disclosure_grant(self):
        f = historian()
        s = b05.replay(f["initial_state"], f["events"])
        event_id = "hist:record_update_002"
        self.assertEqual(b05.visible_history(s, [event_id], 110, "classified",
                                            actor_ref="audience:unknown"), [])
        self.assertEqual(b05.visible_history(s, [event_id], 104, "classified",
                                            actor_ref="audience:cadet"), [])
        s["knowledge_grants"]["audience:cadet"][1]["campaign_id"] = "foreign"
        self.assertEqual(b05.visible_history(s, [event_id], 110, "classified",
                                            actor_ref="audience:cadet"), [])


if __name__ == "__main__":
    unittest.main()
