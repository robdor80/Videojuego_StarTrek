# ASTER — segunda prueba humana: implementación de las tres zonas

Base: especificación completa #212 (`576eeb821b3d834c049a9846017236a3e6821b1e`), sobre #206 (`433096fbfdb2a1f4f50953440fdc9d7243760fe8`). Rama: `codex/f06-aster-tres-zonas-20261123`. **Draft; F06 abierta; aceptación del propietario pendiente.**

## Comportamiento implementado

Los tres marcos permanentes de 3 px conservan rojo a izquierda, azul en el centro y verde a derecha, con proporción inicial 20/38/42 y separadores redimensionables. Mapa arriba y resumen corto abajo; lecturas y acciones contextuales a derecha. El detalle es desplazable y cambia al inicio cuando cambia el objeto o la vista. CONTACTOS incluye el inventario observable completo, con nombres de la carta pública y distinción de transportes por transpondedor, sin asignarles afiliación por su diseño.

ASTER_X1 vuelve a publicar estrella, seis planetas, cuatro lunas, estación, nebulosa, asteroides y sonda de la fuente original. Las seis ciencias planetarias atraviesan la observación enfocada, el contrato de Ciencia y la validación Core. No se copian composiciones ni identidades secretas al mapa.

GENERAL sin selección muestra las bandas ambientales realmente supervisadas; CONTACTOS adapta la ficha al tipo de objeto. SEGUIMIENTO contiene solo objetivos marcados, con navegación, sistemas observados, cambios recientes cuando existen y estado de la transferencia. Las polilíneas utilizan posiciones archivadas, no rutas de Host. ANÁLISIS presenta conocimiento derivado adicional sin repetir la ficha inicial. La orden normal ejecuta una observación enfocada auténtica y devuelve inmediatamente los cálculos; las operaciones temporizadas existentes siguen disponibles en la ABI para los estudios que las necesiten.

Los transportes rutinarios conservan la selección. Una nave desconocida, una discrepancia relevante o una emisión ofensiva interrumpen con contexto coherente en las tres zonas; se conserva la vista, objeto, zoom y desplazamiento anterior. El retorno es explícito. Los avisos ordinarios degradan a los 45 segundos, las emisiones ofensivas duran mientras se miden y las causas resueltas permiten nuevos episodios posteriores. En el fixture QA, la emisión ofensiva cesa a t=420; no se inventa una intención hostil. La avería conserva lecturas históricas y libera el seguimiento dedicado; el oficial puede retomarlo tras la recuperación.

## Contratos y límites físicos

Se añaden interfaces a F06, manteniendo el pin de CoreRPG y los originales F04:

- `f06_deep_analysis`: solo consume conocimiento público autorizado. Aplica Dalton a presión/composición observadas, geometría angular a eslora/distancia y comparación de posiciones e inventarios archivados. Cada resultado identifica sus fuentes públicas. Las presiones parciales se expresan en microbar, la extensión angular en nanorradianes y el desplazamiento en millonésimas de UA. Son modelos estimados explícitos; no certifican habitabilidad, orientación o vulnerabilidades.
- `f06_deliver_evidence`: entrega equipamiento, posiciones enfocadas o informes científicos completos. El receptor obtiene un enlace persistente al registro inmutable Core, con autorización de puesto, control de revisión, vinculación entre sujeto y fuente, idempotencia y parser estricto. El contrato anterior de equipamiento conserva su compatibilidad.
- `f06_contact_tracking`: consulta pública del modo dedicado, sin claves Host. El Host QA revalida autoridad y señal para cada entrega. Al ordenar SEGUIR se entrega el inventario actual; sus cambios se comparten inmediatamente y el movimiento observado se archiva/entrega con cadencia de cinco segundos. Las colas permanecen en el mismo WorldState y sobreviven a otro proceso.

No hay medidas adicionales autorizadas de tripulación, misión, potencia en vatios, química estelar, tecnología interna o puntos vulnerables. La GUI declara estas limitaciones. El blindaje no observable de la nave desconocida sigue filtrado. La carta solo publica nombres de cuerpos detectados. Los recuentos y estados energéticos de los equipos siguen siendo fixtures físicos QA ficticios, no canon. No se añaden LCARS, NPC, modelos 3D sin validar ni universo F13.

## Comunicaciones y persistencia

El guion de voz se genera con identidad, posición, movimiento y señales medidas; se etiqueta como QA y no entrega informes por sí mismo. Enviar informe abre un selector de destinatario. La pantalla confirma entregas reales en lenguaje natural; las fuentes y recibos técnicos permanecen en el protocolo y el archivo exportable. Cambiar el equipamiento observado habilita un nuevo informe del mismo contacto; reintentar el mismo conserva su recibo.

El guardado Core mantiene compatibilidad con `.aster`. El acompañante `.aster.ui.json`, versionado y vinculado por SHA-256, conserva el contexto visual y las notas; sus datos no crean observaciones. Una pareja que no corresponda se rechaza antes de cargar Core. Sin acompañante se recupera el estado Core y se inicia el contexto visual general.

## Verificación y aceptación

Se amplían los contratos nativos con negativos de autoridad, revisión, sujeto/fuente, evidencia inventada, reintento y restauración, además del cálculo físico y la transferencia continua. La prueba Tk real recorre las cuatro vistas, el retorno a la investigación, informes actualizables, ocultación, fin de alerta y recuperación. La matriz de tamaño incluye 1460×825, 1150×700, 2560×1600, 1706×1066 y 1280×800 con distintas escalas Tk. Estos controles no sustituyen el escalado físico ni la aceptación visual del MSI.

Se conservan las campañas separadas de nueve minutos reales a ×1 y ocho horas Core a cadencias ×15/×30/×60. GitHub Actions ejecuta contratos Core/F04/F05/F06 en Windows/Linux, Tk en ambos y la guardia real en Linux. El estado, SHA probado, JUnit, tiempos y limitaciones verificadas se entregan en la PR de implementación y sus artefactos. Los datos temporales de ejecución se mantienen fuera de Git y no son dependencias del producto.

Arranque de doble clic e instrucciones del propietario: `desarrollo/integration/f06/qa/GUIA_PRUEBA_ASTER.md`. No fusionar ni declarar F06 cerrada hasta aceptación humana.
