# USS Sutherland — revisión dimensional y ergonomía del puente

**Fecha:** 27-10-2026  
**Proyecto:** Videojuego Star Trek RPG — Clase Miranda  
**Estado:** DIAGNÓSTICO PRELIMINAR / PROPUESTAS NO APROBADAS  
**Alcance:** análisis de medidas existentes y preparación de ajustes, **sin cambios geométricos**.

## Fuente, protección e incertidumbres

- Fuente dimensional: datos comunicados de una ejecución de Codex con Blender Python; **no se han cotejado aquí** los informes, mallas o capturas locales.
- Original local: `assets/puentes/starfleet/USS Sutherland/star_trek_sutherland_bridge.glb`.
- Blender base local: `juego/Clase Miranda/puente/blender/Miranda_Puente_Sutherland_Base.blend`.
- Blender de análisis local: `juego/Clase Miranda/puente/blender/Miranda_Puente_Sutherland_Analisis.blend`.
- Evidencias locales: `juego/Clase Miranda/puente/analisis_dimensional/`.
- El informe de Codex indica 345 objetos originales intactos. **No equivale a una comprobación independiente desde este expediente**.
- Por política de almacenamiento, GLB, BLEND, texturas PBR y laboratorios permanecen en el MSI y fuera de Git; no añadirlos a la rama o a la PR. Comprobar antes de editar que haya una copia recuperable distinta del original; el respaldo del 27-10-2026 está en el mismo MSI y **no sustituye un respaldo externo**.
- F07 contiene ensayos ya reportados de UE5, puertas, colisiones, sillas y PBR; no repetirlos ni declarar su aceptación definitiva sin sus logs. Ref.: `proyecto/docs/roadmap/master/fases/F07/RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md`.

## Medidas preliminares (cm)

| Elemento | Medida comunicada | Condición |
|---|---:|---|
| Referencia Quinn | 177,3 | altura del personaje |
| Referencia humanoide alto | 250,0 | altura de diseño, anchura/cápsula aún por definir |
| Hueco turboascensor, altura | 388,4 | determinar cota real del umbral |
| Hueco turboascensor, anchura interior | ~143,7 | comprobar ancho libre de colisión |
| Otras puertas, altura | 386,9 | determinar umbral |
| Otras puertas, anchura | 163,6 | comprobar ancho libre de colisión |
| Techos del turboascensor | 424,8–468,3 | altura sobre superficie transitable |
| Otros techos | 409,5–505,4 | altura sobre suelo local |
| Consolas centrales, superficie | 143,9 | uso sentado/de pie por confirmar |
| Consolas centrales, controles máximos | 177,2 | uso, ángulo e interacción por confirmar |
| Consolas laterales, superficies | 113,3–117,7 | uso sentado/de pie por confirmar |
| Cojín capitán | 62,8 sobre podio | medir apoyo de pies |
| Cojines laterales | 77,5 sobre suelo | medir reposapiés y pose real |

### Interpretación inicial

- Las puertas dejan **138,4 cm** (turboascensor) y **136,9 cm** (otras) de holgura vertical teórica sobre un humanoide de 250 cm. No implica que el acceso funcione: faltan geometría de arco, cápsula, animaciones y colisiones.
- El techo más bajo comunicado (409,5 cm) queda 159,5 cm por encima de un personaje erguido de 250 cm. La altura interior puede ser decisión artística deliberada: **no reducir nada por defecto**.
- Los cojines a 62,8/77,5 cm parecen altos para Quinn si sus pies deben apoyar en el suelo de referencia; podrían justificarse por podios, reposapiés, proporciones de rig o animaciones: **inspeccionar antes de alterar**.
- Las consolas centrales a 143,9 cm parecen demasiado altas para manipulación humana convencional, y las laterales a 113,3–117,7 cm pueden servir de pie pero resultar incómodas sentado. Determinar función y punto real de contacto antes de proponer centímetros definitivos.
- No aplicar un factor de escala general al puente: desharía relaciones con puertas, sillas, materiales y colisiones ya ensayadas.

## Prioridades y orden de trabajo

**P0 — Integridad y referencia metrológica (primero):**
1. Confirmar unidades Blender, escalas de objetos, transforms, cota de suelo y coordenadas mundiales.
2. Medir superficie de cojín, reposapiés, suelo/podio, centro de cadera en posición sentada y mandos de cada consola; distinguir ancho/alto del bounding box respecto a espacio libre real.
3. Contrastar con las evidencias y mecanismos F07 existentes, sin sobrescribir ni reconstruir nada.

**P1 — Sentado funcional:** revisar primero asientos laterales, luego capitán. Retomar el bloqueo F07-SEAT-01 (once poses con penetración de muslos reportadas); comprobar que el mecanismo F07-CHAIR-02 de seis bases siga funcionando, con retroceso 27 cm, avance 57 cm y animación 1,9 s reportados.

**P2 — Consolas y alcance:** definir qué mandos se usan sentado y de pie; comprobar alcance de manos/codos con Quinn y ergonomía de una especie de 250 cm. Valorar ajustes locales o estaciones adaptables, no escala global.

**P3 — Accesos y techos:** tomar vistas frontal/lateral del puente con ambas siluetas; verificar turboascensores, umbrales, ancho real libre y tránsito. Mantener dimensiones actuales salvo decisión artística expresa.

**P4 — Colisiones/animaciones UE5:** después de aprobar las soluciones visuales, repetir pruebas focalizadas de sentado/levantado, colisiones, puertas y circulación. No confundir un laboratorio con aceptación UE07 oficial.

**P5 — Geometría definitiva y PBR:** únicamente tras fijar proporciones. La reorganización registra cinco referencias de texturas preexistentes sin resolver para un paquete histórico `assets/ships/starfleet/bridges/USS Suntherland/`; verificar si conciernen a la variante utilizada antes de atribuirlas al GLB actual.

## Siguiente inspección acotada en Blender (solo lectura)

1. Abrir exclusivamente la **copia de análisis**: no guardar el original ni aplicar transformaciones.
2. Conservar una escena sin cambios y superponer Quinn (177,3 cm) y humanoide alto (250 cm).
3. Obtener seis vistas: (a) alzado frontal general; (b) lateral general; (c) lateral asiento del capitán con pies y consola; (d) lateral asiento de operador con pies y consola; (e) frente turboascensor con ambas siluetas; (f) vista superior circulación con anchuras.
4. Generar tabla acotada: asiento (altura efectiva desde apoyo de pies), reposapiés, consola (superficie de acción) y distancia horizontal asiento–mando, incluyendo referencia y coordenadas mundiales.
5. Comparar expresamente F07-CHAIR-02 / F07-SEAT-01 y registrar qué mecanismo/pose existente se reutilizaría.
6. Entregar evidencia clara (capturas + tabla + resumen de incertidumbres), sin cambios en mallas, materiales, transforms, jerarquías, rigs ni assets.

## Puerta de aprobación antes de la primera edición de geometría

El autor revisa las vistas y el encaje real de Quinn. Solo después se acuerdan, por elemento y en cm, modificaciones concretas a **una copia de trabajo**, reversibles, con registro de diferencias. Las puertas, techos y tamaños para personajes de 250 cm **no se alteran automáticamente**.

### Criterios de aceptación posteriores

- Quinn y personaje alto mantienen escala coherente con el suelo y las puertas, sin interpenetraciones impropias.
- Sentado: cadera/cojín, pies/suelo o reposapiés, rodillas y manos/mandos plausibles en las animaciones elegidas, sin penetraciones detectables.
- Movimiento de sillas conservado; puerta/turboascensor y trayectoria transitables.
- Originales, jerarquías y PBR originales intactos; comparativa antes/después recuperable.
- UE5, FPS y estado F07 solo se actualizarán con pruebas y evidencias primarias reales.

**Situación de esta entrega:** exclusivamente plan, análisis de cifras existentes y criterios de ensayo. **Cero modificaciones geométricas, cero validaciones nuevas en Blender/UE5 y cero cierre de F07.**
