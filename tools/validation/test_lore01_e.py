#!/usr/bin/env python3
"""Regresiones documentales cruzadas de LORE-01 E, sin simulación."""
import unittest
from validate_lore01_e import validate, load

class Lore01ECrossLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = validate()
        cls.ops = {r["record_id"]:r for r in load("lore/operations/operational_evidence_v0.1.json")["records"]}
        cls.cases = load("lore/operations/query_scenarios_v0.1.json")["cases"]

    def test_a_and_a1_preserved(self):
        self.assertEqual(self.summary["phase_A_species"],25)
        self.assertEqual(self.summary["phase_A1_guides"],25)

    def test_b_nonstate_classification_preserved(self):
        data=load("lore/factions/LORE01_B_civilizations_index_v0.1.json")["main_game_entries"]
        classified={r["civilization_id"]:r["classification"] for r in data}
        self.assertEqual(classified["maquis"],"NONSTATE_INSURGENCY")
        self.assertEqual(classified["section_31"],"CLANDESTINE_NETWORK")

    def test_c_anchored_not_owned(self):
        data=load("lore/astrography/atlas/anchor_atlas_v0.1.json")
        self.assertEqual(self.summary["phase_C_anchors"],30)
        self.assertTrue(all("political_owner_id" not in r for r in data["locations"]))

    def test_d_event_not_mandatory(self):
        e=load("lore/diplomacy/historical_events_v0.1.json")["events"]
        self.assertTrue(all(not r["is_compulsory_future_script"] for r in e))

    def test_e_complete_domains(self):
        self.assertEqual({v["area"] for v in self.ops.values()},set("ABCDEFGH"))

    def test_romulan_alliance_not_unrestricted(self):
        self.assertIn("no concede",self.ops["OP-B02"]["prohibited_inference"].lower())

    def test_diplomatic_false_information_separated(self):
        self.assertIn("manipulación",self.ops["OP-E04"]["documented_observation"].lower())

    def test_jurisdiction_not_rank(self):
        self.assertIn("rango",self.ops["OP-D01"]["prohibited_inference"].lower())

    def test_first_contact_not_auto(self):
        self.assertIn("automatizar",self.ops["OP-G02"]["prohibited_inference"].lower())

    def test_npc_individuality(self):
        idx=load("lore/cultures/ai_behavior/species_behavior_index_v0.1.json")
        self.assertTrue(idx["no_personality_by_species"])

    def test_delta_future_gate(self):
        p=load("universe/generation/lore01_tng_content_availability_v0.1.json")
        self.assertFalse(p["delta_dlc"]["default_main_game_spawn_allowed"])

    def test_no_world_mutation_from_cases(self):
        self.assertTrue(all("ai_direct_world_mutation" in q["forbidden_outputs"] for q in self.cases))

    def test_no_precise_operational_border(self):
        atlas=load("lore/astrography/atlas/anchor_atlas_v0.1.json")
        self.assertTrue(all(v["coordinates"]["z_ly"] is None for v in atlas["locations"]))

    def test_historical_time_boundaries(self):
        self.assertEqual(self.ops["OP-E04"]["temporal"]["reference_year"],2374)
        self.assertEqual(self.ops["OP-A01"]["temporal"]["not_before_event_id"],"ds9_joint_arrangement")

    def test_sources_persist(self):
        self.assertGreaterEqual(self.summary["phase_D_relations"],27)
        self.assertGreaterEqual(self.summary["open_uncertainties"],15)

if __name__ == "__main__":
    unittest.main(verbosity=2)
