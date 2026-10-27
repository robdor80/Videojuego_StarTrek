# E07 — Validación editorial y regresiones
## Cobertura nueva
El validador E comprueba el árbol documental requerido; referencias A/B/C/D; unicidad de IDs entre eventos heredados/anclas; correspondencia dosieres→eventos, casos de memoria→eventos/dosieres, patrones institucionales→eventos; estado documentario de A–D; fechas 2383/2387 sin día inventado; selector único jugable; control de WorldState, Rómulo y ausencia de futuro obligatorio; no declaración anticipada de cierre E.

Se incluyen tests negativos que mutan datos de entrada para comprobar rechazo de: IDs duplicados, referencias ausentes, evento futuro obligatorio, era histórica jugable, autoridad IA, orden temporal del mismo año inventado, memoria sin acontecimiento real. Son **tests sobre contratos documentales**, no pruebas de CoreRPG.

## Regresiones preexistentes previstas en CI
LORE-01D, LORE-02E, LORE-03A, B, C, D. Los workflows de dichas fases no se sustituyen ni desactivan. El workflow E comprobará Python 3.12 y ejecutará los validadores/test de los paquetes citados. No se exige que E cambie otros validadores ajenos.

## Controles de revisión antes de fusionar
Comprobar diff completo; confirmar ninguna modificación de main ni de sistemas runtime; inspeccionar CI sobre HEAD actualizado; registrar incidentes y estado; pedir autorización expresa; después de fusionar regularizar CONTENT_STATUS mediante PR administrativa aparte. Si CI falla, E sigue en revisión, no COMPLETE.

## Matriz de amenazas
| Caso | Decisión esperada |
|---|---|
| Cronología duplicada con mismo ID | REJECT |
| Referencia a guerra/evento desconocidos | REJECT |
| Destrucción de Rómulo predeterminada en 2387 | REJECT |
| Datos de 2383 con día inferido | REJECT |
| Pike/Kirk como nueva campaña | REJECT |
| IA cambia WorldState | REJECT |
| Testigo nacido después del suceso | REJECT |
| Campañas aisladas divergentes bajo CoreRPG | ALLOW conceptual; NO_RUNTIME_VERIFIED |
