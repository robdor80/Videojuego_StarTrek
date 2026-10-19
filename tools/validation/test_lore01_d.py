#!/usr/bin/env python3
"""Pruebas de regresión documental LORE-01 D."""
import unittest
from validate_lore01_d import validate, load

class DocumentaryDiplomacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=validate()
        cls.rels={r["relation_id"]:r for r in load("lore/diplomacy/relation_evidence_v0.1.json")["relations"]}
        cls.ev={r["event_id"]:r for r in load("lore/diplomacy/historical_events_v0.1.json")["events"]}
        cls.ags=load("lore/diplomacy/agreements_conflicts_v0.1.json")["agreements"]
    def test_coverage(self): self.assertGreaterEqual(self.report["relations"],24)
    def test_historical_density(self): self.assertGreaterEqual(self.report["events"],30)
    def test_federation_klingon_rupture(self):
        self.assertIn("HOSTILE",[a["relation"] for a in self.rels["federation_klingon"]["anchors"]])
    def test_romulan_entry_not_early(self):
        self.assertEqual(self.ev["romulan_enters_war"]["reference_year"],2374)
    def test_breen_entry_not_early(self):
        self.assertEqual(self.ev["breen_enter_war"]["reference_year"],2375)
    def test_bajoran_sovereignty_distinct(self):
        a=self.rels["federation_bajor"]
        self.assertIn("soberanía",a["why"].lower())
    def test_false_tzenkethi_coup(self):
        self.assertEqual(self.ev["tzenkethi_false_coup_report"]["status"],"FALSE_CLAIM_NOT_HISTORICAL_EVENT")
    def test_no_future_treaty_spawns(self):
        self.assertFalse(any(t["automatic_campaign_activation"] for t in self.ags))
    def test_organian_record(self):
        self.assertIn("organian_peace_treaty",{x["treaty_id"] for x in self.ags})
    def test_no_mandatory_canon_events(self):
        self.assertFalse(any(e["is_compulsory_future_script"] for e in self.ev.values()))
    def test_borg_no_dlc_route(self):
        cs=load("lore/diplomacy/player_npc_cases_v0.1.json")["cases"]
        self.assertTrue(all(x["delta_dlc_unlock"] is False for x in cs))
    def test_gorn_stays_unknown_after_tos(self):
        self.assertEqual(len(self.rels["federation_gorn"]["anchors"]),1)
    def test_maquis_not_state(self):
        idx=load("lore/factions/LORE01_B_civilizations_index_v0.1.json")["main_game_entries"]
        self.assertEqual(next(e["classification"] for e in idx if e["civilization_id"]=="maquis"),"NONSTATE_INSURGENCY")
    def test_occupation_not_sovereignty(self):
        gl=load("lore/diplomacy/geopolitical_layers_v0.1.json")["layers"]
        self.assertTrue(all(g["geometry"] is None for g in gl))
    def test_knowledge_requires_observer(self):
        cs=load("lore/diplomacy/player_npc_cases_v0.1.json")["cases"]
        self.assertTrue(all(x["individual_knowledge_required"] for x in cs))

if __name__=="__main__":
    unittest.main(verbosity=2)
