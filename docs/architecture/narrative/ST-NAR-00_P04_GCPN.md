# ST-NAR-00 — P04 Continuidad y Gestor de Continuidad y Paquetes Narrativos (GCPN)
**Aprobación conceptual:** autor, 16-10-2026. Diseño de contrato y referencia offline. No hay integración con saves CoreRPG/UE5 ni importación runtime.

## Propósito
Extender campañas en curso con nuevas temporadas diseñadas fuera del juego por autor y ChatGPT, sin contradecir historia vivida ni predeterminar temporadas ya instaladas. Subsystem específico de Star Trek, no dependencia de Nimroel.

## Cuatro funciones
1. Exportación de contexto: historia efectivamente confirmada durante TODA la campaña, estado actual, conocimiento del protagonista, relaciones, necesidades y versiones de contenido. NO solo temporadas; incluye misiones rutinarias y hechos NPC offscreen.
2. Catálogo narrativo: temporadas instaladas, futuras propuestas y posibles variantes; distinguir expresamente previsión editorial de hechos del universo.
3. Evaluación de packs: validación de seguridad/formato/referencias/capacidades y reglas contra histórico; revalidar frente al presente, no solo frente al snapshot usado durante la autoría.
4. Gestión de instalación: preparar, verificar, registrar y confirmar atómicamente. Instalación no es activación; si falta elegibilidad puede quedar instalado y dormido.

## Exportación reproducible
Archivo lógico: contexto.json según schema st_nar_campaign_context_v0.1, RESUMEN_CAMPAÑA.md human-readable, HISTORIA_REAL.json, ESTADO_ACTUAL.json, TEMPORADAS_INSTALADAS.json, TEMPORADAS_PREVISTAS.json, CAPACIDADES.json y MANIFEST.json con integridad. Los componentes separados serán vistas derivadas del mismo snapshot; no múltiples fuentes de verdad. Empaquetar en zip sin rutas absolutas, contenido secreto de credenciales o ejecutables.
La exportación de autoría completa puede revelar información oculta del juego, marcada full_authoring, y requiere confirmación explícita en interfaz. Una exportación player_visible omite lo desconocido y no sirve para certificación global de compatibilidad. Nunca verter contenido completo de chats, credenciales ni claves.
Cada hecho lleva ID, secuencia, fecha exacta, referencias y alcance. Diferenciar irreversible historical_fact_ids de current_fact_ids mutable. Ejemplo: historia.borg_assimilation permanece verdadera después de una recuperación; current.assimilated puede dejar de ser cierta. No confundir pasado y presente.
El resumen legible debe derivar únicamente de datos confirmados: la IA puede parafrasear, pero las fuentes exactas permanecen y el texto no adquiere autoridad.

## Exportación delta
Se permite modo delta con base_snapshot_revision, from_event_cursor y secuencias contiguas desde cursor+1. Acompaña estado actual completo y histórico indexado, nunca finge cubrir todo el pasado por sí solo. Debe integrarse con la exportación base correspondiente y revalidarse. Los huecos de cursor bloquean el informe.
El fixture actual simula tres eventos. No existe todavía un adaptador capaz de capturar los eventos reales de CoreRPG ni un marcador de truncamiento probado; etiquetar OFFLINE_FIXTURE / NO_RUNTIME_VERIFIED.

## Ingesta y seguridad
1. Examinar paquete en staging aislado, verificar paths relativos seguros, límites, digest, esquema, referencias y prohibición de código.
2. Verificar cronología, era, fuente causal, capacidades runtime registradas, misiones, autoridad y estado presente.
3. Comparar campaign_id, snapshot_revision y catalog_revision del authoring_binding con la campaña actual. Desfase implica revisión antes de incorporar, incluso si las condiciones declaradas siguen siendo posibles.
4. Rechazar de forma permanente constraints incompatibles con hecho histórico confirmado (forbid_history_fact_ids que aparece en historical_fact_ids). Ausencia temporal de condición puede dejar contenido instalado y dormido, pero nunca autoriza inventar el hecho requerido.
5. Presentar diferencias, dependencias, alcance y confirmación opt-in en save existente; política por defecto: sólo nueva campaña.
6. La instalación verdadera, aún por implementar, requerirá Core transaction/rollback, auditoría, metadata digest, restore check y journal de instalación. Fallos dejan intacto catálogo/save previo.
7. Prohibido borrar pack/version usada por una campaña activa si el save la necesita; version pins y migraciones explícitas, reversible o bloqueo seguro. Nunca editar hacia atrás event ledger.

## Qué no exportar o deducir
Los capítulos aún no jugados son propuestas, nunca event_ids ni verdad futura. No fabricar logros, conocimiento, amistades ni historial por usar mejor expediente académico al saltar S00. No inferir que un NPC muerto en la campaña reaparecerá porque figure en un paquete viejo.
La exclusividad de principal es de la experiencia del protagonista; eventos de varias historias continúan concurrentes. Revisión de vigencia de condiciones también al activarse capítulos, no solo al instalar.

## Integración futura obligatoria
Se requiere un adaptador CoreRPG que capture snapshots atómicos y secuencias completas, calcule cobertura, entregue historial de hechos y conocimiento por observador, y acepte journal transaccional de registro de packs. UE5 expone exportar/importar y advertencia de spoilers. Todavía no se ha hecho.
La herramienta de referencia offline puede evaluar los JSON proporcionados pero NO garantiza que procedan realmente de Core, NO instala packs, NO modifica un save y NO ejecuta el director en Unreal.

## Criterios de cierre técnico pendientes
- Escenario real de 8 temporadas, 4 vividas, 5 incorporaciones; historial Borg recuperado, traslado no guionizado y NPC offscreen.
- Export completo/delta con cobertura demostrable; export de autoría visible a ChatGPT sin revelar credenciales.
- Modificar el mundo entre exportación e importación: se exige revalidación.
- Rollback ante fallo de importación y load posterior sin duplicación.
- Pruebas UE5/MSI y del adaptador CoreRPG: bloqueadas hasta integración.
## Contenido textual de los informes
La exportación incorpora ahora world_summary_es y relevant_entities con estado actual, actual_summary_es de temporadas vividas y, en futuros paquetes, premise_es, planned_outline_es y possible_outcomes_es separados de los hechos históricos. El JSON garantiza referencias y el Markdown sirve para creación conjunta de nuevas temporadas sin tener que deducir el argumento de simples IDs.
