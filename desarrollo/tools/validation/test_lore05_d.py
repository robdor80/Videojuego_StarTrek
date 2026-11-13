#!/usr/bin/env python3
import copy
import unittest
from validate_lore05_d import (load, problems_for_data, validate, ENTITY, CASES, SHIPS, CLASSES, PROJECT, FACILITIES, DESIGNS, FACTIONS, REGISTRY)

class TestLore05D(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=[load(x) for x in (ENTITY,CASES,SHIPS,CLASSES,PROJECT,FACILITIES,DESIGNS,FACTIONS,REGISTRY)]
    def mutate(self,fn):
        docs=copy.deepcopy(self.inputs)
        fn(docs)
        self.assertTrue(problems_for_data(*docs))
    @staticmethod
    def ship(d,id_): return next(x for x in d[0]["ships"] if x["ship_id"]==id_)
    @staticmethod
    def facility(d,id_): return next(x for x in d[0]["facilities"] if x["facility_id"]==id_)
    @staticmethod
    def faction(d,id_): return next(x for x in d[0]["factions"] if x["faction_id"]==id_)
    def test_baseline(self): self.assertEqual(validate(),[])
    def test_wrong_start(self): self.mutate(lambda d:d[0].update(campaign_baseline_year=2401))
    def test_runtime_false_claim(self): self.mutate(lambda d:d[0].update(runtime_implemented=True))
    def test_autospawn(self): self.mutate(lambda d:d[0].update(automatic_world_spawns=True))
    def test_missing_ship(self): self.mutate(lambda d:d[0]["ships"].pop())
    def test_renamed_enterprise(self): self.mutate(lambda d:self.ship(d,"uss_enterprise_ncc_1701_d").update(registry="NCC-1701-V"))
    def test_galaxy_not_valhalla(self): self.mutate(lambda d:self.ship(d,"uss_enterprise_ncc_1701_d").update(class_id="valhalla"))
    def test_auto_player_assignment(self): self.mutate(lambda d:self.ship(d,"uss_enterprise_ncc_1701_d").update(auto_assign_to_player=True))
    def test_original_defiant_not_live(self): self.mutate(lambda d:self.ship(d,"uss_defiant_nx_74205").update(documentary_state_2383="ACTIVA"))
    def test_reliant_not_live(self): self.mutate(lambda d:self.ship(d,"uss_reliant_ncc_1864").update(documentary_state_2383="ACTIVA"))
    def test_duplicate_ship_id(self): self.mutate(lambda d:d[0]["ships"].append(copy.deepcopy(d[0]["ships"][0])))
    def test_wrong_source(self): self.mutate(lambda d:d[0]["ships"][0].update(provenance_refs=["NONEXISTENT"]))
    def test_missing_facility(self): self.mutate(lambda d:d[0]["facilities"].pop())
    def test_duplicated_station(self): self.mutate(lambda d:self.facility(d,"canon:facility:deep_space_9").update(auto_generate_duplicate=True))
    def test_no_infinite_resources(self): self.mutate(lambda d:self.facility(d,"canon:facility:spacedock_one").update(automatically_service_player=True))
    def test_facility_owner_unknown(self): self.mutate(lambda d:self.facility(d,"canon:facility:empok_nor").update(owner_current="starfleet"))
    def test_wrong_facility_design(self): self.mutate(lambda d:self.facility(d,"canon:facility:deep_space_9").update(design_ref="starfleet_spacedock_type"))
    def test_historical_base_not_live(self): self.mutate(lambda d:self.facility(d,"canon:facility:starbase_1").update(documentary_state_2383="ACTIVA"))
    def test_faction_not_reassigned(self): self.mutate(lambda d:self.faction(d,"romulan_star_empire").update(display_name_es="Federacion"))
    def test_faction_no_automatic_war(self): self.mutate(lambda d:self.faction(d,"dominion").update(automatic_treaty_or_war=True))
    def test_faction_no_leader_invented(self): self.mutate(lambda d:self.faction(d,"ferengi_alliance").update(active_leadership_current="UNVERIFIED"))
    def test_separate_federation_and_starfleet(self): self.mutate(lambda d:d[0]["institution_profiles"].pop())
    def test_scenario_not_runtime(self): self.mutate(lambda d:d[1].update(simulation_claimed=True))
    def test_missing_case(self): self.mutate(lambda d:d[1]["documentary_cases"].pop())
    def test_wrong_org_reference(self): self.mutate(lambda d:self.faction(d,"bajoran_provisional_government").update(organization_profile_refs=["UNKNOWN"]))
if __name__ == "__main__":
    unittest.main()
