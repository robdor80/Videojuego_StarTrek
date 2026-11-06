"""Exact surface-distance of a translating vertical capsule: its axis sweeps a quad.
Checks the whole translation interval against every broadphase triangle.
"""
import numpy as np
from geom import point_tri_sq,segment_segment_sq,dot
def intersects(p,q,tri):
 p=np.asarray(p);q=np.asarray(q);delta=q-p;a=tri[:,0];ab=tri[:,1]-a;ac=tri[:,2]-a;n=np.cross(ab,ac);den=dot(n,delta);u=np.divide(dot(n,a-p),den,out=np.full(len(tri),-1.),where=np.abs(den)>1e-13);hit=p+u[:,None]*delta;nn=dot(n,n)
 c0=dot(np.cross(tri[:,1]-tri[:,0],hit-tri[:,0]),n);c1=dot(np.cross(tri[:,2]-tri[:,1],hit-tri[:,1]),n);c2=dot(np.cross(tri[:,0]-tri[:,2],hit-tri[:,2]),n)
 # Edge signs have units m^4: an absolute epsilon made tiny decorative triangles
 # accept intersections metres outside their footprint. Normalize by area squared.
 tol=nn*1e-10
 return (u>=-1e-10)&(u<=1+1e-10)&(c0>=-tol)&(c1>=-tol)&(c2>=-tol)&(nn>1e-30)
def swept_distance(tri,p,q,h=1.9,r=.35):
 p=np.array(p);q=np.array(q);corners=np.array([p+[0,0,r],p+[0,0,h-r],q+[0,0,h-r],q+[0,0,r]]);ds=np.minimum.reduce([point_tri_sq(c,tri) for c in corners]);hit=np.zeros(len(tri),bool)
 for a,b in [(0,1),(1,2),(2,3),(3,0)]:
  hit|=intersects(corners[a],corners[b],tri)
  for i,j in [(0,1),(1,2),(2,0)]:ds=np.minimum(ds,segment_segment_sq(corners[a],corners[b],tri[:,i],tri[:,j]))
 for k in [(0,1,2),(0,2,3)]:
  qt=np.broadcast_to(corners[list(k)],tri.shape)
  for i in range(3):ds=np.minimum(ds,point_tri_sq(tri[:,i],qt));hit|=intersects(tri[:,i],tri[:,(i+1)%3],qt)
 return np.sqrt(np.maximum(np.where(hit,0,ds),0))-r
def controls():
 # Wall crossed between free endpoints: continuous test must find the collision.
 wall=np.array([[[0,-2,-1],[0,2,-1],[0,0,4]]],float)
 assert swept_distance(wall,[-1,0,0],[1,0,0])[0]<-.349
 assert abs(swept_distance(wall,[.5,-.4,0],[.5,.4,0])[0]-.15)<1e-8
 flat=np.array([[[-5,-5,0],[5,-5,0],[0,5,0]]],float)
 assert abs(swept_distance(flat,[-.2,0,.004],[.2,0,.004])[0]-.004)<1e-8
 roof=flat+[0,0,2.1];assert abs(swept_distance(roof,[-.2,0,.004],[.2,0,.004])[0]-.196)<1e-8
 reverse=swept_distance(wall,[.5,.4,.1],[.5,-.4,0]);forward=swept_distance(wall,[.5,-.4,0],[.5,.4,.1]);assert np.max(np.abs(reverse-forward))<1e-8
 tiny=np.array([[[3.983953714370728,.9190699338912964,1.9062350034713746],[3.984522294998169,.9195659995079041,1.9062856197357179],[3.9845078706741335,.919551706314087,1.9062856197357179]]])
 assert swept_distance(tiny,[3.7,.55,.78752561],[3.7,.56,.78752561],1.6)[0]>.10
 for scale in [1e-3,1,1e3]:
  assert intersects(np.array([0,0,-1])*scale,np.array([0,0,1])*scale,np.array([[[-1,-1,0],[1,-1,0],[0,1,0]]])*scale)[0]
  assert not intersects(np.array([4,0,-1])*scale,np.array([4,0,1])*scale,np.array([[[-1,-1,0],[1,-1,0],[0,1,0]]])*scale)[0]
 return dict(cases=12,passed=12,includes='tunneling wall, lateral clearance, floor, ceiling, reversal, real tiny triangle regression, scale invariant inside/outside')
