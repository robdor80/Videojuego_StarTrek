#!/usr/bin/env python3
"""H09-P03-C02: contratos/documentos de diseño, no navegación nativa."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
SPEC = DOCS / "H09_P03_C02_CONTRATO_DOMINIO_NAVAL_v1.json"
PLAN = DOCS / "H09_P03_C02_DISENO_DOMINIO_NAVAL_2026-11-27.md"
PROMPT = DOCS / "H09_P03_C02_ENCARGO_CODEX_CLOUD_2026-11-27.md"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class C02DesignContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = read_json(SPEC)
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.prompt = PROMPT.read_text(encoding="utf-8")
        cls.p03 = read_json(DOCS / "H09_P03_CONTRATO_NAVEGACION_CONN_v1.json")
        cls.p01 = read_json(DOCS / "H09_P01_REGISTRO_CONSOLAS_v1.json")

    def test_design_only_never_certifies_runtime(self):
        self.assertEqual(self.s["phase"], "H09-P03-C02")
        self.assertEqual(self.s["contract_kind"], "INTERNAL_DOMAIN_DESIGN_NO_ABI")
        self.assertEqual(self.s["status"], "DESIGNED_NOT_RUNTIME")
        self.assertTrue(all(flag is False for flag in self.s["runtime_flags"].values()))
        self.assertIn("NO IMPLEMENTADO", self.plan)
        self.assertIn("NO movimiento", self.prompt)

    def test_pin_and_c01_merged_baseline(self):
        self.assertEqual(self.s["pin_core_sha"], self.p03["pin_core_sha"])
        self.assertEqual(self.s["c01_pr"], 231)
        self.assertEqual(len(self.s["c01_merged_base"]), 40)
        cmake = (ROOT / "desarrollo/integration/host/CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn(self.s["pin_core_sha"], cmake)

    def test_source_paths_existing_and_internal(self):
        self.assertGreaterEqual(len(self.s["sources"]), 10)
        for key, value in self.s["sources"].items():
            with self.subTest(key=key):
                p = Path(value)
                self.assertFalse(p.is_absolute())
                self.assertNotIn("..", p.parts)
                self.assertTrue((ROOT / p).is_file(), value)

    def test_only_existing_h09_navigation_operation(self):
        p01 = {op["id"]: op for op in self.p01["operations"]}
        self.assertEqual(self.s["scope"]["h09_p01_operation"], "NAVIGATION_ROUTE_PROPOSE")
        self.assertFalse(p01["NAVIGATION_ROUTE_PROPOSE"]["available_in_host_runtime"])
        self.assertFalse(p01["CONN_MANEUVER_ORDER"]["available_in_host_runtime"])
        self.assertFalse(self.p03["flags"]["host_navigation_api_implemented"])
        self.assertFalse(self.p03["flags"]["host_conn_api_implemented"])
        self.assertIn("CONN_MANEUVER_ORDER", self.s["scope"]["out_of_scope"])
        self.assertIn("H09_P04", self.s["scope"]["out_of_scope"])

    def test_authority_unchanged(self):
        a = self.s["authority"]
        self.assertEqual(a["authoritative_location"], "CoreRPG.WorldState")
        self.assertIn("CoreRPG", a["time"])
        self.assertIn("F04", a["persistent_snapshot"])
        self.assertIn("institutional_authority_unchanged", a["f11"])
        self.assertIn("non_authoritative", a["unreal"])

    def test_location_never_inferred_and_legacy_unknown(self):
        e = self.s["entities"]
        self.assertEqual(e["location_absent"], "UNKNOWN_WITH_NULL_REF")
        self.assertIn("NO_SILENT_MIGRATION", e["legacy_save_without_location"])
        self.assertIn("REQUIRES_EXPLICIT", e["bootstrap"])
        self.assertIsNone(e["geometry"]["unknown_z_ly"])
        self.assertIsNone(e["geometry"]["unknown_distance_ly"])
        self.assertIsNone(e["geometry"]["unknown_eta"])
        self.assertFalse(e["geometry"]["wormhole_is_ordinary_warp"])
        self.assertIn("no asignar", self.plan.lower())

    def test_chart_not_implicitly_known_from_reference(self):
        c = self.s["chart"]
        self.assertTrue(c["versioned_publication_required"])
        self.assertTrue(c["observer_scoped_core_knowledge_required"])
        self.assertFalse(c["reference_graph_is_automatically_known"])
        self.assertFalse(c["political_and_sensor_ground_truth_exposed"])
        self.assertTrue(c["hidden_and_missing_destination_indistinguishable_publicly"])
        self.assertTrue((ROOT / c["profiles_source"]).is_file())
        profiles = read_json(ROOT / c["profiles_source"])["preference_profiles"]
        self.assertEqual(set(profiles), set(self.p03["known_route_profiles"]))

    def test_three_readonly_interfaces_and_consistent_fields(self):
        ops = self.s["internal_operations"]
        self.assertEqual([op["id"] for op in ops],
                         ["read_own_location", "read_authorized_chart", "propose_known_route"])
        self.assertTrue(all(not op["mutates"] and not op["runtime_available"] for op in ops))
        self.assertIn("visible_route_legs", ops[2]["returns"])
        self.assertIn("authorized_observer", ops[1]["requires"])
        self.assertIn("owner_thread", ops[0]["requires"])

    def test_proposal_token_never_grants_authority(self):
        tok = self.s["proposal_token"]
        self.assertFalse(tok["authority_token"])
        self.assertFalse(tok["persisted_navigation_state"])
        self.assertFalse(tok["automatically_retried"])
        for field in ("session_generation", "observer_scope", "chart_revision", "knowledge_revision"):
            self.assertIn(field, tok["binding"])
        for event in ("SAVE", "RESTORE", "CLOSE", "AUTHORITY_REVOKED"):
            self.assertIn(event, tok["invalidate_on"])

    def test_pure_proposal_not_motion(self):
        must = self.s["read_only_invariants"]
        self.assertGreaterEqual(len(must), 10)
        self.assertTrue(all(must.values()))
        self.assertIn("F04_MOVE", self.plan)

    def test_failures_are_design_not_new_abi(self):
        statuses = self.s["public_failure_codes_design_only"]
        self.assertIn("SERVICE_UNAVAILABLE", statuses)
        self.assertIn("STALE_CONTEXT", statuses)
        self.assertIn("DESTINATION_UNKNOWN_OR_REDACTED", statuses)
        self.assertEqual(len(statuses), len(set(statuses)))
        self.assertIn("códigos de **diseño**", self.plan)

    def test_gates_explicit_and_stop_on_p0_failure(self):
        gates = self.s["gates"]
        self.assertEqual([g["id"] for g in gates], ["P0", "P1", "P2"])
        self.assertEqual(gates[0]["on_fail"], "STOP_AND_REPORT")
        self.assertTrue(all(not g["may_modify_core"] for g in gates))
        self.assertIn("detener", self.prompt.lower())

    def test_fourteen_cases_are_future_not_run(self):
        cases = self.s["future_native_cases"]
        self.assertEqual([c["id"] for c in cases], [f"CN2-{n:02d}" for n in range(1,15)])
        self.assertTrue(all(c["status"] == "NOT_RUN" for c in cases))
        self.assertEqual({c["gate"] for c in cases}, {"P0","P1","P2"})
        self.assertIn("CN2-01", self.plan)
        self.assertIn("CN2-14", self.plan)
        self.assertEqual(len(self.p03["tests_future"]), 24)
        self.assertTrue(all(c["status"] == "NOT_RUN" for c in self.p03["tests_future"]))

    def test_codex_effort_and_boundaries(self):
        self.assertIn("Sol 6.2", self.prompt)
        self.assertIn("Medium", self.prompt)
        self.assertIn("PR **Draft**", self.prompt)
        self.assertIn("NO modificar CoreRPG", self.prompt)
        self.assertIn("H09-P02", self.prompt)
        self.assertIn("H09-P03-E/F", self.prompt)
        self.assertIn("laboratorios/", self.prompt)

    def test_c01_evidence_is_present_and_documental(self):
        report = (DOCS / "H09_P03_C01_FACTIBILIDAD_CORE_2026-11-27.md").read_text(encoding="utf-8")
        self.assertIn("374/374", report)
        self.assertIn("27/27", report)
        self.assertIn("se detiene por dependencia de dominio", report)
        self.assertIn("PR #231", self.plan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
