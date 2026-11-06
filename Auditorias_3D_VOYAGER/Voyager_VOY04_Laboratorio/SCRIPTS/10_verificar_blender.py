import bpy,json,sys,hashlib,math,collections,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env,segment_tri
from geom import ray,segment_segment_sq
meta=json.loads((R/'DATOS/manifest_blender.json').read_text());seqs=json.loads((R/'DATOS/trayectorias.json').read_text());bpy.ops.wm.open_mainfile(filepath=meta['file'],load_ui=False,use_scripts=False);T=np.array(meta['bridge_translation']);npz=np.load(R/'DATOS/geometria.npz');rows=json.loads((R/'DATOS/objetos.json').read_text());source={};start=0
for row in rows:source[row['name']]=npz['vertices'][start:start+row['vertices']]+T;start+=row['vertices']
def uvdigest(me):
 h=hashlib.sha256()
 for uv in me.uv_layers:
  a=np.empty(len(uv.data)*2,np.float32);uv.data.foreach_get('uv',a);h.update(a.tobytes())
 return h.hexdigest()
copychecks=[];baseenv=Env();navparts=set(baseenv.m['parts']);forward=np.array(baseenv.m['forward']);lastscene=None
for c in meta['copies']:
 o=bpy.data.objects[c['object']];s=bpy.data.scenes[c['scene']]
 if s!=lastscene:bpy.context.window.scene=s;s.frame_set(151 if s.name.startswith('04_') else 1);bpy.context.view_layer.update();lastscene=s
 expected=source[c['source']].copy();k=c['source_key'];config=next((x['config'] for x in seqs if s.name==f'04_PROTO_{x["H"]:.2f}'),None)
 if config and k in navparts:
  if k=='MSB_30191':
   lo=expected[:,2].min();hi=expected[:,2].max();bottom=T[2]+.0483257818;top=T[2]+meta['station_matrix'][2][3]-T[2]-config['drop']-.080;expected[:,2]=bottom+(expected[:,2]-lo)*(top-bottom)/(hi-lo)
  else:
   expected[:,2]-=config['drop']
   if k in ['Object_76','Layer__3','MSB_30192','MSB_30193']:expected+=forward*config['backshift']
 actual=np.array([o.matrix_world@v.co for v in o.data.vertices]);err=float(np.linalg.norm(actual-expected,axis=1).max());uvok=uvdigest(o.data)==c['uv_digest'];matok=[m.name if m else None for m in o.data.materials]==c['materials'];copychecks.append(dict(scene=s.name,key=k,world_vertex_error_m=err,UV_equal=uvok,materials_equal=matok,unique_mesh=o.data.users==1))
bad=[x for x in copychecks if x['world_vertex_error_m']>.00003 or not x['UV_equal'] or not x['materials_equal'] or not x['unique_mesh']]
(R/'DATOS/verificacion_copias_blender.json').write_text(json.dumps(dict(count=len(copychecks),bad=bad,max_world_vertex_error_m=max(x['world_vertex_error_m'] for x in copychecks),results=copychecks),indent=2));print('COPIES_VERIFIED',len(copychecks),'BAD',len(bad),flush=True)
output=[]
for seq in seqs:
 H=seq['H'];s=bpy.data.scenes[f'04_PROTO_{H:.2f}'];bpy.context.window.scene=s;rig=next(o for o in s.objects if o.type=='ARMATURE');root=next(o for o in s.objects if o.name.endswith('__CTRL_DESLIZAMIENTO'));cfg=seq['config'];e=Env().adapted(cfg['drop'],cfg['backshift']).rail(cfg['D']);rest={p['name']:p for p in seq['poses'][0]['body']['parts']};errors=[];fails=[];footwork=[];angles=[]
 for idx in range(601):
  f=1+idx*.5;frame=int(f);s.frame_set(frame,subframe=f-frame);dg=bpy.context.evaluated_depsgraph_get();r=rig.evaluated_get(dg);parts=[]
  for name,old in rest.items():
   pb=r.pose.bones[name];p=np.array(pb.head);q=np.array(pb.tail) if np.linalg.norm(np.array(old['q'])-old['p'])>.0001 else p.copy();parts.append(dict(name=name,p=p,q=q,r=old['r']))
  actual=dict(height=H,parts=parts,invalid_ik=[],joints={});D=float(-np.dot(np.array(root.matrix_world.translation)-(np.array(e.P)+T),e.m['forward']))
  if idx%2==0:
   original=seq['poses'][frame-1]['body']['parts'];errors.extend(max(np.linalg.norm(p['p']-o['p']),np.linalg.norm(p['q']-o['q'])) for p,o in zip(parts,original))
  else:
   test=e.test(actual,chair_delta=(0,-D,0))
   if not test['clear']:fails.append(dict(frame=f,**test))
  if frame==151 and idx%2==0:
   for pt in parts:
    if pt['name'].startswith('PIE'):
     for q in [pt['p'],pt['q'],(pt['p']+pt['q'])/2]:
      sole=q-[0,0,pt['r']];ix=e.candidates(sole,sole,.1);hit=ray(e.tri[ix],sole+[0,0,.02],[0,0,-1],.08);footwork.append(dict(part=pt['name'],sole=sole.tolist(),gap_m=sole[2]-hit['point'][2] if hit else None,floor_object=str(e.names[ix[hit['triangle']]]) if hit else None))
  if idx%120==0:print('VALIDATING',H,f,flush=True)
 maxerr=float(max(errors));output.append(dict(H=H,poses_compared=301,midpoints_tested=300,max_axis_endpoint_error_m=maxerr,midpoint_failures=fails,foot_support_work=footwork,all_sampled_geometry_pass=maxerr<.00003 and not fails,continuous_collision_certified=False));print('RIG_RESULT',H,maxerr,len(fails),flush=True)
(R/'DATOS/verificacion_animacion_guardada.json').write_text(json.dumps(output,indent=2))
assert not bad
assert all(x['max_axis_endpoint_error_m']<.00003 for x in output)
print('VERIFY_COMPLETED',flush=True)
