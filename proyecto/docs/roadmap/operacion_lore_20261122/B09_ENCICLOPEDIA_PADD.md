# B09 — Enciclopedia/PADD: IDEA APLAZADA (sin contenido aprobado)

**RATIFICACIÓN 23-11-2026:** concepto conservado **solo como IDEA para otra conversación**. Las **20 entradas son borradores no aprobados**; no deben interpretarse como hechos definitivos ni contenidos publicados. Se mantienen únicamente como material provisional sin importación a runtime.

**Producto inicialmente propuesto:** base consultable por índices/lecturas, **no** IA implementada ni servicio operativo. Catálogo editorial: `mundo/lore/knowledge/lore_2383_enciclopedia_editorial_v1.json`.

## Precedencia aprobada — enciclopedia de Star Trek Legends, NO canon televisivo automático

**Decisión del autor, 23-11-2026:** la biblioteca/enciclopedia ha de describir **la continuidad propia y aprobada de nuestro videojuego**. [IDEA-0021](../../../ideas/IDEA-0021_enciclopedia_starfleet_continuidad_propia_lcars_padd.md) es la especificación funcional de esta extensión a B09.

**Orden obligatorio:** (1) decisiones autorales vigentes + LORE ratificado del juego para datos estables; (2) CoreRPG/WorldState para acontecimientos realmente ocurridos en cada partida; (3) canon Star Trek **solo cuando no contradiga** lo anterior; (4) información no resuelta, nunca autocompletada con canon externo. La etiqueta de procedencia `SCREEN_CANON` **no otorga prioridad** sobre una divergencia `GAME_ADDITION` aprobada.

**Ejemplo:** si la biografía autorizada de Siete de Nueve difiere de la televisión, prevalece la versión del videojuego. El año 2400 citado al explicar esta regla era **hipotético**, no una nueva fecha de nacimiento fijada. No fabricar datos no ratificados. La Enterprise-D de Proyecto Valhalla se describe según su reconstrucción propia y su WorldState, no por repetir sin filtro otras continuidades.

**Control de publicación:** las 20 entradas iniciales son **semillas editoriales pendientes de auditoría de continuidad autoral**; no publicar respuestas ni habilitar importación runtime hasta verificar cada afirmación frente a las decisiones actuales. No alterar a ciegas entradas históricas ni inventar conciliaciones. Los conflictos quedan señalados para revisión.

**Regla innegociable:** consultar artículos no crea misiones, desbloquea acontecimientos, aprende hechos automáticamente en WorldState ni modifica la partida. Solo lectura, incluida la app Android IDEA-0019.

## 1. Cinco planos de información que no deben mezclarse

1. **Factual histórica**: afirmaciones, fechas, fuentes, confianza y vigencia.
2. **Capacidades de diseño**: una nave/clase *puede* admitir X, no que tenga X instalado.
3. **Estado del mundo**: identidad y condiciones existentes (CoreRPG).
4. **Observación de actor**: qué se midió, por quién, cuándo, con qué precisión.
5. **Autorización**: clasificación, rol, expediente, orden/consentimiento y acceso vigente.

El ordenador **nunca crea** por decir algo una entidad, contacto, diagnosis, destino, orden, disponibilidad de armas, información clasificada o amistad NPC. Solo proyecta fuentes y consultas a la autoridad.

## 2. Campos editoriales del catálogo

- `entry_id` es identificador propio de **contenido**; nunca se reutiliza como `entity_id` de WorldState.
- `title_es`, `domain`, `summary_es`, `source_paths`, `claim_class`, `confidence` permiten visualización y revisión.
- `not_before_year`, `not_after_year` (nullable) indican validez conocida, no programan eventos.
- `default_visibility` describe política editorial, **no una lista de control de acceso definitiva**.
- `release_gate` obliga a consultar Core/autoridad para conocimiento nuevo, permisos o sucesos posteriores.
- `runtime_import_allowed=false`, `fictional_knowledge_guard=true`: no dar por consumido este esquema en HOST.

En futuras versiones, evitar duplicar los JSON y contratos LORE-01–05. Guardar punteros estables a definición, fuente y revisión, no hacer del índice una segunda copia de 73 fichas tecnológicas.

## 3. Flujo de consulta permitido

```text
Usuario pregunta a LCARS/PADD
  -> HOST autentica actor/sesión
  -> CoreRPG valida fase, tiempo, identidad, conocimiento y permisos
  -> índice documental busca artículos candidatos con procedencia
  -> proyección elimina secretos, hechos posteriores no ocurridos y observaciones ajenas
  -> IA (opcional) redacta SOLO desde el contexto autorizado
  -> respuesta con «conocido / no consta / incierto / clasificado / obsoleto»
```

**No usar RAG como bypass de seguridad:** indexar fichas restringidas puede ser legítimo para operadores autorizados, pero una búsqueda textual no concede derecho a leerlas. La ausencia de acceso no debe filtrar siquiera el nombre de un expediente privado si su existencia es secreta.

## 4. Ejemplos de respuesta en castellano

- **«¿Está operativa la Enterprise-D?»** → «En el expediente histórico de 2383 figura *en reconstrucción*. Para disponibilidad actual consulte el registro de buques autorizado». La base editorial no responde «sí» porque 2387 sea objetivo.
- **«¿Qué enfermedad tiene la capitana?»** → «No existe acceso autorizado a información clínica individual». Sin revelar si hay diagnóstico.
- **«¿Dónde está Sisko?»** → «Históricamente se vinculó a los Profetas en 2375. Situación actual sujeta a información disponible». No activar el retorno 2388–2392.
- **«¿Están instalados los torpedos transfásicos?»** → «Se estudian como candidato técnico. Estado de equipamiento individual no confirmado; consulte Ingeniería/Táctica». No ejecutar orden.
- **«¿Qué detecta la nebulosa?»** → «Sin observaciones disponibles o suficientemente recientes no es posible determinarlo». Ofrecer procedimiento, no inventar lectura.
- **«¿Qué ruta hay hacia Gamma?»** → informar sobre el agujero bajorano histórico solo si está en el conocimiento del actor; no suponer que está abierto o autorizado ahora.

## 5. Entrega e integración futura

Este índice es **independiente** de decisiones de modelo IA, embeddings, herramientas de búsqueda, LCARS y uso offline. Para integrarlo se necesitan contrato de proyección, tablas de permisos, reloj, retención, auditoría, sincronía PADD y pruebas de no filtración. El estado `COMPLETE_DOCUMENTARY` de una ficha no significa `INDEXED`, `ACCESSIBLE` ni `CERTIFIED` en juego.
