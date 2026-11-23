# Encargo a Codex — HOST H06-P06: cerrar la partida inicial real

**Modelo recomendado: GPT-6. Razonamiento recomendado: Alto.**
**Repositorio:** `robdor80/Videojuego_StarTrek`.
**Base:** último `main` limpio, con PR #160 fusionada (commit `4ce7dfb5a1c62591046a50fef64379d879d3df64`).
**Entrega:** rama propia, PR **Draft**; no fusionar.
**No abrir otra fase ni volver a implementar la madurez por evidencia.**

## Lo que queremos

Que el jugador cree un personaje de ficción (por ejemplo, humano, 20 años, biografía normal), obtenga una sola `PERSON` de CoreRPG para una campaña Academia, la controle mediante H03, guarde con H04 y la recupere en Unreal después de cerrar. Sin permisos F05/F11 inventados.

## Antes de modificar

Lee `AGENTS.md`, `laboratorios/README.md`, `H06_P06_CIERRE_FUNCIONAL_MINIMO_2026-11-14.md` y los contratos actuales F10, H03, H04 y H06. Inspecciona el código real `academy_core_feasibility.cpp`, `biography_validation.cpp`, `player_bootstrap.h`, `native_session.*`, `host_abi.*`, `session_owner.*`, la persistencia y el proyecto UE real. Reutiliza las pruebas existentes y la matriz CB-01..CB-24.

**Primera entrega técnica:** reproduce con un ejemplo normal qué impide hoy crear una `PERSON` de producto. No infieras que la edad es el problema: desde PR #160 la edad declarada suficiente ya se acepta. Si el obstáculo es la revisión semántica/las fuentes F10, identifica la condición exacta y cuál sería la solución mínima. **No falsifiques el recibo ni cambies por tu cuenta el contrato F10 bloqueado.** Presenta una decisión corta para aprobación si hace falta modificar una regla de producto.

## Implementar en este orden donde sea legítimamente posible

1. **F10 candidato real.** Utilizar CoreRPG fijado y el ensayo Academy existente como prueba de viabilidad, no como factory de producto. Crear campus y `PERSON` de candidato con identidad estable e historia real en un único estado; validar entrada por F10; reintento sin duplicado y error sin publicación parcial. Candidato no es cadete ni ocupa plaza.
2. **H03 vínculo.** Unir el jugador local a esa PERSON a partir de un resultado privado del alta, sin `f05_bind_player` de tripulante ni `person_id` autorizable desde UI. No otorgar rango/permiso/orden.
3. **H04 guardar/cargar.** Persistir y recuperar campaña Academia y el mismo sujeto en otro proceso. Distinguir del save naval heredado `TREKHOST4 1`, sin romperlo. Un fallo de importación no sustituye la sesión actual.
4. **H06 Unreal.** Solo después de demostrar los tres anteriores: conectar petición de creación y vista/guardar/cargar al `StarTrekRPG.uproject` ya aprobado. Reutilizar panel de diagnóstico y ABI C existente; ampliar únicamente lo imprescindible y probar NullRHI/D3D12.

**Si algún paso necesita una decisión normativa o una API ausente**, no simular el resultado ni abrir un gran proyecto alternativo. Completa y prueba lo independiente, señala exactamente la dependencia y termina el corte con una PR auditable.

## Barreras

- La edad del jugador es verdad ficticia; solo comprobar mínimo de especie, disponibilidad, formato y fecha cuando se haya declarado. No exigir madurez biológica, certificados, expediente, IA de edad o A8.
- No crear PERSON o matrícula a partir de `trusted=true`, `validated_creation_ref` o `admission_authorized` enviados por cliente.
- No confundir CANDIDATE con ADMITTED o CADET_YEAR_1: la admisión y las plazas pertenecen a F10. No inventar un aprobado ni fecha exacta en 2383.
- No duplicar CoreRPG, worker HOST, guardado, motor UE o sistema de reglas F11. No modificar pin Core ni F04/F05/F11 históricos.
- No desplegar servicios externos o multijugador. Solo juego local.
- Resultados temporales dentro de `laboratorios/`, ignorados; no borrar ni sobrescribir laboratorios antiguos ni proyectos/artes originales.

## Pruebas mínimas

Positivas: creación única `PERSON`, vinculación H03, guardado/carga entre procesos del mismo sujeto y su biografía, proyección UE y persistencia. Si se implementa admisión legítima, plaza consumida una sola vez.

Negativas: edad inferior, especie no disponible, biografía no validada, reintento, clave repetida con otra biografía, fallo a mitad de alta, ID falsificado, `SUBMIT_SCAN` por candidato sin competencia y carga de slot alterado sin swap.

Ejecutar CI Windows, Linux, ASan/UBSan, Release tests OFF, F10, F11 aislado; tests UE MSI UBT/UHT, NullRHI/D3D12 cuando exista ruta operativa completa. Acompañar pruebas con resultados verificables, no solo declaración de éxito.

## Entrega

En `proyecto/docs/architecture/host/`, publicar un **informe compacto** con (a) qué funciona de verdad, (b) qué sigue bloqueado y el motivo exacto, (c) archivos afectados, (d) comandos y pruebas/CI, (e) HEAD y URL PR. No duplicar documentación previa ni añadir otras taxonomías/registradores.

**Estados:** IMPLEMENTADO, PROBADO, PENDIENTE y FUSIONADO por separado. H06-P06/HU-08/M1 no se certifican por documentación o fixtures. ChatGPT auditará la PR.

**Modelo GPT-6; razonamiento Alto.**
