# USS Sutherland — último estado guardado

28/10/2026, Europe/Madrid. **Corrección exclusiva de puertas terminada. No continuar con otros trabajos automáticamente.**

Proyecto: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Unreal\SutherlandPlayable01.uproject`.
Mapa: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`.

El bloqueo D04 registrado el 27/10 queda resuelto: los colliders de las hojas penetraban el suelo/retorno inferior. Se corrigieron únicamente los BodySetup de las ocho hojas, sin cambiar mallas visibles, UV, materiales, actores o código. El mapa conserva exactamente su SHA-256 anterior.

## Estado validado

- Ocho hojas / cuatro mecanismos: tres ciclos mecánicos consecutivos por puerta, sin impactos o deriva y con sus colliders acompañando el movimiento.
- D04: tres aperturas automáticas por aproximación real de Quinn desde el puente, tres cierres automáticos y entrada/salida de la cabina existente.
- D01–D03: mecanismos preparados, acceso bloqueado por destinos no construidos. No desbloquear ni permitir caída al vacío.
- Sondas de cápsula: hojas cerradas bloquean; abiertas dejan los tres carriles comprobados libres.
- Reapertura y digest de geometría visible, normales, tangentes, UV y materiales de ocho hojas: sin cambios.
- Seis sillas laterales, capitán, consolas, Quinn y resto del puente intactos en esta intervención.

## Evidencia y recuperación

Leer `INFORME_PUERTAS_20261028.md`.
Datos actuales:
- `Data/doors_20261028_fix.json`: ocho paquetes modificados, todos respaldados.
- `Data/doors_20261028_validation.json`: 18/18 comprobaciones.
- `Data/doors_20261028_repeat_validation.json`: tres rondas por cada puerta.
- `Data/doors_20261028_saved_verification.json`: ocho hojas reabiertas correctamente.
- `Data/doors_20261028_final_integrity.json`: originales intactos; cambios limitados a ocho hojas.

Respaldos anteriores: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Backups\Puertas_20261028`.
Resultado validado recuperable: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\unreal\Sutherland_Ergonomia03_ParteA\Backups\Puertas_20261028\Resultado_validado`.
Mapa activo: SHA-256 `cff10a2af8d8926d85951834d63b31117d0fe3420bb50007ae24ed8be9792d29`.

Abrir con `Abrir_Editor.cmd`, jugar con `Jugar_Standalone.cmd`. No repetir la importación del puente ni aplicar otra vez el script 15. Si una interrupción obliga a recuperar, cerrar Unreal y restaurar únicamente los ocho paquetes de hojas, manteniendo las rutas de Content; conservar ambos respaldos.

El informe de Parte A del 27/10 se conserva como histórico. No se han realizado hoy las fases B, C, D o E, ni se está declarando completada otra fase distinta a esta corrección de puertas. Pies suspendidos, ergonomía y VSM permanecen fuera de alcance.

Cierre seguro: Unreal y Blender cerrados; no quedan importaciones ni guardados controlados activos. Los manifiestos y pruebas anteriores de Parte A son históricos; para estas ocho hojas se debe usar el manifiesto doors_20261028_final_integrity.json.
