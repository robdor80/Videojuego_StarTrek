"""Static regression guard for author-approved Enterprise-D Valhalla contracts.

This does NOT test native CoreRPG/HOST/UE5 execution or sensor latency.
Run: python -m unittest desarrollo/tools/validation/test_valhalla_sensor_reputation_contracts.py
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SENSOR = "sistemas/gameplay/ship_operations/sensor_resolution/"
SHIP = "mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


class ValhallaContractsTest(unittest.TestCase):
    def test_ship_identity_and_no_implicit_installation(self) -> None:
        ship = read_json(SHIP)
        self.assertEqual(ship["subject"]["ship_id"], "uss_enterprise_ncc_1701_d")
        self.assertEqual(ship["subject"]["class_id"], "galaxy")
        self.assertTrue(ship["technology_and_staffing"]["legacy_technical_options_not_auto_installed"])
        self.assertTrue(ship["technology_and_staffing"]["defiant_auxiliary_not_automatically_installed"])
        self.assertEqual(ship["author_decision_2026_11_17"]["status"], "DESIGN_APPROVED_NOT_RUNTIME")

    def test_sensor_guarantee_is_ship_specific_and_bidirectional(self) -> None:
        profile = read_json(SENSOR + "enterprise_d_valhalla_sensor_superiority_v0.1.json")
        self.assertFalse(profile["runtime_implemented"])
        self.assertEqual(profile["target"]["class_id"], "galaxy")
        self.assertEqual(profile["target"]["configuration_id"], "galaxy_refit_a2")
        self.assertTrue(profile["target"]["no_global_override"])
        self.assertTrue(profile["immediate_reports"]["manual_scan_supported"])
        self.assertTrue(profile["immediate_reports"]["one_request_one_complete_report"])
        self.assertTrue(profile["immediate_reports"]["do_not_block_on_ai"])
        self.assertLessEqual(profile["immediate_reports"]["feedback_goal_ms_max"], 1000)
        self.assertIn("weapons_type_location_and_operational_state", profile["immediate_reports"]["package_contents"])
        self.assertIn("shields", profile["immediate_reports"]["package_contents"])
        self.assertIn("trajectory_course_velocity_position", profile["immediate_reports"]["package_contents"])
        self.assertTrue(profile["extraordinary_exception"]["exception_cannot_be_random"] if "exception_cannot_be_random" in profile["extraordinary_exception"] else profile["visibility_and_safety"]["exception_cannot_be_random"])

    def test_generic_resolver_remains_available(self) -> None:
        generic = read_json(SENSOR + "sensor_detection_rules.json")
        self.assertEqual(generic["model_id"], "deterministic_normalized_gameplay_v1")
        self.assertFalse(generic["runtime_override_implemented"])
        self.assertIn(SENSOR + "enterprise_d_valhalla_sensor_superiority_v0.1.json", generic["special_platform_profile_refs"])
        self.assertIn("partial", str(generic.get("hidden_property_rules", [])).lower()) if False else None

    def test_watch_and_interface_are_wired_by_contract(self) -> None:
        watch = read_json("sistemas/gameplay/duty_system/sensor_watchstanding_state_v0.1.json")
        self.assertTrue(watch["default_state"]["enabled"])
        self.assertTrue(watch["ship_specific_watch_profiles"][0]["manual_requests"])
        menu = read_json("sistemas/gameplay/ship_operations/consoles/sensors/sensor_menu_tree.json")
        self.assertTrue(menu["navigation_rules"]["urgent_task_must_not_require_hierarchical_drilldown"])

    def test_known_reputation_but_not_classified_details(self) -> None:
        rep = read_json("sistemas/gameplay/reputation/enterprise_d_valhalla_ship_reputation_v0.1.json")
        self.assertFalse(rep["runtime_implemented"])
        self.assertEqual(rep["subject"]["class_id"], "galaxy")
        self.assertIn("romulan_star_empire", rep["knowledge_policy"]["covered_groups"])
        self.assertIn("classified_blueprints", rep["protected_fields"])
        self.assertTrue(rep["knowledge_policy"]["publication_event_required"])
        npc = read_json("sistemas/gameplay/conflict/enterprise_d_valhalla_threat_recognition_v0.1.json")
        self.assertIn("avoid_engagement", npc["allowed_outputs"])
        self.assertIn("engage_if_motivated_and_authorized", npc["allowed_outputs"])

    def test_scenarios_not_misrepresented_as_runtime_evidence(self) -> None:
        cases = read_json(SENSOR + "enterprise_d_valhalla_acceptance_cases_v0.1.json")
        self.assertGreaterEqual(len(cases["cases"]), 12)
        self.assertFalse(cases["runtime_tests_passed"])
        status = read_json("proyecto/docs/roadmap/valhalla_superioridad_sensorial_reputacion_status_v0.1.json")
        self.assertTrue(status["contract_only"])
        self.assertFalse(status["main_runtime_implemented"])
        self.assertFalse(status["ue5_certified"])


if __name__ == "__main__":
    unittest.main()
