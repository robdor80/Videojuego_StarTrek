"""Blender --background --factory-startup --python this_file.py."""
import importlib.util
import os
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import unittest
import numpy as np
if os.environ.get('VH_PYTHON_DEPS'):sys.path.insert(0,os.environ['VH_PYTHON_DEPS'])

spec=importlib.util.spec_from_file_location('geometry',Path(__file__).with_name('build_v07_memory_geometry.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)


class GeometryTests(unittest.TestCase):
    def polygon(self):
        return [np.array([x,y,0.,x/10,y/10,0,0,1]) for x,y in ((-2,-2),(2,-2),(2,2),(-2,2))]

    def test_portal_subtraction_preserves_area_outside(self):
        result,cut=g.subtract_box(self.polygon(),((0,-1,1),(1,-1,1),(2,-1,1)))
        self.assertTrue(cut)
        self.assertAlmostEqual(sum(g.area(p) for p in result),12)
        for p in result:
            for v in p:
                self.assertAlmostEqual(v[3],v[0]/10)
                self.assertAlmostEqual(v[4],v[1]/10)

    def test_nonintersecting_geometry_keeps_area(self):
        result,cut=g.subtract_box(self.polygon(),((0,3,4),(1,-1,1),(2,-1,1)))
        self.assertFalse(cut)
        self.assertAlmostEqual(sum(g.area(p) for p in result),16)

    def test_existing_floor_is_subtracted_once(self):
        tri=[np.array(p,dtype=float) for p in ((-70,-90),(400,-90),(400,90))]
        pieces=g.complementary_surface([tri])
        def area2(poly):return g.area([np.r_[p,0] for p in poly])
        self.assertAlmostEqual(sum(area2(p) for p in pieces),42300)
        pieces=g.complementary_surface([tri,tri])
        self.assertAlmostEqual(sum(area2(p) for p in pieces),42300)

    def test_new_surfaces_use_unreal_front_face_convention(self):
        part=g.new_part('test')
        g.emit(part,self.polygon(),'white',orient_for_unreal=True)
        for tri in part['triangles']:
            a,b,c=[np.array(part['vertices'][i]) for i in tri['v']]
            self.assertLess(np.dot(np.cross(b-a,c-a),np.array(tri['n']).mean(0)),0)


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(GeometryTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():raise RuntimeError('Geometry tests failed')
