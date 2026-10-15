# F15 — Acta de preparación autónoma P01–P05 (referencia verificable)

**Fecha:** 15-10-2026.  
**Base auditada:** `Videojuego_StarTrek/main@18e97128514c9d308e1854675239882429c3e6f4` (F14 fusionada, PR #20).  
**Madurez de este paquete:** referencia/QA reproducible. **No** `ACEPTACION_SUPERADA`, no build distribuible certificado, no Core integrado, no UE5 ejecutado y no perfilado real en MSI.

## 1. Criterio de trabajo

F15 es la puerta final del producto, pero no puede cerrarse antes de que sus dependencias existan. El trabajo autónomo prepara un arnés fail-closed que reutiliza las evidencias ya presentes y evita convertir CI documental en una falsa beta.

Se mantienen estas fronteras:

1. CI y pruebas Python prueban contratos/herramientas, no jugabilidad UE5.
2. Un recorrido E2E solo cuenta si fue ejecutado y tiene evidencias.
3. Métricas de rendimiento solo cuentan si proceden de una ejecución real en el MSI.
4. Un hash de build no prueba por sí solo que el build sea funcional.
5. Ningún validador offline emite `ACEPTACION_SUPERADA` ni certifica distribución.

## 2. F15-P01 — QA transversal

`tools/validation/f15_release_readiness.py` unifica tres capas de evidencia sin sustituirlas:

- QA de dominio/CI;
- integración real con Core;
- automatización/pruebas UE5.

La capa `qa` exige booleanos estrictos y referencias de evidencia. Si falta una capa, el resultado es `BLOCKED`; incluso con las tres declaradas y evidenciadas, el máximo automático es `REVIEW_REQUIRED`.

El auditor de repositorio reutiliza como fuentes de verdad el plan maestro, `ESTADO_GLOBAL.json`, criterios de cierre, el gate F08, la referencia F14 y la política de prototipos. Verifica expresamente que F15 sigue `PLANIFICADA` y que su objetivo continúa siendo `ACEPTACION_SUPERADA`.

## 3. F15-P02 — Recorrido E2E

El contrato de recorrido final queda fijado en esta secuencia mínima:

`Academia → primer destino → misión → decisión de carrera → guardado → carga`.

No se admite reordenar o saltar etapas en una captura de aceptación. Un recorrido declarado como ejecutado necesita referencias de evidencia y continuidad save/load positiva. Aun cumpliéndolo, el gate devuelve `REVIEW_REQUIRED`: la aceptación final requiere revisión humana y evidencias externas.

La plantilla `validation/fixtures/f15/f15_beta_capture_template_v0.1.json` permanece deliberadamente en `NO_EJECUTADO` y **debe ser rechazada** por CI hasta disponer de runtime real.

## 4. F15-P03 — Rendimiento y resiliencia

La captura exige estas medidas reales:

- FPS medio;
- 1% low;
- pico de VRAM;
- pico de RAM;
- tiempo CPU medio;
- duración de sesión;
- evidencia de recuperación ante fallo del proveedor remoto.

No se ha inventado un umbral de aprobación. El validador comprueba que las mediciones sean positivas, completas, ejecutadas en MSI y respaldadas por evidencia; después deja la decisión en `REVIEW_REQUIRED` con `thresholds_applied=false`.

Por tanto, esta preparación no afirma 60 FPS, consumo máximo admisible ni estabilidad de sesión larga.

## 5. F15-P04 — Castellano, controles, accesibilidad y recuperación

La puerta UX exige exactamente siete áreas:

- castellano (`es-ES`);
- controles;
- accesibilidad;
- UX;
- logs;
- migraciones;
- errores recuperables.

Solo un `PASS` en las siete áreas, con referencias de evidencia, puede pasar a revisión humana. En la fotografía actual, `localization/README.md` y `ui/README.md` continúan siendo directorios reservados; el arnés registra esta brecha y no la convierte en contenido terminado.

## 6. F15-P05 — Beta, versiones y distribución

El gate de candidato admite canales neutrales respecto a plataforma: `internal_beta`, `beta` y `release_candidate`.

Para llegar a revisión exige:

- versión semántica;
- SHA-256 del artefacto;
- build realmente ejecutado;
- E2E superado;
- migración probada;
- rollback probado;
- cero bloqueantes;
- referencias de evidencia.

Incluso entonces el resultado automático es `REVIEW_REQUIRED` con `release_certified=false`. La publicación verificable y la aceptación del autor quedan fuera de la autoridad de este script.

## 7. QA reproducible del propio arnés

Artefactos de F15:

- `tools/validation/f15_release_readiness.py`;
- `tools/validation/test_f15_release_readiness.py`;
- `validation/fixtures/f15/f15_release_readiness_scenarios_v0.1.json`;
- `validation/fixtures/f15/f15_beta_capture_template_v0.1.json`;
- `.github/workflows/f15-release-readiness-reference.yml`.

Prueba local previa a publicación:

- **15/15 pruebas unitarias PASS**;
- **37/37 escenarios del fixture PASS** mediante la prueba de regresión;
- la plantilla `NO_EJECUTADO` resulta `BLOCKED`, como debe ser.

La CI de la rama vuelve a ejecutar sintaxis, JSON, 37 escenarios, auditoría del repositorio, 15 unit tests y rechazo deliberado de la plantilla sin runtime.

## 8. Estado real y bloqueos

F15 continúa globalmente **PLANIFICADA** y P01–P05 permanecen sin marcar. Esta rama no modifica `ESTADO_GLOBAL.json`.

Para alcanzar la madurez objetivo siguen siendo necesarios, como mínimo:

- Core/Host realmente integrado y persistencia real;
- build UE5 ejecutable;
- recorrido E2E completo con Academia, destino, misión, carrera y save/load;
- perfilado real en MSI, incluida sesión larga y fallo del proveedor remoto;
- localización/UX/accesibilidad verificadas en juego;
- pruebas de migración y rollback sobre builds reales;
- cero bloqueantes y aceptación humana de la beta/candidato.

**Gobierno:** F02 sigue siendo la única fase principal `EN_CURSO`. F15 queda preparada como cierre integral, no adelantada como producto terminado.
