#!/usr/bin/env python3
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE_PATH = HERE / "simulate_civilization_evolution.py"
FIXTURES = ROOT / "validation" / "fixtures" / "civilization_evolution"

spec = importlib.util.spec_from_file_location("civevo", MODULE_PATH)
civevo = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = civevo
spec.loader.exec_module(civevo)


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class CivilizationEvolutionTests(unittest.TestCase):
    def run_fixture(self, name):
        fixture = load_fixture(name)
        payload = civevo.simulate(**fixture["input"])
        self.assertEqual(civevo.validate(payload), [])
        return fixture, payload

    def test_deterministic(self):
        fixture = load_fixture("stable_growth_20y_v0.1.json")
        self.assertEqual(civevo.simulate(**fixture["input"]),
                         civevo.simulate(**fixture["input"]))

    def test_stable_growth_fixture(self):
        fixture, payload = self.run_fixture("stable_growth_20y_v0.1.json")
        final, expected = payload["final_state"], fixture["expected"]
        self.assertEqual(final["population"], expected["population"])
        self.assertEqual(final["government_id"], expected["government_id"])
        self.assertEqual(final["technology_band"], expected["technology_band"])
        self.assertEqual(final["capability_maturity"], expected["capability_maturity"])
        self.assertEqual(len(payload["history"]), expected["history_events"])

    def test_government_transition_preserves_civilization(self):
        fixture, payload = self.run_fixture("regime_change_v0.1.json")
        final, expected = payload["final_state"], fixture["expected"]
        self.assertEqual(payload["civilization_id"], fixture["input"]["civilization_id"])
        self.assertEqual(final["government_id"], expected["government_id"])
        self.assertEqual(final["governance_state"], expected["governance_state"])
        event = next(x for x in payload["history"] if x["type"] == "government_transition")
        self.assertTrue(event["civilization_id_preserved"])

    def test_divided_world_relations_stay_scoped(self):
        fixture, payload = self.run_fixture("post_contact_divided_world_5y_v0.1.json")
        expected = fixture["expected"]
        by_party = {x["party_ref"]: x for x in payload["final_state"]["external_relations"]}
        for party in ("federation", "neighboring_polity"):
            for key, value in expected[party].items():
                self.assertEqual(by_party[party][key], value)
        self.assertTrue(all(not x["planetary_binding"] for x in by_party.values()))

    def test_high_tension_does_not_auto_create_war(self):
        fixture = load_fixture("post_contact_divided_world_5y_v0.1.json")
        request = fixture["input"]
        request["years"] = 1
        request["scheduled_events"] = [{
            "year":1, "event_id":"evt:tension_only",
            "cause_refs":["cause:diplomatic_incident"],
            "effects":{"relation_target_ref":"federation","tension_delta":55,"trust_delta":-10}
        }]
        payload = civevo.simulate(**request)
        relation = next(x for x in payload["final_state"]["external_relations"] if x["party_ref"] == "federation")
        self.assertEqual(relation["relation_state"], "hostile")
        self.assertNotEqual(relation["relation_state"], "war")

    def test_block_one_never_advances_technology_band(self):
        fixture = load_fixture("stable_growth_20y_v0.1.json")
        request = fixture["input"]
        request["years"] = 3
        request["initial"]["capability_maturity"] = 99
        request["initial"]["institutional_capacity"] = 100
        payload = civevo.simulate(**request)
        self.assertEqual(payload["final_state"]["technology_band"], "early_warp")
        self.assertTrue(payload["final_state"]["technology_transition_candidate"])

    def test_extinction_requires_and_keeps_cause(self):
        _, payload = self.run_fixture("causal_extinction_v0.1.json")
        self.assertEqual(payload["final_state"]["population"], 0)
        self.assertEqual(payload["final_state"]["civilization_status"], "extinct")
        event = next(x for x in payload["history"] if x["type"] == "civilization_extinction")
        self.assertTrue(event["cause_refs"])

    def test_validator_rejects_uncausal_major_event(self):
        fixture = load_fixture("regime_change_v0.1.json")
        fixture["input"]["scheduled_events"][0]["cause_refs"] = []
        payload = civevo.simulate(**fixture["input"])
        self.assertTrue(any("missing cause_refs" in x for x in civevo.validate(payload)))

    def test_validator_rejects_partial_planetary_binding(self):
        fixture = load_fixture("post_contact_divided_world_5y_v0.1.json")
        fixture["input"]["initial"]["external_relations"][0]["planetary_binding"] = True
        payload = civevo.simulate(**fixture["input"])
        self.assertIn("partial polity relation cannot bind whole planet",
                      civevo.validate(payload))


if __name__ == "__main__":
    unittest.main()
