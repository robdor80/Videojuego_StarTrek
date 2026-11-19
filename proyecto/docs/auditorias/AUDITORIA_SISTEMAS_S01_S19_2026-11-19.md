# AUDITORÍA TRANSVERSAL — SISTEMAS S01–S19
## Videojuego Star Trek RPG · versión 1.0 · 19 de noviembre de 2026

**Tipo:** auditoría independiente de concepto, arquitectura, planificación y cobertura.  
**Estado del informe:** ENTREGADO PARA REVISIÓN; las recomendaciones no son decisiones autorales ni certificados técnicos.  
**Repositorio:** robdor80/Videojuego_StarTrek. **Referencia de lectura de main:** 8991e5332b70bfdc1999f610560131e82d3b41ff (18-11-2026, 21:58 UTC).  
**Alcance:** 19 sistemas aprobados en conversación, fuentes de decisión y diseño, roadmap F00–F15, Planificación 2, HOST H00–H13, Lore y dependencias UE5/CoreRPG.  
**Evidencia:** lectura documental y de estructura remota de GitHub; **no** se ha ejecutado código, CI, Unreal, compilación ni prueba en el MSI. Los datos del historial se interpretan según la fecha y madurez de cada fuente. No se han inspeccionado proyectos ni laboratorios locales.

> **DICTAMEN:** Mantener los 19 sistemas como agrupaciones funcionales. No está justificado crear ahora una vigésima familia de jugabilidad. Hay deudas transversales y contradicciones entre documentos históricos y decisiones más recientes que deben corregirse antes de expandir la ejecución. La prioridad es disponer de un primer bucle realmente jugable de la Enterprise-D con verdad Core, coordinación HOST, presentación UE5, NPC y guardado, no producir más contratos desconectados.

---

## 1. Alcance y criterios de auditoría

Se han evaluado cinco dimensiones por sistema: **valor para el jugador**, **propietario de la verdad/acciones**, **dependencias**, **viabilidad en PC objetivo** y **criterios verificables de aceptación**. Se han buscado redundancias, condiciones de bloqueo, estados documentales confundidos con implementación, carencias y riesgo de sobreingeniería.

Se conserva la regla existente: **CoreRPG** es autoridad del mundo y persistencia general; **reglas Star Trek/Fxx** son propietarias de las decisiones de dominio; **HOST** compone sesión, servicios y encaminamiento sin duplicar reglas; **Unreal Engine 5** representa e interactúa; **IA central** interpreta y expresa pero no inventa la realidad ni concede permisos. Documentos aprobados después prevalecen únicamente en lo expresamente modificado; se conserva el historial con indicación de obsolescencia.

**Decisiones que no se reabren:** videojuego estrictamente personal; Enterprise NCC-1701-D reconstruida por La Forge mediante Proyecto Valhalla, **no** nave ni clase denominada Valhalla; Academia desde 2383, graduación aproximada 2387; protagonista único híbrido humano-vulcano descendiente de Khan; aventura principalmente tranquila con emergencias poco frecuentes; no Q/Continuo Q; IA OpenAI única a través del HOST sin API propia por subsistema; sensores extraordinariamente competentes de la Enterprise-D cuando el refit está activo; estilo interior Galaxy Refit A2; interfaz en castellano.

**Limitación de trazabilidad del número 19:** el acuerdo conversacional incorpora la música como sistema 19, pero en main no se localiza aún un DEC o ficha S19 que fije **nombre oficial y límites exactos**. En este informe se denomina **S19 — Música / experiencia musical (etiqueta provisional)**; se auditan las necesidades musicales documentadas, sin presumir que el autor haya aprobado convertir toda la ingeniería de sonido o TTS en S19. La idea documentada IDEA-0002 es solo una parte de su posible alcance. El número no se reasigna.

## 2. Catálogo auditado y evaluación sintética

| Sistema | Función principal | Veredicto de concepto | Deuda dominante |
|---|---|---|---|
| S01 — IA central | Servicio único de lenguaje y análisis | **Mantener** | Integración de consumidores, latencia, límites reales de uso y modo degradado |
| S02 — Interacción e interfaces | LCARS, mundo, órdenes, voz/texto/PADD | **Mantener** | Unificar las intenciones y las autorizaciones; controles alternativos |
| S03 — Universo Vivo | Evolución causal y offscreen | **Mantener, acotar** | Contratos P2 ≠ simulación galáctica ejecutable; coste temporal |
| S04 — Personaje y carrera | Protagonista, Academia, servicio y ascensos | **Revisar implementación** | Migrar F10/HOST desde editor anterior a protagonista fijo |
| S05 — NPC y tripulación | Identidades, agendas, iniciativa y tareas | **Mantener** | Escalado por LOD; frontera S03/S06/F05 |
| S06 — Relaciones sociales | Vínculos, memorias y consecuencias | **Mantener** | Consentimiento/autonomía, coherencia temporal y privacidad |
| S07 — Misiones y narrativa | Episodios, emergencias y arcos | **Mantener, moderar** | Director causal, ritmo y no fabricar hechos para contar historias |
| S08 — Vuelo y navegación | Rutas, órdenes y maniobras | **Mantener** | Autoridad y resolución real; no duplicar astrometría |
| S09 — Combate espacial | Táctica, daño, defensa y retirada | **Mantener** | IA táctica NPC y prestigio de la Enterprise-D sin invulnerabilidad |
| S10 — Sensores y exploración | Detectar, identificar e informar | **Mantener, adaptar** | Doctrina DEC-0021 frente a flujos antiguos lentos |
| S11 — Astrometría 360° | Mapa científico holográfico inmersivo | **Mantener** | Solo diseño; cuatro escalas, conocimiento y rendimiento UE5 |
| S12 — Interiores y desplazamiento | Nave física, puertas, ascensores y rutas | **Mantener** | Transformar geometría y grafo en recorrido jugable estable |
| S13 — Exploración planetaria | Misiones de superficie y descubrimiento | **Mantener, delimitar** | Volumen de assets y escenarios; no prometer planetas infinitos |
| S14 — Holocubierta | Simulaciones y entrenamiento/ocio | **Mantener** | Separación realidad/simulación y control de consecuencias |
| S15 — Objetos e inventario | Equipo, replicador y persistencia | **Mantener** | Identidad/propiedad de objetos y replicación sin creación arbitraria |
| S16 — Vida a bordo | Rutinas, actividades, servicios y descanso | **Mantener** | Dependencias de S05/S06/S12, evitar subsistemas cosméticos vacíos |
| S17 — Minijuegos | Ajedrez y ocio interactivo | **Mantener con alcance pequeño** | Reglas, NPC y esfuerzo frente al bucle principal |
| S18 — Identidad, autenticación y control de accesos | Autenticación y autorización de accesos | **Mantener; bien delimitado** | Es diseño, no cerraduras UE5; frontera S12/Core/HOST |
| S19 — Música / experiencia musical | Música contextual y biblioteca musical personal | **Mantener; formalizar** | Sin decisión/contrato S19 en main; reproducción local, mezcla y permisos |

**Interpretación de la tabla:** no se atribuye a cada sistema un estado runtime completo. Existen distintos niveles de evidencia: diseño, contratos, simuladores de referencia, código nativo parcial, pruebas aisladas y escenas UE5 reportadas. El estado de una fase Fxx o Hxx no certifica automáticamente toda su familia Sxx.

## 3. Auditoría por sistema — hallazgos y prueba de salida

### S01 — IA central
- **Fortaleza:** la infraestructura HOST IA-01 ya documenta una única instancia de servicio, rutas lógicas, cola acotada, transporte HTTPS, cancelación, validación de JSON y ausencia de poderes sobre World State. La conexión real y el uso por todos los sistemas **no están certificados extremo a extremo**.
- **Riesgos:** una sola cola/trabajador puede hacer esperar diálogos prioritarios detrás de resúmenes extensos; un contador de llamadas no es presupuesto monetario; cada petición remota añade latencia y posible fallo/coste. No confundir cuota ChatGPT con consumo de API. Revisar nombres/modelos efectivos al configurar, sin fijar identificadores en reglas de jugabilidad.
- **Acción:** definir clases de prioridad, límite de solicitudes en curso, cancelación por cambio de escena, caché de respuestas derivadas con vigencia, presupuesto por sesión, tratamiento de 401/429/cuota, salida determinista o mensaje de indisponibilidad y prohibición de desbloquear decisiones mediante fallo de API. Las peticiones simples del ordenador no necesitan LLM.
- **Prueba mínima:** dos NPC solicitando diálogo mientras se pide un resumen; cancelar por LOAD; conservar FPS, identidad y conocimiento; comprobar cero llamadas para abrir puertas, hora, inventario o sensores ordinarios.

### S02 — Interacción e interfaces
- **Fortaleza:** la combinación aprobada de interacción 3D y pantalla completa LCARS favorece una nave habitable.
- **Riesgos:** crear distintos intérpretes para PADD, consola, comunicador, turbolift, ordenador y menú; divergencias entre pulsación, texto y voz; dependencia innecesaria de micrófono/API.
- **Acción:** un **contrato de intención** compartido con origen/actor/destino, un validador de autoridad y múltiples representaciones. Acciones básicas siempre disponibles por botones o texto; voz como interfaz opcional, no credencial. Priorizar legibilidad en 2560×1600 y mandos/ratón/teclado; respetar castellano.
- **Prueba:** la misma acción ejecutada por botón y por frase produce idéntico resultado, denegación y registro, sin doble evento.

### S03 — Universo Vivo
- **Fortaleza:** Planificación 2 B01–B10 y las capas procedurales cubren causas, economía, colonias, guerra, crisis, descubrimientos y evolución offscreen de forma documental.
- **Riesgos:** confundir **contratos/referencias cerradas** con simulación viva de escala galáctica; actualizaciones gigantescas en cambios de turno o saltos de Academia; desincronización de NPC presentes frente a resultados offscreen; conocimiento omnisciente en interfaces.
- **Acción:** tres resoluciones explícitas: actores visibles/alta fidelidad; región activa simplificada; universo lejano por eventos agregados. Registro causal, semillas/versiones y reglas deterministas de avance, con un presupuesto medido de CPU/RAM y cola de reincorporación al volver a zona.
- **Prueba:** avanzar semanas/años, cargar partida, reabrir el mismo sector y comprobar identidades, cronología, sucesos y conocimiento del observador sin duplicados.

### S04 — Personaje y carrera
- **Hallazgo crítico:** DEC-0022 (17-11) **sustituye** la selección libre de especie, edad, sexo e historia de origen por un protagonista fijo de 45 años en 2383, híbrido humano-vulcano y descendiente de Khan. H06/F10/IA-03A todavía contienen contratos/código de la propuesta histórica y necesitan migración v2.
- **Acción:** crear un flujo productivo de nueva partida que permita solo nombre/cosmética autorizada, fije biografía/rasgos y aplique evaluaciones, asignaciones y ascensos en sus autoridades reales. No eliminar contratos históricos bloqueados: versionar y migrar. Introducción audiovisual omitible/repetible sin conceder dos ingresos.
- **Diseño narrativo:** Academia de cuatro cursos consistente, pero presentación compacta y progresión libre una vez destinado; la Enterprise-D no se entrega por derecho de nacimiento ni por favor de Picard.
- **Prueba:** nuevo juego con perfil fijo; partida antigua reanudable o migración explícita; cero selección de especie; ascenso únicamente con evidencia F11/Core; recepción ceremonial de Picard solo tras nombramiento legítimo.

### S05 — NPC y tripulación
- **Fortaleza:** F04/F05 y diseño de vida de nave ya reúnen roles, guardias, identidades, órdenes, delegación e iniciativa.
- **Riesgos:** que S05 compita con S03 (evolución fuera de escena) o S06 (relaciones), que cada NPC invoque IA periódicamente y que todos tengan IA de máxima fidelidad continuamente.
- **Acción:** una identidad persistente y un planificador de actividad por niveles de detalle; IA lingüística **bajo demanda**, decisiones rutinarias deterministas; coherencia entre puesto, turno, presencia y acceso S18.
- **Prueba:** dos oficiales terminan guardia, se desplazan y ejecutan tareas sin el jugador, conservan memoria y no atraviesan puertas cerradas tras LOAD.

### S06 — Relaciones sociales
- **Fortaleza:** existen contratos de relaciones multidimensionales, memoria, consentimiento y vida social.
- **Riesgos:** un resumen generado por IA puede atribuir hechos íntimos o acuerdos inexistentes; relaciones con personajes legendarios podrían imponerse por el guion; horarios y distancia física pueden ignorarse.
- **Acción:** la relación se modifica por eventos verdaderos y autorizados; la memoria NPC solo recoge lo observado/comunicado legítimamente. Mantener autonomía de Siete y demás personajes; evitar indicadores simplistas de cariño o «puntos» como fuente única.
- **Prueba:** una conversación no observada no aparece como recuerdo público; rechazo de una invitación se respeta; cambios persistentes solo ante evento confirmado.

### S07 — Misiones y narrativa
- **Fortaleza:** arcos, temporadas, misiones emergentes y decisiones F11 permiten historias largas.
- **Riesgos:** dirigir toda la partida hacia crisis constantes o forzar una tragedia para sostener el drama; duplicar la generación de eventos de S03; introducir hechos retroactivos a favor de un episodio.
- **Acción:** separar generador de candidatos narrativos, validador causal de Core y presentación. **Predominio de vida tranquila**; misiones de alto riesgo excepcionales. Arco Borg lento, Siete y posible Delta se tratan como **contenido** de S07, no sistema nuevo; Directiva Omega como acontecimiento excepcional; **Q excluido**. Órdenes estratégicas relevantes llegan mediante autoridad y comunicaciones diegéticas, no avisos omnipotentes.
- **Prueba:** una misión fallida/pospuesta no crea naves inexistentes; crisis no se dispara durante una escena incompatible; una llamada del almirantazgo no sustituye autorización institucional.

### S08 — Vuelo y navegación
- **Fortaleza:** hay operaciones de nave y contratos de navegación, autoridad y propulsión.
- **Riesgos:** duplicar cálculo de ruta en Astrometría S11; ejecutar saltos/maniobras desde una vista sin autoridad; usar minijuegos técnicos para rutinas que deberían ser directas.
- **Acción:** navegación calcula y ejecuta por orden autorizada; S11 solo **representa/propone**. Priorizar órdenes claras, visualización comprensible y comportamiento profesional de pilotos NPC.
- **Prueba:** una propuesta de ruta de un cadete no mueve la nave hasta recibir orden válida; desviación y cancelación mantienen estado/persistencia.

### S09 — Combate espacial
- **Fortaleza:** combate encaja con tácticas, daños, reparación, alertas y prestigio de una Galaxy refit.
- **Riesgos:** una Enterprise-D superior no debe convertirse en nave invulnerable, y adversarios racionales no deberían atacar suicidamente por defecto; tampoco montar un segundo juego táctico desligado de sensores y cadena de mando.
- **Acción:** compartir datos S10, órdenes F05/F11, daño/ingeniería, reglas de enfrentamiento, retirada, negociación y conocimiento de enemigo. Reputación y disuasión del refit aplicadas solo cuando su perfil esté realmente activo (DEC-0021).
- **Prueba:** NPC puede retirarse o negociar; orden no autorizada de disparo se deniega; daños reales afectan sistemas sin falsear sensores ordinarios.

### S10 — Sensores y exploración
- **Hallazgo crítico de coherencia:** DEC-0021 exige que la Enterprise-D modernizada, operativa y dentro de sus condiciones de observación, entregue **informes ordinarios completos y prácticamente inmediatos**. Prototipos antiguos con análisis triviales lentos pueden seguir siendo históricamente válidos, pero **no son la UX objetivo** del refit.
- **Acción:** una solicitud ordinaria → un informe completo e inmediato, objetivo de medición ~1 s. Separar fenómeno genuinamente excepcional, avería significativa y secreto no conocido; el «0,1 %» orienta rareza narrativa, **no** un dado de fallo de barrido. Precalcular perfiles y reutilizar observación autoritativa.
- **Prueba:** clase/defensas/armamento/propulsión conocidos de un contacto ordinario, sin sucesivas peticiones ni tiempo artificial; casos negativos de camuflaje/anomalía explicables.

### S11 — Astrometría 360°
- **Fortaleza:** DEC-0023, diseño y hoja S11-I01–I08 especifican holograma de cuatro escalas, conocimiento, ciencia y rutas, con criterios de rendimiento.
- **Riesgos:** construir un segundo mapa/estado galáctico, fingir coordenada Z=0, representar todo el Cuadrante Delta como observado, o dedicar la VRAM de 8 GB a estrellas individuales.
- **Acción:** proyecciones derivadas y filtradas de Core; coordenadas de render locales, LOD/instancias, detalle bajo demanda; escala esquemática etiquetada; navegación no ejecutada por la sala.
- **Prueba:** Sol–Vulcano y Tierra–Vulcano, selección/zoom/cámara 360°, filtros de conocimiento, menú/voz opcional, respuesta rápida y FPS medidos en UE5. **Estado actual: diseño, no sala ejecutable.**

### S12 — Interiores y desplazamiento
- **Fortaleza:** corredor, sala y cartografía del refit son el corazón espacial del juego, con rutas/turbolifts.
- **Riesgos:** confundir maqueta Blender con nivel UE5 transitable; puertas físicamente animadas sin permisos; grafos de navegación que no correspondan a la geometría final; inconsistencias de altura/cubiertas; escenas remotas interpretadas como conexiones físicas.
- **Acción:** crear un mapa navegable por tramos, portal/colisión medidos, puertas conectadas a S18, y navegación NPC al **turboascensor y parada reales**. Respetar cubierta y geometría Valhalla aprobadas; puente de batalla externo mediante acceso virtual sin inventar un corredor físico.
- **Prueba:** camarote → corredor → ascensor → zona de trabajo, ida/vuelta de NPC y jugador, puerta pública/privada, carga/reinicio; sin atravesar paredes ni quedarse bloqueado. Los 50/50 y 44/44 de Sutherland están **reportados** y aún requieren cotejo de evidencia primaria.

### S13 — Exploración planetaria
- **Fortaleza:** complementa el universo con decisiones de contacto, ciencia, arqueología y equipos de desembarco.
- **Riesgos:** pretensión implícita de «aterrizar en cualquier planeta» con calidad UE5; assets/biomas/animación y NPC multiplicados por generación; falsas consecuencias por carga de escena.
- **Acción:** separar planetas conocidos en mapa, presencia orbital y **zonas de superficie realmente jugables**. Priorizar pocos escenarios de alta calidad y variantes procedurales controladas; continuidad Core, equipo/transportadores, condiciones ambientales y permisos.
- **Prueba:** misión de superficie limitada, retorno a nave y guardado; no generar planeta nuevo al visitar uno persistente.

### S14 — Holocubierta
- **Fortaleza:** entrenamiento y ocio potentes sin necesidad de una campaña paralela.
- **Riesgos:** objetos/personajes holográficos contaminan inventario o hechos reales; una «victoria simulada» se convierte en experiencia, ascenso o lesión arbitrarios; costes de memoria de escenarios completos.
- **Acción:** ámbito de simulación explícito, reglas de entrada/salida, permisos y objetivos de formación; recompensas profesionales solo a través de evaluaciones reales autorizadas. Reutilizar interfaces, NPC y físicas donde sea viable.
- **Prueba:** salir y recargar conserva mundo verdadero; los objetos simulados no aparecen en almacén ni registros como reales.

### S15 — Objetos e inventario
- **Fortaleza:** equipo personal, PADD, replicador y objetos del entorno pueden sostener interacción cotidiana.
- **Riesgos:** duplicar inventario Core, objetos sin propietario ni versión, replicador como fuente de cualquier equipo clasificado y costes exagerados de física para miles de elementos.
- **Acción:** ID/definición/propiedad/ubicación/permisos; replicación condicionada a patrón disponible, potencia/materia según reglas diseñadas y autorizaciones. Instanciación 3D bajo demanda; migraciones de inventario en LOAD.
- **Prueba:** replicar objeto permitido, denegar objeto restringido, transferir y guardar/cargar sin clonados.

### S16 — Vida a bordo
- **Fortaleza:** descanso, ocio, turnos, higiene, comida, amistades, salud y servicios dan sentido a habitar la Enterprise-D.
- **Riesgos:** crear «barras de necesidades» ajenas al diseño, hacer rutinas estéticas sin efecto o añadir subsistemas completos donde bastan eventos.
- **Acción:** orquestar fuentes S05/S06/S12/S15, horarios y bienestar ya documentados. Dar prioridad a actividades visibles y significativas, no a micromantenimiento. Audio personal depende de S19; localización/privacidad de S18.
- **Prueba:** un ciclo guardia→comida→descanso→interacción reacciona al tiempo y a una alerta, persiste y es jugable.

### S17 — Minijuegos
- **Fortaleza:** el ajedrez clásico con NPC y otras actividades permiten descanso y vinculación social.
- **Riesgos:** más minijuegos aislados que funciones básicas; IA externa usada para validar jugadas que un motor de reglas puede resolver sin coste.
- **Acción:** empezar con ajedrez de reglas deterministas, turnos, dificultad razonable, interrupción y reanudación; NPC puede hablar mediante S01 pero la jugada se valida localmente.
- **Prueba:** partida legal, victoria/tablas, suspensión por alerta y reanudación sin pérdida de piezas.

### S18 — Identidad, autenticación y control de accesos
- **Fortaleza:** DEC-0024 delimita adecuadamente actor verificado, residentes, invitados, permisos, revocaciones, excepciones y política de puerta.
- **Riesgos:** mezclar autenticación con la propia hoja física/animación S12; dar acceso por voz o por uniforme; bloquear evacuación; considerar las pruebas documentales como cerraduras integradas.
- **Acción:** reutilizar IDs Core/F11/propiedad de camarotes; decisión determinista de S18 y ejecución física de S12/ingeniería; privacidad proporcional; salida segura y excepciones trazadas. No crear cuentas del jugador ni otro gestor de PERSON.
- **Prueba:** puerta pública automática y privada pulsada, jugador residente, invitado caducado, NPC no autorizado, revocación, emergencia, avería física y guardado; finalmente UE5/Host/Core certificados. **Estado actual: documentación y contratos, no runtime.**

### S19 — Música / experiencia musical (alcance formal pendiente)
- **Fortaleza:** IDEA-0002 ya aprueba biblioteca **MP3/FLAC local en el MSI**, vínculo de carpetas por defecto sin duplicar, selección/cola y reproducción diegética desde el camarote. Música es importante además para la identidad del protagonista y la ambientación.
- **Riesgos:** no existe ficha oficial S19 con límite claro entre **biblioteca personal**, **música ambiental/cinemática**, **efectos** y **voces/TTS**. No suponer reproducción runtime MP3/FLAC por el mero hecho de importar recursos al editor; tampoco mezclar contenido musical privado con GitHub/API. El usuario no quiere servicios de pago adicionales ni impacto apreciable de voz sobre VRAM/FPS.
- **Acción:** registrar DEC y contratos S19 solo tras fijar nombre/alcance con el autor; reutilizar Starship Computer para órdenes y UE5 para buses/atenuación/oclusión; indexar música sin subir ficheros; volumen y mezcla con prioridad de voz/alertas; política de continuidad al salir del camarote. Mantener TTS como integración de voz independiente bajo IA/audio, preferentemente local CPU/RAM y voz estable por NPC, sin convertir la clonación de famosos en requisito.
- **Prueba:** localizar MP3/FLAC local en build empaquetada, oírla únicamente en zona correcta con puerta abierta/cerrada, pausar/continuar tras LOAD, respetar alertas, no cargar música en servidores y no degradar juego.

---

## 4. Hallazgos transversales ordenados por severidad

**P0 — Bloquean afirmar coherencia de producto; no todos bloquean seguir diseñando.**

| ID | Hallazgo verificado | Impacto | Corrección propuesta |
|---|---|---|---|
| A01 | **Desalineación documental:** ESTADO_GLOBAL.json (fecha 03-11), VISION_PRODUCTO y plan HOST v1.2 mantienen algunos textos de «nueva Clase Valhalla» y estados históricos; DEC-0020/22/23/24 son posteriores | Agentes/Codex pueden trabajar con identidad, UX y rutas antiguas | Índice de decisiones vigentes/precedencia y erratas de estado; preservar actas históricas, no reescribirlas como si nunca hubiesen existido |
| A02 | **F10/H06 frente a S04:** creador antiguo de varias especies vs protagonista único fijo | El inicio podría crear personaje incompatible con el Lore/intro | Versión v2 + migración, pruebas de nueva partida y compatibilidad |
| A03 | **Falta de bucle UE5 integrado de producto certificado** pese a múltiples pruebas nativas, laboratorios, contratos y prototipos | Imposible validar experiencia y costes reales globales | Vertical slice transversal mínimo en Enterprise-D antes de ampliar 3D/sistemas |
| A04 | **Autoridad fragmentable:** S02/08/09/10/11/12/18 y ordenador pueden crear caminos alternativos para emitir órdenes, leer conocimiento o abrir puertas | Inconsistencia, doble efecto, filtraciones de información o mutación indebida | Matriz de propietarios y única tubería intención→autorización→acción Core→evento→presentación, con idempotencia |

**P1 — Deuda importante a planificar antes de ejecución masiva.**

| ID | Hallazgo | Medida |
|---|---|---|
| A05 | IA-01: cola única sin política completa de prioridad/fairness/coste por función | Scheduling, métricas y protección contra ráfagas NPC; sin IA para funciones deterministas |
| A06 | P2 Universo Vivo: diez bloques aprobados documentalmente, runtime galáctico no certificado | Presupuesto LOD/offscreen y reconciliación temporal/guardado |
| A07 | DEC-0021 sensores refit vs patrones lentos heredados | Separar perfil clásico y refit; pruebas de informes instantáneos |
| A08 | Escenarios UE5 Sutherland/Valhalla con evidencias locales no cotejadas en repositorio | Manifestar mapa/build/hash/log/FPS y ensayos negativos, sin mover originales |
| A09 | S19 carece de contrato y nombre final de sistema | Decisión y hoja S19; no extenderlo silenciosamente a TTS |
| A10 | Voz/TTS: diálogo natural puede bloquearse por dependencia remota o consumir VRAM | Entrada manual siempre; TTS local CPU/RAM, voces estables, caché y medición |
| A11 | Política de datos compartidos e identidad: conocimiento NPC, PADD y acceso a habitaciones | Proyecciones por observador y permiso; nunca contexto global a LLM |
| A12 | Campaña muy larga vs Academia/ascensos/vida cotidiana y aceleración temporal | Una política coherente de calendario, saltos, catch-up, deadlines y escenas interrumpidas |

**P2 — Mejoras de mantenibilidad y experiencia.**

| ID | Hallazgo | Medida |
|---|---|---|
| A13 | Material antiguo habla de distribución/publicación o tres épocas seleccionables como si fuera la experiencia vigente | Anotar que el proyecto es personal y que la campaña actual usa continuidad propia; conservar historia sin extender alcance |
| A14 | Los 19 nombres no tienen una única ficha de registro y estado | Catálogo S01–S19 con propietario, contrato, fuente, dependencias, madurez y prueba; este informe puede servir de arranque |
| A15 | Minijuegos, holodeck y planetas pueden crecer sin límite | Presupuesto de contenido y umbral de valor jugable, empezar por ejemplos representativos |
| A16 | Rendimiento de 8 GB VRAM, audio y vistas 3D aún sin presupuesto verificado end-to-end | Telemetría en MSI por escenario y límites medidos antes de crear assets masivos |

**No se infieren fallos de código** de estas observaciones: son conflictos verificables de documentos, dependencias o puertas de aceptación aún abiertas. Las cifras de pruebas que aparecen en documentos históricos se respetan en su alcance original.

## 5. ¿Faltan sistemas?

**No se recomienda elevar automáticamente el catálogo de 19 a 20, 25 o 30.** La cobertura funcional es razonablemente amplia. Sí faltan o deben hacerse explícitos **servicios transversales** que sostienen a casi todos los sistemas. Son componentes compartidos, no necesariamente nuevos sistemas jugables:

| Servicio transversal | Propietario sugerido | Qué debe proporcionar | S afectados |
|---|---|---|---|
| A. Tiempo, simulación y ciclo de sesión | CoreRPG + HOST | Tiempo canónico, turnos, avance offscreen, pausa/salto, reconciliación temporal | 03, 04, 05, 06, 07, 08, 16 |
| B. Persistencia y migraciones | CoreRPG (datos), HOST (sesión), UE5 (representación) | SAVE/LOAD atomizado según contrato, versiones, reanudación, cancelación de tareas obsoletas | Todos, especialmente 03/04/12/18 |
| C. Bus de acciones/eventos e idempotencia | Core/Fxx/HOST | Una acción autorizada, un efecto, confirmación causal, entregas observables | 02, 05, 07, 08, 09, 10, 15, 18 |
| D. Identidad/conocimiento/visibilidad | Core/F11/S18 | Identidad estable, observadores, clasificación, autorización, procedencia de datos | 01, 02, 05, 06, 10, 11, 18 |
| E. Presentación unificada y accesibilidad | UE5 + S02 | LCARS, input, subtítulos, foco, mandos, idioma, feedback, alternativas a voz | Todos los sistemas visibles |
| F. Audio, voz y mezcla | UE5 audio + servicio IA y alcance S19 | Música, SFX, voces NPC, prioridades de alerta, TTS local, control espacial y latencia | 01, 02, 05, 07, 12, 16, 19 |
| G. Observabilidad, QA y rendimiento | F15 + HOST/UE5 | Telemetría CPU/GPU/RAM/VRAM, repros, suites, evidencias por versión, no regresiones | Todos |
| H. Pipeline de recursos/escenas | NAP/Blender + UE5 | Identidad de asset, fuente, importación, colisiones, LOD, presupuestos de escena | 11, 12, 13, 14, 17 |
| I. Orquestación de incidencias operativas | Core + reglas Trek/F05 | Alertas, daños, prioridad de servicios, evacuaciones, escalado institucional | 05, 07, 09, 10, 12, 16, 18 |

**Único posible hueco de catálogo que merece decisión posterior:** si el autor considera **sonido/voz** una experiencia sistémica autónoma —y no un servicio transversal y/o parte de S19—, habrá que discutirlo con él. No se asigna el número 20 unilateralmente. Igualmente, Ordenador de la Nave debe ser servicio común de S02/S01 y operaciones, no un segundo gestor de IA; F11 no se reconstruye en HOST; Director Narrativo pertenece a S07 y no a otro universo.

## 6. Matriz de integración: una sola fuente de verdad

| Flujo | Entrada | Decide | Ejecuta/persiste | Presenta |
|---|---|---|---|---|
| Abrir camarote | Pulsador S12, voz/LCARS S02 | S18 evalúa identidad y permiso; seguridad física comprueba puerta | Core/acciones de puerta; HOST coordina | UE5 hoja, timbre, feedback |
| Consulta de sensores | Consola/voz S02 | Sensor S10 con hechos Core y perfil tecnológico DEC-0021 | Core registra observación/conocimiento | LCARS, holograma S11, voz opcional |
| Ruta estelar | S11/S02 | Navegación S08 + cadena de mando | Core ejecuta movimiento | UE5 y cartografía S11 |
| Conversación NPC | Interacción S02 | Conocimiento y relación Core/S05/S06, autoridad social; IA redacta | Eventos válidos Core; HOST media IA | Voz/subtítulos/animación UE5 |
| Ascenso | F11/órgano competente | F11 conforme a evidencia y reglas | Core registra grado y acto | HOST transmite; escena S07/UE5 |
| Música privada | Orden S02 o reproductor S19 | Permiso de espacio S18 + biblioteca local | Reproductor local; efectos de ocio por S16/Core cuando proceda | UE5 audio espacial |
| Evento galáctico | S03/Planificación 2 | Simulación causal Core + reglas Trek | Core persistente | Conocimiento, noticias/misiones S07 |

**Regla de diseño común:** no llamar al modelo para decidir hechos físicos, rangos, permisos, identidad, autorizar rutas, detectar objetos o simular el universo. La IA puede traducir instrucciones, resumir y dialogar con un contexto filtrado; la respuesta nunca acredita por sí sola un hecho.

## 7. Priorización propuesta: primer corte realmente jugable

Esta priorización es **propuesta de auditoría**, no sustitución automática de F00–F15 ni HOST H00–H13.

**Puerta G0 — Reconciliación documental (ChatGPT + revisión autoral).**
1. Mantener índice de decisiones vigentes DEC-0020–0024 y señalización de páginas maestras con referencias históricas obsoletas.
2. Publicar registro S01–S19 con responsables, referencias y dependencias sin marcarlo «implementado».
3. Formalizar límites S19 cuando el autor quiera discutir música/sonido; no bloquear el núcleo del juego.

**Puerta G1 — Fuente autoritativa y HOST (Codex + auditoría ChatGPT).**
1. Completar/migrar S04 F10/H06 a protagonista fijo v2.
2. Integrar el servicio IA común con consumidores concretos sin vías paralelas, con límites y cancelación.
3. Encauzar todas las acciones desde interfaz a verificaciones Core/Fxx/S18.
4. Integrar guardado/reanudación y evolución offscreen acotada; aplicar conocimiento por actor.

**Puerta G2 — Corte de nave habitable UE5 (Codex + recursos/validación).**
1. Un tramo representativo de Enterprise-D: camarote, corredor, puerta pública, puerta privada, turboascensor, puesto de trabajo y un NPC.
2. Un ciclo completo de servicio: dirigirse a su puesto → consultar sensores ordinarios → comunicar/registrar resultado → regresar y realizar una actividad de ocio → SAVE/LOAD.
3. Identidad S18, ruta S12, S02, S05, S10, S16; IA disponible para conversación no imprescindible para puerta/escaneo; datos no falseados.
4. Medir frametime, RAM, VRAM, latencia, colisiones y tiempos de carga en MSI; repetir tras reiniciar.

**Puerta G3 — Extensión selectiva.** Integrar S08/S09/S11 y módulos procedurales S03, después planetas, holocubierta y minijuegos según necesidad. La Astrometría puede empezar por geometrías esquemáticas verificables y crecer artísticamente sin reescribir Core. S19 biblioteca musical puede validarse como funcionalidad aislada sin bloquear el corte G2.

**Gates de cierre:** un contrato válido no certifica código; una prueba C++ no certifica UE5; una escena Blender no certifica navegación; CI sin telemetría no certifica rendimiento; un resultado de laboratorio comunicado no es evidencia local auditada.

## 8. Pruebas transversales de aceptación propuestas

| ID | Escenario | Sistemas | Resultado obligatorio |
|---|---|---|---|
| E2E-01 | Inicio de partida 2383 con protagonista fijo | 01/02/04 | Perfil de origen aprobado, cosmética permitida, ningún selector de especie |
| E2E-02 | Cadete que pregunta, obedece y no tiene mando | 02/04/05/08 | Diálogo coherente, orden de nave sin autoridad denegada |
| E2E-03 | Puerta privada con NPC invitado, expiración y rescate | 02/12/18 | Permiso y estado físico separados, sin suplantación |
| E2E-04 | Guardia y relevo con dos NPC autónomos | 03/05/06/16 | Ubicación, turno, memoria y acceso coherentes |
| E2E-05 | Contacto espacial ordinario Enterprise-D refit | 02/09/10/11 | Informe íntegro rápido, sin IA ni demora artificial |
| E2E-06 | Ruta S11 propuesta por un subordinado | 08/11/18 | Visualiza y propone, nunca mueve sin mando competente |
| E2E-07 | Emergencia que interrumpe ocio/conversación | 01/05/07/12/16/19 | Prioridades de audio/servicio; sin perder datos |
| E2E-08 | Salida de Holocubierta con objetos simulados | 14/15 | Ninguna entidad simulada contamina World State |
| E2E-09 | Avanzar varios meses fuera de escena y cargar | 03/04/05/06/07 | Continuidad causal, identidad estable, duplicados cero |
| E2E-10 | Biblioteca musical MP3/FLAC local | 02/16/19 | Reproducción real espacial en build, sin subidas ni copia forzosa |
| E2E-11 | API no disponible al conversar/consultar | 01/02/05 | Diagnóstico, no bloqueo Game Thread; acciones básicas siguen disponibles |
| E2E-12 | Recorrido/escena en MSI 2560×1600 | 02/11/12 | FPS/frametime/VRAM medidos, UI legible, reinicio y SAVE/LOAD |

Todos los escenarios están **propuestos**, no ejecutados ni certificados por esta auditoría. El equipo objetivo y niveles de rendimiento deben medirse, no declararse alcanzados de antemano.

## 9. Registro de decisiones pendientes, sin inventar aprobación

- **DECISION_AUTOR_S19:** ratificar nombre y alcance exacto del 19 (biblioteca musical, banda sonora contextual, mezcla u otros). Hasta entonces solo IDEA-0002 y el acuerdo de música son vinculantes en sus términos conocidos.
- **DECISION_AUTOR_RITMO:** concretar en una prueba jugable cuánto se comprimen los cuatro cursos de Academia, sin alterar la cronología aprobada ni convertirlos en otras campañas obligatorias.
- **DECISION_AUTOR_ACEPTACION:** aceptar qué tramo UE5 representa la experiencia mínima suficiente de la Enterprise-D antes de ampliar interiores.
- **DECISION_TECNICA_IA:** determinar prioridades de cola, límites monetarios, degradación y gestión de voz/TTS **sin** añadir proveedores de pago, VRAM significativa ni clonación obligatoria.
- **DECISION_TECNICA_P2:** establecer presupuesto y reconciliación determinista de la simulación offscreen con calendario de juego.
- **DECISION_TECNICA_EVIDENCIAS:** recuperar en el MSI los artefactos F07/Sutherland sin sobrescribir ni mover originales y cotejar pruebas antiguas.

Este informe **no autoriza** implementar por Codex un nuevo sistema, cambiar canon o migrar contratos LOCKED por sí solo. Los cambios de código requieren sus fases, versiones y validaciones correspondientes.

## 10. Documentos contrastados y precedencia

**Fuentes prioritarias recientes:**
- [Índice de decisiones autorales](../decisions/README.md), especialmente DEC-0020/21/22/23/24.
- [DEC-0020 Enterprise-D / Proyecto Valhalla](../decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md).
- [DEC-0021 Superioridad de sensores y reputación](../decisions/enterprise_d_valhalla_superioridad_sensores_reputacion_2026-11-17.md).
- [DEC-0022 Protagonista único](../decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md).
- [DEC-0023 Astrometría 360°](../decisions/s11_astrometria_360_2026-11-18.md) y [plan S11](../roadmap/S11_ASTROMETRIA_360_PLAN_2026-11-18.md).
- [DEC-0024 Accesos](../decisions/s18_identidad_autenticacion_control_accesos_2026-11-18.md) y [plan S18](../roadmap/S18_IDENTIDAD_ACCESOS_PLAN_2026-11-18.md).
- [IA central HOST IA-01](../../../sistemas/ai/HOST_AI_SERVICE_IA01.md) y [decisión OpenAI](../../../sistemas/ai/OPENAI_RUNTIME_DECISION_2026-11-15.md).
- [Transición S04 F10/H06](../architecture/host/H06_S04_TRANSICION_PROTAGONISTA_FIJO_2026-11-17.md).
- [IDEA-0002 biblioteca musical personal](../../ideas/IDEA-0002_biblioteca_musical_personal.md).

**Fuentes de arquitectura y estado, con cautela cronológica:**
- [Criterios de cierre](../roadmap/master/CRITERIOS_DE_CIERRE.md).
- [Estado global F00–F15](../roadmap/master/ESTADO_GLOBAL.json) **fechado 03-11-2026; no representa por sí solo decisiones del 17/18 de noviembre**.
- [Visión de producto v0.1](../vision/VISION_PRODUCTO_RPG_3D_v0.1.md) **contiene conceptos históricos superados**.
- [HOST — Plan H00–H13](../architecture/host/PLAN_MAESTRO_HOST_v1.2_2026-11-11.md), cuya introducción registra un estado de 11-11 y debe leerse con informes posteriores.
- [Planificación 2 — índice](../roadmap/README.md) y [runtime procedural](../roadmap/procedural_runtime_readiness_v0.1.md), histórico: bloques documentales no son galaxia en UE5.
- [F07 evidencia MSI Sutherland](../roadmap/master/fases/F07/RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md).
- [Starship Computer](../../../sistemas/gameplay/ship_operations/ship_computer/README.md).
- [S18 README y contratos](../../../sistemas/gameplay/access_control/README.md).
- [S11 README y contratos](../../../sistemas/gameplay/astrometrics/README.md).
- [Reglas AGENTS.md](../../../AGENTS.md): los laboratorios son temporales/no versionados; este es un **informe definitivo**, por eso reside dentro de proyecto/docs/auditorias, nunca en laboratorios.

## 11. Conclusión ejecutiva

**No hay un defecto de concepto que obligue a desechar ninguno de los 19 sistemas.** La planificación corre mayor riesgo por **sobreextensión, documentación desfasada, falta de pruebas integradas y duplicación entre Core/Fxx/HOST/UE5** que por ausencia de nuevas familias funcionales.

**Orden recomendado:** reconciliar documentación; completar S04 y la acción/autoridad común; certificar un circuito jugable de Enterprise-D con NPC, puertas, sensores y SAVE/LOAD; medir presupuesto de simulación/audio/IA; crecer por utilidad jugable. S11 y S18 disponen ya de diseños concretos y deben integrarse sin saltarse las pruebas. S19 necesita su ficha oficial antes de declararlo cerrado en diseño.

**Cierre de esta auditoría:** DOCUMENTACIÓN AUDITADA. **No** certifica 19 sistemas implementados, no fusiona planes por sí misma, no altera Lore/CoreRPG y no declara nuevas decisiones aprobadas.
