#!/usr/bin/env python3
"""Independent Miranda-120 illustrative 5+2 roster arithmetic, not live NPCs/Core."""
import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "validation/fixtures/f04/miranda_120_watch_5x2_example_v0.1.json"


class MirandaExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    @staticmethod
    def pair_off_days(station_index, watch_index, watch_count):
        offset = (station_index * watch_count + watch_index) % 7
        return ({(5 + offset) % 7, (6 + offset) % 7},
                {(2 + offset) % 7, (3 + offset) % 7})

    @classmethod
    def coverage(cls, model, absent=None):
        occupied = Counter()
        regular_station_hours = Counter()
        member_workdays = Counter()
        for si, station in enumerate(cls.data["stations"]):
            for wi, watch in enumerate(model["watches"]):
                ids = (f"{model['id']}:{station}:{wi}:A",
                       f"{model['id']}:{station}:{wi}:B")
                offs = cls.pair_off_days(si, wi, model["watch_count"])
                assert not (offs[0] & offs[1]), "Pair must not share days off"
                for mi, person in enumerate(ids):
                    member_workdays[person] = sum(day not in offs[mi] for day in range(7))
                for day in range(7):
                    eligible = [mi for mi in range(2)
                                if day not in offs[mi] and ids[mi] != absent]
                    if not eligible:
                        continue
                    chosen = eligible[(day + si + wi) % len(eligible)]
                    for hour in range(watch["start"], watch["end"]):
                        occupied[(day, station, hour)] += 1
                        regular_station_hours[ids[chosen]] += 1
        return occupied, regular_station_hours, member_workdays

    def test_population_and_crew_breakdown(self):
        d = self.data
        self.assertEqual(d["ship"]["class_id"], "miranda")
        self.assertEqual(d["ship"]["crew_count"], 120)
        self.assertEqual(len(d["stations"]), 6)
        self.assertIn("NOT_CANON", d["status"])
        self.assertEqual(len(d["models"]), 2)
        for m in d["models"]:
            with self.subTest(model=m["id"]):
                self.assertEqual(m["watch_count"] * m["watch_hours"], 24)
                self.assertEqual(m["station_staff_total"],
                                 6 * m["watch_count"] * m["staff_per_station_watch"])
                self.assertEqual(sum(m["other_staff"].values()) + m["station_staff_total"], 120)
                self.assertEqual(sorted(h for w in m["watches"]
                                        for h in range(w["start"], w["end"])),
                                 list(range(24)))

    def test_seven_day_coverage_and_5_plus_2(self):
        for m in self.data["models"]:
            with self.subTest(model=m["id"]):
                covered, hours, days = self.coverage(m)
                self.assertEqual(len(days), m["station_staff_total"])
                self.assertTrue(all(n == 5 for n in days.values()))
                self.assertEqual(len(covered), 7 * 24 * 6)
                self.assertTrue(all(value == 1 for value in covered.values()),
                                "Every station-hour covered exactly once, no double occupancy")
                self.assertEqual(sum(hours.values()), 1008)
                pool_hours = m["station_staff_total"] * 5 * m["watch_hours"]
                self.assertEqual(pool_hours, 1440)
                self.assertEqual(pool_hours - sum(hours.values()), 432)

    def test_extended_absence_not_magically_covered(self):
        # Removing one real character for a full week creates uncovered slots.
        # Thus this fixture proves regular days off, NOT vacation/sick leave resilience.
        for m in self.data["models"]:
            absent = f"{m['id']}:{self.data['stations'][0]}:0:A"
            occupied, _, _ = self.coverage(m, absent=absent)
            self.assertLess(len(occupied), 7 * 24 * 6)

    def test_nonoperational_boundaries(self):
        limits = " ".join(self.data["important_limits"])
        for term in ("Medical", "vacations", "save/load", "CoreRPG", "Handoff"):
            self.assertIn(term, limits)


if __name__ == "__main__":
    unittest.main()
