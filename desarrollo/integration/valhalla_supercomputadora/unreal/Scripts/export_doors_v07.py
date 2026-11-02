"""Blender: partition only the three additional doors with identified original leaves.
This is a PARTIAL inventory. Six signposted memory accesses remain unresolved.
All original faces are retained; the center trim of #58 is split with interpolated
UV and normals. The output contains generated geometry and belongs in a new
repository-authorized temporary output directory, never in Git.
"""
import json,hashlib,argparse,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--reference',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
assert not a.output.exists();assert hashlib.sha256(a.source.read_bytes()).hexdigest()=='e55df3cf537365ac8e145b9a7cd96605f5b0edaa5537473a734f090f931a8670'
ref=json.loads(a.reference.read_text());assert ref['source_sha256']=='e55df3cf537365ac8e145b9a7cd96605f5b0edaa5537473a734f090f931a8670';bpy.ops.wm.open_mainfile(filepath=str(a.source));bpy.context.scene.frame_set(20)
placements={(i.parent.name if i.parent else i.object.original.name):(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.type=='MESH'}
materials={r['name']:'/Game/Valhalla/Materials/M_%03d'%i for i,r in enumerate(ref['materials'])};out={'source_sha256':ref['source_sha256'],'materials':materials,'doors':[]}
for id,parent,yaw in [('D02','Component_437343',0),('D03','Component_381616',90),('D04','Component_381616.001',90)]:
 o,matrix=placements[parent];mesh=o.data;mesh.calc_loop_triangles();world=np.array([matrix@v.co for v in mesh.vertices],dtype=float);normal=matrix.to_3x3().inverted().transposed();groups=[[],[],[]]
 if id=='D02':
  # Original west door: its rear leaf plane is distinct from the bevelled frame.
  mobile=lambda tri: all(abs(world[j,0]-15.4550314)<.00002 and -2.92481<=world[j,1]<=-2.06079 for j in tri.vertices)
  split=-2.5321
  for tri in mesh.loop_triangles:groups[(0 if world[list(tri.vertices),1].mean()>split else 1) if mobile(tri) else 2].append(tri)
 else:
  split=(world[:,0].min()+world[:,0].max())/2
  for tri in mesh.loop_triangles:
   coords=world[list(tri.vertices),0]
   if coords.max()>=split:groups[0].append(tri)
   if coords.min()<=split:groups[1].append(tri)
 chosen=np.concatenate([world[list(t.vertices)] for group in groups[:2] for t in group]);lo=chosen.min(0);hi=chosen.max(0);root=(lo+hi)/2;root[2]=lo[2];theta=np.radians(yaw);R=np.array([[np.cos(theta),np.sin(theta),0],[-np.sin(theta),np.cos(theta),0],[0,0,1.]])
 def ue(v):return np.asarray(v)*[100,-100,100]
 record={'id':id,'root':ue(root).tolist(),'yaw':yaw,'width':float(hi[1]-lo[1])*100 if id=='D02' else float(hi[0]-lo[0])*100,'height':float(hi[2]-lo[2])*100,'leaves':[],'source_parent':parent,'source_polygons':len(mesh.polygons),'source_triangles':len(mesh.loop_triangles),'partition_triangles':[len(g) for g in groups]}
 def payload(group,center,side=None):
  verts=[];tris=[]
  for t in group:
   corners=[]
   for j,li in zip(t.vertices,t.loops):
    uv=np.array(mesh.uv_layers[0].data[li].uv) if mesh.uv_layers else np.zeros(2);n=normal@mesh.corner_normals[li].vector;n.normalize();corners.append(np.concatenate([world[j],uv,np.array(n)]))
   if side is not None:
    clipped=[]
    for first,second in zip(corners,corners[1:]+corners[:1]):
     da=(first[0]-split)*side;db=(second[0]-split)*side
     if da>=0:clipped.append(first)
     if (da<0 and db>0) or (da>0 and db<0):clipped.append(first+(second-first)*da/(da-db))
    corners=clipped
   for k in range(1,len(corners)-1):
    indexes=[];uv=[];ns=[]
    for c in [corners[0],corners[k],corners[k+1]]:
     indexes.append(len(verts));verts.append((R@(ue(c[:3])-ue(center))).tolist());uv.append(c[3:5].tolist());n=c[5:];n=n/np.linalg.norm(n);ns.append((R@(n*[1,-1,1])).tolist())
    tris.append({'v':indexes,'uv':uv,'n':ns,'material':int(t.material_index)})
  return {'vertices':verts,'triangles':tris,'materials':[m.name for m in mesh.materials]}
 for idx,g in enumerate(groups[:2]):
  assert g;v=np.concatenate([world[list(t.vertices)] for t in g]);center=(v.min(0)+v.max(0))/2;record['leaves'].append({'closed':(R@(ue(center)-ue(root))).tolist(),'mesh':payload(g,center,1 if idx==0 else -1) if id!='D02' else payload(g,center)})
 if groups[2]:record['frame']=payload(groups[2],root)
 source=next(r for r in ref['instances'] if r['source_instance']==parent and r['source_object']==o.name);record['original_asset']='/Game/Valhalla/Meshes/SM_%03d'%list(ref['meshes']).index(source['mesh']);record['original_location']=source['location'];record['travel']=record['width']/2+4
 if id!='D02':record['original_asset']='/Game/ValhallaV06/G/F14' # Verified V06 private floor-normal variant of #58
 if id=='D02':record.update(rig_frame_asset='/Game/ValhallaV07/Meshes/D02_OriginalFrame',rig_frame_location=[0,0,0],rig_frame_roll=0)
 else:
  frame_parent='Component_381617' if id=='D03' else 'Component_381617.001';frame=next(x for x in ref['instances'] if x['source_instance']==frame_parent and x['source_object']=='Component#51');record.update(rig_frame_asset='/Game/Valhalla/Meshes/SM_%03d'%list(ref['meshes']).index(frame['mesh']),rig_frame_location=(R@(np.array(frame['location'])-ue(root))).tolist(),rig_frame_roll=90)
 def area(data):
  v=np.array(data['vertices']);return sum(np.linalg.norm(np.cross(v[t['v'][1]]-v[t['v'][0]],v[t['v'][2]]-v[t['v'][0]]))/2 for t in data['triangles'])
 source_area=sum(np.linalg.norm(np.cross(world[t.vertices[1]]-world[t.vertices[0]],world[t.vertices[2]]-world[t.vertices[0]]))/2 for t in mesh.loop_triangles)*10000
 partition_area=sum(area(x['mesh']) for x in record['leaves'])+(area(record['frame']) if 'frame' in record else 0)
 record['surface_area_error_cm2']=abs(source_area-partition_area);assert record['surface_area_error_cm2']<.01,(id,source_area,partition_area,record['surface_area_error_cm2'])
 out['doors'].append(record)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,separators=(',',':')));print('PARTITION',[(r['id'],r['partition_triangles'],r['width'],r['height']) for r in out['doors']])


