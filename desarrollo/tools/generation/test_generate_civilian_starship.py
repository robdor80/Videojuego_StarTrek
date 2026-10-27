#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "generate_civilian_starship.py"
spec = importlib.util.spec_from_file_location("civshipgen", MODULE_PATH)
civshipgen = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = civshipgen
spec.loader.exec_module(civshipgen)


class CivilianStarshipGeneratorTests(unittest.TestCase):
    def build(self, need_id="need:cargo:001", role="cargo_freighter"):
        return civshipgen.generate(
            campaign_seed="campaign_demo_001",
            need_id=need_id,
            era_id="tng_ds9_voyager",
            campaign_date="2372-01-01",
            role=role,
            operator_context="independent_civilian",
        )

    def test_deterministic(self):
        self.assertEqual(self.build(), self.build())

    def test_same_design_can_produce_distinct_ships(self):
        a = self.build("need:cargo:001")
        b = self.build("need:cargo:002")
        self.assertEqual(a["design"]["design_id"], b["design"]["design_id"])
        self.assertNotEqual(a["ship"]["ship_id"], b["ship"]["ship_id"])

    def test_watch_allocation_matches_duty_crew(self):
        payload = self.build()
        self.assertEqual(
            payload["shipboard_life"]["watch"]["allocation_total"],
            payload["population"]["duty_crew_target"],
        )

    def test_role_sample(self):
        roles = [
            "cargo_freighter","passenger_liner","courier","tug","salvage",
            "mining","survey","medical","rescue","colony_transport","trader",
            "private_civilian",
        ]
        for index, role in enumerate(roles):
            payload = self.build(f"need:{role}:{index}", role)
            self.assertEqual(civshipgen.validate(payload), [], msg=role)

    def test_bare_smuggling_generation_is_blocked(self):
        with self.assertRaises(ValueError):
            self.build("need:smuggle:001", "criminal_or_smuggling_when_context_valid")


if __name__ == "__main__":
    unittest.main()
