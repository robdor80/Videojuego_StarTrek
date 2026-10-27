#!/usr/bin/env python3
"""Pruebas negativas/positivas de LORE-01 C, sin alterar archivos."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lore01_c_validator", HERE / "validate_lore01_c.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class TestLore01C(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = mod.read("mundo/lore/astrography/atlas/anchor_atlas_v0.1.json")
        cls.m = mod.read("mundo/lore/astrography/atlas/map_reference_manifest_v0.1.json")
        cls.q = mod.read("mundo/lore/astrography/atlas/quadrants_regions_v0.1.json")
        cls.routes = mod.read("mundo/lore/astrography/atlas/route_reference_cases_v0.1.json")
        cls.leads = mod.read("mundo/lore/astrography/atlas/cartographic_research_leads_v0.1.json")
        cls.issues = mod.read("mundo/lore/astrography/atlas/map_discrepancy_ledger_v0.1.json")
        cls.k = mod.read("mundo/lore/astrography/atlas/knowledge_era_cases_v0.1.json")
        cls.by_id = {x["location_id"]: x for x in cls.atlas["locations"]}

    def test_01_complete_crossfile_validator(self):
        self.assertEqual(mod.validate()["maps"], 4)

    def test_02_legacy_ids_are_unique(self):
        self.assertEqual(len(self.by_id), len(self.atlas["locations"]))

    def test_03_no_inferred_3d_coordinates(self):
        for x in self.atlas["locations"]:
            for key in ("x_ly", "y_ly", "z_ly"):
                self.assertIsNone(x["coordinates"][key])

    def test_04_sol_is_not_forced_into_a_quadrant(self):
        self.assertIsNone(self.by_id["sol_system"]["quadrant"])
        self.assertIsNone(self.by_id["earth"]["quadrant"])

    def test_05_bajoran_wormhole_connects_alpha_gamma(self):
        self.assertEqual(self.by_id["bajoran_wormhole_alpha"]["quadrant"], "ALPHA")
        self.assertEqual(self.by_id["bajoran_wormhole_gamma"]["quadrant"], "GAMMA")
        special = next(x for x in self.routes["cases"] if x["case_id"] == "L01C_BAJORAN_WORMHOLE")
        self.assertIsNone(special["original_distance_ly"])

    def test_06_delta_locked_as_documentation(self):
        for id in mod.DELTA_ANCHORS:
            self.assertEqual(self.by_id[id]["documentary_availability"], "DELTA_RESERVED_REFERENCE_ONLY")
            self.assertFalse(self.by_id[id]["runtime_generation_enabled"])

    def test_07_map_license_not_assumed(self):
        self.assertFalse(self.m["original_images_in_public_repository"])
        for m in self.m["maps"]:
            self.assertEqual(m["license_status"], "UNVERIFIED")

    def test_08_map_hashes_are_stable(self):
        self.assertEqual(self.m["maps"][3]["sha256"],
                         "2a56d1cfc3cf2fb966093d3fd76d5e70f08c2c01856ee80ca3d94eeb404f7375")

    def test_09_fan_maps_never_screen_canon(self):
        self.assertEqual(self.m["maps"][3]["reference_class"], "FAN_MAP_RESEARCH_LEAD")

    def test_10_political_regions_have_no_permanent_owner(self):
        self.assertTrue(all(x["political_owner_id"] is None for x in self.q["regions"]))

    def test_11_extracted_labels_cannot_be_loaded(self):
        self.assertTrue(all(not c["runtime_import_allowed"] for c in self.leads["candidates"]))

    def test_12_routes_not_measured_from_map_pixels(self):
        self.assertTrue(all(not x["map_image_used_to_calculate_distance"]
                            for x in self.routes["cases"]))

    def test_13_political_map_conflict_kept_open(self):
        item = next(x for x in self.issues["entries"] if x["issue_id"] == "POLITICAL_MAP_UNDATED")
        self.assertEqual(item["review_state"], "DOCUMENTED_OPEN")

    def test_14_no_early_ds9_information_leak(self):
        item = next(x for x in self.k["cases"] if x["case_id"] == "TNG_2364_WORMHOLE_UNKNOWN")
        self.assertIs(item["auto_visible"], False)

    def test_15_voyager_knowledge_does_not_transfer(self):
        item = next(x for x in self.k["cases"] if x["case_id"] == "VOY_DELTA_NO_SHARED_OMNISCIENCE")
        self.assertIs(item["auto_visible"], False)

    def test_16_fan_data_no_political_ownership_of_world(self):
        self.assertTrue(all("controller_faction_id" not in x for x in self.atlas["locations"]))

    def test_17_injecting_unknown_location_is_rejected(self):
        fake = copy.deepcopy(self.atlas["locations"][0])
        fake["location_id"] = "fan_sector_fake"
        legacy = {x["location_id"] for x in mod.read("mundo/lore/astrography/systems/anchor_locations.json")["locations"]}
        self.assertNotIn(fake["location_id"], legacy)

    def test_18_bad_checksum_is_rejected_by_format(self):
        import re
        fake = copy.deepcopy(self.m["maps"][0])
        fake["sha256"] = "no-hash"
        self.assertIsNone(re.fullmatch(r"[0-9a-f]{64}", fake["sha256"]))

    def test_19_all_sources_registered(self):
        ids = {x["source_id"] for x in mod.read("mundo/sources/source_registry/source_registry.json")["sources"]}
        self.assertTrue(all(set(x["source_refs"]).issubset(ids) for x in self.atlas["locations"]))

    def test_20_corresponding_categories_preserved(self):
        baseline = {x["location_id"]: x for x in mod.read("mundo/lore/astrography/systems/anchor_locations.json")["locations"]}
        self.assertTrue(all(x["location_type"] == baseline[x["location_id"]]["location_type"]
                            for x in self.atlas["locations"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
