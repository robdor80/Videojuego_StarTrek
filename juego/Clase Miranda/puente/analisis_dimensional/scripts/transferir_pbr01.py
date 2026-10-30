"""Append only approved material datablocks; never import or replace geometry.
Run with -- --apply to create the NEW PBR_01 file. Without it, only writes the plan.
"""
import bpy,sys,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pbr01_integrity import *
R=Path(__file__).resolve().parents[1];REPO=R.parents[3]
SOURCE=REPO/'TABULA RASA COPIA SEGURIDAD/01_TEXTURAS_PBR_SUTHERLAND/DERIVADOS_EXISTENTES/Blender_Integracion_Final/Referencia_Visual02.blend'
TARGET=R.parent/'blender/Miranda_Puente_Sutherland_Ergonomia_04.blend'
OUTPUT=TARGET.with_name('Miranda_Puente_Sutherland_PBR_01.blend')
MANIFEST=R/'datos/pbr01_manifest.json'
APPLY='--apply' in sys.argv
assert json.loads((R/'datos/pbr01_preflight.json').read_text())['ok'], 'Saved ergonomic changes not verified'
assert not OUTPUT.exists(), 'Never overwrite an existing output'
controls={str(p):file_sha(p) for p in [SOURCE,TARGET]}
approved={'PBR_Mamparos_Composite_Oscuro','PBR_Paneles_Composite_Claro','PBR_Paneles_Composite_Hueso',
          'PBR_Moqueta_Puente','PBR_Moqueta_Capitan','PBR_Puente_Plataforma_Titanio',
          'PBR_Puente_Barandillas_AceroCepillado','PBR_Techo_Faldones_Gunmetal','PBR_Techo_Acero_Cepillado_Claro',
          'PBR_Puertas_Burdeos_ConTexto','PBR_Luz_Sutherland_Fria','Luz_Azul_Suave_Consola',
          'PBR_Capitan_Titanio','Marcos_Ascensor_Negro'}
lcars={'turbolcar','lcardtype','lcarkey','lcarsdisplay','lcarsdisplay.001'}
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),load_ui=False)
src={o.name:mapping_record(o) for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)}
source_graphs={n:graph_hash(bpy.data.materials[n]) for n in approved}
bpy.ops.wm.open_mainfile(filepath=str(TARGET),load_ui=False)
before=snapshot(); assert len(before['chair_assignments'])==101
target_mapping={o.name:mapping_record(o) for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)}
preserved_faces={n:[(i,m) for i,m in enumerate(r['materials']) if m in lcars or m=='BLUE'] for n,r in target_mapping.items()}
plans=[];exceptions=[]

def uv_equal(a,b):
    return len(a)==len(b) and all(abs(x-y)<1e-6 for u,v in zip(a,b) for x,y in zip(u,v))

def direct(a,b):
    return a['vertices']==b['vertices'] and a['polys']==b['polys'] and a['uv_names']==b['uv_names'] and len(a['uv'])==len(b['uv']) and all(uv_equal(x,y) for x,y in zip(a['uv'],b['uv']))

def paired_mapping(name,t):
    names=[n for n in src if n==name or n.startswith(name+'.')]
    if len(names)!=2 or sum(src[n]['vertices'] for n in names)!=t['vertices'] or sum(len(src[n]['polys']) for n in names)!=len(t['polys']): return None
    result=[]
    for sn in names:
        s=src[sn]
        sign=1 if min(s['world_x'])>0 else -1 if max(s['world_x'])<0 else 0
        if not sign:return None
        vertices=[i for i,x in enumerate(t['world_x']) if x*sign>0]
        if len(vertices)!=s['vertices']:return None
        index={v:i for i,v in enumerate(vertices)}
        faces=[(i,p) for i,p in enumerate(t['polys']) if all(v in index for v in p)]
        if [[index[v] for v in p] for i,p in faces]!=s['polys'] or t['uv_names']!=s['uv_names']:return None
        if len(t['uv'])!=len(s['uv']):return None
        for tuv,suv in zip(t['uv'],s['uv']):
            selected=[]
            for i,p in faces:
                start,total=t['loop_ranges'][i]; selected.extend(tuv[start:start+total])
            if not uv_equal(selected,suv):return None
        result.extend((i,sn,j,s['materials'][j]) for j,(i,p) in enumerate(faces))
    return result if len(result)==len(t['polys']) else None

for name,t in sorted(target_mapping.items()):
    o=bpy.data.objects[name]
    if protected_chair(name):continue
    if o.data.users!=1:
        exceptions.append({'object':name,'reason':'shared mesh datablock; preserved'});continue
    if name in src and direct(src[name],t):
        mapping=[(i,name,i,m) for i,m in enumerate(src[name]['materials'])]; method='same topology, polygon order and current UV'
    else:
        mapping=paired_mapping(name,t) if name.startswith('Editable Mesh_Mat.') else None
        method='paired original sides, normalized topology and per-corner current UV'
    if mapping is None:
        exceptions.append({'object':name,'reason':'no verified topology + UV correspondence; current materials preserved'});continue
    assignments=[];kept_blue=collections.Counter();kept_lcars=0
    for i,sn,j,mat in mapping:
        current=t['materials'][i]
        if current in lcars:kept_lcars+=1;continue
        if current=='BLUE':
            # Only the positively matched original blue strip can receive the original blue emission.
            if mat!='Luz_Azul_Suave_Consola':kept_blue[mat or '(none)']+=1;continue
        if mat not in approved or current==mat:continue
        assignments.append({'face':i,'source_object':sn,'source_face':j,'from':current,'to':mat})
    if assignments:plans.append({'object':name,'method':method,'assignments':assignments})
    if kept_blue:exceptions.append({'object':name,'reason':'current BLUE protected from opaque original materials','faces':sum(kept_blue.values()),'source_materials':dict(kept_blue)})

needed=sorted({a['to'] for p in plans for a in p['assignments']})
manifest={'source':str(SOURCE),'original':str(TARGET),'output':str(OUTPUT),'original_sha256':controls,
          'preflight':'pbr01_preflight.json','mode':'applied' if APPLY else 'plan only',
          'protected_chair_meshes':sorted(before['chair_assignments']),
          'plans':plans,'exceptions':exceptions,'materials':needed,'source_graphs':{n:source_graphs[n] for n in needed},
          'counts':{'objects_before':len(before['objects']),'mesh_datablocks':len(before['meshes']),
                    'objects_assigned':len(plans),'faces_assigned':sum(len(p['assignments']) for p in plans),
                    'protected_chair_meshes':len(before['chair_assignments'])},
          'gray_variant_applied':False}
if APPLY:
    with bpy.data.libraries.load(str(SOURCE),link=False) as (data_from,data_to):
        assert all(n in data_from.materials for n in needed)
        data_to.materials=list(needed)
    recovered={n:m for n,m in zip(needed,data_to.materials)}
    assert all(graph_hash(recovered[n])==source_graphs[n] for n in needed), 'Appended graphs differ'
    for plan in plans:
        o=bpy.data.objects[plan['object']];mesh=o.data
        assert not protected_chair(o.name)
        slots={m.name:i for i,m in enumerate(mesh.materials) if m}
        for a in plan['assignments']:
            mat=recovered[a['to']]
            if mat.name not in slots:
                slots[mat.name]=len(mesh.materials);mesh.materials.append(mat)
            mesh.polygons[a['face']].material_index=slots[mat.name]
    after=snapshot()
    assert before['objects']==after['objects'], 'Object state changed'
    assert before['meshes']==after['meshes'], 'Geometry/UV/normals changed'
    assert before['chair_assignments']==after['chair_assignments'], 'Chair materials changed'
    assert all(after['materials'].get(n)==h for n,h in before['materials'].items()), 'Existing material modified'
    assert all(after['images'].get(n)==im for n,im in before['images'].items()), 'Existing image modified'
    for name,faces in preserved_faces.items():
        mats=face_materials(bpy.data.objects[name])
        for i,mat in faces:
            assert mats[i]==mat or (mat=='BLUE' and mats[i]=='Luz_Azul_Suave_Consola'), 'Protected emission/LCARS replaced'
    assert all(file_sha(p)==h for p,h in controls.items()), 'Original changed'
    manifest['baseline_digests']={k:digest(before[k]) for k in ['objects','meshes','chair_assignments','materials','images']}
    manifest['material_datablocks']={n:recovered[n].name for n in needed}
    manifest['memory_integrity_passed']=True
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT),check_existing=False)
    assert all(file_sha(p)==h for p,h in controls.items()), 'Original changed after saving'
    manifest['output_sha256']=file_sha(OUTPUT)
manifest['plans']=compact_plans(plans)
manifest['range_encoding']='Each [target_face_start, source_face_start, count] uses zero-based polygon indices, increasing both indices by one per face.'
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in manifest.items() if k in ['mode','counts','materials','exceptions','memory_integrity_passed']},ensure_ascii=False),flush=True)
