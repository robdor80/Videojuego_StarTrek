import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'Data'
bpy.ops.wm.open_mainfile(filepath=str(R.parents[1]/'blender/Miranda_Puente_Sutherland_Ergonomia_03.blend'),load_ui=False)
before=json.loads((D/'ue_before.json').read_text());plan=json.loads((D/'export_meshes.json').read_text());split={x['actor_source']:x for x in plan['visual']}
refs={};excluded=[]
for a in before['actors']:
 if not a['label'].startswith('VIS_') or a['parent']:continue
 name=a['label'][4:];source=split[name]['source'] if name in split else name;o=bpy.data.objects[source];m=o.to_mesh();m.calc_loop_triangles();w=[o.matrix_world@v.co for v in m.vertices]
 if name!=source:
  pivot=a['location'][0];selected={i for i,v in enumerate(w) if (v.x>0)==(pivot>0)}
 elif source.startswith('Editable Mesh_Mat.') and name in split and len(w)==2*len(split[name]['expected_world_cm']):
  pivot=a['location'][0];selected={i for i,v in enumerate(w) if (v.x>0)==(pivot>0)}
 else:selected=set(range(len(w)))
 rows=[]
 for t in m.loop_triangles:
  if not all(i in selected for i in t.vertices):continue
  for vi,li in zip(t.vertices,t.loops):
   v=w[vi];uv=m.uv_layers[0].data[li].uv if m.uv_layers else None;rows.append({'p':[v.x*100,-v.y*100,v.z*100],'uv':list(uv) if uv is not None else None})
 refs[name]={'source':source,'points_cm':[[w[i].x*100,-w[i].y*100,w[i].z*100] for i in sorted(selected)],'corners':rows,'uv_layers':len(m.uv_layers),'source_vertices':len(selected),'source_triangles':len(rows)//3};o.to_mesh_clear()
assert len(refs)==79,len(refs)
(D/'resume_20261028_reference.json').write_text(json.dumps({'ok':True,'static_bridge_actors':refs,'source':bpy.data.filepath},separators=(',',':')),encoding='utf-8');print('REFERENCE_OK',len(refs),flush=True)
