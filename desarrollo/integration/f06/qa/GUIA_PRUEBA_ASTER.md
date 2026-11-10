# F06 · Guardia de sensores Aster — prueba jugable de tres zonas

**Rama de prueba:** `fix/f06-aster-guardia-ux-ciencia-20261110`  
**PR:** #97 (Draft, apilada sobre #96; no fusionar todavía).  
**Objetivo:** validar que un jugador puede actuar como oficial de sensores; las pruebas del motor por sí solas no certifican jugabilidad.

## Arranque mañana en el MSI
1. Cierra la consola antigua y abre GitHub Desktop.
2. Comprueba que estás en `fix/f06-aster-guardia-ux-ciencia-20261110`.
3. Pulsa **Fetch origin** y, después, **Pull origin** (si está disponible).
4. Abre `desarrollo/integration/f06/INICIAR_PRUEBA_ASTER.cmd` con doble clic.
5. Pulsa **Iniciar**. Es un banco nativo real CoreRPG + interfaz temporal Tkinter, no la consola LCARS final de UE5.

El lanzador compila en `laboratorios/f06/qa/build` (fuera de Git). Usa la revisión de CoreRPG aprobada y no modifica modelos Blender/Unreal.

## Organización funcional actual
- **Izquierda / OPERACIONES**: GENERAL (inventario); CONTACTOS (solo nuevas detecciones); SEGUIMIENTO (solo objetivos marcados con SEGUIR); ANÁLISIS (objetos cuyo estudio has solicitado).
- **Centro**: mapa grande con zoom y «Ver todos / Enfocar contacto», más la pantalla del trabajo seleccionado.
- **Derecha**: información observada, armas/defensas habituales de la clase cuando están catalogadas, órdenes y, en CONTACTOS, **COMUNICAR CONTACTO AL OFICIAL**. «Ver ficha técnica» despliega datos adicionales **en esta zona**, no registros de depuración.
- **Avisos superiores**: nuevas naves y posibles maniobras de interceptación son importantes; el reloj baja a ×1 cuando aparece una nueva nave, sin pausar la guardia.

## Guardia de aceptación (la secuencia importante)
1. **00:00**: GENERAL debe inventariar el sistema Aster y permitir seleccionar elementos en el mapa. Al elegir un objeto, el mapa enfoca solo Enterprise y el objeto. El zoom debe funcionar durante el avance del reloj.
2. **01:00**: llega el crucero klingon **Vor'cha**, identificado sin esperar un escaneo detallado. Aster debe cambiar automáticamente a **CONTACTOS**, mostrar un parte en texto legible y bajar la velocidad a ×1.
3. **COMUNICAR CONTACTO AL OFICIAL**: registra la comunicación simulada sin duplicados. El texto usa azimut y elevación **en el marco de sensores** (no «a estribor» sin tener orientación de la nave), distancia y, si existen observaciones sucesivas, rumbo de desplazamiento y velocidad relativa estimada. Este banco NO simula aún la respuesta hablada del capitán ni la interacción por voz.
4. **SEGUIR**: el Vor'cha aparece en la sección SEGUIMIENTO. El motor debe seguir calculando acercamiento, rumbo y posible interceptación automáticamente; no hay que pulsar SEGUIR continuamente.
5. **ANÁLISIS DETALLADO**: acepta la orden durante la guardia y termina en 20 segundos de reloj a ×1, con porcentaje real y resultado conservado. ANÁLISIS se limita a los objetivos estudiados; nunca presenta los datos teóricos de la clase como una lectura verificada de los sistemas de esa nave.
6. **02:00**: al hacerse observable la D'deridex debe poder identificarse; al disponer de nueva posición, Aster debe calcular su movimiento. No ocultar armas conocidas detrás de «consulta el catálogo».
7. **Guardar / Recuperar** desde Opciones de prueba: el estado de Core, las observaciones y las listas operativas temporales se recuperan. La comunicación al oficial también se conserva.
8. Comprobar durante toda la prueba que no saltan la lista ni la ficha al hacer scroll, que las alertas no esconden el pie y que los botones siguen operativos.

## Límites explícitos
- La comunicación con el oficial se registra **en la simulación QA**, no en un NPC/diálogo definitivo.
- Táctica usa la misma proyección de sensores mediante `TACTICAL`; el botón «Preparar informe para Táctica (QA)» comprueba la disponibilidad de la lectura, pero **no equivale todavía a una orden táctica persistida ni a una consola de Táctica terminada**.
- El mapa XY y sus magnitudes son las observaciones públicas del Core en el escenario. Falta la orientación real del casco para transformar el azimut en marcación relativa de proa/estribor; no inventamos la referencia.
- La velocidad es una estimación basada en dos observaciones, expresada en UA/s; no se infiere factor warp sin medición.
- Los escaneos detallados conservan resultados de sensores, pero aún no pueden certificar estado de todas las armas, escudos, sistemas internos y tripulación.
- No confundir **prueba jugable en Windows** con integración visual y funcional definitiva en **UE5**.

**F06 sigue abierta** hasta las pruebas reales del operador y revisión de integración/contratos reutilizables con Unreal.
