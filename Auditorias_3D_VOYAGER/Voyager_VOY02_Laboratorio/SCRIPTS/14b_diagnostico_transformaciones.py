import bpy,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for label,path in [('cache','FUENTES/OBJ/puente_base_importado.blend'),('lab','ESCENAS/VOY02_Laboratorio.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(R/path),load_ui=False,use_scripts=False)
 for o in bpy.data.objects:
  if o.name in ['Plane_112','G_INTERIORES_CONECTADOS__Plane_112','Mesh13','PASILLO_PRINCIPAL','G_INTERIORES_CONECTADOS__Mesh_1987']:
   print(label,o.name,'matrix',[list(x) for x in o.matrix_world],'mesh_first',list(o.data.vertices[0].co),'world_first',list(o.matrix_world@o.data.vertices[0].co),flush=True)
