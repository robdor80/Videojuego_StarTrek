# F06-P01 — Auditoría de la consola de Sensores

**Fecha:** 11-10-2026. **Ámbito:** contrato y simulación de referencia; no pantalla UE5.

## Material original localizado
- Árbol: gameplay/ship_operations/consoles/sensors/sensor_menu_tree.json, v0.2.0.
- Instrucciones y reglas aprobadas: gameplay/ship_operations/consoles/sensors/README.md.
- Interacción y acciones: sensor_console_interaction_model.json; sensor_context_actions.json.
- Contratos: gameplay/ship_operations/sensor_resolution/.
- Manual editorial: docs/manuals/sensors/Manual_Operador_Sensores_Flota_Estelar_v0.1.pdf. **Localizado, pero no inspeccionado página por página:** la descarga binaria no fue accesible en esta sesión. No atribuirle cambios no verificados.

## Auditoría de las diez ramas
| ID | Responsabilidad | Grado comprobable |
| --- | --- | --- |
| status | Salud, matrices, carga, progreso | Catálogo; lectura futura de estado Core |
| scans | Corto, largo y focalizado | Barrido simulable en referencia |
| search_localize | Búsqueda por firmas y tipos | Especificación, backend avanzado pendiente |
| contacts | Contactos, fichas y acciones | Candidatos de dossier sin guardar |
| tracking | Seguir, recuperar, trayectoria | Especificación, sin ticks persistentes |
| sensor_readout | Lecturas y confianza | Datos del barrido, no todas las métricas |
| interference | Interferencia y compensación | Penalización al detectar; sin compensación operativa |
| configuration | Perfiles, potencia, matrices | Precondiciones simuladas, sin reconfigurar nave |
| results | Consultar, comparar y enviar | Parcial/final y paquete a Ciencia candidato |
| diagnostics | Calibración y soporte | Rechazo por avería; sin diagnóstico real |

El árbol aprobado conserva **10 categorías principales** y **3 modalidades de barrido**. No presentar funciones definidas solo en el árbol como si ya estuvieran implementadas.

## Recorte jugable
La v0.0.1 sigue siendo una **guardia de Sensores** con controles reales, no un lanzamiento público. El mismo contrato funcional admite interfaz de Academia y de nave; cambiar de menú no debe cancelar operaciones. Un atajo contextual puede rellenar el contacto, pero **jamás ejecutar solo**.

## Riesgos
1. Cotejar visualmente la revisión del manual PDF con árbol v0.2 antes de la interfaz final.
2. Evitar prometer backend para seguimiento, calibración o búsqueda avanzada.
3. El filtro de objetivo focalizado del wrapper es una salvaguarda de salida; selección autorizada en el motor de Core sigue pendiente.
4. La UI debe mostrar estados «disponible/bloqueado/irrelevante» y la razón del bloqueo.

**P01:** catálogo revisado; manual gráfico y funcionamiento UE5: **NO_EJECUTADO**.
