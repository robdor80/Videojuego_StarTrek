# Proyecto HOST — Índice técnico

**Fecha:** 2026-11-11. **Repositorio único de código:** `robdor80/Videojuego_StarTrek`.

El HOST es el coordinador local de las partidas del videojuego Star Trek RPG. Conecta Unreal Engine 5 con los puentes de las reglas Star Trek y con CoreRPG, que sigue siendo la fuente de verdad. **No existe aún un HOST de producto certificado.**

## Documentación del proyecto HOST

- **[Plan Maestro del HOST v1.2](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md)**: fases H00–H13, arquitectura, responsabilidades y restricciones HOST/F11.

## Documentación H00

1. [Inventario y dependencias](H00_INVENTARIO_DEPENDENCIAS_2026-11-11.md): qué existe, qué podemos aprovechar y qué falta.
2. [Gobierno, riesgos y decisiones](H00_GOBIERNO_RIESGOS_2026-11-11.md): límites de propiedad, normas de GitHub, protección de main y reconciliación con F11.
3. [Acta H00](H00_ACTA_2026-11-11.md): alcance ejecutado, evidencias y pendientes de revisión/fusión.

**Baseline auditada:** Star Trek `main@816e72b2b6e2057c47b84473e616a6feda096016`, CoreRPG `main@76a7b7b485616d8c4994f384a90f123bf333591d`. Los archivos existentes conservan sus pins independientes.

## Fases independientes de las del videojuego

| Fase | Materia | Responsable principal |
|---|---|---|
| H00 | Auditoría y gobierno | ChatGPT |
| H01 | Arquitectura y contratos | ChatGPT |
| H02 | Núcleo y sesiones HOST | Codex |
| H03 | Identidad del jugador y personaje | ChatGPT + Codex |
| H04 | Guardado/recuperación | Codex |
| H05 | Integración CoreRPG | Codex |
| H06 | Integración Unreal Engine 5 | Codex |
| H07 | Pasarela de consumo de F11 | ChatGPT + Codex |
| H08 | Eventos y servicios | ChatGPT + Codex |
| H09 | Operaciones de nave | Codex |
| H10 | NPC, IA y computadora | ChatGPT + Codex |
| H11 | Misiones y temporadas | ChatGPT + Codex |
| H12 | Diagnósticos y rendimiento | ChatGPT + Codex |
| H13 | Certificación del HOST | ChatGPT + Codex + aprobación del usuario |

La numeración `Hxx` no sustituye a las fases `Fxx` del videojuego. Cada Hxx tendrá conversación y cierre propios. **Primero se construirá el HOST mínimo funcional; no hay que desarrollar todas las funciones de nave o narrativa para crear y recuperar una partida.**

## Decisión vinculante HOST/F11

El emisor institucional de `F11-P05-A02-03`, las reglas de carrera, competencias, autorizaciones y registros autoritativos pertenecen al **proyecto principal Star Trek RPG/F11 con CoreRPG**. El HOST **no** desarrollará un segundo emisor, no duplicará los validadores de negocio ni otorgará rangos. Solo aporta sesión, identidad operativa, contexto de confianza proporcional al juego local, acceso controlado y encaminamiento hacia las interfaces de F11. Si la API de producto F11 no está disponible, la operación permanece deshabilitada.

Las decisiones fundamentales y las fusiones definitivas corresponden al usuario. No se crean repositorios nuevos; no se alteran CoreRPG, pins históricos ni pruebas para obtener resultados artificialmente verdes.

## Estados

Distinguir siempre **PLANIFICADO, IMPLEMENTADO, PROBADO, CERTIFICADO y FUSIONADO**. El acta H00 es evidencia **documental**; no certifica ningún ejecutable HOST. La entrega de esta rama se mantiene en PR hasta revisión y autorización de fusión.
