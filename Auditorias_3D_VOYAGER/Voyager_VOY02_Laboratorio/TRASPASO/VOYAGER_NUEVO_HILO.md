# Prompt para nueva conversación dedicada exclusivamente a Voyager

Copia el texto desde «CODEX LOCAL» hasta el final en la nueva conversación. Este archivo no inicia automáticamente otra sesión ni envía mensajes a otros chats.

---

CODEX LOCAL — CONTINUACIÓN VOY-02 DESDE TRASPASO CONTROLADO

Proyecto: Videojuego Star Trek RPG. USS Voyager, clase Intrepid. Entorno MSI Raider Windows 11; Blender 5.2.2 LTS; motor final previsto Unreal Engine 5.8.2.

Reanuda exclusivamente el laboratorio técnico VOY-02. La sesión anterior fue detenida para conservar contexto, no porque estuviera terminada. No trabajes sobre Sutherland. No inicies restauración artística definitiva ni integración Unreal.

Antes de ejecutar pruebas o modificar archivos, lee íntegramente estos documentos, en este orden:

1. `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\UE5_ENTORNO_COMPARTIDO.md`
2. `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\SUTHERLAND_ESTADO_FINAL.md`
3. `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\VOYAGER_HANDOFF.md`

Comprueba después el estado real mediante `TRASPASO\ESTADO_PARADA.json`, `INVENTARIO_ARCHIVOS.csv` y `COMPROBACION_ENTRADAS.json`. Distingue cualquier cambio posterior del usuario. No sustituyas baselines para hacer desaparecer diferencias y no repitas `00_preparar.py` en la entrega existente. La última comprobación conservaba las 115 entradas originales y las 106 copias sin cambios; no hay que reconstruirlas.

El laboratorio está en `C:\Users\andro\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio`. El archivo `ESCENAS\VOY02_Laboratorio.blend` contiene ocho escenas y 49 imágenes empaquetadas. Hay 33 capturas, 26 archivos de datos, 14 scripts más cache y 15 logs. No había procesos pendientes ni un guardado interrumpido.

El último trabajo terminado fue `12_capturas.py`. El punto exacto de continuidad es **antes de corregir el encuadre de `shot()`**: G02 y D02 recortan extremos; el filtro de caso B ajusta cámara pero no oculta vecinos. No se ha aplicado ninguna corrección. Verifica también la correspondencia numérica del `.blend` con las transformaciones y geometría ensayadas; abrirlo para capturas no cerró esa comprobación. No rehagas importación, geometría o todos los cálculos por un cambio de cámara.

Continúa la misión original usando sus resultados existentes. Queremos demostrar las posibilidades reales de construir un puente detallado a escala humana, pocos pasillos conectados, acceso al puente, turbolift y un camarote del jugador. Voyager tendrá un alcance menor que la Enterprise Valhalla. No hace falta toda la nave ni todos los interiores de la biblioteca.

Trabaja autónomamente con copias aisladas. Están autorizados cambios de geometría de prueba, pivotes provisionales, adaptadores, agrupaciones, maniquíes/cápsulas, escenas Blender, capturas/renders/animaciones técnicas, scripts y exportaciones útiles para diagnóstico. No modifiques originales, activos de producción, Sutherland, parámetros del personaje existente o proyectos Unreal. Usa herramientas disponibles sin nuevas instalaciones si bastan. No hace falta pedir permiso por cada prueba dentro de ese alcance.

Orden de prioridad: escala humana y arquitectura del puente; compatibilidad modular; unión puente–pasillos; camarote; puertas/sillas/consolas; materiales/rendimiento; prototipo conjunto; hoja de ruta. Aún falta cerrar ergonomía independiente de asientos, consolas, techo, puertas y escalones. No adoptas 1:1 ni 1,508 automáticamente. El factor 1,10 es provisional y los informes deben explicar su confianza y los problemas locales.

No pierdas estas conclusiones parciales ni las conviertas en promesas definitivas:

- Las siete pruebas de corredores pasan cápsulas y soporte en rutas centrales seleccionadas, pero tienen discrepancias de sección y requieren ajustes/adaptadores. No todas son A.
- Existen dos rutas geométricas desde la pasarela posterior del puente a cabina y habitación Mesh4, con 948 y 1110 poses por altura y radio 0,35 m. Esto no demuestra acceso desde el centro o navegación de todo el puente.
- Las puertas del prototipo están abiertas estáticamente. Sus poses intermedias generan contactos; no hay bolsillos o mecanismo certificados.
- Las agrupaciones de sillas y pantallas están identificadas. No están validadas las articulaciones, postura sentada, alcance de controles o UI.
- Los tests de cápsula Blender no son CharacterMovement ni NavMesh UE. No inventes FPS ni costes reales de Lumen.
- La arquitectura MAX coincide por una similitud en muchas piezas, con excepciones. No mezcles familias sin comprobar cada correspondencia.

Lee los resultados de VOY-01 conforme los necesites, sin repetir toda su auditoría: `C:\Users\andro\Documents\Auditorias_3D\Voyager_Puente_2026-10-21`, documentos copiados en `REFERENCIAS`, PR Draft #32 <https://github.com/robdor80/Videojuego_StarTrek/pull/32>. VOY-01 está documentada; VOY-02 todavía no. No interpretes la autorización documental antigua como encargo de publicar esta nueva fase. No hagas publicaciones, fusiones o cambios en `main` en esta misión local.

Completa únicamente lo que falta y repite pruebas cuando un cambio real o una duda concreta lo justifique. Conserva evidencias negativas y resultados sustituidos con una explicación. Clasifica A verificado/compatible; B ajustes menores; C adaptación importante; D reconstrucción recomendada; E no demostrado. Un ajuste de anclas o una vista bonita no basta para grado A.

Entrega los nueve informes en la raíz del laboratorio:

- `00_RESUMEN_EJECUTIVO.md`
- `01_ESCALAS_ERGONOMIA.md`
- `02_MODULARIDAD_PASILLOS.md`
- `03_CONEXION_PUENTE_PASILLOS.md`
- `04_CAMAROTE_JUGADOR.md`
- `05_PUERTAS_SILLAS_CONSOLAS.md`
- `06_MATERIALES_RENDIMIENTO.md`
- `07_HOJA_DE_RUTA_RECOMENDADA.md`
- `08_PRUEBAS_Y_LIMITACIONES.md`

Incluye índice, CSV/JSON de medidas/interfaces/clasificación/matrices/compatibilidades/incidencias/pruebas, scripts y logs, escenas útiles sin duplicación innecesaria, capturas técnicas revisadas que muestren éxitos y defectos, y ZIP con informes/tablas/capturas para compartir con ChatGPT. Los `.blend` pueden quedar fuera del ZIP por tamaño, indicando sus rutas exactas. La fase final de documentación y empaquetado no estaba iniciada: no afirmes que ya está lista.

La hoja de ruta debe separar trabajo autónomo Blender, decisiones artísticas del usuario, pruebas UE5 futuras, soluciones reutilizables Sutherland, sistemas futuros del videojuego y actuaciones que convenga posponer. Prioriza reducir incertidumbre para un puente excelente, corredores creíbles y camarote funcional. No inicies esa restauración o integración al terminar el laboratorio.

Empieza informando brevemente del estado real encontrado y de la primera tarea pendiente que vas a resolver. No solicites de nuevo autorización para las operaciones de laboratorio ya autorizadas. Si detectas cambios posteriores que alteren el punto de partida, preserva esos cambios y explica su impacto antes de actuar sobre ellos.
