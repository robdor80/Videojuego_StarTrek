# R2 — Conciliación de la cadena F06 y corrección de dirección (19-11-2026)

**Clase de intervención:** subsanación de auditoría, **NO continuación ni implementación de F06**. Estado oficial: F06 EN_REVISION, sin atribuir nivel UE5_JUGABLE ni una fuente espacial autoritativa. Evidencia cotejada: PR y checks GitHub a 19-11.

## Árbol de integración realmente existente

| PR | Rama y HEAD de referencia | Base actual | Checks del HEAD consultado | Situación |
|---|---|---|---|---|
| [#91](https://github.com/robdor80/Videojuego_StarTrek/pull/91) | `feat/f06-sensores-core@0f67affecbb56c7d70d129b057fa7c50497a3ebd` | `main` | 16/16 PASS | Draft; 42 ficheros, puente y QA; **fuera de main** |
| [#96](https://github.com/robdor80/Videojuego_StarTrek/pull/96) | `feat/f06-guardia-operativa-sensores-20261110@df7dcb8850932191c9453a92dbad806ef14e7bbc` | #91 | 2/2 PASS | Draft; 10 ficheros; **depende de #91** |
| [#97](https://github.com/robdor80/Videojuego_StarTrek/pull/97) | `fix/f06-aster-guardia-ux-ciencia-20261110@bbf7f5d5d89cc84b4544a6049a1924ebf9632fde` | #96 | 6/6 PASS | Draft; 16 ficheros; **depende de #96** |

Los resultados son válidos **para sus respectivos HEAD y bases**, no equivalen a una cadena montada en `main`, ni a una operación jugable en UE5. Las cuentas de pruebas deben recotejarse al retomar las PR: no son promesas de CI futura.

En `main` existen las referencias #7 y #92–#94, pero no el código nativo pendiente de las tres Draft. **No hay que repetir** el motor base, ni reemplazar sus oráculos/fixtures. La PR #95 es LCARS HTML/JS separado, sin conexión automática a F06 o Unreal.

## Fallos de dirección corregidos

1. **La realidad espacial no la inventa el sensor.** CoreRPG conserva WorldState/tiempo/guardado; el dominio espacial que corresponda proporciona un snapshot de entidades verdaderas con ID, revisión, reloj y procedencia; F06 proyecta **solo observación autorizada** y genera resultado/recibo de operación, no nuevos hechos mundiales por sí mismo. HOST transporta solicitudes y verifica la sesión; no reimplementa detección ni crea naves.
2. **QA Aster no es ordenador de la nave ni UI de jugador.** Sus fixtures pueden poblar pruebas, nunca suplir el productor de mundo ni certificar una consola interactiva.
3. **Una acción es más que un escaneo matemático.** El contrato de producción habrá de expresar: intención → actor/rol/nave → autenticidad y precondiciones F05/Core → ejecución F06 → conocimiento limitado del observador → entrega a Ciencia validada → journal y persistencia Core → respuesta de HOST → UI UE5. Rechazos y reintentos no deben mutar el mundo.
4. **Ninguna integración del stack por inercia.** Primero alinear #91 con `main`, ejecutar regresiones reales Core/F04/F05/F06 y comparar ABI; después actualizar #96 sobre la integración anterior, hacer lo mismo con #97. La CI heredada de rama y el resultado de un Draft no reemplazan esta regresión. No fusionar, rebasear ni ampliar código en este corte de auditoría.
5. **Manual P01 pendiente de aceptación visual.** Verificar íntegro el PDF/árbol de diez ramas contra versión y hash de origen; solo entonces emitir conformidad de P01. La falta de comprobación visual no invalida las pruebas Core independientes.

## Puerta entregable al retomar desarrollo (NO ejecutada aquí)

- Snapshot espacial real y limitado por revisión/tiempo, con contacto identificado, desconocido, falso y perdido; demostrar que ni LLM, ni consola, ni HOST pueden revelar entidades no observadas.
- Actor auténtico y autorización verificable; orden caducada, credenciales ajenas, replay de comando e interferencia deben denegarse sin efectos.
- Informe a Ciencia con identidad del observador, versión, procedencia, recibo de aceptación y evento confirmado, no `event_candidates` tomados por realidad.
- Save/load en **otro proceso** y coherencia antes/después, con duplicación/replay imposibles; serialización legacy auditada.
- Prueba nativa real en Core y prueba posterior en UE5/MSI cuando corresponda. Verificar latencia/memoria y fallback sin IA.
- Evidencias: SHA de producto y Core pin, resultados nativos y negativos, artefacto UE, logs, versión, operador, fecha y aceptación.

**Resultado de R2 en esta auditoría:** contrato corregido y dependencias identificadas; **implementación y fusión de #91/#96/#97 deliberadamente pendientes** para la conversación de Planificación 1 cuando se retome. No modificar F06 a CERRADA por este documento.
