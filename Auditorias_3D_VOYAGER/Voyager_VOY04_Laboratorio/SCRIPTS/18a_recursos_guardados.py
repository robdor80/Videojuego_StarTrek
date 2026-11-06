import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def images():
 return {i.name:dict(packed=bool(i.packed_file),sha256=hashlib.sha256(i.packed_file.data).hexdigest() if i.packed_file else None,bytes=i.packed_file.size if i.packed_file else None) for i in bpy.data.images if i.name not in ['Render Result','Viewer Node']}
bpy.ops.wm.open_mainfile(filepath=str(R/'REFERENCIAS/VOY03_Circulacion.blend'),load_ui=False,use_scripts=False);before=images()
bpy.ops.wm.open_mainfile(filepath=str(R/'ESCENAS/VOY04_Laboratorio.blend'),load_ui=False,use_scripts=False);after=images();markers=[dict(scene=s.name,objects=[o.name for o in s.objects if o.get('VOY04_ROLE') in ['FUTURE_INTERACTION_MARKER','FUTURE_CLOSEUP_CAMERA']]) for s in bpy.data.scenes];passed=before==after and all(x['packed'] for x in after.values());out=dict(Blender=bpy.app.version_string,scenes=[s.name for s in bpy.data.scenes],reference_image_count=len(before),final_image_count=len(after),packed_bytes_SHA256_equal=passed,images=after,markers=markers)
(R/'DATOS/recursos_guardados.json').write_text(json.dumps(out,indent=2));print('PACKED_IMAGES',len(after),'EXACT_BYTE_HASH_EQUAL',passed,flush=True);assert passed;assert len(bpy.data.scenes)==8;assert sum(len(x['objects']) for x in markers)==18
