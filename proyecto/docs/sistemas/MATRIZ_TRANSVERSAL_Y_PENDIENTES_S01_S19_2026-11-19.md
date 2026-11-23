# S01–S19 — matriz transversal de autoridades, servicios y asuntos pendientes

**Fecha:** 19-11-2026 · **Ámbito de modificación:** SISTEMAS exclusivamente. Deriva de [auditoría S01–S19](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md). Las propuestas que exceden SISTEMAS **no modifican ni replanifican** Lore, HOST, Planificación 1 ni Planificación 2.

## 1. Contrato conceptual de autoridad común

**Una acción jugable no se convierte en hecho por aparecer en pantalla, ser pronunciada o ser sugerida por IA.**

Secuencia conceptual única: **interacción/solicitud identificada → intención canónica → identidad y autorización del dominio competente → resolución de reglas/estado CoreRPG y Trek/Fxx → evento confirmado/persistencia → representación UE5 + sonido S19**. HOST transporta, coordina, cancela y mantiene sesión; no se convierte en árbitro paralelo de reglas. La estructura técnica exacta se definirá después, no se fija ninguna API nueva en este documento.

| Responsabilidad | Fuente o propietario, sin duplicados | No hacer |
|---|---|---|
| Identidad persistente, tiempo y WorldState | CoreRPG y sus reglas de estado; instituciones Star Trek/F11 para rango y permisos derivados | Falsificar dato desde UI, LLM, HOST o escena UE5 |
| Interpretación de voz/texto e interfaz | S02/Starship Computer, S01 a través de HOST solo si la frase lo exige | Usar voz como credencial o invocar API por cada botón |
| Autoridad de entrada a habitación/zona | S18 con evidencia Core/F11/propiedad, reglas Trek de seguridad | Darla a S12/Blueprints de proximidad o al ordenador |
| Estado mecánico, colisión y recorrido | S12 + sistema de ingeniería y UE5 | Abrir puerta averiada porque permiso = ALLOW |
| Hechos de sensores y conocimiento | CoreRPG + perfil real S10/Ciencia, observador con procedencia | Generar sensores desde LLM ni mostrar todo el WorldState |
| Visualización astrográfica | S11 en UE5 sobre proyección autorizada | Recalcular/executar rutas ni mantener segunda galaxia |
| Navegación y ejecución | S08 + autoridad de cadena de mando/Fxx | Mover nave por click en S11 sin orden real |
| Combate/táctica y daño | S09/Fxx/Core, con permisos/ROE y estado de armas | Dar invulnerabilidad permanente al refit |
| Universo distante y cambios de sociedad | S03/Planificación 2 bajo Core, presupuestos de simulación | Hacer que S07 invente hechos |
| Selección/presentación de historias | S07 sobre causas Core y órdenes auténticas | Convertir guion en autoridad de hechos |
| NPC, agendas y presencia | S05 bajo Core y estados de actividad | Duplicar localizaciones y relaciones S06 |
| Relaciones, memoria y consentimiento | S06 con eventos verificables Core | Generar consentimiento/memoria privada por relato IA |
| Objetos e inventario | S15 sobre IDs, propiedad y reglas Core | Duplicar inventario o crear bienes sin permiso |
| Vida cotidiana y ocio | S16 coordina oportunidades y bienestar | Programar sus propios motores de juego, audio o vínculos |
| Minijuegos | S17 valida reglas especializadas y resultados | Enviar cada jugada a IA, duplicar S16 |
| Audio, voces y música | S19 coordina; motor de audio UE5 reproduce | Dar a cada sistema su propio reproductor; reproducir música pobre por obligación |

## 2. Handoffs funcionales que deben permanecer coherentes

| Flujo | Productor/intención | Validación y decisión | Resultado verdadero y representación |
|---|---|---|---|
| Camarote de jugador/NPC | Pulsador físico S12 o petición S02 | Identidad Core y política determinista S18; estado mecánico S12 | Core evento; UE5 abre o timbra, S19 SFX correcto |
| Pasillo público | Detección UE5 S12 | Política de paso + estado físico, S18 si hay restricción | Abre sin decisión falsa de residencia; rutas NPC |
| Comando «a mi camarote» | Starship Computer/S02 | Identidad, asignación y localización; seguridad en ascensor y habitación | S12 lleva a parada más próxima y **resto a pie** |
| Consulta sensor refit | Consola manual o vigilancia automática S02/S10 | Core verdad/perfil DEC-0021, alcance observable y conocimiento | Informe completo rápido; S11 puede representarlo |
| Ruta dibujada en S11 | Interacción 3D/LCARS S11 | S08 navegación + cadena de mando | Core mueve solo con orden; S11 refleja resultado |
| Disparo de nave | S02/táctico S09 | Autoridad Fxx/F11, sensores/estado de armamento | Core resuelve, S19 SFX, UE5 representación |
| Diálogo privado | NPC/jugador S05/S06/S02 | Contexto conocido y permisos; HOST IA-01 solo si se necesita lenguaje | Core registra hechos verdaderos, S19 voz o subtítulos |
| Ascenso | F11/órgano legítimo | F11/Core según reglas y evidencia | Core nuevo grado; S07/UE5 ceremonia posterior |
| Evento en galaxia distante | S03/Planificación 2 bajo Core | Reglas causales y observador; agendas/reconciliación | Core historia persistente, S07 misión posible, S11 datos filtrados |
| Música privada | S16/S02, orden manual o frase | Biblioteca local y permisos S18 cuando proceda | S19/UE5 reproducen en emisor del camarote, no suben audio |
| Partida de mus/póquer | S16 propone mesa, NPC disponibles | S17 reglas, nivel y decisión de bots sin LLM | Resultado legítimo persistente, UE5 animación de mesa |
| Holocubierta | S14/S16 y autorización S18 | Reglas de programa, ámbito simulado delimitado | UE5 experiencia, sin objetos reales creados automáticamente |

**No establecer ahora nombres de API, mensajes, clases o números de puerto nuevos:** únicamente las responsabilidades y la forma de validar futuras integraciones.

## 3. Servicios compartidos que cubren carencias sin S20

| Servicio transversal | Propiedad a verificar en su futura auditoría | Reutilizado por |
|---|---|---|
| Tiempo canónico, saltos y simulación de fondo | Core + HOST sesión; P2 para reglas offscreen | S03/04/05/06/07/08/16 |
| SAVE/LOAD, versiones y migración | Core persistencia + HOST coordinación + UE5 rehidratación visual | S01–S19 según alcance |
| Acciones, eventos, idempotencia | Core/Fxx y HOST transporte | S02/05/07/08/09/10/12/15/18/19 |
| Identidad, observación y privacidad | Core/F11 + S18 + reglas de conocimiento | S01/02/05/06/10/11/15/18 |
| UI accesible en castellano | S02 + UE5 | Todos los sistemas visibles |
| Voces y mezcla comunes | S19/UE5; S01/HOST texto e interpretación | S01/02/05/07/12/16/19 |
| Evidencia y rendimiento | F15 + mediciones UE5/HOST/Core | Todos, según consumo real |
| Pipeline de recursos y escenas | NAP/Blender/UE5 bajo F14 y fases pertinentes | S11/12/13/14/15/17/19 |
| Incidencias y emergencias | Core y reglas Fxx con dueños institucionales | S05/07/09/10/12/16/18/19 |

Son **capacidades compartidas, no nuevos sistemas conceptuales aprobados**. No asignar su implementación a esta revisión.

## 4. Duplicidades o fronteras resueltas en el catálogo

1. **S01 no reimplementa HOST IA-01**: S01 define función consumida, HOST gestiona acceso único; sensores, rangos, puertas y turnos se resuelven con lógica determinista.
2. **S02 no manda por interpretar una frase**: todos los orígenes convergen en una intención, identidad, autoridad y evento.
3. **S03 produce causas; S07 selecciona y presenta historias**: una misión no crea acontecimientos galácticos por conveniencia.
4. **S04 define el protagonista actual y su experiencia; F10/F11 mantienen autoridad**: la selección histórica de especies no es UX vigente, y su migración técnica queda pendiente en otra auditoría.
5. **S05 NPC y S06 relaciones**: agenda y acción por un lado; vínculos/memoria/consentimiento por otro.
6. **S08 navega, S10 observa y S11 muestra/proyecta**: no tres universos ni tres motores de ruta. S09 consume sensores.
7. **S12 abre/mueve físicamente; S18 identifica y autoriza**: un permiso no certifica viabilidad física; botón privado ≠ puerta pública automática.
8. **S13 superficie real frente a S14 escenario holográfico**: separar efectos, objetos y consecuencias persistentes.
9. **S15 objetos, S16 actividades, S17 reglas de juegos**: comer/replicar vs ocio vs motor de ajedrez/mus sin duplicación.
10. **S19 mezcla/reproduce, S01 habla/interpreta, F14 produce archivos**: biblioteca de música privada S16/IDEA-0002 usa S19 como reproducción, no constituye un segundo motor de audio.

## 5. Avisos a los otros cuatro pilares — registrar, NO ejecutar aquí

| Pilar / auditoría independiente | Aviso concreto identificado | Estado desde SISTEMAS |
|---|---|---|
| **Planificación 1** | F10/H06 código/editor anterior frente a protagonista fijo DEC-0022; F04/06/07 y sensores S10 refit; evidencia UE5 real y requisitos de vertical slice/guardado, F14 recursos S19 | **PENDIENTE DE AUDITORÍA PROPIA. Sin cambios** |
| **Planificación 2** | B01–B10 documentados no son runtime galáctico; reconciliación offscreen, calendario y presupuesto CPU/RAM/escala | **PENDIENTE DE AUDITORÍA PROPIA. Sin cambios** |
| **LORE** | Vigencia DEC-0020 Enterprise-D Proyecto Valhalla, Academy 2383–2387, genealogía Khan, NPC legendarios, desviación de continuidad y hechos aún sin fijar | **PENDIENTE DE AUDITORÍA PROPIA. Sin cambios** |
| **HOST** | Servicio IA-01 compartido: consumos, prioridades, fallback, cancelación, TTS y seguridad; H06 v2, canal de intención/autoridad/eventos, F11 sin duplicación, SAVE/LOAD | **PENDIENTE DE AUDITORÍA PROPIA. Sin cambios** |

**Sin modificar desde SISTEMAS:** VISION_PRODUCTO histórica, ESTADO_GLOBAL fechado, plan H00–H13, B01–B10 P2, archivos de LORE, contratos LOCKED, código, pruebas CI, binarios, escenas y geometrías.

## 6. Aprobación autoral todavía necesaria

Lo siguiente **no se decide silenciosamente** por recomendaciones de la auditoría:

- Ritmo jugable de los cuatro años de Academia: duración real de escenas/cursos, saltos, actividades obligatorias y presentación compacta sin cambiar el 2383–2387 aprobado.
- Selección final del primer **tramo de Enterprise-D** que represente una experiencia mínima satisfactoria. Un corte camarote–pasillo–ascensor–consola es **propuesta de auditoría**, no nuevo mandato de Fxx.
- Detalles familiares pendientes del protagonista Khan (nombres, genealogía fina, fecha/lugar de nacimiento), trama final de intro, circunstancias precisas de llegada al mando.
- Configuración final de cubierta/ubicación de Astrometría y áreas no fijadas; conexiones físicas no se inventarán.
- Modalidad definitiva y reglas de mesa de póquer, variantes de damas/mus y elección de motores: conservar catálogo inicial S17; pocha/tute son futuras posibilidades.
- Selección/calidad de material musical de S19, transiciones, política exacta de pausas ante alertas; **nunca autorizar música mediocre**.
- Cualquier innovación sustantiva de habilidades, políticas de consentimiento, disponibilidad real de tecnologías refit o historia de Borg que altere lo aprobado.

Estos puntos no bloquean **formalizar el concepto**; necesitan participación del autor cuando se aborde el sistema responsable.

## 7. Criterio común de madurez y certificación futura

**Idea aprobada ≠ especificación técnica ≠ contrato disponible ≠ código parcial ≠ integración UE5 ≠ aceptación certificada.**

Pruebas conceptuales propuestas por la auditoría (E2E-01 a E2E-12): partida de origen fijo, cadete sin mando, puertas privadas, turnos NPC, escaneo inmediato, ruta S11 sin movimiento, emergencia interrumpiendo ocio, holocubierta sin contaminación, salto temporal, audio personal local, API no disponible y rendimiento real en MSI. **Ninguna se ha ejecutado desde esta revisión.**

El procedimiento definitivo de las pruebas y sus criterios técnicos se reserva a cada fase del sistema y [CRITERIOS_DE_CIERRE](../roadmap/master/CRITERIOS_DE_CIERRE.md); no se establecen nuevos gates de Fxx/Hxx aquí.
