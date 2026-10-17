#!/usr/bin/env python3
"""Regresiones independientes del validador de profundidad de lore."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).with_name("validate_lore01_depth.py")
spec = importlib.util.spec_from_file_location("lore01_depth", HERE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

class DeepLoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = mod.load_json(mod.ROOT / "sources/source_registry/source_registry.json")
        cls.sources = {r["source_id"]: r for r in reg["sources"]}
        cls.main = mod.load_json(mod.ROOT / "lore/species/evidence/bolian_v0.2.json")
        cls.delta = mod.load_json(mod.ROOT / "lore/species/evidence/ocampan_v0.2.json")

    def test_all_25_documents(self):
        self.assertEqual(mod.validate_repo(), [])

    def test_invalid_citation(self):
        x = copy.deepcopy(self.main)
        mod.ledger_evidence(x)[0]["source_id"] = "INVALID_TNG_FAKE"
        self.assertTrue(mod.validate_dossier(x, "bolian", self.sources))

    def test_fabricated_screen_canon(self):
        x = copy.deepcopy(self.main)
        next(item for item in mod.ledger_evidence(x) if item["source_id"] == "MA_BOLIAN")["authority"] = "SCREEN_CANON"
        self.assertTrue(mod.validate_dossier(x, "bolian", self.sources))

    def test_missing_unknowns(self):
        x = copy.deepcopy(self.main)
        domain = x.get("domains", x.get("knowledge_domains"))
        domain["unknowns"] = []
        self.assertTrue(mod.validate_dossier(x, "bolian", self.sources))

    def test_dlc_leak(self):
        x = copy.deepcopy(self.delta)
        x["content_scope"] = "MAIN_GAME"
        self.assertTrue(mod.validate_dossier(x, "ocampan", self.sources))

    def test_dlc_spawn(self):
        x = copy.deepcopy(self.delta)
        x["main_game_automatic_spawn_allowed"] = True
        self.assertTrue(mod.validate_dossier(x, "ocampan", self.sources))

    def test_duplicates(self):
        x = copy.deepcopy(self.main)
        mod.ledger_evidence(x)[1]["claim_id"] = mod.ledger_evidence(x)[0]["claim_id"]
        self.assertTrue(mod.validate_dossier(x, "bolian", self.sources))

if __name__ == "__main__":
    unittest.main()
