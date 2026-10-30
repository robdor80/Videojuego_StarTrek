"""Reabrir Ergonomia_02 y verificar persistencia. Produce informe breve."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).parent))
from ergonomia02_inspeccion import object_state,material_state,digest,sha
d=json.loads((ROOT/'datos/ergonomia02_resultados.json').read_text(encoding='utf-8'))
source=json.loads((ROOT/'datos/ergonomia02_inspeccion.json').read_text(encoding='utf-8'))
assert Path(bpy.data.filepath)==Path(d['target'])
bpy.context.view_layer.update()
actual={o.name:digest(object_state(o)) for o in bpy.data.objects}
assert actual==d['expected_hashes'],'Diferencia al reabrir'
protected={p:sha(p)==h for p,h in d['protected_sha256'].items()}
assert all(protected.values())
assert {m.name:digest(material_state(m)) for m in bpy.data.materials}==source['material_hashes']
images={i.name:{'path':i.filepath,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images}
assert all(images[n]==v for n,v in source['images'].items() if n not in ['Render Result','Viewer Node'])
seams={};geometry={};floors={};corner_heights={}
for name,changes in d['changes'].items():
    old=source['objects'][name]['world_vertices'];o=bpy.data.objects[name];new=[list(o.matrix_world@v.co) for v in o.data.vertices]
    max_xy=max(math.dist(a[:2],b[:2]) for a,b in zip(old,new))
    newly_degenerate=0;flipped=0;max_seam_opening=0.;coincident_pairs=0
    # Los triángulos desconectados por UV conservan sus coincidencias de vértices.
    for i,a in enumerate(old):
        for j in range(i):
            if math.dist(a,old[j])<1e-5:
                coincident_pairs+=1
                max_seam_opening=max(max_seam_opening,math.dist(new[i],new[j])-math.dist(a,old[j]))
    for p in o.data.polygons:
        ids=list(p.vertices)
        for k in range(1,len(ids)-1):
            va,vb,vc=(Vector(old[i]) for i in [ids[0],ids[k],ids[k+1]])
            wa,wb,wc=(Vector(new[i]) for i in [ids[0],ids[k],ids[k+1]])
            na=(vb-va).cross(vc-va);nb=(wb-wa).cross(wc-wa)
            if na.length>1e-8 and nb.length<1e-8:newly_degenerate+=1
            if na.length>1e-8 and nb.length>1e-8 and na.dot(nb)<0:flipped+=1
    assert max_xy<2e-6,(name,max_xy)
    assert newly_degenerate==0 and flipped==0,(name,newly_degenerate,flipped)
    assert max_seam_opening<2e-6,(name,max_seam_opening)
    seams[name]={'coincident_pairs_tested':coincident_pairs,'maximum_new_opening_cm':max_seam_opening*100}
    geometry[name]={'max_xy_change_cm':max_xy*100,'new_degenerate_triangles':newly_degenerate,'flipped_triangles':flipped}
for p in d['portals']:
    x,y=p['center'];sign=p['side'];o=bpy.data.objects['Circle_0']
    tr=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(q.vertices) for q in o.data.polygons])
    pt=tr.ray_cast(Vector((x-sign*.4,y,p['floor']+.1)),Vector((0,0,-1)),1)[0]
    assert pt is not None and abs(pt.z-p['floor'])<.00002,(p['id'],pt)
    floors[p['id']]={'sample_world_cm':list(pt*100),'floor_cm':p['floor']*100}
    o=bpy.data.objects[p['frame']]
    zv=[(o.matrix_world@v.co).z for v in o.data.vertices if (o.matrix_world@v.co).x*sign>0]
    upper=[z for z in zv if p['floor']+2<z<4.65]
    corner_heights[p['id']]=100*(min(upper)-p['floor'])
v={'saved_copy_reopened':True,'object_hashes_match':True,'original_object_count':len(actual),
   'unchanged_objects_count':len(actual)-len(d['changes']),'changed_objects':list(d['changes']),
   'protected_files_unchanged':protected,'materials_unchanged':True,'uv_unchanged':True,
   'image_references_unchanged':True,'floor_samples':floors,'seams':seams,'geometry':geometry,
   'central_clear_height_target_cm':300,'bevel_lower_edges_above_floor_cm':corner_heights,
   'passed':True,'limitations':['Altura objetivo medida al dintel central; los biseles conservan cotas inferiores junto a las jambas.',
     'Cobertura del revestimiento comprobada con 2911 rayos por puerta, 95% central del ancho; no certifica volumen estanco ni colisiones de Unreal.',
     'La puerta de referencia se mantiene tal como fue entregada, con altura central de 300.135 cm sobre suelo del puente.',
     'UV sin cambios: las zonas acortadas o alargadas redistribuyen visualmente la textura. Validación visual final por el usuario.']}
(ROOT/'datos/ergonomia02_verificacion_final.json').write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
def cm(x):return f'{x:.2f}'.replace('.',',')
lines=['# MIRANDA-01 — Puertas: Ergonomía 02','',
 'Resultado guardado en `../blender/Miranda_Puente_Sutherland_Ergonomia_02.blend`. Fuente: `Miranda_Puente_Sutherland_Ergonomia_01.blend`. Blender 5.2.2 LTS. Fecha: 27/10/2026.',
 '', '## Antes / después', '',
 'Todas las medidas están en centímetros y coordenadas globales. Altura libre = suelo local hasta la cara inferior del dintel en el centro del paso, con las hojas cerradas excluidas del sondeo. Las hojas permanecen cerradas; no se ha creado animación.', '',
 '| Puerta / ubicación mundial | Suelo Z | Paso antes → después | Hoja derecha antes → después | Hoja izquierda antes → después | Ancho útil antes → después |',
 '|---|---:|---:|---:|---:|---:|']
for p in d['portals']:
    key=p['id'];a=d['before'][key];b=d['after'][key]
    ll=[]
    for aa,bb in zip(a['leaves'],b['leaves']):ll.append(f"{cm(aa['leaf_height_cm'])} → {cm(bb['leaf_height_cm'])}")
    lines.append(f"| {key}: X={cm(p['center'][0]*100)}, Y={cm(p['center'][1]*100)} | {cm(a['floor_world_cm'])} | {cm(a['clear_height_center_cm'])} → {cm(b['clear_height_center_cm'])} | {ll[0]} | {ll[1]} | {cm(a['clear_width_cm'])} → {cm(b['clear_width_cm'])} |")
lines+=['', 'La altura de hoja incluye la parte que ya quedaba por debajo del suelo; por eso supera la altura libre. Las tres puertas nuevas terminan a 300,588 cm sobre su suelo y solapan aproximadamente 0,588 cm bajo el revestimiento. Los extremos inferiores no se han desplazado.',
 '', '## Objetos y diferencias', '',
 '- **D1, referencia del turbo (X negativo, Y negativo):** partes X negativas de `Plane.018_0`, `Plane.019_0` y `Plane.004_0`, íntegramente conservadas. Materiales `door` en hojas; ranuras `cream` y `captainschair` en el marco, con sus asignaciones originales. El marco interior `Plane.039_0` conserva el dintel alto anterior: no se ha modificado la cabina ni la puerta de referencia.',
 '- **D2, opuesta (X positivo, Y negativo):** se modifican solo las partes X positivas de `Plane.018_0`, `Plane.019_0` y `Plane.004_0`. Hueco inclinado unos 10° en planta. Paredes adyacentes `Plane.011_0` y `Plane.022_0`, sin cambios. No tiene habitación construida detrás.',
 '- **D3 y D4 (Y positivo):** hojas de las partes X positiva/negativa de `Plane.001_0` y `Plane.017_0`; marco `Plane.013_0`. Materiales `door` y `grey`. Suelo elevado a Z=60 cm, hueco más ancho, perfil y espesor propios conservados. Paredes adyacentes `Plane.009_0`, `Plane.010_0`, `Plane.014_0` y techo `ceiling_0`, sin cambios. No se han creado habitaciones.',
 '', 'Solo cambian seis objetos de malla compartidos. Se bajan los vértices superiores de las hojas y todo el contorno superior de los tres huecos; los vértices de coronación y los inferiores permanecen fijos. Los paños frontales existentes se alargan hacia abajo con su propia conectividad. No se añaden caras, objetos, materiales ni interiores; no se aplica escala global.',
 '', '## Verificaciones', '',
 f'- Copia reabierta y verificada: {len(actual)} objetos; {len(actual)-len(d["changes"])} objetos completos sin cambios y seis mallas con cambios limitados a los vértices registrados.',
 '- Referencia D1 sin cambios en sus vértices, UV o asignaciones. Los originales Base, Analisis y Ergonomia_01 conservan sus SHA-256.',
 '- Transformaciones, jerarquías, conectividad, índices de materiales, UV y referencias de imágenes conservados. Consistencia de los materiales verificada al reabrir.',
 '- Anchuras, extremos inferiores y coronaciones conservados dentro de la precisión numérica de Blender; variaciones de anchura inferiores a 0,001 cm.',
 '- Consolas y silla del capitán: conservación íntegra respecto a Ergonomia_01, comprobada junto con todos los objetos no relacionados.',
 '- 2.911 rayos por puerta sobre el revestimiento superior sin huecos detectados. Coincidencias de vértices comprobadas; sin nuevas aperturas de costuras, triángulos degenerados o caras invertidas.',
 '', '## Advertencias y límite de la validación', '',
 '- La referencia tiene paso central **300,135 cm** sobre el suelo del puente y se deja intacta. El suelo de la cabina está aproximadamente 0,10 cm más alto; desde ese lado su paso es unos 300,035 cm.',
 f'- Los **300 cm corresponden al centro del dintel**. Se conservan los biseles de cada marco: sus arranques junto a las jambas quedan a {cm(corner_heights["D2_opuesta_Yneg"])} cm en D2 y {cm(corner_heights["D3_Xpos_Ypos"])} cm en D3/D4. La referencia conserva {cm(corner_heights["D1_referencia_turbo"])} cm. No existe un rectángulo de 300 cm de alto que abarque toda la anchura entre jambas.',
 '- Las UV no se han reproyectado: las superficies acortadas o extendidas pueden mostrar compresión o estiramiento de textura, como consecuencia de conservar sus coordenadas originales.',
 '- El muestreo del revestimiento cubre el 95% central de la anchura, desde 3 cm sobre el nuevo dintel hasta 1 cm bajo la coronación. No certifica estanqueidad volumétrica, animaciones o colisiones del motor.',
 '- Validación visual final pendiente del usuario en Blender. No se han modificado Unreal, Valhalla ni otros modelos. Sin commit, push, PR o inclusión forzada de archivos .blend en Git.',
 '', '## Evidencias y reproducción', '',
 '- `datos/ergonomia02_inspeccion.json`: inventario original, geometría mundial, UV, materiales y hashes.',
 '- `datos/ergonomia02_resultados.json`: medidas antes/después, vértices editados, pruebas de cobertura y hashes de la copia.',
 '- `datos/ergonomia02_verificacion_final.json`: comprobaciones tras reabrir el archivo.',
 '- `scripts/ergonomia02_inspeccion.py`, `scripts/ergonomia02_aplicar_verificar.py`, `scripts/ergonomia02_verificacion_final.py`: scripts conservados dentro de analisis_dimensional. El script de edición se niega a sobrescribir un Ergonomia_02 existente.',
 '', 'Trabajo geométrico finalizado. No quedan bloqueos detectados para las operaciones realizadas; se mantienen las limitaciones indicadas.']
(ROOT/'Informe_Ergonomia_02.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('VERIFICACION_FINAL_OK',json.dumps({'objects':len(actual),'changed':list(d['changes']),'protected_files_unchanged':all(protected.values()),'coverage_rays':sum(x['rays'] for x in d['coverage'].values())}))
print('INFORME',ROOT/'Informe_Ergonomia_02.md')
