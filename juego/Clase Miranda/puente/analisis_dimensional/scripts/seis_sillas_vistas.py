"""Temporary render-only views; never saves the blend or changes its persistent scene."""
import bpy, sys, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'capturas'/'seis_sillas';OUT.mkdir(exist_ok=True)
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.render.resolution_x=1500;sc.render.resolution_y=1100;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG'
sc.display.shading.light='STUDIO';sc.display.shading.color_type='MATERIAL'
sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True
sc.display.shading.cavity_type='BOTH';sc.display.shading.background_type='WORLD'
sc.world.color=(.12,.12,.12);sc.view_settings.view_transform='Standard'
cd=bpy.data.cameras.new('QA_TEMP');cam=bpy.data.objects.new('QA_TEMP',cd)
sc.collection.objects.link(cam);sc.camera=cam
def render(name,eye,target,ortho=None):
    cam.location=eye;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    cd.type='ORTHO' if ortho else 'PERSP';cd.ortho_scale=ortho or 10;cd.lens=30
    sc.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
base='Seis_Sillas_01' if 'Seis_Sillas_01' in bpy.data.filepath else 'Original'
meshes=[o for o in sc.objects if o.type=='MESH']
visible={o.name: not o.hide_render for o in meshes}
master=[o.name for o in meshes if o.name.endswith('_0.002') and o.name.startswith('Mesh.')]+['Cilindro','Floor_aiWireframe1_0']
for o in meshes:o.hide_render=o.name not in master
render(base+'_maestra.png',(7.2,-8.1,2.1),(4.65,-5.5,.75),2.5)
for o in meshes:o.hide_render=not visible[o.name]
render(base+'_lateral_Xpos.png',(2.7,-7.3,2.05),(5.1,-3.65,.9))
render(base+'_lateral_Xneg.png',(-2.7,-.2,2.05),(-5.1,-3.65,.9))
if base!='Original' and '--pbr' in sys.argv:
    # All lighting/render edits below are transient; this script never saves a blend.
    sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=True
    sc.render.resolution_x=1200;sc.render.resolution_y=900
    sc.world.use_nodes=True
    for n in sc.world.node_tree.nodes:
        if n.type=='BACKGROUND':n.inputs['Color'].default_value=(.35,.4,.5,1);n.inputs['Strength'].default_value=.4
    for name,loc,energy,size in [('QA_LIGHT_A',(2,-5,3.2),450,4),('QA_LIGHT_B',(-2,-3,3.2),450,4)]:
        light=bpy.data.lights.new(name,'AREA');light.energy=energy;light.shape='DISK';light.size=size
        ob=bpy.data.objects.new(name,light);sc.collection.objects.link(ob);ob.location=loc
    render(base+'_PBR_Xpos.png',(2.7,-7.3,2.05),(5.1,-3.65,.9))
    render(base+'_PBR_Xneg.png',(-2.7,-.2,2.05),(-5.1,-3.65,.9))
# Isolated floor component shows which sliding grooves are actually in the installed platform.
if base=='Original':
    for o in meshes:o.hide_render=o.name!='Floor_aiWireframe1_0'
    render('Original_plataforma.png',(5.4,-6.4,.8),(4.68,-5.51,.01),1)
    for o in meshes:o.hide_render=o.name not in ['FloorRail01_aiWireframe1_0','FloorRail02_aiWireframe1_0']
    render('Original_railes_sin_colocar.png',(2.8,-3,2.4),(0,0,.2),3.2)
