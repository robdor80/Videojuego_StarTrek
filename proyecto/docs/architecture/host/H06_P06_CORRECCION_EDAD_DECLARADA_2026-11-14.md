# H06-P06 — Corrección de criterio: la edad la declara el jugador

**Fecha:** 14-11-2026. **Decisión del autor:** sustituye el diseño de pruebas de madurez individual de A7 y el encargo A8 originalmente propuesto. **Responsable del arreglo:** ChatGPT. **CoreRPG:** pin `76a7b7b485616d8c4994f384a90f123bf333591d`, intacto.

## 1. Regla de producto

El jugador crea un personaje de ficción: selecciona especie y declara cuántos años terrestres tiene. **Ese dato es verdadero para su personaje por decisión del jugador**; no debe ser investigado, certificado ni demostrado mediante un sistema de evidencias de madurez.

F10 hace lo siguiente:

1. Verifica que la especie existe y está disponible en el contenido actual.
2. Verifica que la edad es válida y compara con el **mínimo jugable aprobado** del catálogo existente.
3. Si está por debajo, solicita corregirla. Si cumple el mínimo, **la comprobación de edad ha terminado**.
4. Otras comprobaciones de biografía, permisos y coherencia narrativa son independientes. No convierten la edad en un problema de procedencia.
5. Al crear una PERSON en una fase posterior y autorizada, se conservará la edad declarada sin inventar una fecha exacta de nacimiento si el jugador no la ha dado.

Ejemplo: vulcano, 32 años; mínimo vulcano, 25 años. **Edad válida**. No requiere expediente médico, evaluación de etapa vital, proveedor de IA ni ninguna otra prueba biológica.

## 2. Qué se conserva y por qué

- **Una sola tabla:** `f10_species_maturity_policy_v0.1.json` sigue almacenando los 22 mínimos numéricos. Su revisión interna pasa a `0.1.1` y elimina la obligación de aportar `maturity_evidence_required`. Se conserva la identidad del contrato y su ruta para no duplicar las edades.
- **Tres especies sin mínimo acordado:** `changeling`, `jem_hadar`, `vorta` quedan pendientes de que el autor decida su **edad mínima jugable**, no de montar una autoridad biológica.
- **Cinco especies DLC Delta:** continúan fuera de la campaña principal.
- **Fechas de nacimiento:** si el jugador proporciona una fecha exacta y el año de comienzo 2383 no tiene día/mes, la comprobación en el año del umbral sigue pendiente. Si declara directamente una edad entera válida, este problema no existe.
- **Campos antiguos:** `adult_equivalent_status` permanece en el contrato bloqueado por compatibilidad. No es una prueba adicional; la interfaz futura puede cumplimentarlo internamente al preparar el borrador sin formular otra pregunta al jugador. La migración de ese campo, si se decide, será independiente.
- **Autoridad de otros hechos:** se conservan los registros y barreras que impiden que escribir «soy capitán» o «poseo autorización máxima» conceda rangos o privilegios. Esas protecciones sí tienen sentido.

## 3. Qué se elimina

Se retira del **comportamiento nativo de F10** la emisión de `MATURITY_EVIDENCE_REQUIRED` para un candidato que cumple el mínimo. Se versiona el ruleset `f10-biography/5` para invalidar evaluaciones anteriores. No se requiere una infraestructura nueva ni Codex.

Las propuestas A5/A7 que establecían etapas vitales y fuentes de madurez individual quedan **históricas y expresamente sustituidas**, sin borrar commits ni alterar los perfiles de biología que sí pueden servir para otras mecánicas del juego. El prompt Codex A8 original queda cancelado.

## 4. Límites

Este arreglo **NO** crea PERSON, no guarda partidas en CoreRPG, no selecciona IA real, no concede ciudadanía, rangos, certificaciones, acceso a Academia ni habilidades y no cambia el esquema bloqueado de creación. Únicamente corrige el criterio de la **edad inicial**.

**Validación:** regenerador de reglas, regresiones Python F10, pruebas nativas Windows/Linux, ASan/UBSan, Release, H01 y F11 aislado. Solo declarar resultados que confirme la CI del HEAD final.

**Estado esperado:** corrección de edad IMPLEMENTADA / PROBADA / FUSIONADA cuando pase auditoría; H06-P06-A, HU-08 y M1 siguen PARCIALES / NO CERTIFICADOS por otras dependencias, no por una prueba ficticia de adultez.
