# LORE-01 / A — Auditoría y propuesta de alcance: especies y culturas (TNG)

**Fecha de auditoría:** 2026-10-17  
**Estado:** AUDITED — PROPUESTA PENDIENTE DE VISTO BUENO  
**Rama:** `lore/01-tng-species-cultures`  
**Ámbito de esta etapa:** el siglo XXIV de *The Next Generation*, *Deep Space Nine*, *Voyager* y las películas TNG aceptadas.  
**No autoriza:** cambiar la política global de tres épocas, reescribir fichas existentes, introducir civilizaciones/territorios (B), astrogeografía (C), diplomacia (D) ni modificar CoreRPG o UE5.

## 1. Auditoría del contenido real de `main`

Base consultada: commit `9edfcde1a4ac58aa7a66f9bfbc1ac2aa7e62f953`.

### 1.1. Biología y generación de individuos existentes

- `sistemas/gameplay/species/profiles/`: **15 perfiles de especie** con identificadores estables: `aenar`, `andorian`, `bajoran`, `betazoid`, `cardassian`, `changeling`, `ferengi`, `human`, `jem_hadar`, `klingon`, `romulan`, `tellarite`, `trill`, `vorta`, `vulcan`.
- Existe un **decimosexto fichero**: `borg_assimilated_character_v0.1.json`, correctamente modelado como **estado de personaje asimilado, no especie Borg**. No se debe contabilizar como especie nueva.
- Los modelos `sistemas/gameplay/species/species_runtime_model.json`, `species_biology_contract.json`, `culture_socialization_contract.json`, `character_lifecycle_contract.json`, `reproduction_parentage_framework.json` ya separan rasgos biológicos, cultura, ciudadanía, estados individuales, edad y parentesco.
- Hay agregados/resúmenes en `sistemas/gameplay/species/founding_species_profiles.json`, `major_species_profiles.json` y `dominion_borg_profiles.json`: **no son fichas pendientes de duplicar**.
- Generación procedural ya definida en `sistemas/universe/generation/procedural_sapient_species_morphology_biology_v0.1.json`, `procedural_population_rules.json` y `procedural_civilization_language_naming_generation_v0.1.json`.

### 1.2. Culturas, lenguas y fuentes existentes

- `mundo/lore/cultures/profiles/`: **12 perfiles culturales** (humanidad/Federación, vulcanos, andorianos/Aenar, tellaritas, klingon, romulanos, cardassianos, bajoranos, ferengi, trill, betazoides, y jerarquía cultural del Dominio).
- `mundo/lore/cultures/cultural_profile_contract_v0.1.json`: contrato ya establecido. Los resúmenes de interacción NO sustituyen los perfiles de profundidad.
- `sistemas/gameplay/languages/initial_language_catalogue.json`: **5 entradas** (`klingonese`, `romulan`, `bajoran`, `ferengi`, `trill`); la lógica de traducción y competencia lingüística es más amplia que el catálogo.
- `mundo/sources/source_registry/source_registry.json`: **294 fuentes registradas** en el momento de la auditoría. La presencia de un ID no equivale a que cada afirmación de una ficha esté respaldada por un episodio concreto.
- `mundo/sources/canon_policy.md` y `mundo/sources/provenance_policy.md` establecen jerarquía de fuentes y confianza; `CONTENT_STATUS.md` mantiene especies/culturas/lenguas como `IN_PROGRESS`.
- `proyecto/docs/roadmap/procedural_layers_master_plan_v0.1.md` fija las capas 031–042 para biología, culturas y lenguas. **Capas diseñadas ≠ catálogo de especies completado ≠ integración con CoreRPG**.

### 1.3. Carencias verificadas

1. **Cobertura**: no existen fichas individuales en `sistemas/gameplay/species/profiles/` para especies recurrentes de TNG/DS9/VOY como bolianos, benzitas, el-aurianos, breen, pakled, kazon, ocampas, talaxianos, vidianos e hirogen.
2. **Profundidad desigual**: varios perfiles existentes tienen límites fisiológicos, longevidad, reproducción, costumbres concretas, dialectos o medicina como `unknown`; esto es **preferible a inventar datos**.
3. **Procedencia de afirmaciones**: algunos perfiles descansan especialmente en fuentes secundarias; p. ej. `betazoid_v0.1.json` solo cita `MA_BETAZOID` en su `provenance`. Se necesitan, donde sean relevantes, referencias trazables a episodios retenidos.
4. **Fuente fuera de selección**: `andorian`, `aenar` y `tellarite` (además de sus agregados) contienen referencias `ENT_*`, algunas registradas como `SCREEN_CANON`. La política del proyecto excluye *Enterprise* del **corpus televisivo retenido**; revisar estas citas y distinguir antecedente contextual de prueba dentro del canon seleccionado **sin borrar información ni cambiar políticas por cuenta propia**.
5. **Validez temporal**: los perfiles culturales suelen tener notas genéricas de variación por época, pero falta un índice consumible por fechas/eventos para evitar trasladar automáticamente hechos posteriores a una campaña anterior.
6. **Catálogo lingüístico estrecho**: solo cinco lenguas listadas; no inferir que todos los miembros de una especie hablan una lengua ni que traductor universal significa traducción infalible.
7. **Indexación**: el contenido vive en varios directorios correctos; falta una **tabla de cobertura** que una fichas biológicas, perfiles culturales, idiomas, fuentes y restricciones, sin crear un segundo repositorio de la verdad.

### 1.4. Precauciones que no deben convertirse en errores

- `changeling`, `vorta` y `jem_hadar` son especies diferentes; **Dominio es una organización**, que se desarrollará en B.
- `borg_assimilated_character` es transformación/estado; no genera una especie origen `borg`.
- `aenar` tiene un perfil diferenciado ya aprobado: no fusionarlo sin decisión expresa con `andorian`.
- `trill` unido/no unido se conserva como diferencia de estado, no como dos especies.
- Una cultura puede tener varias especies asociadas y un personaje varias culturas; ninguna se asigna automáticamente por especie.
- No aplicar estereotipos de personalidad ni bonificaciones raciales planas.
- No trasladar Kazon/Hirogen/Ocampa etc. al espacio federado solo por completar población: aparición siempre condicionada a localización, fecha, contactos y hechos de campaña; detalles espaciales corresponden a C.
- No inventar cifras exactas de longevidad, generaciones, idiomas, poblaciones, localizaciones o rasgos médicos para llenar huecos.

## 2. Alcance propuesto (NO APROBADO todavía)

### Mantener y auditar profundamente lo ya existente (15 especies + estado Borg)

Reutilizar las quince fichas, sus resúmenes y los doce perfiles culturales. Completar únicamente los campos ausentes que **tengan fuente y efecto jugable**, sin cambios incompatibles ni duplicaciones.

### Primera ampliación propuesta: 10 especies TNG/DS9/VOY

**Alpha/Beta y vida cotidiana:**
- `bolian` — tripulación y población civil federada.
- `benzite` — tripulación y diferencias ambientales/culturales documentadas.
- `el_aurian` — individuos longevos, diáspora y memoria/historia personal, **sin convertir a todos en Guinan**.
- `breen` — presencia y límites de conocimiento, particularmente hacia 2375; **biología desconocida debe permanecer desconocida**.
- `pakled` — contactos y encuentros, sin reducir a la especie a un rasgo cognitivo obligatorio.

**Voyager/Delta; presencia restringida por contexto:**
- `kazon`
- `ocampan`
- `talaxian`
- `vidiian`
- `hirogen`

Estos nombres constituyen una **lista candidata**, no un permiso para importar fronteras, conductas, sistemas políticos ni datos biológicos inciertos como canon. Se podrán incorporar otros (p. ej. nausicaanos, karemma, especies de espacio fluídico) en una ampliación posterior si una misión lo necesita; el índice no presupone exhaustividad. El número 10 es una propuesta de primera oleada, no un límite fijo del universo.

### Marco temporal

Cobertura de partida del periodo narrativo **2364–2378**, con hechos sujetos a la **fecha concreta de inicio de cada campaña** y a su historia emergente. La fecha de un episodio no convierte automáticamente sus acontecimientos en hechos ocurridos en una campaña divergente.

## 3. Paquetes secuenciales propuestos para completar SOLO A

| Paquete | Entregable | Comprobación |
|---|---|---|
| **A00 — Auditoría** | Este documento, inventario de archivos y riesgos | Auditoría basada en `main`, sin duplicación |
| **A01 — Índice transversal** | Índice con IDs existentes, ruta autoritativa, enlaces a culturas/lenguas, fecha, fuente y estado de cobertura | Cada ruta existe; ningún ID repetido; Borg es estado |
| **A02 — Consolidación base** | Revisión dirigida de las 15 fichas existentes y 12 culturas; evidencia de TNG/DS9/VOY, `unknown` y problemas `ENT_*` | Afirmaciones sensibles trazables, sin borrar hechos aprobados |
| **A03 — Ampliación Alpha/Beta** | Cinco fichas biológicas y cultura asociada solo donde exista base suficiente | Especies, cultura, ciudadanía y profesión separados |
| **A04 — Ampliación Voyager** | Cinco fichas y vínculos, restringidas geográfica y temporalmente según evidencia | No generan presencia aleatoria injustificada |
| **A05 — Lenguas y validación** | Ampliación prudente del catálogo, glosario de términos, referencias cruzadas y pruebas JSON | Referencias, procedencia, duplicidad, campos y fechas validados |

**Orden:** A00/A01 → A02 → A03 → A04 → A05. Un paquete no habilita B automáticamente; la aprobación del autor será del **apartado A completo** tras informe y revisión.

## 4. Responsabilidades y ubicación: sin reorganización masiva

- `sistemas/gameplay/species/profiles/`: biología jugable y restricciones de individuo (fuente actual).
- `mundo/lore/cultures/profiles/`: cultura profunda y variación, sin adjudicación forzada.
- `sistemas/gameplay/languages/`: lenguas y estados de traducción.
- `mundo/lore/species/`: índice documental de cobertura y referencias; no copiar los perfiles de `sistemas/gameplay/species/profiles/`.
- `mundo/sources/source_registry/`: ID de fuentes de nuevos hechos; conflictos sin resolver van a `mundo/sources/unresolved_conflicts/`.
- `proyecto/docs/roadmap/`: auditoría, alcance, decisiones pendientes y progreso.
- `desarrollo/tools/validation/`: pruebas de catálogo, referencias y compatibilidad **documental** con contratos existentes.
- `CONTENT_STATUS.md`: actualizar al cierre de A, preservando significado de estados globales.

## 5. Criterios concretos de salida del apartado A

1. Los **15 perfiles de especies existentes** y la transformación Borg conservan sus identidades y referencias, con revisiones justificadas y sin regresiones.
2. Las **10 nuevas especies propuestas**, una vez aprobadas, tienen ficha utilizable o una exclusión explícita motivada, no un documento vacío disfrazado de COMPLETE.
3. Los **12 perfiles culturales existentes** están enlazados; culturas nuevas solo cuando existen fuentes. El modelo permite variación personal, social y multicultural.
4. Identificadores únicos y estables; fuentes y confianza verificables; biología no determinada no se rellena con conjeturas.
5. Fichas con vigencia temporal y límites de generación suficientemente claros para la **fecha de campaña**, sin promesas de coordenadas.
6. Los idiomas relevantes están enlazados a sus perfiles y al traductor, sin determinar ciudadanía ni cultura automáticamente.
7. Pruebas reproducibles revisan sintaxis JSON, rutas locales, IDs de fuente, fechas cuando existan, compatibilidad con los contratos ya vigentes y coherencia de reglas.
8. Documentación clara en castellano para la computadora y autores; datos estructurados orientados a consumidores, **sin fingir que CoreRPG ya los carga**.
9. PR revisada y fusionada por Roberto; verificación de `main`; rama borrable solo tras revisión. **No iniciar B antes de ese punto.**

## 6. Decisiones requeridas al propietario antes de implementar A02–A05

- Aceptar o ajustar la **primera oleada de 10 especies** y la cobertura TNG/DS9/VOY 2364–2378.
- Ratificar cómo se usarán las referencias de `Enterprise` ya presentes: fuente externa contextual (no `SCREEN_CANON` dentro de las obras retenidas), conservar datos provisionalmente como `NEEDS_REVIEW`, o mantener expresamente esas referencias como excepción de canon. **No se altera la política global sin autorización**.

## 7. Límites de esta entrega

Esta auditoría solo acredita estructura, contratos, fuentes declaradas y ausencias observadas en el repositorio. No certifica aún cada afirmación contra el fotograma/diálogo original ni valida integración runtime. La validación exhaustiva se hará por paquetes; el presente documento es `AUDITED`, **no `COMPLETE` de LORE-01**.
