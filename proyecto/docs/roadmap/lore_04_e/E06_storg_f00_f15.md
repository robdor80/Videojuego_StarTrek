# LORE-04E06 — Trazabilidad ST-ORG-01, F00–F15 y dependencias

**Estado:** AUDITORÍA DOCUMENTAL EN PR DRAFT — sin merge, sin certificación runtime ni decisiones creativas añadidas.

## 1. ST-ORG-01

La organización de Flota (mandos, dotaciones, oficiales, historial y jerarquía) se referencia a través de `sistemas/gameplay/organizations/profiles/STARFLEET_ORGANIZATION_PROFILE_v0.1.json`, `mundo/lore/federation/starfleet/organization/` y `proyecto/docs/roadmap/master/fases/F04/`. No se ha localizado un archivo con identificador literal `ST-ORG-01` en los resultados de búsqueda por código, por lo que se conserva la **dependencia conceptual por perfil y árbol real**; no se afirma una integración certificada con un artefacto inexistente o no localizado.

## 2. Fases existentes

**F00–F03**: arquitectura, autoridad, CoreRPG y persistencia; **F04–F06**: dotaciones, órdenes, sensores; **F07–F09**: assets, guardia y consolas; **F10–F12**: Academia, carrera y vida en nave; **F13**: universo dinámico; **F14–F15**: presentación y preparación de release. La documentación LORE-04 no reescribe ningún contrato ni estado de esas fases, y respeta que aceptaciones de referencia no equivalen a build beta del juego.

## 3. Procedural

Se reutilizan los paquetes cerrados de evolución civilizatoria, expansión, guerra, generación de asentamientos e instalaciones. El bloque de economía viva sigue abierto. Una guerra o ruina histórica puede condicionar la demanda, pero no debe activar retroactivamente economía, misión o infraestructura de modo oculto.

## 4. Estado de prueba

El workflow E ejecuta QA documental B/C/D/E y regresiones contra A, LORE-01/02/03 y referencias relevantes. Las posibles pruebas que dependan del runtime Host/UE5 solo podrán producirse mediante integración separada. La matriz transversal no cambia F00–F15, ST-ORG ni CoreRPG; se limita a verificar coherencia conceptual y dependencias localizables.

**Control:** CoreRPG es dueño del WorldState; fuentes de verdad LORE-01/02/03 y F00–F15 no se duplican. El dictamen final depende de CI, revisión de autor y fusiones posteriores expresas.
