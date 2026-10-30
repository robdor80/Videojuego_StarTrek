"""Bounded repair of the cabin-side upper frame. Never writes the input file."""
import bpy,json,sys,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
from seis_sillas_comun import extra_snapshot
R=Path(__file__).resolve().parents[1]/'hueco_superior_01'
audit=json.loads((R/'inspeccion.json').read_text(encoding='utf-8'));source=Path(audit['source'])
output=source.with_name('Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_Hueco_Cerrado_01.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)==audit['source_sha256'],'Source changed; inspect again'
assert sha(Path(bpy.data.filepath))==audit['source_sha256']
assert not output.exists(),'Output exists; verify instead of overwriting'
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
before=json.loads(json.dumps(extra_snapshot()))
assert before==audit['snapshot'],'Inspection mismatch'
o=bpy.data.objects['Plane.039_0'];inv=o.matrix_world.inverted()
door_top=max((d.matrix_world@v.co).z for name in ['Plane.018_0','Plane.019_0'] for d in [bpy.data.objects[name]] for v in d.data.vertices if (d.matrix_world@v.co).x<0)
# Preserve the imported frame's original bevel and side profile by translating
# all six levels of its inner header together, leaving the outer/top boundary.
old_header=min((o.matrix_world@v.co).z for v in o.data.vertices if 3.88<(o.matrix_world@v.co).z<3.89)
target=door_top+.0005;delta=target-old_header
changed=[]
for v in o.data.vertices:
    p=o.matrix_world@v.co
    if 3.75<p.z<3.93:
        old=list(p);p.z+=delta;v.co=inv@p;changed.append({'index':v.index,'before_world_m':old,'after_world_m':list(p)})
assert len(changed)==40,len(changed)
o.data.update();bpy.context.view_layer.update()
after=json.loads(json.dumps(extra_snapshot()))
object_diffs={n:{k:[before['objects'][n][k],v] for k,v in after['objects'][n].items() if before['objects'][n][k]!=v} for n in before['objects'] if before['objects'][n]!=after['objects'][n]}
if 'Plane.039_0' in object_diffs and set(object_diffs['Plane.039_0'])=={'dimensions'}:
    old,new=object_diffs['Plane.039_0']['dimensions'];assert max(abs(x-y) for x,y in zip(old,new))<2e-6
    del object_diffs['Plane.039_0']
assert not object_diffs,('Object properties changed',object_diffs)
assert before['materials']==after['materials'] and before['images']==after['images']
assert before['assignments_all']==after['assignments_all'] and before['collections']==after['collections']
assert before['image_paths']==after['image_paths'] and before['scene']==after['scene']
mesh=o.data.name
assert {k:v for k,v in before['meshes'].items() if k!=mesh}=={k:v for k,v in after['meshes'].items() if k!=mesh}
b=before['meshes'][mesh];a=after['meshes'][mesh]
differences=[k for k in b if b[k]!=a[k]]
assert set(differences)<={'co','attributes'},differences
assert [(n,d,t,h) for n,d,t,h in b['attributes'] if n!='position']==[(n,d,t,h) for n,d,t,h in a['attributes'] if n!='position']
manifest={'ok':True,'source':str(source),'source_sha256':sha(source),'output':str(output),'modified_objects':['Plane.039_0'],'created_objects':[],'modified_mesh':mesh,'changed_vertices':changed,'world_z_delta_m':delta,'door_top_m':door_top,'header_min_m':target,'clearance_m':.0005,'before_frame_geometry':b,'after_frame_geometry':a,'snapshot_after':after}
# Save before any temporary QA camera or render configuration is introduced.
bpy.ops.wm.save_as_mainfile(filepath=str(output),check_existing=True,relative_remap=False)
assert sha(source)==audit['source_sha256']
manifest['output_sha256']=sha(output)
(R/'reparacion_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print('REPAIR_SAVED',len(changed),'DELTA',delta,'BOTTOM',target,'OUTPUT',output,flush=True)
