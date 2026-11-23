import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
rows=[]
for p in sorted((R/'FUENTES').glob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 images=[dict(name=i.name,packed=bool(i.packed_file),path=i.filepath,resolved=bpy.path.abspath(i.filepath),exists=Path(bpy.path.abspath(i.filepath)).is_file() if not i.packed_file else True) for i in bpy.data.images if i.source=='FILE']
 rows.append(dict(file=str(p.relative_to(R)),blender=bpy.app.version_string,scenes=[s.name for s in bpy.data.scenes],mesh_objects=len(meshes),polygons=sum(len(o.data.polygons) for o in meshes),images=images,read_ok=True))
(R/'VERIFICACION/parada_reapertura_copias.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps([dict(file=x['file'],read_ok=x['read_ok'],meshes=x['mesh_objects'],images_missing=sum(not i['exists'] for i in x['images'])) for x in rows],indent=2))
