import bpy,json,hashlib
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SOURCE=Path(r'C:\Users\andro\ST_ORG_01_FASE_3C_09\2026-10-25_02-17-38\RECUPERACION\P-e4252915fcf5\Blender\Sutherland_PBR_Recovered.blend')
TARGET=R.parents[1]/'blender/Miranda_Puente_Sutherland_Ergonomia_03.blend'
def read(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
 out={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or not len(o.data.vertices):continue
  m=o.to_mesh();m.calc_loop_triangles()
  v=np.array([list(o.matrix_world@x.co) for x in m.vertices],dtype=np.float64)
  out[o.name]={'v':v,'tri':np.array([list(t.vertices) for t in m.loop_triangles]),'materials':[s.material.name if s.material else None for s in o.material_slots],'mi':[p.material_index for p in m.polygons],'polys':[list(p.vertices) for p in m.polygons],'uvhash':hashlib.sha256(b''.join(np.array([list(x.uv) for x in l.data],dtype=np.float32).tobytes() for l in m.uv_layers)).hexdigest(),'matrix':[list(x) for x in o.matrix_world]}
  o.to_mesh_clear()
 return out,{'system':bpy.context.scene.unit_settings.system,'scale':bpy.context.scene.unit_settings.scale_length}
old,ou=read(SOURCE);new,nu=read(TARGET);rows=[];arrays={}
for i,(name,b) in enumerate(new.items()):
 a=old.get(name);delta=float(np.linalg.norm(a['v']-b['v'],axis=1).max())*100 if a and a['v'].shape==b['v'].shape else None
 row={'name':name,'old_vertices':len(a['v']) if a else None,'vertices':len(b['v']),'delta_cm':delta,'old_materials':a['materials'] if a else None,'materials':b['materials'],'topology_equal':bool(a and a['polys']==b['polys']),'uv_equal':bool(a and a['uvhash']==b['uvhash']),'matrix_equal':bool(a and a['matrix']==b['matrix']),'old_bounds_cm':{'min':(a['v'].min(0)*100).tolist(),'max':(a['v'].max(0)*100).tolist()} if a else None,'bounds_cm':{'min':(b['v'].min(0)*100).tolist(),'max':(b['v'].max(0)*100).tolist()},'array':i}
 rows.append(row);arrays['v'+str(i)]=b['v'];arrays['tri'+str(i)]=b['tri']
result={'ok':True,'old':str(SOURCE),'target':str(TARGET),'old_units':ou,'target_units':nu,'old_count':len(old),'new_count':len(new),'removed':sorted(set(old)-set(new)),'objects':rows}
(R/'Data/blender_comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
np.savez_compressed(R/'Data/target_geometry.npz',**arrays)
print('BLENDER_AUDIT',len(old),len(new),'changed',[(r['name'],r['delta_cm']) for r in rows if r['delta_cm'] is None or r['delta_cm']>.001],flush=True)
