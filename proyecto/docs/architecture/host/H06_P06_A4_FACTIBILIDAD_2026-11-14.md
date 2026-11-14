# H06-P06-A4 · Factibilidad de la autoridad interna F10

**Fecha** 14-11-2026. **Base** `bf56700ecfa0e29e45cb5b3532eec92c27d5015b`. **Dominio** F10.

## Punto de partida

| Fuente | Reutilización |
|---|---|
| [PR #152](https://github.com/robdor80/Videojuego_StarTrek/pull/152) | Los puertos `BiographyAuthority` y `SemanticEvaluator` separan evidencia, propuesta semántica y decisión. La evaluación ya vincula el borrador canónico al contexto y la versión y mantiene privado el recibo. |
| [PR #154](https://github.com/robdor80/Videojuego_StarTrek/pull/154) | Las reglas de madurez jugable preceden a la consulta de evidencias. El tratamiento de Delta, especies especiales y fechas ambiguas conserva la prioridad objetiva. |
| [PR #155](https://github.com/robdor80/Videojuego_StarTrek/pull/155) | El [contrato de procedencia](../../../../sistemas/gameplay/character_creation/f10_biography_evidence_semantic_boundary_v0.1.json) define fuentes registradas, versiones, vinculación exacta y fallos cerrados. Su alcance publicado es de diseño. |

## IMPLEMENTADO

Un componente interno puede preparar un registro de procedencias, usar la vinculación devuelta por la evaluación del borrador y aportar decisiones para las afirmaciones exactas que una futura fuente autorizada examine. La infraestructura trabaja en memoria y permite una atestación previa a PERSON por una fuente de antecedentes iniciales validada por F10. El puerto semántico y la decisión del dominio siguen siendo pasos separados.

## PROBADO

La base coincide con el merge de la PR #155. El código C++ está dentro del módulo privado de HOST. El checkout CoreRPG local estaba limpio en `76a7b7b485616d8c4994f384a90f123bf333591d`. La matriz existente cubre los dos sistemas, ASan/UBSan y modo de producto.

## BLOQUEADO

La acreditación de madurez individual requiere una política autoral explícita. Los adaptadores que puedan comprobar antecedentes iniciales, las fuentes de campaña y el proveedor semántico requieren aprobación y una integración posterior.

## PENDIENTE

Auditoría independiente, fecha completa de campaña y políticas para las especies especiales. La publicación de hechos y la admisión pertenecen a operaciones futuras.
