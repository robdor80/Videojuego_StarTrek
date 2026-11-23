import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];path=R/'ESCENAS/VOY02_Laboratorio.blend'
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
labels={'NAVEGACION':'NAVEGACION / 8 PARTES','LATERAL_DER':'LATERAL DER / 31 PARTES','LATERAL_IZQ':'LATERAL IZQ / 31 PARTES','MANDO_IZQ':'MANDO IZQ / 11 PARTES','MANDO_DER':'MANDO DER / 11 PARTES'}
for o in bpy.data.scenes['E_SILLAS_GRUPOS'].objects:
 if o.type=='FONT':
  for key,label in labels.items():
   if o.name.startswith('LABEL_'+key):o.data.body=label;o.data.size=.18
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(path))
(R/'DATOS/leyendas_sillas.json').write_text(json.dumps(dict(only_font_bodies_and_sizes_changed=True,labels=labels,blend_sha256=hashlib.sha256(path.read_bytes()).hexdigest()),indent=2),encoding='utf8')
