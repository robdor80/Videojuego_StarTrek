# Sutherland Ergonomia_03 — Parte A
27/10/2026, Europe/Madrid. Copia protegida única.
Etapa A.1: seleccionada VISUAL_02 recuperada de ST_ORG_01_FASE_3C_09/RECUPERACION/P-e4252915fcf5.
Motivo: conserva Quinn, capitán, cuatro puertas, colisiones y los seis mecanismos laterales que INTEGRACION_FINAL_01 retiró.
La entrega final posterior se ha inspeccionado como referencia, no se promueven sus retiradas sobre esta base.
Etapa A.2: copia y comprobación SHA-256 COMPLETADAS. Ver Data/copy_verified.json y copy_manifest.json. Siguiente: auditoría Blender y nivel UE, sin guardar originales.
Reanudación: python Scripts/01_prepare.py; comprueba cada archivo existente antes de copiar; no sobrescribe diferencias.
No modificar originales. No commit/push/PR. D04 histórica operativa; D01–D03 sin destinos. Pies suspendidos y VSM abiertos.

A.3 preparación verificada: Data/blender_comparison.json; export_meshes.json ok=true (31 visuales, 8 hojas, 51 grupos físicos afectados). Exportaciones FBX completas.
Inventario de referencias: connections_before.json ok=true: Chair01–06, 15 componentes móviles cada una, un STSeatAnchor capitán. Posiciones y alturas laterales protegidas.
IMPORTANTE: VISUAL_02 solo tiene un STSeatAnchor para sentarse/levantarse (capitán); los seis laterales conservan STSlidingChair de 15 piezas con desplazamiento, ocupante y obstrucción. No se inventarán seis anclajes de asiento ausentes.
Hasta aquí Unreal solo auditado; mapa de trabajo todavía original. Siguiente: preparar importación controlada, adaptar únicamente las colisiones dependientes y comprobar sillas sin pérdida.
Intento de importación 3: assets derivados guardados; proceso 26444 detenido tras espera interna sin escrituras (contador WriteTransferCount estable 6712980; mapa SHA-256 aún original 93593853...). No había guardado de mapa activo. Originales intactos; mapa de trabajo todavía anterior. Revisar Logs/07_integrate_retry2.log. No certificar ensayo de sillas hasta resultado explícito.
La espera global FinishAllCompilation del comprobador histórico también bloquea el editor completo. La traza nativa/Python se conserva. Proceso 9020 detenido sin guardado de nivel activo; assets ya guardados. Se sustituye esa batería por seis ciclos Toggle/AdvanceChair con barridos reales, directamente sobre los mecanismos recuperados; sin cambios al código nativo ni a sillas.
A.3 GUARDADA: Data/integration.json ok=true. 31 visuales +8 hojas +51 grupos físicos actualizados en namespace propio, mapa guardado. Seis ciclos reales Toggle/AdvanceChair superados: 57cm ida, retorno0, bases fijas, 15 piezas cada una. No repetir 07_integrate.py. Siguiente: Scripts/08_verify_saved.py en otro proceso y comprobación jugable limitada.
