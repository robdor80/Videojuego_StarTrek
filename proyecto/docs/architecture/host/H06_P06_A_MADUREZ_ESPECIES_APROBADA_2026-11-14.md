# H06-P06-A · Consolidación autoral de madurez por especie (F10)

**Fecha:** 14-11-2026. **Propiedad:** F10. **Estado:** APROBADO COMO DISEÑO por el autor; pendiente de integración en el validador nativo y de la revisión semántica real. **CoreRPG sin modificar.**

## Alcance y fuente de verdad

Contrato aditivo: [f10_species_maturity_policy_v0.1.json](../../../../sistemas/gameplay/character_creation/f10_species_maturity_policy_v0.1.json). Agrupa los acuerdos autorales de esta conversación sin modificar los contratos bloqueados de creación, los perfiles de biología, los programas históricos ni el pin CoreRPG. Los perfiles existentes siguen siendo fuente de hechos biológicos; los números de edad de esta tabla son **reglas jugables propias del proyecto**, no canon demostrado. La campaña comienza en 2383; el día/mes no está aprobado.

La edad mínima jugable es una condición **necesaria, nunca suficiente**: F10 debe verificar madurez individual, cronología, evidencias, origen y contexto; la segunda puerta semántica asistida por IA sigue obligatoria. Si falta evidencia de adultez, devuelve revisión pendiente y no crea PERSON. Para una fecha de nacimiento en el año límite, no inventar el día/mes de la campaña. La admisión a la Academia y el acceso por ciudadanía o contexto político son operaciones F10 separadas. Un cadete NPC humano de 16–17 años no habilita un protagonista humano menor de 18.

## Tabla aprobada (años terrestres)

| Especie | Edad mínima jugable | Disponibilidad | Regla |
|---|---:|---|---|
| `aenar` | 20 | Campaña principal, sujeto a F10 | Parentesco andoriano; telepatía contextual y accesibilidad; sin longevidad copiada automáticamente. |
| `andorian` | 20 | Campaña principal, sujeto a F10 | Sin madurez social obligatoria por ritos; longevidad 120–135 orientativa, no límite. |
| `bajoran` | 18 | Campaña principal, sujeto a F10 | Cultura y fe no obligatorias; la experiencia de ocupación no se impone. |
| `benzite` | 18 | Campaña principal, sujeto a F10 | La necesidad de soporte respiratorio es individual. |
| `betazoid` | 18 | Campaña principal, sujeto a F10 | Telepatía y empatía individuales; ni lectura total ni detección de mentiras. |
| `bolian` | 18 | Campaña principal, sujeto a F10 | Sin cifras universales de madurez o longevidad establecidas. |
| `breen` | 20 | Campaña principal, sujeto a F10 | Anatomía, función del traje y longevidad no se deducen por defecto. |
| `cardassian` | 18 | Campaña principal, sujeto a F10 | Preferencias ambientales contextuales; sin lealtad institucional implícita. |
| `changeling` | Pendiente, sin autorización automática | Campaña principal, sujeto a F10 | Cambio de forma o apariencia adulta no acreditan madurez; desarrollo morfogénico por definir. |
| `el_aurian` | 18 | Campaña principal, sujeto a F10 | Longevidad excepcional sin maduración más tardía asumida; sin poderes de Guinan por especie. |
| `ferengi` | 18 | Campaña principal, sujeto a F10 | Sin comercio, riqueza ni profesión automática; resistencia telepática contextual. |
| `hirogen` | 20 | Solo DLC Delta futuro | Fuerza, resistencia y tradiciones de caza dependen del individuo. |
| `human` | 18 | Campaña principal, sujeto a F10 | NPC cadetes humanos de 16–17 permitidos si admisión F10 los autoriza; no cambia mínimo jugable. |
| `jem_hadar` | Pendiente, sin autorización automática | Campaña principal, sujeto a F10 | Maduración acelerada y origen diseñado; edad cronológica no prueba autonomía o elegibilidad. |
| `kazon` | 18 | Solo DLC Delta futuro | Ritos y afiliación a sectas requieren contexto verificable. |
| `klingon` | 18 | Campaña principal, sujeto a F10 | Ritos de Ascensión no obligatorios; sin profesión o ciudadanía por especie. |
| `ocampan` | 2 | Solo DLC Delta futuro | Dos años es umbral jugable autoral, no madurez biológica canónica ni límite de vida. |
| `pakled` | 18 | Campaña principal, sujeto a F10 | No asignar limitaciones intelectuales, engaño o hostilidad universales. |
| `romulan` | 25 | Campaña principal, sujeto a F10 | Edad no concede acceso político a la Academia; no heredar medicina/telepatía vulcanas. |
| `talaxian` | 18 | Solo DLC Delta futuro | La personalidad de Neelix no define a la especie. |
| `tellarite` | 18 | Campaña principal, sujeto a F10 | Madurez biológica de ~12 es referencia complementaria, no mínimo jugable. |
| `trill` | 18 | Campaña principal, sujeto a F10 | Unión con simbionte independiente; edad del anfitrión y del simbionte separadas. |
| `vidiian` | 18 | Solo DLC Delta futuro | El Fago pertenece al estado médico individual; no se deriva moralidad. |
| `vorta` | Pendiente, sin autorización automática | Campaña principal, sujeto a F10 | Madurez funcional, ingeniería genética y clonación requieren modelo específico. |
| `vulcan` | 25 | Campaña principal, sujeto a F10 | Longevidad frecuentemente >200 orientativa; ritos y disciplina no implican habilidades. |

**Balance:** 25 especies biológicas (22 con mínimo numérico y 3 sin aprobación automática); 5 perfiles son exclusivos del DLC Delta. El perfil `borg_assimilated_character` es un estado de transformación y **no** una especie número 26. No se ha fijado un máximo de edad ni una mortalidad automática a partir de la longevidad orientativa. Los casos `changeling`, `jem_hadar` y `vorta` permanecen bloqueados para una decisión de elegibilidad automática hasta elaborar reglas específicas de desarrollo, ingeniería genética/clonación y evidencia.

## Contratos y autoridad

- `character_creation_contract_v1_0.json` exige adultez equivalente y una biografía coherente. `adult_equivalent_status=true` enviado por el cliente no demuestra nada.
- El validador C++ de PR #152 **no consume este contrato todavía**; el comportamiento de producto es `REVIEW_UNAVAILABLE` cuando no existen autoridad de evidencias ni evaluador semántico aprobados. Añadir números a un JSON no desbloquea esa composición ni hace `OBJECTIVE_VALID`.
- Solo F10 decide la elegibilidad y valida evidencias. HOST coordina campaña, sesión y permisos. CoreRPG conserva los hechos autoritativos; no se ha alterado su pin `76a7b7b485616d8c4994f384a90f123bf333591d`.
- NPC, civiles, aspirantes y cadetes tienen políticas propias; el mínimo de protagonista no es un límite biológico universal ni impone ciudadanía, rango, atributos, educación o personalidad.
- La pertenencia al DLC Delta sigue prohibiendo su aparición/selección en la campaña principal; alcanzar la edad propuesta no anula la restricción.
- Modificar reglas requiere una nueva versión revisada del contrato y debe invalidar cualquier futura decisión que dependiera de la versión anterior. No se emiten recibos hoy.

## Verificación y paso futuro

Test de referencia: `python -m unittest discover -s desarrollo/tools/validation -p 'test_f10_*.py' -v`. Incluye 8 casos nuevos en `test_f10_species_maturity_policy.py`: cobertura exacta del catálogo, edades autorales, excepciones, DLC, no máximos, procedencia de perfiles, contexto cronológico y ausencia de autoridad. Esos tests verifican **estructura y acuerdos**, no un candidato real.

La posterior adaptación C++/F10 deberá implementar y probar: (1) edad entera y fecha de nacimiento con año 2383 y frontera de cumpleaños sin día/mes; (2) 22 mínimos y rechazo determinista solo cuando la edad insuficiente sea demostrable; (3) 3 especies especiales sin atajos; (4) doble puerta objetiva/semántica y recibo ligado al borrador y a la versión; (5) conservación de la barrera DLC; (6) identidad, privacidad, competencia y procedencia. Requiere revisión independiente y PR separada: **Codex — GPT-6, razonamiento Alto**. No iniciar H06-P06-B ni H07 por el mero hecho de fusionar este documento.

**Estado de H06-P06-A:** contrato de edades APROBADO COMO DISEÑO; implementación de esas reglas en producto PENDIENTE; proveedor IA y evidencia de madurez PENDIENTES; H06-P06/M1 PARCIALES.
