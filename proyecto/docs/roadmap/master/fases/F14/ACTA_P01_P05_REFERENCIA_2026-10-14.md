# F14 — Acta de preparación autónoma P01–P05 (referencia verificable)

**Fecha:** 14-10-2026.  
**Base auditada:** `Videojuego_StarTrek/main@090b7e0dec7b18623d07527b66c4f1e783b37f27` (F13 fusionada, PR #19).  
**NAP externo observado:** `robdor80/NAP/main@30a0b199fcb3200ce9e4de97944d2ff9fd0c642c`.  
**Madurez de este paquete:** referencia/auditoría reproducible. **No** `UE5_JUGABLE`, no Star Trek Universe Profile instalado en NAP y no producción audiovisual ejecutada.

## 1. Criterio de trabajo

F14 no puede cerrarse rellenando carpetas vacías ni reinterpretando documentación como assets. La preparación conserva cuatro fronteras:

1. el World State y los contratos del juego deciden qué existe; el sistema visual solo lo representa;
2. NAP es autoridad de ciclo de vida cuando existe un perfil/capacidad realmente configurado y ejecutado;
3. derechos/licencias, original y derivado permanecen separados y trazables;
4. funcionamiento en UE5 requiere evidencia de ejecución en el MSI; CI y JSON no lo sustituyen.

No se ha movido ni reescrito material original de `audiovisual/art_direction/`, `assets/`, `audiovisual/audio/`, `audiovisual/presentation/`, `audiovisual/ui/`, `desarrollo/nap/`, `desarrollo/manifests/` ni `desarrollo/validation/fixtures/nap/`.

## 2. Reconciliación con NAP 2.0 — F14-P01

Se congeló una fotografía explícita en `desarrollo/nap/profile/F14_NAP2_COMPATIBILITY_SNAPSHOT_v0.1.json`.

NAP demuestra en el commit observado contratos actuales de Manifest v2, Universe Profile v4, Package Contract v1, routing, integridad SHA-256, ArchiveRoot/ProductionRoot, recuperación y publicación Git explícita. Esa evidencia permite diseñar una futura configuración Star Trek sin copiar el perfil Nimroel.

**No demostrado en esta fase:** que exista un `universe_id=star_trek` instalado/validado en NAP; que GLB, audio o assets UE5 tengan ya un perfil Star Trek operativo; o que una extensión sintácticamente permitida por el Package Contract implique soporte real de conversión/producción.

El fixture `desarrollo/validation/fixtures/nap/sensors_console_tng_v0.1/` sigue siendo un ejemplo físico y reproducible de trazabilidad, expresamente marcado como **no producción artística**.

## 3. Prioridades de producción — F14-P02

`desarrollo/manifests/assets/f14_asset_priority_manifest_v0.1.json` ordena trabajo sin fabricar assets inexistentes:

- prioridad 0: puente Sutherland del vertical slice y superficie interactiva de Sensores;
- prioridad 1: familia NPC Starfleet y primeras familias jugables Oberth/Miranda;
- prioridad 2: Intrepid, Sovereign y referencias Galaxy/Odyssey;
- prioridad 3: nueva Clase Valhalla;
- prioridad 4: expansión de estaciones, planetas y props movida por necesidades reales del mundo.

La prioridad no concede rango, nave ni mando al jugador. Los blueprints siguen siendo referencias, no mallas de producción.

El Sutherland mantiene el estado real ya documentado: hash conocido del original auditado, licencia declarada CC-BY-4.0 pero **derechos aún no verificados de forma independiente**, y UE5 **NO_EJECUTADO** en F07. Ninguna regla F14 promociona esos campos.

## 4. Presentación — F14-P03

`desarrollo/manifests/presentation/f14_presentation_priority_manifest_v0.1.json` separa UI, cámaras, ambiente, SFX, voz, música y variantes por era.

La fotografía actual distingue referencias existentes de binarios de producción. Las carpetas vacías o README no cuentan como voz, música, ambiente o efectos terminados. La cámara/POV y el fixture de Sensores son datos de referencia; requieren implementación y prueba interactiva real antes de hablar de runtime.

Toda futura voz/audio distribuible necesita procedencia y derechos propios; la existencia de un personaje o franquicia no concede derechos sobre una interpretación vocal.

## 5. Optimización — F14-P04

`desarrollo/tools/validation/f14_audiovisual_reference.py` impone, entre otras, estas puertas:

- un original nunca puede ser sobrescrito por un derivado;
- original y derivado deben conservar hashes/identidades separadas;
- no se admite la etiqueta «optimizado» sin métricas runtime positivas;
- LOD y streaming deben constar verificados para una afirmación de optimización;
- incluso con métricas, la salida queda en revisión y no certifica UE5 desde este validador offline.

No se han creado LOD, texturas optimizadas ni derivados 3D reales en este paquete.

## 6. Trazabilidad, recuperación y builds — F14-P05

El validador rechaza como incoherentes:

- cadenas sin asset/source/original hash/manifest/repo externo;
- hashes mal formados;
- afirmaciones de build funcional sin `UE5 EXECUTED` y evidencia asociada;
- afirmaciones de recuperación sin evidencia;
- derechos convertidos automáticamente en permiso de distribución;
- perfiles NAP «instalados» sin referencia de validación runtime.

La futura prueba P05 real deberá enlazar el original concreto, su manifest, su derivado, el registro NAP, la recuperación/reproducción y la evidencia del build UE5 correspondiente.

## 7. Evidencia automatizada

Artefactos añadidos:

- `desarrollo/tools/validation/f14_audiovisual_reference.py`
- `desarrollo/tools/validation/test_f14_audiovisual_reference.py`
- `desarrollo/validation/fixtures/f14/f14_audiovisual_scenarios_v0.1.json`
- `desarrollo/nap/profile/F14_NAP2_COMPATIBILITY_SNAPSHOT_v0.1.json`
- `desarrollo/manifests/assets/f14_asset_priority_manifest_v0.1.json`
- `desarrollo/manifests/presentation/f14_presentation_priority_manifest_v0.1.json`
- `.github/workflows/f14-audiovisual-reference.yml`

Prueba previa a publicación de la rama:

- **43/43 escenarios** pasan;
- **8/8 pruebas unitarias** pasan;
- auditoría del inventario mínimo F14: `REVIEW_REQUIRED`, sin falsa promoción;
- SHA-256 del fixture de escenarios: `70eb7e270c1d3c559803b818b7788a2e8d5e9ad9b797ffe7fee703385ef52beb`.

Comandos reproducibles:

```bash
python -m py_compile desarrollo/tools/validation/f14_audiovisual_reference.py desarrollo/tools/validation/test_f14_audiovisual_reference.py
python -m json.tool desarrollo/validation/fixtures/f14/f14_audiovisual_scenarios_v0.1.json >/dev/null
python desarrollo/tools/validation/f14_audiovisual_reference.py --scenario desarrollo/validation/fixtures/f14/f14_audiovisual_scenarios_v0.1.json --repo-root . --output desarrollo/validation/results/f14_audiovisual_offline_report.json
python -m unittest discover -s desarrollo/tools/validation -p 'test_f14_*.py' -v
```

## 8. Pendientes para madurez real

F14 continúa globalmente **PLANIFICADA**. Para subir de madurez hacen falta evidencias que este trabajo no puede inventar:

- registrar/verificar los assets locales del MSI y sus licencias/atribuciones;
- definir e instalar en NAP el perfil/capacidades Star Trek realmente necesarias, con pruebas en NAP;
- producir/seleccionar mallas, NPC, texturas, UI y audio reales según prioridades;
- ejecutar Blender/Rob3D cuando corresponda sin destruir originales;
- importar y medir en UE5: escala, colisiones, materiales, LOD, streaming, FPS, VRAM y draw calls;
- validar recuperación/reproducción del asset y build ejecutable;
- resolver las puertas previas de F07/F08 que alimentan el vertical slice.

**Gobierno:** F02 sigue siendo la única fase principal `EN_CURSO`. Esta rama no cambia `ESTADO_GLOBAL.json`, no marca P01–P05 como cerrados y no declara completada la Fase 14.
