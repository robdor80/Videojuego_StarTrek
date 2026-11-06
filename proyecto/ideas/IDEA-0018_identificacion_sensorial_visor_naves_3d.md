# IDEA-0018 — Identificación sensorial con modelos 3D de naves

**Fecha:** 2026-11-06  
**Estado:** PLANIFICADA (idea creativa aprobada; NO IMPLEMENTADA)  
**Origen:** propuesta del autor durante la planificación de F06.  
**Tipo:** Star Trek específico + catálogo de recursos 3D + presentación UE5.

## 1. Experiencia aprobada

Cuando Sensores detecte e identifique una nave, la interfaz podrá presentar en un recuadro/visor un **modelo tridimensional de esa nave o de su clase**, aprovechando la extensa colección de modelos 3D Star Trek disponible localmente para el proyecto. El resultado debe ser visual, intuitivo e inmersivo, sin exigir conocer de memoria las clases de naves. Se mantiene la distinción entre contacto real, clase identificada y representación del catálogo.

Esta aprobación es **del concepto y de la distribución de trabajo entre fases**, no de un archivo concreto, licencia, malla ni skin LCARS definitiva.

## 2. F06: catálogo lógico y semántica (sin visor final)

- **F06-P03:** inventariar los modelos disponibles, registrar clases/variantes/naves concretas con IDs estables y preparar un catálogo JSON versionado (preferido inicialmente frente a una base de datos) que vincule identidad lógica de nave con un `visual_asset_id`.
- Separar **contacto → clasificación/identidad observada → asset lógico → archivo gráfico**. No incrustar rutas de archivos GLB en el estado autoritativo del contacto.
- Diferenciar `unknown`, `partial`, `class_probable`, `class_confirmed` e `identity_confirmed` o sus equivalentes integrados; no equiparar certeza de clase con conocimiento de nombre o matrícula.
- Evitar filtraciones de World State: un contacto desconocido NO revela por el visor un casco exacto; una hipótesis solo admite silueta genérica o representación expresamente **no confirmada**. Mostrar clase o unidad específica únicamente cuando esté suficientemente justificado por observaciones y conocimiento autorizado.
- Asegurar identificadores de clase y variante, resolución de ausencias de recurso y persistencia de clasificación sin persistir el asset visual como hecho sobre el universo.
- **F06-P04:** fijar acciones semánticas de consola, como «Ver perfil», «Mostrar modelo», «Analizar» y «Seguir», condicionadas a conocimiento/permisos, sin renderizar GLB todavía.
- Auditar primero los recursos, formatos, procedencia y permisos de uso. Los modelos locales excluidos de Git NO deben subirse de forma automática ni romper la regla de assets pesados.

**Posibles nombres de entregables** (no crear aún): `ships_visual_catalog.json`, `ship_classification_contract.json` y documento de handoff para F07. Rutas exactas, validadores y formato final se decidirán al implementarse P03.

## 3. F07: presentación visual real en Unreal Engine 5.8.2

- Diseñar un recuadro/visor LCARS interactivo en el puesto de Sensores con representación 3D del asset apropiado.
- Importar/convertir los modelos disponibles, incluidos `.glb` cuando corresponda, al pipeline UE5; no suponer que GLB será el formato de runtime.
- Considerar rotación, zoom, vistas predefinidas y comparación opcional; el alcance concreto se aprobará en diseño de F07.
- El visor refleja exclusivamente la proyección de información autorizada por CoreRPG/Host y no toma decisiones de detección.
- Aplicar presupuestos de geometría, materiales/texturas, LOD, memoria y carga asíncrona para no bloquear la consola ni perjudicar FPS; preservar compatibilidad con el resto del puente.

## 4. Reglas e integración

- **CoreRPG/Star Trek:** realidad única del contacto, conocimiento/identidad, progreso de detección y persistencia.
- **Catálogo visual:** relaciona IDs autorizados con recursos de visualización; no confiere por sí mismo conocimiento de una nave oculta.
- **Unreal/F07:** muestra una instancia visual separada del actor real de nave; un modelo de ficha no implica haber visto físicamente su casco.
- **F06:** motor funcional y catálogo; **F07:** visor/LCARS definitivo; **F08:** validación en primera guardia jugable.
- Reutilizar contratos existentes: `sistemas/gameplay/ship_operations/consoles/sensors/`, `sistemas/gameplay/ship_operations/sensor_resolution/` y `sistemas/gameplay/ship_operations/ship_memory/`; evitar una segunda tabla autoritativa de naves.

## 5. Criterios de aceptación futuros

1. El catálogo identifica las clases/modelos disponibles sin exigir recursos 3D en el repositorio remoto.
2. Contacto desconocido, probable, confirmado e identificado reciben presentaciones diferentes y no filtran información oculta.
3. Se resuelve correctamente una clase con varias variantes y una clase sin modelo disponible.
4. Guardar/cargar conserva la información sensorial y no introduce certeza adicional.
5. La interfaz de F07 muestra el asset autorizado, con carga y rendimiento validados en MSI; hasta esa prueba no se declara «visor 3D jugable».

**Estado de ejecución:** ninguna implementación, modificación del motor, importación masiva de GLB ni diseño visual definitivo autorizados por este registro.
