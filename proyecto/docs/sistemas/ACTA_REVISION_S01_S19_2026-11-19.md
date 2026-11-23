# Acta — revisión y formalización posterior a auditoría de Sistemas S01–S19

**Fecha:** 19 de noviembre de 2026. **Auditoría de partida:** [AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md), PR #172 fusionada. **Objeto:** dejar definiciones y relaciones coherentes para futura construcción por sistema; no certificar ni implementar ahora.

**Alcance efectivamente modificado:** únicamente archivos Markdown nuevos en proyecto/docs/sistemas/. **No se han alterado** contratos históricos, código, binarios, Unreal, recursos 3D, Lore, F00–F15, Planificación 2, HOST H00–H13 ni documentos originales de decisiones. No se ha encomendado tarea a Codex.

## 1. Resultado y sistemas correctamente planteados

La auditoría **mantiene los 19 sistemas**, sin propuesta de S20, pues cubren adecuadamente el conjunto de funciones. Conservados en intención original, sin rediseño creativo: **S02** interacción LCARS/3D/voz; **S05** NPC; **S06** relaciones; **S07** misiones; **S08** vuelo; **S09** combate; **S13** escenarios planetarios limitados de calidad; **S14** ocio holográfico; **S15** equipamiento/objetos; **S16** vida a bordo; **S17** minijuegos (ajedrez, damas, póquer y mus iniciales). Sus límites y dependencias estaban insuficientemente explicitados en un registro único y ahora sí lo están.

S18 ya disponía de buen diseño de autorización y contratos: **no se han reemplazado**; solo se consolidó su frontera con S12. S11 también tenía diseño sólido: se ha aclarado su carácter de vista/propuesta y su falta de runtime.

## 2. Modificaciones documentales con motivo

| Sistemas | Cambio documental realizado | Por qué |
|---|---|---|
| **S01** | Consumidores del servicio OpenAI único HOST; contexto filtrado; sin IA para hechos deterministas; prioridad, consumo, cancelación y fallback como necesidades futuras | A04/A05: evitar segundo servicio, latencia/coste y autoridad falsa |
| **S02** | Una intención común para control 3D/LCARS/PADD/texto/voz, sin doble ejecución; controles sin micrófono | A04/A11: impedir bypass de permisos y duplicados |
| **S03** | Separar escalas visible/región/offscreen, causalidad y reconciliación del calendario sin declarar simulación completa | A06/A12: no confundir B01–B10 documentados con galaxia runtime |
| **S04** | Nueva partida con protagonista fijo DEC-0022; F10/F11 mantienen autoridad; antigua creación libre es histórica | A01/A02: resolver contradictorio editor F10/H06 sin tocarlo |
| **S05/S06** | Agenda/identidad vs vínculos/memoria/consentimiento y LOD NPC; conocimiento por observador | A04/A11: evitar duplicados, omnisciencia y coste IA |
| **S07/S08/S09** | Director narrativo no crea hechos; S08 ejecuta navegación autorizada; combate consume sensores/órdenes y respeta disuasión real | A04/A15: no duplicar S03/S11 ni forzar crisis/combates |
| **S10** | Doctrina de sensores avanzados DEC-0021, informe ordinario único y muy rápido del refit operativo, excepciones justificadas | A07: eliminar patrones lentos de UX objetivo sin alterar prototipos históricos |
| **S11** | Vista holográfica de cuatro escalas, lectura de Core/conocimiento, no segundo mapa, no warp al proponer ruta, límites de LOD/VRAM | A04/A16: autoridad y rendimiento; estado solo diseño |
| **S12** | Geolocalización, puertas públicas automáticas y privadas manuales con S18; ascensor hasta parada viable y luego caminar; conexión virtual del puente de batalla | A04/A08: evitar acceso por trigger, corredor ficticio o maqueta confundida con UE5 |
| **S18** | Responsable solo de identidad/autenticación/política; S12 controla mecanismo y posibles bloqueos físicos; sin biometría real obligatoria ni cuenta extra | A04/A11: una identidad Core, permisos privados y excepciones trazables |
| **S13–S17** | Delimitar alcance, valor realmente jugable, reutilización de recursos y rechazo de minijuegos/campañas de meses | A15/A16: controlar sobreextensión y presupuesto Codex/VRAM |
| **S19** | Ficha completa de SFX, ambientes, voces, audio espacial, mezcla, música condicional y biblioteca MP3/FLAC privada | A09/A10: faltaba formalización; respetar calidad y ausencia de pagos/VRAM TTS |
| **Todos** | Registro único con evidencia y límites, servicios compartidos y handoff independiente a otros pilares | A01/A03/A04/A14: evitar documentación dispersa y «diseño = implementado» |

## 3. Cobertura de los 16 hallazgos A01–A16

**Interpretación:** «resuelto documentalmente» significa que el catálogo sabe cómo debe comportarse y a quién corresponde; **no** significa que la incidencia esté corregida en un ejecutable.

| Hallazgo | Tratamiento desde SISTEMAS | ¿Queda pendiente trabajo en otros pilares o runtime? |
|---|---|---|
| A01 — Catálogo y documentos desactualizados | Registro nuevo y precedencia DEC-0020–0024 | **Sí**. Documentos históricos externos se reconcilian en su ámbito |
| A02 — Protagonista fijo vs creador antiguo | S04 vigente explicitado, migración versionada sin sobrescribir | **Sí**, F10/HOST y pruebas de nueva partida |
| A03 — Falta bucle UE5 certificado | Se distingue idea, prueba parcial y aceptación; ejemplo vertical slice solo sugerido | **Sí**, Planificación 1/UE5/Core/HOST |
| A04 — Autoridad fragmentable | Matriz intención→permiso→estado Core→presentación y dueños claros | **Sí**, conectores y pruebas reales |
| A05 — IA-01 priorización/coste | S01 define necesidad de límites, cancelación, fallback y no-LLM simple | **Sí**, auditoría HOST/configuración/consumo |
| A06 — P2 no runtime completo | S03 con LOD/offscreen y cautela de madurez | **Sí**, auditoría Planificación 2 |
| A07 — Sensores refit vs flujos lentos | S10 recoge DEC-0021 y excepcionalidad legítima | **Sí**, F06/implementación/refit operativo |
| A08 — Evidencias 3D no contrastadas | S12/S11 no confunden mallas/reporte con UE5 validado | **Sí**, MSI/Planificación 1 |
| A09 — S19 sin ficha | **Resuelto documentalmente:** ficha S19 y dependencia S16/IDEA-0002 | **Sí**, implementación UE5 cuando toque |
| A10 — Voz/TTS costosa o invasiva | S01/S19 delimitan TTS local/gratuito/ligero y fallback | **Sí**, pruebas técnicas futuras |
| A11 — Identidad/conocimiento/visibilidad | S18, S06, S10/S11 y tabla de autoridad conectados | **Sí**, autorización por observador/seguridad |
| A12 — Calendario y saltos | S03/S04/S05/S16 exigen coherencia temporal | **Sí**, P2/Planificación 1/HOST y decisión de ritmo |
| A13 — Publicación/eras históricas | Campaña personal y continuidad vigente declaradas; historia conservada | **Sí**, revisión de documentos externos |
| A14 — No había catálogo/estado único | **Resuelto documentalmente:** índice y 19 fichas | **Sí**, actualizar evidencias al implementar |
| A15 — Alcance excesivo mini/holo/planetas | S13/S14/S17 y regla calidad>cantidad delimitadas | **Sí**, decisiones concretas en su fase |
| A16 — Rendimiento no medido | Expresión clara de que no hay presupuesto certificado; requisitos de medición | **Sí**, UE5/MSI/F15 cuando se ejecute |

## 4. Carencias resueltas conceptualmente, sin crear sistema nuevo

- **Tiempo y reanudación**, **identidad y visibilidad por observador**, **eventos idempotentes**, **persistencia y migración**, **UI y control alternativo**, **audio y voz comunes**, **observabilidad/rendimiento** y **recursos 3D** quedan explícitos como servicios compartidos con propietario en la [matriz transversal](MATRIZ_TRANSVERSAL_Y_PENDIENTES_S01_S19_2026-11-19.md). No se duplica Core, HOST, S18, S19 ni se suma un S20.
- Resuelto documentalmente el vacío de **S19** aprobado en conversación sin ficha en main. Conservar la diferencia entre banda sonora opcional, sonido de un objeto en escena, SFX funcional y narración por TTS.
- Se protege el requisito de **no consumir cuota de Codex excesiva por un minijuego** y de **no sacrificar calidad artística**.
- El catálogo ahora distingue la responsabilidad de cada sistema de la producción de contenido y del runtime que aún falta.

## 5. Estado real y pruebas no realizadas

Esta revisión se ha efectuado leyendo la auditoría y documentación del repositorio; **no se ejecutaron compilaciones, CI, UE5, pruebas en MSI, scripts, modelos IA ni consultas de red externas del videojuego**. La lectura de repositorio sí acredita que existen documentos y contratos, no que funcionen.

**Conclusión de madurez:** S01 muestra implementación parcial de su servicio HOST; S04 contiene código histórico para creador anterior, pero diseño nuevo todavía por migrar; S11/S18 tienen diseños y contratos claros con flags explícitos sin runtime; S03 posee B01–B10 documentados pero no simulación completa certificada; S12 contiene propuestas y material gráfico/no certificación; S19 es concepto con ficha, sin runtime general. Los demás tienen conceptos, documentos y contratos de distinta madurez. **Ningún S01–S19 ha recibido aquí estado «integración certificada»**.

## 6. No decisiones nuevas y pendientes de autor

Mantener sin nuevas decisiones automáticas: ritmo jugable de cuatro cursos de Academia, primer corte UE5 representativo, genealogía familiar y detalles del personaje, localización detallada de Astrometría, modalidad/variantes finales de minijuegos, implantación musical concreta (solo si alcanza calidad), fechas y capacidades finales de la Enterprise-D y otros asuntos creativos de Lore. En la matriz figuran también los avisos para las auditorías individuales de Planificación 1, Planificación 2, Lore y HOST.

**No hay sistema nuevo propuesto. Los números S01–S19 y las elecciones creativas aprobadas se mantienen.**

## 7. Entregables de esta revisión

- [Índice de sistemas y precedencia](README.md)
- [Fichas S01–S10](FICHAS_S01_S10_FORMALIZADAS_2026-11-19.md)
- [Fichas S11–S19](FICHAS_S11_S19_FORMALIZADAS_2026-11-19.md)
- [Matriz transversal de autoridades y dependencias](MATRIZ_TRANSVERSAL_Y_PENDIENTES_S01_S19_2026-11-19.md)
- [Ficha completa S19](S19_AUDIO_MUSICA_AMBIENTACION_DINAMICA_2026-11-19.md)

**Cierre documental solicitado:** catálogo listo como referencia para desarrollo **individual futuro**, sin afirmar implementación y sin intervención de Codex en esta tarea.
