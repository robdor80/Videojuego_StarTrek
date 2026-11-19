# Seguimiento de subsanación de la auditoría Planificación 1 — R0–R7
**19-11-2026 · Registro de correcciones, NO planificación de una nueva fase**

**Auditoría de origen:** [AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md](../../auditorias/AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md), fusionada en PR #174. No se repite la auditoría. **El objetivo presente es detectar y reparar errores de gobierno/dirección/documentación y dejar el desarrollo futuro correctamente especificado**, no ejecutar la continuación de F06–F15 ni lanzar F08.

## 1. Cambios realizados y revisión GitHub

| Corte | Instrumento | Resultado verificable | ¿Cierra una fase de juego? |
|---|---|---|---|
| R0 | [PR #176](https://github.com/robdor80/Videojuego_StarTrek/pull/176) | Estado maestro, 16 fases/80 pasos, decisiones/PR reconciliadas, validador de gobierno evolutivo y 11 pruebas; CI del HEAD consultado 37/37 PASS | **NO** |
| R1 | [PR #177](https://github.com/robdor80/Videojuego_StarTrek/pull/177) | Informe documental de P05B: pruebas MSI originales, PR #89 fusionada, manifiesto y 14 aserciones del arranque de Unreal; 19/19 checks del HEAD consultado | **NO**. F05 EN_CURSO sin acta |
| R2 | [PR #179](https://github.com/robdor80/Videojuego_StarTrek/pull/179) | [Matriz real de Draft #91→#96→#97](fases/F06/R2_ESTADO_PR_F06_Y_GATE_PENDIENTE_2026-11-19.md), sin cambiar esas PR ni atribuir F06 a main | **NO** |
| R3/R4/R6 | PR #179 | [Puertas transversales y distribución de autoridad](R3_R4_R6_R7_FRONTERAS_Y_GATES_2026-11-19.md); corrección de README F07/F08 y objetivo F13/P2 | **NO** |
| R5 | PR #179 | [Matriz de identidad y migraciones](R5_IDENTIDAD_AUTORIDAD_Y_MIGRACIONES_2026-11-19.md); Enterprise-D Galaxy, protagonista fijo, emisor F11 como servicio | **NO** |
| R7 | PR #179 | Validador F15 para uso privado, canales locales, copia/restauración exigida, 38 escenarios y 20 tests previstos; desbloqueo de estado administrativo congelado | **NO** |

**Integración:** #176 y #177 son PR Draft sobre `main`; #179 es Draft apilada sobre la rama de #176. Hasta una fusión controlada, estos cambios no constituyen la fotografía de `main`. R1 no acepta por sí misma excepciones de motor ni firma F05. No fusionar PR de desarrollo (#91/#95/#96/#97/#110) por esta auditoría.

## 2. Semántica de estado para no crear falsos cierres

- **SUBSANADO EN PR:** se corrigió un error existente de documentación, gobierno o validador; requiere CI/revisión/merge para ser vigente en `main`.
- **DIRECCIÓN CORREGIDA:** las condiciones, fronteras y pruebas están especificadas, pero **falta implementar o certificar** la funcionalidad cuando se retome su fase.
- **PENDIENTE DE EVIDENCIA/DECISIÓN:** no hay autoridad para elevar estado (F05 acta, F06 manual PDF, escena MSI).
- **PENDIENTE DE DESARROLLO:** no es un fallo de esta reparación; corresponde a la conversación de Planificación 1 y no se activa aquí.

## 3. Los 20 hallazgos, sin ocultar los pendientes del producto

| Hallazgo | Resultado de corrección en esta auditoría | Qué permanece fuera del alcance de la reparación |
|---|---|---|
| P0-01 Validador congelado | **SUBSANADO EN R0:** invariantes, cierres fechados y pruebas negativas | Fusionar #176 tras revisión |
| P0-02 Ausencia E2E F08 | **DIRECCIÓN CORREGIDA:** puerta, observabilidad, SAVE/LOAD y pruebas negativas R3/R4 | Construir/ejecutar/aceptar F08 cuando toque |
| P0-03 Nave antigua | **SUBSANADO documental R0/R5:** Enterprise-D `Galaxy` y programa Valhalla separados | Migrar catálogos, saves y dotación tras diseño propio |
| P0-04 PR F06 fragmentadas | **DIRECCIÓN CORREGIDA R2:** bases/HEAD/CI y autoridad espacial | Integrar #91→#96→#97 y fuente real más adelante |
| P0-05 Emisor/carrera F11 | **DIRECCIÓN CORREGIDA R5:** F11 domina reglas, HOST transporta y autentica | Emisor de producto, vacantes y trayectoria completa |
| P1-06 F05 P05B sin acta | **PENDIENTE DE EVIDENCIA/DECISIÓN:** PR #177 deja la revisión y excepciones por escrito | Cotejar hashes accesibles, aceptar o bloquear aserciones UE, acta firmada |
| P1-07 F07 sin pruebas MSI | **DIRECCIÓN CORREGIDA R3:** #95 no UE5; asiento no aprobado; evidencias requeridas | Corregir asiento, importar escena y medir cuando toque |
| P1-08 Editor F10 legacy | **DIRECCIÓN CORREGIDA R5:** identidad fija versionada y test de migración | Adaptar realmente F10/HOST/S04 y partidas |
| P1-09 F13 sin universo runtime | **SUBSANADO documental R0/R6:** P2 B01–B10 referencia completa | Integrar scheduler/causalidad/LOD Core-HOST |
| P1-10 Distribución pública F15 | **SUBSANADO R7:** README, validador, fixture y pruebas solo privada local | Instalar/restaurar y aceptar build real después |
| P1-11 CI desigual | **SUBSANADO EN R0/R7:** nuevo gobierno y push `main` con filtros en F05/F06/F11 | CI necesita fusión; MSI pesado queda gate local/accionado |
| P1-12 Guardias/relaciones desconectadas | **DIRECCIÓN CORREGIDA R5/R6:** casos de persona, puesto, turno y estado únicos | Runtime coordinado F04/F11/F12 |
| P1-13 Falta contrato operación E2E | **SUBSANADO diseño R3/R4:** cadena y propietario por eslabón | Probar la cadena en runtime |
| P1-14 Rendimiento sin presupuesto | **DIRECCIÓN CORREGIDA R3/R7:** telemetría MSI exigible, sin inventar cifras | Capturas reales, umbrales aceptados |
| P2-15 Manual F06 sin revisión visual | **PENDIENTE DE EVIDENCIA:** procedimiento y gate delimitados R2 | Leer PDF íntegro y firmar conformidad visual cuando esté disponible |
| P2-16 Notas históricas contradictorias | **SUBSANADO en cabeceras R0 y correcciones R2/R3/R7**; actas históricas preservadas | Revisión de consumidores al aplicar futuras migraciones |
| P2-17 Fixture 2372 vs 2383 | **DIRECCIÓN CORREGIDA R5/R4:** dos escenarios diferenciados | Crear/ejecutar fixture campaña al desarrollar |
| P2-18 Autenticidad de saves F11 | **DIRECCIÓN CORREGIDA R5:** hash ≠ autenticidad; principal y recibos | Implementar/validar controles de producto |
| P2-19 Assets F14 | **DIRECCIÓN CORREGIDA R6:** READY/PLACEHOLDER/BLOCKED y campos requeridos | Inventariar/importar/verificar realmente assets |
| P2-20 Alcance infinito | **DIRECCIÓN CORREGIDA R6:** mínimo vs posterior vs experimental; dueño y motivo | Priorizar y aceptar cuando toque; no cambiar las 16 fases |

**Conclusión de remediación:** están preparadas las correcciones posibles sin ejecutar el videojuego ni tomar decisiones creativas nuevas. No llamar «corregido el juego» a una puerta de desarrollo especificada. El seguimiento no concede nuevas fases CERRADAS ni porcentajes de jugabilidad.

## 4. Propiedad y protección contra duplicación

- **CoreRPG:** WorldState, entidades, revisiones, reloj, eventos, guardado y consistencia.
- **Reglas F04/F05/F06/F10/F11/F13:** dominio Star Trek; no reproducirlas en HOST, LCARS o IA.
- **HOST:** sesión, principal, transporte seguro, integración institucional como servicio, IA central y proyección permitida. HOST nunca inventa autoridad.
- **UE5:** escena 3D, UI LCARS, animaciones, input y rendimiento.
- **Lore / decisiones:** identidad, cronología y decisiones creativas vigentes; no reinterpretar unilateralmente.
- **Planificación 2:** B01–B10 completados **solo en referencia**, sin simular el universo aquí.
- **Sistemas S01–S19:** catálogo de requisitos y contratos sin crear un motor paralelo.

## 5. Reglas de cierre de esta corrección (distintas del cierre del juego)

La auditoría de Planificación 1 se considerará **subsanada administrativamente** cuando se revisen e integren las PR de corrección, todas las CI relevantes estén en verde y los hallazgos estén clasificados con evidencia y dueños. Eso **NO** implica F05–F15 terminadas: F05 precisa su propia acta; F06/F07/F08/F10/F11/F13/F15 quedan en sus estados registrados hasta validaciones reales. Ninguna integración de producto queda autorizada por esta matriz.

**Queda deliberadamente fuera:** reabrir la auditoría independiente #174, repetir pruebas MSI sin fundamento, desarrollar nuevas fases, resolver defectos propios de proyectos HOST/Lore/P2, aprobar censo Enterprise-D, declarar jugabilidad por mockup, cambiar libremente el protagonista o preparar distribución a terceros.
