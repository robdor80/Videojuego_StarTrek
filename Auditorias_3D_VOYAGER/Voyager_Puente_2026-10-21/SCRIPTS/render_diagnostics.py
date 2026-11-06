import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];args=sys.argv[sys.argv.index('--')+1:];label=args[0]
if label=='glb':
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/'TEMP/collection.glb'))
else:bpy.ops.wm.open_mainfile(filepath=str(R/'TEMP'/('collection.blend' if label=='blend' else 'recovery.blend')),load_ui=False,use_scripts=False)
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=1500;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.display.shading.light='STUDIO';scene.display.shading.studio_light='paint.sl';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=False
scene.display.shading.background_type='WORLD'
if scene.world is None:scene.world=bpy.data.worlds.new('AuditWorld')
scene.world.color=(0.08,0.08,0.08)
scene.view_settings.view_transform='Standard'
bpy.ops.object.camera_add();cam=bpy.context.object;scene.camera=cam
meshes=[o for o in scene.objects if o.type=='MESH'];manifest=[]
def render(name,predicate,direction,ortho=True,exclude=None):
 selected=[o for o in meshes if predicate(o) and (not exclude or not exclude(o))]
 if not selected:return
 for o in meshes:o.hide_render=o not in selected
 pts=[o.matrix_world@Vector(v) for o in selected for v in o.bound_box];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)/2
 radius=max((p-center).length for p in pts);cam.location=center+Vector(direction).normalized()*radius*3;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO' if ortho else 'PERSP';cam.data.ortho_scale=radius*2.1;cam.data.lens=45;cam.data.clip_end=10000
 scene.render.filepath=str(R/'CAPTURAS'/f'{label}_{name}.png');bpy.ops.render.render(write_still=True)
 manifest.append({'image':scene.render.filepath,'objects':[o.name for o in selected],'camera':list(cam.location),'target':list(center),'engine':scene.render.engine,'method':'studio material diffuse; geometry unchanged; subset isolated; no texture generated'})
def ancestor(o,s):
 while o:
  if o.name.startswith(s):return True
  o=o.parent
 return False
if label in ['glb','blend']:
 bridge=lambda o:ancestor(o,'Group_52_1')
 render('01_catalogo_superior',lambda o:True,(0,0,1))
 render('02_puente_completo',bridge,(1,-1,0.85))
 render('03_puente_superior',bridge,(0,0,1))
 render('04_puente_lateral',bridge,(-1,0,0.35))
 render('05_puente_mobiliario_aislado',bridge,(1,-1,0.8),exclude=lambda o:ancestor(o,'Group_43_1') or ancestor(o,'Group_44_1') or o.name.startswith('Mesh105') or o.name=='Object_108')
 render('06_pasillos',lambda o: ('Hallway' in o.name or 'Corridor' in o.name) if label=='blend' else any(ancestor(o,s) for s in ['Hallway','Corridor']),(1,-1,1)) if label=='glb' else render('06_pasillos',lambda o:any(ancestor(o,s) for s in ['Hallway','Corridor']),(1,-1,1))
 render('07_turbolift',lambda o:ancestor(o,'Turbolift1'),(1,-1,0.65))
 render('08_puerta_marco',lambda o:ancestor(o,'Recessed_Large_Cargo_Type_Door1') or ancestor(o,'Recessed_large_Door_Edge1'),(-1,-1,0.4))
 # Isolate principal architecture, then discard only high faces on temporary copies.
 relevant=[o for o in meshes if bridge(o) and not (o.name.startswith('Mesh105') or o.name=='Object_108')]
 for o in relevant:
  o.data=o.data.copy()
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data)
  high=[f for f in bm.faces if max((o.matrix_world@v.co).z for v in f.verts)>2.5]
  bmesh.ops.delete(bm,geom=high,context='FACES');bm.to_mesh(o.data);bm.free()
 render('09_puente_corte_z250',lambda o:o in relevant,(1,-1,0.9))
 render('10_puente_corte_planta',lambda o:o in relevant,(0,0,1))
 for i in range(1,12):
  render(f'grupo_{i:02}',lambda o,i=i:ancestor(o,f'Group{i}_') if label=='glb' else o.parent and o.parent.name==f'Group{i}',(1,-1,0.8))
else:
 principal=lambda o:o.name!='Voyager Bridge' and (o.matrix_world.translation-Vector((0,0,2))).length<13
 render('01_completo',principal,(1,-1,0.8))
 render('02_superior',principal,(0,0,1))
 for o in meshes:
  if not principal(o):continue
  o.data=o.data.copy()
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data)
  high=[f for f in bm.faces if max((o.matrix_world@v.co).z for v in f.verts)>2.6]
  bmesh.ops.delete(bm,geom=high,context='FACES');bm.to_mesh(o.data);bm.free()
 render('03_corte_z260',principal,(1,-1,0.8))
 render('04_corte_planta',principal,(0,0,1))
 render('05_sillones',lambda o:o.name in ['Armrest01','Armrest02','Armrest03','Armrest04','Box001','Box003','Box004','Box005'],(1,-1,0.6))
 render('06_consolas',lambda o:o.name in ['Mesh1114','Mesh1119','Mesh1127','Mesh1133','Mesh1340','Mesh1717','Plane083','Plane084'],(1,-1,0.7))
 render('07_puertas',lambda o:ancestor(o,'door3') or ancestor(o,'door4') or ancestor(o,'door04') or ancestor(o,'door05') or ancestor(o,'door06') or ancestor(o,'door07'),(1,-1,0.7))
(R/'DATOS'/f'capturas_{label}.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
