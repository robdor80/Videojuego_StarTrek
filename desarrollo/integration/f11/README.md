# F11-P05-A02-01 — Primer ascenso nativo

Implementa exclusivamente `ensign (1101) → lieutenant_junior_grade (1102)`.
Reutiliza `F04Session`, `Campaign`, `ActionEngine`, Timeline y persistencia Core.
No modifica CoreRPG, su pin, las estructuras C anteriores ni el estado del roadmap.

## Microplan y frontera de confianza

1. Añadir vocabulario Trek opt-in, con campos desde 256, sin renumerar F04/F05.
2. Comisionar dos oficiales concretos mediante el bootstrap **privado nativo**
   del escenario de ensayo autorizado. Cada uno tiene graduación, orden de
   comisión separada y comisión en Core. Ninguna plantilla ni carga convierte
   `RANK=0/1/8/10` en un oficial F11.
3. Registrar oficina institucional, raíz de procedencia, concesión con dominio,
   transición exacta, ventana y revocación, evaluación y orden aprobada en el
   mismo WorldState. El capitán y el almirante de F04 carecen de esta concesión.
4. Validar referencias y confirmar grado e historial juntos; conservar evento
   e idempotencia durante persistencia completa y segmentada.
5. Probar Core real, restauración en otro proceso y regresiones con ambos pins.

`TrekF04Bridge` de producto no exporta emisión de identidad, comisión, concesión,
evaluación ni aprobación. Tampoco existe una operación F04/F05 para hacerlo.
El emisor compilado del ensayo está en `src/f11_trial_host.inc`, solo incluido
en **TrekF11TrialHost**, una biblioteca de pruebas separada. Su factoría no
recibe hechos, identidades, actores, JSON ni banderas de verificación del cliente.
La autorización de este escenario procede del encargo A02-01; sus antecedentes
son hechos de bootstrap de prueba, no una graduación jugable ni una evaluación
producida por los sistemas futuros B1. La emisión de órdenes de una campaña
de producto requiere conectar un Host institucional nativo de confianza; este
corte no añade un endpoint que permita a un usuario acreditarse como ese Host.

La ABI continúa dentro de la frontera nativa local de F04: un único hilo
propietario y almacenamiento de guardados controlado por el Host. Los números
de entidad y `F04Ref` no autentican usuarios de red. La raíz conserva procedencia
de contenido; su código de fuente no es una contraseña ni una firma. El checksum
Core detecta corrupción, **no autentica un archivo completamente falsificado**.
La aceptación de archivos externos no confiables requeriría autenticación por
el Host antes de `f04_load`/`history_open`; no se introduce una falsa garantía
criptográfica ni se cambia el motor genérico para simularla.

## Esquema aditivo v1

La identidad profesional son tres escalares de persona, 48+48+32 bits, con
unicidad en el mundo y comprobación de los 32 bits bajos. Se genera desde
entropía nativa independiente de semilla Core, nave, puesto, nombre o EntityId.
Se conservan versión, estado de servicio, comisión y evento vigente de rango.

Tipos: `f11_root`, `f11_office`, `f11_grant`, `f11_graduation`,
`f11_commission_order`, `f11_commission`, `f11_evaluation`, `f11_cause`,
`f11_personnel_order`, `promotion`. Son definiciones `trek.f04:*` en el catálogo
existente. El validador F04 comprueba formas exactas, duplicados y campos
obligatorios; el validador F11 comprueba identidad, tipos, cardinalidad,
procedencia, coherencia de comisión/rango/evaluación/orden y expediente único.
La presencia de `F11_VERSION=1` y definiciones F11 activa la extensión del
archivo; la revisión SCHEMA de organización F04 permanece independiente.
Un lector sin F11 rechaza estas definiciones; no las degrada ni elimina.

Todos los hechos F11 se retienen residentes durante consolidación, incluidas
órdenes caducadas y tombstones de deduplicación. Se conserva el límite existente
de capacidad; no se promete expediente ilimitado ni reducción destructiva.

## Operación y errores

La firma C efectiva es:

```c
uint32_t f11_commit_promotion(F04Session*, const F11PromotionRequest*, F11PromotionReceipt*);
```

`include/f11_promotions.h` define estructuras nuevas, sin modificar las antiguas.
La petición aporta identidad, referencia de sesión, revisión esperada, key y
referencias a hechos Core ya aprobados. No hay un campo `verified`, cargo que
conceda autoridad ni texto de IA que se interprete como autorización.

El lookup de la key precede al control de revisión y autorización viva. Se
compara identidad, persona y **todos los datos semánticos**, incluyendo fecha,
causa y referencias. Scope y revisión son precondiciones, excluidas del payload:
hay que renovar el scope al cargar y se puede conservar o refrescar la revisión
en un reintento ya confirmado. La key igual con payload diferente da conflicto.
Key nueva después del ascenso se deniega. Un reintento tras revocar la concesión
solo devuelve el recibo del hecho pasado, sin conceder autoridad nueva.

Una petición nueva comprueba revisión, comisión, identidad, servicio, rango,
evaluación del mismo tramo, concesión institucional viva y orden exacta. La
fecha debe coincidir con Timeline actual. Se prepara un único `promotion` y
el cambio de grado/puntero de rango en una copia temporal, se valida y se
revalidan los requisitos vivos inmediatamente antes del intercambio. Ninguna
denegación registra eventos ni consume RNG. Confirmar memoria requiere después
guardar o publicar generación para reconocer durabilidad en disco.

Se reutilizan errores F04 de argumento, scope, revisión, tiempo, almacenamiento,
hilo y capacidad. Los errores F11 200–206 distinguen falta de comisión,
autoridad, evaluación, rango, conflicto idempotente, identidad y orden
(valores definidos en el header). El recibo fallido tiene solo `status`;
el correcto conserva el ID histórico y revisión original, junto a revisión
actual separada. `f11_personnel` y `f11_promotion` son consultas del sujeto para
el Host; el mando de nave no obtiene automáticamente acceso al expediente.

## Evento para issue #104

`promotion` contiene ID Core estable, identidad completa, persona, nave/plaza
y departamento al producirse, rango anterior/nuevo, comisión, evento previo,
evaluación, causa documentada, orden, concesión, oficina, raíz de procedencia,
key, revisión de entrada y commit, fecha efectiva y visibilidad
`F11_SUBJECT_AND_PERSONNEL`. La consulta nativa proyecta estos datos desde Core.
El origen es el bootstrap institucional; la fecha es el tick de campaña, no
una fecha de sistema. No existe diálogo almacenado ni `presented_at`.

La distinción entre efecto legal y comunicación queda preservada: no se
espera a una escena para confirmar el rango. Cola/acuse C, presentación D,
E2E E, traslados B3 y los demás ascensos permanecen pendientes. No hay UI,
ceremonias, PADD ni cambios de permisos de mando.

## Reproducción

Preparar CoreRPG limpio en **76a7b7b485616d8c4994f384a90f123bf333591d**.
`OUTPUT` y los checkouts temporales deben estar en el laboratorio autorizado
del encargo; ninguna fuente depende de su ubicación. Requiere CMake 3.25+,
C++20, Python 3, Git y el jsoncons fijado por F05.

```sh
cmake -S desarrollo/integration/f11 -B "$OUTPUT" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCORERPG_SOURCE_DIR="$CORE_SOURCE"
cmake --build "$OUTPUT" --parallel 4
ctest --test-dir "$OUTPUT" -R '^f11\.' --output-on-failure
ctest --test-dir "$OUTPUT" -E 'history_campaign_|persistence_baseline_|persistence_resume_' --output-on-failure
```

La segunda selección replica la recomendada por F05 e incluye su regresión
nativa completa y F04 de corto plazo. Las campañas `history_campaign_*` exigen
el pin histórico independiente **89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98**;
su runner comprueba ese SHA y no son compatibles con la selección F05/F11.
Los diagnósticos de límite monolítico `persistence_baseline_*` y sus resumes
pueden ejecutarse por separado; no acreditan campañas largas completadas.

Para F04 estable, configurar otro OUTPUT desde `desarrollo/integration/f04`,
sin opciones F05/F11, con Core limpio en
**c147d81ed069da2e09149613ab02cbc3ebe95a4a**, compilar y ejecutar CTest.
Los pins y checkouts Core permanecen intactos.

```sh
python -m unittest discover -s desarrollo/tools/validation -p 'test_f11_*.py' -v
python desarrollo/tools/validation/validate_roadmap_state.py
```

Las 340 pruebas offline son referencia y contrato, no evidencia de ejecución
Core. Las pruebas C++ F11 cubren ascenso, negativas, autoridad, identidad,
idempotencia, cinco fallos de preparación/publicación, archivos corruptos,
archivos legacy, consolidación/recuperación, ABI y dos procesos guardar/cargar.
Otra prueba enlaza el puente de producto y reproduce el mismo ascenso,
guardado/carga y recibo sin acceso a ningún símbolo del emisor de ensayo.
NullRHI, D3D12, MSVC/DLL e interacción UE5 requieren el MSI y deben registrarse
como no ejecutadas desde Linux. No se declara F11 completada ni UE5 jugable.
