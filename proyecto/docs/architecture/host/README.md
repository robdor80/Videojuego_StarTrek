# Proyecto HOST — Índice técnico

Fecha: 2026-11-11. Repositorio único de código: robdor80/Videojuego_StarTrek.

HOST coordina una campaña local entre Unreal Engine 5, F04/F05/F11 y CoreRPG, que conserva la autoridad sobre el universo. **No existe todavía un HOST de producto certificado.** H00 documental fusionada mediante PR #111.

## Documentos de gobierno

- [Plan Maestro v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md): fases H00-H13, hitos M0/M1 y frontera con F11.
- [H00 — Inventario](H00_INVENTARIO_DEPENDENCIAS_2026-11-11.md): componentes reales y pines.
- [H00 — Gobierno y riesgos](H00_GOBIERNO_RIESGOS_2026-11-11.md): separación de responsabilidades y protección GitHub.
- [H00 — Acta](H00_ACTA_2026-11-11.md): evidencia de auditoría documental. PR #111 fusionada.

## H01 — Arquitectura y contratos (entrega propuesta)

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
- El proyecto principal UE todavía no dispone de StarTrekRPG.uproject; los proyectos de laboratorio no acreditan integración.
- Los pins históricos siguen intactos. H01 propone F05/F11 Core SHA 76a7b7b485616d8c4994f384a90f123bf333591d como candidato, no upgrade automático.
- Fases y PR independientes; solo el usuario autoriza fusiones. Estados PLANIFICADO, IMPLEMENTADO, PROBADO, CERTIFICADO y FUSIONADO no son intercambiables.
- Logs y artefactos temporales solo en laboratorios/ dentro del repositorio, excluidos de Git. No hay dependencias permanentes hacia esos resultados.

La H01 documental tiene 11/11 comprobaciones estáticas PASS (Actions run 43089381278) y requiere revisión/fusión autorizada antes de considerarse cerrada; sus contratos guían H02-H07, sin sustituir la certificación de F11.

## H04 — Guardado, recuperación y procedencia

Implementación propuesta en [PR #135 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/135).
Estados IMPLEMENTADO y PROBADO por alcance; NO CERTIFICADO y NO FUSIONADO.

- [Arquitectura H04](H04_PERSISTENCIA_2026-11-13.md): ranuras, procedencia, persistencia Core completa, publicación, recuperación e identidad H03.
- [Matriz y evidencia H04](H04_PRUEBAS_2026-11-13.md): casos nativos, procesos, inyección, compilaciones, CI y límites.
- [Acta técnica H04](H04_ACTA_2026-11-13.md): commits, auditoría, incidencias y riesgos pendientes.
