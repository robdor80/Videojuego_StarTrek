# H06 — TABLERO ÚNICO DE CONTROL Y CIERRE

**Corte:** 22-11-2026, actualizado tras merge #197 y preparación documental C-05. **Responsable de seguimiento:** ChatGPT. **Fase única:** H06, integración HOST↔Unreal.
**Estado del documento:** registro de situación verificable; revisado contra fuentes y PR visibles en el repositorio. Se actualiza este archivo, **no se crean nuevas subfases de H06 por defecto**.  
**Regla de gobierno:** los identificadores ya existentes se conservan; un fallo, una prueba o un ajuste no origina otra subfase salvo dependencia técnica nueva justificada y aprobada. Los commits, incidencias y pruebas viven en la PR correspondiente. Todas las fusiones importantes requieren autorización del usuario.

## 1. Un vistazo: qué está hecho y qué no

| Bloque H06 | Situación | Evidencia / siguiente puerta |
| --- | --- | --- |
| **H06-P01…P05 — integración diagnóstica Unreal** | **IMPLEMENTADA, PROBADA en alcance histórico y FUSIONADA; M1 NO certificado** | Proyecto real `StarTrekRPG.uproject`, `HostSessionSubsystem`, diagnóstico y guardado naval; documentación H06 |
| **H06-P06 — camino de nueva partida Academia** | **IMPLEMENTADO en fuentes C-04. Pruebas UE/MSI NOT_RUN** | La entrada `-AcademyMenu` consume IA-03B e IA-03C. La aceptación en UE 5.8.4 queda pendiente |
| **IA-01 — pasarela central IA** | **FUSIONADA** en alcance nativo; LIVE no acreditado | Informe IA-01; conexión futura a consumidores del juego |
| **IA-02 — evaluación biográfica semántica** | **FUSIONADA** en su alcance; no sustituye S04 v2 | Informe IA-02; no obligar a editar biografía fija |
| **IA-03A — reglas de biografía F10** | **FUSIONADA**, pero su editor libre es **histórico y no aplicable** al protagonista fijo | Decisión S04 v2 prevalece; no borrar contratos históricos |
| **IA-03B — candidato Core real + H03 + H04** | **IMPLEMENTADA, PROBADA, AUDITADA Y FUSIONADA (nativa)** | PR #188, #189, #190, #191 y #192; misma PERSON, H03 BOUND y RESTORE en proceso nuevo |
| **IA-03C — fachada de Academia + Unreal** | **EN CURSO, C-05 DOCUMENTADA** | C-01…C-04 fusionadas; protocolo y encargo C-05 preparados, MSI/UE aún NOT_RUN; M1 no certificado |
| **M1 — HOST mínimo integrado en Unreal** | **PENDIENTE DE CERTIFICACIÓN** | Exige crear→vincular→guardar→cerrar→continuar desde UE real y aceptación MSI |

## 2. IA-03C: exactamente cinco subfases, sin crear otras por inercia

| ID | Objetivo comprobable | Responsable | Estado actual |
| --- | --- | --- | --- |
| **C-01** | Inspección y arquitectura de la frontera ABI/UE, matriz de aceptación | **ChatGPT** | **DOCUMENTADO Y FUSIONADO** en [PR #193](https://github.com/robdor80/Videojuego_StarTrek/pull/193), merge `d87c7b2cc1e6775fbcff0573ddc909b0d0a6bec7` |
| **C-02** | Fachada C productiva CREATE/BIND/QUERY y catálogo paginado de H04, con ABI v1 compatible | **Codex — GPT-6 Alto** | **IMPLEMENTADO, PROBADO Y FUSIONADO** en [PR #194](https://github.com/robdor80/Videojuego_StarTrek/pull/194), merge `098246e1bda8c40377f0e344949610c1f7cb948d`. [Informe y evidencia nativa C-02](H06_IA03C02_INTERFAZ_NATIVA_ACADEMIA_2026-11-21.md). |
| **C-03** | Adaptar `HostRuntime` y `HostSessionSubsystem` a la fachada Academy sin bloquear Game Thread | **Codex — GPT-6 Alto** | **IMPLEMENTADO, PROBADO en CI nativa/SDK, AUDITADO favorablemente en alcance Cloud y FUSIONADO** en [PR #195](https://github.com/robdor80/Videojuego_StarTrek/pull/195), merge `ddd4ce57cbacfba6cc1f227a32456f7cd5c8ee26`. Linux/Windows 297/297, ASan/UBSan 142/142, producto 5/5 + SDK 1/1 por SO. **UE 5.8.4 EN MSI: 8 pruebas NOT_RUN (listadas abajo)**. **NO CERTIFICADO en Unreal ni M1**. [Informe C-03](H06_IA03C03_INTEGRACION_UNREAL_2026-11-21.md). |
| **C-04** | Interfaz mínima Nueva partida / Continuar / ficha Academy con nombre editable | **ChatGPT UX + Codex implementación** | Diseño **DOCUMENTADO Y FUSIONADO** en [#196](https://github.com/robdor80/Videojuego_StarTrek/pull/196). Menú Slate **IMPLEMENTADO, PROBADO en Cloud nativo/SDK/presentación C++, AUDITADO FAVORABLE CON RESERVA y FUSIONADO** en [PR #197](https://github.com/robdor80/Videojuego_StarTrek/pull/197), merge `a27af56c200ebf5d8fbbaff23cb1b0cecbf56cb7`. Linux/Windows 297/297, ASan/UBSan 142/142, producto/SDK/presentación 5/5 por SO; seis checks de PR PASS. **UHT/UBT, automatizaciones Slate, UI interactiva, Win64 empaquetado y UE 5.8.4 MSI NOT_RUN; no certificada en motor**. [Informe C-04, evidencia histórica](H06_IA03C04_IMPLEMENTACION_MENU_ACADEMIA_2026-11-22.md). |
| **C-05** | Pruebas UE 5.8.4 NullRHI/D3D12/varios mundos, auditoría y aceptación M1 | **ChatGPT documentación/auditoría + Codex MSI (GPT-6 Alto) + usuario** | **PLANIFICADO Y DOCUMENTADO**, pruebas UE/MSI **NOT_RUN** y M1 **NO CERTIFICADO**. [Protocolo y criterios M1](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md) · [Encargo Codex MSI preparado, no enviado](H06_IA03C05_ENCARGO_CODEX_MSI_2026-11-22.md). |

**Puerta inmediata.** La PR #197 **ya fue auditada y fusionada** (22-11-2026). Se ha preparado C-05 de forma documental, sin ejecución MSI: continuar por las puertas G0–G7 del [protocolo M1](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md), cuando el usuario habilite Codex en su equipo. Las ocho C-03 y las cuatro automatizaciones Slate C-04, además de interacción y juego Win64 real, siguen **NOT_RUN**. No anunciar certificación M1.

### Verificaciones C-03 reservadas para MSI

| Verificación UE 5.8.4 | Estado |
| --- | --- |
| Compilación UBT de `StarTrekRPGEditor` | **NOT_RUN** |
| Compilación UBT de `StarTrekRPG` Win64 | **NOT_RUN** |
| Ejecución real con Unreal NullRHI | **NOT_RUN** |
| Ejecución real con Unreal D3D12 | **NOT_RUN** |
| Cambio real de `UWorld` en Unreal | **NOT_RUN** |
| Carga real en Unreal de las DLL preparadas en MSI | **NOT_RUN** |
| Creación, guardado, cierre de proceso y recuperación desde Unreal | **NOT_RUN** |
| Prueba interactiva del jugador en MSI | **NOT_RUN** |

## 3. Ruta mínima que constituye éxito de H06/M1

```text
Unreal 5.8.4 → Nueva partida (solo nombre) → ABI C Academy
→ B02 crea PERSON canónica real en CoreRPG
→ B03 vincula a H03 sin F05 → ficha Academy válida en UE
→ guardar mediante H04 → cerrar el juego completamente
→ iniciar otro proceso UE → Continuar → mismo personaje/hecho/campaña
→ nueva generación → gateway F05 sigue denegando órdenes navales
```

**Decisión de alcance (22-11-2026):** la Academia será una introducción/tutorial narrativo **ligero**, previsiblemente con escenas 2D; **no** un entorno 3D amplio y detallado. La técnica final de las escenas queda para las fases correspondientes. El esfuerzo 3D se prioriza en la **USS Enterprise NCC-1701-D modernizada / Valhalla**. El menú Slate C-04 sigue siendo infraestructura real, no la Academia final. Ver [registro en C-05](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md#3-decisión-de-diseño-academia-introductoria-ligera).

Quedan **fuera del bloqueo de M1** y se harán en sus fases propias: introducción cinematográfica y tutorial 2D definitivos, modelos 3D de Academia extensos (descartados como objetivo actual), NPC/voz IA, matrículas/ascensos F10/F11, sensores, narrativa de temporadas, IA LIVE completa y interfaz gráfica definitiva. No convertir tales deseos en nuevos C-06, C-07, etc.

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
- [Diseño funcional y matriz de aceptación C-04](H06_IA03C04_DISENO_FUNCIONAL_MENU_ACADEMIA_2026-11-21.md), fusionado en [#196](https://github.com/robdor80/Videojuego_StarTrek/pull/196). [Implementación C-04, PR #197 fusionada; informe histórico](H06_IA03C04_IMPLEMENTACION_MENU_ACADEMIA_2026-11-22.md).
- **C-05:** [Protocolo de certificación M1 y decisión Academia introductoria](H06_IA03C05_PROTOCOLO_CERTIFICACION_M1_2026-11-22.md); [encargo técnico Codex/MSI aún no ejecutado](H06_IA03C05_ENCARGO_CODEX_MSI_2026-11-22.md).
- [H06 índice/README](README.md) y [Plan Maestro H00–H13](PLAN_MAESTRO_HOST_v1.2_2026-11-11.md) **históricos**: sus descripciones iniciales no sustituyen este corte.
- PR fusionadas de B03: [#190](https://github.com/robdor80/Videojuego_StarTrek/pull/190), [#191](https://github.com/robdor80/Videojuego_StarTrek/pull/191), [#192](https://github.com/robdor80/Videojuego_StarTrek/pull/192).
- [Auditoría HOST anterior #183](https://github.com/robdor80/Videojuego_StarTrek/pull/183), Draft y previa al cierre de B03: contiene hallazgos ya parcialmente corregidos y **requiere reconciliación posterior**, no reapertura de B03 como bloque nuevo.

**Compromiso de seguimiento:** este tablero es la referencia operacional única para los próximos trabajos de H06; actualizaciones documentales pequeñas se agruparán cuando exista una PR activa, sin crear conversación, fase o PR distinta solo por cambiar un estado.
