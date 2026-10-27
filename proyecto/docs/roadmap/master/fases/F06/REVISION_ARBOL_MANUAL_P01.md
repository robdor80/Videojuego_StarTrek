# F06-P01 — Auditoría de la consola de Sensores

**Fecha:** 11-10-2026. **Ámbito:** contrato y simulación de referencia; no pantalla UE5.

## Material original localizado
- Árbol: sistemas/gameplay/ship_operations/consoles/sensors/sensor_menu_tree.json, v0.2.0.
- Instrucciones y reglas aprobadas: sistemas/gameplay/ship_operations/consoles/sensors/README.md.
- Interacción y acciones: sensor_console_interaction_model.json; sensor_context_actions.json.
- Contratos: sistemas/gameplay/ship_operations/sensor_resolution/.
- Manual editorial: `proyecto/docs/manuals/sensors/Manual_Operador_Sensores_Flota_Estelar_v0.1.pdf`. **Auditoría complementaria 13-10-2026:** la copia accesible en archivos del proyecto (mismo nombre) tiene **16 páginas**; se leyó el **texto de las 16** y se inspeccionaron visualmente la portada (p. 1) y la referencia rápida (p. 14). No fue posible cotejar su hash con el binario de GitHub ni renderizar todas las páginas: **revisión visual integral NO_EJECUTADA**; evitar afirmar que el PDF de `main` es idéntico.

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

## Revisión de contenido del manual PDF (13-10-2026, alcance limitado)

- **Contenido textual:** 16 páginas inspeccionadas mediante lectura de texto disponible. El índice de p. 2 enumera las diez familias operativas: estado, barridos, búsqueda, contactos, seguimiento, lectura, interferencias, configuración, resultados y diagnóstico; aparecen explicadas en pp. 3–10. Los procedimientos, informes, errores, seis ejercicios y referencia rápida están en pp. 11–14. El registro de edición se encuentra en p. 16.
- **Cotejo semántico:** manual, README y `sensor_menu_tree.json` v0.2 comparten esas diez ramas y tres barridos. La separación Sensores/Ciencia, la incertidumbre, la precedencia de recursos de OPS y la conservación de observaciones figuran explícitamente.
- **Brecha no bloqueante del motor de referencia:** el manual (p. 4) permite describir barrido focalizado sobre **contacto, coordenadas o zona definida**; el *wrapper Python F06* exige un `target_contact_id` previamente conocido. Esto es un **recorte de referencia**, no hay que modificar el manual ni declarar soporte efectivo para coordenadas/zonas hasta disponer de un motor autorizado.
- **Brechas de runtime:** la sensibilidad/ruido de búsquedas, seguimiento múltiple, recuperación de contacto, perfiles, calibración y seguimiento prolongado descritos en el PDF no están cubiertos por una implementación Core/UE5. No etiquetar esas pantallas como funcionales en v0.0.1.
- **Hallazgo editorial:** el texto extraíble de la **página 15** contiene únicamente cabecera/pie; la referencia rápida termina en p. 14 y el registro de edición aparece en p. 16. Posible página de separación vacía o salto accidental. **Pendiente comprobación visual del binario exacto de GitHub** antes de decidir si se elimina/remaqueta.
- **Aspectos visuales comprobables:** la portada y la p. 14 son legibles en la representación recibida; no se certifican cortes ni tablas en las demás páginas sin render completo.
- **Incidencias de prácticas históricas** (p. ej. TUT-08 sensibilidad, TUT-10 sector y TUT-11/12 Seguimiento) requieren ejecución en la interfaz real; esta lectura del manual no constituye regresión funcional de esas prácticas.

**Resultado:** auditoría textual realizada; **P01 sigue EN_REVISION** hasta cotejar visualmente las 16 páginas del PDF exacto, decidir sobre p. 15 y registrar evidencia completa. No se altera el PDF ni el árbol aprobado con una inspección parcial.

## Recorte jugable
La v0.0.1 sigue siendo una **guardia de Sensores** con controles reales, no un lanzamiento público. El mismo contrato funcional admite interfaz de Academia y de nave; cambiar de menú no debe cancelar operaciones. Un atajo contextual puede rellenar el contacto, pero **jamás ejecutar solo**.

## Riesgos
1. Completar inspección visual del PDF exacto en GitHub (la auditoría textual y el cotejo de 10 ramas ya están hechos) antes de la interfaz final.
2. Evitar prometer backend para seguimiento, calibración o búsqueda avanzada.
3. El filtro de objetivo focalizado del wrapper es una salvaguarda de salida; selección autorizada en el motor de Core sigue pendiente.
4. La UI debe mostrar estados «disponible/bloqueado/irrelevante» y la razón del bloqueo.

**P01:** catálogo y texto de 16 páginas revisados; muestra visual limitada a pp. 1 y 14. **Auditoría visual integral y funcionamiento UE5 NO_EJECUTADOS**.
