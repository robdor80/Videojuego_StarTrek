#!/usr/bin/env python3
"""H09-P03: comprobaciones de arquitectura DOCUMENTAL y dependencias.

No implementa rutas ni movimiento; no ejecuta CoreRPG, F06, UE5 o Codex.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "proyecto/docs/architecture/host"
SPEC = DOCS / "H09_P03_CONTRATO_NAVEGACION_CONN_v1.json"
PLAN = DOCS / "H09_P03_AUDITORIA_ARQUITECTURA_PLAN_2026-11-27.md"
P01 = DOCS / "H09_P01_REGISTRO_CONSOLAS_v1.json"
H01 = DOCS / "H01_REGISTRO_CONTRATOS_v1.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class H09P03ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load(SPEC)
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.p01 = load(P01)
        cls.h01 = load(H01)
        cls.sources = cls.spec["source_paths"]

    def source(self, key):
        return ROOT / self.sources[key]

    def test_documented_not_runtime(self):
        s = self.spec
        self.assertEqual(s["phase"], "H09-P03")
        self.assertEqual(s["spec_version"], "1.0.0")
        self.assertEqual(s["status"], "DESIGNED_NOT_RUNTIME")
        self.assertEqual(s["contract_kind"], "LOGICAL_NO_NEW_ABI")
        self.assertEqual(s["authority"], "CoreRPG")
        self.assertEqual(s["institutional_authority"], "F11_PROJECT")
        self.assertTrue(all(value is False for value in s["flags"].values()))
        self.assertIn("no implementado", self.plan.lower())
        self.assertIn("no inicia H09-P04", self.plan)

    def test_sources_all_exist_and_are_repo_relative(self):
        self.assertGreaterEqual(len(self.sources), 25)
        for name, path in self.sources.items():
            with self.subTest(name=name):
                self.assertFalse(Path(path).is_absolute(), path)
                self.assertNotIn("..", Path(path).parts, path)
                self.assertTrue((ROOT / path).is_file(), path)

    def test_core_pin_is_fixed_and_not_claimed_audited(self):
        cmake = self.source("host_cmake").read_text(encoding="utf-8")
        self.assertIn(self.spec["pin_core_sha"], cmake)
        self.assertRegex(cmake, r'host_core_sha\s+"[0-9a-f]{40}"')
        self.assertIn("se ha extendido directamente al repositorio preexistente", self.plan)
        self.assertFalse(self.spec["flags"]["core_ship_motion_verified"])

    def test_pinned_core_public_api_and_f03_route_boundary(self):
        audit = self.spec["pinned_core_api_audit"]
        self.assertEqual(audit["reference_repo"], "robdor80/CoreRPG")
        self.assertEqual(audit["reference_sha"], self.spec["pin_core_sha"])
        self.assertTrue(audit["public_headers_inspected"])
        self.assertFalse(audit["full_core_implementation_audited"])
        self.assertFalse(audit["published_ship_motion_api"])
        self.assertFalse(audit["published_navigation_solver_api"])
        self.assertEqual(set(audit["action_operation_variants"]), {
            "PlaceEntityAction", "RemoveContainmentAction", "AddRelationAction",
            "RemoveRelationAction", "StreamRollAction"
        })
        for url in audit["sources"]:
            self.assertIn(audit["reference_sha"], url)
            self.assertTrue(url.startswith("https://github.com/robdor80/CoreRPG/blob/"))
        f03 = self.source("f03_fixture").read_text(encoding="utf-8")
        f02 = self.source("f02_fixture").read_text(encoding="utf-8")
        report = self.source("f03_report").read_text(encoding="utf-8")
        self.assertIn("f03_schedule_route", f03)
        self.assertIn("f02_place", f02)
        self.assertIn("no es un modelo de vuelo warp", report)
        self.assertTrue(audit["f03_demo_is_not_nav_engine"])
        self.assertIn("Auditoría adicional del CoreRPG fijado", self.plan)

    def test_h09_p01_contract_operation_names_unchanged(self):
        source_ops = {
            item["id"]: item for item in self.p01["operations"]
            if item["planned_for"] == "H09-P03"
        }
        self.assertEqual(set(source_ops), {
            "NAVIGATION_ROUTE_PROPOSE", "CONN_MANEUVER_ORDER"
        })
        self.assertEqual(set(self.spec["scope"]["h09_p01_operations"]), set(source_ops))
        self.assertEqual(set(o["id"] for o in self.spec["operations"]), set(source_ops))
        for op in self.spec["operations"]:
            self.assertEqual(op["kind"], source_ops[op["id"]]["kind"])
            self.assertEqual(op["family"], source_ops[op["id"]]["family"])
            self.assertFalse(op["available_in_host_runtime"])
            self.assertFalse(source_ops[op["id"]]["available_in_host_runtime"])

    def test_h01_envelope_matches_without_new_abi(self):
        self.assertEqual(self.spec["host_contract"], self.h01["spec_version"])
        self.assertEqual(self.spec["message_required"], self.h01["message_required"])
        self.assertNotIn("principal", self.spec["ui_intent_allowed"])
        self.assertTrue({"principal","observer_id","ground_truth","F04Ref"}
                        <= set(self.spec["client_untrusted"]))

    def test_f04_helm_is_not_ship_motion(self):
        f04 = self.source("f04").read_text(encoding="utf-8")
        for symbol in ("F04_ST_HELM", "F04_Q_HELM", "F04_Q_ASTROMETRY", "F04_MOVE"):
            self.assertIn(symbol, f04)
        self.assertIn("no acredita mover una nave espacial", self.plan)
        self.assertFalse(self.spec["flags"]["core_ship_motion_verified"])

    def test_f05_only_supports_f04_scan_on_inspected_boundary(self):
        f05 = self.source("f05").read_text(encoding="utf-8")
        self.assertRegex(f05, r"P01 supports F04_SCAN only, no parameters")
        self.assertIn("f05_submit", f05)
        self.assertIn("f05_execute_order", f05)
        gateway = self.source("host_gateway").read_text(encoding="utf-8")
        self.assertIn("GatewayOp", gateway)
        self.assertNotIn("NAVIGATION_ROUTE_PROPOSE", gateway)
        self.assertNotIn("CONN_MANEUVER_ORDER", gateway)

    def test_known_navigation_intents_reused(self):
        nav = load(self.source("nav_order"))
        self.assertEqual(set(self.spec["reference_intents"]),
                         set(nav["supported_intents"]))
        self.assertEqual(self.spec["operations"][0]["nav_intent_reference"], "set_course")
        self.assertEqual(self.spec["operations"][1]["nav_intent_reference"], "engage_warp")
        self.assertIn("navigation_validation", nav["natural_language_pipeline"])

    def test_route_profiles_reuse_existing_catalogue(self):
        profiles = set(load(self.source("route_cost"))["preference_profiles"])
        handoff = load(self.source("s11_handoff"))
        self.assertEqual(set(self.spec["known_route_profiles"]), profiles)
        self.assertEqual(set(handoff["profiles"]), profiles)
        self.assertFalse(handoff["runtime_implemented"])
        self.assertTrue(handoff["invariants"]["propose_does_not_modify_ship_position"])

    def test_two_console_families_and_handoff(self):
        m = load(self.source("f09"))
        fam = {f["id"]: f for f in m["families"]}
        self.assertEqual(m["family_count"], 16)
        self.assertEqual(self.spec["scope"]["console_families"], ["navigation", "conn"])
        self.assertTrue({"navigation", "conn"} <= set(fam))
        self.assertIn("conn", fam["navigation"]["allowed_data_handoff_targets"])
        self.assertIn("navigation", fam["conn"]["allowed_data_handoff_targets"])
        self.assertEqual(fam["navigation"]["status"], "design_reference")
        self.assertEqual(fam["conn"]["status"], "design_reference")
        self.assertEqual(load(self.source("interconsole"))["contract_id"],
                         "interconsole_data_package")
        self.assertTrue(self.spec["handoff"]["legacy_conn_navigation_must_disambiguate"])
        self.assertTrue(self.spec["handoff"]["never_auto_executes"])

    def test_unknown_geometry_and_eta_are_not_invented(self):
        astro = load(self.source("astrolocation"))
        self.assertIsNone(astro["fields"]["coordinates"]["z_ly"])
        self.assertTrue(any("Z coordinates" in rule for rule in astro["rules"]))
        self.assertIn("current_position", load(self.source("nav_state"))["fields"])
        self.assertIn("current_location", load(self.source("ship_state"))["live_fields"])
        rules = self.spec["route_constraints"]
        for k in ("unknown_coordinate_z_zero_default",
                  "unknown_distance_sets_eta_zero",
                  "compute_warp_from_universal_formula",
                  "route_proposal_moves_ship",
                  "handoff_executes_motion",
                  "ue_world_position_authoritative",
                  "h08_clock_assumes_ship_movement",
                  "restore_reuses_old_generation_receipt"):
            with self.subTest(invariant=k):
                self.assertFalse(rules[k])
        self.assertTrue(rules["no_automatic_retry"])
        self.assertIn("distance_ly", load(self.source("route_edge"))["fields"])
        self.assertIn("warp_time_calculation",
                      load(self.source("route_edge"))["allowed_derivation_types"])

    def test_h08_clock_is_not_navigation(self):
        h08 = self.source("h08_clock").read_text(encoding="utf-8")
        self.assertIn("f04_advance", h08)
        self.assertIn("ADVANCE", self.plan.upper())
        self.assertFalse(self.spec["route_constraints"]["h08_clock_assumes_ship_movement"])
        self.assertTrue(self.spec["route_constraints"]["core_revision_checked_at_commit"])
        self.assertTrue(self.spec["route_constraints"]["command_permissions_rechecked_at_execute"])

    def test_future_acceptance_cases_partition_gates(self):
        cases = self.spec["tests_future"]
        self.assertEqual(len(cases), 24)
        self.assertEqual([c["id"] for c in cases], [f"N3-{n:02d}" for n in range(1,25)])
        self.assertEqual([c["gate"] for c in cases[:17]], ["INDEPENDENT_F06"]*17)
        self.assertEqual([c["gate"] for c in cases[17:]], ["F06_GATE"]*7)
        self.assertTrue(all(c["status"] == "NOT_RUN" for c in cases))
        self.assertIn("N3-01", self.plan)
        self.assertIn("N3-24", self.plan)
        self.assertFalse(self.spec["flags"]["f06_accepted"])
        self.assertFalse(self.spec["flags"]["h09_p02_unblocked"])

    def test_phase_order_roles_and_no_h09_p04(self):
        phases = self.spec["sequence"]
        self.assertEqual([p["id"] for p in phases],
                         [f"P03-{ch}" for ch in "ABCDEFG"])
        self.assertEqual([p["owner"] for p in phases[:2]], ["ChatGPT"]*2)
        self.assertEqual(phases[2]["owner"], "CodexCloud")
        self.assertEqual(phases[2]["model"], "Sol 6.2")
        self.assertEqual(phases[2]["effort"], "Medium")
        for p in phases:
            self.assertIn(p["id"], self.plan)
        self.assertFalse(self.spec["flags"]["h09_p04_started"])
        self.assertTrue(set(self.spec["f06_gated_capabilities"]))
        self.assertTrue(set(self.spec["core_motion_gated_capabilities"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
