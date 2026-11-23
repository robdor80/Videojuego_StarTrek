# ENCARGO PARA CODEX — HOST H06 / IA-03B02: factory de protagonista fijo F10/CoreRPG

**Estado:** PREPARADO por ChatGPT el 20-11-2026; **NO EJECUTADO**. Entregar a Codex tras revisión/fusión de B01, siempre sobre main vigente.
**Modelo recomendado:** **GPT-6**.
**Nivel de razonamiento:** **ALTO**. Justificación: autoridad F10, manipulación de WorldState y publicación transaccional real; no gastar Extra Alto por defecto.
**Repositorio:** robdor80/Videojuego_StarTrek.
**Rama de entrega:** nueva rama propia de IA-03B02 partiendo de main actualizado.
**PR:** Draft, sin fusionar.
**Director técnico/auditor:** ChatGPT. **Propietario autoral y autorizaciones:** usuario.

## 1. Lee obligatoriamente las fuentes antes de tocar código

- AGENTS.md.
- proyecto/docs/architecture/host/H06_IA03B01_ARQUITECTURA_S04_PERSON_ACADEMIA_2026-11-20.md.
- proyecto/docs/architecture/host/H06_IA03B01_CONTRATO_INTEGRACION_v0.1.json.
- proyecto/docs/architecture/host/H06_IA03B01_MATRIZ_ACEPTACION_2026-11-20.md.
- proyecto/docs/decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md y fuentes S04 v2 asociadas.
- sistemas/gameplay/character_creation/S04_MIGRACION_F10_HOST_v2.md.
- f10_host_candidate_factory_contract_v0.1.json, admission_flow.json y academy_state.json.
- desarrollo/integration/host/tests/academy_core_feasibility.cpp.
- desarrollo/integration/host/src/f10, biography_profile_source.h, player_bootstrap.h, native_session.h, session_owner.cpp y puertos públicos actuales.
- H04_PERSISTENCIA_2026-11-13.md y f04_session_bridge.cpp solo para detectar dependencias; B03 será otra tarea.
- PR #185 (IA/CI) y #186 (Unreal/editor), ya fusionadas.

Confirmar las versiones reales de los archivos en main antes de desarrollar; no trabajar sobre un árbol viejo de H06 o la PR #167.

## 2. Objetivo B02 — UNA PERSON candidata real, sin matrícula

Implementar el primer factory nativo F10/CoreRPG de producto capaz de tomar la biografía canónica aprobada S04 v2 **desde una fuente interna verificada**, aceptar únicamente el nombre autorizado, y preparar/publicar **una única PERSON** candidata de Academia en el WorldState del Core fijado, con historia/relación y un recibo privado verificable.

**Protagonista inmutable:** varón híbrido humano-vulcano de 45 años en 2383, padre humano descendiente de Khan, madre vulcana, pasado civil, cuatro artes marciales y vocación científica/música. No aceptar una especie/sexo/edad/historia alternativa enviados desde UI.

**No crear** una variante humana, vulcana pura, ni múltiples arquetipos. Cada nueva campaña tiene una PERSON Core distinta; mismo intento y misma campaña no duplican el protagonista.

No otorgar rango F11, comisión, autorizaciones navales F05, plaza de cadete, estado ADMITTED ni cadet_year_1. La admisión es una transición F10 separada y se coordina con B03/IA-03C.

## 3. Política F10 v2 y procedencia

- Preservar intactos los contratos LOCKED y la ruta IA-03A v1; crear una ruta **versionada** para protagonista canónico.
- Cargar/compilar la fuente autoral S04 internamente. Verificar ID, versión, hash y consistencia de las invariantes. No aceptar identificadores de fuente, person_id, campaign_id, issuer o credential aportados por cliente.
- Conservar como UNKNOWN los nombres de padres, lugar natal, fecha exacta, títulos académicos y demás huecos del canon. No falsificar diplomas, planeta o genética para satisfacer el contrato v1.
- Para biografía fija autoral, implementar una evaluación determinista **únicamente a través de un contrato F10 v2 explícito**. No fabricar una respuesta OpenAI COHERENT ni desactivar la puerta de IA-03A para borradores libres. Si el contrato LOCKED hace imposible la nueva vía sin una decisión de dominio, documentar el conflicto y **detener la publicación de candidato**; entregar el tramo seguro y una propuesta concreta en la PR.
- Los hechos fijos de S04 que puedan representarse en el Core deben ser reales y persistibles, no un texto ornamental. Para habilidades físicas/marciales, **no inventar valores numéricos**: guardar antecedente y dependencia explícita de la regla Core/F10 pendiente. No afirmar haber implementado esa capacidad jugable si no existe escala aprobada.

## 4. Diseño mínimo del factory y atomicidad

- Usar una sola sesión propietaria HOST y el mismo CoreRPG pin 76a7b7b485616d8c4994f384a90f123bf333591d. No crear un WorldState paralelo autoritativo ni un servidor.
- Reutilizar las primitivas Core probadas en academy_core_feasibility, pero **no copiar sin más el fixture**: el catálogo/las definiciones deben ser de producto y reconocibles en restore.
- Preparar catálogo, contexto y entidad/historia en un staging no visible; validar antes de publicar. Una excepción o fallo de publicación deja cero PERSON visibles y conserva íntegra la sesión anterior.
- Implementar idempotencia con clave interna HOST por campaña/intento y digest de fuente+datos editables. Mismo intento repetido => misma PERSON/resultado; misma clave y cambios => conflicto sin efectos.
- El recibo de creación es privado, vinculado a fuente aprobada, contexto H03, generación, campaña, revisión Core, PERSON y hecho candidate_created. Nunca exponer setters de PERSON a Unreal, NPC o IA.
- Si resulta necesaria una extensión aditiva de SessionOwner para hospedar la operación, conservar su hilo propietario y las regresiones navales. **No utilizar f05_bind_player** para “demostrar” que el candidato está vinculado, ni utilizar f04_create(miranda) como campaña Academy.

## 5. Fuera del alcance de B02

- **No** integrar todavía guardado y recuperación Academy H04: IA-03B03.
- **No** implementar el vínculo académico H03 durable completo: IA-03B03.
- **No** crear ABI pública nueva, pantallas UE, intro, modelos/avatar ni HUD: IA-03C.
- **No** escribir acto de admisión, matrícula o plaza de cohorte sin emisor F10 específico. B02 termina en CANDIDATE.
- **No** modificar F11, las órdenes F05, CoreRPG externo, pin, pruebas históricas, contratos LOCKED, assets, S04 canon autoral ni laboratorios previos.
- **No** ejecutar OpenAI LIVE, enviar expedientes personales o consumir API por este encargo. Si la ruta antigua requiere IA, no simularla como credencial de producto.

## 6. Pruebas de aceptación exigidas

Implementar especialmente B02-01 a B02-15 de la matriz:
- Un héroe fijo con nombre variable y una PERSON real, sin plaza.
- Nuevas campañas con identidades diferentes y mismo perfil base.
- Reintentos seguros, clave reutilizada con distinto payload y fallo inyectado con rollback.
- Rechazo de especie/sexo/edad/parentesco alterados, cliente con person_id/emisor/recibo falso, fuente canónica caducada.
- Preservación auténtica de todos los datos UNKNOWN.
- No crear rango F11, servicio F05 ni admisión.
- Pruebas de coexistencia/regresión con IA-03A v1 y H02–H05.
- Evidencia de que **un test de fixture** no sustituye al factory de producto.

Correr CI relevante Windows/Linux, sanitizadores y producto Release tests-OFF. Si no se dispone de una plataforma, indicar NOT_RUN y no atribuirle PASS.

## 7. Entrega

Crear PR **Draft** con cambios mínimos, pruebas e informe permanente (en docs de HOST) con: fuente/digest/versiones, operaciones nuevas, criterios A/B02 cubiertos, pruebas y sus límites, errores de publicación, compatibilidad legacy, ruta del laboratorio prescindible y pendientes concretos para B03.

Artefactos temporales únicamente dentro de laboratorios/host/ia03b02/; nunca versionar ni borrar material anterior, conforme AGENTS.md.

**No fusionar.** ChatGPT auditará la PR antes de autorizar la continuación con IA-03B03.

**Criterio B02:** una PERSON candidata **real de CoreRPG** y sus hechos con procedencia autoral, sobre la sesión auténtica, con idempotencia y pruebas negativas. Nunca basta documentarla, simular un HTTP COHERENT o abrir un fixture de Miranda.
