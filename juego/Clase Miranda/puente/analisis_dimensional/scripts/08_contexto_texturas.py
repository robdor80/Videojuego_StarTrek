"""Render contextual con las texturas existentes. No guarda el blend."""
import bpy,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.color_type='TEXTURE'
sc.render.resolution_x=1800;sc.render.resolution_y=1400;sc.render.resolution_percentage=100
sc.display.shading.show_shadows=False
for o in bpy.data.objects:
    if o.name.startswith('REF_'):
        m=bpy.data.materials.get('ANALISIS_'+str(tuple(o.color)))
        if m is None:m=bpy.data.materials.new('ANALISIS_'+str(tuple(o.color)));m.diffuse_color=o.color
        o.data.materials.append(m)
        o.hide_render=not o.name.startswith('REF_central_')
    if o.name.startswith('ANALISIS_') and o.type=='FONT':o.hide_render=True
roof=json.loads((ROOT/'datos/verificacion_en_memoria.json').read_text())['roof_hidden_for_inspection']
for n in roof:bpy.data.objects[n].hide_render=False
cam=sc.camera;cam.location=(0,-9.6,2.9);cam.rotation_euler=(Vector((0,-3.6,1.4))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=21
sc.render.filepath=str(ROOT/'capturas/08_contexto_texturas_originales.png');bpy.ops.render.render(write_still=True)
