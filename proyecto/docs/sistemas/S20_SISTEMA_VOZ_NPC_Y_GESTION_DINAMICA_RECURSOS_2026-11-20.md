# S20 — Sistema de Voz de NPC y gestión dinámica de recursos

**Decisión autoral:** 20-11-2026. **Estado:** IDEA APROBADA / ESPECIFICACIÓN CONCEPTUAL INICIAL. **No implementado; sin motor TTS elegido, cifras de memoria medidas, contrato de integración ni certificación UE5.8.2.**

**Propósito:** permitir conversaciones con **voz dinámica generada por IA** para NPC seleccionados de *Star Trek Legends*, preservando prioritariamente la calidad gráfica y la fluidez de Unreal Engine en el MSI (RTX 4070 portátil, **8 GB de VRAM**, i9-14900HX, 32 GB de RAM). S20 investigará y, cuando existan mediciones reales, coordinará una política **reversible y medible de presupuestos de recursos** entre la representación gráfica y la síntesis de voz, con alternativas por **GPU o CPU**. No se autoriza aquí una compra, un motor concreto, un sacrificio gráfico permanente ni una implementación inmediata.

## 1. Decisión creativa y objetivo obligatorio

- **Voces especiales**: ciertos personajes de gran importancia narrativa podrán tener diálogos dinámicos hablados, preferentemente con una interpretación vocal diferenciada y convincente. **Picard, Janeway y Siete** son ejemplos de presencias puntuales; **Riker** podría aparecer más a menudo dada su relación con la Enterprise-D. Son preferencias de diseño y ejemplos de perfiles, no una obligación de cargar todos sus modelos a la vez.
- **Resto de NPC**: deben disponer de una alternativa más ligera, con voces compartidas o perfiles diferenciados adecuados, síntesis por CPU cuando resulte eficaz, audio preparado para frases recurrentes y subtítulos. No ejecutar por defecto inferencia GPU costosa por cada conversación trivial.
- **Voz dinámica** significa que un texto autorizado puede transformarse en habla durante el juego. No significa generar en el momento la realidad del universo, las acciones, los permisos o el conocimiento de un NPC.
- **Prioridad del autor:** conseguir las dos cosas —**calidad gráfica alta y diálogos hablados naturales**— mediante medición, streaming, ajustes selectivos, TTS apropiado, DLSS/TSR cuando aporte valor y CPU cuando convenga. No imponer de antemano reducir la calidad de un juego AAA ni prohibir GPU: **probar todas las opciones** y elegir en función del escenario.
- **Coste adicional objetivo: 0 € para TTS** mediante opciones locales/gratuitas si ofrecen calidad suficiente, sin cuotas, compras o dependencias de un servicio remoto impuestas. Evaluar voces especiales caso por caso; **la clonación exacta de actores es hipotética, no requisito de aprobación**.

**Restricción de recursos de partida:** los 8 GB físicos de VRAM son un límite del equipo, **no una reserva disponible para TTS**. La hipótesis de que determinadas escenas consuman 6–8 GB para gráficos se comprobará con perfiles reales; no se deduce de ella ninguna cantidad libre garantizada.

## 2. Fronteras con los sistemas existentes (no duplicar autoridades)

| Componente | Responsabilidad vigente | Relación con S20 |
|---|---|---|
| **CoreRPG / reglas Trek** | Identidad, conocimiento, estado, acciones, permisos, tiempo y consecuencias | Proporciona contexto verdadero/permitido y valida eventos; S20 nunca lo modifica por lo que diga una voz. |
| **S01 y HOST IA-01** | Acceso central a modelos de lenguaje, generación/interpretación de texto, sesiones y encaminamiento; sin segunda API por NPC | S20 **consume texto ya autorizado** y puede solicitar a HOST la coordinación de trabajos TTS, sin crear otro cerebro conversacional ni un acceso paralelo a OpenAI. |
| **S05 / S06 / S02** | NPC, agendas y presencia; relaciones; interacción/conversación y LCARS | Proporcionan actor, proximidad, intención legítima, sesión, interlocutor y prioridades narrativas. |
| **S19 — audio, música y ambientación** | Mezcla, reproducción, atenuación, espacialización, subtítulos, prioridades sonoras y voz en UE5 | **S19 sigue siendo el propietario de la reproducción**. S20 prepara/solicita síntesis, gestiona su presupuesto computacional y entrega audio y metadatos a S19. |
| **Unreal Engine 5.8.2** | Render, streaming real de texturas y niveles, GPU/RHI, recursos gráficos, audio y Game Thread | **Único ejecutor de las decisiones sobre recursos del motor**. S20 formula una política y propone acciones verificables; HOST no descarga texturas de Unreal directamente. |
| **F14 / F15 y rendimiento** | Contenidos audiovisuales, instrumentación y pruebas cuando toque | S20 propone ensayos específicos y criterios; no afirma pruebas ya realizadas ni abre una nueva planificación ejecutiva. |

**Flujo conceptual:** proximidad/intención → propuesta de perfil de voz y presupuesto S20 → texto autorizado S01/HOST/Core → TTS local elegido → audio/subtítulo a S19/UE5 → liberación o recuperación *progresiva* de recursos opcionales según políticas del motor. La voz no es credencial ni fuente de hechos.

## 3. Alternativas de TTS a estudiar (sin selección anticipada)

| Candidato o modalidad | Hipótesis / motivo de estudio | Pendiente de medir |
|---|---|---|
| **Piper** (escritura correcta; también citado informalmente como «Pipper») | TTS local ligero, candidato preferente para CPU y perfiles sencillos | Naturalidad en castellano, voces concretas, tiempo hasta primera muestra, uso de RAM/CPU, disponibilidad de variantes GPU y licencias de voces. |
| **Kokoro** | Candidato de mejor expresividad/calidad potencial; estudiar CPU y GPU según implementación | Naturalidad y pronunciación, latencia de CPU frente a GPU, RAM/VRAM real, inicialización y concurrencia. |
| **Otros TTS locales gratuitos y compatibles** | Posibles mejoras de calidad y latencia con modelos ligeros o medianos | Descargas, licencias, dependencias, idioma, memoria, coste real por voz y estabilidad. |
| **TTS por CPU** | Preservar VRAM del render y reducir interferencias GPU | CPU ocupada por CoreRPG/HOST/UE5, latencia de síntesis, picos de RAM y repercusión en frametime. |
| **TTS por GPU** | Mejor latencia/calidad en algunos modelos y situaciones | Memoria realmente reservada/residente, contexto CUDA/ONNX, VRAM temporal y persistente, transferencia, contención de GPU y riesgo de caída de FPS. |
| **Voz pregrabada / caché local de frases** | Respuestas habituales, emergencias y textos recurrentes con coste de inferencia reducido | Tamaño de caché, variantes, invalidación por cambio de texto/voz, política de privacidad y coherencia de diálogo. |

**Ningún modelo tiene prioridad contractual sobre otro.** En particular, **no se presume** que Piper use la RTX o que Kokoro deba usar GPU. Elegir **por NPC/escenario** tras medición, con la opción de reducir complejidad del TTS o cambiar a CPU antes de afectar elementos visibles importantes.

## 4. Gestión dinámica de VRAM, texturas y cargas gráficas

**Principio esencial:** S20 **NO** promete «vaciar la RTX», liberar X GB ni mover libremente VRAM a RAM a voluntad. Distingue VRAM verdaderamente liberable, memoria reservada/cacheada por UE/driver, memoria de recursos gráficos necesarios y memoria de inferencia. Una optimización se acepta **solo si se demuestra** reducción real de presión de memoria, sin artefactos visuales ni tirones perceptibles.

**Opciones técnicas que deberán estudiarse, combinadas cuando proceda:**

1. **Medición de base y margen de seguridad.** Perfilar escenas (puente, camarotes, Ten Forward, NPC próximos, interiores complejos, Holocubierta y superficies planetarias), además de transición de cámaras y conversaciones. Medir memoria GPU total/ocupada, textura streaming pool, render targets, Nanite/Lumen y modelo TTS cargado. No fijar ahora límites numéricos o presupuestos por suposición.
2. **Texture Streaming de UE5.** Evaluar mips menores **solo para texturas realmente no visibles o de baja prioridad**, grupos apropiados y presupuesto del streaming pool; no descargar el rostro, pelo, uniforme, consola o entorno **visible** del interlocutor. Liberar mips no equivale a recuperar automáticamente toda la memoria, y cambiar el tamaño del pool puede degradar la imagen.
3. **Asset Manager, carga asíncrona y streaming de niveles/World Partition cuando proceda.** Descargar/dejar de mantener recursos **no necesarios** de zonas distantes, ocultas o explícitamente abandonadas, respetando referencias vivas, dependencias y políticas de carga. No asumir que todo escenario del juego utiliza World Partition ni forzar unload de assets aún referenciados.
4. **Preparación anticipada y restauración suave.** La proximidad al NPC y la intención real de iniciar diálogo pueden disparar una *evaluación preventiva* y precalentamiento de TTS. Antes de iniciar cambios gráficos comprobar visibilidad, distancia, memoria disponible y coste estimado. Al terminar y alejarse: liberar el modelo TTS GPU si realmente conviene y **precargar/recuperar progresivamente** texturas y recursos que vuelvan a ser necesarios. Evitar ciclos repetitivos con márgenes/histéresis y tiempos de espera parametrizables.
5. **Escalado selectivo, no sustituto de liberar memoria.** Estudiar DLSS/TSR, resolución interna y calidad de efectos concretos **solo si las mediciones los justifican**. Mejorar FPS no garantiza liberar VRAM; la generación de fotogramas tampoco es una reserva gratuita de memoria. No recortar permanentemente calidad sin aprobación.
6. **Escalonamiento de trabajos.** No iniciar a la vez carga de texturas pesadas, streaming de nivel y preparación de un modelo TTS GPU si eso provoca picos. Evitar operaciones de sincronización/IO en Game Thread; priorizar audio perceptible y coherencia audiovisual.

**Prohibiciones de diseño:** no modificar texturas originales ni sus copias maestras para esta política; no ejecutar comandos masivos arbitrarios de descarga; no interrumpir una conversación para recolectar VRAM; no liberar mallas/recursos de la escena que el jugador necesita; no suponer que cerrar un diálogo recupera automáticamente todo el consumo GPU del motor TTS.

Documentación de referencia para la fase técnica:
- [UE5.8 — Texture Streaming](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-in-unreal-engine)
- [UE5.8 — Texture Streaming Configuration](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-configuration-in-unreal-engine)
- [UE5.8 — World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine)

## 5. Máquina conceptual de decisión (no API ni implementación)

1. **NORMAL:** juego prioriza recursos de render. NPC corrientes usan voz ligera/CPU o contenido de bajo coste si está habilitado; S19 gestiona sonido.
2. **PREDICCIÓN DE DIÁLOGO:** ante proximidad, interacción o escena narrativa legítima, identificar voz requerida y medir presupuesto actual; **la mera cercanía no obliga a sacrificar gráficos**.
3. **ELEGIR RUTA:** si TTS GPU cabe con margen certificado, puede utilizarse; si no, probar TTS por CPU; si tampoco cumple calidad/latencia, usar voz ya preparada o subtítulos sin bloquear la partida. No dar una respuesta IA inventada por fallo TTS.
4. **PREPARAR:** opcionalmente reducir recursos gráficos no visibles mediante UE5 y precalentar voz de forma asíncrona; iniciar conversación cuando haya resultado utilizable.
5. **DURANTE EL DIÁLOGO:** vigilar VRAM, CPU, RAM, frametime y colas; no cambiar voz a mitad de frase ni degradar abruptamente al interlocutor visible. Limitar conversaciones sintéticas concurrentes y respetar alertas/prioridades S19.
6. **SALIDA:** cancelar tareas obsoletas, decidir si descargar motor TTS GPU o mantenerlo temporalmente para evitar recargas, restaurar/precargar calidad visual cuando corresponda, sin picos ni oscilaciones.

Todo umbral, temporización y prioridad será **configurable y se elegirá tras pruebas**, con opción de desactivar por completo la política de «ceder VRAM a voz» cuando no aporte beneficios medidos.

## 6. Calidad, continuidad y fallos seguros

- Una voz distinguible por personaje debe mantener timbre coherente durante la conversación; las voces exactas de intérpretes conocidos **no son condición**.
- Español natural, pronunciación de nombres de Star Trek, latencia razonable, entonación, ausencia de cortes y correcta sincronización con animación facial son criterios de calidad futura.
- El sistema de voz **no debe ocultar el texto**: subtítulos en castellano siempre disponibles y texto de respuesta conservado si el TTS falla; S19 controla mezcla y prioridad ante alarmas.
- Evitar llamadas nuevas a modelos de lenguaje para sintetizar/animar una misma frase. Solo consumir texto autorizado por S01/HOST.
- Sin introducción de facturación TTS externa por defecto; no exponer secretos, transcripciones privadas ni voz en logs.
- Cambios de escena, LOAD, cambio de NPC o cancelación invalidan síntesis pendiente; no reproducir una frase atrasada en otra conversación.
- **La VRAM no es la única restricción**: una ruta CPU que degrade el Game Thread o retrase las respuestas también puede ser inaceptable.

## 7. Investigación y validación futuras obligatorias

**Fase conceptual, sin comprometer fases Fxx/Hxx nuevas:**

1. **Perfil gráfico real:** medir UE5.8.2 con y sin modelos de NPC en distintos escenarios representativos del MSI, en build comparable a la jugable. Identificar la memoria realmente recuperable sin merma visible.
2. **Ensayos TTS aislados:** Piper, Kokoro y otros candidatos locales; CPU vs GPU, variantes de voz en castellano, latencia de inicio y audio, RAM y VRAM en reposo y en inferencia.
3. **Ensayos conjuntos:** gráficos UE5 + conversaciones NPC (modelo generado por S01/HOST cuando proceda) + TTS, con y sin streaming/mips y con distintos perfiles de escalado. Medir comportamiento en transiciones y carga de otros recursos.
4. **Decisión técnica documentada:** elegir política de rutas para NPC especiales y normales, condiciones de preparación/restauración y valores de protección a partir de evidencia. Permitir que la respuesta correcta sea **CPU por defecto sin tocar texturas**.
5. **Piloto E2E y pruebas de regresión:** dos NPC (normal y destacado) en un escenario pesado; conversación en español, calidad facial, subtítulos, retorno de calidad gráfica y SAVE/LOAD. Registrar p50/p95 de latencia de voz y frametime, FPS, picos de VRAM/RAM/CPU, hitching, colas, degradación de texturas y rehidratación tras alejamiento.
6. **Pruebas negativas:** saturación de VRAM, ausencia de motor TTS, voz que tarda, interrupción por emergencia, cambio brusco de nivel, dos NPC conversando, cancelación y falta de Internet si otra parte del diálogo depende de API. El videojuego continúa coherente; no bloquea Game Thread, no provoca OOM ni reproduce audios obsoletos.

**Criterio de aceptación futura:** voces útiles y creíbles con impacto medido y tolerable, estabilidad de FPS, ausencia de degradación gráfica ostensible, presupuestos respetados, recuperación gradual y fallback verificable. **No existe objetivo numérico de FPS, ms de TTS o MB libres aprobado aún**: se fijará después de perfilar el juego.

## 8. Estado, precedencia y trazabilidad

- **Nueva aprobación posterior** al catálogo de S01–S19 formalizado el 19-11-2026; el alcance de aquel acta sigue siendo histórico. S20 **no renumera ni sustituye S01, S05, S19, HOST IA-01 ni F14/F15**.
- **APROBADO:** necesidad de sistema específico de voz de NPC con gestión inteligente del consumo GPU/VRAM, estudio de descarga/precarga segura de texturas en conversaciones, TTS ligeros y opciones CPU/GPU; prioridad de calidad gráfica + voz.
- **NO APROBADO NI HECHO:** proveedor concreto, voces clonadas específicas, umbrales, selección de tecnología, implementación, pruebas RTX, integración con HOST/CoreRPG/UE5, cambios reales de textura o decisiones de reducir calidad.
- **Próximas reconciliaciones cuando se desarrolle:** S01 IA, S05 NPC, S19 audio, planificación HOST y F15 rendimiento. No cambiar esas fichas históricas ni dar por finalizado el sistema desde esta definición.

**Fuente autoral:** acuerdo del 20-11-2026 y conversación previa «Diálogos!» sobre voz dinámica y VRAM. **Naturaleza de la entrega:** documento de diseño, no certificación técnica.
