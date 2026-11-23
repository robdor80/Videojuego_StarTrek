# V07 corregida — lista para recorrer con Quinn

Abrir `ValhallaComputer.uproject` con Unreal 5.8.2 y pulsar Play. El mapa de inicio es
`/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Corregida`.
Controles: WASD, ratón y Espacio.

Desde el vestíbulo, seguir el corredor central hasta cualquiera de los dos círculos.
Las cuatro puertas con ventanas de cada anillo central se abren al aproximarse y
comunican directamente con sus sectores de servidores. Se han conservado las
hojas originales, sus UV, normales y materiales. Son ocho mecanismos nuevos:
SRV_R1_Q1–Q4 y SRV_R2_Q1–Q4.

El problema principal era una identificación equivocada: los seis MEM_C01–C06
validados antes son accesos del perímetro. Las ocho puertas interiores señaladas
en rojo seguían siendo geometría estática; dos pruebas incluso esperaban que
bloquearan a Quinn como si fueran bancos. Ahora se comprueba su apertura y cruce.

También se mantienen las seis puertas azules de servicio. Su retracción hacia
Quinn podía atascarse durante una aproximación descentrada. Usan deslizamiento
lateral por sus alojamientos y detección anticipada de la aproximación. Se han
comprobado ambas direcciones, ocupación, cierre y bloqueo de seguridad.

En el extremo radial señalado en amarillo se reprodujo una caída real en Play:
Quinn podía caminar más allá del último suelo. B10 y B11 cierran los extremos
sin continuación de los dos círculos; B12 protege una junta terminal del este.
Los pequeños rellenos llegan hasta esos cierres. Se conserva el recorrido válido
hasta sus últimos puntos; no se crea una cubierta nueva detrás de los paneles.

Las cajas de escalera tienen sus dos cubiertas superiores y los peldaños existentes
siguen transitables. Se mantienen abiertos los tres accesos a tramos construidos.
Las salidas hacia cubiertas de destino todavía sin construir conservan sus
cierres de seguridad. Esas cubiertas de destino siguen pendientes; no son techos
omitidos de las cajas de escalera. D02–D04 conservan asimismo su bloqueo previsto.

Validación del 6 de noviembre de 2026:

- 178/178 casos funcionales con Quinn y CharacterMovement, ejecutados contra esta
  carpeta de entrega: recorridos, escaleras, puertas, ocupación, cierres, accesos
  descentrados sin espera inicial y límites. Un verificador independiente exige
  cruces físicos de umbral, apertura completa y ciclos completos.
- 396/396 comprobaciones físicas de los 18 mecanismos. Las pruebas de mecanismo
  habilitan temporalmente permisos en el mundo de prueba; no guardan esos cambios.
- Play In Editor con RHI real: recorrido desde PlayerStart a ambos círculos y
  entrada/salida por las ocho puertas interiores, sin teletransportes durante ese
  recorrido. Se observó apertura y cierre. La navegación asistida empleó el
  CharacterMovement de Quinn y no llamó métodos de apertura ni alteró permisos.
- Las seis puertas azules se recorrieron en ambos sentidos en ese mismo mundo PIE.
  Sólo se recolocó a Quinn ante cada acceso para seleccionar el punto inicial;
  los cruces fueron físicos, sin reiniciar las puertas ni sus políticas.
- Entrada real de teclado y salto; caída reproducida antes de reparar el extremo
  y nueva caminata desde PlayerStart hasta el cierre, terminando apoyado en suelo.
- Map Check: 0 errores y 0 advertencias. 621 paquetes locales del juego resueltos,
  sin paquetes de pruebas ni recursos ausentes. Materiales originales conservados.

Esta carpeta es autocontenida. Las evidencias brutas y herramientas desechables
se conservan en el área temporal autorizada del repositorio y no son dependencias
para jugar. No hace falta ejecutar scripts para recorrer el mapa.

Se conservan las entregas anteriores y los Blender originales. Esta es una nueva
V07; no se ha iniciado V08 ni trabajo de rendimiento, ni fusionado la PR #80.

Para reconstruir sobre una copia nueva de V07_Funcional, se incluyen
`prepare_v07_correction.py`, `build_v07_inner_doors.py`,
`build_v07_inner_pockets.py` y `author_v07_correction.py`. Los dos generadores se
usan con Blender; reciben `--geometry`, `--output` y, el segundo, `--doors`.
El script de autoría recibe `VH_INNER_DOORS_MANIFEST`,
`VH_INNER_POCKETS_MANIFEST` y un `VH_EVIDENCE_DIR` nuevo. Debe compilarse el
proyecto copiado antes de importar. Los destinos existentes se rechazan.
El plan de regresión es `Scripts/v07_correction_validation_plan.json`; se revisa
con `check_v07_correction_report.py --plan ... --report ... --output ...`.
