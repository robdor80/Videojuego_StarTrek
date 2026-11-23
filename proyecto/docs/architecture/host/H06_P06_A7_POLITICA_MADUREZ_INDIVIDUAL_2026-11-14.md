> **DOCUMENTO HISTÓRICO — SUSTITUIDO EL 14-11-2026.** El usuario ha decidido que el protagonista declara su edad y F10 solo comprueba el mínimo jugable de su especie. NO implementar el registro de etapas vitales, atestaciones de madurez ni el encargo Codex A8 propuesto aquí. Consultar `H06_P06_CORRECCION_EDAD_DECLARADA_2026-11-14.md`. Este texto se conserva únicamente para explicar el trabajo anterior.

# H06-P06-A7 — Madurez individual y etapa vital del personaje inicial

**Fecha:** 14-11-2026. **Responsable de este corte:** ChatGPT. **F10:** dueño del dominio. **Estado:** PROPUESTA DE DISEÑO, referencia offline y pruebas; pendiente de aprobación específica de reglas de madurez por especie y de implementación C++. **No certifica H06-P06-A, HU-08 ni M1.**

Contrato nuevo: [f10_individual_maturity_policy_v0.1.json](../../../../sistemas/gameplay/character_creation/f10_individual_maturity_policy_v0.1.json). No reemplaza los documentos bloqueados ni crea edades biológicas canónicas.

## 1. Alcance observado en el repositorio

Inspeccionadas las 25 fichas `sistemas/gameplay/species/profiles/*_v0.1.json`, la política de 22 edades mínimas numéricas y tres excepciones de la PR #153, la biología de especie, `character_lifecycle_contract.json`, el contrato de antecedentes A5, la autoridad registrada y el validador nativo A6. **No existe todavía una tabla aprobada y aplicable de etapas de madurez individual para las 25 especies**. La documentación biológica, en diversos perfiles, señala expresamente datos desconocidos o sujetos a contexto. No se puede inferir una regla humana a partir de esos vacíos.

El registro `stage_rule_registry.entries` queda **vacío deliberadamente**. Registrar una etapa adulta requiere una decisión de dominio con base verificable y aprobación autoral; no basta con aprobar este documento. Ninguna especie ha obtenido por esta PR autorización automática de madurez.

## 2. Tres comprobaciones que NO equivalen entre sí

1. **Edad mínima jugable:** un valor de F10 ya acordado por especie. Ejemplo: humano 18, vulcano 25, ocampano 2 en DLC. Por debajo del mínimo demostrado, corrección.
2. **Etapa vital individual adulta:** necesita *regla de desarrollo propia* y *constatación interna individual* coherente para un personaje de esa especie. Puede definirse para un personaje recién creado sin inventar un expediente PERSON previo; pero la regla y la fuente deben existir antes.
3. **Acceso a la Academia:** examen separado de ciudadanía, elegibilidad institucional, permisos y plazas. Ni la madurez ni los estudios determinan una admisión.

En un juego de ficción no debe exigirse al jugador un certificado clínico real. La atestación debe producirla un mecanismo interno F10 al evaluar una propuesta coherente con reglas aprobadas y contexto de campaña. **No** la produce el cliente al indicar `adult_equivalent_status=true`, ni la IA al decir «parece adulto». Las discapacidades, diferencias físicas, costumbres, pon farr, rituales, clonación o apariencia no deben convertir automáticamente a nadie en adulto o menor.

## 3. Cómo acreditarlo sin burocracia

Contrato recomendado para una futura **regla de especie/etapa**:

| Dato | Explicación |
|---|---|
| Identidad de especie y referencia | Perfil vigente al que se aplica |
| Regla y versión F10 | Regla de etapa aprobada, con procedencia comprobable |
| Tipo de origen | Nacimiento biológico, origen diseñado, activación u otro, solo cuando proceda |
| Evidencia individual de etapa | Datos suficientes para aplicar la regla; sin inventar anatomía o facultades |
| Condiciones y límites | Casos especiales, incertidumbres y excepciones |
| Aprobación autoral | Decisión documentada antes de habilitar la fuente |
| Vinculación del borrador | SHA de biografía, contexto, política, emisor, generación y versión |

La fuente interna debe reutilizar `RegisteredBiographyAuthority` y no poder resolver prohibiciones deterministas. Una contradicción o revocación devuelve el caso a pendiente. Aunque se respaldara la etapa adulta, el resultado sería **solo una subcomprobación objetiva**: después quedan otras evidencias y la puerta semántica. La creación de PERSON será una operación F10-Core posterior y separada.

El diseño evita dos extremos: (a) exigir un historial médico imposible a un personaje que todavía no existe y (b) convertir todos los personajes que cumplen el mínimo jugable en adultos reconocidos automáticamente.

## 4. Ejemplos reproducibles y tratamiento

| Borrador | Resultado de la referencia A7 |
|---|---|
| Humano 17 | CHANGES_REQUIRED; por debajo del mínimo |
| Humano 18 y declara adultez | REVIEW_REQUIRED; falta regla/fuente individual |
| Humano 45 | REVIEW_REQUIRED; tener más edad no crea prueba |
| Vulcano 24 | CHANGES_REQUIRED |
| Vulcano 25 | REVIEW_REQUIRED |
| Nacido 2365-01-01 con campaña iniciada en 2383 sin día/mes | REVIEW_REQUIRED; cumpleaños en año límite |
| Ocampano 2 años | CHANGES_REQUIRED en campaña principal por bloqueo DLC |
| Cambiante, jem'hadar o vorta de 100 años | REVIEW_REQUIRED; regla especial no aprobada |
| Texto «parezco adulto», ceremonia o uniforme | No aporta autoridad biológica |
| Cliente adjunta `adult_stage_attested=true` | CHANGES_REQUIRED por inyección de autoridad |

No se fija ningún máximo de edad por esperanza de vida. Ni la experiencia de un NPC legendario ni un rito cultural establecen una regla universal de especie.

## 5. Ficheros y pruebas del corte

- `sistemas/gameplay/character_creation/f10_individual_maturity_policy_v0.1.json` — contrato de diseño, registro vacío y barreras explícitas.
- `desarrollo/tools/validation/f10_individual_maturity_reference.py` — referencia offline y no autoritativa; devuelve solo `REVIEW_REQUIRED` o `CHANGES_REQUIRED`, nunca da evidencias válidas, no usa IA ni escribe Core.
- `desarrollo/tools/validation/test_f10_individual_maturity_policy.py` — 31 tests nuevos de límites, ciclo vital, fuentes, inyección, especies y barreras.

Comando CI: `python -m unittest discover -s desarrollo/tools/validation -p 'test_f10_*.py' -v`. Ejecutar las regresiones nativas de HOST sin afirmar que el código C++ incorpora ya la política.

## 6. Entregable para Codex — posteriormente

**Recomendación de modelo: GPT-6; razonamiento Alto.** Codex, en una PR separada, deberá inspeccionar primero el contrato y las fichas; definir un lector de reglas de etapa F10 y una atestación interna nativa vinculada a borrador, contexto y revisión, sin suplantar `BiographyAuthority`. **No se le autoriza a inventar reglas de madurez de las 25 especies ni a implementar una edad=adultez**. Antes del uso productivo necesita aprobación concreta de las reglas y evidencias.

Quedan pendientes: reglas individuales justificadas, tres especies especiales, fecha completa de 2383, fuentes institucionales, elección de proveedor IA semántico y futura publicación PERSON. `H06-P06-A`, `HU-08`, `M1` siguen **PARCIALES/NO CERTIFICADOS**. No iniciar H07.
