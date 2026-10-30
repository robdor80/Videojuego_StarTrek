"""Compact only the JSON manifest and write the short delivery report. No blend mutation."""
import sys,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pbr01_integrity import compact_plans,expand_assignments,file_sha
R=Path(__file__).resolve().parents[1];path=R/'datos/pbr01_manifest.json'
m=json.loads(path.read_text(encoding='utf-8'));v=json.loads((R/'datos/pbr01_verificacion.json').read_text(encoding='utf-8'))
if m['plans'] and 'assignments' in m['plans'][0]:
    compact=compact_plans(m['plans'])
    assert all(sorted(a['assignments'],key=lambda x:x['face'])==sorted(expand_assignments(b),key=lambda x:x['face']) for a,b in zip(m['plans'],compact))
    m['plans']=compact
m['range_encoding']='Each [target_face_start, source_face_start, count] uses zero-based polygon indices, increasing both indices by one per face.'
assert v['ok'] and all(file_sha(p)==h for p,h in m['original_sha256'].items()) and file_sha(m['output'])==m['output_sha256']
m['visual_check']={'application':'Blender 5.2.2 LTS','mode':'Material Preview; exterior, top and oblique interior views',
   'observed':['two distinct carpets','burgundy doors and existing LCARS atlases','six lateral chairs and captain chair','both isolated consoles with blue/pale-blue strips'],
   'limitations':'Light viewport check only; no heavy render, no artistic approval or UE5 test. Viewport changes were not saved.'}
v['visual_check']=m['visual_check']
path.write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
(R/'datos/pbr01_verificacion.json').write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
rows=collections.defaultdict(lambda:{'faces':0,'objects':[]})
for p in m['plans']:
    for a in expand_assignments(p):
        row=rows[a['to']];row['faces']+=1
        if p['object'] not in row['objects']:row['objects'].append(p['object'])
table='\n'.join('| `'+name+'` | '+str(row['faces'])+' | '+', '.join('`'+n+'`' for n in row['objects'])+' |' for name,row in sorted(rows.items()))
report=f'''# USS Sutherland — transferencia PBR 01

28/10/2026. Blender 5.2.2 LTS. **Entregado:** `../blender/Miranda_Puente_Sutherland_PBR_01.blend` (34.039.949 bytes).

## Fuente y procedimiento

Fuente única de materiales: `{m['source']}`. Destino original: `{m['original']}`. Ambos conservan sus SHA-256. No se sobrescribió ningún original, no se abrió UE5 ni se realizó commit, push o PR. No se cargó ni aplicó la variante `PBR_Paneles_Prueba_Gris`.

Antes de transferir se comprobó el Ergonomia_04 guardado: silla del capitán al 85 % de las dimensiones de Ergonomia_03; cilindro al 85 % en X/Y con altura conservada; tres paneles LCARS 30 cm más bajos; dos soportes inferiores separados y con sus caras superiores ajustadas a las consolas; franja azul presente y conectada a su atlas/emisión. Se utilizó únicamente el registro dimensional anterior para contrastar estas medidas; no se modificaron.

Se añadieron **14 materiales completos**, sin importar objetos ni mallas, y se asignaron **5.435 caras de 33 objetos**. La correspondencia directa exige orden de polígonos, topología y UV actuales coincidentes. Para las consolas agrupadas se verificó cada lado por signo X, índices de vértices normalizados y UV por esquina. Los índices de material anteriores no se sustituyeron globalmente: se añadieron ranuras y se reasignaron solo las caras verificadas.

## Materiales y superficies

| Material recuperado | Caras | Objetos actuales |
|---|---:|---|
{table}

`Circle_0` recupera exactamente 24 caras de moqueta del capitán y 12 de moqueta del puente. `Plane.020_0` conserva la distribución original de cinco acabados; no se unificó el techo. `PBR_Capitan_Titanio` se aplicó únicamente a estructuras del techo (`Plane.012_0`, `Plane.020_0`, `Plane.044_0`), nunca a la silla ni a su cilindro. Las cuatro mallas de puertas mantienen sus dimensiones y geometría (alturas entre 303,08 y 304,50 cm).

## Conservación y excepciones

- **Siete sillas intactas:** se protegieron las 96 piezas de las seis sillas laterales y las cinco piezas de la silla del capitán, incluidos soporte/cilindro. No cambió ninguna geometría, transformación, ranura, asignación ni grafo de sus materiales.
- **LCARS:** 2.198 caras conservan sus materiales y UV; también se conservan sus imágenes y grafos originales.
- **Azul:** `Editable Mesh_Mat.004_0` recibe `Luz_Azul_Suave_Consola` en las 34 caras con correspondencia exacta de la fuente: 18 a un lado y 16 al otro. Otras dos caras del segundo lado conservan `BLUE`, como en la fuente. Ambas franjas mantienen emisión. No se simplificó ningún grafo Light Path/Transparent/Emission.
- **Piezas inferiores:** `Editable Mesh_Mat.003_0` y `.003_0.001` conservan íntegramente sus materiales actuales porque no hay correspondencia de topología + UV verificada. No se copiaron las UV antiguas.
- **BLUE protegido:** no se aplicaron acabados opacos antiguos sobre `Editable Mesh_Mat.007_0`, `.010_0`, `.011_0`, `Plane.008_0`, `Plane.023_0` o `Plane.025_0`. Se preservaron sus caras azules actuales, además de las dos citadas en `.004_0` y las piezas inferiores.
- Los materiales básicos sin sustitución PBR compatible se conservaron, incluidos los materiales de sillas, LCARS, rótulos y otras superficies heredadas. No se trasladaron cueros de las sillas antiguas. No hay dependencias pendientes: **26/26 imágenes utilizadas empaquetadas**, con tamaño válido; ninguna biblioteca Blender enlazada.

## Validación ejecutada

Se guardó el archivo nuevo y se reabrió en un proceso independiente de Blender. Pasaron todas las comprobaciones de `datos/pbr01_verificacion.json`: **346 objetos y 171 mallas**, identidad de vértices, aristas, conectividad y orden de caras/esquinas, todas las capas UV, atributos de normales personalizadas y aristas duras, transformaciones, dimensiones, jerarquías y configuración de modificadores/restricciones. Coinciden los materiales protegidos y todos los grafos/imágenes originales. Las únicas caras reasignadas son las del manifiesto; los 14 grafos añadidos coinciden con los de la fuente, incluidas conexiones y parámetros.

Comprobación visual ligera **ejecutada en la interfaz de Blender**, modo Material Preview, vistas exterior, superior e interior oblicua: se muestran las dos moquetas, puertas burdeos, atlas LCARS, las siete sillas y ambas consolas con franjas azul claro. No se observaron texturas magenta en esas vistas. No se guardaron los cambios de navegación/previsualización. **Esta revisión no constituye aprobación estética definitiva**, ni prueba de iluminación indirecta por render ni validación en UE5.

Manifiesto compacto: `datos/pbr01_manifest.json`; incluye fuente/destino, hashes, exclusiones y correspondencias por intervalos de caras (índices desde cero). Evidencia inicial: `datos/pbr01_preflight.json`. Scripts: `scripts/transferir_pbr01.py`, `scripts/verificar_pbr01.py` y auxiliar `scripts/pbr01_integrity.py`. El script de transferencia rechaza sobrescribir una salida existente.

**Limitación pendiente:** aprobación visual del usuario y, si se desea en otra intervención, revisión artística de las superficies conservadas por precaución. Trabajo finalizado en Blender; sin continuación automática.
'''
(R/'Informe_Transferencia_PBR_01.md').write_text(report,encoding='utf-8')
print('REPORT',R/'Informe_Transferencia_PBR_01.md','MANIFEST_BYTES',path.stat().st_size,'ORIGINALS_UNCHANGED',True,flush=True)
