#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "generate_starship_instance.py"
spec = importlib.util.spec_from_file_location("shipgen", MODULE_PATH)
shipgen = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = shipgen
spec.loader.exec_module(shipgen)


class ProceduralStarshipGeneratorTests(unittest.TestCase):
    def generate(self, seed="ship_test_001", **overrides):
        args = dict(
            campaign_seed=seed,
            era_id="tng_ds9_voyager",
            campaign_date="2372-01-01",
            operator="starfleet",
            role="science",
            requested_watch_pattern=None,
        )
        args.update(overrides)
        return shipgen.generate(**args)

    def test_deterministic_same_seed(self):
        self.assertEqual(self.generate(), self.generate())

    def test_different_seed_changes_identity(self):
        self.assertNotEqual(
            self.generate("ship_test_001")["ship"]["ship_id"],
            self.generate("ship_test_002")["ship"]["ship_id"],
        )

    def test_validation_passes(self):
        payload = self.generate()
        self.assertEqual(shipgen.validate(payload), [])

    def test_watch_allocation_equals_duty_crew(self):
        payload = self.generate()
        self.assertEqual(
            payload["shipboard_life"]["watch"]["allocation_total"],
            payload["population"]["duty_crew_target"],
        )

    def test_civilians_are_not_duty_crew(self):
        payload = self.generate(
            seed="galaxy_population_test",
            role="deep_space_exploration",
        )
        self.assertEqual(
            payload["population"]["total_people_aboard_initial"],
            payload["population"]["duty_crew_target"]
            + payload["population"]["civilian_residents"]
            + payload["population"]["passengers"],
        )

    def test_operator_sample_matrix(self):
        cases = [
            ("starfleet", "tng_ds9_voyager", "2372-01-01"),
            ("klingon", "kirk", "2287-01-01"),
            ("klingon", "tng_ds9_voyager", "2372-01-01"),
            ("romulan", "kirk", "2267-01-01"),
            ("romulan", "tng_ds9_voyager", "2372-01-01"),
            ("cardassian", "tng_ds9_voyager", "2372-01-01"),
        ]
        for index, (operator, era, date) in enumerate(cases):
            payload = shipgen.generate(
                campaign_seed=f"matrix_{index}",
                era_id=era,
                campaign_date=date,
                operator=operator,
                role=None,
                requested_watch_pattern=None,
            )
            self.assertEqual(shipgen.validate(payload), [], msg=(operator, era, date))

    def test_seed_sample(self):
        for index in range(64):
            payload = self.generate(seed=f"sample_{index:02d}")
            self.assertEqual(shipgen.validate(payload), [], msg=index)

    def test_four_shift_is_supported_for_starfleet(self):
        payload = self.generate(requested_watch_pattern="four_shift")
        watch = payload["shipboard_life"]["watch"]
        self.assertEqual(watch["pattern"], "four_shift")
        self.assertEqual(len(watch["definitions"]), 4)
        self.assertTrue(all(x["nominal_duration_hours"] == 6 for x in watch["definitions"]))


if __name__ == "__main__":
    unittest.main()
