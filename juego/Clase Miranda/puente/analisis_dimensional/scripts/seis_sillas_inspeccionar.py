"""Read-only inspection of the saved manual bridge, run with Blender --background."""
import bpy, json, os
from mathutils import Vector
from pathlib import Path

ROOT=Path(bpy.data.filepath).parent.parent/'analisis_dimensional'
def vec(v): return [round(float(x),7) for x in v]
rows=[]
for o in bpy.data.objects:
    corners=[o.matrix_world@Vector(v) for v in o.bound_box] if o.type=='MESH' else []
    rows.append(dict(name=o.name,type=o.type,data=o.data.name if o.data else None,
        parent=o.parent.name if o.parent else None,children=[x.name for x in o.children],
        collections=[c.name for c in o.users_collection],location=vec(o.location),
        rotation=vec(o.rotation_euler),scale=vec(o.scale),world=[vec(r) for r in o.matrix_world],
        dimensions=vec(o.dimensions),bounds=[[min(v[i] for v in corners) for i in range(3)],
        [max(v[i] for v in corners) for i in range(3)]] if corners else None,
        materials=[s.material.name if s.material else None for s in o.material_slots],
        vertices=len(o.data.vertices) if o.type=='MESH' else None,
        modifiers=[(m.name,m.type) for m in o.modifiers],constraints=[(c.name,c.type) for c in o.constraints],
        hidden=[o.hide_viewport,o.hide_render,o.hide_get()]))
result=dict(file=bpy.data.filepath,version=bpy.app.version_string,units=dict(system=bpy.context.scene.unit_settings.system,scale=bpy.context.scene.unit_settings.scale_length),
    objects=rows,collections=[dict(name=c.name,objects=[o.name for o in c.objects],children=[x.name for x in c.children],hide_viewport=c.hide_viewport,hide_render=c.hide_render) for c in bpy.data.collections],
    images=[dict(name=i.name,path=i.filepath,absolute=bpy.path.abspath(i.filepath),packed=bool(i.packed_file or len(i.packed_files)),exists=os.path.isfile(bpy.path.abspath(i.filepath))) for i in bpy.data.images])
out=ROOT/'datos'/'seis_sillas_inspeccion.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print('INSPECTION',out,'OBJECTS',len(rows),'VERSION',bpy.app.version_string)
