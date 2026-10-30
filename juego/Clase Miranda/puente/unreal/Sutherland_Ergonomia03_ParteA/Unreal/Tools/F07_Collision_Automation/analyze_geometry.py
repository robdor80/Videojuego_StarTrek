"""Offline analysis of UE-exported geometry; never writes Unreal packages."""
import pathlib,json,math,collections
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
g=json.loads((OUT/'geometria.json').read_text(encoding='utf-8'))
inv=json.loads((OUT/'01_inventario_inicial.json').read_text(encoding='utf-8'))
def transform(v,inst):
    q=np.array(inst['rotation'][:3]); w=inst['rotation'][3]
    v=v*np.array(inst['scale']); uv=np.cross(q,v)
    return v+2*(w*uv+np.cross(q,uv))+np.array(inst['translation'])
def islands(v,t):
    # Weld by positions so material/normal seams do not split physical pieces.
    keys=[tuple(np.round(x,3)) for x in v]; ids={}; mp=[]
    for k in keys:
        if k not in ids: ids[k]=len(ids)
        mp.append(ids[k])
    parent=list(range(len(ids)))
    def find(a):
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    for a,b,c in t:
        a,b,c=[find(mp[x]) for x in (a,b,c)]
        parent[b]=parent[c]=a
    groups=collections.defaultdict(list)
    for i,tri in enumerate(t): groups[find(mp[tri[0]])].append(i)
    return sorted(groups.values(),key=len,reverse=True)
world={}; stats=[]
for inst in g['instances']:
    md=g['meshes'][inst['mesh']]; vv=[];tt=[]
    for s in md['sections']:
        tt.extend((np.array(s['triangles']).reshape(-1,3)+len(vv)).tolist()); vv.extend(s['vertices'])
    v=transform(np.array(vv),inst); t=np.array(tt,dtype=int)
    world[inst['label']]={'v':v.tolist(),'t':t.tolist(),'actor':inst['actor'],'mesh':inst['mesh']}
    groups=islands(v,t)
    entry={'name':inst['label'],'triangles':len(t),'island_count':len(groups),'islands':[]}
    for group in groups:
        pts=v[t[group].ravel()]; mn=pts.min(axis=0);mx=pts.max(axis=0)
        entry['islands'].append({'triangles':len(group),'min':mn.tolist(),'max':mx.tolist(),'center':((mn+mx)/2).tolist(),'dims':(mx-mn).tolist(),'triangle_indices':group})
    stats.append(entry)
(OUT/'world_geometry.json').write_text(json.dumps(world),encoding='utf-8')
(OUT/'geometry_analysis.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
# Measured horizontal section with mesh IDs; schematic evidence, not a UE screenshot.
W,H=1600,1250; im=Image.new('RGB',(W,H),'#151b24'); d=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
def project(p): return (int(815-p[0]*.68),int(1035-p[1]*.68))
for name,md in world.items():
    v=np.array(md['v']);t=np.array(md['t']); col='#687786'
    if name.startswith('Mesh_589'): col='#d5a46a'
    if name=='Cylinder_002_0': col='#f05f65'
    if name in ['Plane_019_0','Plane_018_0','Plane_001_0','Plane_017_0']: col='#b187ef'
    if name=='Sphere_001_0': col='#f0cb71'
    for tri in v[t]:
        z=100; pts=[]
        for j in range(3):
            a,b=tri[j],tri[(j+1)%3]
            if (a[2]<=z<b[2]) or (b[2]<=z<a[2]): pts.append(a+(b-a)*(z-a[2])/(b[2]-a[2]))
        if len(pts)==2:d.line([project(x) for x in pts],fill=col,width=2)
    if name.startswith(('Plane_0','Cylinder_002','Sphere_001','Mesh_589')):
        pts=v[(v[:,2]>65)&(v[:,2]<250)]
        if len(pts) and (name.startswith('Mesh_589') or name in ['Cylinder_002_0','Sphere_001_0']):
            label=md['mesh'].split('.')[-1]
            p=project(pts.mean(axis=0));d.text(p,label,fill=col,font=font)
d.text((45,35),'F07 - seccion horizontal z=100 cm / geometria UE, sin modificar',font=font,fill='white')
d.text((45,65),'Frente: +Y (pantalla) | Izquierda del Capitan: +X | Derecha: -X',font=font,fill='white')
markers=[(0,1000,'PANTALLA'),(-813,872,'CABINA TURBO')]
catalog=OUT/'puertas_f07_inventario.json'
if catalog.exists():
    for door in json.loads(catalog.read_text(encoding='utf-8'))['doors']:
        markers.append((door['center_cm'][0],door['center_cm'][1],'D'+door['id'][-2:]))
for x,y,txt in markers:
    p=project((x,y));d.ellipse([p[0]-5,p[1]-5,p[0]+5,p[1]+5],fill='#4ae5e0');d.text((p[0]+8,p[1]),txt,font=font,fill='#4ae5e0')
im.save(OUT/'plano_geometria_z100.png')
for s in stats:
    if s['name'] in ['Cylinder_002_0','Plane_019_0','Plane_018_0','Plane_001_0','Plane_017_0','Plane_007_0','Plane_009_0']:
        print(s['name'],s['triangles'],'tri',s['island_count'],'islands')
        for it in s['islands'][:16]: print(' ',it['triangles'],'center',np.round(it['center'],1),'dims',np.round(it['dims'],1))
