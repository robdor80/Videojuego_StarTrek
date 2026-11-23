# LORE-05E — Exploración científica y primer contacto
**13/11/2026 · Año de partida 2383 · Documento de diseño narrativo, no simulación.**

## 1. Una galaxia que existe antes de mirarla
Se reutilizan `exploration_progress_model.json`, `astrographic_knowledge_state.json`, contratos de generación de civilizaciones, observación y P2. **Existencia ≠ detección ≠ clasificación ≠ cartografía ≠ visita ≠ estudio completo ≠ publicación.** La observación puede ser errónea, parcial o quedarse anticuada. No se asignan coordenadas, rutas, peligros, masas ni nuevos descubrimientos desde LORE-05E.

Un oficial científico podría comprobar señales incoherentes, pedir un segundo barrido, investigar vida a partir de lecturas incompletas, contrastar hipótesis y elevar un informe. Ninguna maniobra implica recursos infinitos, éxito seguro o presencia garantizada de vida inteligente. Los logros no se convierten automáticamente en ascensos; pueden quedar como propuestas para el expediente de servicio si CoreRPG y F11 los aceptan.

## 2. Flujo narrativo de descubrimiento
1. **Observación causal:** una entidad preexistente o generada de acuerdo con los contratos del universo produce firmas observables reales.
2. **Registro de indicio:** identificación provisional, instrumento, observador, contexto, marca temporal, confianza y fuente; no elevar una sospecha a certeza.
3. **Hipótesis:** Ciencia puede proponer explicaciones rivales, con datos favorables, en contra y preguntas no resueltas.
4. **Comprobación:** nuevos análisis, sondas o visita **solo si** están disponibles, ordenados, autorizados y físicamente posibles.
5. **Dictamen limitado:** ficha actualizada con lo verificado; la IA no revela propiedades inaccesibles en el estado del mundo.
6. **Difusión y uso:** publicaciones, transmisión a Flota, cartas revisadas o consejos de ruta únicamente a destinatarios permitidos, según latencia, clasificación y conocimiento.
7. **Revisión futura:** evidencias nuevas o cambios de peligros y fronteras pueden invalidar cartas antiguas sin borrar la historia.

Este flujo no suplanta F06 Sensores, navegación, P2-B06 ciencia, B07 anomalías/arqueología, B09 misiones emergentes o B10 evolución offscreen.

## 3. Primer contacto ≠ primer avistamiento
Los contratos existentes ya ordenan detección, estudio previo, Primera Directriz, preparación, decisión de mando, aproximación, identificación mutua, diálogo y cierre. Mantener los estados observador-relativos de `civilization_contact_status_model_v0.1.json`. No saltar de `suspected` a `public_contact` por proximidad ni de `formal_first_contact` a relaciones diplomáticas plenas por un saludo exitoso.

**Evaluación obligatoria:** tecnología y grado de conciencia extraterrestre, autonomía y soberanía, riesgo de contaminación, consentimiento, calidad de traducción, autoridad real del interlocutor, seguridad y cauces de mando. La Primera Directriz es una norma de no injerencia, no un interruptor automático «prewarp = nunca hablar». Si existe exposición previa o contacto inevitable, los responsables valoran el caso y asumen consecuencias; la IA no inventa excepciones.

**Derecho a decir no:** la civilización puede rechazar, posponer o restringir el contacto. Un científico local o capitán de nave puede representar solo a sí mismo, no necesariamente a su planeta. Flota Estelar no impone ciudadanía, tratados, bases ni comercio.

## 4. Escenarios ilustrativos de juego
**La biosfera silenciosa.** Un planeta exhibe posibles señales biológicas. Los sensores no demuestran inteligencia; investigar su ecosistema no autoriza manipularlo ni atribuir recursos explotables.

**La interferencia extraña.** Una señal parece artificial, pero su firma es ambigua. Se conserva como hipótesis hasta obtener nuevas observaciones. El jugador puede preferir prudencia, cambio de estrategia o intervención del especialista.

**El mensaje antes del saludo.** Una cultura desconocida emite una advertencia. Se comprende parte de su vocabulario, pero no la petición concreta. La tripulación puede equivocarse de buena fe; la resolución requiere intercambio plausible, no una traducción milagrosa.

**El representante equivocado.** Contactamos con una nave exploradora de otra civilización. Su oficial al mando puede aceptar conversación naval; eso no significa consentimiento gubernamental para establecer una base.

**La revelación accidental.** Una patrulla provoca que una comunidad no conocedora de vida extraterrestre vea tecnología de la Flota. El incidente debe registrarse y evaluarse; borrarlo del diario o asumir que los testigos olvidan todo está prohibido.

**Los datos caducados.** Una ruta señalada como segura en un informe antiguo puede haber cambiado por eventos de P2. El conocimiento del PADD se presenta con fecha y grado de actualización, no como omnisciencia cartográfica.

## 5. Interfaz de exploración y archivos
El mapa, las consolas y el PADD distinguen: «sin datos», «indicios», «catalogado», «cartografiado», «estudiado», «verificado» y «dato antiguo» cuando el contrato de progreso lo permite. Los estados reales son los definidos en el JSON propietario, no una máquina de estados nueva creada aquí. El jugador puede consultar historia de análisis y versiones de una hipótesis. La observación local del capitán no concede acceso a todos los informes clasificados de la Flota.

**Enterprise-D:** esta documentación sirve a cualquier destino del jugador. La NCC-1701-D sigue siendo Galaxy bajo Proyecto Valhalla durante la Academia iniciada en 2383; no se sitúa automáticamente en misión de exploración ni entra en servicio solo por llegar a 2387.

## 6. Hitos de futura integración, no trabajo completado
- F06/Sensores: evidencia observable, trazabilidad de lecturas, controles in-world.
- CoreRPG/WorldState: escritor único de descubrimientos, decisiones y consecuencias.
- HOST: consultas y traslado de decisiones, sin algoritmos duplicados del CoreRPG ni órdenes propias contra F11.
- P2-B06/B07/B09/B10: ciencia, fenómenos, necesidades emergentes y evolución causal preexistentes, con frontera de referencia offline.
- UE5/PADD: información contextual es-ES filtrada por conocimiento y permisos, sin mostrar secretos por exportación externa.
- LORE-05C/D: reaprovechar lugares y entidades con sus IDs, sin añadir NPC legendarios; LORE-05B sigue cerrado en doce.

## Fuentes y límites
`SCREEN_CANON`: TNG «First Contact», TNG «Who Watches the Watchers», TNG «Darmok». `OFFICIAL_REFERENCE` auxiliar: https://www.startrek.com/news/first-contacts-across-star-trek ; https://www.startrek.com/news/pre-warp-impersonations-prime-directive . `INFERRED`: despiece narrativo del proceso de exploración. `GAME_ADDITION`: recomendaciones de presentación y escenas hipotéticas, sin contratos de runtime. No elevar artículos divulgativos a hechos de pantalla ni construir un tratado universal basado en un único episodio.
