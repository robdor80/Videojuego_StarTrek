# H09-P03-C01 — Primer encargo para Codex Cloud (preparado, NO ejecutado)

**Modelo solicitado por el propietario:** Sol 6.2 — **razonamiento Medium**.  
**Tarea prevista:** factibilidad CoreRPG fijado y, *solo si ya existe costura autoritativa aprobada*, primer adaptador mínimo de solo lectura/propuesta.  
**Estado:** ENCARGO PREPARADO, **no lanzado**. Ejecutar tras fusión de la preparación documental H09-P03 y cuando el propietario decida consumir cuota de Codex.

## Prompt para copiar a Codex Cloud

```text
STAR TREK RPG — HOST H09-P03-C01
MODELO: Sol 6.2
RAZONAMIENTO: Medium
REPOSITORIO: robdor80/Videojuego_StarTrek
TRABAJO: Codex Cloud sobre rama propia + PR Draft. No fusionar.

Objetivo de esta primera intervención:
1. Inspeccionar de verdad el CoreRPG fijado por HOST en 76a7b7b485616d8c4994f384a90f123bf333591d, las costuras F04/F05, HOST H02-H08 y el adaptador UE real. Identificar con ruta/símbolo/contrato si Core ya posee posición naval, solución de ruta, motor de desplazamiento (impulso/warp/segmentos), ticks de viaje, persistencia y control de permisos. No inferir capacidades por nombres como F04_MOVE.
2. Leer obligatoriamente AGENTS.md y:
   - proyecto/docs/architecture/host/H09_P03_AUDITORIA_ARQUITECTURA_PLAN_2026-11-27.md
   - proyecto/docs/architecture/host/H09_P03_CONTRATO_NAVEGACION_CONN_v1.json
   - proyecto/docs/architecture/host/H09_P01_REGISTRO_CONSOLAS_v1.json
   - sistemas/gameplay/navigation/README.md
   - sistemas/gameplay/navigation/navigation_order_contract.json
   - sistemas/gameplay/navigation/navigation_state.json
   - sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_navigation_route_proposal_v0.1.json
   - desarrollo/integration/f05/include/f05_orders.h
3. Comprobar si la lectura de posición propia y la propuesta de ruta sobre destinos YA CONOCIDOS pueden implementarse directamente mediante una API real del dominio, sin F06 y sin duplicar WorldState. Verificar explícitamente qué datos conocidos están disponibles en tiempo de ejecución y cuáles solo existen como documentos JSON.
4. Si, Y SOLO SI, esas APIs autoritativas ya están disponibles en el pin aprobado y el cambio es aditivo, implementar el adaptador C++ interno mínimo de consulta/propuesta con:
   - sesión/generación/identidad H03, hilo Core dueño, contexto de nave/puesto y lectura por observador;
   - distinción estricta entre propuesta y ejecución;
   - rechazo tipado SERVICE_UNAVAILABLE cuando falte la operación real;
   - revalidación de revisión; invalidación SAVE/RESTORE y rechazo sin mutación;
   - sin ABI pública/UE nueva en esta primera intervención salvo justificación previa en informe;
   - pruebas nativas independientes de F06, Windows/Linux cuando sea posible.
   No construir un pathfinder ni motor de movimiento provisional, ni cargar JSON de referencia como WorldState de producción.
5. Si no existe la capacidad real en Core, DETENER la implementación funcional y entregar un INFORME DE BLOQUEO POR DEPENDENCIA con:
   - rutas y símbolos inspeccionados, evidencia positiva/negativa,
   - interfaces mínimas que el Core necesitaría publicar,
   - opciones de integración y consecuencias para el pin de Core, sin modificarlo,
   - fases realistas para completar D/E,
   - matriz de pruebas pendientes y recomendación precisa para el siguiente encargo.
6. No modificar CoreRPG ni sus versiones fijadas, ni pruebas históricas ni emisor F11. No modificar F06, H09-P02 o H09-P04. No hacer integración UE5/MSI; no certificar ni declarar ningún motor de navegación implementado sin pruebas reales.
7. Todos los trabajos temporales y sus limpiezas conforme a AGENTS.md, exclusivamente dentro de laboratorios/ de este repo, sin sobrescribir artefactos previos. Conservar informe definitivo ligero en proyecto/docs/architecture/host/H09_P03_C01_FACTIBILIDAD_CORE_*.md con commit, condiciones, pruebas y resultado.
8. Crear rama propia y PR Draft sin fusionar. Ejecutar pruebas aplicables y GitHub Actions; si alguna falla, no presentar la tarea como PASS. Informar de SHA de HEAD, PR, CI, límites y siguientes pasos.

Restricciones importantes:
- Hoy no hay MSI.
- F06 aún espera la aprobación presencial del propietario; H09-P02 está BLOQUEADA.
- H09-P03-C01 puede avanzar solo en rutas hacia destinos de carta conocida y análisis de APIs; intercepciones de contactos, riesgos recién detectados y E2E sensores quedan aparcados.
- La recepción de datos Navegación→CONN no autoriza mando ni ejecuta warp.
- F05OrderRequest actual declara F04_SCAN como único tipo P01 soportado: NO añadir tipos de CONN, no cambiar ABI ni reutilizar F04_MOVE para vuelo por parecido de nombres.
- H08 f04_advance no equivale a progreso naval, salvo prueba explícita en Core.
- Aun si no hay API real, un informe de factibilidad completo y verificable es un resultado válido. No eludir bloqueos.
- No consumir tiempo rediseñando UX ni S11; los contratos ya están definidos. Evita reestudiar lo documentado y trabaja en la costura nativa.
```

## Decisión esperada

- **Camino 1 — CAPACIDAD EXISTENTE VERIFICADA:** se admite adaptar primero las consultas/propuestas sin mutación, con pruebas reales y PR Draft.
- **Camino 2 — CAPACIDAD NO EXISTENTE O NO AUTORIZADA:** informe de dependencia y parada técnica; cualquier ampliación de Core o pin necesita decisión independiente del propietario.
- **Camino 3 — CAPACIDAD PARCIAL:** delimitar exactamente la lectura/propuesta operativa; no prometer ejecución ni simulación de movimiento por fragmentos.

En cualquier caso H09-P03-E (orden real CONN y movimiento) permanece pendiente hasta tener motor Core y autoridad F04/F05 verificados; H09-P03-F requiere integración y validación en MSI.
