#!/usr/bin/env python3
"""Sector-level determinism, stable IDs, star spacing and canon protection."""
from __future__ import annotations
import json
import math
import unittest
import astro_sector_v1 as sector

class SectorTests(unittest.TestCase):
    def test_sector_is_deterministic_and_distinct(self):
        a=sector.generate_sector("game-seed","041",systems=5)
        self.assertEqual(a,sector.generate_sector("game-seed","041",systems=5))
        b=sector.generate_sector("different-seed","041",systems=5)
        self.assertNotEqual(a["region"]["seed_hash"],b["region"]["seed_hash"])
        self.assertEqual(len(a["systems"]),5)
        ids=[s["system"]["system"]["system_id"] for s in a["systems"]]
        self.assertEqual(len(set(ids)),5)
        coords=[s["position_light_years"] for s in a["systems"]]
        for i,p in enumerate(coords):
            for q in coords[i+1:]:
                self.assertGreaterEqual(math.dist(p,q),1.49999)
        self.assertEqual(len(a["standalone_objects"]),len({
            obj["entity_id"] for obj in a["standalone_objects"]}))
        view=json.dumps(sector.public_sector_index(a))
        self.assertNotIn("biosphere",view)
        self.assertNotIn("ground_truth",view)

    def test_canonical_reservation_and_boundaries(self):
        with self.assertRaisesRegex(ValueError,"reserved"):
            sector.generate_sector("canon","041",reserved_system_names={"PROC-041-1"})
        with self.assertRaises(ValueError):
            sector.generate_sector("bad","041",systems=0)
        with self.assertRaises(ValueError):
            sector.generate_sector("bad","041",systems=26)

    def test_rare_objects_are_not_forced_per_system(self):
        for n in range(12):
            a=sector.generate_sector(f"region-{n}","041",systems=2)
            self.assertLessEqual(len(a["standalone_objects"]),2)
            for obj in a["standalone_objects"]:
                self.assertFalse(obj["canonical_reserved"])
                self.assertTrue(obj["entity_id"].startswith("gen:"))

if __name__=="__main__":
    unittest.main(verbosity=2)
