import bpy,json,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];TARGET=R.parent/'blender/Miranda_Puente_Sutherland_Ergonomia_04.blend'
bpy.ops.wm.open_mainfile(filepath=str(TARGET),load_ui=False)
old=json.loads((R.parent/'unreal/Sutherland_Ergonomia03_ParteA/Data/blender_comparison.json').read_text())
old={r['name']:r['bounds_cm'] for r in old['objects']}
def bounds(o):
 a=np.array([list(o.matrix_world@v.co) for v in o.data.vertices])*100
 return {'min':a.min(0).tolist(),'max':a.max(0).tolist(),'dimensions':np.ptp(a,axis=0).tolist()}
out={'ok':False,'file':bpy.data.filepath,'object_count':len(bpy.data.objects),'relevant':{},'blue_materials':{},'chair_mesh_names':[]}
for o in bpy.context.scene.objects:
 if o.type!='MESH' or not len(o.data.vertices):continue
 if o.name.startswith('Editable Mesh_Mat.') or o.name in ['Sphere.001_0','Cylinder_0','Plane.032_0','Plane.025_0','Plane.023_0']:
  out['relevant'][o.name]={'bounds_cm':bounds(o),'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'materials':[s.material.name if s.material else None for s in o.material_slots]}
 if o.name.startswith('Mesh.') and o.name!='Mesh.453_0':out['chair_mesh_names'].append(o.name)
cap=out['relevant']['Sphere.001_0']['bounds_cm']['dimensions'];cyl=out['relevant']['Cylinder_0']['bounds_cm']['dimensions']
out['captain_dimension_ratio_vs_03']=[cap[i]/(old['Sphere.001_0']['max'][i]-old['Sphere.001_0']['min'][i]) for i in range(3)]
out['cylinder_dimension_ratio_vs_03']=[cyl[i]/(old['Cylinder_0']['max'][i]-old['Cylinder_0']['min'][i]) for i in range(3)]
out['lcars_delta_vs_03_cm']={n:[out['relevant'][n]['bounds_cm']['min'][2]-old[n]['min'][2],out['relevant'][n]['bounds_cm']['max'][2]-old[n]['max'][2]] for n in ['Plane.032_0','Plane.025_0','Plane.023_0']}
for n in ['BLUE','light.001']:
 m=bpy.data.materials.get(n)
 if m and m.node_tree:out['blue_materials'][n]=[{'node':q.type,'inputs':{s.name:list(s.default_value) if hasattr(s.default_value,'__len__') else s.default_value for s in q.inputs if hasattr(s,'default_value')}} for q in m.node_tree.nodes if q.type=='EMISSION']
parts=[out['relevant'][n] for n in ['Editable Mesh_Mat.003_0','Editable Mesh_Mat.003_0.001']]
top=out['relevant']['Editable Mesh_Mat.005_0']['bounds_cm']['max'][2]
blue=bpy.data.materials['BLUE'];bar=bpy.data.objects['Editable Mesh_Mat.004_0']
out['checks']={
 'captain_reduced_15_percent':all(abs(x-.85)<.0001 for x in out['captain_dimension_ratio_vs_03']),
 'cylinder_narrowed_15_percent_height_preserved':all(abs(x-.85)<.0001 for x in out['cylinder_dimension_ratio_vs_03'][:2]) and abs(out['cylinder_dimension_ratio_vs_03'][2]-1)<.0001,
 'lcars_lowered':all(v<-29.99 for delta in out['lcars_delta_vs_03_cm'].values() for v in delta),
 'lower_parts_separate_and_adjusted':all(p['vertices']==32 and p['faces']==16 and abs(p['bounds_cm']['max'][2]-top)<.001 for p in parts) and parts[0]['bounds_cm']['max'][0]<0<parts[1]['bounds_cm']['min'][0],
 'blue_bar_both_sides':any((bar.matrix_world@v.co).x<0 for v in bar.data.vertices) and any((bar.matrix_world@v.co).x>0 for v in bar.data.vertices),
 'blue_emission_linked_to_image':any(n.type=='EMISSION' and n.inputs['Strength'].default_value>0 and n.inputs['Color'].is_linked and n.inputs['Color'].links[0].from_node.type=='TEX_IMAGE' for n in blue.node_tree.nodes),
 'six_lateral_chairs_96_parts':len(out['chair_mesh_names'])==96}
out['ok']=all(out['checks'].values())
(R/'datos/pbr01_preflight.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False),flush=True)
