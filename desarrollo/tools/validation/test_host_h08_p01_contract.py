#!/usr/bin/env python3
"""H08-P01 static contract checks. No native event bus, Core or Unreal invoked."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
REGISTRY_PATH = DOCS / "H08_P01_REGISTRO_EVENTOS_v1.json"
CONTRACT_PATH = DOCS / "H08_P01_CONTRATO_EVENTOS_SERVICIOS_v1_2026-11-23.md"
H01_PATH = DOCS / "H01_REGISTRO_CONTRATOS_v1.json"
HEADERS = {
    "F04": ROOT / "desarrollo/integration/f04/include/f04_bridge.h",
    "F05": ROOT / "desarrollo/integration/f05/include/f05_orders.h",
    "F11": ROOT / "desarrollo/integration/f11_host/include/f11_host_reader.h",
}
EXPECTED_CASES = [f"HE-{i:02d}" for i in range(1, 17)]


class H08P01ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.contract = CONTRACT_PATH.read_text(encoding="utf-8")
        cls.h01 = json.loads(H01_PATH.read_text(encoding="utf-8"))
        cls.headers = {k: v.read_text(encoding="utf-8") for k, v in HEADERS.items()}

    def test_documented_not_implemented(self):
        r = self.registry
        self.assertEqual(r["spec_version"], "1.0.0")
        self.assertEqual(r["status"], "DESIGNED_NOT_RUNTIME")
        self.assertFalse(r["runtime_available"])
        self.assertFalse(r["native_tests_run"])
        self.assertFalse(r["unreal_tests_run"])
        self.assertFalse(r["certified"])
        self.assertIn("NO IMPLEMENTADO", self.contract)
        self.assertIn("H08-P02", self.contract)
        self.assertIn("H08-P03", self.contract)
        self.assertIn("H08-P04", self.contract)

    def test_h01_subscription_remains_logical(self):
        r = self.registry
        h01_ops = {op["name"]: op for op in self.h01["operations"]}
        self.assertEqual(r["host_contract"], self.h01["spec_version"])
        self.assertEqual(r["operation"], "SUBSCRIBE_EVENTS")
        self.assertIn("SUBSCRIBE_EVENTS", h01_ops)
        self.assertIsNone(h01_ops["SUBSCRIBE_EVENTS"]["existing_api"])
        self.assertEqual(r["message_envelope_required"], self.h01["message_required"])
        service = next(s for s in r["service_catalog"] if s["name"] == "SUBSCRIBE_EVENTS")
        self.assertIsNone(service["existing_api"])
        self.assertEqual(service["status"], "NOT_IMPLEMENTED")

    def test_ownership_no_parallel_world_or_issuer(self):
        r = self.registry
        self.assertEqual(r["authoritative_state"], "CoreRPG")
        self.assertNotEqual(r["institutional_authority"], "HOST")
        self.assertEqual(r["ownership"]["core"], ["world_state", "clock", "timeline", "knowledge", "persistence"])
        self.assertNotIn("issuer", r["ownership"]["host"])
        self.assertFalse(r["delivery"]["mutates_core"])
        self.assertNotIn("f11_trial_host", REGISTRY_PATH.read_text(encoding="utf-8").lower())
        self.assertNotIn("TrekF11TrialHost", self.contract)

    def test_real_source_reader_symbols(self):
        expected = {
            "F04": {"f04_history_page", "f04_history_relations", "f04_stats", "f04_advance"},
            "F05": {"f05_events_page", "f05_order"},
            "F11": {"promotion"},
        }
        for owner, names in expected.items():
            for symbol in names:
                with self.subTest(owner=owner, symbol=symbol):
                    self.assertRegex(self.headers[owner], r"\b" + re.escape(symbol) + r"\s*\(")
        sources = {s["name"] for s in self.registry["source_types"]}
        self.assertEqual(sources, {"F04_FACT", "F05_ORDER", "F11_PROMOTION"})
        for source in self.registry["source_types"]:
            self.assertTrue(source["observer_filtered"])
            self.assertTrue(source["confirmed_only"])

    def test_source_ids_are_grounded(self):
        self.assertEqual(
            {s["event_id_field"] for s in self.registry["source_types"]},
            {"F04HistoryFact.id", "F05EventView.id", "Promotion.promotion_event"},
        )
        for symbol in ("F04HistoryFact", "F05EventView", "promotion_event"):
            joined = "\n".join(self.headers.values())
            self.assertIn(symbol, joined)

    def test_dedup_identifiers_and_replay(self):
        r = self.registry
        self.assertEqual(
            r["stable_fact_identity"], ["campaign_id", "source", "source_event_id", "kind"]
        )
        self.assertEqual(r["projection_identity"][-1], "resolved_observer_identity")
        self.assertTrue({"session_generation", "correlation_id", "core_revision", "page_offset"}.issubset(
            r["forbidden_dedup_identity"]
        ))
        self.assertTrue(set(r["stable_fact_identity"]).isdisjoint(r["forbidden_dedup_identity"]))
        self.assertEqual(r["delivery"]["semantics"], "AT_LEAST_ONCE")
        self.assertEqual(r["delivery"]["missing_history"], "RESYNC_REQUIRED")

    def test_privacy_and_fail_closed(self):
        p = self.registry["observer_policy"]
        self.assertTrue(p["resolved_by_host"])
        self.assertFalse(p["client_selects_observer"])
        self.assertTrue(p["filter_before_queue"])
        self.assertTrue(p["domain_filter_required"])
        self.assertFalse(p["raw_facts_public"])
        self.assertEqual(p["wrong_observer_output"], "EMPTY")
        self.assertIn("ACCESS_DENIED", self.registry["normalized_errors"])
        self.assertIn("SERVICE_UNAVAILABLE", self.registry["normalized_errors"])

    def test_causality_not_artificial_global_order(self):
        p = self.registry["ordering"]
        self.assertTrue(p["source_order_must_hold"])
        self.assertFalse(p["foreign_sources_total_order"])
        self.assertTrue(p["causal_link_must_be_proven"])
        self.assertTrue(p["display_sort_is_not_authority"])
        self.assertIn("F05EventView.previous", self.contract)

    def test_core_clock_and_no_auto_mutation_retry(self):
        clock = self.registry["clock"]
        self.assertEqual(clock["authoritative"], "CoreRPG")
        self.assertEqual(clock["source"], "f04_stats")
        self.assertEqual(clock["advance_api"], "f04_advance")
        self.assertEqual(clock["advance_only_in"], "H08-P03")
        self.assertFalse(clock["automatic_retry_mutations"])
        self.assertTrue(clock["separate_realtime_clock"])

    def test_generation_and_ack_guards(self):
        life = self.registry["lifecycle"]
        self.assertEqual(life["allowed_state"], "ACTIVE")
        self.assertTrue({"SAVING", "LOADING", "CLOSING", "CLOSED"}.issubset(life["blocked_states"]))
        self.assertEqual(life["flush_on"], ["RESTORE", "CLOSE"])
        self.assertTrue(life["generation_fence"])
        self.assertEqual(self.registry["delivery"]["late_generation"], "DROP")
        self.assertEqual(self.registry["delivery"]["ack_effect"], "PRESENTATION_ONLY")
        self.assertFalse(self.registry["delivery"]["ack_persisted"])

    def test_case_matrix_and_pin(self):
        self.assertEqual(self.registry["case_ids"], EXPECTED_CASES)
        rows = re.findall(r"^\|\s*(HE-\d{2})\s*\|", self.contract, flags=re.MULTILINE)
        self.assertEqual(rows, EXPECTED_CASES)
        pin = (ROOT / "desarrollo/integration/f05/core-revision.txt").read_text(encoding="utf-8").strip()
        self.assertEqual(pin, self.h01["candidate_core_pin"])
        self.assertIn(pin, self.contract)


if __name__ == "__main__":
    unittest.main(verbosity=2)
