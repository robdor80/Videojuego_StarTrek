# DEC-0013–0016 — Programa Odyssey → Valhalla y flujo cuántico

**Aprobación expresa del autor:** 30 de octubre de 2026. **Estado:** APROBADO EN DISEÑO / GAME_ADDITION; aún no implantado en CoreRPG ni UE5. **Ámbito transversal:** LORE-03 (historia), F01 (visión), F04 (naves y tripulaciones), sistemas de tecnología, F11 (carrera) y futuros arcos de misiones. Este documento **prevalece en cronología y flujo cuántico** sobre las propuestas de 21 y 23 de octubre que no fijaban año o proponían Valhalla en 2383. No revoca otras decisiones técnicas o artísticas de Valhalla.

## 1. Calendario autoral vigente

| Año | Decisión |
|---|---|
| **2379** | Tras *Star Trek: Nemesis* y las crisis Borg, Dominio y Shinzon, se impulsa el **programa de desarrollo Valhalla** (origen narrativo; GAME_ADDITION). |
| **2380** | Comienza la fase de **construcción/desarrollo de Valhalla**. |
| **2380–2386** | Desarrollo, construcción, integración, ensayos y corrección de fallos; las pruebas pueden continuar hasta su entrada en servicio. |
| **2383** | El jugador **ingresa en la Academia** (día/mes todavía sin fijar); la **clase Odyssey ya está en servicio y es la punta de lanza tecnológica de la Flota**. Su introducción en 2383 es una **divergencia aprobada del videojuego**, no fecha canonizada de pantalla. |
| **2383–2387** | Cuatro cursos de Academia, salvo que la ruta elegida permita omitirla conforme a las reglas preexistentes. |
| **2387** | **Objetivo de entrada en servicio de la primera unidad de clase Valhalla**, nueva punta de lanza de la Flota: **siete años transcurridos desde el inicio de construcción en 2380**. El año queda aprobado, pero día/mes y orden exacto con la graduación están pendientes. |
| **2387 aprox.** | Graduación del cadete como alférez. Puede aspirar a plaza real en una Valhalla cuando esa nave entre efectivamente en servicio y exista una vacante compatible: **no hay destino automático ni capitanía al graduarse**. |

**Distinciones obligatorias:** desarrollo de una clase ≠ entrada en servicio ≠ construcción y disponibilidad de cada casco ≠ identidad de una Enterprise concreta. «Punta de lanza» describe liderazgo tecnológico/institucional, no que toda nave Odyssey o Valhalla tenga cada equipamiento experimental. La USS Enterprise-F de pantalla no se adelanta automáticamente a 2383 por esta decisión, ni la etiqueta de clase asigna matrícula a una nave.

## 2. Flujo cuántico como programa tecnológico y argumento de misiones

1. En **2383**, el **motor de flujo cuántico (quantum slipstream)** existe en la línea de investigación de Flota y comienza una fase **experimental muy restringida sobre una o varias Odyssey de pruebas designadas expresamente**. **NO es equipamiento estándar de toda la clase Odyssey**. Se deben verificar disponibilidad, autorización, instalación, recursos y estado de cada casco.
2. Entre **2383 y 2387**, los ensayos aportan datos, incidentes, avances, modificaciones y consecuencias persistentes; no hay éxito garantizado ni una mejora automática por transcurso del calendario.
3. Para **Valhalla**, el flujo cuántico es una **capacidad prevista en el programa de investigación y una posible modernización posterior**. La entrada en servicio de la primera Valhalla en 2387 **no obliga** a que lleve un motor de flujo cuántico certificado. Su instalación puede requerir pruebas adicionales después de 2387.
4. Puede convertirse en **arco de misiones**: investigación de estabilidad del corredor, planificación de navegación, recursos críticos, pruebas limitadas, incidentes, rescates, autorizaciones de Flota, evaluación de riesgos y decisión de despliegue. Los resultados se decidirán por causas, acciones y estado de mundo, no por una escena obligatoria centrada en el jugador.
5. Conservar **warp convencional** como propulsión operativa mientras el sistema experimental no sea autorizado y validado. No fijar velocidades, consumo, porcentajes de éxito, cantidades de cristales ni compatibilidad energética sin investigación y decisiones posteriores.
6. No confundir **propulsión de flujo cuántico** con **torpedos cuánticos**. Son tecnologías diferentes.
7. La autoridad de estado, progreso, averías, misiones y cronología corresponde exclusivamente a **CoreRPG**; los contratos de Star Trek interpretan sus datos y Unreal/IA no pueden conceder sistemas a voluntad.

## 3. Continuidad y límites

- Esta cronología está marcada **GAME_ADDITION / AUTHOR_DECISION**: no reescribir como `SCREEN_CANON` la historia de televisión.
- La historia anterior al comienzo de campaña se prepara hasta la fecha efectiva `D`; a partir de `D`, el universo persiste y diverge, sin acontecimientos futuros obligatorios. No se debe forzar que la Valhalla esté lista en 2387 si una campaña causa legítimamente retrasos o altera el programa.
- **2383** es el año inicial aprobado de la ruta Academia de referencia; **el día y mes siguen abiertos**. La clase Odyssey debe estar operativa en el estado inicial de esa ruta, sin inventar el día exacto de su primera botadura.
- **2387** es año objetivo de entrada de Valhalla. **Sin fecha exacta ni garantía de disponibilidad antes de la graduación**.
- Se mantiene el diseño Valhalla aprobado: clase propia inspirada en Galaxy, separación funcional, blindaje ablativo, armamento especial, tres hangares, nave auxiliar Defiant con sus condiciones, dotación nominal de 1.800 Flota + 400 civiles. No se atribuye automáticamente una matrícula, tripulación, capitán, montaje de motor o tecnología experimental a todos los cascos.
- El nombre y la matrícula `USS Enterprise / NCC-1701-G` siguen siendo identidad creativa/de trabajo sujeta a los acuerdos previos; **la clase Valhalla no equivale por sí sola a la Enterprise-G**.
- Se preserva el acceso de carrera temprano a Valhalla como alférez o teniente si existe plaza legítima, sin ascensos forzados.

## 4. Alcance técnico y pendientes

Esta acta registra **decisiones de diseño**, no hace aparecer naves ni propulsores en una partida existente. La implementación de filtros temporales, estados experimentales, agendas de investigación, resultados de prueba, seguridad y posibles misiones pertenece a sus respectivas fases y **requiere revisión antes de fusionarse al runtime**.

**Pendientes:** día/mes de ingreso 2383; fecha exacta de comisión de Odyssey y Valhalla; qué cascos Odyssey serán bancos de pruebas; ingeniería de flujo cuántico, requisitos y fallos; punto de instalación/validación en Valhalla; nombre de misiones, consecuencias y posibles cambios de campaña.

**Fuentes de proyecto relacionadas:** `proyecto/docs/decisions/lore03a_valhalla_2383_academy.md` (antecedente superado respecto a 2383 Valhalla); `proyecto/docs/decisions/playable_eras.md`; `mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json`; `mundo/lore/starships/classes/core_starship_classes.json`; `mundo/lore/technology/valhalla_tech_decisions_v0.1.json`; `sistemas/gameplay/technology/technology_capability_contract.json`; `proyecto/ideas/IDEA-0007_carrera_temporadas_llegada_y_mando_valhalla.md`.

**Registro de cambios:** 2026-10-30, sustitución explícita del objetivo «Valhalla 2383» por «Odyssey operativa en 2383 → Valhalla objetivo 2387», con siete años de construcción y programa experimental de flujo cuántico como eje narrativo.
