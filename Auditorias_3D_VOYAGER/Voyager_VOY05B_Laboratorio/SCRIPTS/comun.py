import bpy,json,hashlib,collections
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
def dump(name,data):
 p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf8')
def world(o):return np.array([o.matrix_world@v.co for v in o.data.vertices],float)
def setup(s,x=1200,y=1000):
 if not s.world:s.world=bpy.data.worlds.new('Diagnostico')
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=x;s.render.resolution_y=y;s.render.resolution_percentage=100
 s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=False;s.display.shading.background_type='WORLD';s.world.color=(.055,.065,.08);s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
def camera(s,c,d,span):
 m=bpy.data.cameras.new('CAM_DIAGNOSTICO');o=bpy.data.objects.new('CAM_DIAGNOSTICO',m);s.collection.objects.link(o);o.location=Vector(c)+Vector(d).normalized()*span*3;o.rotation_euler=(Vector(c)-o.location).to_track_quat('-Z','Y').to_euler();m.type='ORTHO';m.ortho_scale=span;m.clip_start=.001;m.clip_end=2000;s.camera=o;return o
def render(s,name,c,d,span):
 cam=camera(s,c,d,span);s.render.filepath=str(R/'CAPTURAS'/name);bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
def pack_images():
 out=[]
 for i in bpy.data.images:
  if i.source not in ['FILE','TILED']:continue
  if not i.packed_file:
   choices=list((R/'FUENTES/PUENTE').rglob(Path(i.filepath.replace('\\','/')).name))
   if choices:i.filepath=str(choices[0]);i.reload()
   if i.size[0]:i.pack()
  i.filepath='//TEXTURAS/'+Path(i.filepath.replace('\\','/')).name
  out.append(dict(name=i.name,packed=bool(i.packed_file),size=list(i.size),path=i.filepath))
 return out
