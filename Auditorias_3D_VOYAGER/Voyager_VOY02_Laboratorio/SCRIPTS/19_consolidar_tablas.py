import json,csv,math,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'DATOS';V1=R.parent/'Voyager_Puente_2026-10-21/DATOS'
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def write(n,d):(P/n).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
def csvout(n,rows):
 rows=list(rows)
 if not rows:return
 keys=list(dict.fromkeys(k for r in rows for k in r))
 with (P/n).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows)
# Material metadata: no pixels reloaded, changed or resized.
gltf=json.loads((V1/'gltf_Voyager_Bridge_Trabajo.json').read_text());valid=json.loads((V1/'gltf_validacion_numerica.json').read_text());vv=next(x for x in valid if Path(x['path']).name=='Voyager_Bridge_Trabajo.glb')
images=[]
for im in vv['images']:
 row={k:im[k] for k in ['name','width','height','mode','bytes','sha256']};w,h=im['width'],im['height'];row['RGBA8_base_MiB']=w*h*4/1048576;row['RGBA8_ideal_mips_MiB']=row['RGBA8_base_MiB']*4/3
 for cap in [2048,4096]:
  factor=min(1,cap/max(w,h));a=max(1,round(w*factor));b=max(1,round(h*factor));row[f'cap{cap}_width']=a;row[f'cap{cap}_height']=b;row[f'cap{cap}_RGBA8_base_MiB']=a*b*4/1048576;row[f'cap{cap}_ideal_mips_MiB']=a*b*4/1048576*4/3
 images.append(row)
materials=[]
for m in gltf['materials']:
 p=m.get('pbrMetallicRoughness',{});materials.append(dict(name=m['name'],alphaMode=m.get('alphaMode','OPAQUE'),alpha=p.get('baseColorFactor',[1,1,1,1])[3],doubleSided=m.get('doubleSided',False),baseColorTexture=p.get('baseColorTexture'),normalTexture=m.get('normalTexture'),metallicRoughnessTexture=p.get('metallicRoughnessTexture'),occlusionTexture=m.get('occlusionTexture'),emissiveTexture=m.get('emissiveTexture'),emissiveFactor=m.get('emissiveFactor'),metallicFactor=p.get('metallicFactor',1),roughnessFactor=p.get('roughnessFactor',1)))
metrics=dict(images=len(images),materials=len(materials),double_sided=sum(m['doubleSided'] for m in materials),alpha_modes=dict(collections.Counter(m['alphaMode'] for m in materials)),texture_hypotheses={k:sum(x[k] for x in images) for k in ['RGBA8_base_MiB','RGBA8_ideal_mips_MiB','cap2048_RGBA8_base_MiB','cap2048_ideal_mips_MiB','cap4096_RGBA8_base_MiB','cap4096_ideal_mips_MiB']},source='VOY-01 decoded image metadata; aspect-preserving longest-side caps rounded to integer pixels. Mip estimate 4/3 approximation, no power-of-two padding or GPU compression. Not measured VRAM.',materials_data=materials,images_data=images)
write('materiales_rendimiento_revision.json',metrics);csvout('texturas_presupuesto.csv',images);csvout('materiales_canales.csv',materials)
objects=read('obj_objetos.json');tri_by_mat=collections.Counter()
for o in objects:tri_by_mat.update(o['materials'])
csvout('materiales_triangulos.csv',[dict(material=k,triangles=v,share=v/sum(tri_by_mat.values())) for k,v in tri_by_mat.most_common()])
# Complete catalog by source identity. A functional label is not a pass-through claim.
modules=read('interfaces_modulos.json');tested={'Mesh12','Mesh13','Mesh18','Mesh41','Mesh40','Mesh38','Mesh14','Mesh37','Mesh17','Mesh57','Mesh4'};module_rows=[];port_rows=[]
for m in modules:
 parent=m.get('parent') or '';low=parent.lower()
 family='conducto_jefferies' if 'j_tube' in low or 'j_tube' in low or 'j_tube' in low or 'jt_' in low else 'mantenimiento' if 'maintenance' in low else 'turbolift_cabina' if parent=='Turbolift1' else 'turbolift_acceso' if 'turbolift' in low else 'sala_conferencias' if 'conference' in low else 'sanitario' if 'restroom' in low else 'acceso_residencial' if 'residential' in low else 'marco_o_nicho' if 'recessed' in low else 'pasillo' if 'hallway' in low or 'corridor' in low else 'envolvente_o_puente_por_verificar'
 if m['name']=='Mesh4':family='envolvente_habitacion_ensayada'
 ports=[p['code'] for p in m['ports'] if p['open_candidate']]
 grade='C' if m['name'] in tested else 'E'
 module_rows.append(dict(mesh=m['name'],parent=parent,family=family,triangles=m['triangles'],bbox_size_m=[b-a for a,b in zip(m['bounds_min'],m['bounds_max'])],candidate_ports=ports,grade=grade,scope='Selected assembly route tested; profiles/materials require adaptation' if m['name'] in tested else 'Catalogued; no complete functional route for this resource certified',normalize_translation=m['normalize_translation']))
 for p in m['ports']:port_rows.append(dict(mesh=m['name'],parent=parent,port=p['code'],point_m=p['point'],outward_normal=p['normal'],floor_z=p['floor_z'],ceiling_z=p['ceiling_z'],widths_z040_100_170_220=p['width_z040_100_170_220'],candidate=p['open_candidate'],blocked=p['centerline_blocked_z040_100_170_220']))
csvout('clasificacion_modulos.csv',module_rows);csvout('interfaces.csv',port_rows)
cases=read('ensamblajes_pruebas.json');csvout('compatibilidades.csv',[dict(case=c['id'],**j) for c in cases for j in c['joins']])
proto=read('prototipo_conjunto.json');placements=[]
for case,pp in [(c['id'],c['placements']) for c in cases]+[('G',proto['placements'])]:
 for p in pp:
  yaw=p['yaw'];cs=math.cos(yaw);ss=math.sin(yaw);x,y,z=p['translation'];nx,ny,nz=p['original_to_canonical'];matrix=[[cs,-ss,0,x+cs*nx-ss*ny],[ss,cs,0,y+ss*nx+cs*ny],[0,0,1,z+nz],[0,0,0,1]]
  placements.append(dict(case=case,**p,world_source_to_placed_matrix=matrix))
csvout('matrices_instancias.csv',placements);write('matrices_instancias.json',placements)
csvout('adaptadores.csv',[{k:v for k,v in a.items() if k!='triangles'} for a in proto['adapters']])
csvout('medidas_puertas.csv',[dict(id=d['id'],scale=s['scale'],human_height=h['human_height'],clear=h['clear'],samples=h['samples'],minimum_clearance_obj=h['minimum_clearance'],stroke_obj=d['stroke_obj_units'],width_profiles=d['widths'],center_obj=d['center'],leafA=d['leafA'],leafB=d['leafB']) for d in read('puertas_medidas.json') for s in d['scale_tests'] for h in s['tests']])
csvout('pruebas_rutas.csv',[dict(case=c['id'],height=r['height'],radius=r['radius'],samples=r['samples'],clear=r['clear'],minimum_clearance=r['minimum_clearance'],floor_support=c.get('support',c.get('floor_support'))) for c in cases+proto['routes'] for r in c['routes']])
erg=read('ergonomia_detallada.json');csvout('medidas_puestos.csv',[{k:v for k,v in s.items() if k not in ['sample_points_m','approach_tests','nearest_screen_candidates']} for s in erg['seats']]);csvout('alturas_zonas.csv',[{k:v for k,v in z.items() if k!='standing'} for z in erg['zones']]);csvout('secciones_niveles.csv',[dict(section=s['id'],**r) for s in erg['level_sections'] for r in s['runs']]);csvout('pantallas.csv',read('preparacion_funcional.json')['screens'])
csvout('contactos_puertas.csv',[dict(door=d['id'],fraction=p['fraction'],new_pairs=p['new_pairs'],transverse=p['transverse'],coplanar=p['coplanar'],other_touch_or_edge=p['other_touch_or_edge'],by_object=p['by_object']) for d in read('carreras_investigacion.json')['doors'] for p in d['poses']])
write('clasificacion_modulos.json',module_rows)
print('MATERIALS',metrics['images'],metrics['materials'],metrics['texture_hypotheses']);print('CATALOG',len(module_rows),'PORTS',len(port_rows),'MATRICES',len(placements))
