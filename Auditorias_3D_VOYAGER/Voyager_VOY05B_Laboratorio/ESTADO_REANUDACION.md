# VOY-05B — Estado de reanudación

Fecha: 22 de octubre de 2026. Estado: **PARADA CONTROLADA solicitada por el usuario. Esperar autorización posterior para reanudar.**

Laboratorio: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY05B_Laboratorio`.

Cuota consultada al iniciar la parada: 85 % consumido / **15 % restante** en la ventana de cinco horas; 77 % consumido / **23 % restante** semanal. No se consumió ningún restablecimiento de cuota. Se detuvo con margen, sin esperar al 10 %.

## Alcance autorizado que debe mantenerse

Solo VOY-05B.0 (calibración dimensional), VOY-05B.1 (piloto estático BR_03) y examen sin modificación de Mesh4/5/6/9/11/81. No comenzar VOY-05B.2 ni fases posteriores, animaciones, mecanismos, Unreal, Valhalla ni modificaciones de repositorios. Todo trabajo geométrico debe realizarse en copias. No hay escala definitiva aprobada ni puerta apta para producción.

La reanudación requiere autorización expresa posterior. La entrega completa futura deberá publicarse y verificarse en Drive, pero el usuario ha indicado que **no hace falta publicar esta parada parcial**.

## Trabajo completado y validado

- Leídos los informes técnicos VOY-05A 04 a 11, familias, catálogo y scripts relevantes. Leída la habilidad Google Drive. Listada la carpeta remota de partida y consultados sus metadatos.
- Confirmado Blender instalado: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`, versión **5.2.2 LTS**, hash `d13f752e3b9c`.
- Creado el laboratorio independiente. Copiados físicamente los informes, datos, referencias, fuentes del puente y dos escenas originales de inspección de A.
- **221 originales** comparados con `VOY05A/VERIFICACION/originales_antes.json`: SHA-256 coincidentes tanto al inicio como al detenerse.
- **5.158 archivos de VOY-05A** inventariados al inicio de B y nuevamente comparados al detenerse: todos intactos.
- **216 archivos copiados** comparados con A: coincidentes.
- Cinco JSON nuevos legibles y siete scripts comprobados sintácticamente en la validación de parada. `91_reabrir_copias.py` también fue ejecutado correctamente por Blender.
- Reapertura independiente y sin guardar cambios de ambas escenas copiadas: colección **83 mallas**, puente **630 mallas**; cero imágenes ausentes según las rutas resueltas de Blender.
- Identificación espacial de BR_03 y tres renders exploratorios del marco, sin modificación de geometría.
- Repetición de medidas estáticas por BVH en BR_01 a BR_04: por acceso, 5.808 muestras de anchura, 2.475 rayos superiores y 2.475 muestras de soporte. Se guardan respuestas nulas, objetos intersectados y coordenadas. No hay certificación de paso continuo.
- Estudio preliminar de reservas laterales mediante SAT triángulo/caja, sin desplazar hojas ni crear animación. Las cuatro cajas estudiadas no intersectaron triángulos según ese ensayo; **esto no demuestra que exista una cavidad física cerrada, con holguras, guías o retornos**.
- Medición estática de Mesh4/5/6/9/11/81 y comparadores Mesh12/13/18: topología soldada solo de diagnóstico (10 µm), superficies horizontales con orientación, retícula 41×41 de suelo/techo y referencias de accesos de A.

Certificados: `VERIFICACION/parada_integridad.json`, `VERIFICACION/parada_reapertura_copias.json`. El manifiesto de parada registra los hashes de todos los archivos existentes salvo el propio manifiesto.

## Hallazgos preliminares que deben conservarse

BR_03: raíz de estudio `(1.1911309957504272, 6.38205099105835, 0.7122955561927033)` en coordenadas mundo fuente. +X local = `(0,1,0)` hacia el lado posterior del puente; +Y local = `(-1,0,0)`; +Z = `(0,0,1)`. El destino funcional de ese lado aún debe describirse mediante la arquitectura real, sin inventar una habitación.

Dos grupos de ocho fragmentos, según el inventario de A:

- Grupo con Y local positivo: Mesh_1992, Mesh_1988, Mesh_1990, Mesh_1993, Mesh_1991, Mesh_1994, Mesh_1989, Mesh_1987.
- Grupo con Y local negativo: Mesh_1986, Mesh_1982, Mesh_1985, Mesh_1981, Mesh_1983, Mesh_1980, Mesh_1984, Mesh_1979.

Estos grupos conservan piezas principales, bandas y adornos. Todavía no se han creado colecciones semánticas, pivotes ni jerarquías. Debe definirse explícitamente el punto de vista antes de rotular izquierda/derecha. **Doorpanel_6 es un control**, no una hoja.

Mesh_1832: 54 caras de retorno, intervalo X local aproximadamente `+0.021255` a `+0.123202` m. Mesh_1833: 114 caras, de las que 60 son coplanares a X local `−0.123181` m y 54 cubren retornos hasta `−0.021255` m. Ambos tienen normales personalizadas; cualquier separación debe conservarlas y validarlas por esquina junto con todos los UV. Esta partición es una hipótesis geométrica de despiece, aún sin ejecutar ni aprobar semánticamente.

La ranura central tiene unos 42,51 mm entre retornos y las hojas tienen esa misma envolvente de espesor. Esto no acredita margen funcional. Los mamparos locales no prueban cierre lateral/posterior de un bolsillo; todavía deben inspeccionarse cortes y continuidad.

La malla de rayos más densa detecta anchuras cercanas a 0,648 m cerca de la zona alta redondeada del perfil. **No sustituir sin explicación el ancho de A por ese mínimo:** pertenecen a alturas y planos distintos. Analizar anchura frente a altura, techo frente a posición lateral y respuestas nulas antes de sacar conclusiones. Cero impactos de los rayos transversales dentro del prisma central muestreado no equivale a ausencia de obstáculos en todo el paso.

En las habitaciones se detectan caras de suelo con normales ascendentes y techos con normales descendentes. Mesh4 tiene suelo alrededor de Z=1,110 m y techo Z=3,873 m; Mesh5/6 muestran niveles de suelo alrededor de 0,550 y 1,110 m. **No clasificarlas aún como bloques sólidos por su aspecto exterior ni como habitaciones funcionales por tener suelo:** faltan inspección visual interior, interpretación de desniveles, continuidad y accesos. Las superficies horizontales registradas son áreas trianguladas, no áreas útiles certificadas.

## Trabajo iniciado pero pendiente

- VOY-05B.0: interpretación de mediciones, comparación de formatos, consecuencias de escalas, perfiles antropométricos sintéticos de varias estaturas y anchos, alternativas localizadas/mixtas, vistas comparativas y recomendación. No se ha adoptado ningún factor.
- VOY-05B.1: identificación inicial realizada; **no se ha separado ni modificado todavía ninguna geometría**. Falta mapa fuente→pieza/cara/vértice/bucle, conservación comprobada de materiales/UV/normales, pivotes propuestos, despiece de marco/mamparo, arquitectura con hojas retiradas y diagnóstico de cavidad con cortes.
- Habitaciones: datos obtenidos, pero falta clasificación razonada de las seis piezas y evidencia visual nueva.
- No existen aún informes finales `01_ESTUDIO_DIMENSIONAL.md`, `02_PILOTO_BR03.md` ni `03_ESTADO_HABITACIONES.md`; tampoco escena Blender de piloto ni entrega final autocontenida.
- Faltan todos los paquetes, validaciones de extracción, manifiestos finales y publicación/verificación remota de B.

## Procesos detenidos y estado de las escenas

Los procesos Blender por lotes finalizaron normalmente. No quedó una operación en curso ni se canceló un guardado. No se creó ni modificó ninguna escena de trabajo de B. Las únicas escenas conservadas son **copias físicas intactas** de inspección de A en `FUENTES`; `ESCENAS` permanece reservada para el futuro piloto.

No hay información geométrica pendiente solo en memoria. Los renders exploratorios fueron guardados, junto con JSON, scripts y logs. Ningún temporal necesario fue borrado. No se creó carpeta ni archivo remoto de B.

## Archivos y rutas que deben conservarse

- Laboratorio B completo, incluidos `FUENTES`, `DATOS`, `SCRIPTS`, `CAPTURAS`, `LOGS` y `VERIFICACION`.
- `DATOS/BR03_contexto_exploracion.json` — objetos próximos y límites locales.
- `DATOS/marco_caras_exploracion.json` — índices de caras y límites de Mesh_1832/1833.
- `DATOS/puente_medicion_repetida.json` — todas las muestras nuevas de BR_01 a BR_04.
- `DATOS/BR03_reservas_cavidad.json` — cuatro pruebas estáticas conservadoras; sin cavidad certificada.
- `DATOS/espacios_medidos.json` — nueve objetos, retículas y superficies de diagnóstico.
- `CAPTURAS/EXPL_MARCO_FRENTE.png`, `EXPL_MARCO_OBLICUA.png`, `EXPL_MARCO_DESTINO.png` — exploración, no láminas finales. Azul=Mesh_1832; ocre=Mesh_1833; verde=Doorpanel_6.
- `FUENTES/VOY05A_Puente_Original_Inspeccion.blend`, `FUENTES/VOY05A_Coleccion_Original_Inspeccion.blend`, `FUENTES/PUENTE` y `FUENTES/VOY05A`.
- `VERIFICACION/VOY05A_inicio.json`, `originales_inicio.json`, `parada_integridad.json`, `parada_reapertura_copias.json`, `manifiesto_parada.json`.
- Laboratorio A íntegro: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY05A_Laboratorio`. Mantenerlo de solo lectura en el flujo de trabajo.

## Última operación segura

Verificación de integridad de originales, archivos A y copias; reapertura de las dos escenas copiadas con Blender 5.2.2 LTS, sin guardar ni modificar sus archivos; redacción de este estado y manifiesto de parada.

## Siguiente operación exacta, solo tras autorizar la reanudación

1. Leer este archivo y `VERIFICACION/manifiesto_parada.json`. Verificar hashes de los archivos B que se vayan a utilizar. No volver a ejecutar `00_preparar.py` ni repetir mediciones ya completas.
2. Leer `DATOS/puente_medicion_repetida.json`, `DATOS/marco_caras_exploracion.json` y los tres renders. Crear `SCRIPTS/04_sintesis_dimensional.py` para resumir las medidas por profundidad y altura, separar respuestas nulas, relacionar mínimo superior con el arco y calcular las hipótesis dimensionales. No escalar mallas fuente.
3. Antes del despiece, crear script nuevo que cargue la copia del puente, registre el estado completo de vértices/caras/bucles, UV, materiales y normales de los 16 fragmentos y Mesh_1832/1833, y escriba una escena nueva en `ESCENAS`. Separar únicamente caras justificadas, con correspondencia exhaustiva y pruebas de conservación. No sobrescribir las escenas de `FUENTES`.
4. Continuar el resto de B.0/B.1 y el examen de habitaciones dentro del alcance original; revisar técnicamente antes de publicar.

Drive de referencia A: https://drive.google.com/drive/folders/1UO8mR8A42k3Vde5SFm59HOwWQiW68pVL . Padre remoto observado: `0AK-3Bmq_e2j1Uk9PVA`. En la entrega futura crear una carpeta **hermana independiente** `Voyager_VOY05B_Laboratorio`; no escribir dentro de A. No se han creado enlaces remotos de B.

**No declarar VOY-05B.0 ni VOY-05B.1 completas. La parada es recuperable; el trabajo técnico sigue pendiente.**


## Comprobación adicional previa al apagado del MSI

2026-10-22T11:25:06.714795+00:00 — A petición expresa del usuario, se verificaron los 242 archivos del manifiesto de parada mediante SHA-256: todos coinciden. El laboratorio permaneció estable durante la comprobación; todos sus archivos admitieron apertura exclusiva de lectura, sin bloqueos de escritura detectados. Las dos escenas y sus dependencias conservan los hashes con los que fueron reabiertas correctamente. Scripts y JSON vuelven a ser legibles.

Se prepara una solicitud de apagado completo normal de Windows mediante `shutdown.exe /s /t 0`, sin `/f`, sin `/hybrid` y sin reinicio. Este texto registra la preparación, no certifica que el hardware se haya apagado. Si Windows muestra una aplicación bloqueante, no forzar su cierre. La reanudación técnica de VOY-05B continúa pendiente de autorización. Evidencia: `VERIFICACION/preapagado.json`.
