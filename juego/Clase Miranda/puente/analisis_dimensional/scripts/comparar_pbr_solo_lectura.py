"""Bounded read-only inspection: three material sources and Ergonomia_04.
Never saves Blender data, changes a node/material, renders, or exports geometry.
"""
import bpy,json,hashlib,collections,re
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
F=REPO/'TABULA RASA COPIA SEGURIDAD/01_TEXTURAS_PBR_SUTHERLAND/DERIVADOS_EXISTENTES/Blender_Integracion_Final'
REC=Path(r'C:\Users\andro\ST_ORG_01_FASE_3C_09\2026-10-25_02-17-38\RECUPERACION\P-e4252915fcf5\Blender')
LAB=REPO/'assets/ships/starfleet/bridges/USS Suntherland/Sutherland_PBR_Lab_v01.blend'
candidates=[LAB,Path(str(LAB)+'1'),REC/'VisualSource/Sutherland_PBR_Lab_v01.blend',REC/'VisualSource/Sutherland_PBR_Lab_v01.blend1',REC/'Sutherland_PBR_Recovered.blend',F/'Referencia_Visual02.blend',F/'Sutherland_Definitivo_20261025.blend',F/'Sutherland_Definitivo_Recuperado.blend']
TARGET=R.parent/'blender/Miranda_Puente_Sutherland_Ergonomia_04.blend'
chosen={'lab_v01':LAB,'visual02':F/'Referencia_Visual02.blend','final_recuperado':F/'Sutherland_Definitivo_Recuperado.blend'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def val(x):
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 try:return list(x)
 except:return str(x)
control={str(p):sha(p) for p in candidates+[TARGET] if p.is_file()}
# The existing channel index names only 13 bounded PBR folders. No disk search.
channels=json.loads((REPO/'TABULA RASA COPIA SEGURIDAD/07_INFORMES_Y_VERIFICACION/texturas_pbr_canales.json').read_text())
external_index=collections.defaultdict(list)
library_roots=[REPO/'TABULA RASA COPIA SEGURIDAD/01_TEXTURAS_PBR_SUTHERLAND/ORIGINALES_DESCARGADOS/Sutherland_PBR_Lab',F/'PBRSource']
for entry in channels:
 folder=Path(entry['folder'])
 names=set(n for ns in entry['maps_available'].values() for n in ns)|set(entry['other_images_or_previews'])
 for root in library_roots:
  for n in names:
   p=root/folder/n
   if p.is_file():external_index[n.lower()].append(str(p))
for root in [F/'RecoveredTextures',F.parent/'Exports_Textures']:
 if root.is_dir():
  for p in root.iterdir():
   if p.is_file():external_index[p.name.lower()].append(str(p))
def reachable(tree,seen=None):
 seen=seen or set();nodes=set();outputs=[n for n in tree.nodes if n.type in ['OUTPUT_MATERIAL','GROUP_OUTPUT'] and getattr(n,'is_active_output',True)]
 def visit(n):
  if n in nodes:return
  nodes.add(n)
  for socket in n.inputs:
   for link in socket.links:visit(link.from_node)
 for n in outputs:visit(n)
 return nodes
def image_info(im):
 packed=list(im.packed_files) if hasattr(im,'packed_files') else []
 embedded=bool(im.packed_file or packed);path=Path(bpy.path.abspath(im.filepath)) if im.filepath else None
 name=Path(im.filepath.replace('\\','/')).name if im.filepath else im.name
 return {'name':im.name,'path':im.filepath,'resolved_path':str(path) if path else None,'external_exists':bool(path and path.is_file()),'packed':embedded,'packed_bytes':sum(p.packed_file.size for p in packed) if packed else (im.packed_file.size if im.packed_file else 0),'size':list(im.size),'source':im.source,'colorspace':im.colorspace_settings.name,'known_recovery_paths':external_index.get(name.lower(),[])}
def inspect(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False);objects={};usage=collections.defaultdict(dict)
 for o in bpy.context.scene.objects:
  if o.type!='MESH' or not len(o.data.vertices):continue
  m=o.data;counts=collections.Counter(p.material_index for p in m.polygons)
  mats=[s.material.name if s.material else None for s in o.material_slots]
  for i,count in counts.items():
   if i<len(mats) and mats[i]:usage[mats[i]][o.name]=count
  uv=[]
  for l in m.uv_layers:
   a=np.empty(len(l.data)*2,dtype=np.float32);l.data.foreach_get('uv',a);uv.append({'name':l.name,'hash':hashlib.sha256(a.tobytes()).hexdigest()})
  objects[o.name]={'vertices':len(m.vertices),'faces':len(m.polygons),'topology':digest([list(p.vertices) for p in m.polygons]),'uv':uv,'uv_render':[l.name for l in m.uv_layers if l.active_render],'materials':mats,'used_materials':{mats[i]:n for i,n in counts.items() if i<len(mats) and mats[i]},'attributes':[(a.name,a.data_type,a.domain) for a in m.attributes if not a.name.startswith('.')],'parent':o.parent.name if o.parent else None,'modifiers':[{'name':x.name,'type':x.type,'viewport':x.show_viewport,'render':x.show_render} for x in o.modifiers]}
 materials={};images={}
 for name,users in usage.items():
  m=bpy.data.materials[name];props={'name':name,'objects':users,'node_types':{},'shader_inputs':[],'mapping':[],'images':[],'uv_maps':[],'coordinate_outputs':[],'groups':[],'procedural_nodes':[],'light_path':False};records=[];groups_seen=set()
  def tree_info(tree,prefix=''):
   nodes=reachable(tree);props['node_types'].update(dict(collections.Counter(n.type for n in nodes)))
   for n in sorted(nodes,key=lambda n:n.name):
    row={'path':prefix+n.name,'type':n.bl_idname,'inputs':{s.name:val(s.default_value) for s in n.inputs if hasattr(s,'default_value')},'links':[(s.name,l.from_node.name,l.from_socket.name) for s in n.inputs for l in s.links]}
    for k in ['operation','blend_type','vector_type','interpolation','extension','projection','uv_map','attribute_name']:
     if hasattr(n,k):row[k]=val(getattr(n,k))
    if n.type=='TEX_IMAGE' and n.image:
     im=n.image;images[im.name]=image_info(im);props['images'].append(im.name);row['image']=im.name
    if n.type in ['BSDF_PRINCIPLED','EMISSION','MIX_SHADER','BSDF_TRANSPARENT']:props['shader_inputs'].append(row)
    if n.type=='MAPPING':props['mapping'].append(row)
    if n.type=='UVMAP':props['uv_maps'].append(n.uv_map)
    if n.type=='TEX_COORD':props['coordinate_outputs'].extend(s.name for s in n.outputs if s.is_linked)
    if n.type=='LIGHT_PATH':props['light_path']=True
    if n.type.startswith('TEX_') and n.type not in ['TEX_IMAGE','TEX_COORD']:props['procedural_nodes'].append(n.type)
    if n.type=='VALTORGB':row['ramp']=[{'position':e.position,'color':list(e.color)} for e in n.color_ramp.elements]
    if n.type=='GROUP' and n.node_tree and n.node_tree.name not in groups_seen:
     groups_seen.add(n.node_tree.name);props['groups'].append(n.node_tree.name);tree_info(n.node_tree,prefix+n.node_tree.name+'/')
    records.append(row)
  if m.use_nodes and m.node_tree:tree_info(m.node_tree)
  props['graph_hash']=digest(records);props['images']=sorted(set(props['images']));props['uv_maps']=sorted(set(props['uv_maps']));props['coordinate_outputs']=sorted(set(props['coordinate_outputs']));materials[name]=props
 return {'path':str(path),'objects':objects,'materials':materials,'images':images,'unused_material_names':[m.name for m in bpy.data.materials if m.name not in usage],'library_dependencies':[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries]}
all_data={k:inspect(p) for k,p in chosen.items()};target=inspect(TARGET);comparisons={}
for key,src in all_data.items():
 common=set(src['objects'])&set(target['objects']);same=[];uv_same=[];needs=[];merged=[]
 for n in sorted(common):
  a,b=src['objects'][n],target['objects'][n]
  if a['topology']==b['topology'] and a['vertices']==b['vertices']:
   same.append(n)
   if a['uv']==b['uv'] and a['uv_render']==b['uv_render']:uv_same.append(n)
   else:needs.append({'object':n,'reason':'UV layers differ','source_uv':[u['name'] for u in a['uv']],'target_uv':[u['name'] for u in b['uv']]})
  else:
   pair=[x for x in src['objects'] if x==n or x.startswith(n+'.')]
   if n.startswith('Editable Mesh_Mat.') and len(pair)==2 and sum(src['objects'][x]['vertices'] for x in pair)==b['vertices'] and sum(src['objects'][x]['faces'] for x in pair)==b['faces']:merged.append({'target':n,'source_parts':pair})
   else:needs.append({'object':n,'reason':'Topology differs'})
 comparisons[key]={'common_objects':len(common),'same_topology':same,'same_uv_and_topology':uv_same,'needs_adaptation':needs,'merged_console_parts':merged,'missing_used_images':[im for im in src['images'].values() if not im['packed'] and not im['external_exists']],'materials_changed_vs_visual02':[n for n in src['materials'] if n in all_data['visual02']['materials'] and src['materials'][n]['graph_hash']!=all_data['visual02']['materials'][n]['graph_hash']]}
out={'ok':True,'candidate_paths':[{'path':str(p),'exists':p.is_file(),'sha256':control.get(str(p)),'mtime':p.stat().st_mtime if p.is_file() else None} for p in candidates],'sources':all_data,'target':target,'comparison':comparisons,'files_unchanged':all(sha(Path(p))==h for p,h in control.items()),'inspected_sources':len(chosen)}
assert out['files_unchanged'];dest=R/'datos/pbr_comparacion_resumen.json';dest.write_text(json.dumps(out,separators=(',',':'),ensure_ascii=False),encoding='utf-8')
for key,src in all_data.items():print('SOURCE',key,'objects',len(src['objects']),'used_materials',len(src['materials']),'images',len(src['images']),'packed',sum(x['packed'] for x in src['images'].values()),'missing',len(comparisons[key]['missing_used_images']),'common/topology/uv',comparisons[key]['common_objects'],len(comparisons[key]['same_topology']),len(comparisons[key]['same_uv_and_topology']),'merged',len(comparisons[key]['merged_console_parts']),flush=True)
print('TARGET',len(target['objects']),len(target['materials']),'UNCHANGED',out['files_unchanged'],'JSON_BYTES',dest.stat().st_size,flush=True)
