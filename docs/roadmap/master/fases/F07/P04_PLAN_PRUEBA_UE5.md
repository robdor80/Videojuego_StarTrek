# F07-P04 — Montaje y recorrido UE5 Sutherland

**Preparado documentalmente, NO EJECUTADO en MSI.** Nivel sugerido nuevo L_F07_Sutherland_Transit_Test bajo Content/StarTrek/Prototypes/F07/Sutherland/; comprobar antes las rutas reales. Nunca sobrescribir Kelvin_Bridge_Test ni Kelvin_Bridge_ThirdPerson_Test.

1. Importar **copia** del GLB con hash documentado y anotar configuración de Unreal, plugins, escalas, orientación y ruta final.
2. Añadir PlayerStart, cámara/cápsula de primera persona, Enhanced Input para mover, mirar, interactuar y cancelar. Orientar respecto a entrada real, no inventar coordenadas.
3. Montar colisiones simples de suelo, paredes, plataforma, barandillas y muebles; recorrer turboascensor/acceso → estación de Sensores sin clipping, atasco ni suelo intangible.
4. Crear un actor de interacción con trigger o line trace a distancia corta, texto «Sensores», control de foco y apertura/cierre de UI en castellano. Validar restauración de input y cámara al salir.
5. UI de **demostración visual explícita** «SIN CORE / SIN ESCANEO REAL». Widget Component, Render Target u overlay sobre consola; pantalla LCARS original estática no cuenta. No simular resultados como si fueran conocimiento autoritativo.
6. Reiniciar 3 veces, recorrer entrada→consola→entrada, probar interacción en marcha/parado y tras perder foco; documentar vídeo/capturas y log.

### Matriz de prueba (todos NO_EJECUTADO)
UE07-01 importación aislada; UE07-02 escala humana; UE07-03 tránsito completo; UE07-04 colisiones sólidas; UE07-05 activar consola; UE07-06 salir/restaurar movimiento; UE07-07 independencia de IA remota; UE07-08 materiales y LCARS legibles; UE07-09 reinicio reproducible.

La conexión real de órdenes NPC, detección, conocimiento, eventos y save/load **es F08/Core/F06**, no se presenta como resuelta con una UI de prueba.
