#!/usr/bin/env python3
import copy
import unittest
from validate_lore05_e import load,problems_for_data,validate,OVERLAY,CASES,SOURCE,LANGMODEL,SUBSPACE

class TestLore05E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs=[load(x) for x in (OVERLAY,CASES,SOURCE,LANGMODEL,SUBSPACE)]
    def mutation(self,fn):
        d=copy.deepcopy(self.docs)
        fn(d)
        self.assertTrue(problems_for_data(*d))
    def test_valid(self): self.assertEqual(validate(),[])
    def test_wrong_year(self): self.mutation(lambda d:d[0].update(campaign_baseline_year=2401))
    def test_duplicate_runtime(self): self.mutation(lambda d:d[0].update(runtime_implemented=True))
    def test_core_boundary(self): self.mutation(lambda d:d[0].update(world_state_authority="HOST"))
    def test_autodiscovery(self): self.mutation(lambda d:d[0].update(automatic_discoveries=True))
    def test_autocontact(self): self.mutation(lambda d:d[0].update(automatic_contact=True))
    def test_autodiplomacy(self): self.mutation(lambda d:d[0].update(automatic_diplomacy=True))
    def test_dlc_unlocked(self): self.mutation(lambda d:d[0].update(automatic_dlc_unlock=True))
    def test_species_created(self): self.mutation(lambda d:d[0].update(canonical_faction_or_civilization_additions=1))
    def test_language_created(self): self.mutation(lambda d:d[0].update(new_playable_language_definitions=1))
    def test_missing_language(self): self.mutation(lambda d:d[0]["existing_languages"].pop())
    def test_language_reroll(self): self.mutation(lambda d:d[0]["existing_languages"][0].update(language_id="synthetic_new"))
    def test_language_fluency(self): self.mutation(lambda d:d[0]["existing_languages"][0].update(auto_assume_fluency=True))
    def test_language_rename(self): self.mutation(lambda d:d[0]["existing_languages"][0].update(display_name_es="IMPROVISADO"))
    def test_dlc_scope(self): self.mutation(lambda d:next(x for x in d[0]["existing_languages"] if x["language_id"]=="talaxian").update(availability_scope="MAIN_GAME"))
    def test_translator_states(self): self.mutation(lambda d:d[0]["translator_states"].append("always_correct"))
    def test_channels(self): self.mutation(lambda d:d[0]["channel_states"].remove("recipient_refused"))
    def test_missing_source(self): self.mutation(lambda d:d[0]["source_contracts"].update(language_runtime="wrong/place.json"))
    def test_incomplete_rule(self): self.mutation(lambda d:d[0]["narrative_rules"][0].update(rule_es="sí"))
    def test_missing_case(self): self.mutation(lambda d:d[1]["documentary_cases"].pop())
    def test_case_mutation(self): self.mutation(lambda d:d[1]["documentary_cases"][0].update(world_state_mutations=True))
    def test_scenario_runtime(self): self.mutation(lambda d:d[1].update(simulation_claimed=True))
    def test_domain_balancing(self): self.mutation(lambda d:d[1]["documentary_cases"][0].update(domain="AUTHORITY"))
    def test_no_empty_expected(self): self.mutation(lambda d:d[1]["documentary_cases"][0].update(expected=""))
if __name__=="__main__":
    unittest.main()
