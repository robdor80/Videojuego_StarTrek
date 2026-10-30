"""Transient Workbench QA; no file saves, no PBR or scene edits persisted."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]/'hueco_superior_01';D=R/'capturas';D.mkdir(exist_ok=True)
tag='Reparado' if 'Hueco_Cerrado' in bpy.data.filepath else 'Antes'
sc=bpy.context.scene
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1200;sc.render.resolution_y=1200;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='Standard'
shade=sc.display.shading;shade.light='STUDIO';shade.studiolight_rotate_z=math.radians(25);shade.color_type='OBJECT';shade.show_shadows=True;shade.show_cavity=True;shade.cavity_type='BOTH';shade.show_backface_culling=True;shade.background_type='VIEWPORT';shade.background_color=(.08,.08,.08)
for o in sc.objects:
 if o.type=='MESH':o.color=(.48,.48,.48,1)
bpy.data.objects['Plane.039_0'].color=(.30,.46,.60,1)
cd=bpy.data.cameras.new('QA_Hueco_TEMP');cam=bpy.data.objects.new('QA_Hueco_TEMP',cd);sc.collection.objects.link(cam);sc.camera=cam;cd.type='ORTHO';cd.ortho_scale=3.5
for side,eye,target in [('Puente',(-3.7,-7.9,3.5),(-5.8,-8.34,3.0)),('Cabina',(-8.25,-8.85,3.6),(-5.95,-8.33,3.0))]:
 cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(D/(tag+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
print('QA_VIEWS',tag)
