"""MAP-01 deterministic unit tests. Run: python -m unittest discover -s desarrollo/tools/validation -p test_interior_navigation.py"""
import copy
import json
import unittest
from pathlib import Path

from interior_navigation import MapValidationError, route, validate_map

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / "desarrollo/validation/fixtures/f12/interior_navigation_synthetic_v0.1.json"


class InteriorNavigationTests(unittest.TestCase):
    def setUp(self):
        self.graph = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.allowed = {x["location_id"] for x in self.graph["locations"]} - {"deck_e_restricted"}

    def test_valid_fixture(self):
        validate_map(self.graph)

    def test_route_between_decks(self):
        self.assertEqual(route(self.graph, "deck_d_corridor", "deck_e_engineering",
                               permitted_locations=self.allowed),
                         ["deck_d_corridor", "deck_d_lift", "deck_e_lift", "deck_e_engineering"])

    def test_access_denied(self):
        self.assertIsNone(route(self.graph, "deck_d_corridor", "deck_e_restricted",
                                permitted_locations=self.allowed))

    def test_blocked_turbolift(self):
        self.assertIsNone(route(self.graph, "deck_d_corridor", "deck_e_engineering",
                                permitted_locations=self.allowed, blocked_links={"d_to_e"}))

    def test_unknown_destination(self):
        self.assertIsNone(route(self.graph, "deck_d_corridor", "invented_room",
                                permitted_locations=self.allowed))

    def test_unknown_origin(self):
        self.assertIsNone(route(self.graph, "invented_room", "deck_e_engineering",
                                permitted_locations=self.allowed))

    def test_unverified_link_rejected(self):
        broken = copy.deepcopy(self.graph)
        broken["links"][0]["verified"] = False
        with self.assertRaises(MapValidationError):
            validate_map(broken)

    def test_missing_node_rejected(self):
        broken = copy.deepcopy(self.graph)
        broken["links"][0]["to"] = "nonexistent"
        with self.assertRaises(MapValidationError):
            validate_map(broken)

    def test_duplicate_location_rejected(self):
        broken = copy.deepcopy(self.graph)
        broken["locations"].append(copy.deepcopy(broken["locations"][0]))
        with self.assertRaises(MapValidationError):
            validate_map(broken)

    def test_directionality(self):
        broken = copy.deepcopy(self.graph)
        broken["links"][1]["bidirectional"] = False
        self.assertIsNone(route(broken, "deck_e_engineering", "deck_d_corridor",
                                permitted_locations=self.allowed))

    def test_empty_permission_set(self):
        self.assertIsNone(route(self.graph, "deck_d_corridor", "deck_e_engineering",
                                permitted_locations=set()))


if __name__ == "__main__":
    unittest.main()
