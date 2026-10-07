#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "generate_facility_project.py"
spec = importlib.util.spec_from_file_location("facgen", MODULE_PATH)
facgen = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = facgen
spec.loader.exec_module(facgen)


class FacilityGeneratorTests(unittest.TestCase):
    def base(self, **overrides):
        args = dict(
            campaign_seed="facility_test_campaign",
            need_id="need:communications:001",
            era_id="tng_ds9_voyager",
            campaign_date="2372-01-01",
            operator="starfleet",
            role="communications_relay",
            site_id="site:relay_chain:001",
            site_type="deep_space_relay_node",
            origin_trigger="persistent_world_need",
            need_strength=35,
            strategic_value=30,
            existing_coverage=50,
            expected_need_years=20,
            alternative_sufficiency=30,
            site_advantage=85,
            operator_capacity=90,
            sustainment=85,
            redundancy_need=20,
            allow_major_complex=False,
            allow_controlled_design=False,
            allow_restricted_design=False,
            commit_construction=True,
            elapsed_construction_months=24,
        )
        args.update(overrides)
        return facgen.generate(**args)

    def test_deterministic(self):
        self.assertEqual(self.base(), self.base())

    def test_reference_relay_uses_relay_design(self):
        payload = self.base()
        self.assertEqual(payload["outcome"], "FACILITY_PROJECT")
        self.assertEqual(payload["design"]["design_id"], "starfleet_relay_station_47_type")
        self.assertEqual(payload["causality"]["resolved_scale"], "micro_outpost")
        self.assertEqual(payload["population_target"]["operator_duty_staff"], 2)
        self.assertEqual(payload["project"]["lifecycle_state"], "operational")
        self.assertEqual(facgen.validate(payload), [])

    def test_player_repair_convenience_is_rejected(self):
        payload = self.base(
            need_id="need:player_repair",
            origin_trigger="player_needs_repairs",
        )
        self.assertEqual(payload["outcome"], "NO_PERMANENT_FACILITY")
        self.assertIn("prohibited_origin_trigger:player_needs_repairs", payload["rejection_reasons"])
        self.assertIsNone(payload["facility_id"])

    def test_high_alternative_sufficiency_is_rejected(self):
        payload = self.base(alternative_sufficiency=90)
        self.assertEqual(payload["outcome"], "NO_PERMANENT_FACILITY")
        self.assertIn("lower_cost_alternative_is_sufficient", payload["rejection_reasons"])

    def test_uncommitted_project_has_no_facility_identity(self):
        payload = self.base(commit_construction=False, elapsed_construction_months=0)
        self.assertEqual(payload["outcome"], "FACILITY_PROJECT")
        self.assertIsNone(payload["project"]["facility_id"])
        self.assertEqual(payload["project"]["lifecycle_state"], "authorized")
        self.assertEqual(facgen.validate(payload), [])

    def test_construction_is_not_instant(self):
        payload = self.base(elapsed_construction_months=0)
        self.assertEqual(payload["project"]["lifecycle_state"], "construction")

    def test_same_campaign_same_procedural_design_can_make_distinct_facilities(self):
        common = dict(
            campaign_seed="same_campaign",
            era_id="tng_ds9_voyager",
            campaign_date="2372-01-01",
            operator="ferengi",
            role="trade_cargo_transfer",
            site_type="orbital_trade_node",
            origin_trigger="persistent_world_need",
            need_strength=65,
            strategic_value=45,
            existing_coverage=20,
            expected_need_years=30,
            alternative_sufficiency=20,
            site_advantage=80,
            operator_capacity=85,
            sustainment=85,
            redundancy_need=10,
            allow_major_complex=False,
            allow_controlled_design=False,
            allow_restricted_design=False,
            commit_construction=True,
            elapsed_construction_months=60,
        )
        a = facgen.generate(**common, need_id="trade:001", site_id="site:trade:001")
        b = facgen.generate(**common, need_id="trade:002", site_id="site:trade:002")
        self.assertEqual(a["design"]["design_id"], b["design"]["design_id"])
        self.assertNotEqual(a["project"]["facility_id"], b["project"]["facility_id"])

    def test_major_complex_needs_explicit_authorization(self):
        payload = self.base(
            role="shipyard",
            need_strength=100,
            strategic_value=100,
            existing_coverage=0,
            expected_need_years=50,
            alternative_sufficiency=0,
            site_advantage=100,
            operator_capacity=100,
            sustainment=100,
        )
        self.assertEqual(payload["outcome"], "NO_PERMANENT_FACILITY")
        self.assertIn("major_complex_requires_explicit_high_level_authorization", payload["rejection_reasons"])

    def test_sample_roles_validate(self):
        roles = [
            "communications_relay","sensor_listening_outpost","research_observatory",
            "medical_quarantine","depot_supply","trade_cargo_transfer","orbital_habitat",
            "refinery_processing","repair_drydock","military_outpost","detention_security",
            "diplomatic_administrative","colony_support"
        ]
        for index, role in enumerate(roles):
            payload = self.base(
                need_id=f"need:{role}:{index}",
                site_id=f"site:{role}:{index}",
                role=role,
                need_strength=72,
                strategic_value=60,
                existing_coverage=15,
                expected_need_years=25,
                alternative_sufficiency=15,
                site_advantage=85,
                operator_capacity=90,
                sustainment=90,
                elapsed_construction_months=200,
            )
            self.assertEqual(facgen.validate(payload), [], msg=role)


if __name__ == "__main__":
    unittest.main()
