"""S11 Astrometría 360° documentary validation. Not a runtime engine test."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
A = ROOT / "sistemas/gameplay/astrometrics"
X = ROOT / "sistemas/gameplay/ship_operations/interconsole"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestS11Astrometrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projection = load(A / "s11_projection_contract_v0.1.json")
        cls.interaction = load(A / "s11_interaction_contract_v0.1.json")
        cls.room = load(A / "s11_enterprise_d_scene_profile_v0.1.json")
        cls.cases = load(A / "s11_acceptance_cases_v0.1.json")
        cls.state = load(A / "s11_status_v0.1.json")
        cls.nav = load(X / "s11_astrometrics_to_navigation_route_proposal_v0.1.json")
        cls.sci = load(X / "s11_astrometrics_to_science_study_v0.1.json")

    def test_author_approved_but_not_runtime(self):
        self.assertTrue(self.state["author_approved"])
        self.assertEqual(self.state["status"], "DESIGN_APPROVED_NOT_RUNTIME")
        self.assertFalse(self.state["ue5_hologram_runtime"])
        self.assertFalse(self.state["host_adapter_runtime"])
        self.assertFalse(self.state["real_ue5_acceptance_passed"])

    def test_unique_valhalla_ship_target(self):
        self.assertEqual(self.projection["target"]["ship_id"], "uss_enterprise_ncc_1701_d")
        self.assertEqual(self.projection["target"]["configuration_id"], "galaxy_refit_a2")
        self.assertTrue(self.projection["target"]["only_if_operational"])

    def test_four_levels_are_hierarchical(self):
        self.assertEqual([v["level"] for v in self.projection["scales"]], [1, 2, 3, 4])
        self.assertEqual([v["id"] for v in self.projection["scales"]],
                         ["GALAXY_QUADRANT", "REGION_SECTOR", "STAR_SYSTEM", "CELESTIAL_OBJECT"])

    def test_data_refers_to_actual_existing_sources(self):
        for path in self.projection["source_contracts"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_authority_separated(self):
        owners = self.projection["owners"]
        self.assertEqual(owners["truth"], "CoreRPG")
        self.assertEqual(owners["route_and_movement"], "Navigation")
        self.assertEqual(owners["authorized_view"], "HOST")
        self.assertEqual(owners["display"], "UE5")

    def test_no_truth_leak_or_fake_z(self):
        rules = self.projection["rules"]
        for v in ("hide_hidden_world_truth", "classification_enforced",
                  "unknown_z_never_default_zero", "unknown_positions_schematic_and_labeled",
                  "historical_not_future_truth", "non_authoritative_hypothesis_labeled"):
            self.assertTrue(rules[v], v)

    def test_sensors_immediate_and_no_grind(self):
        s = self.projection["sensor"]
        self.assertTrue(s["automatic_and_manual"])
        self.assertTrue(s["ordinary_report_immediate_and_complete_if_in_operational_scope"])
        self.assertTrue(s["no_repeated_scan_grind"])
        self.assertTrue(s["no_fake_90s_wait"])
        self.assertTrue(s["rare_exception_requires_world_reason"])

    def test_volumetric_but_not_all_stars(self):
        v = self.projection["render"]
        self.assertTrue(v["volumetric"])
        self.assertTrue(v["instancing"])
        self.assertTrue(v["lod"])
        self.assertTrue(v["streaming"])
        self.assertTrue(v["relative_origin"])
        self.assertTrue(v["not_all_stars_instanced"])
        self.assertTrue(v["targets_not_verified"])

    def test_controls_include_manual_voice_and_padd(self):
        x = self.interaction
        self.assertIn("ROOM_HOLOGRAM_360", x["modes"])
        self.assertIn("PADD_COMPACT", x["modes"])
        self.assertIn("spanish_voice", x["inputs"])
        self.assertIn("gamepad", x["inputs"])
        self.assertTrue(x["rules"]["manual_controls_always_available"])
        self.assertTrue(x["rules"]["voice_offline_fallback"])
        self.assertTrue(x["rules"]["reduced_motion_and_2d_accessibility"])

    def test_comparison_navigation_and_history_actions(self):
        names = {a["id"] for a in self.interaction["commands"]}
        for s in ("COMPARE", "ROTATE_360", "ROUTE_OPTIONS", "SEND_ROUTE_PROPOSAL",
                  "HISTORY", "FORECAST", "OBJECT_INFO"):
            self.assertIn(s, names)

    def test_very_limited_ai_role(self):
        self.assertTrue(self.interaction["rules"]["deterministic_common_commands_without_ai"])
        self.assertTrue(self.interaction["rules"]["never_reveal_classified"])
        self.assertTrue(self.interaction["rules"]["no_client_world_mutation"])

    def test_handoff_can_never_move_ship_directly(self):
        nav = self.nav["invariants"]
        self.assertTrue(nav["astrometrics_may_propose_not_execute"])
        self.assertTrue(nav["propose_does_not_modify_ship_position"])
        self.assertTrue(nav["require_authorized_navigator_and_valid_f11_command"])
        self.assertTrue(nav["route_result_ETA_computed_by_navigation"])
        self.assertTrue(nav["request_idempotent"])

    def test_science_owns_results_and_sources(self):
        sci = self.sci["invariants"]
        self.assertTrue(sci["science_owns_conclusion"])
        self.assertTrue(sci["ship_existing_observations_only"])
        self.assertTrue(sci["scientific_result_has_provenance"])
        self.assertTrue(sci["no_unrevealed_core_truth"])

    def test_room_dimensions_not_invented(self):
        self.assertEqual(self.room["interior"]["deck"], "UNDECIDED_INTERIOR_PHASE")
        self.assertFalse(self.room["runtime_implemented"])
        self.assertFalse(self.room["technical"]["goals_measured"])

    def test_acceptance_cases_pending_runtime(self):
        ids = [c["id"] for c in self.cases["cases"]]
        self.assertEqual(len(ids), 20)
        self.assertEqual(len(set(ids)), 20)
        self.assertEqual(self.cases["status"], "CASES_DEFINED_NOT_EXECUTED")
        self.assertTrue(all(c["runtime_status"] == "PENDING" for c in self.cases["cases"]))
        self.assertFalse(self.cases["real_ue5_tests_passed"])

    def test_decision_and_design_files_exist(self):
        decision = ROOT / "proyecto/docs/decisions/s11_astrometria_360_2026-11-18.md"
        design = A / "S11_ASTROMETRIA_360_DISENO_v1.md"
        for path in (decision, design):
            self.assertTrue(path.is_file(), str(path))
        self.assertIn("DEC-0023", decision.read_text(encoding="utf-8"))
        self.assertIn("APROBADO EN DISEÑO", design.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
