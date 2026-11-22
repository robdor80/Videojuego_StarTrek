# A04 — Revisión editorial de tecnología, equipamiento, medicina y ciencia

**Resultado:** compilada una matriz de uso seguro de los catálogos existentes. **No se altera `status=NEEDS_REVIEW` de ninguna ficha por decreto**, porque un estado de dataset no es prueba de revisión individual de su contenido, enlaces y fuentes.

## Inventario verificado en main

| Colección | Conteo observado | Estado almacenado | Autoridad |
|---|---:|---|---|
| `mundo/lore/technology/lore02_a_system_atlas_v0.2.json` | 45 sistemas, 8 huecos A-G01–A-G08 | NEEDS_REVIEW | referencia no runtime |
| `mundo/lore/equipment/lore02_b_equipment_catalogue_v0.1.json` | 73 equipos, 7 categorías | NEEDS_REVIEW | referencia no runtime |
| `mundo/lore/medicine/lore02_c_species_clinical_atlas_v0.1.json` | 26 perfiles de especie | NEEDS_REVIEW | no diagnóstico |
| `mundo/lore/medicine/lore02_c_conditions_v0.1.json` | 38 entradas clínicas | NEEDS_REVIEW | no prescripción |
| `mundo/lore/science/lore02_d_phenomena_atlas_v0.1.json` | 20 fenómenos | NEEDS_REVIEW | no spawn ni oráculo |

Cierre histórico de LORE-02 por #31/#33/#34/#35/#36 **no implica** ficha revalidada en 2026. Evitar copiar catálogo de equipos al manifest de una nave: fuente existente ≠ equipamiento asignado.

## Matriz cualitativa de operación

| Familia | Puede decir la enciclopedia con procedencia | Nunca debe afirmar sin WorldState + permisos |
|---|---|---|
| Propulsión de impulso/warp | concepto, limitaciones, requisitos de energía, daño y navegación | velocidad alcanzable de nave averiada, llegada prevista inventada |
| Energía, EPS y reactor | dependencias, aislamiento, refrigeración y riesgo | potencia disponible, avería reparada o consumo cero |
| Escudos y ablativo | categoría tecnológica, riesgos e instalación específica | escudos triples Galaxy activos por legado Valhalla |
| Fáseres, torpedos | funcionamiento general, situación de seguridad y variantes | disparo autorizado o carga transfásica disponible |
| Sensores/tricorder | medición, error, resolución, interferencia y procedencia | composición, biología o identidad perfectas sin muestra |
| Comunicaciones | canales, cifrado, latencia y fallos | recepción inmediata a cualquier distancia |
| Transportadores | condiciones de bloqueo, patrón, riesgo y redundancia | transporte seguro sin estado ambiental y personal |
| Replicadores | disponibilidad, demanda de recursos, restricciones y replicación | materia, energía o equipamiento infinito |
| Ordenadores/PADD/IA | catálogo de conocimientos y contextualización autorizada | secretos, órdenes, detecciones o decisiones de Core |
| Equipos personales | categoría, entrenamiento, inventario y seguridad | dispositivo en manos del actor sin registro de entrega |

## Medicina: criterios de revisión y rechazo

- Separar `observable` (lectura con fuente/fecha), `hypothesis` (interpretación incierta), `diagnosis` (acto profesional), `treatment` (recurso/autoridad) y `outcome` (hecho persistente). Un tricorder no salta de observación a curación.
- Para humanos, vulcanos, klingon, cardassianos, bajoranos y ex-Borg, personalizar condiciones fisiológicas por individuo. Nunca extrapolar dosis humanas a especie no humana ni dar una cifra única de constantes sin fuente.
- Registro médico privado: no indexarlo como conocimiento general de una consola. La autorización de consulta no es universal ni irreversible.
- Cualquier posible capacidad terapéutica de la sangre del protagonista (PR #175 **abierta en el corte**) queda como **propuesta documental separada**: consentimiento, extracción supervisada, evidencia y resultado individual; no cura universal ni intervención forzada.
- Casos clínicos citados en el atlas son **ficción**, no instrucciones sanitarias reales.

## Ciencia: criterios de contrastación

Toda ficha sobre anomalía, singularidad, nebulosa o fenómeno subespacial debe poder devolver `observado`, `no observado`, `indeterminado`, `hipótesis competidoras`, `instrumental y límites`, `grado de confianza` y `próxima prueba admisible`. Datos antiguos pueden ser caducos. La investigación nunca muta por sí sola el fenómeno ni inventa entidades.

**Cierre del proceso 04/05 en esta operación:** especificada explotación/revisión transversal y criterios negativos; **auditoría manual per-record y fuentes externas de todos los 202+ registros no acreditada**, mantener deuda visible. Pruebas de importación CoreRPG y UE no ejecutadas.
