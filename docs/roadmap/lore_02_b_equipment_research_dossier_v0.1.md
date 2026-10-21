# LORE-02 B — Investigación técnica, diseño de uso y frontera de integración

**Corte:** 21-10-2026 · **Estado:** NEEDS_REVIEW · **Modo:** investigación documental / datos de autoría, NO runtime.  
**Base verificada:** `Videojuego_StarTrek/main` = `d1ee2af3c395d3216072afc37edfaf48021e1874` (PR #31, LORE-02 A fusionada); `CoreRPG/main` documentado con 4.13, content contract 0.1.0, acciones y persistencia.  
**Criterio de autoridad:** verdad y mutaciones exclusivamente CoreRPG; reglas específicas en capa Star Trek/Host; representación/interacción en UE5.

## 1. Corpus y trazabilidad

- Catálogo único: [73 equipos, familias y variantes](../../lore/equipment/lore02_b_equipment_catalogue_v0.1.json). Las familias son **ciencia (12), seguridad (9), medicina (9), ingeniería (10), entorno (10), comunicaciones (7), otros operadores (16)**.
- [15 perfiles de dotación + 6 plantillas de misión](../../lore/equipment/lore02_b_roles_loadouts_v0.1.json), orientativos y NO distribución física de stock.
- [45 casos adversariales](../../lore/equipment/lore02_b_adversarial_scenarios_v0.1.json), observaciones frente a resultados prohibidos.
- **15 fuentes incorporadas** a `sources/source_registry/source_registry.json`, con fuentes oficiales de StarTrek.com y secundarias especializadas de Memory Alpha. Evidencias de equipos TNG / VOY procedentes de anuncios de réplicas autorizadas **sirven para existencia, aspecto y denominación, pero NO para especificaciones de juego ni desempeño técnico**.
- Las fichas `GAME_ADDITION` describen **herramientas, kits, pasos de operación o control diseñados para el videojuego**; su existencia canónica, tecnología real o apariencia no se afirma. Las fichas `SOURCE_BOUNDED_INFERENCE` se apoyan en anclas de equipo/familia, pero **los bucles, guardias, recursos y fallos son reglas propuestas y revisables**.
- Política de fuentes: [canon_policy](../../sources/canon_policy.md), [provenance_policy](../../sources/provenance_policy.md). Todas las afirmaciones numéricas operativas (potencia, autonomía, alcance, dosis, recarga, resistencia, tamaños) quedan sin definir cuando no hay evidencia por dispositivo y época. El juego podrá definir parámetros propios en gameplay, etiquetados.

## 2. Tricorders y ciencia

**Evidencia:** `L02B_MA_TRICORDER`, `L02B_ST_TNG_PROPS`, `L02B_ST_VOY_PROPS`. Se documentan generaciones distintas de tricorder y utilización de scanners médicos. Una familia de instrumento no equivale a un sensor omnipotente.

**Bucle previsto:** autorización/selección de dispositivo → comprobación de energía/calibración/entorno → elección pasivo/activo/muestreo → observaciones de mundo disponibles al sensor → estimación con confianza, procedencia, lagunas y anomalías → registro y transferencia si hay enlace → hipótesis analítica derivada de conocimiento real del personaje. La pantalla no puede consultar datos secretos de CoreRPG que no habrían sido detectados.

**Variantes y límites:** perfil geológico, biológico o atmosférico sólo si modelo/módulo realmente asignado. Tricorder del siglo XXIII, TNG y Voyager no se intercambian automáticamente. Una nave con sensores potentes no convierte su tricorder en equipo infinito. Sondas y balizas tienen identidad, energía, recuperación o gasto. Muestras necesitan origen, identificador, contaminación y custodia. Distinguir muestra científica de muestra clínica: esta última enlaza a LORE-02 C.

**Fallos:** perturbación electromagnética, lecturas fuera de rango, saturación, falsos positivos, calibración caducada, datos almacenados sin enlace; los valores y porcentajes futuros son calibración del simulador, no canon.

## 3. Seguridad, armamento y custodia

**Evidencia:** `L02B_MA_PHASER`, `L02B_ST_TNG_PROPS`, `L02B_ST_VOY_PROPS`. Se diferencian tipos I, II y III, rifles de variantes concretas, y accesorios de dotación. La clasificación tipo I/II/III no supone idéntica interfaz, efecto o reserva energética en todas las épocas ni entre fabricantes.

**Bucle previsto:** arma asignada y custodiada → reglas de fuerza y orden válida → condición, seguro, energía, ajuste permitido y blanco confirmado → verificación contextual (civiles, atmósfera, seguridad interior, eventual desescalada) → petición de acción al Host → resolución CoreRPG → efecto observable en UE5, consumos, daños y registro sólo si se implementan las reglas específicas. Ni llevar un fáser ni que la computadora interprete «dispara» concede permisos.

**Ajustes:** aturdimiento/efectos mayores se representan conceptualmente, pero NO se fijan cifras, niveles universales ni un modo que siempre incapacite. Uso técnico excepcional para corte o liberación requiere evaluación específica. Guardas evitan que el simple activo visual resuelva una detención, un daño o la integridad de la nave.

**Protección/contención:** restricciones de custodia, campos portátiles y sellos se etiquetan como propuestas donde no hay ancla audiovisual suficiente; un campo depende de energía y configuración, la custodia de decisiones legítimas y trazabilidad, y una protección adaptativa Borg de estado real y hechos observados.

## 4. Medicina y emergencias

**Evidencia:** `L02B_MA_MED_TRICORDER`, `L02B_ST_MED_PROPS`, `L02B_ST_HYPO`, `L02B_MA_HYPO`, `L02B_MA_MEDKIT`. Tricorder médico y sensor de mano pueden complementarse, no siempre son un único dispositivo. Hipospray es instrumento de administración; el cartucho y la medicación son elementos distintos, limitados y trazables.

**Bucle previsto:** identificación del paciente / especie conocida y estado de privacidad → evaluación preliminar → hipótesis con incertidumbre → autorización clínica y valoración de incompatibilidades → uso de material realmente disponible → solicitud de cambio de estado por el Host al Core → observación, historial y seguimiento. Un botón no cura por sí mismo; sin conocimiento o recursos el resultado es incompleto o actuación limitada.

**Separación con LORE-02 C:** aquí se documentan dispositivo, conexión, permisos, consumible y fallo; NO tratamiento, diagnóstico específico, pronóstico, dosis ni interacciones farmacológicas reales. Se exige compatibilidad biológica y prudencia ante anatomías no humanas. El comunicador puede solicitar ayuda, pero no garantiza enlace ni transporte.

**Fallos:** cartucho equivocado/agotado, falsa lectura, sensor contaminado, suministro insuficiente, especie desconocida, aislamiento ineficaz, plan de evacuación no disponible.

## 5. Ingeniería, mantenimiento y reparación

**Contratos:** `gameplay/engineering/engineering_loop.json`, `gameplay/logistics/repair_requirement_model.json`, `gameplay/logistics/maintenance_state_model.json`.

**Bucle previsto:** síntoma → diagnóstico local / de consola → confirmar seguridad y aislamiento → calificar trabajo como a bordo, campo o instalación → comprobar personal, permisos, pieza, energía y tiempo → parche temporal o reparación adecuada → prueba y registro. El tricorder de Ingeniería observa, el adaptador accede sólo a sistemas compatibles y el kit **no contiene automáticamente** todas las piezas.

**Fallos:** acoplador incompatible; corte en sistema activo; sensor no calibrado; cambio de chip sin protocolo compatible; reparación provisional confundida con definitiva; material reservado en misión simultánea. Una reparación de campo no sustituye un dique seco sin justificación. Las herramientas de taller genéricas se marcan como diseño del juego, no props canónicas especificadas.

## 6. EVA, protección ambiental y rescate

**Evidencia:** `L02B_MA_EV_SUIT` permite identificar trajes por época, casco, reserva ambiental y elementos de anclaje/maniobra. Ninguna autonomía, auto-sellado o protección se universaliza entre trajes. La fisiología del usuario y el lugar importan.

**Bucle previsto:** evaluar peligro y atmósfera → asignar traje compatible y entrenar → revisar cierre, componentes, reserva, comunicación, ruta y medio de recuperación → operación EVA con control de riesgos → retorno, descontaminación, mantenimiento y reposición. Botas magnéticas no agarran todos los materiales; una máscara filtrante no mantiene vida en vacío; un propulsor exige trayectoria y formación.

**Fallos:** fuga, batería sin reserva, separarse del casco, pérdida de radio, anclaje roto, visibilidad reducida, exposición no cubierta. Rescate y supervivencia requieren medios y decisiones causales, nunca «equipar traje» como inmunidad general.

## 7. Comunicaciones, PADD y acceso

**Evidencia:** `L02B_MA_COMMS`, `L02B_ST_MED_EMERGENCY`, `L02B_ST_TNG_PROPS`. Comunicador de mano en TOS y distintivo en TNG/VOY; PADD para registro/acceso. Distinguir la existencia física de un dispositivo, el derecho de abrir un expediente y la conectividad operativa.

**Bucle previsto:** selección de identidad y destino → cifrado/acceso cuando exista → viabilidad de enlace / retransmisión / traducción → transmisión y recepción limitada a paquetes efectivamente entregados → informe disponible para personajes autorizados. El comunicador NO es un transportador, ni PADD universal. El conocimiento local puede estar desactualizado.

**Fallos:** corte de enlace, interferencias, receptor caído, suplantación, datos caducados, error de interpretación, idioma sin base, fichero potencialmente manipulado. La IA recibe sólo hechos que el contexto autorice.

## 8. Otras civilizaciones: tecnología y cultura sin estereotipos

- **Klingon:** disruptores, bat'leth y d'k tahg según personaje, tradición y unidad. Ni todo klingon es militar ni portar un arma implica agresión. Algunos sensores de campaña figuran sólo como propuesta.
- **Romulano:** disruptor registrado como familia; acceso, espionaje y terminales especializados son específicos de organización/modelo. No asumir que todo civil pertenece a inteligencia.
- **Cardassiano:** armamento de mano/largo y terminales de campo por órgano y época. Sus interfaces y municiones no tienen compatibilidad automática con Flota.
- **Borg:** interfaz de dron, nanoprobes y protección adaptativa dependen de colectivo, dron y estado. Ni asimilación ni inmunidad automáticas como propiedad de etiqueta.
- **Bajorano:** rifle de la milicia diferenciado de rifles de Flota, incluidos posibles problemas de alimentación o autorización.
- **Vulcano / Ferengi:** dispositivos individuales y comerciales posibles; no garantizar posesión, habilidad, legalidad ni superioridad por especie.

**Fuentes:** `MA_KLINGON`, `MA_ROMULAN`, `MA_CARDASSIAN`, `MA_BORG_DRONE`, `L02B_MA_BORG_NANOPROBE`, `L02B_MA_BAJORAN_RIFLE`, `L02B_MA_PHASER`. Verificar especificaciones y episodio individual al convertir una propuesta en dato canónico fuerte.

## 9. Academia, NPC, asignación y persistencia

- Los perfiles de formación muestran ejercicios en simulador sin regalar físicamente el objeto al cadete. Un resultado académico puede aportar evidencia de formación **si una regla de carrera aprobada lo reconoce**, sin modificar directamente `capability_state_model`.
- La **misión determina dotación condicional**, no cada especie o rango. Al prestar un tricorder, cambiar de nave o recuperar un PADD, el objeto no se duplica; continúa con `object_id` estable. Stock fungible (cartuchos, filtros, parches) puede estar agregado hasta convertirse en un objeto persistente concreto.
- El estado del equipamiento (cargado, roto, custodiado, reservado, calibrado) **nunca va en la definición estática** y debe reconstruirse por persistencia CoreRPG cuando exista adaptador.
- Escaneo, reporte o mensaje afecta a la información del personaje **solo tras la acción de dominio resuelta**. La IA narrativa no otorga permisos, tratamiento ni curaciones. La computadora puede **proponer** comandos, no ejecutar mutaciones por texto.

## 10. Compatibilidades, fronteras y pendientes técnicos

| Dominio | Contrato existente | Responsabilidad futura (NO implementada aquí) |
|---|---|---|
| Identidad física | `gameplay/inventory/persistent_unique_object_contract.json` | Instancias, dueño, localización e historial en CoreRPG |
| Almacenes/consumo | `gameplay/logistics/resource_inventory_state.json` | Altas, reservas, gasto y reposición validados por Host |
| Acción técnica | `gameplay/engineering/engineering_loop.json` | Reglas de reparación Trek y estado persistido |
| Sensores | `gameplay/science/sensor_analysis_model.json` | Resolver sensor local con conocimiento parcial sin omnisciencia |
| Clínica | `gameplay/medical/medical_state_model.json` | Reglas LORE-02 C y seguimiento real |
| Acceso/comunicaciones | `gameplay/communications/communications_model.json` | Autenticar, entregar información y registrar transmisiones |
| Carrera | `gameplay/characters/character_runtime_model.json` | Calificación y asignación real, no por simple lore |
| Época | `gameplay/ship_operations/era_technology_matrix.json` | Consultar compatibilidad contextual sin convertir matriz de naves en inventario portátil |
| Simulación | CoreRPG 4.10–4.13 | Adaptador de acciones Trek, checks de Host, contenido JSON 0.1.0 de Core, interfaz UE5 |

**Deudas explícitas no bloqueantes de autoría:** política cuantitativa de carga/energía, combate y resultados de potencia, modelos 3D y monturas, prototipo interactivo de tricorder, tareas médicas de LORE-02 C, parámetros de reparación real, catálogo de equipamiento individual por nave y estación, localización de animaciones, reglas concretas de aprovisionamiento, adaptación oficial de estos datos a un Content Pack CoreRPG.

## 11. Cierre y aceptación

La documentación se acepta sólo si la CI comprueba unicidad y contabilidad de registros/casos, integridad de fuentes, familias cubiertas, referencias existentes de consumidores y anclas, distinción explícita de lore/gameplay/runtime, ausencia de precisión numérica inventada, separación de Core y límites clínicos, coherencia perfiles/casos y regresión con LORE-02 A y LORE-01.  
**Este informe no acredita** inventario ejecutable, que una captura de pantalla sea canon del parámetro, integración o juego probado en UE5, ni simulación real de casos adversariales.

**Pendiente de autor:** revisión/fusión de PR de B. Antes de aprobar cambiar `NEEDS_REVIEW` a `COMPLETE` sólo después de comprobar `main`, exactamente como se regularizó LORE-02 A.
