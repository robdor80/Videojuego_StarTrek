# Operación LORE — Documentación ratificada por el autor (23-11-2026)

**Continuidad:** exclusivamente la del videojuego privado **Star Trek Legends**. **Precedencia:** aprobaciones personales del autor > lore vigente del juego > material audiovisual compatible > propuestas antiguas. Una nota de archivo anterior no recupera autoridad por haber estado fusionada.

## Acta de autoridad

**[DECISIONES_RATIFICADAS_20261123.md](DECISIONES_RATIFICADAS_20261123.md)** — Registro aprobado de los puntos **1–20**; el punto 21 es esta auditoría editorial y su integración. Incluye expresamente lo eliminado, conservado y aplazado.

## Documentos y situación

| Archivo | Situación |
|---|---|
| [A01 — Auditoría previa](A01_AUDITORIA_PRECEDENCIAS.md) | HISTÓRICO, con nota de precedencia |
| [A02 — Galaxy / Valhalla / 16 VAL-TEC](A02_ENTERPRISE_D_VALHALLA.md) | RECONCILIADO con tecnologías aprobadas, alta narrativa en 2387 y flujo cuántico posterior |
| [A04 — Catálogos técnicos](A04_TECNOLOGIA_MEDICINA_CIENCIA.md) | CONSERVADO: 45 sistemas / 73 equipos, revisión individual pendiente |
| [B03 — Cronología galáctica](B03_CRONOLOGIA_2383_2387.md) | RECONCILIADA: historias anteriores compatibles; continuidad propia prevalece |
| [B05 — Medicina/ciencia/especies](B05_MEDICINA_CIENCIA_ESPECIES.md) | CONSERVADO: 26 perfiles / 38 condiciones / 20 fenómenos, revisión individual pendiente |
| [B07 — Instituciones y astrogeografía](B07_INSTITUCIONES_ASTROGRAFIA.md) | CONSERVADO sin creación de rutas o facciones |
| [B09 — Enciclopedia/PADD](B09_ENCICLOPEDIA_PADD.md) | **IDEA APLAZADA**; 20 entradas no aprobadas |
| [C11 — Protagonista Rise](C11_BIOGRAFIA_PROTAGONISTA.md) | RATIFICADO, sin genealogía/maestros inventados |
| [C12 — Legendarios y relaciones](C12_LEGENDARIOS_ARCOS.md) | RATIFICADO, rangos, edades y Data 2386/2387 corregidos |
| [C14 — Historia Enterprise-D](C14_HISTORIA_VALHALLA.md) | RATIFICADO, **sin las ocho misiones inventadas** |
| [C15 — Academia/Consejo](C15_PROLOGO_ACADEMIA.md) | SOLO hechos narrativos; **guion eliminado** y titularidad de la conversación de intro |
| [D10 — Auditoría de cierre](D10_AUDITORIA_CIERRE.md) | Control de coherencia y riesgos restantes |

## Archivos de datos

- **S04 protagonista**: anexo documental versionado `sistemas/gameplay/character_creation/s04_protagonist_narrative_annex_20261122.json`. Conserva apellido **Rise**, madre T'Ralis, padre Naveen Rise, genealogía no enumerada, cuatro artes marciales, piano, nueve aptitudes y personalidad evolutiva. **No sustituye** el contrato S04 v2 bloqueado ni se consume en HOST.
- **Enciclopedia**: `mundo/lore/knowledge/lore_2383_enciclopedia_editorial_v1.json`, **borrador de 20 entradas no aprobado**, sin importación runtime; desarrollo reservado a IDEA-0021 y su conversación.
- **Tecnología antigua**: `mundo/lore/technology/valhalla_tech_decisions_v0.1.json` permanece como **registro histórico** de 16 acuerdos, con identidad de clase ya superada; no modificar su SHA ni convertirlo en estado activo de la Enterprise-D.

## Control técnico y límites

- **CoreRPG** conserva hechos, rangos, autorizaciones, mundo, persistencia y temporalidad.
- **HOST** orquesta consultas y representa identidad autorizada; ninguna documentación crea una ABI nueva.
- **Unreal** muestra las escenas; la cinematografía de la intro se desarrolla en su propia conversación.
- **No se incluyen cambios en C++, ABI, contratos históricos con hashes, guardados ni activos UE**.
- 2387 es **hito narrativo aprobado** para la entrada de Enterprise-D; el sistema técnico no debe asumir materialización automática desde el catálogo.
- El programa experimental de **flujo cuántico** se incorpora **después** de la entrada en servicio de 2387, al concluir pruebas y autorizaciones.
- La aprobación documental no equivale a implementación certificada ni a auditoría fuente a fuente de los catálogos.

**Pruebas reproducibles:** `python3 desarrollo/tools/validation/validate_operacion_lore_20261122.py` y `python3 -m unittest discover -s desarrollo/tools/validation -p 'test_operacion_lore_20261122.py' -v`. Los resultados efectivos deberán constar en GitHub Actions de la PR de ratificación.