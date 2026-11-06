import bpy,bmesh,ast,json,math,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];meta=json.loads((R/'DATOS/manifest_blender.json').read_text());M=Matrix(meta['station_matrix']);B=M.to_3x3();parsed=ast.parse((R/'SCRIPTS/08_blender.py').read_text());exec(compile(ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name in ['camera','shot']],type_ignores=[]),'<VOY04_camera>','exec'));bpy.ops.wm.open_mainfile(filepath=meta['file'],load_ui=False,use_scripts=False)
navparts=set(json.loads((R/'DATOS/inventario_medidas.json').read_text())[0]['parts']);allowed=navparts|{'Mesh_1728','Object_75','Object_129','Plane_94','Plane_95','VOY04_GUIA_NUEVA','VOY04_CARRO_NUEVO'}
for H in [1.6,1.75,1.9]:
 for prefix,frame,label in [('03_ORIGINAL',1,'ORIGINAL'),('04_PROTO',151,'ADAPTADO')]:
  s=bpy.data.scenes[f'{prefix}_{H:.2f}'];bpy.context.window.scene=s;s.frame_set(frame)
  for o in s.objects:
   if o.type!='MESH':continue
   key=o.get('SOURCE_KEY');o.hide_render=not (key in allowed or o.get('VOY04_ROLE')=='MANNEQUIN')
   if key in ['Object_129','Plane_94','Plane_95']:
    bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=M.translation,plane_no=B.col[0],clear_outer=True);bm.transform(o.matrix_world.inverted());bm.to_mesh(o.data);bm.free()
  shot(s,f'E_{label}_SECCION_{H:.2f}',frame,(2,-.12,.16),(0,.12,.02),2.1)
print('REVISION_VISUAL_TERMINADA',flush=True)
