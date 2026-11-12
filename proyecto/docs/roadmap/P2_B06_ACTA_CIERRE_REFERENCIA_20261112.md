# P2-B06 — Acta de cierre de referencia (12/11/2026)

**Bloque:** 6 de 10, Ciencia, tecnología y descubrimientos.
**Nivel técnico:** `COMPLETE_REFERENCE` sobre contrato, simulador y tests; **NO** runtime, ciencia jugable ni integración CoreRPG/HOST/UE5.
**Base:** Bloques 1–3, P2-B04 PR #113 y P2-B05 PR #114 ya fusionadas. Rama `design/p2-b06-science-discovery-20261112`, PR #115.

## Qué se ha cerrado

1. Auditoría de LORE-02 D, catálogo científico y legado, decisiones vinculantes y frontera de CoreRPG.
2. Dieciocho paquetes ST001–ST018: sujetos preexistentes, actores/instalaciones, asignaciones finitas, observaciones y evidencias, investigación independiente y contradicción; evaluación institucional; diseño de ingeniería aprobado para era/clase; orden de trabajo, tiempo de astillero, instalación, ensayos, activación por **nave individual**; nombramiento honorífico formal; conocimiento comunicado por permisos.
3. IDs estables por campaña, reloj monótono, prefijo canónico sellado, registros con hash, reproducción determinista, idempotencia y rechazo atómico.
4. Prohibiciones probadas: no ciencias con presencia del jugador, no tecnología de viaje temporal, no Omega como circuito ordinario, no creación de agujeros de gusano, anomalías, crisis, guerras, misiones ni despliegue automático de toda la Flota.
5. Carrera científica y trabajo de NPC igualmente elegibles; crédito de todos los contribuyentes sin usurpación. Para el jugador capitán, decisiones de prioridad, autorización y riesgo sin conocimiento de física real obligatorio.
6. Adaptador de referencia que acepta hechos **externos ya declarados**, no crea la verdad física. No se altera ningún archivo de CoreRPG ni código UE5 o HOST.

## Pruebas reales

En el commit [`68718aabb3119ec0a5b3fdb23089d1eafcf8e492`](https://github.com/robdor80/Videojuego_StarTrek/commit/68718aabb3119ec0a5b3fdb23089d1eafcf8e492), workflow [P2-B06 #43198790144](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43198790144) = **SUCCESS**:

- **54/54** pruebas propias de B06 (incluidas negativas contra ensayos suplantados/reutilizados, cronología y homónimos honoríficos).
- **152/152** pruebas conjuntas de referencia B1–B6 (incluidas las 54 anteriores).
- **28/28** F13 y frontera secuencial.
- JSON de contrato y fixture válido; CLI de referencia con 11 eventos, un proyecto y una instalación activada sólo tras ensayo. Hash `ebb3d47e521bf93b7017c1c635c9a4d1ac645178496fabe5c70ebb4da8c1a249`.

El workflow también debe pasar sobre el **último commit documental** de la rama antes del merge. Las pruebas sobre el commit de código no certifican por sí solas un commit documental posterior.

## Límites y obligaciones para el runtime

`accepted` para hechos de sensor, ensayos y asignaciones es una **declaración de fixture**; un adaptador real deberá demostrar su origen contra la verdad firmada/autorizada por CoreRPG y las órdenes de HOST. Tampoco se ha probado presupuesto real B04, inventario real, instalaciones 3D, presencia de instrumentación, comunicaciones entre naves, persistencia tras reiniciar CoreRPG, investigadores verdaderamente autónomos ni simulación offscreen B10. El simulador Python **no debe importarse como segundo motor de estado**.

LORE-02 D mantiene la excepción narrativa Omega con **mínimo una misión especial de autor pendiente de escritura**. B06 no la implementa. «Sensores Rise» sigue siendo un ejemplo, no componente instalado por defecto. No se debe cambiar ninguna clase/rango/nave por el mero hecho de completar este bloque.

## Frontera secuencial

Aprobado documentalmente el Bloque 6, **el siguiente elegible es el Bloque 7 — Fenómenos, anomalías y arqueología procedural**, sólo tras verificarse PR #115 fusionada y CI final. F13 principal sigue `PLANIFICADA`; ninguna condición de cierre general de F13 ha sido satisfecha por B06.
