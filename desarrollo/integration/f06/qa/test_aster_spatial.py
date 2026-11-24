"""Angular QA display math, independent of Tk and Core distance scale."""
import unittest

from aster_spatial import angles, project


class SpatialProjectionTests(unittest.TestCase):
    def test_cardinal_bearings(self):
        for xyz, expected in (((0, 1000, 0), 0), ((1000, 0, 0), 90),
                              ((0, -1000, 0), 180), ((-1000, 0, 0), 270)):
            with self.subTest(xyz=xyz):
                self.assertEqual(round(angles(*xyz)[0]), expected)

    def test_elevation_and_quadrants(self):
        self.assertEqual(angles(0, 1000, 1000)[1], 45)
        self.assertEqual(angles(0, 1000, -1000)[1], -45)
        self.assertEqual(angles(0, 0, 1000), (0, 90))
        self.assertEqual(angles(0, 0, -1000), (0, -90))
        self.assertAlmostEqual(angles(-1000, -1000, 0)[0], 225)
        self.assertIsNone(angles(0, 0, 0))
        self.assertIsNone(project(0, 0, 0, 40, 50, 50, 30))

    def test_views_share_one_observation_and_ignore_distance(self):
        top, side, bearing, elevation = project(1000, 1000, 1000, 40, 50, 50, 30)
        self.assertGreater(top[0], 50)
        self.assertLess(top[1], 50)
        self.assertGreater(side[0], 50)
        self.assertLess(side[1], 50)
        self.assertEqual((bearing, round(elevation)), (45, 35))
        self.assertEqual(project(1, 1, 1, 40, 50, 50, 30),
                         project(1000000, 1000000, 1000000, 40, 50, 50, 30))


if __name__ == "__main__":
    unittest.main()
