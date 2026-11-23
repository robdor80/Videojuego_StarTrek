import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/'TEMP/obj_export.glb'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False;s.cycles.device='CPU';s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.world=bpy.data.worlds.new('Audit_World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.4,.4,.4,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;s.view_settings.view_transform='Standard'
for pos in [(0,0,6),(5,3,4),(-5,-3,4)]:
 bpy.ops.object.light_add(type='AREA',location=pos);l=bpy.context.object;l.data.energy=500;l.data.shape='DISK';l.data.size=5;l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();c=bpy.context.object;s.camera=c;c.data.clip_end=1000
manifest=[]
def shot(name,pos,target,ortho=0):
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO' if ortho else 'PERSP';c.data.ortho_scale=ortho or 12;c.data.lens=24;s.render.filepath=str(R/'CAPTURAS'/f'obj_texturizado_{name}.png');bpy.ops.render.render(write_still=True);manifest.append({'image':s.render.filepath,'camera':list(pos),'target':list(target),'materials':'original GLB shaders unchanged','lighting':'temporary neutral world .5 + 3 area lights 500 W; Standard; Cycles CPU 64 samples, no denoise','cut':name.startswith('corte')})
shot('interior', (0,-1,1.65),(0,5,1.5))
bpy.ops.object.light_add(type='POINT',location=(0,0,2.4));bpy.context.object.data.energy=180;bpy.context.object.data.shadow_soft_size=.3
shot('interior_luz_diagnostico',(0,-1,1.65),(0,5,1.5))
for o in list(s.objects):
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);high=[f for f in bm.faces if max((o.matrix_world@v.co).z for v in f.verts)>2.5];bmesh.ops.delete(bm,geom=high,context='FACES');bm.to_mesh(o.data);bm.free()
shot('corte_perspectiva',(10,-12,13),(0,0,1),17)
shot('corte_planta',(0,0,25),(0,0,0),16)
(R/'DATOS/capturas_obj_texturizado.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
