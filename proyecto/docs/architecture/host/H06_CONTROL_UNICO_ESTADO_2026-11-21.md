# H06 — TABLERO ÚNICO DE CONTROL Y CIERRE

**Corte:** 21-11-2026. **Responsable de seguimiento:** ChatGPT. **Fase única:** H06, integración HOST↔Unreal.  
**Estado del documento:** registro de situación verificable; revisado contra fuentes y PR visibles en el repositorio. Se actualiza este archivo, **no se crean nuevas subfases de H06 por defecto**.  
**Regla de gobierno:** los identificadores ya existentes se conservan; un fallo, una prueba o un ajuste no origina otra subfase salvo dependencia técnica nueva justificada y aprobada. Los commits, incidencias y pruebas viven en la PR correspondiente. Todas las fusiones importantes requieren autorización del usuario.

## 1. Un vistazo: qué está hecho y qué no

| Bloque H06 | Situación | Evidencia / siguiente puerta |
| --- | --- | --- |
| **H06-P01…P05 — integración diagnóstica Unreal** | **IMPLEMENTADA, PROBADA en alcance histórico y FUSIONADA; M1 NO certificado** | Proyecto real `StarTrekRPG.uproject`, `HostSessionSubsystem`, diagnóstico y guardado naval; documentación H06 |
| **H06-P06 — camino de nueva partida Academia** | **PARCIAL**; los caminos históricos de formulario/biografía no constituyen la nueva entrada UE con protagonista fijo | La realización final consume IA-03B e IA-03C; no duplicar un segundo camino de creación |
| **IA-01 — pasarela central IA** | **FUSIONADA** en alcance nativo; LIVE no acreditado | Informe IA-01; conexión futura a consumidores del juego |
| **IA-02 — evaluación biográfica semántica** | **FUSIONADA** en su alcance; no sustituye S04 v2 | Informe IA-02; no obligar a editar biografía fija |
| **IA-03A — reglas de biografía F10** | **FUSIONADA**, pero su editor libre es **histórico y no aplicable** al protagonista fijo | Decisión S04 v2 prevalece; no borrar contratos históricos |
| **IA-03B — candidato Core real + H03 + H04** | **IMPLEMENTADA, PROBADA, AUDITADA Y FUSIONADA (nativa)** | PR #188, #189, #190, #191 y #192; misma PERSON, H03 BOUND y RESTORE en proceso nuevo |
| **IA-03C — fachada de Academia + Unreal** | **EN CURSO** | IA-03C-01…05; única vía restante para cierre M1 |
| **M1 — HOST mínimo integrado en Unreal** | **PENDIENTE DE CERTIFICACIÓN** | Exige crear→vincular→guardar→cerrar→continuar desde UE real y aceptación MSI |

## 2. IA-03C: exactamente cinco subfases, sin crear otras por inercia

| ID | Objetivo comprobable | Responsable | Estado actual |
| --- | --- | --- | --- |
| **C-01** | Inspección y arquitectura de la frontera ABI/UE, matriz de aceptación | **ChatGPT** | **DOCUMENTADO, PR Draft #193 sin fusionar** |
| **C-02** | Nueva fachada C productiva CREATE+BIND+QUERY Academy y catálogo mínimo de ranuras; preservar ABI v1 | **Codex — GPT-6 Alto** | **IMPLEMENTADA, pruebas locales PASS; CI y auditoría pendientes**. [Informe C-02](H06_IA03C02_INTERFAZ_NATIVA_ACADEMIA_2026-11-21.md); PR Draft dependiente de #193 en preparación. Ejecución local Windows y CI, sin ejecutor Cloud conectado |
| **C-03** | Adaptar `HostRuntime` y `HostSessionSubsystem` a la nueva fachada sin bloquear Game Thread | **Codex — GPT-6 Alto** | **PENDIENTE**; validación UE local MSI |
| **C-04** | Interfaz mínima Nueva partida / Continuar / ficha Academy (nombre editable, sin biografía libre) | **ChatGPT UX + Codex implementación** | **PENDIENTE** |
| **C-05** | Pruebas UE 5.8.4 NullRHI/D3D12/varios mundos, auditoría y aceptación M1 | **Codex + ChatGPT + usuario** | **PENDIENTE** |

**Puerta inmediata:** integrar o revisar la PR documental **#193** y ejecutar **C-02**. **No encargar a Codex repetir C-01**: ya está redactada. La implementación C-02 puede usar la rama #193 si sigue abierta, creando PR Draft dependiente; después de su fusión actualizar a `main`.

## 3. Ruta mínima que constituye éxito de H06/M1

```text
Unreal 5.8.4 → Nueva partida (solo nombre) → ABI C Academy
→ B02 crea PERSON canónica real en CoreRPG
→ B03 vincula a H03 sin F05 → ficha Academy válida en UE
→ guardar mediante H04 → cerrar el juego completamente
→ iniciar otro proceso UE → Continuar → mismo personaje/hecho/campaña
→ nueva generación → gateway F05 sigue denegando órdenes navales
```

Quedan **fuera del bloqueo de M1** y se harán en sus fases propias: introducción cinematográfica completa, modelos 3D de Academia, NPC/voz IA, matrículas/ascensos F10/F11, sensores, narrativa de temporadas, IA LIVE completa y interfaz gráfica definitiva. No convertir tales deseos en nuevos C-06, C-07, etc.

## 4. Reglas operativas para no perder el control

1. Una sola PR Draft o un conjunto encadenado **dentro de la misma subfase en curso**. No fusionar sin el usuario.
2. Ante un defecto pequeño: corregir dentro de la misma PR. Ante defecto de una fase ya fusionada: PR de corrección con etiqueta del ID original, **no** crear subfase adicional.
3. Cada respuesta de seguimiento H06 comienza por **ESTAMOS EN C-XX**, indica PR, evidencia y siguiente acción. Si el usuario dice “siguiente”, significa pasar al **ID existente** y no fragmentarlo.
4. C-01 es exclusivamente documento, por lo que no tiene CTest; C-02 tendrá pruebas de biblioteca/ABI; C-03/04/05 deben validar UE real en MSI cuando corresponda.
5. Mantener `AGENTS.md`: temporales solo en `laboratorios/`, sin proyectos paralelos; proteger binarios `.uasset/.umap` fuera de Git mediante copia en unidad diferente antes de modificación.
6. Estados distintos: **PLANIFICADO / DOCUMENTADO / IMPLEMENTADO / PROBADO / AUDITADO / FUSIONADO / CERTIFICADO**. Ningún check CI nativo certifica por sí solo Unreal.
7. El HOST no legisla F10 ni F11; el candidato no adquiere plaza ni grado por el hecho de entrar en UE. CoreRPG es fuente de verdad.

## 5. Documentos y trazabilidad

- [Diseño detallado C-01](H06_IA03C01_PLAN_INTEGRACION_ACADEMIA_UE584_2026-11-21.md), PR [#193](https://github.com/robdor80/Videojuego_StarTrek/pull/193).
- [H06 índice/README](README.md) y [Plan Maestro H00–H13](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) **históricos**: sus descripciones iniciales no sustituyen este corte.
- PR fusionadas de B03: [#190](https://github.com/robdor80/Videojuego_StarTrek/pull/190), [#191](https://github.com/robdor80/Videojuego_StarTrek/pull/191), [#192](https://github.com/robdor80/Videojuego_StarTrek/pull/192).
- [Auditoría HOST anterior #183](https://github.com/robdor80/Videojuego_StarTrek/pull/183), Draft y previa al cierre de B03: contiene hallazgos ya parcialmente corregidos y **requiere reconciliación posterior**, no reapertura de B03 como bloque nuevo.

**Compromiso de seguimiento:** este tablero es la referencia operacional única para los próximos trabajos de H06; actualizaciones documentales pequeñas se agruparán cuando exista una PR activa, sin crear conversación, fase o PR distinta solo por cambiar un estado.
