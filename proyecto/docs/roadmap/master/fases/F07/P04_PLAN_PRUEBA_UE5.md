# F07-P04 — Montaje y recorrido UE5 Sutherland

**Actualizado 23-10-2026. EN_REVISION.** El texto del 13-10-2026 describía una prueba aún no ejecutada; **posteriormente sí se comunicaron importación, recorridos, puertas y colisiones en el MSI**, pero no se han anexado aquí los logs/escenas originales. [Acta de reconciliación](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md).

El nivel sugerido inicialmente era `L_F07_Sutherland_Transit_Test` bajo `Content/StarTrek/Prototypes/F07/Sutherland/`, **no una ruta verificada**. Localizar el nivel realmente usado y documentar su versión. No sobrescribir `Kelvin_Bridge_Test` ni `Kelvin_Bridge_ThirdPerson_Test`.

## Matriz UE07 y estado sin sobreafirmaciones

| ID | Criterio original | Estado al 23-10-2026 | Qué falta cotejar |
|---|---|---|---|
| UE07-01 | Importación aislada | **REPORTADO_PENDIENTE_COTEJO** | Mapa aislado, parámetros GLB, versión UE5, hash del derivado y logs. |
| UE07-02 | Escala humana | **REPORTADO_PARCIAL_PENDIENTE_COTEJO** | Se reporta locomoción de personaje; medir cápsula/Quinn y alturas reales. |
| UE07-03 | Tránsito completo | **REPORTADO_PARCIAL_PENDIENTE_COTEJO** | Recorridos locales reportados; evidenciar específicamente entrada/turboascensor → Sensores → salida sin bloqueantes. |
| UE07-04 | Colisiones sólidas | **REPORTADO_PARCIAL_PENDIENTE_COTEJO** | Puertas/circulación reportadas; revisar colisiones del mapa final, variantes y logs. |
| UE07-05 | Activar consola Sensores | **NO_EJECUTADO en expediente** | Ensayo específico de actor trigger/line trace, foco/UI en castellano. |
| UE07-06 | Salir y restaurar movimiento | **NO_EJECUTADO en expediente** | Ensayo específico de cierre UI, devolución de cámara/input, fallo de foco. |
| UE07-07 | Independencia de IA remota | **NO_EJECUTADO en expediente** | Ensayo offline/sin servicio remoto, claramente de interfaz demostrativa. |
| UE07-08 | Materiales y LCARS legibles UE5 | **NO_EJECUTADO en expediente** | Ensayo visual en UE5; una edición PBR en Blender no acredita esto. |
| UE07-09 | Reinicio reproducible | **NO_EJECUTADO en expediente** | Tres reinicios y repetición documentada de recorrido + UI. |

Estos estados son de **documentación y trazabilidad**: `NO_EJECUTADO en expediente` significa que no consta una prueba aceptable en el registro, **no** demuestra que nadie la haya intentado localmente.

## Pruebas relacionadas, fuera de la matriz oficial estricta

- **Puertas:** se comunicó una suite local de **50/50** pruebas superadas.
- **Circulación/colisiones:** se comunicó **44/44** pruebas superadas.
- **Sillas F07-CHAIR-02:** **59/59** comprobaciones reportadas, bases aprobadas, retranqueo 27 cm, avance 57 cm en 1,9 segundos.
- **Sentado F07-SEAT-01:** **NO APROBADO**; once poses de muestra con intersección asiento/muslos.
- **Materiales:** pruebas artísticas PBR en Blender reportadas, no verificadas en UE5 aquí.

Estos recuentos se anotan como **resultados comunicados**. No se han inspeccionado sus informes originales desde GitHub. No convierten automáticamente UE07-03/04 en `PASS` general.

## Guion pendiente de aceptación integrada

1. Identificar mapa y modelo exactos importados; registrar captura, configuración, origen y checksum.
2. Comparar alturas/cápsula del personaje con la geometría y completar rutas de entrada → Sensores → entrada.
3. Comprobar colisiones continuas, puertas operativas y ausencia de clipping/bloqueantes en la **variante que se pretenda aceptar**.
4. Implementar/probar una interfaz de **demostración** «SIN CORE / SIN ESCANEO REAL»; abrir consola, ceder input y volver al personaje al cerrar.
5. Probar con/sin IA remota y variaciones de foco/movimiento.
6. Validar la legibilidad de materiales, texturas emisivas y pantalla de consola **en UE5**.
7. Ejecutar tres reinicios, registrar vídeos/capturas/logs y actualizar cada UE07-XX solo con evidencia cotejada.

La integración real de órdenes, NPC, detección, conocimiento, eventos y save/load corresponde a F08/Core/F06. **No declarar F07 cerrada por haber realizado únicamente locomoción, puertas o mecánica de sillas.**
