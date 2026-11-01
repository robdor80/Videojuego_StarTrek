"""Small geometry operations used by the P01/T01 constructive prototypes.

Array/polygon functions and a read-only mesh adapter; no scene, file, or
visibility changes. Callers must
work on private copies, supply measured ownership boundaries, preserve source
attributes, and audit the resulting surfaces in their complete environment.
Requires NumPy and Shapely >= 2.1 (constrained triangulation); exercised with
Blender 5.2.2 / Shapely 2.1.2. Does not repair arbitrary nonmanifold solids.
"""
import numpy as np
import shapely
from shapely.geometry import MultiPoint, Point, Polygon


def fit_border(vertices, basis, center, planes, gap=.002,
               full_band=.020, zero_band=.080):
    """Adapt an outer border to convex opening planes without moving its pose.

    `basis` columns are tangent, up, depth. Each opening half-space is n.x <= d,
    with unit n pointing out of the opening. The frame outline is its convex
    hull in tangent/up coordinates. A displacement measured at that outline
    is extended across a narrow border, retaining bevel widths much better
    than projecting each offending vertex independently. The smooth falloff
    reaches zero at `zero_band`; glazing must be checked independently.

    This is appropriate only for an inspected convex outline and a sufficiently
    wide border. It is not an automatic solution for arbitrary windows.
    """
    if not 0 < full_band < zero_band or gap <= 0:
        raise ValueError('Require a positive joint and ordered border widths')
    vertices=np.asarray(vertices,dtype=float);basis=np.asarray(basis,dtype=float)
    center=np.asarray(center,dtype=float)
    if not np.allclose(basis.T@basis,np.eye(3),atol=1e-6):
        raise ValueError('Expected an orthonormal frame')
    q=(vertices-center)@basis;hull=MultiPoint(q[:,:2]).convex_hull
    if hull.geom_type!='Polygon':raise ValueError('No two-dimensional outline')
    depth=float(np.max(abs(q[:,2])));constraints=[]
    for normal,offset in planes:
        normal=np.asarray(normal,dtype=float)
        if abs(np.linalg.norm(normal)-1)>1e-6:raise ValueError('Non-unit plane')
        n=normal@basis[:,:2]
        if n@n<1e-12:raise ValueError('Opening plane parallel to depth axis')
        constraints.append((n,float(offset-gap-normal@center-abs(normal@basis[:,2])*depth)))
    result=vertices.copy()
    for index,point in enumerate(q):
        nearest=np.array(hull.exterior.interpolate(hull.exterior.project(Point(point[:2]))).coords[0])
        distance=float(np.linalg.norm(nearest-point[:2]));boundary=nearest.copy()
        for _ in range(100):
            violation=0.
            for normal,offset in constraints:
                amount=max(0.,float(normal@boundary-offset))
                boundary-=amount*normal/(normal@normal);violation=max(violation,amount)
            if violation<1e-11:break
        else:raise ValueError('Opening constraints did not converge')
        weight=float(np.clip((zero_band-distance)/(zero_band-full_band),0,1))
        weight=weight*weight*(3-2*weight)
        result[index]+=(basis[:,:2]@(boundary-nearest))*weight
    # A failed fit must not be mistaken for an accepted construction.
    if any(np.max(result@normal-(offset-gap))>1e-8 for normal,offset in planes):
        raise ValueError('Border too narrow or outline unsuitable for this fit')
    return result


def polygon_parts(geometry):
    if geometry.is_empty:return []
    if geometry.geom_type=='Polygon':return [geometry]
    if not hasattr(geometry,'geoms'):return []
    return [part for child in geometry.geoms for part in polygon_parts(child)]


def vertical_prisms(region,low,high):
    """Partition an inspected footprint into exact triangular column cutters.

    Returned cutters contain low/high AABBs and outward unit half-planes.
    This is a 2.5D construction, not a generic reconstruction of a 3D solid.
    A caller must verify that the selected support is vertical over this band.
    """
    if not low<high:raise ValueError('Empty height band')
    result=[]
    for polygon in polygon_parts(region):
        triangles=list(shapely.constrained_delaunay_triangles(polygon).geoms)
        if abs(sum(t.area for t in triangles)-polygon.area)>1e-7:
            raise ValueError('Triangulation does not cover the footprint')
        for triangle in triangles:
            xy=np.array(triangle.exterior.coords)[:3];a=xy[1]-xy[0];b=xy[2]-xy[0]
            if a[0]*b[1]-a[1]*b[0]<0:xy=xy[::-1]
            planes=[]
            for a,b in zip(xy,np.roll(xy,-1,axis=0)):
                dx,dy=b-a;normal=np.array([dy,-dx,0.]);normal/=np.linalg.norm(normal)
                planes.append((normal,float(normal[:2]@a)))
            planes.extend([(np.array([0.,0.,-1.]),-low),
                           (np.array([0.,0.,1.]),high)])
            result.append((np.r_[xy.min(0),low],np.r_[xy.max(0),high],planes))
    return result


def split_surface(polygon,normal,offset):
    """Split a convex surface polygon; columns after XYZ interpolate linearly.

    Extra columns may carry original loop UV coordinates or other continuous
    attributes. Material IDs and other discrete attributes belong to the face
    and must be retained by the caller. Both results retain the source winding.
    """
    inside=[];outside=[]
    for a,b in zip(polygon,np.roll(polygon,-1,axis=0)):
        da=float(normal@a[:3]-offset);db=float(normal@b[:3]-offset)
        if da<=1e-10:inside.append(a)
        if da>=-1e-10:outside.append(a)
        if da*db<0:
            crossing=a+(b-a)*da/(da-db);inside.append(crossing);outside.append(crossing)
    return np.array(inside),np.array(outside)


def has_surface(polygon):
    if len(polygon)<3:return False
    area_vector=sum((np.cross(polygon[i,:3]-polygon[0,:3],
                             polygon[i+1,:3]-polygon[0,:3])
                     for i in range(1,len(polygon)-1)),np.zeros(3))
    return np.linalg.norm(area_vector)>1e-11


def subtract_convex(polygon,cutter):
    """Return convex surface fragments outside one convex volume.

    Does not cap a cut, infer a solid from open surfaces, repair old holes, or
    add materials. Explicit local termination faces, if required by the chosen
    joint, must be constructed separately and verified by the caller.
    """
    low,high,planes=cutter
    if np.any(polygon[:,:3].max(0)<low-1e-9) or np.any(polygon[:,:3].min(0)>high+1e-9):
        return [polygon]
    remaining=polygon;outside=[]
    for normal,offset in planes:
        distances=remaining[:,:3]@normal-offset
        # A coplanar surface belongs to the cutter's owner. Emitting it as
        # both inside and outside duplicates entire interface faces.
        if distances.max()<=1e-9:continue
        if distances.min()>=-1e-9:return outside+[remaining]
        remaining,fragment=split_surface(remaining,normal,offset)
        if has_surface(fragment):outside.append(fragment)
        if not has_surface(remaining):return outside
    return outside


def repair_frame_diagonals(obj,world,bad_faces):
    """Retriangulate two inspected inverted frame-face pairs in a private plan.

    Reads a Blender mesh object without modifying it. Only coplanar neighbours
    with matching material, smoothing and continuous, locally affine UVs may
    participate. Returns replacement surface records; callers must preserve
    the source mesh and audit the resulting mesh after serialization.
    """
    mesh=obj.data;matrix=np.array(obj.matrix_world);old=np.array([obj.matrix_world@v.co for v in mesh.vertices]);world=np.asarray(world);records=[]
    for face in mesh.polygons:
        indices=list(face.vertices);values=np.array([np.concatenate([world[vi]]+[np.asarray(layer.data[li].uv) for layer in mesh.uv_layers]) for vi,li in zip(indices,face.loop_indices)])
        records.append({'values':values.tolist(),'material':face.material_index,'smooth':bool(face.use_smooth),'source_triangle':face.index,'original_indices':indices})
    def key(v):return tuple(np.round(v,6))
    edges={};keys=[]
    for f in mesh.polygons:
        kk=[key(old[i]) for i in f.vertices];keys.append(kk)
        for a,b in zip(kk,kk[1:]+kk[:1]):edges.setdefault(tuple(sorted([a,b])),[]).append(f.index)
    patches=[];used=set()
    for fi in bad_faces:
        if fi in used:continue
        face=mesh.polygons[fi];best=None
        for a,b in zip(keys[fi],keys[fi][1:]+keys[fi][:1]):
            for gj in edges[tuple(sorted([a,b]))]:
                if gj==fi or gj in used:continue
                other=mesh.polygons[gj]
                if face.material_index!=other.material_index or face.use_smooth!=other.use_smooth or face.normal@other.normal<.9999:continue
                points={};uv_errors=[]
                for idx in [fi,gj]:
                    rec=records[idx]
                    for kk,vi,values in zip(keys[idx],rec['original_indices'],rec['values']):
                        if kk in points:uv_errors.append(np.max(abs(np.array(values[3:])-points[kk][1][3:])))
                        else:points[kk]=(old[vi],np.array(values))
                if len(points)!=4 or max(uv_errors,default=0)>1e-4:continue
                edgepairs=[]
                for idx in [fi,gj]:
                    for u,v in zip(keys[idx],keys[idx][1:]+keys[idx][:1]):
                        if set([u,v])!=set([a,b]):edgepairs.append((u,v))
                loop=[edgepairs[0][0]]
                for _ in range(4):
                    nxt=[v for u,v in edgepairs if u==loop[-1]]
                    if len(nxt)!=1:break
                    loop.append(nxt[0])
                if len(loop)!=5 or loop[-1]!=loop[0]:continue
                loop=loop[:-1];source=np.array([points[k][0] for k in loop]);attrs=np.array([points[k][1] for k in loop]);normal=np.cross(old[list(face.vertices)][1]-old[list(face.vertices)][0],old[list(face.vertices)][2]-old[list(face.vertices)][0]);axis=int(np.argmax(abs(normal)))
                original2=np.delete(source,axis,1);new2=np.delete(attrs[:,:3],axis,1);polygon=Polygon(new2)
                if not polygon.is_valid or polygon.area<1e-10:continue
                fit=np.linalg.lstsq(np.column_stack([original2,np.ones(4)]),attrs[:,3:],rcond=None)[0];uv_error=float(np.max(abs(np.column_stack([original2,np.ones(4)])@fit-attrs[:,3:])))
                if uv_error>1e-4:continue
                triangles=[]
                for tri in shapely.constrained_delaunay_triangles(polygon).geoms:
                    coords=np.array(tri.exterior.coords)[:3];ids=[int(np.linalg.norm(new2-v,axis=1).argmin()) for v in coords];data=attrs[ids]
                    if np.cross(data[1,:3]-data[0,:3],data[2,:3]-data[0,:3])@normal<0:data=data[::-1]
                    triangles.append({'values':data.tolist(),'material':face.material_index,'smooth':bool(face.use_smooth),'source_triangle':None,'source_patch':[fi,gj]})
                if len(triangles)!=2:continue
                score=min(np.linalg.norm(np.cross(np.array(t['values'])[1,:3]-np.array(t['values'])[0,:3],np.array(t['values'])[2,:3]-np.array(t['values'])[0,:3])) for t in triangles)
                candidate=(score,gj,triangles,uv_error)
                if best is None or score>best[0]:best=candidate
        if best is None:raise ValueError(('No UV-continuous local diagonal repair',fi))
        score,gj,triangles,uv_error=best;used.update([fi,gj]);patches.append({'source_faces':[fi,gj],'replacement':triangles,'maximum_uv_affine_error':uv_error,'new_min_triangle_area_m2':score/2})
    kept=[r for i,r in enumerate(records) if i not in used]
    for patch in patches:kept.extend(patch['replacement'])
    return {'source_object':obj.name,'uv_layers':[l.name for l in mesh.uv_layers],'materials':[m.name for m in mesh.materials],'faces':kept,'diagonal_repairs':patches}


def point_triangle_distance_squared(point,t):
    a=t[:,0];n=np.cross(t[:,1]-a,t[:,2]-a);nn=(n*n).sum(1);valid=nn>1e-24
    safe=np.maximum(nn,1e-30);height=((point-a)*n).sum(1)/safe;q=point-height[:,None]*n
    inside=valid.copy()
    for i,j in [(0,1),(1,2),(2,0)]:
        sign=(np.cross(t[:,j]-t[:,i],q-t[:,i])*n).sum(1)
        inside&=sign>=-1e-12*nn
    best=np.where(inside,height*height*nn,np.inf)
    for i,j in [(0,1),(1,2),(2,0)]:
        a=t[:,i];d=t[:,j]-a;dd=(d*d).sum(1);f=np.clip(((point-a)*d).sum(1)/np.maximum(dd,1e-30),0,1);q=a+f[:,None]*d
        best=np.minimum(best,((q-point)**2).sum(1))
    return best

def edge_distance_squared(a,b,c,d):
    u=b-a;v=d-c;w=a-c;aa=np.sum(u*u,axis=-1);bb=np.sum(u*v,axis=-1);cc=np.sum(v*v,axis=-1);dd=np.sum(u*w,axis=-1);ee=np.sum(v*w,axis=-1);den=aa*cc-bb*bb
    safe=np.where(abs(den)>1e-14*aa*cc,den,1);s=np.where(abs(den)>1e-14*aa*cc,np.clip((bb*ee-cc*dd)/safe,0,1),0);t=(bb*s+ee)/np.maximum(cc,1e-30)
    below=t<0;above=t>1;s=np.where(below,np.clip(-dd/np.maximum(aa,1e-30),0,1),s);s=np.where(above,np.clip((bb-dd)/np.maximum(aa,1e-30),0,1),s);t=np.clip(t,0,1)
    x=w+s[...,None]*u-t[...,None]*v;return np.sum(x*x,axis=-1)
def segment_pierces_triangles(a,b,triangles):
    n=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]);nn=np.sum(n*n,1);delta=b-a;den=np.sum(delta*n,axis=-1);valid=(abs(den)>1e-18)&(nn>1e-24);t=np.sum((triangles[:,0]-a)*n,axis=-1)/np.where(abs(den)>1e-18,den,1);valid&=(t>=0)&(t<=1);point=a+t[:,None]*delta
    for i,j in [(0,1),(1,2),(2,0)]:valid&=np.sum(np.cross(triangles[:,j]-triangles[:,i],point-triangles[:,i])*n,axis=-1)>=-1e-12*nn
    return valid
def triangle_surface_gaps(triangle,others):
    """Euclidean triangle-to-triangle gaps, including crossings and edge minima.

    Accepts one (3,3) triangle and an (N,3,3) array. This measures real
    tessellated surfaces, rather than substituting fitted supporting planes.
    Filtering candidates with expanded triangle AABBs belongs to the caller.
    """
    count=len(others);repeat=np.repeat(triangle[None,:,:],count,axis=0);best=np.full(count,np.inf)
    for j in range(3):
        best=np.minimum(best,point_triangle_distance_squared(triangle[j],others));best=np.minimum(best,point_triangle_distance_squared(others[:,j],repeat))
        for k in range(3):best=np.minimum(best,edge_distance_squared(triangle[j],triangle[(j+1)%3],others[:,k],others[:,(k+1)%3]))
        best[segment_pierces_triangles(triangle[j],triangle[(j+1)%3],others)]=0;best[segment_pierces_triangles(others[:,j],others[:,(j+1)%3],repeat)]=0
    return np.sqrt(np.maximum(best,0))
