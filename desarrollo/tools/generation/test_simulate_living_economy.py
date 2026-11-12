#!/usr/bin/env python3
"""Reference-level regression suite: P2/B04 Living Interstellar Economy."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIXTURES = ROOT / "desarrollo/validation/fixtures/living_economy"
MODULE_PATH = HERE / "simulate_living_economy.py"
spec = importlib.util.spec_from_file_location("living_economy", MODULE_PATH)
assert spec and spec.loader
le = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = le
spec.loader.exec_module(le)


def fixture(name="living_economy_frontier_supply_v0.1.json"):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def initial():
    return copy.deepcopy(fixture()["initial_state"])


def event(kind, **kwargs):
    return {"event_id": "test-" + kind, "kind": kind, "tick": 1,
            "authority_ref": "authorized_actor", **kwargs}


def produced():
    return le.apply_event(initial(), event("produce", facility_id="frontier_workshop",
                                         item="spare", quantity=3, labor_ref="technician"))


def dispatched():
    s = produced()
    return le.apply_event(s, event("dispatch", tick=2, operator_ref="freight_company",
                                    agreement_ref="contract_001", from_store="colony_depot",
                                    to_store="station_warehouse", route_id="alpha_beta_corridor",
                                    vessel_id="freighter_001", shipment_id="manifest_001",
                                    item="spare", quantity=2))


class LivingEconomyTests(unittest.TestCase):
    def test_01_happy_path_fixture(self):
        f = fixture()
        s = le.replay(f["initial_state"], f["happy_path_events"])
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["ore"], f["expected"]["colony_ore"])
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["spare"], f["expected"]["colony_spares"])
        self.assertEqual(s["stores"]["station_warehouse"]["stock"]["spare"], f["expected"]["station_spares"])
        self.assertEqual(s["last_tick"], f["expected"]["final_tick"])
        self.assertFalse(s["shipments"])

    def test_02_production_consumes_resources_and_power(self):
        s = produced()
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["ore"], 6)
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["spare"], 3)
        self.assertEqual(s["facilities"]["frontier_workshop"]["power_units"], 17)

    def test_03_insufficient_material_rolls_back(self):
        s = initial()
        s["stores"]["colony_depot"]["stock"]["ore"] = 1
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, "insufficient raw material"):
            le.apply_event(s, event("produce", facility_id="frontier_workshop",
                                    item="spare", quantity=2, labor_ref="technician"))
        self.assertEqual(s, before)

    def test_04_batch_capacity_enforced(self):
        with self.assertRaisesRegex(ValueError, "batch"):
            le.apply_event(initial(), event("produce", facility_id="frontier_workshop",
                                            item="spare", quantity=6, labor_ref="technician"))

    def test_05_production_needs_labor_ref(self):
        with self.assertRaisesRegex(ValueError, "labor_ref"):
            le.apply_event(initial(), event("produce", facility_id="frontier_workshop",
                                            item="spare", quantity=1))

    def test_06_replication_requires_real_energy_and_feedstock(self):
        s = le.apply_event(initial(), event("replicate", facility_id="frontier_workshop",
                                            item="medkit", quantity=2))
        f = s["facilities"]["frontier_workshop"]
        self.assertEqual((f["power_units"], f["feedstock"]), (16, 2))
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["medkit"], 2)

    def test_07_powerless_clinic_is_not_magically_supplied(self):
        f = fixture("living_economy_replication_crisis_v0.1.json")
        s = initial()
        s["facilities"][f["modification"]["facility_id"]]["power_units"] = 0
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, f["expected_failure"]):
            le.apply_event(s, f["attempt"])
        self.assertEqual(s, before)
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["medkit"], 0)

    def test_08_missing_pattern_never_generates_strategic_part(self):
        s = initial()
        with self.assertRaisesRegex(ValueError, "pattern"):
            le.apply_event(s, event("replicate", facility_id="frontier_workshop",
                                    item="transphasic_torpedo", quantity=1))

    def test_09_feedstock_and_permission_matter(self):
        s = initial()
        s["facilities"]["frontier_workshop"]["feedstock"] = 0
        with self.assertRaisesRegex(ValueError, "feedstock"):
            le.apply_event(s, event("replicate", facility_id="frontier_workshop",
                                    item="medkit", quantity=1))
        s = initial()
        s["facilities"]["frontier_workshop"]["replication_profiles"]["medkit"]["permitted"] = False
        with self.assertRaisesRegex(ValueError, "permitted"):
            le.apply_event(s, event("replicate", facility_id="frontier_workshop",
                                    item="medkit", quantity=1))

    def test_10_consumption_requires_real_stock_and_cause(self):
        e = event("consume", store_id="colony_depot", item="ration",
                  quantity=2, cause_ref="rations_for_colonists")
        s = le.apply_event(initial(), e)
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["ration"], 8)
        e["quantity"] = 50
        with self.assertRaisesRegex(ValueError, "insufficient stock"):
            le.apply_event(initial(), e)

    def test_11_stock_loss_needs_causal_record(self):
        with self.assertRaisesRegex(ValueError, "cause_ref"):
            le.apply_event(initial(), event("loss", store_id="colony_depot",
                                            item="ration", quantity=1))
        s = le.apply_event(initial(), event("loss", store_id="colony_depot",
                                            item="ration", quantity=1, cause_ref="hold_damage"))
        self.assertEqual(s["stores"]["colony_depot"]["stock"]["ration"], 9)

    def test_12_shipments_conserve_goods_and_do_not_teleport(self):
        s = produced()
        before = le.total_item(s, "spare")
        t = dispatched()
        self.assertEqual(le.total_item(t, "spare"), before)
        self.assertEqual(t["stores"]["station_warehouse"]["stock"]["spare"], 0)
        self.assertEqual(t["shipments"]["manifest_001"]["quantity"], 2)
        self.assertFalse(t["vessels"]["freighter_001"]["available"])

    def test_13_delivery_only_after_elapsed_travel_time(self):
        t = dispatched()
        with self.assertRaisesRegex(ValueError, "not yet due"):
            le.apply_event(t, event("deliver", tick=4, shipment_id="manifest_001"))
        u = le.apply_event(t, event("deliver", tick=5, shipment_id="manifest_001"))
        self.assertEqual(u["stores"]["station_warehouse"]["stock"]["spare"], 2)
        self.assertEqual(u["vessels"]["freighter_001"]["location_ref"], "station_beta")
        self.assertTrue(u["vessels"]["freighter_001"]["available"])

    def test_14_border_closed_before_departure_blocks_dispatch(self):
        s = produced()
        s["routes"]["alpha_beta_corridor"]["legal_access"] = False
        e = event("dispatch", tick=2, operator_ref="freight_company",
                  agreement_ref="contract_001", from_store="colony_depot",
                  to_store="station_warehouse", route_id="alpha_beta_corridor",
                  vessel_id="freighter_001", shipment_id="manifest_001",
                  item="spare", quantity=2)
        with self.assertRaisesRegex(ValueError, "inaccessible"):
            le.apply_event(s, e)

    def test_15_border_closed_during_transit_defers_delivery(self):
        s = dispatched()
        close = event("set_route_access", tick=3, route_id="alpha_beta_corridor",
                      open=False, legal_access=False, policy_ref="blockade_event_001")
        s = le.apply_event(s, close)
        prior = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, "delivery held"):
            le.apply_event(s, event("deliver", tick=5, shipment_id="manifest_001"))
        self.assertEqual(s, prior)
        self.assertIn("manifest_001", s["shipments"])
        reopen = event("set_route_access", event_id="test-route-reopen", tick=6, route_id="alpha_beta_corridor",
                       open=True, legal_access=True, policy_ref="border_permission_002")
        s = le.apply_event(s, reopen)
        s = le.apply_event(s, event("deliver", tick=6, shipment_id="manifest_001"))
        self.assertEqual(s["stores"]["station_warehouse"]["stock"]["spare"], 2)

    def test_16_route_vessel_capacity_and_origin(self):
        s = produced()
        e = event("dispatch", tick=2, operator_ref="freight_company",
                  agreement_ref="contract_001", from_store="colony_depot",
                  to_store="station_warehouse", route_id="alpha_beta_corridor",
                  vessel_id="freighter_001", shipment_id="manifest_001",
                  item="spare", quantity=6)
        with self.assertRaisesRegex(ValueError, "capacity"):
            le.apply_event(s, e)
        e["quantity"] = 2
        e["vessel_id"] = "imaginary_freighter"
        with self.assertRaisesRegex(ValueError, "unknown vessel"):
            le.apply_event(s, e)
        e["vessel_id"] = "freighter_001"
        e["from_store"] = "colony_customer"
        with self.assertRaisesRegex(ValueError, "route does not connect|insufficient stock"):
            le.apply_event(s, e)

    def test_17_trade_latinum_only_with_explicit_unit_and_balances(self):
        s = le.apply_event(initial(), event("trade", seller_store="colony_merchant",
                                            buyer_store="colony_customer", item="ration",
                                            quantity=2, seller_acceptance_ref="sale_offer",
                                            buyer_acceptance_ref="sale_accepted",
                                            consideration={"mode": "latinum", "unit": "latinum_strip",
                                                           "amount": 7, "buyer_wallet": "customer_wallet",
                                                           "seller_wallet": "merchant_wallet"}))
        self.assertEqual(s["wallets"]["customer_wallet"]["balance"], 13)
        self.assertEqual(s["wallets"]["merchant_wallet"]["balance"], 9)
        self.assertEqual(s["stores"]["colony_customer"]["stock"]["ration"], 2)
        self.assertEqual(s["stores"]["colony_merchant"]["stock"]["ration"], 2)

    def test_18_wallet_mismatch_and_insufficient_funds_rejected(self):
        e = event("trade", seller_store="colony_merchant", buyer_store="colony_customer",
                  item="ration", quantity=1, seller_acceptance_ref="signed",
                  buyer_acceptance_ref="signed", consideration={"mode": "latinum", "unit": "latinum_strip",
                  "amount": 100, "buyer_wallet": "customer_wallet", "seller_wallet": "merchant_wallet"})
        with self.assertRaisesRegex(ValueError, "insufficient funds"):
            le.apply_event(initial(), e)
        e["consideration"]["amount"] = 1
        e["consideration"]["seller_wallet"] = "other_currency_wallet"
        with self.assertRaisesRegex(ValueError, "accounting unit"):
            le.apply_event(initial(), e)

    def test_19_barter_exchanges_existing_goods_without_magic(self):
        e = event("trade", seller_store="colony_merchant", buyer_store="colony_customer",
                  item="ration", quantity=2, seller_acceptance_ref="offer",
                  buyer_acceptance_ref="acceptance",
                  consideration={"mode": "barter", "item": "ore", "quantity": 2})
        s = le.apply_event(initial(), e)
        self.assertEqual(s["stores"]["colony_merchant"]["stock"]["ore"], 2)
        self.assertEqual(s["stores"]["colony_customer"]["stock"]["ore"], 1)
        self.assertEqual(s["stores"]["colony_customer"]["stock"]["ration"], 2)

    def test_20_service_allocation_and_gift_need_basis(self):
        for mode in ("service", "allocation", "gift"):
            e = event("trade", seller_store="colony_merchant", buyer_store="colony_customer",
                      item="ration", quantity=1, seller_acceptance_ref="offered",
                      buyer_acceptance_ref="accepted", consideration={"mode": mode})
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, "basis"):
                le.apply_event(initial(), e)
            e["consideration"]["basis_ref"] = "verified_contextual_authorization"
            self.assertEqual(le.apply_event(initial(), e)["stores"]["colony_customer"]["stock"]["ration"], 1)

    def test_21_unknown_payment_cannot_be_assumed_free(self):
        e = event("trade", seller_store="colony_merchant", buyer_store="colony_customer",
                  item="ration", quantity=1, seller_acceptance_ref="offered",
                  buyer_acceptance_ref="accepted", consideration={"mode": "UNKNOWN"})
        with self.assertRaisesRegex(ValueError, "unsupported"):
            le.apply_event(initial(), e)

    def test_22_duplicate_event_is_idempotent(self):
        e = event("consume", store_id="colony_depot", item="ration",
                  quantity=1, cause_ref="meal")
        s = le.apply_event(initial(), e)
        self.assertEqual(le.apply_event(s, copy.deepcopy(e)), s)
        self.assertEqual(len(s["event_log"]), 1)

    def test_23_divergent_event_id_never_silently_overwrites_history(self):
        e = event("consume", store_id="colony_depot", item="ration",
                  quantity=1, cause_ref="meal")
        s = le.apply_event(initial(), e)
        e["quantity"] = 2
        with self.assertRaisesRegex(ValueError, "collision"):
            le.apply_event(s, e)

    def test_24_time_regression_rejected(self):
        s = le.apply_event(initial(), event("consume", tick=8, store_id="colony_depot",
                                            item="ration", quantity=1, cause_ref="meal"))
        with self.assertRaisesRegex(ValueError, "time regression"):
            le.apply_event(s, event("consume", event_id="test-consume-second", tick=7, store_id="colony_depot",
                                    item="ration", quantity=1, cause_ref="meal2"))

    def test_25_lod_does_not_change_physics_or_ledger(self):
        f = fixture()
        results = [le.replay(f["initial_state"], f["happy_path_events"], lod=x)
                   for x in ("high", "low", "offscreen")]
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])

    def test_26_forecasts_and_player_presence_do_not_mutate_world(self):
        s = initial()
        before = copy.deepcopy(s)
        v = le.shortage_view(s, {"colony_clinic": {"medkit": 7}})
        self.assertEqual(v[0]["unmet"], 7)
        self.assertEqual(s, before)
        self.assertEqual(le.replay(s, []), le.replay(s, [], lod="offscreen"))

    def test_27_illegal_values_rejected(self):
        s = initial()
        s["stores"]["colony_depot"]["stock"]["ore"] = -1
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            le.validate_state(s)
        s = initial()
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            le.apply_event(s, event("consume", store_id="colony_depot",
                                    item="ration", quantity=-1, cause_ref="meal"))

    def test_28_contract_and_lore_compatibility(self):
        root = ROOT
        p = root / "sistemas/universe/generation/living_economy_reference_contract_v0.1.json"
        contract = json.loads(p.read_text(encoding="utf-8"))
        self.assertTrue(contract["no_runtime_claim"])
        self.assertIn("NO_GLOBAL_EXCHANGE", contract["invariant_ids"])
        for reference in contract["related_contract_refs"]:
            self.assertTrue((root / reference).is_file(), reference)
        for other in ("proyecto/docs/roadmap/lore_04_b/B03_intercambio_latinio.md",
                      "proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md"):
            self.assertTrue((root / other).is_file())

    def test_29_state_malformed_missing_owners_or_vessels(self):
        s = initial()
        del s["stores"]["colony_depot"]["owner_ref"]
        with self.assertRaises((ValueError, KeyError)):
            le.validate_state(s)
        s = initial()
        del s["vessels"]["freighter_001"]
        e = event("dispatch", tick=2, operator_ref="freight_company",
                  agreement_ref="contract", from_store="colony_depot",
                  to_store="station_warehouse", route_id="alpha_beta_corridor",
                  vessel_id="freighter_001", shipment_id="shipment",
                  item="ration", quantity=1)
        with self.assertRaisesRegex(ValueError, "unknown vessel"):
            le.apply_event(s, e)

    def test_30_permit_required_for_every_mutation(self):
        for kind in ("consume", "loss"):
            e = event(kind, store_id="colony_depot", item="ration",
                      quantity=1, cause_ref="event")
            e["authority_ref"] = ""
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "authority"):
                le.apply_event(initial(), e)


if __name__ == "__main__":
    unittest.main()
