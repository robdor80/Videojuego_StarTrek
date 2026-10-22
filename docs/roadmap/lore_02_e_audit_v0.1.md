# LORE-02 E — Auditoría transversal y preparación para implementación (v0.1)

**Fecha:** 2026-10-22. **Repositorio:** `robdor80/Videojuego_StarTrek`. **Alcance:** diseño documental de LORE-02 A–D, sin runtime, sin cambios en CoreRPG o UE5.

**Estado del expediente:** `IN_PROGRESS / DRAFT / PENDIENTE DE APROBACIÓN DEL AUTOR`. **No afirmar LORE-02 E ni todo LORE-02 como COMPLETE** antes de aprobación, fusión y verificaciones posteriores en `main`.

## 1. Línea de base y trazabilidad

- A: PR #31, 14 fichas iniciales más 45 ampliadas = **59** tecnologías; 9 operadores y 14 familias de instalación; 14 + 36 = **50** escenarios de prueba documental.
- B: PR #33, **73** equipos, 15 perfiles de dotación y 6 plantillas; 45 escenarios adversariales.
- C: PR #34, **26** perfiles xenoclínicos, 38 condiciones, 26 procedimientos, 13 agentes, 38 rutas clínicas, 9 instalaciones, 12 perfiles profesionales, 13 perfiles interculturales y 62 casos adversariales.
- D: PR #35, commit de fusión `2f5e2c15fe0f6d5c638da662b74ab6328ff68a1e`; **14** disciplinas, **20** fenómenos, **9** métodos, 6 instalaciones, 10 roles y 10 casos científicos. Política de legado y cinco decisiones de autoría preservadas.
- Estado CoreRPG consultado: `main@4f282863737bcd8f5add401202a9e1064c133672`, con cabeceras/contratos genéricos y documentación hasta **4.13**. No se encontró evidencia documental de un adaptador operativo para esta colección Star Trek. Las validaciones aquí no son pruebas ejecutadas de CoreRPG ni de UE5.
- Verificación inicial a través de contenidos reales: IDs de tecnología 59, de equipo 73, de medicina y ciencia coincidentes, **370 enlaces cruzados** recorridos en la muestra estructural y **225 referencias de procedencia** contrastadas con **501 fuentes**. Se ajustó el tratamiento de `possible_agent_links`, que es lista de objetos con `agent_ref`, no de cadenas.
- Las comprobaciones reproducibles y negativas se incorporan al script `tools/validation/validate_lore02_e.py` y `tools/validation/test_lore02_e.py`, y a `.github/workflows/lore02-e-integration.yml`. Sus resultados definitivos son los de Actions, no estos recuentos preliminares.

## 2. Hallazgos, clasificación y resolución

| Ref. | Grado | Situación observada | Resolución / pendiente |
|---|---|---|---|
| E-ADM-01 | Administrativa, comprobada | `CONTENT_STATUS.md` presentaba D `IN_PROGRESS` pese a PR #35 fusionada y E `TODO` pese a iniciarse auditoría. | Corregidos D `COMPLETE` documental y E `IN_PROGRESS` en rama E; nunca cierre de E sin autorización. |
| E-VAL-02 | Regresión, comprobada | Validadores A y D exigían literalmente el antiguo estado D/E, lo que rompería CI tras regularizarlo. | Ajustadas expectativas y mutación negativa de D para exigir fase fusionada sin admitir regresión. |
| E-IDX-03 | Documental, comprobada | README de Tecnología, Equipamiento, Medicina y Ciencia usaban redacción anterior a las fusiones. | Índices actualizados preservando la distinción entre estado del bloque y `NEEDS_REVIEW` de fichas no importables. |
| E-DATA-04 | Controlado, no crítico | Los cuatro bloques tienen identificadores y fuentes propios, pero *no* un único formato runtime ni un mapeo de entidades CoreRPG para instalación, inventario y conocimiento individual. | No inventar API ni converter. Registrar adaptadores posteriores; entradas de LORE no se convierten directamente en WorldState. |
| E-CANON-05 | Reserva para implementación | La disponibilidad por era, clase, operador, refit e instalación real no puede inferirse de la sola existencia de una ficha tecnológica; parte de A procede de fuentes secundarias o inferencias acotadas. | Mantener ausencias como «no investigado», no como prohibición universal. No modificar canon ni declarar compatibilidad sin prueba por instancia. |
| E-CROSS-06 | Riesgo de seguridad de información | Un hallazgo científico, dato clínico u Omega no debe filtrarse a IA, capitán o NPC por el simple hecho de figurar en los catálogos. | Contratos de observador, autorización y mínimo necesario como prerrequisitos del futuro adaptador. Tests negativos documentales de estos invariantes. |
| E-LEG-07 | Diferencia entre diseño y capacidad | Flujo descubrimiento → validación → ingeniería → astillero → pruebas → adopción está aprobado pero no implementado. Reconocimiento «Sensores Rise» es ejemplo, no item instalado. | Prohibir nombre/invento automático, créditos sin equipo o diálogo de uso sin instalación certificada. Reservar diseño de estado/acciones futuro. |

**Discrepancias de canon que requieran reescritura inmediata de las decisiones del autor:** ninguna identificada en esta auditoría estructural. **Lagunas con incertidumbre:** persisten fuentes no primarias, requisitos cuantitativos sin certificar, acceso Omega y compatibilidades particulares. No se resuelven de forma silenciosa ni constituyen bloqueo de la **coherencia documental**; sí pueden bloquear una implementación específica.

## 3. Contratos compartidos y fronteras

| Dominio | Fuente documental | Titular de verdad futura | Control necesario antes de usar |
|---|---|---|---|
| Tecnología de nave y estación | A, matriz temporal y contrato de capacidad | CoreRPG/Host para instancia, recursos y autorización | Época, operador, clase, diseño, refit, instalación, energía, estado y órdenes |
| Equipo personal | B, modelos de inventario/objeto | CoreRPG, inventario y acciones validadas | Titularidad, entrega, localización, estado, consumibles y acceso |
| Paciente y asistencia | C, privacidad/estado clínico | CoreRPG, proyección autorizada al actor | Identidad clínica, consentimiento, profesional habilitado, diagnóstico no omnisciente |
| Investigación y sensores | D, contratos de observación y conocimiento | CoreRPG, conocimiento/visibilidad por observador | Fuente, instrumento instalado, calibración, fecha, error, permisos, evidencia |
| Hallazgo y legado | Decisiones D y política JSON | CoreRPG para IDs, tiempo, validación, reconocimiento, historial | Colaboradores/NPC, aval independiente, aprobación institucional, nombre no automático |
| Reforma en astillero | Flujo D, contratos de nave e instalaciones A | CoreRPG para obra, recursos, nave modificada y certificación | Proyecto viable, astillero real, tiempos, piezas, pruebas posteriores, adopción gradual |
| Conversación de NPC e IA | Autoría filtrada y proyección de conocimiento | Ninguna autoridad de escritura para IA | Información visible a actor, consistencia temporal, confidencialidad, estado real |
| Visualización e interacción 3D | Futuro proyecto UE5.8.2 | Sin autoridad sobre estado del mundo | Representar acciones y resultados autorizados; nunca conceder capacidades por escena |

**Regla de unificación:** `definition_id` editorial no es `entity_id` de CoreRPG; `exists_in_catalogue` no implica `known_by_actor`, `installed_on_ship`, `authorized_for_use`, `safe_to_use` o `working_now`. Esta auditoría no define un esquema de persistencia duplicado ni inventa API de CoreRPG.

## 4. Matriz de preparación para futura implementación

| Sistema/conjunto | Preparación documental | CoreRPG, dependencia real | UE5, dependencia futura | Adaptador / dato pendiente | Prioridad futura | Condición mínima de prueba jugable |
|---|---|---|---|---|---|---|
| Tecnología A, era y naves | Catálogo cualitativo y escenarios | Entidad nave, estado, acción, persistencia | Consola y estados visibles | `technology_id` → definición/instancia; matriz clase/refit | P1 | Nave con módulo instalado y otra sin él; comparar denegación |
| Equipamiento B | 73 fichas, 15 dotaciones, negativos | Instancias únicas, actor, inventario, recursos | Objeto equipable, UI, animación | `equipment_id` → objeto materializado, permisos/consumo | P1 | Dos personajes, equipo entregado/no entregado, agotamiento |
| Sensores e investigación D | 14/20/9, observación parcial | Visibilidad y Knowledge, acciones, reloj/eventos | Lecturas, informes y laboratorio | Modelo observación con evidencia y caducidad, ejecución offscreen | P1 | Falso positivo, sensores averiados, dos observadores distintos |
| Medicina C | Atlas, clínica y privacidad | Estado individual, conocimientos, roles, permisos | Enfermería, instrumento y diálogo | Historial clínico seguro, eficacia contextual, no dosis universal | P2 | Diagnóstico incierto, consentimiento, reserva de historial |
| Instalaciones A/C/D | Roles y necesidades de capacidad | Localización, módulos, personal, recursos | Naves, estaciones, astilleros, salas | IDs de instalaciones persistentes y disponibilidad por instancia | P2 | Mismo procedimiento con/sin módulo o personal disponible |
| Carrera científica autónoma | Etapas y legado aprobados | Agenda/tiempo, NPC, proyectos, recursos | Acciones opcionales e informes | Investigación offscreen y trabajos de varios NPC | P2 | Descubrimiento ajeno al jugador con consecuencias limitadas |
| Transferencia a tecnología | Ciclo 8 pasos aprobado | Entidades de diseño, revisión, estado de refit | Obra en astillero y pruebas | Proyecto de ingeniería/orden de trabajo y certificado por nave | P3 | Instalar en una sola nave sin alterar otra |
| Reconocimiento «Rise» | Semántica y persistencia aprobadas | Créditos, identidad, nombres, memoria del NPC | Diálogo y consulta histórica | Nombre validado, alias, visibilidad individual, cambios de carrera | P3 | Tras años, NPC informado nombra tecnología; ignorante no |
| Omega y gusanos espaciales | Excepciones autorales escritas | Conocimiento clasificado y tránsito bajo reglas | Misiones/visualización posteriores | Diseño narrativo Omega especial; rutas raras en atlas | P3 | Sin salto temporal, sin Omega general, tránsito solo ruta validada |

**P1–P3 son prioridades propuestas para el futuro y no autorización para desarrollar esta fase.**

## 5. Pruebas y criterios de cierre

1. Validador E: unicidad de IDs, cantidades registradas, integridad de referencias entre A/B/C/D, fuentes, rutas conocidas, privacidad/estado y preservación de decisiones D.
2. Pruebas E de mutación: introducir orfandad, falsificar canon/fuentes, filtrar privacidad, permitir viajes temporales o Omega ordinario, premiar nombres automáticos, saltar astillero o cerrar E sin autorización debe ser rechazado.
3. Regresiones en CI: validadores/test anteriores A–D, LORE-01 A1–E y tests de referencia F07–F15. Todos documentales/offline; no sustituyen pruebas de UE5 ni CoreRPG.
4. Verificación de workflow/pr después de cada cambio; no dar CI como verde antes de ejecutar y consultar GitHub Actions. La rama E no equivale a fusión.
5. **Aprobación humana y fusión posterior**: sólo el autor autoriza pasar E y LORE-02 a cierre completo. Entonces, y sólo tras verificar `main`, podrá elevarse estado e índice principal.

## 6. Pendientes explícitos fuera de alcance

- No hay Content Pack Star Trek certificado contra contrato CoreRPG 0.1.0 ni puente específico de estado/acciones/visibilidad implementado.
- No se ha comprobado en Unreal el ciclo de investigación, materialización de equipo, enfermería ni reforma en astillero.
- La misión especial Omega obligatoria se reserva para narrativa futura, nunca se elimina ni se implementa aquí.
- Tampoco se implementa viaje temporal jugable. Agujeros de gusano raros deben conectar anclas reales de LORE-01.
- La revisión de episodios/fuentes primarias para cada detalle tecnológico y clínico cuantitativo sigue pendiente antes de codificar capacidades.
- Las fichas `NEEDS_REVIEW` siguen siendo editoriales, aunque A–D hayan sido fusionadas.

**Criterio de propuesta:** si CI está verde y no hay errores críticos de consistencia, presentar la PR Draft al autor para revisión. Su fusión requerirá autorización aparte.
