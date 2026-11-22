# Sistema 04 — Protagonista, identidad, acceso y carrera

**Versión:** 2.0 · 17-11-2026 · **APROBADO EN DISEÑO**, todavía no implementado en CoreRPG/HOST/UE5. **Decisión superior:** [DEC-0022](../../../proyecto/docs/decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md).

## 04.0 — Qué hace (y qué deja de hacer)

**Antes:** creador abierto con tres especies jugables, edad/origen/biografía libre, evaluación del borrador y generación de un cadete. **Ahora:** una sola biografía canónica elegida por el autor, presentación audiovisual y edición **solo estética/nombre**, seguida por una carrera y una vida verdaderamente abiertas a las decisiones del jugador. No es un creador universal ni una «clase Khan» para todos los personajes. Conserva y reutiliza las infraestructuras históricas de validación, personaje persistente, Academia, NPC y carrera sin confundirlas con UX vigente.

**Recorrido objetivo de nueva partida:**

```text
INICIAR NUEVA PARTIDA
  -> alias/perfil de jugador separado (si procede)
  -> nombre jugable + peinado/barba/pequeñas facciones/estética
  -> ficha fija canónica del aspirante (sin editar su historia)
  -> validación F10 de coherencia de adaptación/procedencia (no autocompletado creativo)
  -> acto institucional de admisión con fuente/autoridad (sin fabricar plazas)
  -> presentación cinematográfica del expediente, debate y vida previa
  -> escena de entrada a Academia en 2383
  -> 4 años de aprendizaje y pruebas; ingreso en servicio como alférez si legítimo
  -> carrera, relaciones, mando y moral emergentes; posible capitanía de Enterprise-D
```

La secuencia puede montar la **audiencia antes del acto efectivo** y mostrar el veredicto después; las fechas reales quedan registradas. El jugador no repetirá la tramitación que la historia ya resolvió en la misma partida. Aceptación ≠ rango ≠ destino ≠ capitanía.

## 04.1 — Identidad no editable

| Dimensión | Valor |
|---|---|
| Presentación corporal/sexo | Varón, sin opción de cambio |
| Especie | Híbrido humano-vulcano (`human_vulcan_hybrid`) |
| Madre | Vulcana biológica |
| Padre | Humano, descendiente directo por generaciones de Khan Noonien Singh |
| Sangre del linaje | Reexpresión individual excepcional de características mejoradas; sin augments auto-replicados en otros NPC |
| Año/edad | Entrada 2383, 45 años terrestres, nacimiento aprox. 2338; apariencia ~30 |
| Longevidad | Envejecimiento lento, expectativa amplia híbrida 150–200 años como guía, no muerte fijada |
| Rasgos | Fuerza, reflejos y resistencia muy elevados pero finitos; tolerancia a lesiones no invulnerabilidad |
| Artes marciales | Maestro kung-fu, kárate, aikido y Suus Mahna |
| Emociones | Expresión y control aprendidos; furia posible, no pérdida obligatoria ni poder gratis |
| Vocación | Ciencias, astronomía/astrofísica; música y estudio como equilibrio |
| Preparación | Décadas de preparación física, mental y académica antes de solicitar plaza |
| Transparencia | Declara su ascendencia y características, no oculta ni falsifica expediente |
| Carrera anterior | Civil; sin grados, puestos, destinos ni accesos Starfleet previos |

**No se cambiarán** infancia, genes, edad, especie, rama Khan, sexo, estudios base, padres, motivación o formación marcial en una nueva partida. La biografía aprobada es el contenido fijo; los detalles aún no escritos requieren decisión autoral, **no una IA que rellene huecos libremente**.

## 04.2 — Personalización sí permitida

- **Nombre:** nombre y, si el autor lo decide, apelativo/apellidos/forma de tratamiento. El linaje Khan no obliga a usar «Noonien Singh» como apellido público.
- **Rostro y aspecto:** peinado, vello facial, pequeños ajustes faciales, color y matices visuales consistentes con ascendencia/identidad, rasgos vulcanos dentro de una horquilla creíble, uniforme/accesorios conforme a cargo. No remodelación genética.
- **Vista previa:** 3D UE5 cuando exista un modelo validado; la falta de avatar no bloquea definir el diseño ni crear 2D para intro.
- **Continuidad:** cambios de peinado y barba pueden suceder durante campaña por acciones normales; siempre el mismo `character_id` de esa partida, la misma biografía y procedencia. Los retratos/escenas deben seguir el aspecto registrado o evitar mostrar contradicciones.
- **Sin selector** de especie, sexo, edad de entrada, origen paterno/materno, historia aleatoria, valores de atributos, «clase» o afinidad inicial con Siete.

## 04.3 — Genética, capacidades y vida previa

**Capacidades reales:** el legado de Khan (tras generaciones de baja expresión) y la fisiología vulcana producen capacidades físicas y neuromotoras extraordinarias, a validar sobre escala comparativa coherente con el universo. No reducidas a una mejora cosmética del 5 %, tampoco eficacia infinita, telepatía omnipotente, conocimiento automático, inmunidad a armas ni condición de invencible. Definir curvas/efectos mediante CoreRPG antes de implementarlos. No aplicar este perfil al resto de humanos o híbridos.

### 04.3.1 — Potencial biomédico de la sangre del protagonista (ampliación autoral 19-11-2026)

**Hecho de diseño aprobado:** por su linaje directo de Khan Noonien Singh y la reexpresión excepcional de rasgos heredados, **la sangre del protagonista presenta propiedades biológicas extraordinarias potencialmente aprovechables en medicina**. La interacción con su fisiología humano-vulcana es una explicación narrativa posible, aún no cuantificada. Esta característica pertenece a **este protagonista**, no se atribuye automáticamente a todos los descendientes de Khan, humanos aumentados o híbridos.

**Utilidad jugable buscada:** el personal médico de la nave podrá **solicitar su presencia voluntaria en Enfermería** para una extracción o evaluación clínica cuando exista una necesidad razonable, incluso cuando el protagonista esté sano. Tras los análisis pertinentes, las muestras podrán apoyar **investigaciones, desarrollo de tratamientos, sueros, antídotos, vacunas o terapias regenerativas para problemas determinados**. No se fijan todavía patologías concretas, protocolos, probabilidades, potencias, número de muestras ni eficacia: se diseñarán al concretar las capacidades del personaje y la medicina del juego.

**Límites expresos:** no es una cura universal ni un mecanismo automático de resurrección al estilo de cualquier escena Kelvin; la respuesta depende del paciente, compatibilidad biológica, diagnóstico, disponibilidad, procesamiento, investigación y validación médica. No asegura curar todas las enfermedades ni evita lesiones, daños o mortalidad del protagonista. La propiedad **no convierte el origen Kelvin en canon íntegro de nuestra continuidad**: es una decisión autoral propia inspirada en *Star Trek: En la oscuridad*.

**Situaciones posibles:** aviso del jefe médico; consulta y conversación en Enfermería; consentimiento informado; extracción y registro de muestra; análisis del laboratorio; petición de colaboración en una investigación; seguimiento de un tratamiento y consecuencias clínicas o narrativas reales. La donación puede producir nuevas interacciones cotidianas, dilemas o misiones sin exigir que el jugador enferme. Los NPC no conocerán automáticamente datos clínicos privados ni el jugador estará obligado a donar en toda petición; las respuestas y sus consecuencias se concretarán durante el diseño.

**Fronteras:** S04 define el rasgo personal y su disponibilidad; las reglas médicas/validación y el estado verdadero se implementarán en el dominio competente y CoreRPG; S05 aporta iniciativa de médicos, S07 oportunidades narrativas, S02/S12 interacción y visita física, S15 muestras como objetos trazables, S16 vida cotidiana y S18 acceso/privacidad cuando corresponda. HOST y UE5 coordinan/presentan, sin fabricar curaciones ni llamadas de IA que determinen hechos médicos. No se crea un sistema S20 ni se modifican ahora contratos F10/HOST/UE5, parámetros jugables, archivos JSON de identidad o código. **Estado: IDEA AUTORAL APROBADA, DISEÑO CONCEPTUAL; IMPLEMENTACIÓN Y BALANCE PENDIENTES.**

**Dominio marcial existente:** décadas de educación desde edad temprana justifican la pericia en cuatro disciplinas; maestría no equivale a diplomas inventados de instituciones concretas. Los hechos autorales de instrucción validados se reflejan en capacidad inicial; no sumar puntos desde un campo de texto. En una pelea, debe existir una ventaja notable contra combatientes ordinarios; la misión del juego no es fabricar peleas constantes.

**Lógica y emociones:** la madre le enseñó prácticas de disciplina vulcana. No completó automáticamente Kolinahr ni se suprimieron sus emociones; elige gobernarlas. La furia hereditaria es un **rasgo narrativo de temperamento**, no una predisposición moral inevitable ni un botón de berserker que multiplica daño gratuitamente. Puede tener efectos positivos (determinación, intensidad) y negativos (impulsividad si falla el control) vinculados a circunstancias y decisiones. Artes marciales y música como estrategias aprendidas de autorregulación.

**Formación académica civil:** ciencias, astronomía/astrofísica y música antes de 2383, con competencias reales de aprendizaje. Ningún grado universitario específico, investigación clasificada, licencia médica o maestría científica universal sin que el autor lo concrete. La vocación científica es fuerte, pero el jugador podrá desarrollar carrera/mandos y especialidades posteriores sin forzar un destino de Seguridad.

## 04.4 — Admisión institucional, Cinemática y Academia

- El expediente de 2383 declara genética/linaje y formación completa; las objeciones institucionales son razonadas y con contradicción.
- **Janeway y Picard están A FAVOR del derecho a ser admitido mediante evaluación justa**, no de sortear reglas. Contra: 2–3 almirantes ficticios. Janeway primero como defensa pragmática; Picard culmina debate, menciona que fue Locutus y la diferencia entre origen y elecciones.
- Junta consultiva **distinta** de órgano formal que emite decisión académica; conservar valor de pruebas de ingreso F10 y reglas de admisión, aunque el comienzo definitivo como cadete precise haberlas completado antes de la escena de llegada. No «un jurado literario da un PERSON».
- Narración acompaña imágenes de **cinco etapas**: nacimiento, manifestación infantil, adolescencia/conciencia familiar, décadas de formación, solicitud a los 45. Estética 2D magnífica preferida a 3D pobre; voces y música como producción posterior.
- Sisko ausente del debate en 2383 (según LORE-05B). El guion definitivo y detalles artísticos se co-diseñarán después; documento `S04_INTRO_CINEMATICA_PLAN_v1.md`.
- Academia **duración aprobada 4 años**, año real 2383–2387 aproximado, currículo, pruebas y vida social según F10; no modificar aquí F10 currículo ni añadir academia 3D obligatoria. El carácter excepcional no concede aprobados por defecto.
- El protagonista empieza con identidad y antecedes, **no con rango**, puede aprender, cometer errores, crear amistades y ganar méritos.

## 04.5 — Relaciones y conocimiento del mundo

- **Picard** conoce expediente y defiende candidatura de forma institucional en 2383. Relación personal comienza durante Academia y evoluciona desde el interés hasta una mentoría ganada. Entrega personal de galones al ascender legítimamente a capitán según F11.
- **Janeway** lee expediente y lo defiende en 2383 sin encuentro presencial garantizado; su primer encuentro personal puede llegar mucho después, a través de Siete. Futuro puente a misiones del Delta.
- **Siete de Nueve** sigue siendo persona independiente, con trauma Borg, experiencia compartida de ser juzgada, metas, agenda, consentimiento; potencial amistad/romance solo por actos de campaña. Janeway puede hablarle de la candidatura y mérito del oficial cuando exista motivo y derecho a compartirlo.
- **Contraalmirantes ficticios** pueden sostener reservas al principio y cambiar de opinión por hechos; el estatus opositor no determina moralidad/hostilidad de por vida. No añadir personajes legendarios nuevos.
- Relación y memoria de NPC provienen de hechos conocidos, no de conocimiento omnisciente de la IA. La reputación se propaga por fuentes concretas, respetando privacidad del expediente genético.

## 04.6 — Carrera, decisiones y rejugabilidad

- Independientemente de cuántas veces se reinicie, **identidad y prólogo son los mismos** (con nombre/aspecto personalizables); cronología del nacimiento, legado Khan y núcleo de personalidad no cambian.
- Historia tras el comienzo: libre de elegir obediencia, ética, disciplina, alianzas, especialidad dentro de su vocación, objetivos, destinos, relaciones y forma de ejercer el mando. Los rangos y mandos no se regalan ni están preasegurados.
- Mantener carrera acordada: Academia → alférez → teniente junior → teniente → teniente comandante → comandante → capitán; puestos separados del grado; el destino/mando en Enterprise-D no procede directamente de los genes.
- Un comportamiento profesional malo tiene consecuencias reales sin borrar retrospectivamente que Picard defendió la oportunidad. Podrá decepcionar, ganar respeto o afrontar sanciones.
- El arco de Khan es identidad de origen y motor narrativo, **no misión permanente**. La ciencia, exploración, paz, cotidianeidad y el mundo vivo continúan siendo centrales.
- La intro solo representa historia ya registrada: saltar o rever no crea ni revoca admisión, amistad, rango o expediente. Guardado/carga conserva el mismo sujeto y procedencia.

## 04.7 — Arquitectura y responsabilidades

**Propiedad de datos:** DEC-0022 fija decisiones; `s04_fixed_protagonist_contract_v2.json` y `s04_protagonist_biography_v1.json` materializan perfil inicial de referencia; `S04_INTRO_CINEMATICA_PLAN_v1.md` gobierna la puesta en escena.

**F10:** interpreta biografía autoral fija y verificación institucional; nunca crea héroes alternativos desde formulario. La validación IA puede analizar contradicciones de cambios futuros de **diseño**, pero no exigir al jugador que reescriba los genes aprobados. **CoreRPG:** crea PERSON autorizada y decide estado/habilidades/rango/vida. **HOST H03/H04/H06:** sesión y vínculo único, persistencia, proyección de perfil, selección estética y reproducción idempotente del prólogo; no concede derechos. **UE5:** avatar/interfaz/ilustraciones/vídeo. **F11:** carrera y autoridad. **NPC/social:** hechos conocidos y vínculos emergentes.

Los contracts F10 `character_creation_contract_v1_0.json`, `f10_initial_player_rules_v0.1.json`, `f10_formulario_inicial_v0.3.json` siguen preservados porque el HOST los usa y son evidencia histórica. **Su selección libre ya no prevalece como decisión autoral del producto**. Plan de migración: `S04_MIGRACION_F10_HOST_v2.md`. No declarar que H06/IA-03A se ha adaptado con esta PR documental.

## 04.8 — Pruebas de aceptación previstas

- Rechaza intentar alterar especie, sexo, edad, linaje, padres, maestría de base o historia en UI y payload.
- Admite cambios de nombre, peinado/barba/facciones cosméticas sin alterar ADN, poderes o historia.
- Instancia solo el héroe predefinido mediante F10 con prueba/autoridad; ningún texto cliente o IA fabrica PERSON/credenciales.
- Prueba genética y entrenamiento se reflejan en capacidad efectiva, sin automatismo de Security.
- Picard/Janeway conocen de forma temporalmente válida el expediente; no se fuerza encuentro personal con Janeway en Academia ni encuentro temprano con Siete.
- Debate inicial y cinco recuerdos se representan de forma legible en 2D y la escena de ingreso es idempotente.
- Repetición cinematográfica/carga no repite acta institucional, guardado ni bonus.
- Sisko no aparece antes de su regreso, capitán continúa siendo meta ganada; cadete no tiene rango.
- Se conserva el funcionamiento de NPC no protagonistas y de viejas partidas con política de migración prudente.

**Las pruebas son criterios aún no ejecutados, salvo las verificaciones documentales que consten en esta PR.**
