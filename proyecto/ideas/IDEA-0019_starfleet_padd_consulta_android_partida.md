# IDEA-0019 — Starfleet PADD: terminal Android de consulta de la última partida

**Fecha de aprobación expresa:** 2026-11-06.  
**Estado:** **APROBADA CONCEPTUALMENTE; sin implementación ni planificación de fase definitiva.**  
**Decisión del autor:** disponer de una aplicación Android (móvil y tablet) con interfaz LCARS que permita consultar fuera del videojuego el estado registrado de la última sesión de Star Trek, **sin ejecutar el juego, sin simular tiempo fuera de sesión y sin modificar la partida desde Android**.

## Experiencia de juego

- Terminal personal Starfleet PADD con expediente del jugador, retrato/avatar, rango, destino, puesto, responsabilidades, guardias, bitácora, planos/mapas de la nave y datos autorizados de misión.
- Como alférez, acceso a órdenes, horario y expediente propios. Como teniente o jefe de Sensores, acceso a personal, turnos, tareas, disponibilidad y registros del departamento según competencia. Como primer oficial, coordinación transversal. Como capitán, registros de mando y comunicaciones de Flota de su competencia, incluidos posibles expedientes clasificados **solo si el juego los ha generado y autorizado**.
- **Rango ≠ puesto ≠ destino ≠ habilitación ≠ conocimiento.** Los permisos derivan de la autoridad y el conocimiento autoritativos del personaje en la última partida, no de una tabla simplificada que entregue secretos automáticamente al ascender.
- Información de bajas, salud, privacidad familiar, ubicaciones, expedientes clasificados y seguridad debe minimizarse según autorización efectiva; no divulgar diagnósticos ni ubicaciones sensibles indiscriminadamente.
- La app muestra **el último estado sincronizado** y su fecha/hora de juego y de exportación. Nunca anuncia datos «en directo» cuando UE5 está cerrado.

## Arquitectura candidata (sin APIs ni infraestructura aprobadas)

1. **CoreRPG/Star Trek:** única fuente autoritativa de identidades, destinos, roles, conocimiento, eventos y guardados. Un exportador del juego construye una **proyección de lectura** de la partida guardada; nunca publica el guardado bruto.
2. **Filtrado previo a la subida:** comprobar alcance, rol, conocimiento y permisos **antes de exportar**. El snapshot solo contiene información permitida; no basta con ocultar pestañas en Android.
3. **Transporte:** Firebase Authentication + Firestore para metadatos e índices pequeños; Cloud Storage, si procede, para snapshots grandes, mapas y miniaturas. GitHub se considera alternativa de distribución de recursos públicos/versionados, **no** almacenamiento recomendado de expedientes privados de partida.
4. **Android:** Kotlin/Jetpack Compose, LCARS adaptativo vertical/horizontal, caché local de solo lectura y consulta offline; posible uso de RobStyle donde no contradiga la estética LCARS. No requiere MSI ni Unreal en ejecución para consultar una copia ya descargada.
5. **Seguridad:** acceso autenticado, reglas de seguridad por propietario, aislamiento entre usuarios/partidas, cifrado en tránsito y protección de caché local; no incluir secretos de Firebase en el cliente. Revisar borrado, sustitución y revocación de snapshots obsoletos al cambiar permisos.
6. **Sincronización:** exportación tras guardar/cerrar cuando el guardado haya sido confirmado. Fallos de red no corrompen la partida: cola/reintento idempotente con ID de partida, revisión y checksum; evitar snapshots parciales y carreras entre guardados.
7. **Lectura estricta:** **ninguna orden, decisión, cambio de guardia, mutación, tiempo simulado, evento narrativo ni modificación de guardado desde el PADD**. Sincronización unidireccional juego → nube → Android.

## Dominios candidatos

- **Personal y carrera:** avatar, rango, asignación, expediente, trayectoria.
- **Departamento:** dotación, guardias, tareas, ausencias, órdenes e informes permitidos.
- **Mando:** informes de varios departamentos, preparación, órdenes de Flota, clasificación.
- **Bitácora:** eventos ya sucedidos y conocidos por el personaje.
- **Cartografía:** planos **de la configuración real de la nave jugable**, ubicaciones conocidas, sectores y sistemas descubiertos; no revelar zonas o información que el personaje desconozca.
- **Vida a bordo:** camarote, relaciones familiares y mascotas, cuando sus respectivos sistemas existan y el acceso sea legítimo.

## Dependencias y fases

- **F02/F03:** identidad, conocimiento, persistencia y proyección autoritativa.
- **F04/F05:** dotación, tareas, órdenes, delegación y permisos efectivos.
- **F06/F09:** sensores, exploración, sistemas conocidos y datos operativos.
- **F07/F14:** modelos/planos, retratos y recursos visuales de la nave.
- **F11:** progresión de carrera, destino, rango y puesto.
- **F12:** horarios, NPC, familia, residencia y vida a bordo.
- **F15 o integración complementaria posterior:** certificación end-to-end, seguridad, desconexión y regresiones. **No abrir una nueva fase principal ni cambiar F05 por registrar esta idea.**

Subprograma candidato: **PADD-01** contrato de proyección/visibilidad; **PADD-02** exportador y versiones; **PADD-03** Firebase/seguridad/sincronización; **PADD-04** app Android LCARS; **PADD-05** módulos de consulta; **PADD-06** QA y pruebas de regresión.

## Invariantes y casos de prueba

- Con el juego cerrado, tres días reales después, **no transcurre tiempo de juego** ni cambia un turno.
- Un teniente no obtiene datos de ingeniería o secretos de capitán por tener la app.
- Cambio de destino, destitución o pérdida de habilitación no conserva indefinidamente snapshots clasificados antiguos; definir política de revocación y borrado seguro en nube y caché.
- No se muestra un NPC, una orden, un planeta ni un incidente que el World State no tenga y el personaje no pueda conocer.
- La exportación no afecta a los guardados y es recuperable tras interrupciones, desconexión y repetición.
- En móvil vertical y tablet horizontal, LCARS mantiene legibilidad y accesibilidad.

**No implementado:** no existe aún exportador de partida, backend PADD, aplicación Android ni interfaz LCARS funcional. Este documento registra la idea aprobada y sus límites.
