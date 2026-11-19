# R5 — Corrección de contratos de identidad, autoridad y compatibilidad
**19-11-2026 · Remediación documental de Planificación 1, NO implementación F10/F11/F04**

Prevalencia de decisiones ya aprobadas:
- [DEC-0020 — Enterprise-D / Proyecto Valhalla](../../decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md).
- [DEC-0022 — protagonista fijo](../../architecture/host/H06_S04_TRANSICION_PROTAGONISTA_FIJO_2026-11-17.md) y sus contratos S04.
- [F11 — plan de carrera vigente](fases/F11/PLAN_F11_ACTUALIZADO_2026-11-11.md).

## 1. Identidad de nave y límites de migración

| Concepto | Referencia histórica compatible | Decisión vigente / fuente de verdad | Prohibición |
|---|---|---|---|
| Clase anterior `valhalla` | Plantillas F04, catálogos y guardados históricos pueden conservar este ID | **No es** clase de la nave final; conservar identificador legacy hasta migración explícita | Reetiquetar en masa todo `valhalla` como `galaxy` |
| Nave objetivo individual | Antigua primera «Valhalla», propuesta como nueva clase | **USS Enterprise NCC-1701-D**, clase **Galaxy**, identidad individual persistente; Proyecto Valhalla es su programa de reconstrucción | Crear una segunda nave Enterprise-D o dar a la clase histórica su identidad |
| Dotación | Plantilla histórica 1.800 Flota + 400 civiles | **No hay censo definitivo aprobado** para la Enterprise-D reconstruida | Importar 2.200 personas automáticamente |
| Capacidades | Propuestas de refit / Odyssey / flujo cuántico / nave auxiliar | Cada capacidad necesita instalación concreta, reglas, evidencias y disponibilidad temporal | Heredar todas las prestaciones por alias |
| Cronología | Fixture Sutherland **2372** válido para regresión | **2383** inicio Academia; programa de reconstrucción desde 2380, objetivo narrativo 2387 **no garantizado como hecho runtime** | Introducir Enterprise-D reconstruida plenamente operativa en 2383 |
| Acceso | Nave deseada y capitanía futura | Destino/plaza/órdenes válidas F11; incluso tras graduación no hay asignación automática | Conceder mando o plaza por narrativa, editor o LLM |

**Norma de compatibilidad:** preservar `class_id`, `ship_id`, `save_schema_version` y semánticas anteriores hasta publicar un migrador explícito y reversible. En lectura legacy, interpretar según versión y contexto; si ambiguo, **REVIEW_REQUIRED o denegación sin mutar**. En lectura nueva, `ship_id` Enterprise-D y `class_id` Galaxy deben ser independientes; no aceptar una cadena «Valhalla» como prueba de ambas.

## 2. Protagonista F10/S04 — selección y credenciales

**Diseño aprobado, no migración efectiva:** hombre híbrido humano-vulcano, 45 años en 2383, madre vulcana y ascendencia paterna de Khan; nombre y apariencia dentro de los parámetros autorizados. La UI histórica IA-03A con selección humano/vulcano/híbrido, edad y biografía abierta **sigue siendo código legacy**. No hay que maquillarla como convertida en protagonista fijo; tampoco se debe borrar sin pruebas de partidas y validadores antiguos.

Fuente autoral confiable/versionada → reglas de admisión F10 → servicio HOST → hechos confirmados CoreRPG → vista Unreal. El formulario, un texto IA, un documento de personaje y la cinemática 2D **no pueden crear** identidad, autoridad, rangos o títulos. El guion de intro, su repetición o salto no puede matricular/ascender dos veces al jugador.

La genética especial, habilidades y posibilidades médicas del protagonista se especificarán en su sistema propietario cuando corresponda; **esta auditoría no concede capacidades nuevas ni modifica curaciones**.

## 3. F11 y el emisor institucional — separación de responsabilidades

**Corte probado:** primer ascenso **1101→1102** y persistencia mediante PR #106/#107; lector de expediente HOST **solo lectura** PR #109. La [PR #110](https://github.com/robdor80/Videojuego_StarTrek/pull/110) es **Draft de diseño y casos NO_EJECUTADO**, sin emisor productivo. Ninguna de ellas prueba carrera completa hasta capitán.

- **F11/Trek:** reglas de mérito, escalafón, vacante, puesto, sucesión, idempotencia, condiciones y efecto autorizado.
- **CoreRPG:** entidades, versiones, reloj, journal, persistencia y mutación final comprobable.
- **HOST:** verifica principal/sesión/procedencia, entrega la solicitud al dueño del dominio y proyecta respuesta; nunca calcula o concede por su cuenta un ascenso.
- **UE5 y LCARS:** muestran solicitud y resultado confirmados; una animación/ceremonia no altera rango.
- **IA:** produce texto y conversación, jamás autoridad institucional.

Un checksum de integridad de archivo **no acredita autenticidad** de la partida; un ID numérico de puesto tampoco es credencial. El emisor de ensayo y los payloads de pruebas no son emisores del producto.

## 4. Casos de regresión definidos ahora para ejecutar al retomar las fases

| ID | Entrada / condición | Resultado exigido y evidencia futura |
|---|---|---|
| MIG-01 | Guardado con clase histórica `valhalla` | Se conserva tal cual o se migra por regla explícita; nunca metamorfosis silenciosa a Enterprise-D |
| MIG-02 | Nueva partida 2383 | Una identidad protagonista aprobada, edad/ascendencia fija; sin selector libre de especie/historia |
| MIG-03 | Repetir/saltar intro | Ninguna admisión, vínculo o mérito duplicado |
| MIG-04 | Pedir destino Enterprise-D sin plaza/orden | Rechazo o espera causal; no asignación automática |
| MIG-05 | Guardado modificado / expediente ajeno | No concede rango ni revela información privada |
| MIG-06 | Reintento tras grabar ascenso antes de comunicarlo | Un único evento y un único recibo; ceremonia reanudable |
| MIG-07 | Cambio de puesto por baja o relevo en F04/F12 | Nadie ocupa simultáneamente cargos incompatibles; NPC conserva trazabilidad |
| MIG-08 | Oferta F11 rechazada / pospuesta | No fuerza cese del NPC, no regala la siguiente oportunidad |
| MIG-09 | Referencias de investigación Odyssey 2383 | No aparecen instaladas en Enterprise-D sin evento de instalación auténtico |
| MIG-10 | Cambio de versión de esquema de partida | Validar versión, procedencia, backup/rollback y causalidad Core |

**Resultado R5 de la auditoría:** dirección y contratos corregidos; solo se han fijado pruebas y propietarios para futuras implementaciones. No se modifica aquí F10, F11, HOST, CoreRPG, Lore ni las partidas. Sin pruebas nativas y aceptación no se cierra ninguna fase.
