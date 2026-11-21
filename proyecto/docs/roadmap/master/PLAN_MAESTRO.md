# PLAN MAESTRO — Star Trek Legends · Planificación 1 (F00–F15)

**Fotografía de gobierno R0: 19-11-2026.** Fuente estructurada: [ESTADO_GLOBAL.json](ESTADO_GLOBAL.json). Diagnóstico: [auditoría independiente F00–F15](../../auditorias/AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md), PR #174 fusionada. Esta versión sustituye las frases administrativas del 03-11, **no** sus actas, pruebas ni contratos históricos, que siguen accesibles en el historial Git.

**Dictamen:** Planificación 1 **NO está terminada**. Conserva **16 fases y 80 pasos**. F00–F04 están cerradas solo en sus **alcances originales diferentes**; F05 tiene pruebas técnicas MSI pero falta acta; F06 y F07 necesitan integrar borradores y UE5; F11 tiene un primer ascenso real; F13/P2 está terminada solo como **referencia**. No existe una guardia F08 E2E aceptada en Unreal. PR fusionada ≠ fase cerrada; PR Draft ≠ main; simulador ≠ juego.

## Decisiones vigentes (precedencia sobre documentos antiguos)

- **DEC-0020:** nave de destino = **USS Enterprise NCC-1701-D**, **clase Galaxy**, modernizada. **Proyecto Valhalla** es el programa de reconstrucción, **no una nueva clase de nave**. La antigua «Clase Valhalla» es referencia histórica; no migrar identificadores/guardados ni atribuirle una dotación heredada de 1.800+400 sin autorización y pruebas.
- Academia comienza en **2383**, cuatro años de formación y graduación objetivo hacia **2387**. El estado real de la Enterprise-D y la fecha de entrega requieren coherencia con Lore; no implican capitanía automática ni equipamiento no validado. **USS Sutherland** sigue siendo piloto técnico F07/F08, no se sustituye por la Enterprise-D sin decisión del autor.
- **DEC-0021:** Sensores deben exponer observaciones y conocimientos autorizados, nunca omnisciencia. **DEC-0022:** protagonista único aprobado, varón híbrido humano-vulcano de 45 años al iniciar la Academia; nombre y pequeños aspectos editables. La migración del editor productivo F10/HOST sigue pendiente.
- **Uso exclusivamente privado:** F15 no requiere lanzamiento público ni distribución. Exige build local en MSI, instalación, actualizaciones, copias, rollback y recuperación probados.
- **Fuentes de verdad:** CoreRPG = WorldState/tiempo/persistencia; fases Star Trek = reglas de dominio; HOST = sesión/autenticidad/emisor de servicios/enrutamiento IA; Unreal = interacción, visualización, escenas y rendimiento. Ni IA, LCARS, HTML ni voz pueden aplicar mutaciones por sí solas.

## Fases y metas — estado de gestión ≠ madurez demostrada

| Fase | Tema | Estado global | Entrega objetivo |
|---|---|---|---|
| [F00](fases/F00/README.md) | Auditoría, inventario y gobierno | **CERRADA** | DOCUMENTACION_AUDITADA |
| [F01](fases/F01/README.md) | Visión y canon del producto | **CERRADA** | DISENO_VALIDADO |
| [F02](fases/F02/README.md) | Arquitectura e integración | **CERRADA** | CONTRATO_VALIDADO |
| [F03](fases/F03/README.md) | Mundo autoritativo y persistencia | **CERRADA** | CORE_INTEGRADO |
| [F04](fases/F04/README.md) | Naves, dotación y autoridad | **CERRADA** | REFERENCIA_PROBADA |
| [F05](fases/F05/README.md) | Órdenes, delegación e iniciativa NPC | **EN_CURSO** | CORE_INTEGRADO |
| [F06](fases/F06/README.md) | Sensores funcionales | **EN_REVISION** | REFERENCIA_PROBADA |
| [F07](fases/F07/README.md) | Pipeline 3D y puente piloto | **EN_REVISION** | UE5_JUGABLE |
| [F08](fases/F08/README.md) | Primera guardia jugable v0.0.1 | **PLANIFICADA** | ACEPTACION_SUPERADA |
| [F09](fases/F09/README.md) | Resto de consolas | **PLANIFICADA** | UE5_JUGABLE |
| [F10](fases/F10/README.md) | Academia jugable | **PLANIFICADA** | UE5_JUGABLE |
| [F11](fases/F11/README.md) | Carrera y flota jugable | **EN_REVISION** | UE5_JUGABLE |
| [F12](fases/F12/README.md) | Vida a bordo y relaciones | **PLANIFICADA** | CORE_INTEGRADO |
| [F13](fases/F13/README.md) | Universo dinámico | **PLANIFICADA** | CORE_INTEGRADO |
| [F14](fases/F14/README.md) | Recursos audiovisuales y NAP | **PLANIFICADA** | UE5_JUGABLE |
| [F15](fases/F15/README.md) | QA, beta privada y mantenimiento local | **PLANIFICADA** | ACEPTACION_SUPERADA |

**Interpretación:** F00 (documentación), F01 (diseño), F02 (contrato de laboratorio), F03 (corte Core) y F04 (referencia operativa) no tienen idéntico significado de CERRADA. Los 29 pasos marcados CERRADA en la fotografía anterior no eran 29 experiencias jugables; los 51 restantes contienen trabajo real todavía no actualizado por aceptación. Los 80 pasos permanecen en el JSON y sus estados no se traducen a un porcentaje de finalización de juego. No se conoce un número de horas o semanas restante fiable.

## Progreso y puertas no resueltas

**F00–F04.** F02 #60 prueba Core↔UE solo de laboratorio; F03 #62/Core #12 certifica persistencia de un corte sintético; F04 #76/Core #13 conserva cinco perfiles/guardias/campañas de referencia. **No rehacer** esas bases. F04-INTEGRACION-04, independencia de secciones y plantilla autoral de Enterprise-D siguen fuera del corte cerrado.

**F05.** #81/#82/#84/#85 y **#89 están fusionadas**. La certificación #89 registra dos repeticiones oficiales en MSI, por repetición Core 482 PASS y 1 SKIP POSIX, symlink 3/3, F04/F05 395/395, UE5 12/12 NullRHI y 12/12 D3D12 sobre RTX 4070 Laptop. Se trata de **automatizaciones de laboratorio**, no de pantalla de juego. Se observaron **14 errores globales de arranque Unreal** reproducidos en controles sin módulos Star Trek, sin aserción concreta identificada. El archivo acceptance.json mantiene FINAL=PENDIENTE_ACTA y revisión RHI en espera. **R1 debe auditar logs y aprobar o rechazar la excepción explícitamente antes del cierre F05.**

**F06.** #92/#93/#94 aportan ensayos en main. **#91 → #96 → #97** siguen **Draft**, encadenadas; pruebas Tk de Aster no son consola UE5 y el puerto espacial de #91 no dispone de generador runtime universal. Quedan manual visual P01, observación espacial autoritativa, permisos, transferencia a Ciencia, save/load y rendimiento.

**F07.** Sutherland y pipeline GLB/PBR tienen ensayos reportados pero faltan evidencias primarias, prueba de sentado correcta (F07-SEAT-01 NO aprobada), materiales, colisiones y perfil MSI. **#95 sigue Draft**: LCARS HTML/JS aislado; no es interfaz UE5 conectada a Core.

**F08.** **PRIMER GATE JUGABLE PRIORITARIO:** orden legítima de capitán NPC → contacto observado → barrido y análisis → parte científico → consecuencia Core confirmada → SAVE/LOAD en otro proceso → interacción y aceptación reales en UE5 MSI. Incluir rechazos, filtrado de conocimiento y fallback sin IA. Conservar el fixture técnico 2372/Sutherland separado de la historia de Academia 2383–2387. F08-P01…P05 aún no ejecutados E2E.

**F09.** Dieciséis familias de consolas y contratos offline, pero sin estaciones funcionales en juego. Priorizar solo las necesarias para la guardia antes de ampliar catálogo.

**F10–F11.** F10 contiene currículo de cuatro años y ensayos de referencia, admisión parcial y HOST diagnóstico; pendiente migración DEC-0022 y continuidad jugable. F11 tiene **primer ascenso Core 1101→1102** con expediente y persistencia (#106/#107) y lector HOST de solo lectura (#109), todo ello fusionado. **#110 es Draft de documentación con 33 casos NOT_RUN, no un emisor institucional funcional.** Faltan emisión productiva, rangos restantes, ofertas/plazas, sucesiones, ceremonias, rechazo, guardado y campaña UE5.

**F12–F14.** F12 (vida social) sigue siendo referencia. **Planificación 2 B01–B10 está REFERENCE_COMPLETE**, pero **F13 no simula el universo galáctico** en Core/HOST/Unreal; reutilizar sus contratos sin duplicar P2. F14 dispone de recursos/biblias pero necesita manifest de assets realmente importables, colisiones, LOD, animación y huella de VRAM de la ruta F08.

**F15.** Gate documental fail-closed con plantilla NO_EJECUTADO es correcto. La aceptación final exige pruebas E2E, negativas, persistencia, recuperación, rendimiento y **build privada instalable, actualizable y reparable**. No habilitar distribución a terceros.

## Cortes R0–R7

| Corte | Trabajo concreto | Responsable | Estado |
|---|---|---|---|
| R0 | Gobierno: JSON + plan + CI/validador + seguimiento veraz | ChatGPT, pruebas automatizadas | PR revisable |
| R1 | Cierre F05: contraste #89, MSI, excepciones y acta | ChatGPT + aceptación del propietario; Codex si hay defectos | Pendiente de acta |
| R2 | #91→#96→#97, universo espacial y conocimiento F06 | Codex C++/HOST; ChatGPT revisión | Pendiente |
| R3 | #95 LCARS, puente Sutherland y UE5 MSI | ChatGPT contrato; Codex UE; propietario valida | Pendiente |
| R4 | Guardia F08 E2E autorizada y repetible | Codex integración, ChatGPT QA, propietario | Pendiente: prioridad jugable |
| R5 | Protagonista F10, Academia y carrera F11 sin atajos | ChatGPT diseño, Codex ejecución | Pendiente |
| R6 | F09/F12/F13/F14, amplitud mínima después de F08 | Responsables de cada dominio | Pendiente |
| R7 | QA, instalación y mantenimiento local privado F15 | ChatGPT QA, Codex build, propietario | Pendiente |

No transferir tareas propias de HOST, Lore, Sistemas S01–S19 o Planificación 2 sin sus respectivas auditorías. Este programa registra dependencias y fronteras; no crea «Planificación 3» ni altera la estructura F00–F15.

## Evidencias de aceptación y máquina objetivo

Por operación registrar: actor y principal, permiso/revisión Core, hechos observables y ocultos, orden y rechazo, recibo de consecuencias, journal, persistencia, UI UE5, fallo de IA/TTS, versión y SHA de build y assets, comando/log/captura MSI, tiempos/VRAM/RAM/CPU/FPS y decisión del propietario. Ejecutar negativas por orden falsa, contacto no observado, revisión caducada, corrupción de guardado y caída de proveedor remoto. **NullRHI/Python no prueban jugabilidad D3D12**.

MSI de referencia: i9-14900HX, RTX 4070 Laptop **8 GB VRAM**, **32 GB RAM**. Los presupuestos concretos (frametime, memoria, latencia, frecuencia de simulación y degradación) se fijarán con telemetría antes de certificar F07/F08; no se inventa un FPS medido. Evitar que IA o TTS comprometan el bucle del juego o la autoridad de Core.

## Archivo histórico

[Acta 13-10](ACTA_RECONCILIACION_F00_F06_2026-10-13.md), [cierre F04](fases/F04/ACTA_CIERRE_ADMINISTRATIVO_2026-10-31.md), [certificación técnica F05](fases/F05/F05-P05B_CERTIFICACION_INTEGRAL_MSI_20261105.md) y [criterios](CRITERIOS_DE_CIERRE.md) siguen siendo fuentes originales. Las antiguas referencias a «Clase Valhalla», #89 «Draft» o P2 bloque 4 pendiente se consultan como **historia de su fecha**, no como fotografía de hoy.
