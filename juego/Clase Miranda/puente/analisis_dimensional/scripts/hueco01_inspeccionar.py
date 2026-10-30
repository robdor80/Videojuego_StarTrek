import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
from seis_sillas_comun import extra_snapshot
R=Path(__file__).resolve().parents[1]/'hueco_superior_01';R.mkdir(exist_ok=True)
source_mode=bpy.context.mode
if source_mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
def world(o):return [o.matrix_world@v.co for v in o.data.vertices]
original=R.parent.parent/'blender/Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_01.blend'
out={'source':str(original),'opened_copy':bpy.data.filepath,'saved_ui_mode':source_mode,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'objects':{}}
names=['Plane.004_0','Plane.039_0','Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0','Plane.011_0','Plane.021_0','Plane.038_0','Plane.034_0','Plane.020_0']
for n in names:
 o=bpy.data.objects[n];vs=world(o);out['objects'][n]={'world_vertices':[list(v) for v in vs],'faces':[{'index':p.index,'vertices':list(p.vertices),'material':p.material_index,'normal_world':list((o.matrix_world.to_3x3().inverted().transposed()@p.normal).normalized())} for p in o.data.polygons],'materials':[s.material.name if s.material else None for s in o.material_slots],'bounds':[[min(v[i] for v in vs) for i in range(3)],[max(v[i] for v in vs) for i in range(3)]],'matrix':[list(r) for r in o.matrix_world]}
out['snapshot']=extra_snapshot()
(R/'inspeccion.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('SOURCE',out['source_sha256'])
for n,r in out['objects'].items():print(n,'VERTS',len(r['world_vertices']),'FACES',len(r['faces']),'BOUNDS',r['bounds'])
