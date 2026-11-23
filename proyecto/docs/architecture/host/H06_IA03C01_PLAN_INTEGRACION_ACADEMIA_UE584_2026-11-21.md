# H06 — IA-03C-01 · Plan de integración de Academia y protagonista con Unreal Engine 5.8.4

**Fecha:** 21-11-2026. **Responsable:** ChatGPT. **Estado:** DISEÑO / PREPARACIÓN, NO IMPLEMENTADO EN UE NI PROBADO.  
**Repositorio:** `robdor80/Videojuego_StarTrek`. **Base:** `main` posterior a las PR #188–#192 fusionadas.  
**Proyecto UE real:** `juego/UE5/StarTrekRPG/StarTrekRPG.uproject`, UE 5.8.4; no crear otro proyecto.  
**Límite:** IA-03C conecta al candidato real de B02/B03 con Unreal; **M1 solo se cerrará tras pruebas interactivas efectivas sobre el MSI**.

## 1. Inspección de interfaces reales

| Componente en `main` | Capacidad existente | Brecha específica IA-03C |
| --- | --- | --- |
| `AcademyCandidateFactory` B02 | Crea una PERSON autoritativa y una candidatura real en `AcademyCampaign` mediante recibo privado | Solo entrada C++ de confianza, no consumible por el módulo UE a través de la ABI C |
| `AcademyPlayerBinding` B03-02 | Vincula esa PERSON a H03; `current_player` la proyecta y deniega F05 | Sin fachada pública C/Unreal para iniciar vínculo Academy |
| `SlotStore` y `AcademyCampaign::restore` B03-03 | SAVE/LOAD entre procesos con `TREKHOST4 2\nACADEMY`; preserve `TREKHOST4 1` naval | La ABI C v1 ya puede seleccionar el lector de RESTORE por `AUTO`, pero no expone consulta tipada de Academia, selección de guardado y ficha íntegra |
| `include/trek/host/host_abi.h` | ABI **1** con ocho operaciones `OPEN`…`RESTORE`; `TrekHostRequest` de 80 bytes y `TrekHostCompletion` de 120 | `OPEN` es naval, exige clase de nave; no tiene `CREATE_ACADEMY`, `BIND_ACADEMY` ni `QUERY_ACADEMY` |
| `src/host_abi.cpp` | `TrekHostClient` posee un `SessionOwner` y gestiona `submit/poll`, ocho pendientes y CLOSE reservado | Extender **sobre el mismo cliente/sesión**, sin abrir un segundo Core, exponiendo los recibos B02 solo dentro de la implementación |
| `HostRuntime.{h,cpp}` | Carga dinámicamente TrekHost.dll y resuelve símbolos ABI v1 con tamaño de estructuras fijado | Nueva interfaz C debe negociarse, sin romper exports v1 ni buscar punteros C++ internos |
| `HostSessionSubsystem.{h,cpp}` | `UGameInstanceSubsystem` con `UWorldSubsystem` por mundo, observación asíncrona, generaciones, SAVE/RESTORE | Crear entrada de Academia, vincular y consultar ficha sin bloquear Game Thread; invalidar vistas en viajes/LOAD |
| `HostDiagnosticGameMode`, `HostAutomation` y mapa | Flujo H06 diagnóstico naval, UE 5.8.4 reparado y UMG/editor disponibles | No confundir el panel diagnóstico con nueva partida jugable ni sobrescribir el mapa existente |

**Diagnóstico principal:** los subsistemas UE y la persistencia nativa son reutilizables, pero la **fachada ABI C de Academia todavía no existe**. Conectar B02/B03 mediante el `TREK_HOST_OPEN` naval, un ID introducido en Blueprint o un segundo `SessionOwner` sería incorrecto.

## 2. Objetivo funcional mínimo de IA-03C

```text
UE5: NUEVA PARTIDA (solo nombre editable del protagonista S04 v2)
     -> fachada C versionada de HOST
     -> B02 crear PERSON real con fuente canon
     -> H03 bind privado usando recibo legítimo del mismo propietario
     -> confirmación: nueva generación, campaña UUID, ficha Academy
     -> escena / UMG de diagnóstico mínima de Academia
     -> H04 SAVE alpha
     -> cerrar UE/proceso
     -> volver a abrir UE
     -> listar/seleccionar partida Academy conocida y restaurarla
     -> misma campaña/PERSON, nueva generación, ficha y candidato intactos
```

No implantar como atajo la admisión ni entrar por F05. La candidatura aún no concede plaza, curso, rango, mando o destino. La introducción cinematográfica y los assets finales siguen un plan propio; reproducir/saltar la intro no puede duplicar candidatura ni admisión. El aspecto/cosmética **no debe confundirse** con el único campo diegético autorizado hoy: nombre. Cualquier configuración visual debe disponer de contrato propio y no alterar el canon.

## 3. Contrato de fachada nativa: decisiones para Codex

1. **Preservar ABI v1 exactamente** (exports, tamaños, números de operaciones, métodos y semántica naval), incluyendo consumidor Win64 y pruebas históricas. Implantar una extensión **aditiva y negociable**: nuevos exports C de Academia o ABI v2 con negociación compatible; comparar ambas opciones, documentar elección y demostrar compatibilidad. No modificar el layout de `TrekHostRequest` v1 a escondidas.
2. La extensión se implementará **en el mismo `TrekHostClient` y `SessionOwner`**. Deberá proveer operaciones de dominio tipadas: (a) crear y vincular automáticamente al mismo candidato con recibo privado B02, (b) consultar la ficha del candidato BOUND, (c) consultar metadatos de partidas/ranuras compatibles para menú Continuar. SAVE/RESTORE deberán reutilizar H04 existente, no otra base de datos.
3. El nombre llega como UTF-8 acotado y se valida con `academy_display_name`/S04 aprobado, no con reglas reimplementadas en Unreal. No hay selección libre de especie, edad, biografía, carrera, rango o PERSON.
4. `AcademyReceipt` e `AcademyIntent` no se entregan a UE ni Blueprint: la composición de confianza los utiliza internamente. Definir una política explícita y comprobable para idempotencia de reintentos e interrupciones entre CREATE y BIND; jamás publicar al cliente un supuesto BOUND si el vínculo no quedó confirmado.
5. El sobre de salida expone únicamente datos de lectura: tipo campaña, UUID, generación, `person_id` descriptivo, nombre, estado candidato y errores estructurados. No incorporar campos `isAdmitted` modificables por UE. La lista de ranuras debe distinguir familia, compatible, recuperable, procedencia y versión.
6. Mantener la misma política asíncrona del `HostSessionSubsystem`: tickets acotados, `Poll` sin esperas, CLOSE reservado, comprobación de generación, cancelación de observación al cambiar de mundo. No esperar resultados Core en el Game Thread; no retener punteros a `TCHAR`, UTF-8 temporales, `UObject` ni buffers externos.
7. Cualquier adaptación a `TrekHostClient` debe conservar el bloqueo de F05 desde Academy BOUND/restored. No simular una campaña Academy con clase Miranda.
8. Conservar pin CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d`, F11 y contratos LOCKED.

**Decisión pendiente de implementación:** forma concreta de la extensión C (nuevos exports frente a ABI 2). Requerirá inspección de compatibilidad y pruebas. No declarar ya existente ninguna función conceptual anterior.

## 4. Subfases y responsables

| Subfase | Trabajo | Responsable | Salida de aceptación |
| --- | --- | --- | --- |
| **IA-03C-01** | Inventario, arquitectura, frontera Core/HOST/UE, UX mínima y matriz de pruebas | **ChatGPT** | Esta propuesta documental, revisable en PR |
| **IA-03C-02** | Extensión nativa ABI C para CREATE+BIND+QUERY Academy y listado de slots, con negativos e idempotencia | **Codex Cloud, GPT-6 Alto** | PR Draft, CI Linux/Windows/ASan y tests-OFF, ABI v1 intacta |
| **IA-03C-03** | Integración `HostRuntime`/`HostSessionSubsystem` y exposición segura a UI | **Codex, GPT-6 Alto**, trabajo de fuentes Cloud cuando sea posible; **MSI para validar UBT/UE** | UBT Windows, interfaces UE asíncronas y sin acoplamiento a mundos |
| **IA-03C-04** | Pantalla mínima nueva partida/continuar y ficha Academy, sin editor biográfico completo | **ChatGPT diseño + Codex implementación**, MSI para UMG y funcionalidad | E2E real crear/guardar/cerrar/continuar |
| **IA-03C-05** | Pruebas de producto/UE 5.8.4 (NullRHI, D3D12, transición UWorld, sesión y carga) y auditoría M1 | **Codex pruebas + ChatGPT auditoría + usuario aceptación** | Evidencia reproducible, acta: M1 PASS o pendientes explícitos |

**Criterio de avance:** IA-03C-02 puede empezar sin esperar diseño de gráficos. IA-03C-04 debe limitarse al mínimo jugable; no bloquear H06 por assets definitivos de intro, diálogos, voice TTS o modelos 3D.

## 5. Matriz mínima de aceptación (propuesta, NO ejecutada)

| ID | Prueba | Oráculo |
| --- | --- | --- |
| **C01** | Resolver ABI 1 en consumidor anterior | Misma semántica naval, tamaños y exports sin cambiar |
| **C02** | Nueva campaña Academy en ABI extendida | Una PERSON Core, un hecho `candidate_created`, misma generación y H03 BOUND; nunca F05 |
| **C03** | Nombre inválido o intento de editar especie/edad/biografía | Rechazo antes de crear, sin PERSON parcial |
| **C04** | Dos CREATE concurrentes/replay/ticket viejo | Una campaña y una PERSON, conflicto o replay estable |
| **C05** | Consultar ficha desde UE tras cambio `UWorld` | Misma identidad `GameInstance`, proyecciones del mundo anterior invalidadas |
| **C06** | SAVE/RESTORE al cerrar y reabrir UE en procesos diferentes | Misma campaña, PERSON, nombre y hechos, nueva generación |
| **C07** | Un slot naval histórico y uno Academy en menú Continuar | Tipos/compatibilidad/procedencia correctos, sin conversión |
| **C08** | Candidate BOUND y RESTORED intenta cinco operaciones F05 | ACCESS_DENIED antes de bridge y cero mutación |
| **C09** | Archivo manipulado / no registrado / versión antigua incompatible | Fail closed sin activar perfil impostor |
| **C10** | Cerrar sesión durante crear/guardar/cargar y viajar entre mapas | Sin callback en UObject destruido, sin deadlock ni reactivación tardía |
| **C11** | UBT/UHT Win64 Editor y Game sobre UE 5.8.4 + NullRHI/D3D12 en MSI | Evidencia local de build y ejecución positiva, no inferida de CI nativa |
| **C12** | Repetir o saltar intro + consultar estado candidato | Sin PERSON adicional ni admisión/rango inventado |

**Seguridad proporcional:** aplicación local de un jugador. No crear autenticación en red, DRM ni servidores. Los checks de integridad/identidad/autoridad del HOST son obligatorios.

## 6. Pruebas y política de recursos Unreal

- Las pruebas que tocan recursos UE deben realizarse primero sobre una copia aislada del proyecto y no sobrescribir recursos anteriores. `AGENTS.md` obliga a guardar temporales solo bajo `laboratorios/`, sin dependencias finales hacia el laboratorio.
- El README oficial indica que `.uasset` y `.umap` están excluidos de Git. No afirmar que una PR almacena widgets o mapas; documentar qué se crea, dónde queda y cómo reproducirlo.
- Antes de modificar `Content` principal, respaldar en otra unidad física con `Build/Backup-Content.ps1` y verificar con `Build/Verify-ContentBackup.ps1`. No borrar backups anteriores.
- El motor verificado es **UE 5.8.4**. En el MSI, compilar `StarTrekRPGEditor` y `StarTrekRPG` con el `Prepare-Host.ps1` del mismo proyecto/compilación y después ejecutar NullRHI/D3D12, sin usar como sustituto un laboratorio antiguo.
- No se ejecutan pruebas UE/MSI, OpenAI LIVE ni historial de admisión en IA-03C-01. Se etiquetan explícitamente NOT_RUN hasta su ejecución real.

## 7. Restricciones de gobierno

No modificar indiscriminadamente F10, CoreRPG, F05, F11, S04 ni fases futuras. F10 conserva autoridad sobre admisión; HOST gestiona sesiones/transporte; UE es presentación. Desarrollar en ramas y PR Draft. Fusionar cambios significativos solo con autorización del usuario. Todas las certificaciones requieren evidencia. No proclamar H06/M1 completado al terminar la documentación.

**Próximo encargo tras revisión de esta especificación:** IA-03C-02 para Codex Cloud, modelo **GPT-6, razonamiento Alto**.
