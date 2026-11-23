# H07-P05 — Integración Unreal de consulta institucional v1

Implementación para auditoría, sin certificación H07. Base: P03 `3eb8ca458f64785741fbb1167ae49422a7c67042`. CoreRPG permanece fijado en `76a7b7b485616d8c4994f384a90f123bf333591d`.

## Frontera

`institutional_abi.h` añade cuatro exports independientes de las tablas y estructuras congeladas H05 v1 y Academy v2: versión, submit, poll y current. Reutiliza el mismo cliente, capacidad compartida de ocho tickets, descarte, sesión y cola propietaria. No añade emisión, selección de principal, observador, persona, scope o permiso. El campo `event_id` es únicamente una clave de consulta. F11/Core siguen decidiendo visibilidad y contenido.

La petición de 40 bytes contiene tamaño, versión 1, operación CAREER/PROMOTION, reservado cero, generación, correlación e ID del evento. CAREER exige ID cero; PROMOTION exige ID distinto de cero. La respuesta de 96 bytes contiene tamaño, código, operación, reservado, ticket, correlación, generación, época, revisión Core, ID del hecho y campos tipados de carrera o ascenso. Los valores son códigos F11; la fecha efectiva se presenta como tick Core, sin inventar una conversión al calendario. Un hecho inicial de rango no se transforma en ascenso.

Cada consulta delega en `InstitutionalQueries` de P03. Su worker resuelve el vínculo F05, comprueba procedencia H04 y ámbito antes de llamar al lector. Poll solo consume tickets de su propia extensión; una llamada al poll equivocado devuelve ABI_MISMATCH y conserva el ticket. Las denegaciones conservan ticket/correlación/operación y tienen generación, época y hechos completamente a cero. Evento ajeno y desconocido siguen siendo indistinguibles.

## Vigencia y Unreal

El consumidor serializa llamadas como exige H05. Submit, poll y current usan admisión try-lock: devuelven RETRY ante contención y PENDING mientras trabaja el hilo propietario; no esperan a IO/Core en el Game Thread. El destructor continúa retirándose fuera del Game Thread con las DLL retenidas.

Unreal negocia todos los exports y versión juntos. Una biblioteca anterior conserva H05/H06 y deja esta capacidad SERVICE_UNAVAILABLE. La preparación y UBT requieren ahora las tres cabeceras y las dos DLL de la misma composición Release.

`UHostSessionSubsystem` genera correlaciones monótonas y observa cada ticket mediante referencia débil al UWorld. `UHostWorldProjection::GetInstitutional` entrega una copia solo después de revalidar la época y generación en el HOST. Si current devuelve RETRY, oculta momentáneamente los hechos. No hay copia autoritativa ni expediente persistente en Unreal.

SAVE admitido borra las vistas y descarta sus tickets; CLOSE/RESTORE y cambios de generación hacen lo mismo. Un UWorld retirado descarta sus observaciones. Poll verifica ticket, operación y correlación y vuelve a comprobar vigencia antes de publicar. El getter repite la comprobación inmediatamente antes de presentar; un resultado viejo nunca se reutiliza para la partida recuperada.

## Presentación

El diagnóstico HOST ofrece consulta del expediente propio y búsqueda del ascenso por ID. La ficha de candidatura Academy reutiliza esa vista técnica; el candidato sin comisión obtiene SERVICE_UNAVAILABLE y ningún rango. Los botones no contienen llamadas de emisión ni bindings Blueprint. La recuperación naval usa únicamente el vínculo ya persistido y verificado por H04.

## Pruebas y límites

`host.h07.p05.abi` es un consumidor C real: versiones/layout, poll equivocado, hechos confirmados, correlación, repetición, denegación, expiración al guardar, restauración y cierre. Consume un guardado H04 producido por las pruebas P03 a partir de la salida de un proceso F11 aislado. El productor no forma parte del grafo del HOST de producto.

`StarTrek.H07.Institutional.Roundtrip` usa las DLL reales y controles Slate: restaura ese guardado de laboratorio, compara rango/evento/revisión original, comprueba denegación, SAVE/RESTORE/CLOSE y una nueva candidatura sin comisión. El parámetro H07Expected solo pertenece a esta automatización de desarrollo y contiene metadatos de comparación; el ejecutable de producto no recibe oficiales ni archivos de ensayo incorporados.

El consumidor C detectó que H04 anteponía el prefijo extendido Win32 a raíces con separadores `/`. Se normalizan los separadores con `make_preferred()` antes del prefijo, conservando las comprobaciones de volumen local, ruta absoluta y ausencia de enlaces. La prueba comprueba la ruta entregada por CMake en Windows.

El emisor institucional de producto F11 sigue ausente. Los comandos admitidos continúan devolviendo SERVICE_UNAVAILABLE. No se añade progresión, ceremonia, acuse narrativo, presented_at ni graduación implícita. Las evidencias y sus limitaciones se publican en el informe técnico de esta entrega; una prueba técnica no constituye aceptación humana.
