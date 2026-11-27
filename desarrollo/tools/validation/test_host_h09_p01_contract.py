#!/usr/bin/env python3
"""H09-P01: checks on a *design-only* ship-console contract.

No CoreRPG runtime, F06 detection, F05 order, Unreal or AI is executed.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
REGISTRY = DOCS / "H09_P01_REGISTRO_CONSOLAS_v1.json"
CONTRACT = DOCS / "H09_P01_INVENTARIO_CONTRATO_CONSOLA_v1_2026-11-23.md"
F09_MATRIX = ROOT / "sistemas/gameplay/ship_operations/consoles/f09_reference_matrix_v0.1.json"
H01_REGISTRY = DOCS / "H01_REGISTRO_CONTRATOS_v1.json"
EXPECTED_CASES = [f"H9-{i:02d}" for i in range(1, 19)]


class H09P01ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.contract = CONTRACT.read_text(encoding="utf-8")
        cls.f09 = json.loads(F09_MATRIX.read_text(encoding="utf-8"))
        cls.h01 = json.loads(H01_REGISTRY.read_text(encoding="utf-8"))

    def test_contract_is_design_only(self):
        r = self.registry
        self.assertEqual(r["phase"], "H09-P01")
        self.assertEqual(r["spec_version"], "1.0.0")
        self.assertEqual(r["status"], "DESIGNED_NOT_RUNTIME")
        self.assertEqual(r["contract_kind"], "LOGICAL_NO_NEW_ABI")
        for k in ("runtime_available", "native_core_tests_run", "unreal_tests_run", "certified"):
            self.assertIs(r[k], False, k)
        self.assertIn("NO IMPLEMENTADO EN RUNTIME", self.contract)
        self.assertIn("NO ABI", self.contract)

    def test_16_families_match_f09_exactly(self):
        families = self.registry["console_families"]
        actual = self.f09["families"]
        self.assertEqual(self.f09["family_count"], 16)
        self.assertEqual(len(families), 16)
        self.assertEqual([f["id"] for f in families], [f["id"] for f in actual])
        self.assertTrue(all(f["design_only"] for f in families))
        self.assertTrue(all(f["source_status"] == a["status"] for f, a in zip(families, actual)))

    def test_sources_exist_and_reference_real_contracts(self):
        sources = self.registry["source_paths"]
        for name, rel in sources.items():
            with self.subTest(source=name):
                self.assertFalse(Path(rel).is_absolute())
                self.assertFalse(".." in Path(rel).parts)
                self.assertTrue((ROOT / rel).is_file(), rel)
        self.assertEqual(json.loads((ROOT / sources["f06_request"]).read_text(encoding="utf-8"))["contract_id"], "sensor_scan_request")
        self.assertEqual(json.loads((ROOT / sources["f06_result"]).read_text(encoding="utf-8"))["contract_id"], "sensor_scan_result")
        self.assertEqual(json.loads((ROOT / sources["interconsole"]).read_text(encoding="utf-8"))["contract_id"], "interconsole_data_package")

    def test_h01_envelope_not_invented(self):
        r = self.registry
        self.assertEqual(r["host_contract"], self.h01["spec_version"])
        self.assertEqual(r["request_required"], self.h01["message_required"])
        self.assertEqual(r["authoritative_state"], "CoreRPG")
        self.assertEqual(r["institutional_authority"], "F11_PROJECT")

    def test_legacy_scan_is_not_f06(self):
        r = self.registry["existing_abi_scan"]
        abi = (ROOT / self.registry["source_paths"]["host_abi"]).read_text(encoding="utf-8")
        self.assertRegex(abi, r"\bTREK_HOST_SUBMIT_SCAN\s*=\s*4")
        self.assertIn("TrekHostScan", abi)
        self.assertEqual(r["underlying_domain"], "F04_F05_ORDER")
        self.assertIs(r["is_f06_sensor_scan"], False)
        self.assertIs(r["allowed_as_f06_adapter"], False)
        self.assertIn("no demuestran", self.contract)

    def test_operations_are_proposals_not_fake_endpoints(self):
        r = self.registry
        operations = r["operations"]
        ids = [o["id"] for o in operations]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 13)
        families = {f["id"] for f in r["console_families"]}
        source_keys = set(r["source_paths"])
        for operation in operations:
            with self.subTest(operation=operation["id"]):
                self.assertIn(operation["family"], families)
                self.assertTrue(operation["planned_for"].startswith("H09-P0"))
                self.assertFalse(operation["available_in_host_runtime"])
                self.assertTrue(set(operation["source_keys"]) <= source_keys)
                self.assertIn(f"`{operation['id']}`", self.contract)
        self.assertEqual(r["first_corridor"], ["sensors", "science", "navigation", "conn", "operations"])

    def test_host_cannot_grant_rank_or_hidden_truth(self):
        r = self.registry
        self.assertNotIn("world_state", r["ownership"]["host"])
        self.assertNotIn("institutional_authority", r["ownership"]["host"])
        self.assertEqual(r["ownership"]["ai"], ["optional_verbalization_only"])
        self.assertTrue({"principal", "observer_id", "F04Ref", "ground_truth"} <= set(r["client_untrusted"]))
        self.assertTrue({"ground_truth", "authoritative_entity_id", "entities_in_scope"} <= set(r["forbidden_player_fields"]))
        self.assertEqual(len(r["admission_gates"]), 7)

    def test_no_parallel_world_timer_or_retry(self):
        m = self.registry["mutations"]
        self.assertTrue(m["require_domain_revalidation"])
        self.assertFalse(m["automatic_retry"])
        self.assertFalse(m["ui_ack_is_core_commit"])
        self.assertFalse(m["model_core_tick_locally"])
        self.assertFalse(m["authoritative_world_moved_by_host"])
        self.assertFalse(self.registry["cross_phase"]["h08_events_are_source_of_truth"])
        self.assertTrue(self.registry["cross_phase"]["restoration_invalidates_ux_generation"])

    def test_enterprise_a2_profile_not_overgeneralized(self):
        p = self.registry["enterprise_d_a2"]
        official = json.loads((ROOT / self.registry["source_paths"]["f06_refit"]).read_text(encoding="utf-8"))
        self.assertEqual(p["activation"], official["target"]["activation"])
        self.assertEqual(p["target_latency_ms"], official["immediate_reports"]["feedback_goal_ms_max"])
        self.assertFalse(official["runtime_implemented"])
        self.assertFalse(p["implementation_available"])
        self.assertFalse(p["latency_measured"])
        self.assertFalse(p["global_ship_override"])
        self.assertTrue(p["weapons_without_transponder_when_observable"])
        self.assertTrue(p["identity_must_not_be_fabricated"])

    def test_ui_skins_cannot_change_rules(self):
        r = self.registry["ui"]
        ui = json.loads((ROOT / self.registry["source_paths"]["sensor_ui"]).read_text(encoding="utf-8"))
        self.assertEqual(len(ui["layout"]["logical_panels"]), 3)
        self.assertEqual(r["action_states"], ui["contextual_action_semantics"]["states"])
        self.assertFalse(r["prefill_may_execute"])
        self.assertFalse(r["change_menu_cancels_job"])
        self.assertFalse(r["world_truth_from_ui"])

    def test_acceptance_matrix_present_not_fake_success(self):
        self.assertEqual(self.registry["tests_future"], EXPECTED_CASES)
        cases = re.findall(r"^\|\s*(H9-\d{2})\s*\|", self.contract, re.MULTILINE)
        self.assertEqual(cases, EXPECTED_CASES)
        self.assertIn("18 pruebas son requisitos futuros, no resultados", self.contract)
        self.assertIn("5–10 minutos", self.contract)
        self.assertTrue(self.registry["cross_phase"]["f06_final_runtime_must_be_reconciled_before_h09_p02"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
