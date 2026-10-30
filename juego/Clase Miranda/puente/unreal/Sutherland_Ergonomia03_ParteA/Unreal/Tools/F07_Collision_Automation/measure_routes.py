import pathlib,json
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2];OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
g=json.loads((OUT/'world_geometry.json').read_text());instances=json.loads((OUT/'geometria.json').read_text())['instances']
def intersections(name,y):
    md=g[name];v=np.array(md['v']);t=np.array(md['t']);points=[]
    for tri in v[t]:
        for j in range(3):
            a,b=tri[j],tri[(j+1)%3]
            if (a[1]<=y<b[1]) or (b[1]<=y<a[1]):
                p=a+(b-a)*(y-a[1])/(b[1]-a[1])
                if 37<=p[2]<=147:points.append(p)
    return np.array(points)
rows=[]
for a in instances:
    if not a['mesh'].split('.')[-1].startswith('Mesh_589'):continue
    label=a['label'];sgn=1 if a['bounds'][0][0]>0 else -1;center=a['bounds'][0]
    samples=[]
    for y in np.arange(center[1]-30,center[1]+31,1):
        cp=intersections(label,y);bp=intersections('Cylinder_002_0',y)
        if not len(cp) or not len(bp):continue
        bp=bp[bp[:,0]*sgn>0]
        if not len(bp):continue
        front=float(max(cp[:,0]*sgn));base=float(min(bp[:,0]*sgn));gap=base-front
        samples.append({'y_cm':float(y),'chair_x_abs_cm':front,'base_x_abs_cm':base,'gap_cm':gap})
    minimum=min(samples,key=lambda x:x['gap_cm'])
    row={'asset':a['mesh'],'actor':a['actor'],'side':'IZQUIERDA' if sgn>0 else 'DERECHA','capsule_diameter_cm':70,
         'capsule_full_radius_z_range_cm':[37,147],
         'minimum_measured_cross_section':minimum,
         'method':'Interseccion exacta de triangulos renderizados con planos Y, limitada al cilindro vertical de la capsula; no AABB de toda la escena',
         'conclusion':'HUECO_MENOR_QUE_CAPSULA' if minimum['gap_cm']<70 else 'ANCHO_SUFICIENTE_AQUI_NO_CERTIFICA_RUTA'}
    rows.append(row)
(OUT/'medidas_pasillos.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
for row in rows:print(row['asset'].split('.')[-1],row['side'],row['minimum_measured_cross_section'])
