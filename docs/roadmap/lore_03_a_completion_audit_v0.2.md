# LORE-03 A — Auditoría final documental v0.2

**Fecha:** 2026-10-23 · **Base:** `main@867077e4` · **Rama/PR:** `lore/03-a-chronology-history` / #38.  
**Dictamen:** **NEEDS_REVIEW**, lista para revisión del autor tras GitHub Actions; **no** fusionada, **no** certificada escena por escena ni importada a runtime.

## Evidencia producida

- Decisión posterior de única época jugable TNG/DS9/Voyager registrada sin borrar tres perfiles históricos.
- Índice con **40 referencias por ID** de LORE-01 D **no duplicadas** y **21 fichas nuevas** para cubrir anclas 2364–2378, con referencias por `source_id` y fechas de año aproximado.
- Atlas continuo de **15 años** y antecedentes del siglo XXIII/primera mitad XXIV.
- **6 referencias oficiales adicionales** añadidas al registro central de fuentes, por tanto **507 fuentes** tras el cambio, sin convertir artículos en pantalla primaria.
- Apartado de versiones/errores de fecha, histórico personal e institucional, anacronismos, escenarios de corte D, riesgos al filtrar por era, futuro no garantizado.
- Validadores documentales y pruebas de mutación; regresiones LORE-01 D y LORE-02 E, y workflow exclusivo de LORE-03 A.

## Matriz de contraste de fuente y precisión

| Familia | Fuente documental | Precisión admitida | Límite |
|---|---|---|---|
| Borg/Wolf 359 | TNG *The Best of Both Worlds*, DS9 *Emissary*, StarTrek.com batallas | Año aproximado 2367; ofensiva 2366 LORE-01 D conservada y marcada como discrepancia | No generar dos invasiones por fechas editoriales |
| Política klingon | TNG *Redemption*, StarTrek.com *Inside the Nebula Class Starship* | 2368 aprox. | No asignar conducta a toda especie |
| Bajor/DS9 | DS9 *Emissary*, *The Siege*, *Duet*; TNG *Ensign Ro* | 2369/2370 aprox.; anterior ocupación por fases sin fecha inicial única | No inventar soberanía territorial ni conocimiento religioso unánime |
| Desaparición y retorno Voyager | VOY *Caretaker* / *Endgame*, StarTrek.com perfil Voyager | 2371 y 2378 aprox. | No activar final, viaje temporal ni portal Delta |
| Enterprise-D/E | StarTrek.com perfiles de D y Sector 001, film *First Contact* | D perdida ~2371; E confirmada ~2372/2373 | Sin despliegue en 2364, clase/instancia/3D separados |
| Guerra Dominio | DS9 *Call to Arms*, *What You Leave Behind* y StarTrek.com | 2373–2375 aprox. | Ya existen registros LORE-01 D; LORE-03 B estudia guerras, no esta A |
| Historia Delta | VOY *Scorpion*, *The Killing Game*, *Dragon's Teeth*, *Unimatrix Zero*, *Homestead* | Aproximación editorial anual sin días exactos | No implica acceso jugable al cuadrante ni conocimiento general |

## Hallazgos con resolución y reservas

1. **A-CANON-01 [reserva consciente]:** `borg_earth_offensive` LORE-01 D = 2366; Wolf 359 = 2367 aprox. Las fuentes alternan periodización; no corregir silenciosamente un LORE fusionado. Mantener cruce, investigar correspondencia de stardate si la futura importación necesita exactitud.
2. **A-CANON-02 [reserva]:** inicio de la ocupación Bajor expresado como ~2319 o ~2328 (presencia frente a anexión). Evitar falsa fecha única.
3. **A-DATA-03 [reserva]:** `dominion_cardassian_war_bajor` y `dominion_war_begins` pueden referirse a alcances superpuestos, no presumir dos guerras. LORE-03 B decide relaciones de conflictos.
4. **A-DATA-04 [reserva]:** fechas de registros heredados (`derna_hospital_dispute`, ofensiva Borg) requieren contraste al importar con granularidad superior al año, no bloquean la estructura cronológica.
5. **A-ERA-05 [deuda de integración]:** Academia, matriz de tecnología, catálogos y generadores aún reconocen Pike/Kirk como históricos; sus UI/selector deben respetar `playable: false` en etapa futura. **No se modifica runtime.**
6. **A-SHIP-06 [decisión autoral pendiente]:** Valhalla/Odyssey y fecha D sin resolver. Soberanía creativa del autor, no suposiciones.
7. **A-KNOW-07 [enlace a C]:** conocimiento no omnisciente, archivos reservados y memoria individuales quedan conceptuales; LORE-03 C redactará profundidad y casos, sin duplicarlos aquí.
8. **A-TEST-08:** corte D con año igual al del evento produce `UNRESOLVED_SAME_YEAR`, evitando inclusión forzosa; años claramente previos/futuros funcionan como ejemplos documentales, no código de bootstrap.

## Criterios de cierre de A y evidencia

| Condición | Evidencia | Estado |
|---|---|---|
| Corpus 2364–2378 y pasado histórico | Atlas completo 15 años + precedentes | Sí |
| Índices y fuentes sin duplicación | 40 IDs LORE-01 D por enlace + nuevas fichas distintas | Sí |
| Evidencia/precisión y dudas | Referencias oficiales/episodios, rangos aproximados, reservas expresas | Sí, con reservas no bloqueantes |
| Autoridad Core y no futuro obligado | Flags, contrato y pruebas de año D | Sí |
| Coherencia de naves | Matrix D/E/Voyager/Defiant/Odyssey/Valhalla | Sí, sin fechas inventadas |
| Validación documental | Validador + suite de mutaciones, workflow, regresiones | Pendiente de verificar último HEAD en Actions |
| Revisión y fusión humana | PR #38 | **NO**: no autorizado fusionar |

**Alcance del dictamen:** suficiencia editorial para LORE-03 A, con puntos de precisión rastreados para B–E y futura conversión a datos de juego. **No** se presenta como exhaustividad del canon Star Trek ni compatibilidad automática con CoreRPG/UE5.
