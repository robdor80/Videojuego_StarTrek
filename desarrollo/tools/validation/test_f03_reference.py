#!/usr/bin/env python3
"""Pruebas herméticas del validador de fixture F03. NO ejercitan World State Core."""
from __future__ import annotations
import copy
import json
import unittest

from validate_f03_reference import (FIXTURE, EVENTS, ContractError,
                                    load_json, validate_reference, validate_sources)

class F03ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.data = load_json(FIXTURE)
        self.events = load_json(EVENTS)

    def reject(self, modify):
        candidate = copy.deepcopy(self.data)
        modify(candidate)
        with self.assertRaises(ContractError):
            validate_reference(candidate)

    def test_01_valid_reference(self):
        self.assertEqual(validate_reference(self.data)["entities"], 2)

    def test_02_canonical_json_roundtrip_only(self):
        original = json.dumps(self.data, ensure_ascii=False, sort_keys=True)
        roundtrip = json.loads(original)
        self.assertEqual(original, json.dumps(roundtrip, ensure_ascii=False, sort_keys=True))
        self.assertEqual(validate_reference(roundtrip), validate_reference(self.data))

    def test_03_duplicate_entity_blocked(self):
        self.reject(lambda d: d["materialized_entities"].append(copy.deepcopy(d["materialized_entities"][0])))

    def test_04_new_entity_after_observation_blocked(self):
        self.reject(lambda d: d["materialized_entities"][0].update(materialized_at="2372-03-14T10:43:00"))

    def test_05_duplicate_slot_blocked(self):
        self.reject(lambda d: d["population"]["slots"][1].update(slot_id="ship_alpha_role_01"))

    def test_06_population_inflation_blocked(self):
        self.reject(lambda d: d["population"].update(total_slots=99))

    def test_07_promotion_without_slot_identity_blocked(self):
        self.reject(lambda d: d["population"]["slots"][2].update(tier="B"))

    def test_08_player_truth_leak_blocked(self):
        self.reject(lambda d: d["observer_projections"][0]["observed"].update(
            ground_truth={"classified": "secret"}))

    def test_09_player_entity_id_leak_nested_blocked(self):
        self.reject(lambda d: d["observer_projections"][0]["observed"].update(
            debug={"entity_id": "vessel_beta_001"}))

    def test_10_premature_classification_blocked(self):
        self.reject(lambda d: d["observer_projections"][1]["observed"].update(
            classification="Science vessel"))

    def test_11_premature_properties_blocked(self):
        self.reject(lambda d: d["observer_projections"][1]["observed"].update(
            properties={"secrets": "classified"}))

    def test_12_hidden_property_without_evidence_blocked(self):
        self.reject(lambda d: d["observer_projections"][0]["observed"].update(
            resolved_hidden_properties={"mission": "secret"}))

    def test_13_unknown_truth_entity_blocked(self):
        self.reject(lambda d: d["projection_links_private"][0].update(entity_id="absent"))

    def test_14_missing_observer_mapping_blocked(self):
        self.reject(lambda d: d["projection_links_private"].pop())

    def test_15_duplicate_contact_per_observer_blocked(self):
        self.reject(lambda d: d["observer_projections"].append(
            copy.deepcopy(d["observer_projections"][0])))

    def test_16_invalid_confidence_blocked(self):
        self.reject(lambda d: d["observer_projections"][1].update(confidence=1.1))

    def test_17_future_observation_blocked(self):
        self.reject(lambda d: d["observer_projections"][0].update(
            acquired_at="2372-03-14T11:00:00"))

    def test_18_wrong_causal_parent_blocked(self):
        events = copy.deepcopy(self.events)
        events["events"][1]["causal_refs"] = ["evt_from_the_future"]
        with self.assertRaises(ContractError):
            validate_reference(self.data, events)

    def test_19_event_order_regression_blocked(self):
        events = copy.deepcopy(self.events)
        events["events"][1]["occurred_at"] = "2372-03-14T10:39:00"
        with self.assertRaises(ContractError):
            validate_reference(self.data, events)

    def test_20_duplicate_idempotency_key_blocked(self):
        self.reject(lambda d: d["operational_state"]["orders"][1].update(
            idempotency_key="idempotent_scan_op_7781"))

    def test_21_completed_order_without_result_blocked(self):
        self.reject(lambda d: d["operational_state"]["orders"][0].update(result_id=None))

    def test_22_overlapping_exclusive_shifts_blocked(self):
        self.reject(lambda d: d["operational_state"]["exclusive_assignments"].append({
            "character_id": "player_001", "start": "2372-03-14T10:45:00",
            "end": "2372-03-14T11:10:00", "station_id": "sickbay"}))

    def test_23_foreign_contact_in_knowledge_blocked(self):
        self.reject(lambda d: d["operational_state"]["knowledge_state"][1].update(
            contact_refs=["alpha_contact_04"]))

    def test_24_future_schema_is_rejected_without_mutating_original(self):
        original = copy.deepcopy(self.data)
        self.reject(lambda d: d.update(schema_version="99.0"))
        self.assertEqual(self.data, original)

    def test_25_clock_cannot_reverse(self):
        self.reject(lambda d: d["campaign"].update(timeline_cursor="2372-03-14T10:41:00"))

    def test_26_13_original_invariants_and_source_contracts(self):
        self.assertEqual(validate_sources()["sensor_invariants"], 13)

if __name__ == "__main__":
    unittest.main()
