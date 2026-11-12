#!/usr/bin/env python3
"""Pruebas positivas y mutaciones negativas de LORE-05A; solo referencia."""
import copy
import json
import unittest
from pathlib import Path
from validate_lore05_a import ROOT, IDENTITY, SOURCE_SHIPS, SOURCE_CLASSES, problems_for_data, validate

class Lore05ATest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads((ROOT / IDENTITY).read_text(encoding="utf-8"))
        cls.ships = json.loads((ROOT / SOURCE_SHIPS).read_text(encoding="utf-8"))
        cls.classes = json.loads((ROOT / SOURCE_CLASSES).read_text(encoding="utf-8"))

    def altered(self, location, key, value):
        doc = copy.deepcopy(self.original)
        doc[location][key] = value
        return problems_for_data(doc, self.ships, self.classes)

    def test_baseline_documentary(self):
        self.assertEqual(validate(), [])
        self.assertEqual(problems_for_data(self.original, self.ships, self.classes), [])

    def test_reject_class_valhalla(self):
        self.assertTrue(self.altered("subject", "class_id", "valhalla"))

    def test_reject_renaming(self):
        self.assertTrue(self.altered("subject", "ship_is_renamed", True))

    def test_reject_automatic_captaincy(self):
        self.assertTrue(self.altered("academy", "captaincy_automatic", True))

    def test_reject_automatically_finished_ship(self):
        self.assertTrue(self.altered("future", "readiness_2387_guaranteed", True))

    def test_reject_donor_syracuse_2387(self):
        self.assertTrue(self.altered("future", "syracuse_donor_required_in_2387", True))

    def test_reject_auto_quantum(self):
        self.assertTrue(self.altered("quantum_slipstream", "installed_on_enterprise_d_by_default", True))

    def test_reject_2401_mandatory(self):
        doc = copy.deepcopy(self.original)
        doc["chronology"][-1]["campaign_initialization"] = "AUTO_APPLY"
        self.assertTrue(problems_for_data(doc, self.ships, self.classes))

    def test_reject_2387_canon(self):
        doc = copy.deepcopy(self.original)
        doc["chronology"][-2]["provenance"] = "SCREEN_CANON"
        self.assertTrue(problems_for_data(doc, self.ships, self.classes))

    def test_reject_non_core_authority(self):
        doc = copy.deepcopy(self.original)
        doc["authoritative_world_state"] = "AI_NARRATOR"
        self.assertTrue(problems_for_data(doc, self.ships, self.classes))

    def test_reject_missing_legacy_class(self):
        cls = copy.deepcopy(self.classes)
        cls["classes"] = [c for c in cls["classes"] if c["class_id"] != "valhalla"]
        self.assertTrue(problems_for_data(self.original, self.ships, cls))

if __name__ == "__main__":
    unittest.main()
