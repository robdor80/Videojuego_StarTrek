# Playable Eras — Decisión vigente

**Estado:** APROBADO · **Decisión autoral:** 2026-10-23 · **Proyecto:** Star Trek RPG.

> Este documento **sustituye** la elección histórica de tres épocas jugables descrita en su versión previa (2026-10-02) y en actas F01. No elimina la investigación, arte, canon ni perfiles de Pike y Kirk; cambia únicamente qué épocas pueden seleccionarse para una nueva campaña.

## Rectificación vigente — 2026-10-30 (DEC-0013–0016)

Queda **aprobado el año 2383 para el comienzo de la ruta de Academia**, con día/mes todavía pendientes y graduación aproximada 2387. **Odyssey está en servicio y es la punta de lanza de Flota al empezar** (GAME_ADDITION, no inferir Enterprise-F individual). **Valhalla empieza desarrollo/construcción en 2380 y su primera unidad tiene entrada objetivo 2387**, no 2383. **Flujo cuántico experimental** en Odyssey de pruebas, posible modernización posterior de Valhalla, nunca habilitación automática a todas las naves. [Acta general vigente](odyssey_valhalla_program_2383_2387_quantum_slipstream.md). Toda formulación inferior que deje sin fijar estos **años** es historia de diseño superada; **las fechas exactas** siguen abiertas y las consecuencias posteriores al inicio de partida no están predeterminadas.

## Addendum de diseño — academia y Valhalla (2026-10-23)

El autor propone **2383** como comienzo preferente de campaña (año aprobado por decisión posterior 2026-10-30), con **cuatro años de Academia** y graduación de alférez aproximada en **2387**. No se traslada el comienzo a 2384. El programa de clase Valhalla surge tras *Némesis* de 2379, con fabricación prevista desde 2380 y **entrada en servicio objetivo en 2383** (propuesta histórica sustituida por objetivo **2387** el 2026-10-30), para que el jugador pueda ser destinado a ella al graduarse; no es una fecha histórica de pantalla. Esto **extiende la investigación documental hasta 2383** y no crea época jugable adicional. Ver [addendum Valhalla/Academia](lore03a_valhalla_2383_academy.md).

## Única época jugable

**`tng_ds9_voyager`** — segunda mitad del siglo XXIV, núcleo **2364–2378**, extendido documentalmente hasta **2383**, como **ventana histórica de referencia**, no como año fijo de comienzo, límite forzoso del tiempo simulado ni guion de series.

Se estudian como un mismo universo histórico:
- *Star Trek: The Next Generation*
- *Star Trek: Deep Space Nine*
- *Star Trek: Voyager*

La selección de campaña puede especificar un año/fecha dentro de la ventana cuando lo decida el autor; **el año inicial de Academia está aprobado como 2383**; permanecen pendientes día/mes y otras modalidades de inicio. Un hecho, nave, personaje, tecnología o institución requiere validez **en la fecha elegida**, no basta con pertenecer a esta época.

## Perfiles preservados pero NO jugables

- `pike` — *Strange New Worlds*: antecedentes históricos, patrimonio documental/arte y posibles referencias culturales.
- `kirk` — *The Original Series* y películas asociadas: antecedentes, biografías, naves veteranas, tratados y legado.

Se preservan identificadores y documentación para que las referencias ya existentes no se rompan. Su existencia **no** habilita menús, academias ni campañas en esos periodos. El dato `playable: false` de los perfiles es la señal de selección; **no** debe interpretarse como prohibición de consultar pasado o utilizar naves antiguas todavía operativas en 2364–2378.

## Política histórica y continuidad

1. El canon anterior al inicio de la campaña aporta el estado inicial, con fuentes y precisión temporal; no impone un destino futuro.
2. Desde el comienzo, la continuidad **real del guardado** es autoridad exclusiva de CoreRPG sobre el estado de mundo; IA y Host no pueden decretar hechos.
3. Los episodios, campañas militares, encuentros, regresos o fallecimientos televisivos posteriores al inicio **no se disparan automáticamente**.
4. Se permite continuidad creativa propia, incluido un cambio excepcional del pasado, **solo por aprobación y registro expreso como GAME_ADDITION**, con impactos/fecha analizados. No se reescribe `SCREEN_CANON`.
5. No habrá **viajes temporales jugables**. La documentación de hechos históricos de pantalla que contengan viajes en el tiempo no es una autorización de mecánicas jugables.
6. Las clases Miranda, Intrepid, Sovereign, Odyssey y Valhalla y los ejemplares Enterprise-D/E/F requieren auditoría y disponibilidad temporal individual. La existencia de modelos 3D no implica alta de nave en la historia.
7. Valhalla es clase propia, con **objetivo de primera entrada 2387 aprobado**; Odyssey está **en servicio en 2383** por GAME_ADDITION aprobada. No se presupone Odyssey disponible en 2364–2378 ni se atribuyen automáticamente matrículas o equipamientos a cascos concretos.
8. El jugador puede saltar Academia conforme a las decisiones de carrera ya aprobadas; eso no cambia el filtro de época.
9. No se crean universos independientes por serie ni se exige proximidad espacial entre personajes que coinciden en el tiempo.

## Trazabilidad

- Decisión anterior: tres perfiles jugables; preservada en el historial Git y actas históricas F01.
- Decisión posterior prevalente: **2026-10-23, único perfil jugable TNG/DS9/Voyager**.
- Contratos relacionados: `proyecto/docs/decisions/campaign_continuity.md`, `mundo/sources/canon_policy.md`, `sistemas/universe/chronology/era_profiles/` y `proyecto/docs/roadmap/lore_03_master_plan_v0.1.md`.
- Cambio de alcance **documental**: no declara filtros ejecutables en UE5 ni CoreRPG ni elimina assets.

## Control de cambios

Nuevas épocas jugables y cambios de fecha inicial necesitan decisión expresa del autor y PR propia/revisable.
