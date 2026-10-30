# F04 — organización operativa sobre CoreRPG

Corte nativo real, con ABI C y laboratorio Unreal 5.8.2. Core posee todos los
datos persistentes; las reglas Trek interpretan entidades y relaciones. Los
Actors son proyecciones prescindibles. No modifica F02/F03 ni sus dependencias.

## Dependencias y compilación

Core F04: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`, en `core-revision.txt`.
Core F03 permanece en `9c53a33787de13d91eb2abe4da07033ee0fa1dc1`.
Core F02 permanece en `4f282863737bcd8f5add401202a9e1064c133672`.

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/native -G "Visual Studio 18 2026" -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreRPG
cmake --build C:/F04/native --config Release --parallel 4
ctest --test-dir C:/F04/native -C Release --no-tests=error --output-on-failure
```

Para Linux: Ninja, `-DCMAKE_BUILD_TYPE=Release`, sin `-A x64` ni `-C Release`.
El generador compila los IDs y dotaciones nominales del catálogo JSON existente;
las cantidades reales se configuran explícitamente. Cada checkout Core debe estar limpio y en su SHA.
Las 52 pruebas originales incluyen dos procesos CTest distintos para guardar y recuperar
un archivo, comparando byte a byte el futuro reproducido. No son pruebas de UI.

## Laboratorio Unreal

Compilar primero F02 y F03 en directorios nuevos con sus revisiones originales.
El script solo genera un proyecto dentro de BuildRoot y rechaza un laboratorio
preexistente ajeno. No se usa ningún proyecto artístico como destino.

```powershell
./desarrollo/integration/f04/run_f04.ps1 -Stage All `
  -CoreSource C:/F04/CoreRPG -BuildRoot C:/F04 `
  -F02NativeBuild C:/F04/f02-native -F03NativeBuild C:/F04/f03-native `
  -F02CoreSource C:/F04/core-f02
```

El comando ejecuta 18 pruebas reales de UWorld/Actors: F02 6, F03 6, F04 6.
`-NullRHI` valida integración lógica y ciclo de representación; no acredita
una escena gráficamente jugable. El proyecto, DLL, compilaciones y archivos
de campaña generados permanecen fuera de Git.

## Escenario y frontera de confianza

`f04_create(1,"miranda",...)` abre una **muestra sintética**, no Sutherland
canónica: nave 1, población 2, siete tripulantes (3–8,11), civil 9 y almirante
visitante 10 (pasajero, no dotación), plazas 12–14. `passenger` y `admiral`
son dos alias del mismo ID 10, nunca dos personas. Las personas son entidades Core individualizadas una sola
vez por bootstrap; no hay generación al descubrir vacantes. Cada persona tiene
categoría, departamento, rango y cualificación separadas. El relevo 8 tiene
habilitación temporal hasta tick 86400 para probar caducidad.

El visitante tiene además un mandato externo de misión **explícito de prueba**,
importado por bootstrap, limitado a primer contacto. No obtiene mando a bordo,
no puede tocar ingeniería ni cambiar guardias por rango. El capitán tampoco
puede revocar sus órdenes superiores; el emisor las revoca o caducan.

La ABI y sus consultas diagnósticas son para un host confiable que autentica
al actor. No son autenticación de red ni API abierta a scripts/IA. El subsistema
Unreal es código nativo de laboratorio sin funciones Blueprint mutadoras.
La IA solo aporta una propuesta auditada. `cause` referencia documentación o
un incidente validado por el host; no otorga autoridad.

`F04_CONTACT_REVIEW` registra revisión de contexto (bit 1), interferencia
(bit 2), misión (bit 4) y riesgo (bit 8), con responsable, evidencia y ventana.
Una revisión incompleta devuelve REVIEW al intentar contacto. El riesgo
registrado no es un veto universal. Cada intento vuelve a comprobar mando,
revisión y órdenes superiores; no se implementa una simulación diplomática.

## Estado y operaciones

Entidades tipadas: nave/clase, población, personas, plazas, actividades,
nombramientos, delegaciones, mandatos, órdenes externas, revisiones, tareas y
eventos. Referencias usan RelationKind 1–7; escalares usan los 16 bits altos
`0xF000+campo` y 48 bajos para el valor, como relación consigo mismo. Es un
vocabulario de contenido versionado por `SCHEMA=1`; no cambia el formato Core.
Los campos obligatorios, tipos, duplicados, intervalos y exclusividad se
validan al cargar. El archivo no es una firma criptográfica contra edición
maliciosa; su checksum detecta corrupción.

Todas las mutaciones se preparan sobre una copia y se publican por intercambio
tras validación. Las relaciones pasan por ActionEngine; la creación y el
bootstrap usan las API de identidad/población de WorldState. El reloj es
Timeline. Tareas aplazadas se guardan en WorldState y se reautorizan al vencer.
La copia es una transacción temporal, no una segunda autoridad persistente.

`f04_execute` devuelve motivo y revisión; una denegación válida genera evento,
pero no aplica su efecto. Un handle de otra sesión/carga se rechaza sin evento.
El host debe usar la revisión más reciente. `f04_advance` es servicio privilegiado
de reloj: presupuesto agotado publica progreso acotado y devuelve CAPACITY;
reanudar con el mismo horizonte conserva determinismo. Se registran también
los cambios de mando al atravesar comienzos/finales sin Actors.

| Intención | Parámetros específicos |
| --- | --- |
| ASSIGN | target=plaza, aux=persona existente (0 desasigna) |
| DUTY | target=persona, aux=plaza asignada, start/end |
| REST / ONCALL | target=persona, start/end; REST también representa franco protegido |
| ABSENCE | target=persona, start/end, value=LEAVE/SICK/SUSPENDED |
| RELIEF | target=actividad DUTY saliente, aux=persona entrante; desde ahora hasta fin vigente |
| APPOINT | target=persona, value=rol, aux=departamento, start/end |
| DELEGATE | target=persona, value=POLICY, start/end |
| REVOKE | target=nombramiento/delegación/orden; autoridad vigente o emisor externo según tipo |
| MEDICAL | target=persona, value=SICK, start/end, cause=juicio documentado |
| POLICY | value=3 o 4; exige cobertura del siguiente ciclo |
| BRIDGE | value=alerta 1 verde / 2 amarilla / 3 roja (0 equivale a 1) |
| MOVE | target=consola de la guardia propia; ubicación diagnóstica, sin simular viaje |
| SCAN | estación Sensores propia, guardia/aptitud/cualificación/presencia válidas |
| CONTACT_REVIEW | value=bits de revisión descritos arriba, start/end, cause=evidencia |
| CONTACT | target=revisión persistida vigente del comandante actual |
| SUPERIOR | actor con mandato externo, value=dominio, start/end, cause=documento |
| QUEUE | value=SCAN, start=instante de ejecución, end=caducidad, cause |
| RECALL | target=descanso activo, value=deuda positiva, cause=emergencia |
| PROPOSE | Solo registra sugerencia; no aplica su política |

El diagnóstico SCAN persiste RNG y evento; no sustituye la simulación completa
de sensores F06. BRIDGE modifica la alerta en WorldState y permite comprobar
una consecuencia operativa real del oficial de guardia.

El manifiesto distingue disponibilidad, guardia, localización y consola física.
Las plazas distinguen requerida, asignada y cubierta, e indican si el observador
está habilitado actualmente. Ausencias invalidan cobertura sin borrar la plaza;
un relevo usa una persona existente. Descanso exige cancelación explícita por
emergencia con causa y deuda persistente. Francos son intervalos protegidos.
Los patrones 3×8 y 4×6 tienen ventanas consultables [inicio,fin); cambiar patrón
exige mando/delegación y cobertura durante el siguiente ciclo completo.

## Límites del corte

La ampliación de dotaciones está descrita en [DOTACIONES.md](DOTACIONES.md).
La creación general, altas/bajas, plazas y consulta individual/paginada sustituyen
la limitación de nueve personas para campañas nuevas. La muestra ABI 1 sigue
existiendo con sus handles y archivo SCHEMA=1. F04 permanece EN_CURSO.

No incluye: editor visual de flotas; rotaciones
personalizadas más allá de 3×8/4×6; planificación biológica de fatiga por especie;
equidad multisemanal; movimiento por interiores; traspaso completo de conocimiento
durante relevos; motor clínico; totalidad de sistemas técnicos; adjudicación
jurídica de conflictos; iniciativa NPC/órdenes completas F05; UI gráfica jugable.
La prueba de cobertura de 24 h usa agendas sintéticas prolongadas para comprobar
intervalos y vacantes, y **no** valida un régimen laboral saludable. La regresión
Miranda-120 mantiene su cálculo 5+2 separado y no define la dotación de esta muestra.
