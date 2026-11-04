# IDEA-0017 — Sistema integral de vida personal, sentimental y familiar

**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de aprobación expresa:** 4 de noviembre de 2026  
**Estado:** **APROBADA CONCEPTUALMENTE; diseño documentado, implementación y pruebas pendientes.**  
**Decisión del autor:** crear un sistema opcional de vida personal que incluya soltería, vida de soltero **picaflor y mujeriego**, citas y relaciones informales, pareja estable, convivencia, matrimonio, posibilidad de tener hijos y crianza; no obligar al jugador a seguir ninguno de estos caminos.
**Contexto naval vigente:** **Proyecto Valhalla = USS Enterprise NCC-1701-D clase Galaxy restaurada y modernizada por Geordi La Forge**, «la Gran Dama de la Flota Estelar», con identidad, casco e inscripciones Enterprise-D; **no hay Enterprise-G ni clase Valhalla jugable**. La distribución exacta, alojamientos y servicios se decidirán según la versión real de la Enterprise-D restaurada.  
**Principio:** relaciones y acontecimientos de familia son parte del World State persistente; IA dialoga, pero no inventa nacimientos, matrimonios, consentimiento ni efectos autoritativos.

## 1. La vida que el jugador elige vivir

El jugador puede comenzar en la Academia y desarrollar una carrera Starfleet, pero también vivir su **propia vida personal en paralelo**. El juego no debe imponer una pareja ni un arco de boda o paternidad.

Posibilidades igualmente válidas:
- Permanecer soltero siempre.
- Disfrutar de una vida de **soltero ligón, picaflor y mujeriego**, conocer mujeres adultas, flirtear, tener encuentros y citas consentidos, relaciones ocasionales o recurrentes sin compromiso.
- Acordar relaciones **informales no exclusivas** con términos conocidos por las personas implicadas.
- Mantener una **relación estable**, con o sin convivencia.
- **Casarse** mediante una decisión recíproca y una ceremonia real del mundo.
- **Tener hijos** si se cumplen las condiciones de la historia, decisiones compartidas y las reglas de especie, o plantear otras formas de formar familia en extensiones futuras.
- Afrontar conflictos, ruptura, reconciliación o distancia profesional.
- Cambiar de deseos y estilo de vida con el tiempo; nada de menú fijo «modo ligón» frente a «modo marido».

**No existe una cadena obligatoria** citas → noviazgo → matrimonio → hijos. Cada relación requiere hechos y decisiones propios y cada NPC es una persona autónoma.

## 2. Reutilización de los sistemas existentes

**Antes de implementar:** auditar contratos reales de CoreRPG/Star Trek, reutilizar identidades, relaciones, agenda, convivencia, memoria y eventos; no levantar un segundo simulador social.

Referencias vigentes:
- `sistemas/gameplay/social/README.md`: relaciones multidimensionales, autonomía y vida social.
- `sistemas/gameplay/social/social_event_rules.json`: invitación, rechazo, expresión romántica, intimidad consentida, compromisos, ruptura y reconciliación.
- `sistemas/gameplay/social/adult_heterosexual_relationship_canon_v0.1.json`: **canon autoral bloqueado vigente**, de ámbito global, que delimita las relaciones románticas/sexuales adultas; esta idea **lo respeta y no lo modifica**.
- `sistemas/gameplay/ship_operations/shipboard_life_state_contract.json`: residencia, familia, privacidad, disponibilidad, guardias y alertas.
- `sistemas/gameplay/ship_operations/off_duty_activity_catalog_v0.1.json`: tiempo familiar, tiempo romántico, vida en camarote, ocio y encuentros.
- `sistemas/gameplay/characters/activity_schedule_model.json`: citas, obligaciones, guardias, desplazamientos, descanso.
- `sistemas/gameplay/characters/character_runtime_model.json`: personajes con identidad persistente, experiencias, afiliación y relaciones.

**Hueco real:** necesitamos **módulo de vida familiar**, matrimonio, unidad doméstica, parentesco, embarazo/nacimiento cuando proceda, niños como NPC persistentes, crianza, educación y efectos a largo plazo. La documentación actual **no acredita que esas mecánicas estén ya implementadas en UE5**.

## 3. Soltería, flirteo, relaciones informales y libertad personal

La modalidad de vida de **soltero picaflor/mujeriego** está **expresamente aprobada**. El jugador puede conocer a diferentes mujeres adultas compatibles, conversar, coquetear, concertar citas, mantener relaciones ocasionales, cambiar de opinión o no tener pareja sin castigo automático.

- La atracción, aceptación de citas, relaciones y límites dependen de cada NPC, la historia compartida y consentimiento contextual.
- Amistad, rango militar, invitaciones, regalos o tiempo transcurrido **no garantizan** interés romántico ni intimidad.
- Diferenciar **no exclusividad acordada**, expectativa ambigua y **compromiso de exclusividad explícito**.
- No crear penalizaciones morales genéricas por flirtear o por una relación casual consensuada y transparente.
- Sí puede haber **consecuencias causales** por promesas incumplidas, engaños, incompatibilidades, celos razonables derivados de hechos conocidos, pérdida de confianza o conflictos profesionales.
- Si el jugador tiene autoridad jerárquica, no permitirá intimidación, coerción, represalias, favores injustificados, ni saltarse responsabilidades de mando mediante romance.
- La IA no inventará recuerdos de intimidad, celos, compromisos o aventuras sin hechos/eventos que los sustenten.
- Los NPC pueden iniciar acercamientos, rechazar, buscar una relación seria, proponer acuerdos distintos o elegir continuar solteros.

Las escenas íntimas adultas, si se decidieran desarrollar, se regirán por los límites de contenido y el diseño artístico del juego; **no son requisito** para demostrar el sistema de relaciones.

## 4. Pareja consolidada, convivencia y matrimonio

Una pareja estable surge de **decisiones mutuas y evolución verificable**, no de completar una barra. Debe tener identidad y expectativas individuales, memoria de encuentros, acuerdos, convivencia, independencia y posibles proyectos comunes.

**Convivencia:**
- Asignar habitación compartida únicamente cuando existe espacio/aprobación y la situación del personaje lo permite; la convivencia no supone disponibilidad continua.
- Compartir comidas, descansos, actividades, conversaciones y amistades según guardias/horarios reales.
- Respetar puerta, privacidad, intercomunicador, asignación de camarote y permisos.

**Matrimonio:**
- Decisión explícita de ambas personas; no aparece por salto de tiempo o sugerencia de IA.
- Registro persistente de vínculo, fecha, lugar, identidad de ambos y ceremonia si se realiza.
- Ceremonia opcional con testigos/invitados que realmente puedan asistir, conversación y recuerdos que se conservan después.
- Posibles efectos profesionales/civiles acorde con la configuración de nave/campaña, sin inventar reglamentos concretos.

**Conflictos y separación:**
- Una pareja consolidada no tiene garantizada felicidad eterna; puede aparecer distancia, desacuerdos, reconciliación o separación.
- Las rupturas no destruyen identidades, relaciones previas ni vínculos de parentesco.
- Nunca se altera la voluntad del jugador sin decisión expresa cuando una transición requiere su participación.

## 5. Tener hijos y formar una familia

**La posibilidad de tener hijos queda aprobada como objetivo de diseño, nunca como obligación.** Debe surgir de decisiones conscientes de los adultos, condiciones de especie/biología o alternativas familiares que el autor apruebe posteriormente y tiempos efectivos del mundo.

### Embarazo y nacimiento, cuando corresponda
- Modelar decisiones de pareja/parentalidad, bienestar y procesos biológicos según las especies aplicables y datos autorizados; no fijar gestaciones idénticas para todas las especies de Star Trek.
- El embarazo y su desarrollo son eventos **persistentes** con tiempo, revisiones y circunstancias realistas de la nave, no un texto narrativo inventado.
- Evitar embarazos arbitrarios que secuestren la voluntad del jugador o NPC. Las reglas concretas de planificación familiar y resultados deberán definirse antes de implementar.
- El nacimiento crea **un nuevo personaje persistente** con identidad propia, progenitores/vínculos, fecha, lugar y estado, no un objeto decorativo ni una sustitución de NPC.
- La IA puede narrar llegada a Enfermería, diálogo con la doctora y celebración solo después de que el motor confirme el evento.

### Crecimiento y crianza
- Niño como persona con **edad y desarrollo**, parentescos, rasgos, necesidades y acontecimientos, conservando su identidad a lo largo de los años.
- Etapas de desarrollo representadas en función de calendario y especie; evitar complejidad de simulación que no genere experiencia significativa.
- Rutinas de familia: desayunos, juegos, actividades, educación, celebraciones y conversaciones acordes a edad.
- Escuela, instalaciones y responsables adultos **solo si existen** en esa nave; no crear una escuela invisible en cada barco.
- Vida a bordo con LOD: una criatura puede seguir una rutina fuera de cámara sin cargar permanentemente su actor 3D.
- Decisiones familiares y educativas relevantes respetan roles de cuidado y consentimiento del adulto responsable, sin convertir al menor en elemento de romance o interacciones adultas.

**Protección de menores:** ninguna mecánica de romance/sexualidad aplicable a adultos podrá aplicarse a menores de edad real o equivalente de especie; acontecimientos familiares son cotidianos y no sexualizados.

## 6. Enterprise-D restaurada y traslados entre naves

La nave central del **Proyecto Valhalla** es la **Enterprise-D modernizada por Geordi**, conservando su identidad Galaxy e inscripciones. En la versión con civiles/familias previstas, podrán diseñarse:
- camarotes familiares y estancias compartidas;
- escuelas/espacios infantiles y áreas de ocio, si su configuración real lo permite;
- Enfermería y servicios adecuados;
- reuniones familiares y eventos sociales a bordo.

**Restricciones de carrera:** ascender, obtener mando, trasladarse o cambiar de nave no mueve automáticamente a pareja/hijos. Por ejemplo, un nuevo destino que no aloje familiares puede exigir relación a distancia, traslado autorizado, permanencia en otra nave o decisiones personales difíciles.

Se mantiene la decisión del proyecto de que la clase **Sovereign no aloja civiles habitualmente**; la simulación deberá respetar restricciones de cada clase/instancia/época y no duplicar ocupantes. Si el jugador vive en otra nave, los familiares siguen en World State y se comunican mediante los canales disponibles.

## 7. Integración de las ideas de inmersión

- [IDEA-0014 — Intercomunicadores](IDEA-0014_intercomunicadores_inteligentes_camarotes.md): visitas, respeto a privacidad y acceso de pareja/familia, interacción natural en la puerta.
- [IDEA-0015 — Turboascensores](IDEA-0015_turboascensores_inteligentes_lenguaje_natural.md): ir al camarote familiar o a una ubicación, solo si es alcanzable.
- [IDEA-0016 — Insignias Starfleet](IDEA-0016_insignias_starfleet_comunicaciones_universales.md): contactar con pareja/hijos cuando corresponda y la comunicación sea posible; las personas civiles pueden necesitar otro dispositivo.
- [IDEA-0012 — Ajedrez con NPC](IDEA-0012_ajedrez_clasico_3d_con_npc.md): ocio, amistades y actividades familiares acordes a edad.

**Importante:** los sistemas de IA expresan emociones, diálogos, iniciativa y relaciones a partir del estado; no pueden decidir por sí mismos matrimonio, filiación, nacimientos, embarazos o transferencias definitivas. Se requiere validación, eventos y persistencia.

## 8. Arquitectura del módulo familiar

**Familias de datos conceptuales, no contratos existentes:**
- Relaciones: `relationship_id`, expectativas de compromiso/exclusividad, límites, hitos, memoria causal, historia.
- Unidad doméstica: `household_id`, `ship_id`, `residence_location_id`, miembros, derechos de acceso, capacidad y convivencia.
- Matrimonio/unión: `union_id`, participantes, fecha, estado, lugar, testigos y registros.
- Parentesco: `kinship_edge_id`, roles de progenitor/tutor/descendiente y temporalidad; no inferir parentescos sin evento válido.
- Maternidad/paternidad: decisiones/condiciones, embarazo y nacimiento si aplican, cambios de estado, cuidados, calendario.
- Niñez/desarrollo: ID de persona, edad biológica relevante, necesidades, rutina, centro educativo/lugar de cuidado, relaciones, recuerdos y desarrollo.
- Vida familiar: reuniones, cenas, celebraciones, desacuerdos, obligaciones, permisos, destinos profesionales y comunicación a distancia.

**Regla cardinal:** ningún NPC, bebé, matrimonio, cumpleaños o evento familiar aparece solamente porque la IA lo ha escrito. El motor autoritativo registra primero lo que sucede; la IA lo narra después.

## 9. Etapas propuestas — LIFE-01 a LIFE-09 (NO iniciadas)

1. **LIFE-01 — Auditoría y ampliación mínima de relaciones:** verificar contratos, intenciones, privacidad, acuerdos y persistencia.
2. **LIFE-02 — Soltería, citas y relaciones informales:** interés recíproco, libertad, autonomía, acuerdos de exclusividad/no exclusividad, reacciones y memoria.
3. **LIFE-03 — Pareja consolidada y convivencia:** horarios, espacios, intimidad privada, actividades y decisiones conjuntas.
4. **LIFE-04 — Matrimonio:** compromiso explícito, ceremonia, registros, efectos de estado y memoria.
5. **LIFE-05 — Decisiones reproductivas y nacimiento:** condiciones de especie, gestación cuando corresponda, filiación y seguridad narrativa.
6. **LIFE-06 — Hijos persistentes y desarrollo:** edad, educación, cuidados, personalidad y representación por etapas.
7. **LIFE-07 — Carrera vs. familia:** traslados, restricciones de naves, vida civil, vivienda y relaciones a distancia.
8. **LIFE-08 — IA narrativa y memoria:** diálogos y acontecimientos creíbles, sin crear hechos no autorizados.
9. **LIFE-09 — QA y continuidad de años:** decisiones del jugador, autonomía NPC, consentimiento, guardados, tiempos, naves/ubicaciones y familias persistentes.

## 10. Criterios mínimos de aceptación

1. El jugador no está obligado a iniciar una relación ni formar familia, y puede cambiar de preferencias con el tiempo.
2. Vida de soltero/picaflor/mujeriego, citas ocasionales y relaciones informales son posibles **sin penalización moral automática** y sin que el NPC pierda autonomía.
3. Intenciones, consentimiento, compatibilidad romántica y límites respetan el **canon autoral vigente** y sus reglas de adultos.
4. Amistad, jerarquía, tiempo y reputación no generan romance o sexo por defecto.
5. Una relación estable, matrimonio o filiación tiene **evento causal, voluntad legítima y estado persistente**.
6. Hijos son NPC persistentes, con identidad, fecha, parentesco, edad y rutina coherentes, no texto improvisado.
7. Convivencia y educación usan instalaciones existentes y disponibles; no hay NPC en dos lugares a la vez.
8. Traslados, ausencia, vida familiar y cambios de nave tienen consecuencias sin desaparecer ni duplicar a familiares.
9. La simulación social conserva recuerdos privados y públicos con límites de conocimiento y confidencialidad.
10. Solo se declarará implementado cuando haya demostraciones reales y pruebas de continuidad, incluidas en MSI/UE5 cuando corresponda.

## 11. Decisiones cerradas y pendientes

**Aprobado expresamente:** vida personal completamente opcional; vida de soltero ligón/mujeriego, relaciones informales, pareja estable, matrimonio, hijos y crianza, y consecuencias en la carrera; integración en la USS Enterprise-D modernizada del Proyecto Valhalla.

**Pendiente de futura concreción:** alcance exacto de ceremonias y desarrollo infantil, datos por especie, reglas de planificación reproductiva, escuelas y alojamientos reales, escenas 3D, modalidades de diálogos íntimos permitidos, formatos de contratos y prioridades de fase.

**Estado administrativo:** IDEA-0017 **APROBADA COMO DISEÑO**. No se ha implementado ninguna de estas mecánicas por inscribirla en el buzón.
