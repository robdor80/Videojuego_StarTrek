"""Síntesis reproducible de la auditoría; sólo escribe en informes."""
import collections
import datetime
import json
from pathlib import Path
import re
import unicodedata


def key(s):
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s.casefold() if not unicodedata.category(c).startswith('C')))


def props(p):
    return {x['text'].split(None,1)[0]:x['text'].split(None,1)[1] for x in p['properties'] if len(x['text'].split(None,1))>1}


def inputs(m):
    return {s['name']:s['value'] for n in m['nodes'] if n['type']=='ShaderNodeBsdfPrincipled' for s in n['inputs']}


def clean(s):
    return ''.join(c for c in s if not unicodedata.category(c).startswith('C')).replace('|','\\|').strip()


def basename(path):
    return re.split(r'[\\/:]',path)[-1].casefold()


def rename(s):
    return re.sub(r'(?<=\d)\.(?=\d)','_',s)


def enrich(r):
    objects={o['name']:o for o in r['objects']}
    meshes=[o for o in r['objects'] if o['type']=='MESH' and o['name']!='Voyager Bridge']
    materials=[m for m in r['materials'] if any(a['subset']!='legacy_OBJ' for a in m['assignments'])]
    nodes=r['max_partial_reader']['nodes']
    source_names=collections.Counter(n['name'] for n in nodes)
    for o in r['objects']:
        if o['name']=='Voyager Bridge':
            o['provenance']=dict(subset='legacy_OBJ',evidence='Declaración explícita del usuario y nombre exacto; aislado de todos los cómputos MAX.')
        elif source_names[o['name']]:
            o['provenance']=dict(subset='MAX',evidence='Nombre exacto presente en nodos del lector MAX instalado.',source_name=o['name'])
        elif o['name'].endswith('.001') and source_names[o['name'][:-4]]==2:
            o['provenance']=dict(subset='MAX',evidence='Dos nodos MAX con el mismo nombre; sufijo de unicidad Blender .001. No se asigna cada duplicado a su nodo individual.',source_name=o['name'][:-4])
        else:
            o['provenance']=dict(subset='unverified',evidence='Sin correspondencia nominal probada.')
    r['scope']['provenance']='640 objetos con coincidencia nominal exacta MAX; otros 2 con nombres fuente duplicados y sufijo .001; OBJ separado por nombre exacto y declaración del usuario. No equivale a validación íntegra de geometría.'
    r['scope']['verified_provenance_counts']=dict(collections.Counter(o['provenance']['subset'] for o in r['objects']))
    for m in r['materials']:
        for a in m['assignments']:
            if a['subset']=='MAX_candidate':a['subset']='MAX'
    metrics={k:sum(o['mesh'][k] for o in meshes) for k in ['vertices','polygons','triangles','boundary_edges','nonmanifold_edges_gt2','loose_vertices','degenerate_polygons']}
    r['summary']=dict(max_geometry=metrics,max_materials=len(materials),
        uv_layer_counts=dict(collections.Counter(len(o['mesh']['uv_layers']) for o in meshes)),
        shared_materials=[m['name'] for m in materials if any(a['subset']=='legacy_OBJ' for a in m['assignments'])],
        missing_material_objects=[o['name'] for o in meshes if not o['material_slots']],
        no_uv_objects=[o['name'] for o in meshes if not o['mesh']['uv_layers']],
        lights_source=[n for n in nodes if n['super_id']=='0x30'],
        cameras_source=[n for n in nodes if n['super_id']=='0x20'],
        source_metadata=[h['text'] for s in r['max_binary']['strings'] if 'DocumentSummary' in s['stream'] for h in s['hits'] if re.match(r'(Vertices|Faces|Objects|Shapes|Lights|Cameras|3ds Max Version):',h['text'])])
    files={f['name'].casefold():f for f in r['texture_files']}
    paths=sorted({h['text'] for s in r['max_binary']['strings'] if s['stream']=='FileAssetMetaData2' for h in s['hits'] if re.search(r'\.(png|jpe?g|tif|tga)$',h['text'],re.I)})
    assets=[]
    for p in paths:
        b=basename(p);candidate=files.get(b) or files.get(rename(b))
        assets.append(dict(original_path=p,basename=b,status='same_basename' if b in files else 'renamed_candidate' if candidate else 'absent_in_originales',
            candidate_path=candidate['path'] if candidate else None,
            evidence='Nombre y decodificación local; no checksum del bitmap original MAX.' if candidate else 'No hay coincidencia exacta ni cambio punto-guion bajo entre los 104 archivos locales. Uso activo no probado.'))
    r['texture_reconciliation']=dict(max_metadata_paths=assets,
        unique_basenames=len({a['basename'] for a in assets}),
        missing_basenames=sorted({a['basename'] for a in assets if a['status']=='absent_in_originales'}),
        unique_status_counts=dict(collections.Counter(next(a['status'] for a in assets if a['basename']==b) for b in {a['basename'] for a in assets})),
        local_extras=sorted(set(files)-{rename(a['basename']) for a in assets}))
    poser=r['poser']['materials'];comparisons=[]
    explicit={'doorpanel01':'DoorPanel','chairgray':'Chair_Grey','voygray':'Floor','metalsteelplate':'Helm_MetalPlating'}
    for m in materials:
        name=clean(m['name']);stem=name.split('_scn')[0]
        if stem.startswith(('$','(')):stem=stem[1:]
        if stem.startswith('6light'):stem=stem[1:]
        candidates=[p for p in poser if key(p['name'])==key(stem)]
        evidence='Coincidencia nominal normalizada; no prueba de equivalencia de shader.'
        if not candidates:
            base=re.sub(r'_(?:BURLAP01|LEATH01|Metal_Co|VP_col|Voygray|n011|DP_01|alumb_t|MVS)$','',stem,flags=re.I)
            candidates=[p for p in poser if key(p['name'])==key(base)]
            if candidates:evidence='Nombre base tras sufijo bitmap del importador; referencia textual al recurso.'
            elif key(base) in explicit:
                candidates=[p for p in poser if p['name']==explicit[key(base)]]
                evidence='Candidato por función/nombre y referencia de textura; no equivalencia nominal exacta.'
        if 'blue glow' in stem:
            candidates=[p for p in poser if p['name'] in ['Light_Blue_Center','Light_Blue_Aft']]
            evidence='Hipótesis funcional: glow azul MAX frente a dos zonas Poser; asignación exacta pendiente.'
        elif 'white to blue' in stem:
            candidates=[];evidence='Gradiente MAX sin contraparte inequívoca MC6.'
        v=inputs(m);matches=[]
        for p in candidates:
            pp=props(p)
            rgb=[float(x) for x in pp['KdColor'].split()[:3]] if 'KdColor' in pp else None
            matches.append(dict(poser_material=p['name'],line=p['line'],properties=pp,
                kd_raw_numeric_match=bool(rgb and all(abs(a-b)<1e-5 for a,b in zip(v.get('Base Color',[0,0,0])[:3],rgb))),
                ambient=[i for i in p['inputs'] if 'Ambient' in i['header']],texture_references=p['texture_references']))
        comparisons.append(dict(blender_material=m['name'],base_color=v.get('Base Color'),roughness=v.get('Roughness'),metallic=v.get('Metallic'),
            alpha=v.get('Alpha'),emission_color=v.get('Emission Color'),emission_strength=v.get('Emission Strength'),
            evidence=evidence,poser_candidates=matches,fully_recovered=False,
            limitation='La igualdad numérica no implica igualdad de espacio de color, modelo de reflexión, iluminación o respuesta visual.'))
    r['material_comparisons']=comparisons
    source_deltas=[]
    for n in nodes:
        raw=n.get('raw_geometry')
        if raw and source_names[n['name']]==1 and n['name'] in objects:
            blend_mesh=objects[n['name']].get('mesh')
            if blend_mesh and raw['faces']!=blend_mesh['polygons']:
                source_deltas.append(dict(object=n['name'],source_reader_faces=raw['faces'],blender_faces=blend_mesh['polygons'],
                    difference=raw['faces']-blend_mesh['polygons'],repeated_vertex_faces=raw['repeated_vertex_faces'],duplicate_vertex_sets_faces=raw.get('duplicate_vertex_sets_faces')))
    r['source_geometry_comparison']=dict(objects_with_face_count_difference=source_deltas,
        net_face_difference=sum(d['difference'] for d in source_deltas),
        limitation='Nombres únicos y lector parcial; las diferencias no prueban por sí solas qué operación las produjo.')
    rails=['Mesh1372','Mesh1373','Mesh1374','Mesh1375','Mesh1376',*[f'Mesh{i}' for i in range(1324,1333)],*[f'Mesh{i}' for i in range(1387,1404)]]
    roles=[
        dict(role='Suelo central y escalones',objects=['Mesh1500','Mesh1715','Mesh566'],confidence='verificado por geometría y vista aislada',evidence='Planos horizontales y bastidor central; materiales Voygray y Brushed_Aluminium.'),
        dict(role='Suelo de pasillos/plataforma exterior',objects=['hallwayfloor','Mesh1497','floorfront'],confidence='parcial',evidence='hallwayfloor tiene superficie de 16 m²; floorfront y Mesh1497 conservan muchos vértices sin cara y requieren investigación de contornos.'),
        dict(role='Paneles del suelo y cubierta',objects=['Mesh468','Mesh1206'],confidence='geometría verificada; función óptica de cubierta pendiente',evidence='35 paneles del suelo; Mesh1206 cubre todos los centroides a 8,017 mm. Material #122 opaco actual.'),
        dict(role='Paneles azules de techo',objects=[f'Object{i:03}' for i in range(28,50)],confidence='verificado',evidence='Material light blue glow; Z entre 4,1566 y 4,4741 m; anillo perimetral en vista aislada.'),
        dict(role='Elementos glow inferiores',objects=[a['object'] for m in materials if 'blue glow 2' in m['normalized_name'] for a in m['assignments'] if a['subset']!='legacy_OBJ'],confidence='geometría y asignación verificadas; función individual parcial',evidence='17 objetos distribuidos en bases, frentes y consolas; alturas distintas. No son todos paneles de techo.'),
        dict(role='Techo y luminarias centrales',objects=['Mainroof','centerlight','centerlights01','Centerpiece','blackinset','centerinset','lightsring02','lightring03','lightringback','lightssupport','Mesh86'],confidence='verificado',evidence='Techo, anillos y domo por nombres, cotas y vistas; Mesh86 es plano superior con Window.'),
        dict(role='Barandillas y soportes centrales',objects=rails,confidence='verificado por vista aislada',evidence='31 piezas; cinco pasamanos y soportes de Brushed_Aluminium. Otros usuarios del material no son necesariamente barandillas.'),
        dict(role='Carcasas de consolas',objects=['Mesh1114','Mesh1119','Mesh1127','Mesh1133','Mesh1340','Mesh1717','Plane083','Plane084'],confidence='verificado por grupo aislado; nombres de estaciones pendientes',evidence='Carcasas con DimGray; superficies de pantalla inventariadas por material en anexo.'),
        dict(role='Sillones centrales',objects=['Box001','Box003','Box004','Box005','Armrest01','Armrest02','Armrest03','Armrest04'],confidence='verificado por vista aislada',evidence='Dos sillones centrales con cuero Leather2 y cuatro apoyabrazos.'),
        dict(role='Asientos de estaciones',objects=['ChamferBox','ChamferBox001.001','ChamferBox002','Layer:0','Layer:001','Layer:002'],confidence='verificado por geometría y parentesco',evidence='Tres grupos de sillas Group009, Group008, Group003; componentes MSB y Object asociados a estos padres.'),
        dict(role='Puertas y hojas',objects=['door01',*[o['name'] for o in meshes if o['parent'] and o['parent'].startswith('door')]],confidence='verificado por jerarquía; ensamblaje completo pendiente',evidence='Grupos door3, door4, door04–door07 y sus hijos; Doorpanel01–04 son controles pequeños.'),
        dict(role='Controles de puertas',objects=[f'Doorpanel{i:02}' for i in range(1,5)],confidence='verificado',evidence='Material Doorpanel01_DP_01 y dimensiones pequeñas; no confundir con hojas.'),
    ]
    for role in roles:role['objects']=sorted(set(role['objects']))
    r['piece_roles']=roles
    r['diagnoses']=[
        dict(priority=1,issue='Materiales MAX sin texturas y emisión desactivada',evidence='90 materiales usados, cero nodos ShaderNodeTexImage, Emission Strength=0 en todos.',confidence='verificado'),
        dict(priority=1,issue='Paneles del suelo cubiertos por material opaco',evidence='Mesh1206, Alpha=1 y Transmission Weight=0; rayos +Z desde 2172 centroides de Mesh468 encuentran Mesh1206 a 0,008017 m.',confidence='muestreo geométrico verificado; resultado óptico condicionado por normales/culling'),
        dict(priority=1,issue='Contornos de suelo sin superficie completa',evidence='floorfront: 593/606 vértices sin cara; Mesh1497: 531/633. Revisar lectura de polígonos y contornos, sin borrar vértices.',confidence='defecto de superficie Blender verificado; origen pendiente'),
        dict(priority=2,issue='Iluminación y cámaras ausentes',evidence='MAX: 8 luces, 17 cámaras; Blender: 0 y 0.',confidence='clases y metadatos verificados'),
        dict(priority=2,issue='Mallas alejadas del puente',evidence='Mesh992 y Mesh993, hijas de Group006/007, cotas máximas 17,641/17,993 m.',confidence='posición verificada; causa no confirmada'),
        dict(priority=2,issue='Cinco recursos MAX no disponibles localmente',evidence=r['texture_reconciliation']['missing_basenames'],confidence='ausencia en originales verificada; uso activo no confirmado'),
    ]
    r['future_export']=dict(status='No se ha exportado ningún modelo.',rob3d='No hay Rob3D ni contrato de exportación suministrado en este directorio; capacidades y versión no verificadas. No se ha modificado ningún repositorio externo.',
        required=['Selección explícita de 642 objetos MAX; excluir OBJ incluso si no queda oculto al abrir en background.',
            'Verificar superficie de suelos, normales y transformaciones antes de decidir escala UE.',
            'Preservar slots, UV, jerarquías de puertas y nombres fuente en mapa estable.',
            'Transportar texturas resueltas y crear parámetros PBR/emisión en UE; validar con exportación de prueba autorizada.',
            'Definir colisiones, pivotes, piezas interactivas y presupuesto de draw calls por estación.'],
        references=[dict(title='Epic: FBX Static Mesh Pipeline',url='https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine'),
            dict(title='Epic: Emissive Material Input',url='https://dev.epicgames.com/documentation/unreal-engine/using-the-emissive-material-input-in-unreal-engine'),
            dict(title='Epic: Lumen Global Illumination',url='https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine')])
    return r


def write_report(r,root):
    root=Path(root);out=root/'informes';obj={o['name']:o for o in r['objects']};s=r['summary'];g=s['max_geometry'];legacy=obj['Voyager Bridge']
    files=r['texture_files'];m468=obj['Mesh468'];cov=obj['Mesh1206'];recon=r['texture_reconciliation']
    maxm=[m for m in r['materials'] if any(a['subset']!='legacy_OBJ' for a in m['assignments'])]
    missing='\n'.join('- `'+n+'`.' for n in recon['missing_basenames'])
    def rows(items):return '\n'.join('| '+' | '.join(str(x).replace('\n',' ') for x in row)+' |' for row in items)
    def group_names(m):return ', '.join('`'+a['object']+'`' for a in m['assignments'] if a['subset']!='legacy_OBJ')
    role_rows=rows((p['role'],', '.join('`'+n+'`' for n in p['objects']),p['confidence']+'. '+p['evidence']) for p in r['piece_roles'])
    date=(datetime.datetime.fromisoformat(r['generated_utc'])+datetime.timedelta(hours=2)).strftime('%d/%m/%Y %H:%M')
    report=f'''# Auditoría técnica de la USS Voyager — Misión 1

Fecha: {date} (Europe/Madrid). Auditoría de solo lectura del BLEND de trabajo, MAX 2011, MC6 y texturas suministradas.

## Diagnóstico principal

Se ha recuperado un conjunto separable de **631 mallas MAX y 11 empties**, pero su apariencia no está restaurada: los **90 materiales usados por esas piezas no tienen nodos de textura y todos tienen Emission Strength=0**. Las 49 imágenes de archivo del BLEND tienen rutas rotas y ningún contenido empaquetado. Los **104 archivos de textura disponibles se decodifican correctamente** en Blender, por lo que gran parte del trabajo visual es recuperable a partir de los recursos locales.

Hay además problemas de superficie y ensamblaje que impiden declarar la geometría completa: `floorfront` conserva 606 vértices pero sólo una cara minúscula, `Mesh1497` tiene 531 vértices sin cara, y dos mallas están muy alejadas del puente. La comparación del MAX es parcial y no certifica equivalencia geométrica ni visual completa.

**Mesh468 son 35 paneles planos del suelo**, no el suelo completo. Sus caras miran hacia −Z; la cubierta `Mesh1206` está 8,017 mm encima, comparte la planta de los paneles y actualmente tiene un material opaco. Activar emisión en Mesh468, por sí solo, no resuelve este conjunto.

## Integridad, alcance y reproducción

Se calcularon tamaño, fecha de modificación en nanosegundos y SHA-256 de los **{len(r['input_manifest'])} archivos de originales**, antes y después. Resultado: **sin cambios**. El JSON conserva ambos manifiestos. No se guardó el BLEND, no se exportaron GLB/FBX, no se eliminaron ni fusionaron objetos y no se editaron materiales, colores ni repositorios externos.

Blender verificado: `{r['blender']['version']}`, build `{r['blender']['build_hash']}`. Ejecución background con `--factory-startup --disable-autoexec`; apertura mediante `open_mainfile(use_scripts=False, load_ui=False)`. La preferencia de ejecución automática observada fue `{r['blender']['autoexec_preference']}`. Los scripts de diagnóstico calculan cachés de triangulación y cargan imágenes temporales para comprobar decodificación, sin alterar los datablocks originales de imagen. Las vistas usan una escena/cámara temporal Workbench y un modo de visualización monocromo; no prueban los colores ni el render del modelo original.

Desde el directorio de trabajo, ejecutar en PowerShell:

```powershell
& 'C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe' --background --factory-startup --disable-autoexec --python-exit-code 1 --python 'scripts\\auditoria_voyager.py'
```

`scripts/informe_auditoria.py` genera la síntesis Markdown y enriquece el JSON. `scripts/vistas_diagnostico.py` genera sólo PNG de diagnóstico; `scripts/resumir_auditoria.py` facilita consultas al inventario. No hay que ejecutar los scripts incrustados del BLEND.

## Inventario y separación del OBJ

| Dato | Escena global | Conjunto MAX | OBJ antiguo |
|---|---:|---:|---:|
| Objetos | 643 | 642 | 1 |
| Mallas | 632 | 631 | 1 |
| Empties | 11 | 11 | 0 |
| Vértices | {g['vertices']+legacy['mesh']['vertices']:,} | {g['vertices']:,} | {legacy['mesh']['vertices']:,} |
| Polígonos | {g['polygons']+legacy['mesh']['polygons']:,} | {g['polygons']:,} | {legacy['mesh']['polygons']:,} |
| Triángulos de Blender | {g['triangles']+legacy['mesh']['triangles']:,} | {g['triangles']:,} | {legacy['mesh']['triangles']:,} |

Se encontraron **171 materiales**, frente a los aproximadamente 172 indicados previamente; es el recuento real de este archivo. Hay 51 datablocks de imagen: 49 de archivo más `Render Result` y `Viewer Node`. Hay una escena, una colección (`Collection`), ningún enlace de biblioteca y ningún modificador en las 631 mallas MAX. El inventario JSON conserva también jerarquías, visibilidad, propiedades personalizadas, atributos, UV y asignaciones de material por cara.

La malla OBJ se identifica inequívocamente como el objeto exacto **`Voyager Bridge`**, separado en todas las estadísticas, búsqueda de piezas y pruebas de rayos. Tiene 102 slots de material y dimensiones aproximadas 13,150 × 13,011 × 3,840 m. No se usó su geometría como fuente para localizar las piezas MAX.

El lector parcial del MAX encuentra 640 nombres de objetos Blender exactamente. Los otros dos son `ChamferBox001.001` y `hallwaysupports01.001`: existen dos nodos MAX con cada nombre base. El sufijo distingue duplicados nominales, no prueba duplicación geométrica. No se puede identificar cuál de los dos nodos fuente corresponde a cada instancia sólo por el nombre. El registro `provenance` conserva esta limitación.

**22 materiales tienen caras asignadas tanto al OBJ como al conjunto MAX**. Una restauración posterior deberá aislar esa dependencia antes de editar. La antigua malla tiene `hide_viewport=False`, `hide_render=False` y aparece visible al cargar este BLEND en el proceso de auditoría. Esto no informa sobre un ocultamiento temporal/local en una sesión interactiva; la exclusión de exportación debe hacerse por identidad explícita y no depender de la visibilidad.

## Piezas localizadas y prioridad

Las identificaciones físicas se contrastaron con cotas, asignaciones y vistas de geometría aislada. Las etiquetas de estación concreta (seguridad, ciencia, ingeniería, etc.) siguen pendientes cuando sólo hay nombres `Mesh/Plane/Object`.

| Familia | Objetos | Evidencia y alcance |
|---|---|---|
{role_rows}

Vistas: [corte inferior](vistas/max_corte_inferior.png), [suelo y estructura](vistas/suelo_estructura.png), [barandillas](vistas/barandillas.png), [consolas DimGray](vistas/gris_dimgray.png), [sillones y tapizado](vistas/sillones_materiales.png), [exterior y piezas alejadas](vistas/max_exterior.png). El corte selecciona piezas cuya cota máxima es inferior a 2,5 m; una pieza ausente de esa imagen puede existir en la escena completa.

## Mesh468: geometría, material y cubierta

| Propiedad | Valor verificado |
|---|---|
| Origen del objeto | (2,847747; −3,199653; −0,025731) |
| Rotación / escala | (0, 0, 0) / (0,320695877; 0,320695877; 0,320695877) |
| Caja mundial de geometría | X −4,723806 a 4,515859; Y −4,567110 a 1,100726; Z −0,025746882 |
| Dimensiones mundiales | 9,239665 × 5,667836 × 0 m |
| Centro de la caja | (−0,103974; −1,733192; −0,025747), distinto del origen del objeto |
| Geometría | 2.242 vértices; 4.379 aristas; 2.172 caras triangulares |
| Componentes conectados | 35, sin vértices sueltos |
| Área sumada de superficie | 8,192385 m² |
| Material | Un slot; nombre exacto JSON `\\u001clight floor\\u0003`; 2.172 caras asignadas |
| Normales | 2.172 caras hacia −Z; determinante de transformación positivo |
| Topología | 2.242 aristas de borde; 0 aristas con más de dos caras; 0 caras degeneradas |
| UVMap | U −2871,443 a −1737,140; V 1833,406 a 2529,215; valores finitos |

La planta aislada confirma paneles con esquinas redondeadas, triángulos y trapecios, dispuestos en arco con dos ramales. La superficie no tiene espesor. Las UV están muy fuera de 0–1: no impiden un material uniforme, pero una nueva textura requerirá validar su escala y repetición.

![Mesh468: planta geométrica](vistas/mesh468_planta.png)

La pieza superior **Mesh1206** tiene 2.270 vértices, 2.207 triángulos y 35 componentes; prácticamente la misma planta y área. Z ≈ −0,0177298 m. Los rayos hacia +Z desde **los 2.172 centroides de triángulo** de Mesh468 encuentran Mesh1206 a 0,00801723–0,00801730 m, dentro de un alcance de 5 cm. Es un muestreo de cobertura geométrica, no una intersección exacta ni un render de transmisión.

Su único material es el nombre exacto ` Material #122\\u0003`: Base Color blanco, Alpha=1, Transmission Weight=0 y Emission Strength=0. Sus caras también apuntan hacia −Z. Es **hipótesis fuerte** que sea una cubierta de los paneles; no se ha demostrado su material óptico original. `Glass_Floor_Light` del MC6 ofrece una referencia candidata (transparencia 0,9), pero la igualdad de pieza/material entre formatos no está probada. En Blender el culling del material está desactivado; la futura exportación debe resolver tanto normales como cubierta y transparencia.

## Suelos y defectos geométricos reales

`floorfront` no debe considerarse un suelo recuperado por su nombre ni por su caja de vértices: de 606 vértices, **593 no participan en ninguna cara**. Su única cara usa 13 vértices y suma sólo **0,000133254 m²** según la triangulación de Blender. La caja de todos los vértices mide 19,831 × 9,868 m, pero la caja de su superficie es sólo 0,411 × 0,046 m. El JSON distingue `bounds_world` y `bounds_surface_world`.

`Mesh1497` conserva 633 vértices, 14 caras y **531 vértices sin cara**. Su caja de vértices tampoco certifica una plataforma rellena. `hallwayfloor` sí contiene una cara de 363 vértices (361 triángulos, ≈16 m²); esa gran cara requiere comprobar triangulación y colisión. `Mesh1500` es un plano central de ≈28,458 m² a Z≈0,190723 m, con 372 de 373 caras orientadas hacia −Z. `Mesh1715` es un plano inferior de ≈10,235 m² a Z≈−0,434634 m. `Mesh566` aporta bastidor y escalones.

El conjunto MAX presenta **{g['loose_vertices']:,} vértices sin cara, {g['degenerate_polygons']:,} caras de área local inferior a 1e−12 y {g['nonmanifold_edges_gt2']:,} aristas usadas por más de dos caras**. Hay {g['boundary_edges']:,} aristas de borde; muchas pertenecen a planos abiertos deliberados y no son defectos por sí mismas. Los recuentos no constituyen una certificación de manifold: no se examinan todas las autointersecciones, winding ni solapamientos exactos. No se aplicó `mesh.validate()` a ninguna malla de la escena.

La lectura previa a validación aporta una evidencia concreta: `floorfront` tiene en el lector MAX dos caras, una de **604 índices con vértices repetidos** y otra de 13. El BLEND conserva sólo la de 13. Para `Mesh1497`, el lector encuentra 15 caras, incluida una de **553 índices con repeticiones**; Blender conserva 14. `Mesh69` pasa de 235 caras leídas a 233, con dos caras de índices repetidos. Es compatible con el rechazo de contornos que MAX permite representar y Blender no acepta como un polígono simple. La causa exacta no se certifica sin el registro de importación o una prueba posterior autorizada sobre una copia. La información de vértices aún conservada puede ser útil para reconstruir esos contornos; no debe eliminarse.

En 19 objetos con nombre fuente único hay diferencias de caras frente al lector, que suman **190 caras menos en Blender**. Destacan Centerpiece (8.447 → 8.342), centerRA (634 → 605) y Mainroof (14.454 → 14.447); el lector cuenta siete conjuntos de vértices de cara duplicados en Mainroof. La lista completa está en `source_geometry_comparison`. Son diferencias comprobadas con ese lector, no una afirmación de que todas esas caras deban reinstalarse: algunas pueden ser duplicados o contornos incompatibles.

590 mallas tienen una capa UV; 41 no tienen ninguna. No se encontraron UV no finitas. No hay segunda capa UV registrada para lightmaps. `Mesh551` está vacía; `Mesh150`, `Mesh72` y `Mesh73` no tienen slots de material. La ausencia de UV no obliga a corregir una pieza que vaya a usar material uniforme.

`Mesh992` (Group006) tiene centro (−21,360; 3,252; 16,611) m y `Mesh993` (Group007), (−19,024; 5,786; 16,898) m. Son piezas reales presentes, muy fuera del volumen principal. Sus padres y transformaciones se conservan; no se ha demostrado si el desplazamiento procede del MAX, del importador, del ensamblaje o de una edición posterior. **No ajustar toda la escena usando la caja global ni moverlas automáticamente.** Las unidades declaradas son METRIC, scale_length=1, METERS; eso no certifica la escala física del puente ni su equivalencia con el OBJ antiguo.

## Materiales luminosos y demás shaders

Los nombres originales con caracteres de control se conservan íntegros en JSON. Se detectaron ocho nombres con controles. Algunos dejan prefijos imprimibles (`$`, `(`, `6`) tras limpiar los controles: no se renombraron ni se consideraron contenido semántico fiable. El MAX contiene cadenas limpias `light floor`, `light blue glow`, `light blue glow 2` y `light white to blue glow`.

| Material prioritario | Asignación física | Propiedades Blender verificadas |
|---|---|---|
| light floor | Mesh468, 2.172 caras | Base Color (0,7; 0,5; 0,2), Roughness=1, Metallic=0, Alpha=1; emisión negra y fuerza 0 |
| light blue glow | Object028–Object049, 22 paneles del techo | Mismas propiedades y sin texturas |
| light blue glow 2 | 17 piezas inferiores enumeradas en tabla/anexo | Mismas propiedades; no agruparlas como techo |
| light white to blue glow | centerlight, sólo 64 de sus 2.688 caras | Mismas propiedades; no hay nodos que produzcan un gradiente blanco–azul |
| Material #122 | Mesh1206, cubierta de paneles | Blanco, Alpha=1, Transmission Weight=0; emisión 0 |
| lights con controles | centerlights01, lightringback, Mesh03, Mesh499, Mesh513 | Color (0,7; 0,5; 0,2), emisión 0 |
| Lights | 13 piezas: Mesh451–Mesh498 según inventario | Color ≈(1; 0,972549; 0,913726), emisión 0; distinto datablock del anterior |
| light white on to off | lightring03, lightsring02, Object060 | Fuerza de emisión 0; no hay animación de encendido/apagado en objetos auditados |
| Light TL | Mesh20, 108 caras | Color naranja ≈(1; 0,54902; 0), emisión 0 |

Siete materiales MAX repiten el color (0,7; 0,5; 0,2), incluidas luces y `Brushed_Aluminium`; ese valor está verificado en Blender, **no validado como apariencia original**. Los 90 materiales MAX tienen sólo Principled/Output y, en seis casos, un Normal Map cuyo Color no está conectado a una imagen. Son `fabric brown_BURLAP01`, `Leather2_LEATH01`, `Leather_LEATH01`, `Metal_Co_Metal_Co`, `Plaque_VP_col` y `Voygray_Voygray`. No hay recuperación efectiva de esos mapas normales por el mero hecho de existir el nodo.

Las **50 instancias de nodo Image Texture** de la escena están en materiales asociados al OBJ antiguo, no en los shaders usados por MAX. Por tanto, reenlazar las imágenes existentes no basta para restaurar los materiales MAX: hay que reconstruir sus conexiones. No se declara ningún material MAX plenamente recuperado.

## Comparación con Poser MC6

Se analizaron **142 definiciones** mediante lectura de llaves, propiedades y árboles de shader con números de línea. Sus **54 nombres de textura distintos** tienen archivos locales exactos y decodificables. El MC6 es una variante Poser: sus parámetros y nombres sirven de evidencia, pero no sustituyen automáticamente el shading mental ray del MAX.

| Comparación | Coincidencia verificada | Diferencia o incertidumbre |
|---|---|---|
| light floor ↔ Light_Floor (línea 48507) | Nombre funcional compatible; MC6 KdColor blanco, KaColor blanco; sin mapas | Blender es ocre y emisión 0. MC6 Ambient_Value=0: KaColor blanco por sí solo **no demuestra emisión efectiva** ni su intensidad |
| Mesh1206 ↔ Glass_Floor_Light (línea 7785) | MC6 KdColor≈0,054902 y tMin=tMax=0,9 | Candidato por función; material MAX de cubierta original no recuperado ni identificado inequívocamente |
| blue glow ↔ Light_Blue_Center/Aft (líneas 18423/30189) | MC6 declara KdColor blanco y Ambient_Color azul | Ambient_Value=0 en ambos. La relación exacta con los paneles MAX es hipótesis; no trasladar esos valores como emisión activa |
| Mainscreen_MVS ↔ MainScreen (8385) | MVS.jpg está en MC6, metadatos MAX y carpeta local; geometría Object074 | Blender sin textura conectada y color base negro; MC6 KdColor blanco. Correspondencia de recurso, no shader completo |
| scrn1.1_scn1.1 ↔ Scrn1_1 (47615) | Cambio sistemático scn1.1.png → scn1_1.png; MC6 apunta al archivo local | Blender sin imagen conectada y color negro; MC6 mapa en Diffuse_Color. Las variantes _i no están conectadas en MAX importado |
| fabric brown_BURLAP01 ↔ Fabric_Brown (18723) | BURLAP01.JPG nombrado en MC6 y sufijo material MAX | Propiedades y mapas normales requieren reconstrucción; verificar tapizado mediante render |
| Leather/Leather2 ↔ Leather/Leather2 (29743/19169) | LEATH01.JPG disponible y referenciado | Shaders MAX sin imagen; Normal Map con color constante no recupera relieve |
| Plaque_VP_col ↔ Plaque (3447) | VP_col.png/VP_bump.png disponibles y documentados en recursos | MC6 no tiene textureMap en la propiedad principal y usa VP_bump en Bump/Gradient_Bump; no asumir idéntico esquema MAX |
| Brushed_Aluminium ↔ Railing (9) | Geometría de barandillas aislada; MC6 define Railing | Nombres de materiales diferentes y color distinto. Equivalencia funcional candidata, sin mapa de materiales 1:1 probado |
| Window ↔ Glass_Ceiling (10477) | Window asignado a Mesh86, plano de techo; MC6 contiene vidrio de techo | Window Alpha≈0,2 y Transmission=0; MC6 transparencia 0,9. Comparación funcional, no shader equivalente |

El anexo enumera los 90 materiales MAX con sus candidatos MC6, propiedades verificadas y objetos usuarios. La coincidencia numérica de Kd no acredita recuperación completa: no se ha validado equivalencia entre espacios de color, exponentes de brillo Poser y roughness PBR, reflexión, refracción ni render.

## Texturas: enlaces, empaquetado, candidatos y ausencias

| Estado | Cantidad | Interpretación |
|---|---:|---|
| Archivos locales de textura | 104 | Todos decodificados en imágenes temporales de Blender; tamaño, profundidad y hash en JSON |
| Imágenes FILE registradas en BLEND | 49 | Todas sin datos de píxeles y rutas inexistentes `//VOYBRIDGETEX-1\\Textures\\...` |
| Imágenes correctamente enlazadas y decodificadas | 0 | No hay enlace de archivo válido en el BLEND auditado |
| Imágenes empaquetadas | 0 | No hay copia recuperable dentro del BLEND |
| Candidatos locales de igual nombre para imágenes BLEND | 10 | alumb_t, BURLAP01, DP_01, LEATH01, Metal_Co, n011, scn8, scn9, Voygray, VP_col |
| Candidatos con punto cambiado a guion bajo | 39 | scn1.1 → scn1_1, scn10.1 → scn10_1, etc.; no son una ausencia real de archivo |
| Buffers de render/compositor | 2 | Render Result y Viewer Node; no contarlos como texturas faltantes |
| Nombres únicos bitmap en metadatos MAX | {recon['unique_basenames']} | 22 con igual basename y 78 candidatos renombrados; 5 sin candidato |

Los candidatos renombrados se apoyan también en referencias del MC6 al nombre con guion bajo. Se ha verificado existencia y decodificación, **no identidad byte a byte con el bitmap original del MAX**: el MAX referencia rutas, no aporta un checksum original utilizable para esta comparación. Los archivos `_i`, BM_NRM.tif, BM_DISP.tif, VP_bump.png, BNC.png, MVS.jpg, XYT.jpg y otros están disponibles aunque no aparezcan como imagen conectada en el conjunto MAX.

Los cinco recursos sin candidato en `originales` son:

{missing}

Están referenciados en `FileAssetMetaData2`; su ausencia local es real dentro del paquete auditado, pero **no se ha probado que todos estén activos en el render original**. El filtro glare corresponde por nombre a un efecto de cámara; los JPG alternativos no deben sustituirse por pantallas PNG sin comprobación. Los recursos locales adicionales respecto a esos basenames son `alumin.JPG`, `Map__2_Gradient.tga`, `Metal_Al.jpg` y `VP_Spec.png`. Son candidatos útiles para investigación, no mapas ya asignados.

## Qué permite afirmar el MAX y qué limita el importador

El MAX es un contenedor CFB/OLE con diez streams. Se inspeccionaron nombres, tamaños, hashes y cadenas legibles; se recorrieron parcialmente nodos, clases y referencias con el **importador instalado io_scene_max 1.9.2**, hash de código `{r['max_partial_reader']['sha256']}`. No se llamó a `load`, `read`, `make_scene`, `create_shape` ni otras rutinas que construyen una escena. El JSON conserva posibles errores del lector (en esta ejecución: {len(r['max_partial_reader']['errors'])}).

Metadatos del MAX:

{chr(10).join('- `'+v+'`.' for v in s['source_metadata'])}

El lector encuentra **671 nodos con nombre**: 631 entradas geométricas/principales (incluidas 89 envolturas 0x2032), 11 dummies, 17 cámaras, cuatro targets de cámara y ocho luces. Los targets tienen super_id 0x10 y GUID 0x1020; no deben contarse como mallas. Las 17 cámaras más targets y ocho luces explican 29 nodos fuente ausentes, junto con los dos duplicados nominales diferenciados por Blender.

Las luces originales identificadas son: `mr Area Omni001`, `Fspot001`, `Fspot002`, `Fspot003`, `Omni002`, `Omni003`, `Omni004`, `Omni005`. No se recuperaron intensidades, unidades, sombras, render shaders ni equivalencia óptica. Las cámaras conservadas sólo como evidencia de nombres/clases incluyen estaciones, turbolift y vista frontal; no están en Blender.

La comparación 188.929 vértices / 221.871 caras / 635 objetos del resumen MAX frente a 184.697 / 212.147 / 631 mallas de Blender tiene diferencias de 4.232 vértices, 9.724 caras y cuatro objetos. **Son indicadores para investigar, no prueba de cuatro mallas concretas perdidas**: los resúmenes pueden incluir evaluación de modificadores o conteos con convenciones distintas, y no se ha certificado que sus cifras sean actuales. El conteo de triángulos Blender no debe compararse directamente con “Faces” sin saber qué cuenta MAX.

Limitaciones verificadas en el código local `import_max.py`:

1. `SKIPPABLE` (líneas 82–100) incluye cámaras, targets, Omni y Free Direct. `create_mesh` (2156–2191) sólo crea tipos soportados y omite otros; no crea luces/cámaras. La ausencia de esos elementos en Blender no demuestra que faltaran en el MAX.
2. `get_arch_material` (1579–1587) sólo extrae diffuse/specular/shinines. No convierte mapas, emisión, falloff o árboles completos de Arch & Design. El lector encuentra Arch & Design en Mesh468, centerlight, barandillas y otros objetos; los materiales luminosos no han recuperado su comportamiento.
3. `adjust_material` (1671–1712) construye Principled, carga algunos bitmaps, normal y transparencia; asigna emission_color pero **no emission_strength**. Usa además `blend_method='HASHED'`, una ruta que debe contrastarse con la API actual antes de una nueva importación. No se conservan logs de la importación original para demostrar qué errores ocurrieron entonces.
4. `create_shape` (1865–1885) ejecuta `mesh.validate()` antes de asignar índices de material. Si elimina caras, las longitudes de asignaciones pueden divergir; el código imprime errores de longitud. El caso de contornos/suelos requiere investigación específica. La auditoría no ejecuta esa validación en la escena de trabajo.
5. Las conversiones de UV, índices, primitivas, matrices y pivotes son parciales. El código permite errores por objeto y continúa (`make_scene`, 2223–2228); puede producir una escena aparentemente completa aunque algunos elementos fallen.

`VideoPostQueue` contiene **Lens Effects Glow**, con nombres Floorglow, Blueglow, Redglow, orangeglow y Turbolift Lights. La biblioteca y los metadatos identifican mental ray Renderer. Son referencias verificadas a shaders/postprocesado original: no certifican sus parámetros ni que todos estuvieran habilitados, y no se han recreado en Blender.

## Propuesta ordenada de restauración visual — pendiente de autorización

1. **Preparar una copia de trabajo** fuera de originales y un conjunto explícito MAX. Conservar identidad del OBJ y aislar los 22 materiales compartidos. Guardar correspondencias nombre fuente ↔ nombre limpio ↔ pieza ↔ slot; no fusionar piezas para simplificar nombres.
2. **Resolver geometría crítica antes del look**: recuperar o verificar contornos de floorfront/Mesh1497 desde el MAX, revisar orientación de suelos, investigar Mesh992/Mesh993 y revisar padres/pivotes de puertas. No borrar los vértices sin cara: pueden contener información necesaria para la recuperación.
3. **Preparar un mapa de recursos** sin renombrar originales: enlaces a los 10 nombres exactos y 39 candidatos renombrados, 54 referencias MC6 y bitmaps adicionales MAX. Buscar los cinco ausentes sólo cuando se demuestre uso activo; conservar alternativas marcadas como tales.
4. **Reconstruir un grupo piloto de suelo**: Mesh468 + Mesh1206 + Mesh566 + Mesh1500. Confirmar cubierta, normales, transparencia y material óptico frente a referencias antes de definir emisión. La fuerza y tono luminosos deben comprobarse visualmente; MC6 Ambient_Value=0 no aporta una intensidad activa fiable.
5. **Restaurar pantallas y luminarias**: usar base color y mapas `_i` sólo donde la función del canal se verifique; reconstruir el gradiente white-to-blue, anillos y elementos del turbolift. Separar emisión de material, luces que iluminan y efectos de resplandor.
6. **Restaurar materiales físicos**: tapizados/cuero, metales/barandillas, plaque, vidrio de techo y puertas. Verificar cada shader mediante render con exposición e iluminación controladas, no por nombre o color de viewport.
7. **Comparar vistas fijas del puente** con referencias del original que se dispongan. Registrar qué propiedades coinciden, qué se han aproximado y qué falta. No declarar fidelidad total sin comprobar luces, transparencia, relieve, brillo y textura sobre su geometría real.

## Preparación para Unreal Engine 5 mediante Rob3D

En el directorio auditado no se suministró Rob3D, su configuración, versión ni contrato de exportación; no se ha inspeccionado ni modificado un repositorio externo. Por tanto, no se afirma que transporte materiales, luces, jerarquías o colisiones automáticamente. Estas son condiciones que deberá cumplir una exportación futura autorizada:

- Seleccionar las 631 mallas y 11 empties MAX explícitamente; excluir `Voyager Bridge`. Mantener puertas/controles/estaciones separables para interacción y pivotes correctos. La pérdida de animación original significa que su lógica de juego deberá construirse y comprobarse.
- Resolver suelos, normales y transformaciones antes de decidir escala en centímetros UE. Mantener una medida patrón y un mapa de transformaciones; no usar la caja global afectada por las mallas alejadas.
- Preservar UV activas y slots de material por cara. Hay 41 mallas sin UV y ninguna segunda capa UV en MAX; decidir lightmaps sólo si se van a usar. Preparar colisiones caminables y de puertas independientemente de los planos luminosos.
- Transportar texturas con rutas verificadas y una tabla PBR/emisión/cubierta. No asumir que un shader Blender complejo se importará igual. La ruta FBX de Epic conecta automáticamente sólo ciertos canales, como Color y Normal; otros necesitan revisión y conexiones explícitas. [Documentación oficial de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).
- Reconstruir emisión y bloom con parámetros de material y validar iluminación por separado. Epic documenta Emissive Color HDR y modelos Lit/Unlit; la elección debe corresponder al uso de cada panel. [Emissive Material Input](https://dev.epicgames.com/documentation/unreal-engine/using-the-emissive-material-input-in-unreal-engine). Con Lumen, superficies emisivas demasiado pequeñas/intensas pueden producir ruido; planificar luces complementarias tras una prueba visual. [Lumen](https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine).
- Evaluar rendimiento con 631 mallas, 261.433 triángulos y 90 materiales. Esos números describen el contenido, no los draw calls medidos ni una aprobación de rendimiento. Optimizar sólo después de preservar interacción y apariencia, con pruebas en el hardware objetivo.

No se ha realizado ninguna exportación ni iniciado la restauración. La siguiente fase queda pendiente de autorización del usuario.

## Anexo A — Materiales MAX, propiedades y usuarios

Los prefijos imprimibles de nombres dañados se muestran como existen tras quitar sólo controles. El JSON conserva el nombre exacto escapado. “Candidato MC6” describe una comparación; ningún material tiene validación visual completa.

| Material Blender | Base Color RGB / roughness / alpha | Candidato MC6 | Objetos MAX con caras asignadas |
|---|---|---|---|
'''
    comparisons={x['blender_material']:x for x in r['material_comparisons']}
    for m in maxm:
        v=inputs(m);rgb=', '.join(f'{x:.5g}' for x in v.get('Base Color',[0,0,0])[:3])
        candidates=', '.join(p['poser_material'] for p in comparisons[m['name']]['poser_candidates']) or 'Sin coincidencia inequívoca'
        report+=rows([(clean(m['name']),f'{rgb} / {v.get("Roughness",0):.5g} / {v.get("Alpha",0):.5g}',candidates,group_names(m))])+'\n'
    report+='''
## Anexo B — Evidencia binaria y geometría prioritaria

Los conteos siguientes usan únicamente el lector instalado, antes de construir/validar una malla. No constituyen un parser independiente validado del MAX.

| Objeto fuente | Vértices leídos | Caras leídas | Caras con vértices repetidos | Caras con índices inválidos | Caras Blender |
|---|---:|---:|---:|---:|---:|
'''
    priority_names={'floorfront','Mesh1497','Mesh69','Mesh468','Mesh1206','Mesh1500','Mainroof','Mesh551','Mesh992','Mesh993'}
    for n in r['max_partial_reader']['nodes']:
        if n['name'] not in priority_names:continue
        raw=n.get('raw_geometry')
        if raw:
            report+=rows([(n['name'],raw['vertices'],raw['faces'],raw['repeated_vertex_faces'],raw['invalid_index_faces'],obj[n['name']]['mesh']['polygons'] if n['name'] in obj else 'N/A')])+'\n'
    report+='''
El lector aporta conteos de 630 entradas de malla; la primitiva Torus no se decodificó mediante estas rutinas de malla. Todos los registros, distribuciones de longitud de caras, repeticiones y limitaciones están en `max_partial_reader.nodes` del JSON. El cuadro anterior selecciona los objetos prioritarios.

## Anexo C — Localización de datos detallados

`auditoria_voyager.json` contiene inventario completo, no sólo prioridades:

- `input_manifest`, `integrity`: hashes y prueba de integridad de originales.
- `objects`: cada objeto, su procedencia, jerarquía, transformación, visibilidad, geometría, UV, topología y componentes; `material_faces` aporta número de caras y caja física de cada slot.
- `materials`: propiedades, todos los nodos/sockets, valores, enlaces y alcance del output activo; asignaciones separadas legacy_OBJ/MAX.
- `images` y `texture_files`: enlaces, empaquetado, píxeles, candidatos locales y decodificación de 104 recursos.
- `poser`, `material_comparisons`: 142 materiales con líneas MC6 y comparación explícita de propiedades.
- `max_binary`, `max_partial_reader`: estructura CFB, cadenas, metadatos y clases; errores/limitaciones conservados.
- `source_geometry_comparison`: diferencias de caras por objeto entre el lector MAX y Blender, con alcance limitado explícito.
- `texture_reconciliation`, `mesh468_occlusion`, `piece_roles`, `diagnoses`, `future_export`: conciliación de recursos, prueba de cobertura, piezas y plan de recuperación.

El informe no certifica identificación anatómica de cada una de las 631 mallas, ausencia total de defectos ni reproducción del render mental ray. Sí proporciona el inventario trazable para continuar esa recuperación sin mezclar el OBJ.
'''
    (out/'auditoria_voyager.md').write_text(report,encoding='utf-8')


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    r=enrich(json.loads((root/'informes/auditoria_voyager.json').read_text(encoding='utf-8')))
    write_report(r,root)
    (root/'informes/auditoria_voyager.json').write_text(json.dumps(r,ensure_ascii=True,indent=2,allow_nan=False),encoding='utf-8')
