# F04 — Escenario ilustrativo Miranda-120: guardias de 3×8 / 4×6 con francos 5+2

**Fecha de registro:** 2026-10-13.  
**Clasificación:** `TEST_CASE_ILLUSTRATIVE`, aprobado como **ejemplo para evaluar la lógica**, **no** plantilla canónica, canon fijo, dotación obligatoria de Miranda ni régimen laboral universal de la Flota.  
**Alcance:** cobertura semanal teórica de seis puestos permanentes con descansos ordinarios. **NO demuestra** dotación completa en emergencias, vacaciones, sustituciones por enfermedad, cronología oficial o Core/UE5 ejecutables.

## Supuestos de esta Miranda ficticia

- **120 oficiales y especialistas reales** asignados al manifiesto de una Miranda de patrulla/exploración. El catálogo de clase no fija una única tripulación universal; cifra elegida **solo para este ejercicio**.
- **Seis puestos mínimos** cubiertos continuamente en navegación normal: oficial de guardia puente, timón/navegación, Sensores, Operaciones/comunicaciones, Ingeniería de guardia y Seguridad/táctica.
- No se presuponen dos NPC con la misma identidad, ni se suman por segunda vez oficiales de guardia al grupo administrativo.
- **Sanidad:** los nueve efectivos asignados sirven de base para atención y localización, pero **no** queda validada una cobertura clínica de emergencia 24/7 por este cálculo de seis puestos. Otros servicios, patrullas, mantenimiento, hangares, ciencia y mando requieren su propio detalle de horarios.
- **Cinco días de actividad programada + dos francos** por persona, escalonados entre equipos. Algunos de los cinco días son labores de apoyo, no ocupación de consola. El descanso **fuera de guardia** (sueño, ocio, comidas, etc.) y los francos completos son conceptos diferentes. Vacaciones y permisos prolongados no están incluidos en la demostración.
- Rotación de francos por parejas **desfasada** para que nadie tenga simultáneamente libres los mismos dos días que su único compañero, con un desplazamiento `(station_index * watch_count + watch_index) % 7`; esto solo verifica **una semana**, no equidad multisemanal.

## Comparativa del equipo esencial

| Dato | Tres guardias de 8 horas | Cuatro guardias de 6 horas |
| --- | ---: | ---: |
| Alpha | 08:00–16:00 | 06:00–12:00 |
| Beta | 16:00–00:00 | 12:00–18:00 |
| Gamma | 00:00–08:00 | 18:00–00:00 |
| Delta | — | 00:00–06:00 |
| Estaciones 24/7 | 6 | 6 |
| Plazas funcionales por día (franjas × estaciones) | 18 | 24 |
| Personas por plaza/franja | 2 | 2 |
| Personas del grupo de cobertura continua | **36** | **48** |
| Jornada nominal (5 días × duración) | 40 h/semana | 30 h/semana |
| Horas de ocupación de consolas por semana | **1008** | **1008** |
| Horas semanales nominales disponibles en grupo | **1440** | **1440** |
| Horas nominales sobrantes después de cubrir consola | **432** | **432** |

**Ojo con las 432 h:** no equivalen automáticamente a mano de obra libre. Deben reservarse para relevos, formación, coordinación, tareas auxiliares, descansos y limitaciones personales. La disponibilidad efectiva se calcula con Core y la agenda individual.

### Dotación de 120 sin doble conteo

| Grupo | Tres guardias | Cuatro guardias |
| --- | ---: | ---: |
| Guardias esenciales y sus relevos (incluye los 6 puestos) | 36 | 48 |
| Ingeniería, reparaciones y mantenimiento adicional | 19 | 15 |
| Seguridad/patrullas/respuesta adicional | 15 | 11 |
| Ciencia, laboratorios e investigación | 13 | 11 |
| Sanidad | 9 | 9 |
| Hangares, transporte, intendencia y suministros | 11 | 10 |
| Mando, administración y planificación | 8 | 8 |
| Servicios, bienestar y formación | 9 | 8 |
| **Total sin civiles/pasajeros** | **120** | **120** |

Es un **reparto propuesto**, no el manifiesto oficial de la clase ni garantía de que todos los servicios puedan afrontar vacaciones simultáneas. Al pasar de 3 a 4 guardias, se trasladan 12 personas desde actividades adicionales hacia las franjas esenciales.

## Demostración del ciclo 5+2 por puesto y franja

Se toma cada combinación de `puesto + guardia` y se asignan dos personajes distintos (A/B), con descansos no coincidentes. Ejemplo sin desfase, días lunes–domingo:

| Personaje | L | M | X | J | V | S | D |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Servicio/apoyo | Servicio/apoyo | Servicio/apoyo | Servicio/apoyo | Servicio/apoyo | **Franco** | **Franco** |
| B | Servicio/apoyo | Servicio/apoyo | **Franco** | **Franco** | Servicio/apoyo | Servicio/apoyo | Servicio/apoyo |
| Puesto | Cubierto | Cubierto | Cubierto | Cubierto | Cubierto | Cubierto | Cubierto |

Cada uno tiene **exactamente cinco días con actividad programada y dos días francos**; cuando están ambos de servicio, uno ocupa la consola y el otro puede estar en apoyo o relevo, sin ocupar dos puestos incompatibles. Las demás parejas se desplazan para repartir francos y carga.

El validador comprueba que se cubren **7 × 24 × 6 = 1008 horas-puesto** por semana, sin huecos ni doble ocupación; comprueba las 36/48 identidades de cobertura y las 120 personas del reparto de departamentos. También demuestra un negativo: **si falta uno de los dos durante toda la semana, aparecen huecos**. El motor futuro no puede cubrirlos creando un NPC artificial.

## Lo que queda expresamente pendiente

1. Planificar cobertura sanitaria real, personal de reserva y vacaciones, bajas simultáneas, sanciones, permutas, entrenamientos obligatorios, descansos entre jornadas, latencia de desplazamiento y solapamientos de relevo (orientación F04: **10–20 min** rutinario, **15–30 min** complejo).
2. Comprobar los cambios de modelo con descansos biológicos por especie, fatiga y equidad en periodos de varias semanas, no solo una.
3. Validar la cobertura frente a alertas/averías, bajas de combate, puestos adicionales y misiones de distinta naturaleza.
4. Integrar identidad/ocupación, cambio de guardia, nombramientos, eventos, sanciones, save/load y el cuadrante real con Core RPG; después mostrar las consecuencias en UE5.
5. Obtener autorización del capitán para 3×8, 4×6 o personalizadas; no imponer este `5+2` a todas las naves.

**Fuentes normativas vigentes:** `gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json`, `duty_assignment_model.json`, `activity_schedule_model.json`; [F04-P02](GUARDIAS_AGENDAS_P02.md) y [F04-P05](VALIDACION_Y_TRASPASO_P05.md).

**Archivos de QA de esta muestra:** `validation/fixtures/f04/miranda_120_watch_5x2_example_v0.1.json`, `tools/validation/test_f04_miranda_example.py`. La CI de esta PR valida **únicamente la consistencia aritmética de la muestra**, no sube la madurez ni cierra puertas de F04.
