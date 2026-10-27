import bpy, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=1600; sc.render.resolution_y=1400;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG'
sc.display.shading.light='STUDIO';sc.display.shading.studiolight_rotate_z=0.4
sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=True
sc.display.shading.show_cavity=True;sc.display.shading.cavity_type='BOTH'
sc.display.shading.background_type='WORLD';sc.world.color=(0.12,0.12,0.12)
sc.view_settings.view_transform='Standard'
camdata=bpy.data.cameras.new('ANALISIS_CAM');cam=bpy.data.objects.new('ANALISIS_CAM',camdata);sc.collection.objects.link(cam);sc.camera=cam
for o in sc.objects:
    if o.type=='MESH':
        zmin=min((o.matrix_world@Vector(c)).z for c in o.bound_box)
        if zmin>3.8:o.hide_render=True
def render(name,eye,target,ortho=None):
    cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    camdata.type='ORTHO' if ortho else 'PERSP';camdata.ortho_scale=ortho or 20;camdata.lens=24
    sc.render.filepath=str(ROOT/'capturas'/name);bpy.ops.render.render(write_still=True)
render('00_previa_cenital.png',(-2,-4,24),(-2,-4,0),20)
render('00_previa_interior.png',(0,-7.8,2.7),(0,0,1.6))
render('00_previa_turbo.png',(-7,-7,3),(-8.2,-8.8,1.7))
