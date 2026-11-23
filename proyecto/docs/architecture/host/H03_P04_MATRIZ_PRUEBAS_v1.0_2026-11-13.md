# H03-P04 — Matriz adversaria y de conformidad de identidad

**Fecha:** 2026-11-13 · **Estado de los casos:** DISEÑADOS / **NO EJECUTADOS** contra implementación H03.  
**Dueño del diseño y auditoría:** ChatGPT. **Dueño de implementación de pruebas nativas y CI:** Codex.  
**Referencia:** [Contrato H03-P01](H03_P01_IDENTIDAD_CONTRATO_v1.0_2026-11-13.md); [H01 HC-07, HC-08 y HC-35](H01_MATRIZ_CONFORMIDAD_v1.0_2026-11-11.md).

## Condiciones de ensayo

Suite nativa real sobre `TrekHost` y `TrekF04Bridge`, Core fijado conforme a la política H02, pruebas inyectadas solo cuando no sea posible un fallo real reproducible. Capturar estado de vínculo, `State` y generación H02, código Core F04/F05 cuando exista, revisión antes/después de cada rechazo, y ausencia de salida privilegiada. Resultados temporales según `AGENTS.md`; nunca modificar fixtures, oráculos, histórico o pins para que una prueba «pase». Revisión de errores normalizados con cobertura negativa y de concurrencia.

| ID | Escenario | Resultado esperado | Ejecución que corresponde |
|---|---|---|---|
| HI-01 | Nueva campaña creada desde HOST, personaje PERSON elegible verificado | Un único principal/campaña/personaje y `BOUND`; F05 admite primer vínculo | H03 nativa |
| HI-02 | `ACTIVE` sin vincular; consulta o acción del jugador | `PRINCIPAL_UNBOUND`, cero acceso por sujeto y cero mutación | H03 nativa |
| HI-03 | Intento de pasar actor, `F04Ref`, «verified» o rango desde UI/IA | Rechazar como capacidad; resolver identidad solo internamente | H03 nativa / contrato de adaptador H05 |
| HI-04 | El mismo sujeto se vincula por segunda vez | Idempotente: sin segundo hecho F05 y sin cambio de identidad | H03 nativa |
| HI-05 | Segundo sujeto diferente en la misma campaña | Denegación `IDEMPOTENCY_CONFLICT` o normalización fiel, no reemplazo | H03 nativa |
| HI-06 | `F04Ref` válido pero correspondiente a otra campaña o scope | Rechazo, no correlacionar por `id` coincidente | H03 nativa |
| HI-07 | `Generation` caducada tras cierre/reapertura | `GENERATION_EXPIRED`, sin acceso ni mutación | H03 nativa |
| HI-08 | Dos solicitudes simultáneas de primer vínculo | A lo sumo un único `BOUND` y registro F05 | H03 nativa |
| HI-09 | CLOSE admitido mientras vínculo está resolviéndose | No publicar vínculo de generación cerrada, sin use-after-free | H03 nativa / fault |
| HI-10 | Revisión Core vieja en el primer `f05_bind_player` | Rechazo coherente (F04_STALE), sin fingir éxito; política explícita de reconsulta | H03 nativa |
| HI-11 | `f05_bind_player` devuelve error de ámbito o actor no PERSON | Ningún `BOUND` publicado; no mutación parcial | H03 nativa / fault |
| HI-12 | Tras primer vínculo, F05 devuelve revisión actualizada | HOST no continúa usando revisión pre-bind | H03 nativa |
| HI-13 | Cerrar campaña y abrir otra con ID de persona repetido | Sujeto anterior no se hereda ni concede acceso a otra campaña | H03 nativa |
| HI-14 | Personal de Flota exige rango, expediente o permiso vía identificador | HOST no deduce ni altera F11; operación institucional no disponible si F11 no está | H03 contrato; H07 runtime |
| HI-15 | Restore legítimo con mismo personaje y scope nuevo | Nueva generación y referencia resuelta, continuidad sin usurpar personaje | **DIFERIDO H04** |
| HI-16 | Restore con persona inexistente o F05 previamente vinculado a otro | `PRINCIPAL_UNBOUND`/`ACCESS_DENIED`, ningún intercambio silencioso | **DIFERIDO H04** |
| HI-17 | Save importado que afirma credencial o identidad profesional | No eleva confianza ni autoriza operaciones institucionales | **DIFERIDO H04/H07** |
| HI-18 | Callback tardío de UI/IA después de LOAD | Rechazo por generación y limpieza sin Core | **DIFERIDO H04/H10** |
| HI-19 | Falla la validación mientras el usuario conserva campaña sana | Sin publicar vínculo erróneo; estado/rollback definido sin ocultar efecto Core | H03 nativa / fault |

## Prueba de independencia de reglas

Verificar que ni las cabeceras ni los símbolos enlazados del HOST incorporan el emisor de ensayo `f11_trial_host.inc`, que no se asignan grados profesionales por identidad local y que no se habilita un «cambio de personaje» público. Regresiones F05/H02 antes y después. F11 sigue certificando su propio emisor en el proyecto principal.

## Informe mínimo por caso

- Test y ruta del código probado, sistema/compilador, HEAD de Star Trek, SHA de CoreRPG, flags CMake y resultados de CI.
- Resultado `PASS/FAIL/SKIP`; un caso diferido sigue **PENDIENTE**, no `PASS`.
- Evidencia del puente real y, para denegaciones, revisión Core o prueba equivalente que descarte mutación.
- Desviaciones de contrato y decisión explícita antes de alterar APIs F04/F05.
- Cierre total H03 no incluye la certificación H04, UE ni F11; se registran las dependencias pendientes por separado.
