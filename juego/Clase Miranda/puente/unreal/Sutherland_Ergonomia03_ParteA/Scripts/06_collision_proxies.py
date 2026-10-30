import bpy,bmesh,json,traceback,math
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'collision_groups':[],'doors':[]}
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False);result={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or not len(o.data.vertices):continue
  o.data.calc_loop_triangles();result[o.name]={'v':np.array([list(o.matrix_world@v.co) for v in o.data.vertices])*[100,-100,100],'polys':[list(p.vertices) for p in o.data.polygons],'tri':[(t.polygon_index,list(t.vertices)) for t in o.data.loop_triangles]}
 return result
def components(verts,tris):
 parent=list(range(len(verts)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for t in tris:
  for j in t[1:]:parent[root(j)]=root(t[0])
 groups={}
 for t in tris:groups.setdefault(root(t[0]),[]).append(t)
 out=[]
 for faces in groups.values():
  ids=sorted({i for t in faces for i in t});remap={i:j for j,i in enumerate(ids)};out.append((np.array(verts)[ids],[[remap[i] for i in t] for t in faces]))
 return out
def export(mesh,name,local_shapes,path):
 objects=[];obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);objects.append(obj)
 for i,(points,faces) in enumerate(local_shapes):
  m=bpy.data.meshes.new('ReusedCollision');m.from_pydata((points*np.array([.01,-.01,.01])).tolist(),[],faces);m.update()
  q=bpy.data.objects.new('UCX_'+name+'_'+str(i).zfill(3),m);bpy.context.scene.collection.objects.link(q);objects.append(q)
 bpy.ops.object.select_all(action='DESELECT')
 for q in objects:q.select_set(True)
 bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.fbx(filepath=path,use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_NONE',mesh_smooth_type='FACE',use_tspace=True,bake_anim=False,path_mode='STRIP')
 for q in objects:
  m=q.data;bpy.data.objects.remove(q,do_unlink=True);bpy.data.meshes.remove(m)
def triangle_weights(p,a,b,c):
 v0=b-a;v1=c-a;v2=p-a;d00=v0.dot(v0);d01=v0.dot(v1);d11=v1.dot(v1);d20=v2.dot(v0);d21=v2.dot(v1);den=d00*d11-d01*d01
 if abs(den)<1e-10:return np.array([1.,0.,0.])
 v=(d11*d20-d01*d21)/den;w=(d00*d21-d01*d20)/den;return np.array([1-v-w,v,w])
try:
 plan=json.loads((D/'export_meshes.json').read_text());assert plan['ok'];dump=json.loads((D/'collision_shapes_before.json').read_text());assert dump['ok']
 base=snapshot(R.parents[1]/'blender/Miranda_Puente_Sutherland_Base.blend');new=snapshot(R.parents[1]/'blender/Miranda_Puente_Sutherland_Ergonomia_03.blend')
 ref=Path(json.loads((D/'copy_verified.json').read_text())['source']);fabrication={x['name']:x for x in json.loads((ref/'Sources/collision_fabrication.json').read_text())['exports']}
 for row in plan['collisions']:
  original=fabrication[row['actor']];ov=[];nv=[];tri=[]
  for part in original['source_parts']:
   name=part['object'];assert base[name]['polys']==new[name]['polys'],('Unsafe collision topology',name)
   chosen=set(part['faces'])
   for fi,ids in base[name]['tri']:
    if fi not in chosen:continue
    j=len(ov);ov.extend(base[name]['v'][ids]);nv.extend(new[name]['v'][ids]);tri.append([j,j+1,j+2])
  ov=np.array(ov);nv=np.array(nv);tree=BVHTree.FromPolygons([Vector(x) for x in ov],tri,all_triangles=True)
  # Establish the correspondence to the actually retained collider render data.
  drift=max((tree.find_nearest(Vector(p))[3] for p in original['world_vertices_UE_cm']),default=0)
  assert drift<.01,('Collision ancestry mismatch',row['actor'],drift)
  source=next(iter(dump['actors'][row['actor']].values()));pv=np.array(original['pivot_UE_cm']);shapes=[]
  for points,faces in components(source['world_cm'],source['triangles']):
   updated=[]
   for p in points:
    q,_,idx,_=tree.find_nearest(Vector(p));ids=tri[idx];weights=triangle_weights(np.array(q),*ov[ids]);updated.append(p+weights@(nv[ids]-ov[ids]))
   shapes.append((np.array(updated)-pv,faces))
  mesh=bpy.data.meshes.new('UpdatedDependentCollision');mesh.from_pydata(((nv-pv)*[.01,-.01,.01]).tolist(),[],tri);mesh.update()
  export(mesh,'ERG_'+row['actor'],shapes,row['file']);out['collision_groups'].append({'actor':row['actor'],'reused_shapes':len(shapes),'ancestry_drift_cm':drift,'method':'Retained each old primitive hull, displaced by barycentric source-to-Ergonomia03 surface correspondence; exported UCX without global regeneration.'})
 # Door source polygons are convex bevelled leaves. Retain the existing single
 # convex hull and its component transform, adapting its actual old vertices.
 audit={a['label']:a for a in json.loads((D/'ue_before.json').read_text())['actors']}
 for row in plan['doors']:
  c=next(c for c in audit[row['actor']]['components'] if c['name']==row['component']);source=dump['actors'][row['actor']][row['component']];oldpts=np.array(source['rendered_world_cm']);target=np.array(row['expected_world_cm'])
  def normalized(a):return (a-a.min())/max(float(np.ptp(a)),.0001)
  oh=normalized(oldpts[:,2]);th=normalized(target[:,2]);mapping=[]
  for p,h in zip(oldpts,oh):mapping.append(target[np.argmin(np.sum((target[:,:2]-p[:2])**2,axis=1)+((th-h)*100)**2)])
  mapping=np.array(mapping);yaw=math.radians(c['rotation'][2]);rot=np.array([[math.cos(yaw),-math.sin(yaw),0],[math.sin(yaw),math.cos(yaw),0],[0,0,1]]);origin=np.array(c['location']);shapes=[]
  for points,faces in components(source['world_cm'],source['triangles']):
   updated=[]
   for p in points:
    nearest=int(np.argmin(np.sum((oldpts-p)**2,axis=1)));updated.append(p+mapping[nearest]-oldpts[nearest])
   shapes.append(((np.array(updated)-origin)@rot,faces))
  assert len(shapes)==1,('Unexpected door hull count',row['actor'],row['component'])
  o=bpy.data.objects[row['source']];mesh=o.data.copy();mesh.transform(o.matrix_world);world=np.array([list(v.co) for v in mesh.vertices])*[100,-100,100];sign=np.sign(target[:,0].mean())
  bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table();bmesh.ops.delete(bm,geom=[v for v in bm.verts if world[v.index,0]*sign<0],context='VERTS');bm.to_mesh(mesh);bm.free()
  for v in mesh.vertices:v.co=Vector(((np.array(v.co)*[100,-100,100]-origin)@rot)*[.01,-.01,.01])
  mesh.materials.clear();mesh.materials.append(bpy.data.materials.get('PBR_Puertas_Burdeos_ConTexto') or bpy.data.materials.new('PBR_Puertas_Burdeos_ConTexto'))
  for p in mesh.polygons:p.material_index=0
  export(mesh,row['asset_name'],shapes,row['file']);out['doors'].append({'actor':row['actor'],'component':row['component'],'reused_shapes':len(shapes),'new_local_hull_bounds_cm':{'min':shapes[0][0].min(0).tolist(),'max':shapes[0][0].max(0).tolist()}})
 out['ok']=True
except Exception:out['error']=traceback.format_exc();print(out['error'],flush=True)
(D/'collision_proxy_update.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('COLLISION_PROXY_RESULT',out['ok'],len(out['collision_groups']),len(out['doors']),flush=True)
