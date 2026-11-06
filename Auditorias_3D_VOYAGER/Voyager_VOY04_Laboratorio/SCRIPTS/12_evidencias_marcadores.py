import bpy,bmesh,ast,json,hashlib,math,sys,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
meta=json.loads((R/'DATOS/manifest_blender.json').read_text());seqs=json.loads((R/'DATOS/trayectorias.json').read_text());M=Matrix(meta['station_matrix']);P=Vector(json.loads((R/'DATOS/inventario_medidas.json').read_text())[0]['seat_point']);T=Vector(meta['bridge_translation']);B=M.to_3x3();scenes=[];rigmeta=[]
parsed=ast.parse((R/'SCRIPTS/08_blender.py').read_text());exec(compile(ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name in ['scene','camera','shot','material','capsule_mesh','make_rig','digest']],type_ignores=[]),'<VOY04_render_helpers>','exec'))
bpy.ops.wm.open_mainfile(filepath=meta['file'],load_ui=False,use_scripts=False);bpy.context.preferences.filepaths.save_version=0
if hasattr(bpy.context.preferences.edit,'keyframe_new_interpolation_type'):bpy.context.preferences.edit.keyframe_new_interpolation_type='LINEAR'
def state():
 out={}
 for sc in bpy.data.scenes:
  bpy.context.window.scene=sc;sc.frame_set(151 if sc.name.startswith('04_') else 1);bpy.context.view_layer.update()
  for ob in sc.objects:
   if ob.type=='MESH':out[ob.name]=(digest(ob.data),np.array(ob.matrix_world))
 return out
before=state()
marker_data=[]
for seq in seqs:
 s=bpy.data.scenes[f'04_PROTO_{seq["H"]:.2f}'];bpy.context.window.scene=s;s.frame_set(151);H=seq['H'];work=seq['poses'][150]['body'];approach=seq['poses'][60]['body'];pts={'APROXIMACION':np.mean([approach['joints']['ankle_-1'],approach['joints']['ankle_1']],axis=0)-[0,0,.045*H],'CADERA_SENTADA':work['joints']['hip'],'MANO_MENOS':work['joints']['hand_-1'],'MANO_MAS':work['joints']['hand_1'],'INTERACCION_CONSOLA':[-.01,.49,.2725]}
 for key,pt in pts.items():
  o=bpy.data.objects.new(s.name+'__ANCHOR_'+key,None);s.collection.objects.link(o);o.empty_display_type='ARROWS';o.empty_display_size=.09;o.location=M@Vector(pt);o['VOY04_ROLE']='FUTURE_INTERACTION_MARKER';o['USO']='Solo referencia geometrica; sin logica de juego';marker_data.append(dict(scene=s.name,key=key,local=list(pt),world=list(o.location),matrix=[list(r) for r in o.matrix_world]))
 cam=camera(s,s.name+'__CAMARA_AMPLIADA',(-.01,.49-.418*.95,.2725+.907*.95),(-.01,.49,.2725),1.3);cam.data.type='PERSP';cam.data.lens=32;cam['VOY04_ROLE']='FUTURE_CLOSEUP_CAMERA';marker_data.append(dict(scene=s.name,key='CAMARA_AMPLIADA',matrix=[list(r) for r in cam.matrix_world],lens_mm=32))
 # Restore the regular review camera as active.
 s.camera=next(o for o in s.objects if o.type=='CAMERA' and o.name.startswith('CAM_PROTO'))
after=state();maxmatrix=float(max(np.abs(before[k][1]-after[k][1]).max() for k in before));assert all(before[k][0]==after[k][0] for k in before) and maxmatrix<.00002,('Adding anchors changed geometry',maxmatrix)
(R/'DATOS/marcadores_interaccion.json').write_text(json.dumps(dict(markers=marker_data,mesh_state_equal_before_after=True),indent=2));bpy.context.window.scene=bpy.data.scenes['04_PROTO_1.75'];bpy.ops.wm.save_as_mainfile(filepath=meta['file'],compress=True);print('MARKERS_SAVED',len(marker_data),flush=True)
# Render-only cutaways: never write these cuts into the main laboratory.
navparts=set(json.loads((R/'DATOS/inventario_medidas.json').read_text())[0]['parts']);allowed=navparts|{'Mesh_1728','Object_75','Mesh_1856','Object_129','Object_126','Object_127','Plane_94','Plane_95','VOY04_GUIA_NUEVA','VOY04_CARRO_NUEVO'}
for seq in seqs:
 s=bpy.data.scenes[f'04_PROTO_{seq["H"]:.2f}'];bpy.context.window.scene=s;s.frame_set(151)
 for o in s.objects:
  if o.type!='MESH':continue
  key=o.get('SOURCE_KEY');o.hide_render=not (key in allowed or o.get('VOY04_ROLE')=='MANNEQUIN')
  if key in ['Object_129','Object_126','Object_127','Plane_94','Plane_95']:
   bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=M.translation,plane_no=B.col[0],clear_outer=True);bm.transform(o.matrix_world.inverted());bm.to_mesh(o.data);bm.free()
 shot(s,f'D01_SECCION_PIERNAS_{seq["H"]:.2f}',151,(2,-.12,.18),(0,.15,-.02),1.9)
# Make actual Blender snapshots of rejected poses. No animation evaluation can overwrite them.
red=material('FALLO_A1_A3',(.95,.035,.035));temps=[]
def snapshot_context(dest,source,frame,offset=(0,0,0),include=None):
 bpy.context.window.scene=source;source.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get()
 for o in source.objects:
  if o.type!='MESH' or o.get('VOY04_ROLE')=='MANNEQUIN':continue
  if include is not None and o.get('SOURCE_KEY') not in include:continue
  me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg);c=bpy.data.objects.new(dest.name+'_'+o.name,me);dest.collection.objects.link(c);c.matrix_world=o.matrix_world.copy();c.location+=B@Vector(offset);c.hide_render=False;c['VOY04_ROLE']='EVALUATED_SNAPSHOT'
source=bpy.data.scenes['04_PROTO_1.75']
for tag,file,frame in [('A1_GUIA','trayectorias_A1_FALLO_GUIA.json',56),('A3_MANOS','trayectorias_A3_FALLO_MANOS.json',146)]:
 raw=next(x for x in json.loads((R/'DATOS'/file).read_text()) if x['H']==1.75);pose=raw['poses'][frame-1];s=scene('FALLO_'+tag);snapshot_context(s,source,frame);make_rig(s,[dict(frame=1,body=pose['body'])],red);shot(s,'D02_FALLO_'+tag,1,(-1.7,-1.2,.9),(0,.0,.05),2.1);temps.append(s)
# Comparative seated silhouettes with actual chair geometry, stripped of occluding architecture.
comp=scene('COMPARACION_ALTURAS');colors=[material('ALTURA_160',(.05,.42,.95)),material('ALTURA_175',(.08,.75,.35)),material('ALTURA_190',(.95,.48,.06))]
for seq,col,offset in zip(seqs,colors,[(-1.1,0,0),(0,0,0),(1.1,0,0)]):
 src=bpy.data.scenes[f'04_PROTO_{seq["H"]:.2f}'];snapshot_context(comp,src,151,offset,navparts|{'VOY04_CARRO_NUEVO'});pose=seq['poses'][150];rig,parts=make_rig(comp,[dict(frame=1,body=pose['body'])],col,name='H'+str(seq['H']));rig.location+=B@Vector(offset)
 for o in parts:o.location+=B@Vector(offset)
shot(comp,'D03_COMPARACION_TRES_ALTURAS',1,(-2.8,-5,1.8),(0,0,.1),4.4);temps.append(comp)
# Source LCARS material evidence and real close-up using its original nodes/images.
s=bpy.data.scenes['02_SILLA_PILOTO_PIVOTES'];bpy.context.window.scene=s;s.frame_set(1);mats=[]
for name in ['scrn10_3','scrn10_4']:
 mat=bpy.data.materials.get(name)
 if mat:mats.append(dict(name=name,nodes=[dict(type=n.bl_idname,image=n.image.name if getattr(n,'image',None) else None) for n in mat.node_tree.nodes] if mat.use_nodes else [],diffuse=list(mat.diffuse_color)))
(R/'DATOS/materiales_lcars.json').write_text(json.dumps(mats,indent=2))
for o in s.objects:
 if o.type=='MESH':o.hide_render=o.get('SOURCE_KEY') not in {'Plane_94','Plane_95','Object_129','Mesh_2131'}
camera(s,'CAM_LCARS',(-.01,-.1,1.2),(-.01,.49,.27),1.25);s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1300;s.render.resolution_y=850
for at in [(-1,-1,2),(1,0,2)]:
 ld=bpy.data.lights.new('LUZ_INSPECCION','AREA');lo=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(lo);lo.location=M@Vector(at);lo.rotation_euler=(M@Vector((0,.4,.2))-lo.location).to_track_quat('-Z','Y').to_euler();ld.energy=250;ld.shape='DISK';ld.size=3
s.render.filepath=str(R/'CAPTURAS/D04_LCARS_ORIGINALES.png');bpy.ops.render.render(write_still=True,scene=s.name);print('LCARS_RENDERED',flush=True)
# Keep rejected poses reviewable in a separate file, together with a labelled comparative scene.
for sc in list(bpy.data.scenes):
 if sc not in temps:bpy.data.scenes.remove(sc)
bpy.context.window.scene=temps[0];bpy.ops.wm.save_as_mainfile(filepath=str(R/'ESCENAS/VOY04_Fallos_y_Comparativa.blend'),compress=True);print('EVIDENCE_SAVED',flush=True)
