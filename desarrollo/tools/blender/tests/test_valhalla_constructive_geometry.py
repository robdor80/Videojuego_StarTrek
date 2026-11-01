"""Analytic checks for surface subtraction, ownership and UV interpolation."""
import sys
from pathlib import Path
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from shapely.geometry import box,GeometryCollection,LineString
from valhalla_constructive_geometry import vertical_prisms,subtract_convex,fit_border,triangle_surface_gaps


def subtract_all(surface,cutters):
    pieces=[surface]
    for cutter in cutters:pieces=[p for old in pieces for p in subtract_convex(old,cutter)]
    return pieces


def area(pieces):
    return sum(np.linalg.norm(sum((np.cross(p[i,:3]-p[0,:3],p[i+1,:3]-p[0,:3])
                                  for i in range(1,len(p)-1)),np.zeros(3)))/2 for p in pieces)


class ConstructiveGeometryTests(unittest.TestCase):
    def setUp(self):
        self.cutters=vertical_prisms(box(0,0,1,1),0,1)

    def test_inside_surface_removed(self):
        surface=np.array([[.2,.2,.5],[.8,.2,.5],[.8,.8,.5],[.2,.8,.5]])
        self.assertAlmostEqual(area(subtract_all(surface,self.cutters)),0)

    def test_outside_surface_unchanged(self):
        surface=np.array([[2,2,.5],[3,2,.5],[3,3,.5],[2,3,.5]])
        self.assertAlmostEqual(area(subtract_all(surface,self.cutters)),1)

    def test_partial_subtraction_preserves_area_and_uv(self):
        xy=np.array([[-.5,-.5],[1.5,-.5],[1.5,1.5],[-.5,1.5]])
        surface=np.column_stack([xy,np.full(4,.5),xy*3+2]);pieces=subtract_all(surface,self.cutters)
        self.assertAlmostEqual(area(pieces),3,places=9)
        for polygon in pieces:np.testing.assert_allclose(polygon[:,3:],polygon[:,:2]*3+2,atol=1e-10)

    def test_coplanar_interface_has_one_owner(self):
        surface=np.array([[0,0,1],[1,0,1],[1,1,1],[0,1,1]],dtype=float)
        self.assertAlmostEqual(area(subtract_all(surface,self.cutters)),0,places=9)

    def test_height_band_does_not_cut_lower_surface(self):
        surface=np.array([[0,0,-1],[1,0,-1],[1,1,-1],[0,1,-1]],dtype=float)
        self.assertAlmostEqual(area(subtract_all(surface,self.cutters)),1,places=9)

    def test_shared_boundary_lines_have_no_cutter_volume(self):
        collection=GeometryCollection([box(0,0,1,1),LineString([(1,0),(1,1)])])
        self.assertEqual(len(vertical_prisms(collection,0,1)),2)

    def test_subtraction_is_invariant_under_rigid_motion(self):
        angle=.37;rotation=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1]])
        shift=np.array([8.,-4.,3.]);surface=np.array([[-.5,-.5,.5],[1.5,-.5,.5],[1.5,1.5,.5],[-.5,1.5,.5]])
        transformed=[]
        for low,high,planes in self.cutters:
            corners=np.array([[x,y,z] for x in [low[0],high[0]] for y in [low[1],high[1]] for z in [low[2],high[2]]])@rotation.T+shift
            transformed.append((corners.min(0),corners.max(0),[(rotation@n,d+(rotation@n)@shift) for n,d in planes]))
        self.assertAlmostEqual(area(subtract_all(surface@rotation.T+shift,transformed)),3,places=8)

    def test_border_fit_preserves_inner_glazing_and_depth(self):
        outer=np.array([[x,y,z] for x in [-.5,.5] for y in [-1,1] for z in [-.01,.01]])
        inner=np.array([[x,y,0] for x in [-.3,.3] for y in [-.7,.7]])
        vertices=np.vstack([outer,inner]);planes=[(np.array([1.,0,0]),.49),(np.array([-1.,0,0]),.49)]
        result=fit_border(vertices,np.eye(3),np.zeros(3),planes)
        np.testing.assert_array_equal(result[len(outer):],inner)
        np.testing.assert_array_equal(result[:,2],vertices[:,2])
        self.assertLessEqual(float(abs(result[:,0]).max()),.48800001)

    def test_real_triangle_gap_for_parallel_planes(self):
        tri=np.array([[0.,0,0],[1,0,0],[0,1,0]])
        self.assertAlmostEqual(float(triangle_surface_gaps(tri,(tri+[0,0,.002])[None,:,:])[0]),.002,places=12)

    def test_edge_piercing_another_face_has_zero_gap(self):
        tri=np.array([[0.,0,0],[1,0,0],[0,1,0]]);other=np.array([[.2,.2,-1],[.2,.2,1],[.3,.2,0]])
        self.assertAlmostEqual(float(triangle_surface_gaps(tri,other[None,:,:])[0]),0,places=12)

    def test_real_gap_is_preserved_under_rigid_motion(self):
        tri=np.array([[0.,0,0],[1,0,0],[0,1,0]]);angle=.39;rotation=np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]);shift=np.array([11.,-7.,9.])
        value=triangle_surface_gaps(tri@rotation.T+shift,((tri+[0,0,.002])@rotation.T+shift)[None,:,:])[0]
        self.assertAlmostEqual(float(value),.002,places=11)


if __name__=='__main__':unittest.main()
