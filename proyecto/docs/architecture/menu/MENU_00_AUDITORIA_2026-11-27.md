# MENU-00 — Auditoría de partida y reutilización
Fecha 2026-11-27 · Responsable ChatGPT · Revisión inmutable `1242f7852f435e59a80ae0eddab9edf968052dc1` de main. Método: lectura directa de árbol Git (6.710 entradas, no truncado), contratos, código fuente y metadatos PR. Sin ejecución local ni Codex; no se han modificado archivos de runtime.

## P01 — H08
Fuente: [índice HOST](../host/README.md) y H08_P01…P04 de la misma carpeta. PR #207–#210 fusionadas, confirmado por índice y [acta H07](../host/H07_AUDITORIA_RECONCILIACION_2026-11-27.md). Los estados antiguos de informes no son el estado de fusión actual.
| Subfase | Capacidad real | Aplicación al menú / límite |
| --- | --- | --- |
| H08-P01 | Contrato de eventos y proyecciones, no ABI | Patrón de estados, correlación y visibilidad; no suscripción pública genérica. |
| H08-P02 | Distribución C++ interna de eventos de una orden F05 concreta; cola y acuse efímero | Aprovechar patrón para avisos autorizados; no feed de todo el universo ni API UE ya conectada. |
| H08-P03 | avance explícito interno por SessionOwner, F04/Core, revisión/tick e intención; parciales | Menú no avanza tiempo; pausa debe coordinar trabajo en curso, no crear reloj paralelo. |
| H08-P04 | notificaciones nativas derivadas de F05 (castellano) | Consumir mediante futuro adaptador; no confundir ack con efecto Core. |
H08 no tiene todavía nueva ABI pública de eventos/reloj ni widgets conectados para estas capacidades. RESTORE/CLOSE invalidan generación, tokens y resultados; no se promete entrega exactamente una vez entre procesos.

## P02 — Dependencias
- H02/H03: sesión única, hilo propietario, identidad y generación. H04: persistencia, autenticidad, compatibilidad y recuperación. H05: ABI C v1 con tickets; RETRY significa no admitido, PENDING espera, resultado de dominio distinto del transporte.
- H06/M1: menú Slate de Academia certificado con alcance limitado en fullscreen; H07 #205 corrige DPI pero la aceptación humana en ventana sigue pendiente. La corrección técnica documenta cliente 2538×1472 al 150%, no garantía de cliente 2560×1600 en ventana.
- H07 #203–205 fusionadas y técnicamente probadas según acta 27/11. Consulta de expediente/promociones confirmadas en UE, solo lectura y alcance autorizado. Emisor F11 SERVICE_UNAVAILABLE. No se certifica presencialmente ni se reevalúa aquí su CI.
- H09-P01 #211 comprobada directamente como merged (dd9b51678c85de4d3c33776772d0d305cf497237); contrato de 16 familias, 13 operaciones propuestas no disponibles en runtime. [Acta H09](../host/H09_P01_ACTA_AUDITORIA_FUSION_2026-11-27.md). H09-P02 sigue bloqueada hasta aceptación F06; TREK_HOST_SUBMIT_SCAN es legado F04/F05 y no sensor F06. No bloquear MENU-01–04 documental por ello.
- Cinemática: [PR #220](https://github.com/robdor80/Videojuego_StarTrek/pull/220) abierta Draft a fecha de consulta, head 5397ba237b8bd4b104db7bd4116e14a9925a0bd9, apilada en feat/intro-cinematic-automation. El informe de PR registra pruebas anteriores del Acto I; no demuestra Acto II ni transición final. En main el DefaultEngine.ini todavía apunta a /Game/Diagnostics/HostDiagnostic. Revisar Acto II en MENU-07; no cambiar mapas ni ramas audiovisuales hoy.

## P03/P04 — Inventario y decisión de reutilización
Rutas de código relativas a raíz del repositorio. Nativo y UE se inspeccionaron selectivamente; presencia de archivo no acredita funcionamiento ni rendimiento actual.

| Componente real | Evidencia | Decisión |
| --- | --- | --- |
| UHostSessionSubsystem / UHostWorldProjection | juego/UE5/StarTrekRPG/Source/StarTrekRPG/Private/HostSessionSubsystem.h | REUTILIZAR: GameInstanceSubsystem conserva sesión; proyección de World y resultados vigentes, invalidación, receipts. No crear segundo cliente HOST. |
| FHostAcademyMenu / FAcademyMenuFlow | misma ruta HostAcademyMenu.cpp y HostAcademyMenuFlow.h | REUTILIZAR lógica probada de operaciones, verificación, guardado inicial, recuperación, cierre seguro y catálogo; extender solo donde contrato lo permita. |
| SHostAcademyMenu | misma ruta SHostAcademyMenu.cpp | ADAPTAR patrones Slate de foco, botones, textos localizados, estados y confirmaciones. No tratar como widget UMG existente ni forzar estética actual. |
| HOST Academy / catálogo | HostSessionSubsystem.h: CreateAcademy, QueryAcademy, ListAcademySlots, RestoreAcademy; FHostAcademySlot con campaign, slot, version, compatibility, recoverability, reason | REUTILIZAR catálogo paginado y versión exacta; el filtro existente es Academia. Continuar actual abre catálogo, no última partida automática universal. |
| Persistencia H04 | desarrollo/integration/host/src/slot_store.h; host_abi.h; tests persistence_tests.cpp y academy_persistence_tests.cpp (presencia verificada) | REUTILIZAR SlotStore/save/prepare/inspect_page; no duplicar savegame UE para mundo canónico. Metadatos extra, autoguardado, política de borrado y catálogo naval: analizar MENU-03. |
| ABI | desarrollo/integration/host/include/trek/host/host_abi.h | REUTILIZAR OPEN/CLOSE/QUERY_VIEW/SAVE/RESTORE con tickets; no exponer operaciones lógicas inexistentes. |
| Lectura institucional | UHostWorldProjection::GetInstitutional y UHostSessionSubsystem::QueryInstitutional; H07 P05 | REUTILIZAR bajo visibilidad y generación; proyección de solo lectura, sin emitir ascensos ni acceder a expediente ajeno. |
| Automatización | juego/UE5/StarTrekRPG/Build/Tests/HostAcademyMenuFlowTest.cpp, Private/HostAcademyMenuAutomation.cpp, HostAcademyNavigationAutomation.cpp, HostInstitutionalAutomation.cpp | REUTILIZAR patrones y suites como regresión; no afirmar que pruebas se ejecutaron aquí. |
| UI, audio y localización | audiovisual/ui/menus/README.md y save_load/README.md reservados; carpetas ui/lcars, ui/themes, audio/music, audio/sfx, localization/es-ES presentes en árbol | REUTILIZAR estructura; carpetas no implican assets funcionales. No duplicar repositorio. |
| Ajustes y escalado | juego/UE5/StarTrekRPG/Config/DefaultEngine.ini: bAllowHighDPIInGameMode=True; H07 P05 | ADAPTAR API UE de settings/UMG según versión y capacidades reales en MENU-02/06. No encontrado menú definitivo de configuración en inventario selectivo. |
| Intro / Actos | #220 y rama base indicada | REUTILIZAR canal de transición y assets aprobados cuando se integren; no reproducir intro por defecto en todas las sesiones sin política MENU-07. |

## Riesgos y puertas de aceptación
| Riesgo | Mitigación / propietario |
| --- | --- |
| Dos menús / dos clientes HOST | Shell nuevo sobre SessionSubsystem, menú Academia como destino/flujo; preservar diagnóstico hasta regresión UE. |
| Pérdida de partida o doble solicitud | Ticket/generación, bloqueo durante operaciones, estados de guardado incierto y restauración; H04 no se reemplaza. |
| Pantalla / DPI | MENU-05/06/08, aceptación MSI 16:10 y 150% en modos ventana y fullscreen. |
| Expansión de extras y sensores | H07/F11/H09/F06 límites explícitos; ocultar o deshabilitar sin inventar información. |
| Audio/VRAM | MENU-02/07/08 presupuesto medido en MSI, carga diferida, canales independientes y transiciones. |
| Protagonista prefijado vs campo nombre del prototipo | Reconciliar lore aprobado y contrato F10 en MENU-03, sin modificar ahora candidatura ni persistencia. |

## P05 — Evidencias y conclusión
Plan maestro: [MENU v1.0](PLAN_MAESTRO_MENU_v1.0_2026-11-27.md), 9 fases/90 subfases. P01–P04: auditoría documental realizada; P05: plan redactado. Verificación estructural de conteo en la preparación de la entrega: 5+8+12+11+11+12+11+9+11=90. No se ejecutaron compilación, CTest, Unreal, Win64, GitHub Actions específicos ni pruebas MSI desde MENU-00. No se atribuye PASS de ejecución a la fase. La inspección no es exhaustiva de cada asset binario. No se generaron laboratorios, archivos pesados o recursos temporales en el equipo del propietario; limpieza no aplicable.

Criterio de cierre documental: plan e inventario publicados, cambio acotado, revisión de comparación Git y aceptación/fusión por flujo de PR. La fase siguiente de diseño puede prepararse sin MSI ni F06. Ningún estado de otras fases cambia por esta auditoría.
