# Proyecto HOST — Índice técnico

Fecha de creación: 2026-11-11. **Estado revisado: 2026-11-20**, sobre `main` SHA `57fcc1c99f3075b026525ab1411421da925cb5e5`. Repositorio: robdor80/Videojuego_StarTrek.

HOST coordina una campaña local entre Unreal Engine 5, F04/F05/F11 y CoreRPG, que conserva la autoridad sobre el universo. **No existe todavía un HOST de producto certificado.** H00–H05 están fusionadas con sus alcances; H06 ya integró y verificó el diagnóstico Unreal 5.8.2, pero **M1 sigue parcial**: falta la creación y vinculación productiva del personaje/Academia y las órdenes de jugador. IA-01, IA-02 e IA-03A están integradas; no equivalen a una integración total con el juego.

> **Nota de vigencia:** el [Plan Maestro v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) y muchas actas describen el estado histórico **en su fecha**. No deben utilizarse como estado actual de ramas, PR o módulos. Consultar también la [auditoría H00–H13 del 20/11, PR Draft #183](https://github.com/robdor80/Videojuego_StarTrek/pull/183) en su rama/PR Draft #183 mientras no se fusione.

## Documentos de gobierno

- [Plan Maestro v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md): fases H00-H13, hitos M0/M1 y frontera con F11.
- [H00 — Inventario](H00_INVENTARIO_DEPENDENCIAS_2026-11-11.md): componentes reales y pines.
- [H00 — Gobierno y riesgos](H00_GOBIERNO_RIESGOS_2026-11-11.md): separación de responsabilidades y protección GitHub.
- [H00 — Acta](H00_ACTA_2026-11-11.md): evidencia de auditoría documental. PR #111 fusionada.

## H01 — Arquitectura y contratos (entrega documental histórica, ya integrada)

1. [H01-P01 Arquitectura](H01_P01_ARQUITECTURA_v1.0_2026-11-11.md): módulos, hilos, ciclo de vida y propiedad.
2. [H01-P02 Contratos](H01_P02_CONTRATOS_v1.0_2026-11-11.md): solicitudes, resultados, errores y versiones.
3. [H01-P03 Confianza](H01_P03_CONFIANZA_v1.0_2026-11-11.md): principal, partida importada y límites offline.
4. [H01-P04 Compatibilidad](H01_P04_COMPATIBILIDAD_v1.0_2026-11-11.md): pines Core, CMake, historial y no duplicación.
5. [Matriz de conformidad H01](H01_MATRIZ_CONFORMIDAD_v1.0_2026-11-11.md): 35 casos para futuras fases; no ejecutados en runtime.
6. [Registro de contratos v1](H01_REGISTRO_CONTRATOS_v1.json): catálogo lógico verificable, no ABI compilada.
7. [Acta H01](H01_ACTA_2026-11-11.md): entregas, límites y transición a H02.

Validador estático: desarrollo/tools/validation/test_host_h01_contracts.py y CI host-h01-contracts.yml. No constituye prueba del HOST de producto.

## Fases y responsables

H00 y H01: ChatGPT (auditoría y diseño). H02: Codex (núcleo). H03: ChatGPT+Codex (identidad). H04: Codex (persistencia). H05: Codex (Core/F04/F05). H06: Codex (UE real). H07: ChatGPT+Codex (lector y pasarela NO emisora de F11). H08-H11: coordinación y sistemas progresivos. H12-H13: estabilidad y certificación.

## Restricciones vinculantes

- Solo CoreRPG conserva WorldState y tiempo autoritativo. F11 del proyecto principal desarrolla y certifica su emisor de Personal de Flota. HOST no emite comisiones, grados ni rangos, ni replica sus reglas.
- Las APIs F04/F05/F11 usan una única F04Session en hilo propietario. ID, F04Ref, cause y CAUSE=110501 no son credenciales.
- El proyecto principal UE **sí** incluye `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`. La compilación requiere preparar `host_abi.h`, `TrekHost.dll` y `TrekF04Bridge.dll` mediante `Build/Prepare-Host.ps1`. La generación del mapa diagnóstico sigue el [README de StarTrekRPG](../../../../juego/UE5/StarTrekRPG/README.md); las pruebas históricas documentadas fueron en UE 5.8.2, no certifican por sí mismas UE 5.8.4.
- Los pins históricos siguen intactos. H01 propone F05/F11 Core SHA 76a7b7b485616d8c4994f384a90f123bf333591d como candidato, no upgrade automático.
- Fases y PR independientes; solo el usuario autoriza fusiones. Estados PLANIFICADO, IMPLEMENTADO, PROBADO, CERTIFICADO y FUSIONADO no son intercambiables.
- Logs y artefactos temporales solo en laboratorios/ dentro del repositorio, excluidos de Git. No hay dependencias permanentes hacia esos resultados.

La H01 documental registró 11/11 comprobaciones estáticas PASS (Actions run 43089381278) y se integró posteriormente. Estas pruebas no sustituyen una certificación del juego ni de F11.

## H04 — Guardado, recuperación y procedencia

Implementación **fusionada** mediante [PR #135](https://github.com/robdor80/Videojuego_StarTrek/pull/135). Probada en el alcance nativo/fixtures H04; **no significa que el circuito de nueva partida M1 esté terminado ni certificado**.

- [Arquitectura H04](H04_PERSISTENCIA_2026-11-13.md): ranuras, procedencia, persistencia Core completa, publicación, recuperación e identidad H03.
- [Matriz y evidencia H04](H04_PRUEBAS_2026-11-13.md): casos nativos, procesos, inyección, compilaciones, CI y límites.
- [Acta técnica H04](H04_ACTA_2026-11-13.md): commits, auditoría, incidencias y riesgos pendientes.
