import bpy,bmesh,json,math,sys,hashlib,csv
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env,serial
seqs=json.loads((R/'DATOS/trayectorias.json').read_text());inventory=json.loads((R/'DATOS/inventario_medidas.json').read_text());nav=inventory[0];P=Vector(nav['seat_point']);B=Matrix(nav['basis']);T=Vector(json.loads((R/'REFERENCIAS/prototipo_conjunto.json').read_text())['bridge_translation']);M=B.to_4x4();M.translation=P+T;Q=Matrix((Vector(nav['right']),-Vector(nav['forward']),Vector((0,0,1)))).transposed().to_4x4();Q.translation=P+T
bpy.ops.wm.open_mainfile(filepath=str(R/'REFERENCIAS/VOY03_Circulacion.blend'),load_ui=False,use_scripts=False)
if hasattr(bpy.context.preferences.edit,'keyframe_new_interpolation_type'):bpy.context.preferences.edit.keyframe_new_interpolation_type='LINEAR'
old=list(bpy.data.scenes);src=bpy.data.scenes['01_REFERENCIA_ORIGINAL'];manifest=json.loads((R/'REFERENCIAS/manifest_blender.json').read_text());names=set(manifest['architecture_fingerprints']);geo=[o for o in src.objects if o.name in names];source_keys=lambda o:str(o.get('VOY02_ORIGEN','')).removeprefix('OBJ:')
def digest(me):
 h=hashlib.sha256();h.update(str([(tuple(v.co),) for v in me.vertices]).encode());h.update(str([(tuple(p.vertices),p.material_index) for p in me.polygons]).encode())
 for uv in me.uv_layers:
  a=np.empty(len(uv.data)*2,np.float32);uv.data.foreach_get('uv',a);h.update(a.tobytes())
 return h.hexdigest()
def uvdigest(me):
 h=hashlib.sha256()
 for uv in me.uv_layers:
  a=np.empty(len(uv.data)*2,np.float32);uv.data.foreach_get('uv',a);h.update(a.tobytes())
 return h.hexdigest()
source_digests={o.name:digest(o.data) for o in geo};scenes=[];copies=[];prepared=[];rigmeta=[]
def scene(name):
 s=bpy.data.scenes.new(name);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1600;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new(name+'_WORLD');s.world.color=(.12,.12,.12);s.view_settings.view_transform='Standard';s.render.fps=24;s.frame_end=301;s['ESCALA_ARQUITECTURA']=1.1;scenes.append(s);return s
def copy_context(s,all=False):
 out={}
 for o in geo:
  key=source_keys(o);vs=np.array([o.matrix_world@Vector(v)-T-P for v in o.bound_box]);lo=vs.min(0);hi=vs.max(0);dist=np.linalg.norm(np.maximum(np.maximum(lo,-hi),0))
  if not all and (not str(o.get('VOY02_ORIGEN','')).startswith('OBJ:') or dist>2.5):continue
  c=o.copy();c.data=o.data.copy();c.parent=None;c.matrix_world=o.matrix_world.copy();c.name=s.name+'__'+key;c.hide_render=False;c.hide_viewport=False;s.collection.objects.link(c);c['SOURCE_KEY']=key;c['SOURCE_OBJECT']=o.name;c['VOY04_ROLE']='ORIGINAL_COPY';out[key]=c
  copies.append(dict(scene=s.name,object=c.name,source=o.name,source_key=key,data=c.data.name,source_digest=source_digests[o.name],uv_digest=uvdigest(o.data),materials=[m.name if m else None for m in o.data.materials],unchanged_initial=digest(c.data)==source_digests[o.name]))
 return out
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
blue=material('MANIQUI_160',(.05,.42,.95));green=material('MANIQUI_175',(.08,.75,.35));orange=material('MANIQUI_190',(.95,.48,.06));red=material('FALLO_CONSERVADO',(.95,.03,.04));railmat=material('MECANISMO_PROPUESTO',(.05,.7,.8))
def empty(s,name,matrix,parent=None):
 o=bpy.data.objects.new(s.name+'__'+name,None);s.collection.objects.link(o);o.empty_display_type='ARROWS';o.empty_display_size=.18;o.matrix_world=matrix
 if parent:o.parent=parent;o.matrix_world=matrix
 o['VOY04_ROLE']='CONTROL_LAB';return o
def chair(s,ctx,drop=0,backshift=0,D=0):
 root=empty(s,'CTRL_DESLIZAMIENTO',Q.copy());lift=empty(s,'CTRL_ALTURA',Q.copy(),root);backm=Q.copy();backm.translation=M@Vector((0,-.25,0));back=empty(s,'CTRL_RESPALDO',backm,lift);basekeys={'MSB_30191'};backkeys={'Object_76','Layer__3','MSB_30192','MSB_30193'};records=[]
 for k in nav['parts']:
  o=ctx[k];oldw=o.matrix_world.copy();control=root if k in basekeys else back if k in backkeys else lift
  # Change the copied object's origin without changing its geometry in world space.
  before=[oldw@v.co for v in o.data.vertices];pivot=control.matrix_world.copy();o.data.transform(pivot.inverted()@oldw);o.matrix_world=pivot;o.parent=control;o.matrix_world=pivot
  err=max((a-o.matrix_world@v.co).length for a,v in zip(before,o.data.vertices));assert err<.00002,(k,err)
  if drop and k in basekeys:
   # Localized sleeve reconstruction; rest of original mesh/UV is unchanged.
   vworld=[o.matrix_world@v.co for v in o.data.vertices];lo=min(v.z for v in vworld);hi=max(v.z for v in vworld);bottom=T.z+.0483257818;top=T.z+P.z-drop-.080
   for v,w in zip(o.data.vertices,vworld):w.z=bottom+(w.z-lo)*(top-bottom)/(hi-lo);v.co=o.matrix_world.inverted()@w
   o['VOY04_ROLE']='SLEEVE_REBUILT_EXPERIMENTAL'
  records.append(dict(key=k,object=o.name,parent=control.name,origin_after=list(o.matrix_world.translation),matrix_after=[list(x) for x in o.matrix_world],matrix_before=[list(x) for x in oldw],pivot_world_error_m=err,role=o.get('VOY04_ROLE')))
 lift.location.z-=drop;back.location.y-=backshift
 if D:
  floor=.0233257818-P.z
  for name,lo,hi,parent in [('GUIA_NUEVA',[-.035,-D-.08,floor+.001],[.035,.08,floor+.009],None),('CARRO_NUEVO',[-.075,-.08,floor+.009],[.075,.08,floor+.025],root)]:
   vs=[M@Vector((x,y,z)) for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]];fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)];me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(railmat);o=bpy.data.objects.new(s.name+'__'+name,me);s.collection.objects.link(o);o['SOURCE_KEY']='VOY04_'+name;o['VOY04_ROLE']='NEW_PROPOSED_MECHANISM'
   if parent:world=o.matrix_world.copy();o.parent=parent;o.matrix_world=world
 prepared.append(dict(scene=s.name,drop=drop,backshift=backshift,D=D,parts=records,controls=[dict(name=o.name,matrix_world=[list(x) for x in o.matrix_world],parent=o.parent.name if o.parent else None) for o in [root,lift,back]]))
 return root,lift,back
def capsule_mesh(name,p,q,r):
 p=Vector(p);q=Vector(q);axis=q-p;L=axis.length;rot=axis.to_track_quat('Z','Y').to_matrix() if L>1e-7 else Matrix.Identity(3);vs=[];fs=[];N=16;A=6
 for c,angles in [(0,np.linspace(-math.pi/2,0,A)),(L,np.linspace(0,math.pi/2,A))]:
  for ang in angles:
   for az in np.linspace(0,2*math.pi,N,endpoint=False):vs.append(p+rot@Vector((r*math.cos(ang)*math.cos(az),r*math.cos(ang)*math.sin(az),c+r*math.sin(ang))))
 for k in range(2*A-1):
  for j in range(N):fs.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);return me
def make_rig(s,seq,mat,name='MANIQUI'):
 bpy.context.window.scene=s;rest=seq[0]['body'];ad=bpy.data.armatures.new(s.name+'_'+name);rig=bpy.data.objects.new(ad.name,ad);s.collection.objects.link(rig);rig.matrix_world=M.copy();bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
 for part in rest['parts']:
  bone=ad.edit_bones.new(part['name']);bone.head=part['p'];bone.tail=part['q'] if (Vector(part['q'])-Vector(part['p'])).length>.0001 else Vector(part['p'])+Vector((0,0,.001));bone.use_deform=True
 bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True;objects=[]
 for part in rest['parts']:
  me=capsule_mesh(part['name'],part['p'],part['q'],part['r']);me.materials.append(mat);o=bpy.data.objects.new(s.name+'__'+part['name'],me);s.collection.objects.link(o);o.matrix_world=M.copy();group=o.vertex_groups.new(name=part['name']);group.add(list(range(len(me.vertices))),1.,'REPLACE');mod=o.modifiers.new('RIG_RIGIDO_ARTICULADO','ARMATURE');mod.object=rig;o['VOY04_ROLE']='MANNEQUIN';o['SEGMENT']=part['name'];o['RADIUS_M']=part['r'];o['HEIGHT_M']=rest['height'];objects.append(o)
 length_errors=[]
 for pose in seq:
  frame=pose['frame'];s.frame_set(frame)
  for part in pose['body']['parts']:
   pb=rig.pose.bones[part['name']];p=Vector(part['p']);q=Vector(part['q']);axis=q-p;L=axis.length;rot=axis.to_track_quat('Y','Z') if L>.0001 else Vector((0,0,1)).to_track_quat('Y','Z');target=rot.to_matrix().to_4x4();target.translation=p;pb.rotation_mode='QUATERNION';pb.matrix=target
   pb.keyframe_insert('location',frame=frame);pb.keyframe_insert('rotation_quaternion',frame=frame);pb.keyframe_insert('scale',frame=frame)
   if L>.0001:length_errors.append(abs(L-ad.bones[part['name']].length))
 rig['HEIGHT_M']=rest['height'];rig['VOY04_ROLE']='LAB_RIG';rigmeta.append(dict(scene=s.name,rig=rig.name,bones=len(ad.bones),frames=len(seq),maximum_segment_length_error_m=max(length_errors,default=0),initial_body=rest))
 assert max(length_errors,default=0)<.00002
 return rig,objects
def camera(s,name,at,aim,scale=2.8):
 cd=bpy.data.cameras.new(name);c=bpy.data.objects.new(name,cd);s.collection.objects.link(c);c.location=M@Vector(at);target=M@Vector(aim);c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=scale;cd.clip_start=.005;cd.clip_end=200;s.camera=c;return c
def shot(s,name,frame=1,at=(-2,-1.5,1.4),aim=(0,.1,.2),scale=2.8):
 bpy.context.window.scene=s;s.frame_set(frame);camera(s,name,at,aim,scale);s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=s.name);print('SHOT',name,flush=True)
ref=scene('01_REFERENCIA_INTACTA');refctx=copy_context(ref,True);camera(ref,'CAM_GENERAL',(-8,-10,9),(0,-1,.5),17)
prep=scene('02_SILLA_PILOTO_PIVOTES');prepctx=copy_context(prep);chair(prep,prepctx);camera(prep,'CAM_PIVOTES',(-1.5,-1.6,1.0),(0,0,.2),2.4)
orig_scenes=[];proto_scenes=[]
for seq,mat in zip(seqs,[blue,green,orange]):
 H=seq['H'];orig=scene(f'03_ORIGINAL_{H:.2f}');ctx=copy_context(orig);o=json.loads((R/'DATOS'/f'original_{H:.2f}.json').read_text());make_rig(orig,[dict(frame=1,body=o['body'])],red);camera(orig,'CAM_ORIGINAL',(2,0,.4),(0,.1,.1),2.3);orig_scenes.append(orig)
 s=scene(f'04_PROTO_{H:.2f}');ctx=copy_context(s);cfg=seq['config'];root,lift,back=chair(s,ctx,cfg['drop'],cfg['backshift'],cfg['D']);rig,parts=make_rig(s,seq['poses'],mat)
 for p in seq['poses']:
  root.location=P+T-Vector(nav['forward'])*p['state']['retreat'];root.keyframe_insert('location',frame=p['frame'])
 for frame,label in [(1,'SILLA_REFERENCIA'),(31,'SILLA_RETIRADA'),(61,'PRE_SENTADO'),(91,'SENTADO'),(121,'PUESTO'),(151,'TRABAJO'),(181,'RETIRAR_MANOS'),(211,'SILLA_ATRAS'),(241,'DE_PIE'),(271,'SALIDA'),(301,'RETORNO_SILLA')]:s.timeline_markers.new(label,frame=frame)
 camera(s,'CAM_PROTO',(-1.8,-1.4,1.2),(0,.0,.15),2.6);s.frame_set(151);proto_scenes.append(s);print('SCENE',s.name,len(s.objects),flush=True)
# Independent geometry data for every saved scene, including all reference copies.
for s in old:bpy.data.scenes.remove(s)
for o in list(bpy.data.objects):
 if not o.users_collection:bpy.data.objects.remove(o)
assert all(o.data.users==1 for s in scenes for o in s.objects if o.type=='MESH'), 'Unexpected shared mesh datablocks'
assert all(c['unchanged_initial'] for c in copies)
meta=dict(file=str(R/'ESCENAS/VOY04_Laboratorio.blend'),scenes=[s.name for s in scenes],source_count=len(geo),copies=copies,chairs=prepared,rigs=rigmeta,bridge_translation=list(T),station_matrix=[list(x) for x in M],proper_chair_matrix=[list(x) for x in Q],images=[dict(name=i.name,packed=bool(i.packed_file),path=i.filepath) for i in bpy.data.images])
(R/'DATOS/manifest_blender.json').write_text(json.dumps(meta,indent=2),encoding='utf8');bpy.context.preferences.filepaths.save_version=0;bpy.context.window.scene=proto_scenes[1]
for s in scenes:s.frame_set(151 if s in proto_scenes else 1)
bpy.ops.wm.save_as_mainfile(filepath=meta['file'],compress=True);print('SAVED',meta['file'],flush=True)
# Technical evidence uses real Blender geometry. No saving after render-only visibility changes.
shot(prep,'B01_PUESTO_PILOTO',1,(-1.6,-1.5,1.4),(0,.15,.2),2.8)
for i,s in enumerate(orig_scenes):shot(s,f'B02_ORIGINAL_FALLO_{seqs[i]["H"]:.2f}',1,(2,0,.25),(0,.0,.15),2.2)
for i,s in enumerate(proto_scenes):
 H=seqs[i]['H'];shot(s,f'B03_TRABAJO_{H:.2f}',151,(-1.7,-1.1,1.1),(0,.12,.18),2.25);shot(s,f'B04_PIERNAS_{H:.2f}',151,(2,0,.12),(0,.05,-.05),1.9)
for frame in [1,31,61,76,91,106,121,136,151,181,211,226,241,271,301]:shot(proto_scenes[1],f'C_SECUENCIA_{frame:03d}',frame,(-1.9,-1.3,1.25),(-.1,-.05,.1),2.8)
# Despiece on private copies of the 8 chair objects in a separate render-only scene.
expl=scene('TEMP_DESPIECE');ctx={}
for j,k in enumerate(nav['parts']):
 src=prepctx[k];o=src.copy();o.data=src.data.copy();o.parent=None;o.matrix_world=src.matrix_world.copy();o.location+=B@Vector(((j%4-1.5)*.85,(j//4)*1.0,0));expl.collection.objects.link(o);o.hide_render=False
shot(expl,'B05_DESPIECE_REAL',1,(-3,-5,4),(0,.5,.15),5.4)
# Axes are actual modeled rods, visible in the render (empties themselves do not render).
for ctrl in [o for o in prep.objects if o.type=='EMPTY']:
 p=ctrl.matrix_world.translation
 for axis,col in zip(range(3),[(1,.05,.05),(.05,1,.05),(.05,.25,1)]):
  q=p+ctrl.matrix_world.to_3x3().col[axis]*.23;me=capsule_mesh('PIVOT',p,q,.007);me.materials.append(material('EJE',col));o=bpy.data.objects.new('EJE_'+ctrl.name,me);prep.collection.objects.link(o)
shot(prep,'B06_PIVOTES_Y_CONTROLES',1,(-1.4,-1.2,.9),(0,0,.1),2.0)
# Short real frame sequence, 101 frames at 8 fps; package as animated image externally if available.
anim=proto_scenes[1];anim.render.resolution_x=900;anim.render.resolution_y=680;camera(anim,'CAM_ANIMACION',(-1.9,-1.3,1.25),(-.1,-.05,.1),2.8)
bpy.context.window.scene=anim
for frame in range(1,302,3):
 anim.frame_set(frame);bpy.context.view_layer.update();anim.render.filepath=str(R/'ANIMACIONES'/f'VOY04_{frame:03d}.png');bpy.ops.render.render(write_still=True,scene=anim.name)
print('EVIDENCIAS_TERMINADAS',flush=True)
