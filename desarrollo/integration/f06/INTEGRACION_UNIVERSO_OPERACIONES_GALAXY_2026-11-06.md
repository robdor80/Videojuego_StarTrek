# F06 — Auditoría P02/P04 y perfil Enterprise-D (06-11-2026)

**Estado:** IMPLEMENTACIÓN NATIVA EN PR DRAFT #91; *NO* F06 CERRADA.
**Fuente de realidad:** única campaña CoreRPG/F04/F05; F04 original y sus oráculos históricos INTACTOS.

## 1. Integración con universo espacial: alcanzado y límite

**Implementación realizada:** `f06_host_world_snapshot` recibe del **Host de mundo autorizado** una foto completa del espacio en coordenadas globales: IDs estables, posiciones, clase/firma, transpondedor, interferencia y presencia. Valida la revisión temporal de la fuente, entradas duplicadas, rango, geometría y revisión Core; ordena las entradas por identidad, materializa firmas en Core y actualiza contactos por barridos pasivos. La ausencia de un ID en un snapshot COMPLETO pasa a «contacto perdido», nunca «nave destruida». Reaparición preserva el mismo contacto; guardar/cargar y avanzar Core mantienen el estado.

**Límite crítico:** el repositorio actual **no contiene todavía un runtime espacial Core que publique las naves y movimientos de la galaxia**. F13 y los contratos de `sistemas/universe/generation` son referencias, NO fuentes autoritativas conectadas. Por tanto, está implementado y probado el **puerto de integración y materialización**, **NO** la alimentación automática efectiva desde todas las naves existentes en un universo jugable. Queda abierta la integración con el proveedor real cuando esté desarrollado. No fabricar naves desde JSON, el catálogo 3D, diálogos Luna/Sol ni la detección.

El código se ubica en `desarrollo/integration/f06/` y utiliza entidades del WorldState Core. Sin base de datos paralela ni otro reloj, y sin cambios en el repositorio CoreRPG.

## 2. Diez áreas de Sensores: matriz de implementación nativa

| Área | Contratos ya realizados | Límites explícitos |
|---|---|---|
| Estado | `f06_array_status`, `f06_installed_profile`, `f06_diagnostics` | Control de arrays por sección física pendiente |
| Barridos | Vigilancia pasiva `f06_poll`, ejecución F05, `f06_focus` y `f06_scan_area` | Duración y colas de acción/recursos temporales completas pendientes |
| Búsqueda/localización | `f06_search_contacts_page`: clase observada, tipo observado, distancia, confianza y estado; barrido por coordenadas | No consulta directamente el universo oculto ni inventa firma por buscar una clase |
| Contactos | `f06_contacts_page`, ID opaco, pérdidas, recuperación, guardado/carga | Políticas ampliadas de archivo histórico pendientes |
| Seguimiento | `f06_tracking_status`, `f06_set_tracking`, cupos normal/prioritario, liberación automática | Comparaciones técnicas preliminares, sin simulación orbital autónoma |
| Lecturas | `F06ContactView`: posición, distancia y confianza observadas; `f06_results_page` | No interpretación científica inventada ni firma exacta con identificación débil |
| Interferencias | Compensación limitada y con coste desde `f06_configure`, junto a calidad de matrices | Bandas espectrales detalladas, cloaking avanzado y calibración por banda pendientes |
| Configuración | `f06_configuration_status`, `f06_configure`, parámetros persistentes, límites de trade-off | Intervalo preferido aún no crea un scheduler a segundos; preset es una selección persistente |
| Resultados | Instantáneas inmutables de barridos **focalizados**, `f06_compare_results`, persistencia | La vigilancia pasiva NO genera cientos de resultados históricos; comparaciones más avanzadas futuras |
| Diagnósticos | `f06_diagnostics`, `f06_run_self_test`, estados según equipo real | Reparación física y soporte Ingeniería siguen fuera de Sensores |

**Integración lateral:** `f06_science_handoff` genera solicitudes Core a Ciencia con lo observado (no resultados inventados); `f06_request_power` / `f06_decide_power` registran la aprobación legítima de Operaciones pero **NO** materializan potencia física. Consola final LCARS y visor GLB quedan en F07.

## 3. Equipamiento USS Enterprise NCC-1701-D reconstruida

`sistemas/gameplay/ship_operations/consoles/sensors/sensor_capability_profiles_f06.json` contiene cinco perfiles **para pruebas de balance**, no magnitudes canon:

1. Miranda (equipamiento tradicional).
2. Intrepid (exploración).
3. Sovereign (avanzado).
4. Odyssey (vanguardia 2383 de la ficción de juego).
5. **USS Enterprise-D de la clase Galaxy modernizada por Geordi La Forge**, refit de **una nave individual**, NO clase Valhalla ni actualización genérica a todas las Galaxy.

El generador validado por CMake `generate_sensor_profiles.py` produce coeficientes de detección de corto/largo alcance, barrido focal, resistencia a interferencias y cupos de seguimiento. La puntuación efectiva depende también de firma, rango, interferencias, potencia, integridad y configuración operativa; sigue existiendo incertidumbre. Los valores son **provisionales y ajustables** en pruebas del MSI, no distancias canónicas ni fechas de instalación acreditadas.

**Redundancia platillo/cuerpo:** en el catálogo de instalación figura la exigencia de dos matrices independientes cuando se implemente separación. La simulación física de ambas secciones y su estado independiente **NO está resuelta** por un campo `independent_arrays` en JSON; requiere la entidad/estado real de separación y dos aportaciones de sensores verificadas. No afirmar que es jugable ya.

La API `f06_host_install_profile` sólo pertenece al Host fiable y debe verificar la instalación individual antes de invocarse. En tests se utilizan cascos simulados sobre el laboratorio F04: **no se ha creado un perfil Galaxy jugable en F04 ni un puente Unreal nuevo**.

## 4. Pruebas / aceptación

- Tests nativos nuevos cubren fuente espacial estable, movimiento del observador, reaparición, claves duplicadas, perfiles cualitativos y comparativa real contra Odyssey, configuración, límites, búsqueda por tipo observado, diagnósticos, historial, persistencia e integración F05.
- Los tests son escenarios controlados que **materializan entidades confiables mediante Host**. No demuestran dinámica espacial del juego completo.
- CI: `.github/workflows/f06-sensors-native.yml` Linux y Windows. Una modificación posterior a un resultado PASS requiere volver a ejecutar CI del **mismo HEAD**.
- F05 completa, historia y regresiones de F02-F04 ya tenían evidencia de compatibilidad antes de estas adiciones; comprobar resultados del último HEAD cuando terminen.
- **PENDIENTE MSI:** compilación local, guardia F06 con mundo real, UE5.8.2 NullRHI/D3D12, seguridad de ABI, pruebas de rendimiento y aceptación del usuario.

**No fusionar la PR #91 ni declarar F06 cerrada antes de resolver los límites que afectan a la jugabilidad real.**
