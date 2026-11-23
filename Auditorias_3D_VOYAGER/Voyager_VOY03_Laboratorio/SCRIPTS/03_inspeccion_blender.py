import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());T=Vector(proto['bridge_translation'])
bpy.ops.wm.open_mainfile(filepath=str(R/'REFERENCIAS/VOY02/VOY02_Laboratorio.blend'),load_ui=False,use_scripts=False)
s=bpy.data.scenes['G_INTERIORES_CONECTADOS'];bpy.context.window.scene=s;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1800;s.render.resolution_y=1300;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.view_settings.view_transform='Standard'
def cut():
 for o in list(s.objects):
  if o.type!='MESH' or o.get('VOY02_TIPO')!='GEOMETRIA_EXISTENTE_COPIADA':continue
  o.data=o.data.copy();bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,2.4+T.z),plane_no=(0,0,1),clear_outer=True);bm.transform(o.matrix_world.inverted());bm.to_mesh(o.data);bm.free()
def shot(name,at,aim,scale=None,only=None):
 hidden=[]
 for o in s.objects:
  if o.type=='FONT':o.hide_render=True
  if o.type=='MESH' and (not o.get('VOY02_ORIGEN','').startswith('OBJ:') or (only and o.get('VOY02_ORIGEN','')[4:] not in only)):
   if not o.hide_render:hidden.append(o);o.hide_render=True
 cd=bpy.data.cameras.new(name);cam=bpy.data.objects.new(name,cd);s.collection.objects.link(cam);s.camera=cam;cam.location=Vector(at)+T;cam.rotation_euler=(Vector(aim)+T-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO' if scale else 'PERSP';cd.ortho_scale=scale or 10;cd.lens=32;cd.clip_start=.005;cd.clip_end=1000;s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=s.name)
 for o in hidden:o.hide_render=False
 print('SHOT',name,flush=True)
cut();shot('A01_planta_original',(0,0,22),(0,0,0),17);shot('A02_escalera_derecha_contexto',(5.9,-1.9,2.7),(4.1,.1,.5));shot('A03_escalera_izquierda_contexto',(-5.9,-1.9,2.7),(-4.1,.1,.5));shot('A04_escalones_aislados',(6,-7,6),(0,-1.6,.4),11,{'Mesh_1856'});shot('A05_navegacion_escalones',(0,-.2,2.9),(0,-2.5,.2))
