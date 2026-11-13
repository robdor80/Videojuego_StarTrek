#!/usr/bin/env python3
"""Pruebas adversariales del contrato documental LORE-05C."""
import copy
import unittest
from validate_lore05_c import load, problems_for_data, validate, CATALOGUE, SCENARIOS, ANCHORS, REGISTRY, FACILITIES

class Lore05CTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = [load(CATALOGUE),load(SCENARIOS),load(ANCHORS),load(REGISTRY),load(FACILITIES)]
    def verify(self, change):
        data = copy.deepcopy(self.base)
        change(data)
        self.assertTrue(problems_for_data(*data))
    def test_baseline(self):
        self.assertEqual(validate(),[])
    def test_illegal_coordinate_flag(self):
        self.verify(lambda d: d[0].update(no_new_coordinates=False))
    def test_illegal_routes(self):
        self.verify(lambda d: d[0].update(no_new_routes=False))
    def test_illegal_runtime(self):
        self.verify(lambda d: d[0]["locations"][0].update(world_state_mutations=True))
    def test_missing_anchor(self):
        self.verify(lambda d: d[0]["locations"][0].update(anchor_location_id="planet_uninvented"))
    def test_missing_facility(self):
        self.verify(lambda d: d[0]["locations"][1].update(facility_id="canon:facility:fake"))
    def test_unknown_source(self):
        self.verify(lambda d: d[0]["locations"][0].update(source_refs=["NOT_A_SOURCE"]))
    def test_unregistered_profile(self):
        self.verify(lambda d: d[0]["locations"][0].update(depth_profile_ref="none.json"))
    def test_new_bajor_cannot_be_live(self):
        self.verify(lambda d: next(x for x in d[0]["locations"] if x["id"]=="new_bajor").update(availability="ANCHORED_DOCUMENTARY"))
    def test_dorvan_not_a_registered_navigation_node(self):
        self.verify(lambda d: next(x for x in d[0]["locations"] if x["id"]=="dorvan_v").update(anchor_location_id="earth"))
    def test_mars_not_automatic_project_location(self):
        self.verify(lambda d: next(x for x in d[0]["locations"] if x["id"]=="mars_utopia").update(facility_id="canon:facility:fake"))
    def test_scenario_claims_runtime(self):
        self.verify(lambda d: d[1].update(runtime_executed=True))
    def test_not_new_population(self):
        self.verify(lambda d: d[0]["locations"][0].update(population_count=100000))
    def test_missing_scenario(self):
        self.verify(lambda d: d[1]["scenarios"].pop())
if __name__ == "__main__":
    unittest.main()
