#!/usr/bin/env python3
"""Regresiones de LORE-01 A sin dependencias externas."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

FILE = Path(__file__).with_name("validate_lore01_tng.py")
spec = importlib.util.spec_from_file_location("lore01_validation", FILE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

class Lore01Tests(unittest.TestCase):
    def setUp(self):
        self.gate = mod.read(mod.ROOT, mod.GATE)

    def test_real_repository_catalogue(self):
        self.assertEqual(mod.validate_repo(), [])

    def test_dlc_cannot_appear_in_main(self):
        x = copy.deepcopy(self.gate)
        x["main_game"]["species_ids_added"].append("kazon")
        self.assertTrue(mod.validate_policy(x))

    def test_no_dlc_default_spawn(self):
        x = copy.deepcopy(self.gate)
        x["delta_dlc"]["default_main_game_spawn_allowed"] = True
        self.assertTrue(mod.validate_policy(x))

    def test_borg_available_without_dlc(self):
        self.assertTrue(self.gate["exceptions"]["borg"]["main_game_allowed"])
        x = copy.deepcopy(self.gate)
        x["exceptions"]["borg"]["main_game_allowed"] = False
        self.assertTrue(mod.validate_policy(x))

    def test_el_aurian_diaspora_main(self):
        self.assertTrue(self.gate["exceptions"]["el_aurian"]["main_game_allowed"])
        x = copy.deepcopy(self.gate)
        x["exceptions"]["el_aurian"]["main_game_allowed"] = False
        self.assertTrue(mod.validate_policy(x))

    def test_portal_not_implemented(self):
        x = copy.deepcopy(self.gate)
        x["delta_dlc"]["planned_travel"]["implementation_status"] = "IMPLEMENTED"
        self.assertTrue(mod.validate_policy(x))

if __name__ == "__main__":
    unittest.main()
