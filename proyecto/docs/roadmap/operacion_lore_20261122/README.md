# Operación LORE — Reconciliación y ampliación integral (22-11-2026)

**Ámbito:** exclusivamente documental, en la continuidad privada de *Star Trek Legends*. **Línea base auditada:** `main@8e9c70648f315dbc5c1dfba7d17c3c7a8518b088` (PR #198 fusionada). **Autoridad:** las decisiones vigentes prevalecen sobre redacciones históricas. **Estado de este registro:** candidato en rama; ninguna declaración de fusión ni certificación se infiere de su mera presencia.

## Índice de entregas

- [A01 — Auditoría de actualidad y precedencias](A01_AUDITORIA_PRECEDENCIAS.md).
- [A02 — Enterprise-D, programa Valhalla y matriz de tecnología](A02_ENTERPRISE_D_VALHALLA.md).
- [A04 — Revisión tecnológica, clínica y científica](A04_TECNOLOGIA_MEDICINA_CIENCIA.md).
- [B03 — Cronología y situación de 2383](B03_CRONOLOGIA_2383_2387.md).
- [B05 — Medicina, ciencia y especies](B05_MEDICINA_CIENCIA_ESPECIES.md).
- [B07 — Instituciones, facciones y astrografía](B07_INSTITUCIONES_ASTROGRAFIA.md).
- [B09 — Preparación de enciclopedia consultable](B09_ENCICLOPEDIA_PADD.md).
- [C11 — Biografía canónica completa del protagonista](C11_BIOGRAFIA_PROTAGONISTA.md).
- [C12 — Elenco, mando y arcos condicionales](C12_LEGENDARIOS_ARCOS.md).
- [C14 — Historia y misiones de Proyecto Valhalla](C14_HISTORIA_VALHALLA.md).
- [C15 — Guion de prólogo y storyboard de Academia](C15_PROLOGO_ACADEMIA.md).
- [D10 — Auditoría y cierre transversal](D10_AUDITORIA_CIERRE.md).

## Registro de procesos (se actualiza con evidencia real)

| P | Objetivo | Entregable principal | Estado de este paquete |
|---|---|---|---|
| 01 | Actualidad LORE-01–05 | A01 | DOCUMENTADO, revisión exhaustiva automatizada no acreditada |
| 02 | Enterprise-D y Valhalla | A02, C14 | DOCUMENTADO; integración futura |
| 03 | Cronología | B03 | DOCUMENTADO; no se sustituye LORE-03A |
| 04 | Tecnología y equipamiento | A04 | DOCUMENTADO; fichas originales NEEDS_REVIEW preservadas |
| 05 | Medicina y ciencia | B05 | DOCUMENTADO; no se certifica diagnóstico |
| 06 | Especies y civilizaciones | B05 | DOCUMENTADO, selección priorizada |
| 07 | Federación y facciones | B07 | DOCUMENTADO, sin gobiernos instanciados |
| 08 | Astrografía | B07 | DOCUMENTADO, sin coordenadas inventadas |
| 09 | Enciclopedia | B09 y JSON anexo | PREPARADO, no integrado en consola |
| 10 | Auditoría global | A01, D10 | DOCUMENTADO; pendiente validación de PR |
| 11 | Protagonista fijo | C11 y JSON anexo | BIOGRAFÍA DEFINIDA, anexo no empotrado en HOST |
| 12 | Legendarios | C12 | DOCUMENTADO; elenco 12 cerrado |
| 13 | Arcos futuros | C12 | ESCENARIOS CONDICIONALES |
| 14 | Reconstrucción | C14 | CRONOLOGÍA DE PROYECTO, sin alta garantizada |
| 15 | Prólogo | C15 | GUION DE PROPUESTA, sin assets ni reproducción |

Los estados `COMPLETE_DOCUMENTARY`, `IMPLEMENTED`, `TESTED` y `CERTIFIED` **no son intercambiables**. Una validación del repositorio prueba documentación, no juego real. Al cerrar PR, revisar checks/resultado GitHub y registrar SHA de fusión; no predeterminarlo.

## Fronteras y deuda técnica

- CoreRPG conserva verdad del mundo, hechos, tiempo, sujetos, órdenes, acceso y persistencia.
- HOST coordina sesiones; H06 IA-03B B01–B03 y C-01–C-04 tienen entregas fusionadas según registro H06, mientras C-05/M1 **sigue NOT_RUN en MSI**.
- Unreal 5.8.4 presenta la experiencia; el prólogo 2D y el ordenador contextual **no se ejecutan** por documentarlos aquí.
- Identificadores `valhalla` históricos, JSON S04 v2 y huellas empotradas se **conservan intactos**. No hay migración de partidas antiguas.
- PR abiertas #175 (cualidad terapéutica S04) y #178 (intro audiovisual general) son trabajo separado; esta operación no presume su fusión.
- La nueva autorización del 22-11-2026 delega decisiones editoriales antes reservadas a coautoría, **pero no** otorga capacidad técnica de cambiar una ABI.

## Fuentes rectoras

`CONTENT_STATUS.md`; `proyecto/docs/roadmap/README.md`; LORE-01–04, LORE-05F; DEC-0020, DEC-0021, DEC-0022; H06 control único y protocolo C-05; `mundo/sources/canon_policy.md`; `mundo/sources/provenance_policy.md`.

**GAME_ADDITION** identifica toda propuesta/decisión creativa del videojuego. El año 2383 está aprobado; el día y mes siguen sin fijarse. El futuro a partir del inicio depende de la campaña.
