#!/usr/bin/env python3
"""Regresiones negativas y positivas del contrato documental LORE-01 B."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path

P = Path(__file__).with_name("validate_lore01_b.py")
spec = importlib.util.spec_from_file_location("lore01_b_validator", P)
v = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v
spec.loader.exec_module(v)


class Lore01BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        index = v.read_json(v.ROOT / v.INDEX)
        cls.index = index
        cls.row = next(r for r in index["main_game_entries"] if r["civilization_id"] == "klingon_empire")
        cls.data = v.read_json(v.ROOT / cls.row["evidence_ref"])
        cls.md = (v.ROOT / cls.row["monograph_ref"]).read_text(encoding="utf-8")
        registry = v.read_json(v.ROOT / "sources/source_registry/source_registry.json")
        cls.sources = {s["source_id"]: s for s in registry["sources"]}

    def invalid(self, data, md=None):
        return v.validate_entry(self.row, data, self.md if md is None else md, self.sources)

    def test_repository_integrity(self):
        self.assertEqual(v.validate_repo(), [])

    def test_no_ai_core_authority(self):
        data = copy.deepcopy(self.data)
        data["core_mutations_allowed"] = True
        self.assertTrue(self.invalid(data))

    def test_species_is_not_citizenship(self):
        data = copy.deepcopy(self.data)
        data["identity_axes"] = ["species_id"]
        self.assertTrue(self.invalid(data))

    def test_missing_institutional_domain(self):
        data = copy.deepcopy(self.data)
        del data["domains"]["ley_justicia"]
        self.assertTrue(self.invalid(data))

    def test_no_false_screen_provenance(self):
        data = copy.deepcopy(self.data)
        data["evidence"][0]["source_id"] = "ENT_4X22_THESE_ARE_THE_VOYAGES"
        self.assertTrue(self.invalid(data))

    def test_source_must_be_registered(self):
        data = copy.deepcopy(self.data)
        data["evidence"][0]["source_id"] = "UNKNOWN_FICTIONAL_EPISODE"
        self.assertTrue(self.invalid(data))

    def test_no_faked_scene_review(self):
        data = copy.deepcopy(self.data)
        data["verification_status"] = "SCENE_BY_SCENE_VERIFIED"
        self.assertTrue(self.invalid(data))

    def test_future_canon_not_forced(self):
        data = copy.deepcopy(self.data)
        data["chronology"][0]["event_relation"] = "MANDATORY_FUTURE_EVENT"
        self.assertTrue(self.invalid(data))

    def test_chronology_order(self):
        data = copy.deepcopy(self.data)
        data["chronology"][0]["year"] = 2400
        self.assertTrue(self.invalid(data))

    def test_never_backfill_unknowns(self):
        data = copy.deepcopy(self.data)
        data["unknowns"] = []
        self.assertTrue(self.invalid(data))

    def test_borg_not_species(self):
        borg = v.read_json(v.ROOT / "lore/factions/evidence/borg_collective_v0.1.json")
        self.assertEqual(borg["entity_kind"], "red_colectiva_tecnopolitica")
        self.assertTrue(any("biolog" in s.lower() or "especie" in s.lower()
                            for s in borg["domains"].values()))

    def test_legacy_faction_unchanged(self):
        base = v.read_json(v.ROOT / "gameplay/diplomacy/major_faction_catalogue.json")
        self.assertEqual(len(base["factions"]), 8)

    def test_false_coup_is_not_history(self):
        tr = v.read_json(v.ROOT / "lore/factions/evidence/tzenkethi_polity_v0.1.json")
        self.assertIn("falsedad", tr["domains"]["identidad_historia"].lower())

    def test_delta_excluded(self):
        self.assertFalse(set(e["civilization_id"] for e in self.index["main_game_entries"]) & v.DELTA)
        self.assertFalse(self.index["deliberately_not_main_game"][0]["encounter_generation_enabled"])


if __name__ == "__main__":
    unittest.main()
