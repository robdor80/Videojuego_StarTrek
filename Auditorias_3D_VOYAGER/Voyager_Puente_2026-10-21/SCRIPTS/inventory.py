import os,json,hashlib,struct,zipfile,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LIB=Path(r'C:\Users\andro\Documents\GitHub\3D Star Trek')
models={'.glb','.gltf','.blend','.fbx','.obj','.max','.dae','.3ds','.usd','.usdz'}
found=[]; candidates=[]; count=0
roots=[LIB,Path(r'C:\Users\andro\Documents\Voyager_Bridge_Recovery\originales'),Path(r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ')]
for base,dirs,files in (v for root in roots for v in os.walk(root)):
    dirs[:]=[d for d in dirs if d not in {'.git','node_modules','.venv'}]
    for n in files:
        p=Path(base)/n; count+=1
        if any(s in str(p).lower() for s in ['voyager','sutherland','intrepid']):
            st=p.stat(); row={'path':str(p),'extension':p.suffix.lower(),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns}
            row['sha256']=hashlib.file_digest(p.open('rb'),'sha256').hexdigest() if hasattr(hashlib,'file_digest') else hashlib.sha256(p.read_bytes()).hexdigest()
            found.append(row)
            if p.suffix.lower() in models: candidates.append(str(p))
(ROOT/'DATOS/inventario_archivos.json').write_text(json.dumps({'scope':'Targeted model library plus two Voyager source directories','roots':[str(p) for p in roots],'scanned_files':count,'files':found},indent=2,ensure_ascii=False),encoding='utf-8')
with (ROOT/'DATOS/inventario_archivos.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['path','extension','bytes','mtime_ns','sha256']);w.writeheader();w.writerows(found)
glbs=[]
for s in candidates:
    p=Path(s)
    if p.suffix.lower()!='.glb' or 'voyager' not in s.lower():continue
    data=p.read_bytes(); magic,ver,total=struct.unpack_from('<4sII',data);off=12;chunks=[];j=None
    while off+8<=len(data):
        size,typ=struct.unpack_from('<II',data,off);off+=8;chunks.append({'type':typ,'bytes':size})
        if typ==0x4e4f534a:j=json.loads(data[off:off+size])
        off+=size
    (ROOT/'DATOS'/('gltf_'+p.stem+'.json')).write_text(json.dumps(j,indent=2,ensure_ascii=False),encoding='utf-8')
    acc=j.get('accessors',[]); prim=[pr for m in j.get('meshes',[]) for pr in m.get('primitives',[])]
    r={'path':s,'header':{'magic':magic.decode(),'version':ver,'declared_bytes':total,'actual_bytes':len(data)},'chunks':chunks,'asset':j['asset'],'counts':{k:len(j.get(k,[])) for k in ['scenes','nodes','meshes','materials','textures','images','animations','skins','cameras','accessors']},'extensionsUsed':j.get('extensionsUsed',[]),'extensionsRequired':j.get('extensionsRequired',[]),'primitives':len(prim),'vertices_primitive_sum':sum(acc[pr['attributes']['POSITION']]['count'] for pr in prim),'triangles_primitive_sum':sum((acc[pr['indices']]['count'] if 'indices'in pr else acc[pr['attributes']['POSITION']]['count'])//3 for pr in prim if pr.get('mode',4)==4),'uv_primitives':sum('TEXCOORD_0'in pr['attributes'] for pr in prim),'attributes':sorted(set(a for pr in prim for a in pr['attributes'])),'buffers':j.get('buffers',[]),'images':j.get('images',[]),'materials':j.get('materials',[]),'mesh_names':[m.get('name') for m in j.get('meshes',[])]}
    glbs.append(r)
archives=[]
for r in found:
    if 'voyager' in r['path'].lower() and r['extension']=='.zip':
        with zipfile.ZipFile(r['path']) as z:
            entries=[]
            for i in z.infolist():
                e={'name':i.filename,'bytes':i.file_size,'compressed':i.compress_size}
                if i.file_size<100_000_000 and Path(i.filename).suffix.lower() in models:e['sha256']=hashlib.sha256(z.read(i)).hexdigest()
                entries.append(e)
            archives.append({'path':r['path'],'entries':entries})
(ROOT/'DATOS/glb_resumen.json').write_text(json.dumps(glbs,indent=2,ensure_ascii=False),encoding='utf-8')
(ROOT/'DATOS/archivos_zip.json').write_text(json.dumps(archives,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'scanned':count,'matched':len(found),'models':[r for r in found if r['extension']in models],'glbs':[{'path':r['path'],'counts':r['counts'],'triangles':r['triangles_primitive_sum']} for r in glbs],'archives':archives},ensure_ascii=False,indent=2))
