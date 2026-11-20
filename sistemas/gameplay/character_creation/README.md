# Sistema 04 — Protagonista único, identidad y carrera (v2)

**DECISIÓN AUTORAL VIGENTE 17-11-2026: DISEÑO APROBADO, IMPLEMENTACIÓN PENDIENTE.**

**La nueva partida del videojuego Star Trek RPG ya no usa un creador de personaje libre.** Tiene un solo protagonista canónico, siempre el mismo **varón híbrido humano-vulcano**, hijo de **madre vulcana** y **padre humano descendiente de Khan Noonien Singh**, que ingresa con **45 años (aparenta ~30)** en la Academia de **2383**. Posee longevidad híbrida, expresión excepcional de características del linaje Khan, formación profunda en cuatro artes marciales (kung-fu, kárate, aikido y Suus Mahna), autocontrol emocional aprendido, vocación científica y música. Su pasado es fijo; sus decisiones durante el juego no.

**Ampliación autoral de 19-11-2026:** su sangre tiene **potencial biomédico excepcional** heredado del linaje Khan. Enfermería podrá pedirle muestras para investigar y desarrollar tratamientos, vacunas o terapias para casos concretos, también como actividad cotidiana cuando esté sano. La donación es voluntaria, no hay cura universal ni resurrección automática y las mecánicas médicas específicas quedan pendientes. Referencia de diseño: [S04 v2, §04.3.1](S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md). **Documentado; no implementado.**

## Documentación ACTUAL (siempre comenzar aquí)

1. [DEC-0022 — decisión de autor y precedencia](../../../proyecto/docs/decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md).
2. [Sistema 04 v2 — diseño integral](S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md).
3. [Contrato estructurado v2 — protagonista fijo](s04_fixed_protagonist_contract_v2.json).
4. [Ficha biográfica canónica](s04_protagonist_biography_v1.json).
5. [Plan de intro cinematográfica ilustrada](S04_INTRO_CINEMATICA_PLAN_v1.md).
6. [Migración F10 y HOST](S04_MIGRACION_F10_HOST_v2.md).
7. [Estado de implementación](s04_initial_persona_status_v2.json).

## Comienzo de nueva partida previsto

```text
Nueva partida
→ Nombre del protagonista + pequeños ajustes de aspecto
→ Validación institucional/F10 de origen canónico
→ Intro: Janeway y Picard debaten con almirantes ficticios,
         Picard recuerda Locutus; 5 recuerdos ilustrados 2D
→ Admisión legítima y comienzo como cadete en la Academia, 2383
→ Cuatro años académicos; carrera, decisiones y relaciones abiertas
```

**Editable:** nombre, peinado, barba, detalles del rostro e indumentaria estética compatible con su situación. **Fijo:** sexo, especie, edad, progenitores, genética, biografía, vocación científica y destrezas marciales iniciales. El nombre personalizable no altera linaje ni parentesco; no hay selector masculino/femenino, humano/vulcano/híbrido ni caja de texto para inventar una vida alternativa.

Picard y Janeway conocen y defienden institucionalmente la solicitud desde 2383; **no** son automáticamente amigos íntimos. Picard lo conoce personalmente durante la Academia, y Janeway puede conocerlo en persona más tarde con Siete de Nueve. El romance con Siete nunca se regala. Sisko **no** aparece en el consejo de 2383 (LORE-05B: retorno posterior 2388–2392). La Academia no otorga gratis galones ni el mando de la Enterprise-D.

**Realismo técnico:** legado Khan da superioridad física **real** cuando se integre; ninguna puntuación arbitraria ni «cuatro maestrías» puramente decorativas. F10 y Core mantienen validación y autoridad, HOST coordina y UE5 representa. La introducción es una estructura aprobada, **sin guion final ni assets generados**.

## Material histórico preservado / NO UX vigente

| Archivo antiguo | Estado correcto tras DEC-0022 |
|---|---|
| `character_creation_contract_v1_0.json` | Baseline bloqueada histórica; NO sustituir en caliente, versionar |
| `f10_initial_player_rules_v0.1.json` | Selección de 3 especies del antiguo producto empotrada en HOST; requiere migración |
| `f10_species_maturity_policy_v0.1.json` | Perfiles generales 18/25/22 todavía utilizables por reglas de especies, pero no para selector de nueva partida |
| `f10_formulario_inicial_v0.1.json`, `f10_formulario_inicial_v0.3.json` y formularios HTML | Prototipos offline históricos de editor abierto |
| `FORMULARIO_INICIAL_H06_F10_V0_1.md`, `FORMULARIO_INICIAL_H06_F10_V0_3.md` | Informes históricos de su desarrollo |
| `background_contracts/HUM_01...`, `VUL_01...`, `HVA_01...` | Referencias genéricas de especie/crianza, no opciones libres del héroe |
| `biography_validation_rules.md`, `character_sheet_model_v1_0.json`, `player_profile_contract.json` | Lógica de validación/ficha/alias a reutilizar con fuente fija y adaptación autorizada |

**NO afirmar que HOST/F10/UE5 ya muestra la nueva pantalla.** El diseño está reescrito; el cambio de código y tests, incluso las reglas IA-03A que siguen permitiendo tres especies, queda pendiente de integración cuando haya capacidad de Codex. No desinstalar ni rehacer sistemas genéricos de NPC.

## Separación de registros

```text
FICHA DEL PROTAGONISTA ≠ EXPEDIENTE ACADEMIA
                         ≠ EXPEDIENTE SERVICIO
                         ≠ HISTORIA/MEMORIA DE PARTIDA
                         ≠ ALIAS DE USUARIO
```

Las capacidades cambian por evidencia real; el rango/autoridad de F11 no surge del apellido; la intro no crea ni re-crea hechos Core.
