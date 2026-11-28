# F06-B — Primera porción de universo materializable (referencia)

**Estado:** trabajo de referencia, no cierre F06-B ni F06/F12/F13. Base main a325c54221806b0f45d29ff7acd4b77ca9e7d208. ASTER probado a534480f216d33e6abc4b40603a738704f208ad1; Core fijado 76a7b7b485616d8c4994f384a90f123bf333591d. No modifica PR #206/#212/#213/#215 ni Core/HOST/UE.

## B01. Inventario y fronteras

| Fuente reutilizada | Papel | Límite |
|---|---|---|
| astro_physics_v1.py (blob f8111892c9c655c84b45c1a42978473eea9a14f0 recuperado de #215 sin cambios) | estrella, planeta, luna, física privada | aproximaciones, no simulación orbital temporal completa |
| generate_v0_0_1_system.py | referencia histórica | no reemplazar ni alterar su oráculo |
| generate_starship_instance.py | clase, configuración, dotación, turnos, identidad | no inventario físico ni manifiesto vivo |
| generate_civilian_starship.py | diseño reutilizable e instancia civil | no carga real ni instalación física |
| perfiles de clase, especies, tecnología y staffing | definiciones y límites | no son por sí solos instancias ni mediciones |
| generate_civilization_first_contact.py; P2 B01–B10; F12 | referencias futuras para causas, economía, población y evolución | no afirmar integración real; no duplicar sus propietarios |
| Core WorldState y F04/F05 | autoridad, identidad, tiempo, población, hechos, persistencia | materialización de este paquete pendiente B11/C |
| F06 / H09-P02 | observación y publicación autorizada | jamás leer directamente este JSON privado desde LCARS |

## Decisiones de alcance

Primer corte deliberadamente acotado a una estrella con planetas/lunas, una D'deridex y cargueros procedurales; catálogo admite Oberth si la selección original la devuelve. Si una clase, diseño, tecnología, especie o rol carece de perfil aprobado, rechazar en lugar de rellenar silenciosamente. La geometría es una descripción paramétrica privada, no un GLB ni una reconstrucción de sensores. Catálogo QA no canónico: valores físicos/energéticos/sistemas de ejemplo, no especificaciones aprobadas del juego. El usuario no ha fijado esos balances; exigir revisión antes de importación productiva. La clase M original se conserva como candidato climático histórico, se añade un cribado humano explícito que evita presentar un M no respirable como apto; no se cambia el canon ni se fuerza O2. La decisión definitiva de nomenclatura/respirabilidad por especie corresponde al autor y Ciencia. La vida planetaria detallada, yacimientos, meteorología, civilizaciones y evolución social siguen fuera de este corte.

## B02–B10

Se añade una composición ejecutable de referencia, con módulos identificables, perfiles por diseño, población individual de ejemplo, asignación a compartimentos, carga vinculada a necesidad y oferta finita, ruta, estado inicial y evolución explícita sin observador. Identidad, revisión, unidades, procedencia y validación son obligatorias. Nunca genera hechos al escanear. Las pruebas verifican tanto invariantes como casos negativos. No es una segunda campaña, ni un simulador F13 completo. El JSON de salida es candidato PRIVADO, no entrada de UE o IA ni archivo de partida.

## Puerta B11 — encargo nativo (Codex, Sol 6.2 medio según preferencia de autor)

1. Auditar primero la costura real de producto H09/F04/F05 y el pin Core. Reconciliar #215, esta PR y main sin mover pines, ni cambiar formatos/oráculos históricos sin aprobación diferenciada.
2. Demostrar materialización y lectura de un candidato validado en el único WorldState y el reloj existente. No tratar el JSON de referencia como autoridad persistente paralela. Las nuevas instalaciones, personas, inventarios, geometría y eventos deberán conservar identidad y procedencia.
3. Diseñar migración, compatibilidad de guardados antiguos, deduplicación y validación al restaurar. Desarrollar adaptador privado, no endpoint público de verdad oculta.
4. Si el pin no admite las propiedades o la evolución transaccional sin comprometer invariantes, detener esa parte y elevar propuesta precisa de ampliación Core al propietario. No improvisar otro motor.
5. Ejecutar pruebas Linux/Windows, guardado/carga, reproducción, aislamiento, regresiones históricas y medir recursos. Las pruebas de sensores y el proveedor galáctico completo pertenecen a C/D; no marcar B como producción por un test Python.
6. Aplicar AGENTS.md: conservar evidencia ligera, eliminar solo laboratorios propios regenerables.

## B12

ChatGPT revisará diff, resultados sobre SHA exacto, procedencia, compatibilidad y bloqueos. B11 y B12 de producto no se certifican hasta ejecución nativa real. No fusionar automáticamente. No usar datos sintéticos como canon ni autorizar su filtración a observadores.
