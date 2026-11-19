# S19 — Audio, música y ambientación dinámica

**Aprobación autoral:** 19-11-2026 · **Estado:** CONCEPTO APROBADO / FICHA FORMALIZADA / COORDINADOR GENERAL SIN RUNTIME CERTIFICADO.

**Fuente:** [auditoría de sistemas](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md), acuerdos expresos del autor en esta conversación y [IDEA-0002](../../ideas/IDEA-0002_biblioteca_musical_personal.md).

## 1. Visión y norma de calidad

El juego necesita **efectos** (puertas, LCARS, transportadores, fásers, torpedos, alertas, warp, impactos), **ambientes** (naves, cubiertas, planetas, holocubiertas), **voces** (tripulación, ordenador, mensajes prioritarios) y una **mezcla** que los haga inteligibles y espacialmente coherentes.

La música ambiental, de exploración, tensión, combate o escenas emotivas es **opcional y queda sujeta a resultado artístico y técnico excelente**. El autor aprobó expresamente: **si la música queda mal, no se introduce**. Se puede disponer de un magnífico conjunto de efectos y ambientes sin llenar la experiencia de música mediocre. **Silencio deliberado es un resultado correcto.**

S19 **no compone música ni proporciona assets**: gestiona cuándo se oyen, dónde, su prioridad, transiciones, pausa y detención. La producción de recursos audiovisuales es tarea separada de F14, sin modificar F14 en esta revisión.

## 2. Funciones que sí pertenecen a S19

### Efectos confirmados por la realidad del juego

- Evento de puerta que **realmente se abre** → sonido de hoja/mecanismo ubicado en la puerta, según diseño y estado físico.
- Disparo realmente autorizado y ejecutado → SFX de arma/torpedo según posición y contexto; solicitud de disparo denegada **no** suena como disparo.
- Acción de consola/ordenador, teletransportador, alarma, motores, avería e impacto → variantes y duración que correspondan.
- Evitar repetir el mismo efecto al reenviar una intención o recibir notificaciones duplicadas; respetar concurrencia y prioridades.

### Ambientes 3D

Capas ambientales por escena y ubicación: zumbido de nave, ventilación, Ingeniería, Ten Forward, camarotes, corredores, bosque, océano, lluvia, fauna y programas holográficos. Atenuación, oclusión por puertas, diferencia entre ubicaciones y mezcla según situación y presencia. **S19 no genera zonas planetarias**, solo representa acústicamente zonas reales o simuladas ya existentes.

### Voz, locuciones y comunicación

- Voces del ordenador, NPC, comunicaciones, avisos y alarmas. Bajar música/ambientes mientras habla alguien de forma importante; subtítulos y alternativa textual cuando falte TTS.
- La **IA central S01 vía HOST** genera o interpreta lenguaje cuando haga falta; S19/UE5 gestiona reproducción y síntesis sonora. TTS no concede permisos ni crea hechos.
- Preferencia aprobada: TTS gratuito local preferentemente en CPU/RAM, voces genéricas estables apropiadas para cada NPC, sin facturas añadidas ni degradación significativa de FPS/VRAM; clonación de voces de actores **no obligatoria**.
- No imponer transcripción ni micrófono para operar sistemas deterministas.

### Música de fondo contextual, si suena bien

Podrá reaccionar a calma, exploración, contacto desconocido, peligro, combate, ceremonia y escenas emotivas **solo desde acontecimientos verdaderos y contextos válidos**. Transiciones suaves, control de interrupciones, prioridad a conversación/alerta y posibilidad de música nula. **No se aprueba ningún repertorio concreto ni implantación musical obligatoria** por el mero hecho de aprobar S19.

### Música privada de camarote y piano

- [IDEA-0002](../../ideas/IDEA-0002_biblioteca_musical_personal.md): MP3/FLAC desde **archivos y carpetas locales del MSI**, **vincular carpeta como opción predeterminada** sin duplicar archivos, copia local solo a petición del usuario; controles manuales y ordenador; reproducción **diegética** en el camarote, no sonido que siga al avatar.
- Importación desde USB es una posible fuente local; Spotify o servicios comerciales **no forman parte del requisito básico**, solo investigación futura si el autor la pide y resulta viable.
- Rutas/índices y audio privados no suben a GitHub, OpenAI, Firebase ni nube. Reproducción MP3/FLAC seleccionada durante juego exige comprobar **decodificación runtime y build empaquetada**, no basta con importación del editor.
- S16 define la actividad y escena de piano en Ten Forward: personaje sentado, gesto y grabación musical apropiada, sin animación individual de dedos ni simulador de teclado completo. S19 gestiona el sonido.

## 3. Reparto inequívoco de responsabilidades

| Acontecimiento | Quién decide que ocurrió | Qué hace S19 | Quién reproduce |
|---|---|---|---|
| Apertura de puerta | S18 autoriza, S12/ingeniería verifica posibilidad y Core registra estado | Selecciona SFX/ubicación/volumen | UE5 |
| Disparo de fáser o torpedo | S09/Fxx/Core validan y resuelven | Efecto de disparo e impacto contextual | UE5 |
| Alerta auténtica | Operaciones/estado Core | Prioriza sirena, voz y mezcla | UE5 |
| Cambio de cubierta | S12/Core | Ambientes locales y oclusión | UE5 |
| Conversación o mensaje de la nave | S05/S02 y texto autorizado S01/HOST cuando proceda | Voz, subtítulos, ducking, fallback | UE5 |
| Orden válida de reproducción privada | S02 + preferencias locales y permisos S18 si proceden | Reproducir/pausar/cambiar en emisor local | UE5/runtime local |
| Cambio de situación narrativa | S03/S07/S09/Core | Posible música de calidad o silencio | UE5 |

**Flujo conceptual común:** evento confirmado → contexto acústico y prioridades → resolución S19 → reproducción, atenuación o silencio por UE5. No otra base de hechos, sistema de IA ni bus de eventos paralelo.

## 4. Herramientas y límites

Unreal Engine proporciona mezclador, submixes, atenuación, espacialización, oclusión y posibilidades de MetaSounds/Audio Modulation y control de simultaneidad. **Reutilizarlas**, no crear un motor de audio alternativo.

No deben solaparse indebidamente alarmas críticas con voz, ni una biblioteca privada debe revelar rutas personales. La solución debe conservar FPS, RAM y VRAM razonables en el MSI, pero la compatibilidad real y las cifras **se medirán más adelante**, no se prometerán por documento.

## 5. Criterios futuros de comprobación, no pruebas ejecutadas

1. Una puerta pública abre y reproduce su efecto espacial; una apertura denegada no finge ejecución.
2. Una alerta interrumpe ocio sin perder diálogo, reanudando niveles adecuadamente.
3. Dos emisores en puntos diferentes respetan distancia, puerta y cambios de cubierta.
4. MP3/FLAC local se reproduce en build real sin subidas, con error comprensible ante archivo ausente.
5. TTS, si se incorpora, mantiene voz estable y no compromete la experiencia ni obliga pagos externos.
6. Música de fondo **solo si la calidad artística y técnica está a la altura**; su aplazamiento **no invalida** SFX/ambientes de calidad.

## 6. Estado de evidencia

Las carpetas audiovisuales del repositorio están **reservadas**: audiovisual/audio/sfx/, ambience/, music/, voice/, manifests/ y audiovisual/presentation/audio_direction/. Su presencia no demuestra assets ni un coordinador funcional. F14 contempla producción audiovisual, pero **no se ha auditado ni modificado desde SISTEMAS**. IDEA-0002 es diseño de biblioteca personal, **no una aplicación MP3/FLAC ya validada en UE5**.

**Resultado de esta entrega:** S19 formalizado como sistema conceptual; **sin creación de canciones, SFX, plugins, cambios de Unreal, HOST, Lore o Planificación 1/2**.
