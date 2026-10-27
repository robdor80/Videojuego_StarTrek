# F08 — Validador de evidencias, continuidad y bloqueo de ejecución

**Fecha:** 13-10-2026. **Alcance:** referencia de aceptación / QA.  
**Fase global:** sin cambio en el registro oficial (F08 planificada para runtime, F02 EN_CURSO).  
**No existe acreditación de Core↔UE5 ni de build en MSI.**

## Qué se ha implementado de verdad
- `desarrollo/tools/validation/f08_acceptance_gate.py`: auditor **read-only** para capturas procedentes de un futuro build. No escribe World State, no emite ni valida órdenes en Core, no realiza barridos y no aplica efectos.
- `desarrollo/tools/validation/test_f08_acceptance_gate.py`: **20 pruebas sintéticas** de la propia herramienta, con casos negativos (órdenes, identidades, eventos, información de pantalla, continuidad save/load, hashes y rutas).
- `desarrollo/validation/fixtures/f08/sutherland_watch_setup_v0.1.json`: escenario piloto, sin suplantar identidades de Core. Sutherland es puente de presentación, Kelvin excluido.
- `desarrollo/validation/fixtures/f08/evidence_capture_template_v0.1.json`: plantilla explícitamente `NO_EJECUTADO`, con los **13 IDs oficiales** de aceptación.
- `.github/workflows/f08-acceptance-contracts.yml`: sintaxis, suite unitaria y comprobación negativa de que la plantilla sin ejecución **NO** supera aceptación.

**CI registrada:** [F08, Actions run 38381645226](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38381645226) — SUCCESS: sintaxis, 20 pruebas unitarias y plantilla rechazada. [Roadmap governance 38381645149](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38381645149) — SUCCESS. Son exclusivamente pruebas de consistencia del validador y de estado del repositorio.

## Proceso de uso cuando exista el build real

1. Capturar desde los propietarios correspondientes las órdenes/autoridad/eventos y los antes/después de save/load (Core), la proyección al jugador y los datos de entorno, build y rendimiento (Host UE5).
2. Conservar archivos originales de evidencia **fuera del repositorio** cuando contengan partidas, registros privados, voz u otros datos sensibles. Registrar rutas relativas a una carpeta controlada, hash SHA-256 y metadatos técnicos.
3. Copiar la plantilla F08 a un manifiesto **nuevo**, sin alterar el oficial, e incorporar resultados de pruebas realmente ejecutadas. En `artifacts` se requieren: `core_trace`, `ue5_log`, `save_file`, `screenshot` y `performance`.
4. Validar localmente:

```powershell
python desarrollo/tools/validation/f08_acceptance_gate.py --capture C:\F08\captura.json --artifacts-dir C:\F08\evidencias
```

5. Interpretar salida con rigor: `BLOCKED` (faltan resultados), `INCONSISTENT` (contratos o evidencia no coherentes) o `READY_FOR_MANUAL_REVIEW` (captura *autodeclarada* formalmente coherente). **Nunca** `ACCEPTED`. El auditor verifica hashes de archivos pero **no demuestra quién produjo esos archivos**, ni que las APIs/UE5 se hayan ejecutado o que no haya filtración semántica camuflada dentro de campos permitidos.
6. Solo tras inspección independiente de logs, partida, build y funcionamiento del MSI podrá redactarse acta de aceptación real y actualizar el estado oficial.

El exit code 0 del validador significa *preparado para revisión manual*, **no guardia superada**. La plantilla `NO_EJECUTADO` devuelve error expresamente; el workflow prueba esta denegación.

## Estado real por punto de F08

| Paso | Avance autónomo comprobado | Para poder cerrar |
|---|---|---|
| P01 | Documento de escenario, contexto 2372, registro JSON Sutherland y datos de Core sin inventar | Instanciar nave, oficial, capitán, guardia y contactos en Core; mapa UE5 transitable |
| P02 | Contratos F04/F05 reutilizados + estructura de registro de orden/autoridad en auditor F08 | Acciones/autoridad reales de Core; órdenes del capitán NPC verificadas |
| P03 | Contratos F06/Sensores reutilizados + auditoría de eventos y proyección al observador | Consola 3D UE5 vinculada a acciones del Core y resultado real |
| P04 | Comprobador de continuidad antes/después y hashes de save y logs | Persistencia real completa en Core y save/load UE5 |
| P05 | 20 tests de auditor y workflow, fixture de 13 casos sin ejecutar | 13/13 pruebas E2E y negativos, performance MSI, build, licencias, aceptación |

## Dependencias que no se deben ocultar
- **F07**: Sutherland aún sin importar/recorrer/colisionar/medir en el MSI, y derechos/hash del derivado pendientes. F07 scripts PBR sí están integrados como referencia.
- **CoreRPG**: revisar API/ABI en SHA de `main` al integrar (World State, tiempo, reglas, Knowledge, Actions, persistencia y orden contextual). La 4.7 es base del guardado; 4.9–4.10 son dependencias funcionales y la 4.14 contempla integración UE5. No asumir que culminar una fase garantiza el adaptador completo de Star Trek.
- **UE5/Host**: no se dispone del proyecto .uproject en este repositorio ni de ejecución Windows; no presentar prueba Python como render/transitabilidad/build.
- **IA**: opcional, sin autoridad; caída de Gemini no puede detener operación determinista ni afirmar ejecución de órdenes.

**Política:** hasta que lleguen datos reales, guardar solamente contratos, tests y evidencias de referencia. No afirmar `CORE_INTEGRADO`, `UE5_JUGABLE` ni `ACEPTACION_SUPERADA`.
