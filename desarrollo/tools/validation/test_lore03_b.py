#!/usr/bin/env python3
"""Positive and mutation-negative checks for documentary LORE-03B."""
import copy
import unittest
import validate_lore03_b as v

class Lore03BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context = v.reference_context()
        cls.index = v.load(v.INDEX)
        cls.scenarios = v.load(v.SCENARIOS)
        cls.dossiers = {x["conflict_id"]: v.load(x["ref"]) for x in cls.index["dossiers"]}

    def test_all_repository_references(self): self.assertEqual(v.validate()["dossiers"],22)
    def test_12_peaceful_scenarios(self): self.assertEqual(v.validate()["scenarios"],12)
    def test_prior_events_counts(self): self.assertEqual(v.validate()["prior_events"],(40,26))
    def test_coalitions_change(self): self.assertEqual(self.dossiers["dominion_war"]["coalition_membership"],"CHANGES_OVER_TIME")
    def test_borg_incursions_distinct(self): self.assertNotEqual(self.dossiers["borg_wolf359_2366_2367"]["conflict_id"],self.dossiers["borg_sector001_2373"]["conflict_id"])
    def test_bajor_occupation_start_uncertain(self): self.assertIsNone(self.dossiers["cardassian_occupation_bajor"]["start_date_or_range"]["reference_year"])
    def test_romulus_alive_at_2383(self): self.assertIn("Rómulo NO está destruido",self.dossiers["romulan_shinzon_crisis_2379"]["uncertainty_and_canon_limits"])
    def test_delta_actor_not_forged(self): self.assertEqual(self.dossiers["borg_species8472_delta_conflict"]["unregistered_actor_name"],"Species 8472")
    def test_hirogen_not_forged(self): self.assertEqual(self.dossiers["voyager_hirogen_crisis_2374"]["unregistered_actor_name"],"Hirogen")
    def test_no_future_canon_script(self): self.assertTrue(all(x["is_compulsory_future_script"] is False for x in self.dossiers.values()))
    def test_no_runtime_state_changes(self): self.assertTrue(all(x["runtime_state_mutation"] is False for x in self.dossiers.values()))

    def mutation(self,id,key,value):
        bad=copy.deepcopy(self.dossiers[id]);bad[key]=value
        with self.assertRaises(v.InvalidLore03B):v.validate_dossier(bad,self.context)

    def test_reject_gameplay_activation(self): self.mutation("dominion_war","gameplay_activated",True)
    def test_reject_auto_bootstrap_future(self): self.mutation("dominion_war","auto_bootstrap_future",True)
    def test_reject_auto_war(self): self.mutation("dominion_war","auto_start_conflict",True)
    def test_reject_compulsory_canon(self): self.mutation("dominion_war","is_compulsory_future_script",True)
    def test_reject_mutating_world(self): self.mutation("dominion_war","runtime_state_mutation",True)
    def test_reject_noncore_authority(self): self.mutation("dominion_war","world_state_authority","AI")
    def test_reject_missing_faction(self): self.mutation("dominion_war","participant_refs",["fictional_empire"])
    def test_reject_missing_event(self): self.mutation("dominion_war","major_event_refs",["unregistered_event"])
    def test_reject_missing_treaty(self): self.mutation("dominion_war","treaty_refs",["fictional_peace"])
    def test_reject_missing_source(self): self.mutation("dominion_war","source_refs",["MISSING_CANON_SOURCE"])
    def test_reject_fake_exact_date(self): self.mutation("dominion_war","campaign_start_exact_date","2383-01-01")
    def test_reject_empty_causes(self): self.mutation("dominion_war","origin_and_causes","")
    def test_reject_reversed_date(self):
        x=copy.deepcopy(self.dossiers["dominion_war"]);x["start_date_or_range"]["reference_year"]=2387
        with self.assertRaises(v.InvalidLore03B):v.validate_dossier(x,self.context)
    def test_reject_false_coup(self):
        x=copy.deepcopy(self.dossiers);x["tzenkethi_border_provocation_2372"]["asserted_tzenkethi_coup_happened"]=True
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,self.scenarios,x,self.context)
    def test_reject_divided_dominion_war(self):
        x=copy.deepcopy(self.dossiers);x["dominion_war"]["shared_war_events_not_separate_conflicts"]=[]
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,self.scenarios,x,self.context)
    def test_reject_static_coalitions(self):
        x=copy.deepcopy(self.dossiers);x["dominion_war"]["coalition_membership"]="FIXED"
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,self.scenarios,x,self.context)
    def test_reject_scenario_war_trigger(self):
        sc=copy.deepcopy(self.scenarios);sc["scenarios"][0]["automatic_war"]=True
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,sc,self.dossiers,self.context)
    def test_reject_no_diplomacy(self):
        sc=copy.deepcopy(self.scenarios);sc["scenarios"][0]["peaceful_route"]=""
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,sc,self.dossiers,self.context)
    def test_reject_duplicate_scenario(self):
        sc=copy.deepcopy(self.scenarios);sc["scenarios"][1]["seed_id"]=sc["scenarios"][0]["seed_id"]
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,sc,self.dossiers,self.context)
    def test_reject_scenario_runtime(self):
        sc=copy.deepcopy(self.scenarios);sc["new_missions_created"]=True
        with self.assertRaises(v.InvalidLore03B):v.validate_index(self.index,sc,self.dossiers,self.context)
    def test_reject_index_runtime(self):
        ix=copy.deepcopy(self.index);ix["gameplay_activated"]=True
        with self.assertRaises(v.InvalidLore03B):v.validate_index(ix,self.scenarios,self.dossiers,self.context)
    def test_reject_index_status_complete(self):
        ix=copy.deepcopy(self.index);ix["status"]="COMPLETE"
        with self.assertRaises(v.InvalidLore03B):v.validate_index(ix,self.scenarios,self.dossiers,self.context)

if __name__=="__main__":unittest.main(verbosity=2)
