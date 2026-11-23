# Planificación 2 — Bloque 8: Crisis sistémicas y consecuencias a escala galáctica

**Fecha:** 12-11-2026 · **Objetivo de madurez:** REFERENCE_COMPLETE · **Alcance:** arquitectura específica Star Trek, contratos, caso sintético determinista y pruebas adversariales. **Sin modificación de CoreRPG, HOST, F11, F06, UE5 ni activos visuales.**

## Propósito y experiencia

Un universo vivo puede sufrir sucesos sin relación con el jugador. Una perturbación subespacial previamente aceptada puede degradar comunicaciones; esa degradación ejerce presión sobre redes comerciales, abastecimiento médico o servicios de una colonia. Un accidente ambiental posterior puede agravar el contexto. Instituciones, NPC, la Flota y autoridades locales toman decisiones propias. Algunas crisis son locales; una crisis galáctica exige una red *realmente conectada*, no una regla de dramatismo. La Enterprise NCC-1701-D puede llegar, recibir noticias tarde o no visitar nunca los sistemas afectados.

Un informe de riesgos no equivale al daño real ni a un encargo de misión. Las necesidades surgidas de consecuencias **realmente aceptadas** podrán alimentar posteriormente B09; nunca se inventará un desastre para ofrecer una misión.

## Referencias auditadas

- Contrato previo de disrupciones: sistemas/universe/generation/network_disruption_crisis_contract.json; no se sustituye.
- B01 y B02 son dueños de civilizaciones, asentamientos, población, derechos, fronteras y movimientos reales.
- B03 conserva guerra, escalada militar y decisiones de combate. La guerra ya existente puede generar un choque B08, pero B08 no declara guerras.
- B04 conserva producción, stock, consumo, flujos, energía y transporte efectivos; B08 no escribe inventarios.
- B05 conserva historia; B06 investigación, hipótesis, cura o tecnología; B07 fenómenos, origen físico y sensorización.
- F11/HOST gobiernan poderes de mando y sesiones. CoreRPG será el único escritor del WorldState y dueño del reloj, eventos y guardado.
- B09 será dueño de misiones emergentes; B10 será dueño de programación galáctica/offscreen. UE5, IA y PADD leen proyecciones autorizadas.

## 20 paquetes cerrables

| ID | Decisión | Evidencia exigida |
|---|---|---|
| CR001 | Un único escritor autoritativo | Simulador no muta fuentes externas |
| CR002 | Respeto al canon y corte de partida | No sobrescribe reserva ni pasado |
| CR003 | Origen causal aceptado | Nunca nace de distancia a jugador |
| CR004 | Identidad por campaña y causa | Sin reroll ni ID de otra campaña |
| CR005 | Redes y dependencias preexistentes | Sin rutas o nodos inventados |
| CR006 | Propagación acotada interregional | Replay estable y ciclos seguros |
| CR007 | Crisis compuestas | Dos choques acreditados sin doble contabilizar víctimas |
| CR008 | Activa, contenida, resuelta | Estados con verificaciones |
| CR009 | Riesgos de comercio/energía/sanidad | No consumos ni stocks ficticios |
| CR010 | Presión ecológica/poblacional | Sin cifras de migración arbitrarias |
| CR011 | Instituciones y diplomacia | Sin cambio político automático |
| CR012 | Mitigación y reconstrucción | Permisos y hechos acreditados |
| CR013 | Primera Directriz y soberanía | Excepción explícita en mundo prewarp |
| CR014 | Informes y conocimiento parcial | Destinatario, tiempo y confidencialidad |
| CR015 | Frontera con B09 | Ninguna misión generada |
| CR016 | Excepciones Omega/temporales | Sin hechos extraordinarios de azar |
| CR017 | Event log, idempotencia, hash | Rechazo atómico y cronología |
| CR018 | Fixture y tests adversariales | CI + regresiones B01–B08/F13 |
| CR019 | Puertas de runtime | Sin atribuir integración a CoreRPG |
| CR020 | Acta, manifiesto, fusión | B09 como siguiente bloque |

## Modelo de referencia

1. **Choque:** un hecho ya aceptado tiene campaña, momento causal, red existente, tipo y severidad cuantificada en puntos básicos. La etiqueta accepted del fixture no sustituye verificación CoreRPG.
2. **Dependencias:** cada red preexistente tiene una región, un peso de criticidad y dependencias declaradas. El simulador determina exposición directa como el mayor choque de una red menos las mitigaciones ya aceptadas; nunca inventa capacidad física adicional.
3. **Cascada:** cada dependencia transmite como máximo la fracción fijada del estrés de la red precedente; se aplica el máximo y truncamiento entero. Los ciclos no amplifican más del 100 %. Ningún dato de jugador, cámara o LOD interviene.
4. **Consecuencias:** la presión por región es un indicador de riesgo, no la cifra de heridos, muertos, residentes evacuados, camas, créditos, pérdida de energía o daño de casco. Estos cambios exigirán eventos de sus propietarios de Core.
5. **Extensión:** un radio de alcance no se fija artificialmente. Una red conectada puede transportar presión a distintos sectores y un segundo choque aceptado puede superponer efectos; las crisis mal comunicadas se conocen sólo cuando llega cada informe.
6. **Mitigación:** una intervención necesita un hecho concreto de mitigación y otra autorización válida para esa misma crisis, actor, región y alcance. En un mundo prewarp se exige además revisión explícita y aprobada de Primera Directriz. La IA no se otorga permisos.
7. **Contención:** parte aceptado y presión regional residual inferior a 2.500 bps, umbral exclusivamente del modelo de prueba, no canon. La crisis sigue existiendo.
8. **Resolución:** parte acreditado de recuperación, contención previa y ausencia de estrés de red pendiente. No se declara resuelta por dejar de mirar la pantalla o cerrar la misión.
9. **Comunicación:** emisor y destinatario concretos, clasificación public/restricted/classified y llegada causal. Los NPC, el ordenador y el PADD no obtienen la verdad global ni noticias futuras.

## Escenario de aceptación no canónico

Campaña ficticia demo-2383. Un choque subespacial externo afecta a Orion Reach. La colonia Lyra depende de esa red; los servicios médicos de Beltran dependen de Lyra y una región prewarp presenta una dependencia indirecta. Ninguna interferencia con esa cultura se ejecuta. Un segundo choque ambiental, también documentado, empeora el expediente. Una agencia con autorización independiente aplica medidas, contiene la presión y más tarde certifica recuperación completa. El capitán recibe **dos versiones diferentes** del expediente con retrasos; un observador sin notificación no adquiere información.

Se prueban colisiones con canon, hechos futuros/no aceptados, etiquetas de campaña ajena, cambios retroactivos, manipulación del historial, permisos insuficientes, emergencia prewarp sin excepción, filtraciones de información, ciclos de red, mitigaciones duplicadas y cierres prematuros.

## Salidas definitivas y responsabilidad

- Contrato JSON de B08 en sistemas/universe/generation/systemic_crises_galactic_consequences_reference_contract_v0.1.json.
- Evaluador Python offline y batería de tests en desarrollo/tools/generation/.
- Fixture no canónico en desarrollo/validation/fixtures/systemic_crises/.
- Workflow .github/workflows/p2-b08-systemic-crises.yml.
- Estado y acta en proyecto/docs/roadmap/.
- Actualización del plan de 10 bloques, plan maestro, F13, índice y CONTENT_STATUS.

Los datos temporales de pruebas se generan únicamente por GitHub Actions o laboratorios desechables según AGENTS.md, nunca se añaden al historial del repositorio como assets permanentes. Los ficheros anteriores sí constituyen contratos y pruebas permanentes.

## Puerta y límite de cierre

REFERENCE_COMPLETE exige CI del último HEAD verde, pruebas propias, regresiones B01–B08 y F13, verificación documental y fusión segura. Se mantendrán F13 PLANIFICADA y CoreRPG/HOST/UE5 pendientes de ejecución real. Si todas las puertas se superan, **Bloque 9 — Misiones emergentes derivadas del estado del universo** será el siguiente habilitado.
