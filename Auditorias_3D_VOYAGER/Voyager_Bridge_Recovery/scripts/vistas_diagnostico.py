"""Vistas geométricas temporales; no modifica objetos, materiales ni BLEND."""
from pathlib import Path
import json, math
import bpy
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'originales/Voyager_Bridge_MAX_Trabajo.blend'),use_scripts=False,load_ui=False)
bpy.context.view_layer.update()
r=json.loads((root/'informes/auditoria_voyager.json').read_text())
records={o['name']:o for o in r['objects']}
out=root/'informes/vistas';out.mkdir(exist_ok=True)
scene=bpy.data.scenes.new('AUDITORIA_TEMPORAL_NO_GUARDAR')
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.display.shading.light='STUDIO';scene.display.shading.color_type='SINGLE'
scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH';scene.display.shading.show_object_outline=True
scene.display.shading.background_type='WORLD';scene.world=bpy.data.worlds.get('World')
camdata=bpy.data.cameras.new('AUDITORIA_CAM_TEMP');cam=bpy.data.objects.new('AUDITORIA_CAM_TEMP',camdata)
scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO'

def view(name, names, direction, margin=1.15):
    for ob in list(scene.collection.objects):
        if ob!=cam:scene.collection.objects.unlink(ob)
    coords=[]
    for name_o in names:
        ob=bpy.data.objects.get(name_o)
        if ob is None or ob.type!='MESH' or not len(ob.data.vertices):continue
        scene.collection.objects.link(ob)
        parent=ob.parent
        while parent:
            if parent.name not in scene.collection.objects:scene.collection.objects.link(parent)
            parent=parent.parent
        coords.extend(ob.matrix_world@Vector(c) for c in ob.bound_box)
    lo=Vector([min(c[i] for c in coords) for i in range(3)])
    hi=Vector([max(c[i] for c in coords) for i in range(3)])
    center=(lo+hi)/2
    d=Vector(direction).normalized();cam.location=center+d*50
    cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    inv=cam.rotation_euler.to_matrix().transposed()
    proj=[inv@(p-center) for p in coords]
    width=max(p.x for p in proj)-min(p.x for p in proj)
    height=max(p.y for p in proj)-min(p.y for p in proj)
    camdata.ortho_scale=max(width,height*4/3)*margin
    scene.render.filepath=str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True,scene=scene.name)
    print('VISTA',name,len(names),flush=True)

max_names=[o['name'] for o in r['objects'] if o['type']=='MESH' and o['name']!='Voyager Bridge']
view('max_exterior',max_names,(1,-1,0.8))
low=[n for n in max_names if records[n]['mesh']['bounds_world'] and records[n]['mesh']['bounds_world']['max'][2]<2.5]
view('max_corte_inferior',low,(0,-0.4,1))
view('mesh468_planta',['Mesh468'],(0,0,1))
chair_names=sorted({a['object'] for m in r['materials'] if any(s in m['normalized_name'] for s in ['leather','fabric','chairgray']) for a in m['assignments'] if a['subset']!='legacy_OBJ'})
view('sillones_materiales',chair_names,(1,-1,0.65))
glow=sorted({a['object'] for m in r['materials'] if 'glow' in m['normalized_name'] or 'light floor' in m['normalized_name'] for a in m['assignments'] if a['subset']!='legacy_OBJ'})
view('paneles_glow',glow,(0,-0.4,1))
for label,needle in [('aluminio','brushed_aluminium'),('gris_dimgray','dimgray'),('metal_co','metal_co_metal_co'),('puertas','door')]:
    names=sorted({a['object'] for m in r['materials'] if needle in m['normalized_name'] for a in m['assignments'] if a['subset']!='legacy_OBJ'})
    if label=='puertas':names=sorted(set(names)|{'door01'}|{o['name'] for o in r['objects'] if o['parent'] and o['parent'].lower().startswith('door')})
    view(label,names,(1,-1,0.7))
view('barandillas',['Mesh1372','Mesh1373','Mesh1374','Mesh1375','Mesh1376',*[f'Mesh{i}' for i in range(1324,1333)],*[f'Mesh{i}' for i in range(1387,1404)]],(1,-1,0.7))
view('suelo_estructura',['Mesh566','Mesh468','floorfront','Mesh572','Mesh1500'],(0,-0.35,1))
(out/'grupos.json').write_text(json.dumps(dict(max=max_names,corte_inferior=low,sillones=chair_names,paneles_glow=glow),indent=2))
