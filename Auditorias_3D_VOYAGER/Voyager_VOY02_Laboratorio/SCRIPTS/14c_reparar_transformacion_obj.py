"""Repair only derived scene datablocks: restore measured OBJ import basis once per mesh."""
import bpy,json,hashlib,shutil
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];path=R/'ESCENAS/VOY02_Laboratorio.blend'
bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/OBJ/puente_base_importado.blend'),load_ui=False,use_scripts=False)
basis={o.name:o.matrix_world.copy() for o in bpy.context.scene.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
if bpy.context.scene.get('VOY02_BASE_OBJ_CORREGIDA'):raise RuntimeError('Already repaired; refusing double basis transform')
backup=R/'TRASPASO/VOY02_Laboratorio_ANTES_CORRECCION_OBJ.blend'
assert not backup.exists(),'Preserve existing backup; do not repeat repair'
shutil.copy2(path,backup);before=hashlib.sha256(path.read_bytes()).hexdigest();assert hashlib.sha256(backup.read_bytes()).hexdigest()==before
done={};rows=[]
for o in bpy.data.objects:
 source=o.get('VOY02_ORIGEN','')
 if o.type!='MESH' or not source.startswith('OBJ:'):continue
 name=source[4:];me=o.data
 if me.as_pointer() in done:continue
 assert name in basis,name
 me.transform(basis[name]);me.update();done[me.as_pointer()]=name
 rows.append(dict(mesh=me.name,source=name,basis=[list(x) for x in basis[name]],vertices=len(me.vertices)))
# Optional empty factory scene is not one of the eight authored scenes.
for s in list(bpy.data.scenes):
 if s.name=='Scene' and len(s.objects)==0:bpy.data.scenes.remove(s)
for s in bpy.data.scenes:s['VOY02_BASE_OBJ_CORREGIDA']=True
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(path))
out=dict(reason='11_construir_escenas.py reset OBJ template matrix to identity and omitted its +90deg X import basis. Numerical NPZ already had the correct world basis; only saved laboratory meshes repaired.',backup=str(backup),before_sha256=before,after_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),shared_datablocks_transformed=len(rows),meshes=rows,source_files_modified=False)
(R/'DATOS/correccion_base_obj.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8');print('REPAIRED_OBJ_BASIS',len(rows),flush=True)
