# F11-P05-A02-01 — Encargo preparado para Codex (NO ejecutado)

**Estado:** BORRADOR TÉCNICO PREPARADO. Solo usar tras autorización expresa para iniciar A02-01.  
**Modelo recomendado:** **GPT-6**.  
**Nivel de pensamiento:** **Alto**.  
**Repositorios:** `robdor80/Videojuego_StarTrek`; CoreRPG `robdor80/CoreRPG` solo como dependencia fijada.  
**Contrato rector (obligatorio):** `sistemas/gameplay/careers/promotions/f11_p05_a02_00_personnel_contract_v0.1.json`.  
**Explicación y puerta de cierre:** `F11-P05-A02-00_CONTRATO_IDENTIDAD_RANGOS_AUTORIDAD_2026-11-11.md`.

## Prompt preparado

Actúa como ingeniero C++ responsable de implementar el **primer ascenso verdaderamente autoritativo** de F11-P05, respetando los módulos CoreRPG, F04 y F05 y **sin construir un segundo estado de campaña**. Trabaja únicamente en una rama `codex/f11-p05-a02-01-first-promotion-<fecha>` de `robdor80/Videojuego_StarTrek`. Crea PR **draft** para revisión; **no fusiones**.

### A. Primera acción: investigar la compatibilidad y escribir microplan

- Examina `AGENTS.md`, `desarrollo/integration/f04/README.md`, `desarrollo/integration/f05/README.md`, las interfaces C `f04_bridge.h`, `f05_orders.h`, `f04_bridge.cpp`, `f05_orders.inc`, la validación `schema()`, `F04Session`, historial segmentado y persistencia Core.
- Respeta el pin exacto de F05: **`76a7b7b485616d8c4994f384a90f123bf333591d`**. F04 sin historia conserva el pin propio **`c147d81ed069da2e09149613ab02cbc3ebe95a4a`**; no migrar pines ni tocar ramas de Core por conveniencia.
- No inventes una API de CoreRPG si sus entidades/relaciones/ActionEngine bastan. No añadas SQLite/JSON lateral como nueva autoridad.
- Documenta en el PR qué extensión **aditiva y opt-in** del esquema Trek permite crear identidad, comisión, concesión institucional, orden de personal y evento de promoción. Recuerda que el validador F04 rechaza campos de persona desconocidos.
- Antes de codificar, aclara cómo se emite de manera **confiable** el primer `commission_event_id` de un oficial de ensayo en Core sin convertir todos los `RANK=0` de la plantilla en alféreces. La raíz de Personal de Flota debe provenir de bootstrap/Host privado, **no** de bool en JSON o argumentos de un usuario. Si no es posible autenticarla de manera real en la arquitectura actual, informa de la limitación y prepara un diseño seguro en vez de introducir un atajo.

### B. Implementación limitada

**Único efecto profesional autorizado:** `ensign` (`RANK=1101`) → `lieutenant_junior_grade` (`RANK=1102`).

- Mantén el resto de la escala `1101–1106` como contrato; **no** implementes todavía las otras cuatro promociones ni las capitanías o sucesiones.
- Crear/ligar `character_id` de 128 bits (tres campos de 48+48+32), sin reusar `F04Ref` como identidad global.
- El jugador de prueba debe tener comisión, identidad y evento inicial de rango verificables **dentro del mismo Core WorldState**. Prohibido tratar `RANK=0` como alférez, o interpretar el `RANK=8` histórico del capitán de ejemplo como orden del lore.
- Implementar control de `fleet_personnel_promotions` por autoridad institucional emitida por Host confiable con concesión, ámbito, revocación, tiempo y prueba de la orden. Un capitán sin concesión no puede autoascender a su tripulación. IA y Blueprint no conceden permisos.
- Utilizar **una sola** instancia `F04Session` y staging validado del mundo, con escritura atómica de nuevo rango más **evento de expediente `promotion`**. El evento se vincula a comisión, evaluación, orden y procedencia, sin alterar puesto, unidad, departamento, cualificaciones ni turnos.
- No camuflar el ascenso como `F04_APPOINT`, `F04_CREDENTIAL`, `F04_SCAN`, ni llamarlo mediante `F04_ASSIGN` que puede sustituir un titular. La autoridad de F05 permanece operativa para tareas que ya soporta.
- La API C propuesta `f11_commit_promotion` puede ajustar detalles ABI a la forma real del puente, **sin alterar estructuras ni enumeradores existentes**. Documentar la firma efectiva y el contrato de errores; utilizar valores F04 de 48 bits cuando corresponda.
- Idempotencia profesional: misma clave y contenido **recupera el evento persistido**; clave igual con datos distintos **conflicto**; clave nueva tras ascenso **denegación**; reintento después de carga nunca duplica. La búsqueda de idempotencia debe anteceder a rechazar una revisión del mundo obsoleta si se trata de la misma petición **ya confirmada**.
- Confirmación efectiva **solo en el instante actual de la campaña**. No programar ascensos futuros todavía.
- No editar ni borrar modelos 3D, configuraciones Unreal, librerías PBR ni documentos originales. No alterar permisos del PADD.

### B.1. Requisito transversal aprobado para la presentación futura del ascenso

La decisión autoral [ascensos diegéticos F11-P05](../../../../decisions/f11_p05_ascensos_diegeticos_presentacion_narrativa_2026-11-11.md) y la [issue #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104) son **obligatorias**. En este corte A02-01 **NO** implementar ni dibujar ventanas/menús de «subida de nivel», escenas 3D, PADD ni colas visuales. Sí asegurar que el evento autoritativo `promotion` que ya exige este encargo posea de forma persistente:

- **`promotion_event_id` estable y único** apto para deduplicar futuras comunicaciones.
- **`subject_character_id`**, rango anterior/nuevo, referencia a orden/autoridad y **`effective_at`** (instante de campaña cuando el ascenso es legalmente válido).
- Referencia de identidad/destino/presentación suficiente para que un futuro director consulte Core con permisos sin inventarse superior, nave o contexto. **No almacenar un diálogo fijo como verdad autoritativa.**
- Prueba tras guardar/cargar de que el evento mantiene la misma identidad y momento efectivo.

La distinción `effective_at` vs. `presented_at` es **innegociable**: que el personaje esté en combate o no se haya construido el despacho no puede retrasar el efecto legal del ascenso. La **cola/acuse persistente** se desarrolla en **F11-P05-C**, y la comunicación personal, encuentro con superior, insignias y ceremonia jugable se desarrollan en **F11-P05-D**. Las pruebas de presentación E2E son **F11-P05-E**. Este bloque es una obligación de compatibilidad futura, **sin ampliar el alcance nativo A02-01 a UI/UE5**.

### C. Pruebas nativas obligatorias

1. **Positiva:** alta confiable y comisión previa de alférez, promoción autorizada; `f04_person` informa `1102` y permanecen misma identidad, nave, plaza, departamento, cualificaciones, destino y origen de mando.
2. **Negativas:** persona no comisionada, `RANK=0` legado, `RANK=1/8/10` sintético sin migración, evaluación de otro personaje/otro evento de rango, orden no emitida o revocada, capitán sin concesión de Flota, clave en conflicto, petición caducada, revisión obsoleta, salto hasta capitán, segundo ascenso.
3. **Atomicidad:** fallos inyectados en preparación/publicación nunca dejan rango sin evento o evento sin rango, sin RNG extra ni registros huérfanos. La denegación no altera el mundo.
4. **Idempotencia:** misma clave reintentada, revision antigua después de primer commit, cambios de orden, nueva clave conflictiva, reintento tras guardar/cargar en **otro proceso**.
5. **Persistencia:** guardados con el contrato F11, guardados antiguos íntegros, historial segmentado y consolidación sin perder identidad/último rango/idempotency tombstone.
6. **Regresiones completas:** F04/F05 actuales con sus revisiones de Core fijadas, 340 tests offline de F11, gobernanza del roadmap; **NO** declarar tests Unreal si no se han ejecutado. Si la revisión nativa no puede ejecutarse en entorno disponible, indicarlo sin etiquetar Core como integrado.
7. En la prueba de salida, el oficial sigue sin autoridad de mando de nave por el mero hecho de tener grado 1102.

### D. Localización obligatoria de artefactos

- Todo build, caché, compilación, resultado temporal y log se guarda en **`laboratorios/f11/p05-a02-01/`** dentro del repositorio Trek, ignorado por Git y eliminable, de acuerdo con `AGENTS.md`. Nunca fuera del repo ni se sube `laboratorios/` a GitHub.
- Los archivos definitivos de código, tests, políticas y documentación residen en las rutas ya establecidas de `desarrollo/integration/`, `sistemas/` y `proyecto/docs/`. Nada definitivo dependerá de `laboratorios/`.
- Si es estrictamente necesaria una función genérica de CoreRPG, proponla en PR separada con justificación, impacto en pin y regresión; **no cambies el pin silenciosamente**.

### E. Forma de entrega

- PR **draft**, commits identificables, resumen de cada fichero tocado, sin fusión automática.
- Tabla `PASS/FAIL/SKIP` de pruebas ejecutadas de verdad, SHA de Core usado, log relevante y reproducibilidad.
- Demostración de `ensign 1101 → lieutenant_junior_grade 1102` sobre **CoreRPG real**, guardado y cargado; no confundir Python/contract checks con prueba nativa.
- Lista de cualquier limitación pendiente, especialmente identidad inter-naves (P05-B3) e interacción con Unreal (P05-D).
- No modificar `ESTADO_GLOBAL.json` ni marcar F11 como jugable.

### F. Criterio de aborto seguro

Si se identifica que para emitir una autorización legítima de Flota o registrar el nuevo esquema sin romper la compatibilidad es imprescindible modificar el motor genérico CoreRPG, **no introduzcas un bypass**. Prepara un diagnóstico, pruebas que demuestren la brecha y una propuesta de PR separada. Mantén la rama y la campaña intactas.

## Observación para ChatGPT antes de enviar a Codex

Este prompt **no debe ejecutarse** hasta que el usuario autorice A02-01. Al arrancar esa subfase, comprobar de nuevo los SHA de `main`, el Core pin y la cuota disponible, y ajustar las rutas solo si el código real ha cambiado.

No se ha gastado cuota de Codex en A02-00.
