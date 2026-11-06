# Sistema Aster — escenario acotado de aceptación F06 (NO CANON)

**Estado:** fixture determinista para pruebas del motor CoreRPG + F06; no es una localización aprobada del lore ni sustituye a F13.

**Composición en el fichero JSON:** 1 estrella, 6 planetas (H, M, Y, J, P, L), 4 lunas, 1 nebulosa, 1 cinturón de asteroides representativo, 1 estación, 1 carguero civil, 1 nave científica de la Federación (Intrepid), 1 crucero klingon (Vor'cha), 1 nave romulana (D'deridex), 1 lanzadera y 1 sonda. Total **20 entidades**. Todos los nombres son provisionales.

## Las ocho horas de guardia

| Reloj Core | Suceso previsto |
| --- | --- |
| 00:00 | Estrella, planetas/lunas y objetos próximos; el klingon está fuera de alcance y la nave romulana no emite una firma detectable |
| 01:00 | Crucero klingon entra en alcance; carguero y lanzadera actualizan sus posiciones |
| 02:00 | La nave romulana pasa a emitir una firma observable; no se presupone simulación real de camuflaje |
| 04:00 | El crucero klingon se aleja y se registra pérdida con evidencia de alcance |
| 08:00 | El mismo crucero regresa y se readquiere manteniendo su identidad |

### Qué prueba y qué NO prueba

- `build_validation_system.py` lee el JSON y genera **solo firmas y posiciones autorizadas** para `f06_host_world_snapshot`. No introduce nombres, clase M, química ni relaciones de planetas en los datos públicos de Sensores.
- `f06.mini_system` recorre cada fotograma en una sesión **real** del puente F04, usando reloj, persistencia y vigilancia F06 en Core, sin crear una segunda galaxia ni simular misiones falsas.
- Las categorías astronómicas `STAR/PLANET/MOON/NEBULA/STATION/ASTEROID` son extensiones *append-only* de la ABI F06: indican el **tipo observado** cuando el nivel de detección lo permite; no revelan composición ni clase planetaria.
- `science_truth` en JSON es **información privada del Host para una futura Ciencia/F07**. El sistema F06 actual todavía NO determina ni publica la clase M/J/Y ni los porcentajes de atmósfera. Cuando exista espectroscopia real, deberá liberar lecturas progresivas únicamente tras observaciones autorizadas, nunca mediante un `if` de catálogo o LLM.
- Nebulosa: **firma detectable**. Efectos ambientales por volumen, afectación a otras naves, dinámica orbital, pirámide de LOD y camuflaje físico quedan fuera de esta fixture y deberán implementarse de forma independiente.
- Las coordenadas y emisiones son **valores normalizados de ensayo**, NO distancias astronomicamente precisas ni valores canon. No hay simulación orbital en ocho horas.
- `visual_asset_id=null` en todos los objetos. El autor dispone de modelos 3D descargados en su MSI: se asignarán a estos `key` estables después de revisión de derechos/formatos/escala/licencias y sin subir modelos pesados al repo. La vista de F07 puede renderizar un cuerpo solo con **conocimiento ya observado**.

**Fuente única de prueba:** `fixtures/aster_f06_qa.json`. **Generador:** `build_validation_system.py`. **CTest:** `f06.mini_system`.

Este escenario es reemplazable por la fuente autorizada de F13 sin modificar la lógica de F06.
