# E08 — Dictamen transversal y cierre condicionado
**Situación actual: AUDIT_DOCUMENTARY_IN_REVIEW, sin fusión autorizada.**

## Dictamen editorial
LORE-03A–D ofrece un corpus estructurado: 40 hitos diplomáticos heredados sin duplicación + 26 anclas; 22 dosieres de conflictos; 13 casos y seis patrones de memoria; 35 escenarios de continuidad. El modelo preserva canon previo, distingue noticias falsas y precisión incierta, deja el futuro abierto y reserva la autoridad del WorldState a CoreRPG. La revisión de E integra estos cuatro trabajos sin abrir un segundo origen de datos.

## Hallazgos clasificados
- **E-01 / deuda documental:** cabezera de CONTENT_STATUS.md mantiene alcance anterior de tres eras y texto genérico de «todas las épocas jugables». Lo sustituye la decisión autoral posterior de solo TNG; no borrar perfiles históricos. Migración de consumidores/selector pendiente.
- **E-02 / incertidumbre legítima:** ofensiva Borg 2366 vs Wolf 359 ~2367; mantener mismo ciclo con duda de datación.
- **E-03 / incertidumbre legítima:** cronología de ocupación bajorana (presencia / anexión).
- **E-04 / solapamiento identificado:** eventos de Guerra del Dominio no son dos guerras.
- **E-05 / conocimiento:** golpe tzenkethi reportado falsamente, no hecho histórico.
- **E-06 / pendientes autor:** comienzo exacto dentro de 2383, fecha real y matrícula Valhalla, futuras asignaciones no aprobadas.
- **E-07 / deuda técnica:** importación a CoreRPG, reloj/corte, deltas, persistencia, aislamiento de campaña, evolución offscreen, conocimiento y vistas UE5/NPC/IA requieren pruebas reales.
- **E-08 / deuda externa:** F07 tiene una regresión histórica relativa al inventario/evidencias UE5, no subsanable falseando resultados; fuera de alcance de esta auditoría.

No se afirman contradicciones canónicas resueltas donde la evidencia admite más de una lectura. El reparto de fuentes de verdad es consistente a nivel de arquitectura documental; no se ha realizado verificación audiovisual completa de cada hecho.

## Criterios para propuesta de fusión
1. Validador y pruebas E + regresiones relevantes correctos en CI.
2. Diff limitado a documentación E, validador/tests E, workflow E y notas de coordinación sin cambiar decisiones A–D.
3. Conservar en CONTENT_STATUS.md la fila E TODO hasta fusión.
4. Revisar las comprobaciones del último HEAD. Solicitar al autor autorización.
5. Tras fusión autorizada, verificar commit de merge, checks posteriores y regularizar estado mediante PR administrativa, **nunca antes**.

**Dictamen propuesto:** base histórica **documentalmente preparada con reservas explícitas**; no implementación certificada ni cierre administrativo definitivo de LORE-03. Esta propuesta permanece sujeta a pruebas/CI/PR y autorización de merge.
