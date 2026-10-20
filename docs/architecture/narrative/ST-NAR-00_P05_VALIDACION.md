# ST-NAR-00 — P05 Plan de validación, evidencia y puerta de integración
**Estado:** referencia técnica offline implementada en rama; nunca calificar como integración de juego terminada por superar CI.

## Entregas verificables
- Esquemas documentales JSON Schema draft 2020-12: season manifest, chapter y campaign context.
- Datos técnicos sintéticos: paquete de dos capítulos; contexto completo y delta con hechos históricos y estado presente diferentes.
- tools/validation/st_nar_00.py: validador de formato/contenido declarativo y grafo, inspección de cobertura de contexto, gate opt-in/compatibilidad, producción de ZIP de contexto derivado del JSON y comprobación de integridad del ZIP.
- tools/validation/test_st_nar_00.py: casos herméticos positivos/negativos con pruebas para duplicados, eventos fuera de tiempo, historia inmutable, stale snapshot, permiso opt-in, necesidades dormidas, rutas, ciclos, código inesperado, capacidades, seguridad de ZIP.
- Workflow .github/workflows/st-nar-00-reference.yml ejecuta sintaxis, unit tests, pack, contextos y ZIP en Actions para PR; sin modificaciones de saves.

## Comandos reproducibles desde raíz repo (Python 3.10+)
- python -m unittest discover -s tools/validation -p 'test_st_nar_00.py' -v
- python tools/validation/st_nar_00.py check-pack --pack validation/fixtures/seasons/reference_pack
- python tools/validation/st_nar_00.py check-context --context validation/fixtures/seasons/campaign_context_full_v0.1.json
- python tools/validation/st_nar_00.py check-context --context validation/fixtures/seasons/campaign_context_delta_v0.1.json
- python tools/validation/st_nar_00.py export-bundle --context validation/fixtures/seasons/campaign_context_full_v0.1.json --output /tmp/st_nar_00_context_reference.zip
- python tools/validation/st_nar_00.py verify-bundle --bundle /tmp/st_nar_00_context_reference.zip

## Cobertura y límites
El checker stdlib implementa de forma explícita un SUBCONJUNTO de JSON Schema usado por estos contratos. No se presenta como certificador general del estándar. La revisión de arco y compatibilidad narrativa sutil es humana.
El ZIP es una VISTA derivada de contexto suministrado, con sha256 como detección de alteración accidental, no firma criptográfica ni prueba de proveniencia. No conecta al juego ni demuestra que un reporte sea exhaustivo; esa cobertura depende del adaptador CoreRPG.
La evaluación de incorporación NUNCA instala un pack; los estados REVIEW_REQUIRED / DORMANT_ELIGIBILITY indican posibilidades sujetas a runtime y autorización. Los datos de referencia tienen status reference_only y no se instalan.
Un ejemplo sin argumento no sustituye a la Temporada 0 (ST-NAR-01 creativa), que solo se escribirá con el autor.

## Integración pendiente fuera de alcance offline P05
Bloqueador B01: revisar APIs reales de CoreRPG posteriores a 4.8 para snapshot atómico, event stream, extensión narrativa de guardado, idempotency journal y dos fases de commit.
B02: implementar con garantías la activación de premisas seed candidate por reglas autoritativas y no por presión de argumento.
B03: implementación de gestor de packs sandboxed; firma/política de confianza opcional, importación transaccional, migraciones, rollback, dependencia de assets y revocación segura.
B04: UI UE5 para exportación FULL vs visible, confirmación de spoilers, picker de pack, opt-in en saves vivos y errores traducidos.
B05: pruebas E2E, realismo de mando, NPC offscreen, guardado/carga/LOD, daños, carrera/Academia, MSI; evidencia necesaria para cerrar integración.

## Puerta para PR de referencia
[ ] GitHub CI de referencia verde, scripts compilan y fixtures pasan.
[ ] Revisión de rutas y no alteración de F01–F15 ni de CoreRPG.
[ ] Revisión humana de seguridad/contratos; status final ST-NAR-00 'ARQUITECTURA REFERENCIA PREPARADA' y runtime 'BLOQUEADO POR INTEGRACIÓN', nunca producto listo.
[ ] El autor fusiona PR; después verificar main, borrar rama solo tras validación, pull móvil/PC.

## Cronograma técnico posterior
I01 adaptar cursor/snapshot y paginación a API Core; I02 implementar importador real y persistencia; I03 integrar con mando/IA/UE5; I04 pruebas de campañas reales e incorporaciones tardías; I05 diseño narrativo conjunto de S00 cuando alcance su fase propia. Las fases I no han sido ejecutadas.

## Rastro de decisiones
D01–D09 acordadas en ST-NAR-00 y GCPN aprobado el 16-10-2026. Especificación de referencia P03–P05 queda sujeta a CI y auditoría posterior a PR.