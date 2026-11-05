# F12 — Anexo de planificación futura: IDEA-0017 Vida personal, pareja y familia

**Fecha de análisis arquitectónico:** 2026-11-05.  
**Estado:** **RESERVA DE PLANIFICACIÓN / SIN IMPLEMENTAR**. No altera F12-P01…P05, la cifra de 80 pasos del Plan Maestro, el estado de F05 ni los cierres de fases.  
**Decisión autoral de producto:** [IDEA-0017 aprobada](../../../../../ideas/IDEA-0017_vida_personal_pareja_matrimonio_familia.md). La experiencia sentimental y familiar es **opcional para el jugador**, pero una capacidad **deseada para el producto**; no puede omitirse de la planificación por confundir ambas formas de «opcional».  
**Fase propietaria propuesta:** **F12 — Vida a bordo, NPC y relaciones**; programa funcional transversal **LIFE-01–LIFE-09**. No añadir F16 ni adelantarlo a F05.  
**Contexto creativo vigente:** **Proyecto Valhalla = Enterprise-D modernizada por Geordi La Forge**, no la antigua Enterprise-G/clase Valhalla. **Conflicto documental pendiente:** Plan Maestro, decisiones y F11 todavía contienen decisiones históricas de nueva clase Valhalla; la actualización de canon/cronología es una tarea separada del presente anexo y requiere conciliación formal con el autor. No se sobreescriben aquí fuentes históricas.

## 1. Resultado del análisis del árbol de Git

El árbol `main` consultado contenía **3.655 archivos versionados**. La arquitectura relevante ya está distribuida en varios directorios; deben **reutilizarse** sus contratos sin reescribirlos para inventar otro sistema social.

| Dominio | Archivo o directorio existente | Responsabilidad |
|---|---|---|
| Grafo de relaciones y romance | `sistemas/gameplay/social/relationship_graph_model.json`, `social_event_rules.json`, `adult_heterosexual_relationship_canon_v0.1.json` | Intimidad, citas, autonomía, compatibilidad autoral, límites y hechos causales; conservar canon bloqueado hasta decisión distinta |
| Parentesco estable | `sistemas/gameplay/relationships/kinship_family_network_contract.json` | Padres/hijos, hermanos, adopción, parentesco separado de afecto, hogar y tutela |
| Procedencia de vínculos | `sistemas/gameplay/relationships/relationship_change_provenance_contract.json` | Causa, fecha y visibilidad de cambios de relación, incluso fuera de escena |
| Biología y filiación | `sistemas/gameplay/species/reproduction_parentage_framework.json`, `species_biology_contract.json` | Reproducción por especie, embarazo si corresponde, filiación legal/social/biológica distinta |
| Crecimiento | `sistemas/gameplay/species/character_lifecycle_contract.json`, `sistemas/gameplay/characters/character_runtime_model.json` | Identidad única de un hijo y etapas de desarrollo sin regeneración |
| Hogar y capacidad | `sistemas/gameplay/ship_operations/shipboard_life_state_contract.json`, `shipboard_habitability_profile_contract_v0.1.json` | Camarotes, servicios, civiles, familia, capacidad y privacidad por nave |
| Vida cotidiana | `sistemas/gameplay/characters/activity_schedule_model.json`, `sistemas/gameplay/ship_operations/off_duty_activity_catalog_v0.1.json` | Guardias, sueño, tareas familiares, educación y tiempo libre |
| Persistencia | `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json` | Save/load y LOD sin cambiar identidad, parentescos ni historia |
| Representación social | `sistemas/gameplay/social/social_simulation_lod.json`, `sistemas/ai/memory/` | LOD A/B/C, recuerdos, intimidad contextual, carga de actores sólo cuando procede |

**Brecha verificada:** ningún contrato de parentesco, ciclo vital o ideas es por sí mismo un **sistema ejecutable completo de matrimonio, hogar, nacimientos y crianza**. La F12 posee **45 escenarios de referencia y replay offline de hasta 24 meses**, pero su propia acta confirma **CoreRPG, save/load en partida, UE5/MSI y simulación autoritativa de meses NO EJECUTADOS**.

## 2. Fronteras arquitectónicas

**CoreRPG (repositorio independiente):** proporcionar y, cuando la necesidad real lo justifique, ampliar primitivas **neutrales a cualquier universo**: `EntityId`, relaciones tipadas, acciones/eventos validados, reloj, conocimiento, identidad, historial, transacciones, persistencia, simulación fuera de cámara y recuperación. **No** introducir `StarfleetMarriage`, `GalaxyQuarters` ni reglas biológicas ficticias en el núcleo. El Core existente incluye primitivas de entidades, relaciones, timeline, historia, conocimiento y guardado; **no** asumir que ya ofrece un motor familiar rico. Cualquier nueva API se diseña/acepta por contrato propio y requiere pruebas sobre su SHA actual.

**Star Trek / Content Pack:** reglas de pareja, compromiso matrimonial, casa familiar, tutela, gestación cuando esté soportada, parentesco, responsabilidades, educación, servicios de nave, especies y consecuencias de traslado. Crear **un dominio coordinador propuesto `sistemas/gameplay/family/`**, sin duplicar `social/`, `relationships/`, `species/`, `characters/` ni `ship_operations/`.

**Host / UE5:** representar NPC adultos y menores con modelos adecuados, hogar/camarotes, actividades, conversaciones, ceremonias, rutinas, cámaras y sonidos. Los actores 3D no son la identidad persistente de esos personajes. El repositorio `juego/UE5/` permanece destino de integración, no fuente alternativa de verdades familiares.

**IA:** conversación, interpretación y narrativa personal sobre contexto autorizado. No puede **crear matrimonio, consentimiento, embarazo, nacimiento, parentesco o recuerdos sin resultado autoritativo**.

## 3. Ubicación propuesta para nuevos contratos de familia

```text
Videojuego_StarTrek/
├── proyecto/ideas/
│   └── IDEA-0017_vida_personal_pareja_matrimonio_familia.md   [EXISTE]
├── proyecto/docs/roadmap/master/fases/F12/
│   └── ANEXO_IDEA-0017_VIDA_PERSONAL_Y_FAMILIAR.md            [ESTE ANEXO]
├── sistemas/gameplay/
│   ├── social/         [EXISTE: relaciones, citas, consentimiento]
│   ├── relationships/  [EXISTE: parentesco, procedencia, estados]
│   ├── species/        [EXISTE: biología, filiación, ciclo vital]
│   ├── characters/     [EXISTE: identidad, edad y horarios]
│   ├── ship_operations/[EXISTE: hogar, capacidad, ocio]
│   └── family/         [PROPUESTA FUTURA: orquestación doméstica y familiar]
├── desarrollo/validation/fixtures/f12/family/  [PROPUESTA FUTURA]
├── desarrollo/tools/validation/                 [pruebas de contrato y regresión]
├── mundo/lore/starships/classes/shipboard_life/ [capacidad por nave]
└── juego/UE5/                                   [representación e interacción]
```

**Candidatos conceptuales dentro de `sistemas/gameplay/family/`** (no crearlos todavía, no son contratos existentes):
- `family_domain_contract.json`: invariantes y referencias a los contratos existentes.
- `partnership_union_state_contract.json`: acuerdos de pareja, convivencia/matrimonio, ceremonia/ruptura, independencia de romance y parentesco.
- `household_residency_contract.json`: miembros, asignaciones, capacidad, privacidad, visitas y cambios de nave.
- `parenting_guardianship_contract.json`: tutela, cuidados, obligaciones y decisiones legítimas sobre menores.
- `family_event_rules.json`: eventos causales de vida familiar ligados a reloj, lugar y personajes; **sin duplicar los eventos sociales generales**.

**No crear un segundo `relationship_graph` ni un sistema de embarazo alternativo:** deben reutilizarse los existentes. Los nombres anteriores son **sugerencias de planificación**, sujetos a auditoría/contrato real al llegar a F12.

## 4. Dependencias por fase

| Fase | Qué aporta o cuándo intervenir |
|---|---|
| **F03** | Base autoritativa de identidad, reloj, eventos, conocimiento y guardado: **ya cerrada a su corte definido**, no reabrir ahora para introducir todo el módulo familiar |
| **F04** | Dotación, autoridad, ocupación/capacidad de naves y contexto profesional: dependencia para civiles/familias y alojamiento real |
| **F05 (actual)** | Órdenes/delegaciones e **iniciativa NPC operativa limitada**. **NO implementar romance, matrimonio ni hijos en F05**. Reutilizar mecanismos genéricos después, sin asumir que la iniciativa de escaneo ya simula vida social |
| **F07** | Interacción/escenas UE5: preparar convenciones de acceso a camarotes e identidad, sin construir familia completa todavía |
| **F10** | Cadetes, relaciones sociales y recuerdos persistentes; antecedente sentimental opcional, sin forzar compromisos o familia en la Academia |
| **F11** | Carrera y traslados: relaciones a distancia, decisiones profesionales, vivienda y acompañantes sin trasladarlos automáticamente |
| **F12** | **PROPIETARIA del dominio completo**: vida sentimental opcional, relaciones informales, pareja, matrimonio, unidad doméstica, filiación, hijos, crianza, iniciativa social y persistencia |
| **F13** | Integración eventual con eventos emergentes y evolución del universo; nunca crear cambios familiares sin causa |
| **F14** | Actores por edades, hogares, ceremonias, audio, animaciones y UI/diálogos |
| **F15** | QA integrado UE5/MSI, continuidad de campañas largas, migraciones/guardado, límites de IA y pruebas de regresión |

**La IDEA-0017 es opcional para el personaje, no necesariamente prescindible para el producto.** Antes de cerrar F12, el equipo debe decidir formalmente qué alcance LIFE queda **obligatorio para la aceptación prevista** y qué subfuncionalidad se aplaza, con aprobación expresa del autor. No declarar LIFE implementado por haber cerrado F12-P01…P05 a nivel de referencia.

## 5. Correspondencia con pasos F12 ya existentes

- **F12-P01 — Identidad y relaciones:** LIFE-01 auditoría; LIFE-02 soltería, citas e intereses recíprocos; LIFE-04 contrato de matrimonio/pareja cuando toque.
- **F12-P02 — Tiempo y lugares:** LIFE-03 convivencia, residencia, turnos, intimidad y rutinas; LIFE-07 carrera/traslados/familia.
- **F12-P03 — Iniciativa social y privacidad:** LIFE-02/04 voluntades y compromisos; LIFE-05 decisiones de parentalidad y nacimiento autorizadas; LIFE-08 diálogo/memoria; NPC↔NPC y jugador↔NPC.
- **F12-P04 — Simulación LOD:** LIFE-06 hijos persistentes, desarrollo por edad/especie, tutela/escuela/actividades y representación visual parcial; familia sigue existiendo fuera de cámara.
- **F12-P05 — Continuidad y regresión:** LIFE-07/09 años de campaña, destinos distintos, reconciliaciones, separaciones, partos y crianza mediante guardados/recargas e historial causal.

La distribución LIFE **no cambia la numeración oficial de cinco pasos** ni obliga a desarrollar todas sus dependencias a la vez; el conjunto de **LIFE-01–LIFE-09** ya está propuesto y registrado en IDEA-0017.

## 6. Alcance jugable, privacidad y consentimiento

- El jugador puede seguir soltero, llevar una vida de **picaflor/mujeriego** con citas y relaciones consensuadas informales, consolidar pareja, convivir, casarse, decidir tener hijos o no tenerlos.
- No hay un «modo matrimonio» impuesto ni karma automático por ser soltero. Los NPC son autónomos y el interés romántico o la exclusividad se basan en hechos y decisiones.
- Toda mecánica romántica/sexual aplica **solo a adultos equivalentes** y respeta el canon autoral actualmente bloqueado `adult_heterosexual_relationship_canon_v0.1.json` sin reinterpretarlo.
- Embarazo y filiación solo se generan mediante hechos/eventos habilitados y particularidades biológicas/culturales documentadas; **no surgen automáticamente de convivir, casarse o intimar**.
- Un hijo tiene ID propio, origen legítimo y parentescos, edad/desarrollo, privacidad, actividades y ubicación. La simulación infantil no incluye ninguna mecánica romántica/sexual adulta.
- Distinguir **romance, matrimonio, parentesco, tutoría, convivencia, propiedad y afecto**: cada vínculo es independiente y con reglas/eventos propios.
- Las consecuencias laborales del rango y la relación sentimental no permiten coerción ni privilegios profesionales automáticos.

## 7. Riesgos y pruebas de aceptación propuestos

1. **Permisividad incorrecta:** que cohabitación/cita/matrimonio cree automáticamente embarazo, filiación, confianza o derechos de acceso. Probar casos negativos.
2. **NPC inexistente:** hijo o pareja generados por diálogo sin evento autoritativo; **prohibido**.
3. **Duplicados y continuidad:** nacimiento, ceremonia o adopción repetidos tras reintento/restore; bloquear idempotencia y preservar IDs.
4. **Escena vs. realidad:** compañero o hijo en dos lugares, o desaparece cuando su cubierta se descarga; probar LOD y autoridad.
5. **Edad/especie:** crecimiento humano aplicado por defecto a especies no humanas sin datos; abortar/informar como desconocido.
6. **Autonomía:** propuestas de IA que cambian por su cuenta compromiso, consentimiento, embarazo o matrimonio; rechazar.
7. **Carrera:** traslado entre Galaxy con familias y destino no habilitado para dependientes; familia no se teletransporta y se conservan relaciones.
8. **Campaña larga:** la F12 de referencia solo ensaya hasta 24 meses; para hijos/carrera exigir además **ensayos de 5, 10 y 20 años** y save/load entre años, con regresión de memoria, parentesco, crecimiento y ubicación.
9. **Casos de jugador sin familia:** toda la campaña principal debe funcionar sin pareja, hijos ni domicilio compartido.
10. **Prueba final MSI:** interacción real con un NPC adulto, encuentro, compromiso opcional, matrimonio y eventual hijo persistente en una partida de prueba representativa, sin necesidad de ejecutar todo el arco durante el tiempo físico de la prueba.

## 8. Decisiones pendientes para el inicio formal de F12

- Determinar qué entregas LIFE serán requisitos de cierre de F12 y cuáles se someterán a aceptación posterior.
- Reconciliar en el canon/plan actual la **Enterprise-D resucitada** frente a textos históricos que siguen afirmando clase Valhalla/Enterprise-G nueva.
- Definir contrato matrimonial y derechos de residencia/tutela según jurisdicción/culturas sin inventarlos.
- Elegir límites de granularidad para infancia/crianza (LOD y rendimiento), IA, modelos 3D por edades y rangos de años.
- Diseñar integración real C++/CoreRPG/Host/UE5 sin asumir APIs que hoy no estén implementadas.
- Consultar al autor cuando una decisión sobre matrimonio, descendencia, intimidad o trayectoria familiar afecte agencia del jugador o modifique canon previamente bloqueado.

**Reserva final:** IDEA-0017 queda **ubicada de forma visible en F12 como ampliación funcional planificada**, apoyada en F03/F04/F05/F10/F11 y F14/F15. **No se ha programado ningún sistema familiar ni adelantado el estado de F12 o de F05 por escribir esta nota.**
