# H01-P03 — Confianza local, identidad y procedencia v1.0

Fecha: 2026-11-11. Estado: DISEÑADO, NO IMPLEMENTADO. Entorno: un jugador, ejecución offline, sin servidor.

## Modelo de confianza proporcional

HOST puede defender la coherencia del ejecutable legítimo contra solicitudes falsas de UI/IA, scopes erróneos, restauraciones defectuosas y archivos corrompidos. No puede demostrar de forma fuerte la identidad del propietario que controla el ejecutable y disco. Checksum, hash y manifiesto local detectan errores accidentales pero NO acreditan autoridad institucional: pueden modificarse juntos. No implantar servidor, cuentas ni criptografía con secreto en el cliente como solución ficticia.

| Objeto | Fuente válida | Nunca equivale a |
|---|---|---|
| Principal local | Sesión creada/recuperada por HOST | Cuenta externa o funcionario de Flota |
| Campaña | Contenido Core admitido y ranura HOST | Derecho a conceder rangos |
| Personaje jugador | Entidad Core vinculada de forma controlada | ID aportado por UI/LLM |
| Actor/observador | F04Ref resuelto de sesión activa | Token de autenticación |
| F11CharacterId | Identidad profesional en Core | Permiso profesional |
| F04Request.cause, CAUSE=110501 | Causa o referencia del dominio/fixture | Credencial institucional |
| Procedencia del archivo | Evaluación operativa HOST | Firma infalsificable de la Flota |

El vínculo principal-campaña-personaje se valida al comenzar y después de restaurar. f05_bind_player se usa por la iniciativa F05, no para autenticar al usuario. HOST no replica rangos, conocimientos, evaluaciones, permisos ni expedientes F11.

## Clases de procedencia operativa

- CREATED_LOCALLY: campaña recién creada por flujo controlado HOST.
- KNOWN_LOCAL: guardado producido por HOST, manifest y ruta consistentes y Core lo acepta.
- IMPORTED_UNVERIFIED: archivo externo válido o no; no proviene de un flujo demostrado.
- REJECTED: corrupto, incompatible, no admisible o fuera de límites.

Las clases son información auxiliar de IO, no hechos Core. Política de H04: nombres y rutas canónicas bajo raíz autorizada, límites de longitud/tamaño, enlaces simbólicos controlados, validación Core antes de swap y publicación durable tras copia segura. Un archivo importado no se convierte silenciosamente en KNOWN_LOCAL. Puede habilitarse inspección inocua de solo lectura o denegarse; habilitar operación institucional requiere política separada F11 y no basta validarlo como save de Core. Rechazo conserva archivo y sesión buena. Migración en nueva ruta y backup, no sobreescritura de origen.

## Superficies de acceso

| Superficie | Puede | No puede |
|---|---|---|
| UI/Blueprint | Pedir intención tipada y consultar vista filtrada | Pasar F04Session o forzar actor/permission |
| NPC | Solicitar acciones de dominio con competencia y conocimiento | Leer diagnósticos como hechos |
| LLM | Recibir F05AiContext mínimo y devolver propuesta | Leer WorldState/save bruto, dar comisiones |
| PADD futuro | Ver hechos conocidos Y permitidos | Exportar secretos o cambiar campaña |
| HOST | Resolver vínculo, hilo, revisión, ranura y canal | Calcular merecimiento de ascenso |
| F11 producto | Validar autoridad y efectuar actos profesionales | Creer verified=true procedente de UI |

F11_READ_PERSONNEL se ejecuta exclusivamente cuando HOST ha comprobado identidad y divulgación. Respuestas denegadas vacían buffers. F11_INSTITUTIONAL_COMMAND permanece SERVICE_UNAVAILABLE hasta que el proyecto principal F11 aporte API interna certificada. Nunca compilar ni enlazar f11_trial_host.inc en HOST producto.

## Matriz de ataques a probar

1. F04Ref de otra generación, mismo id de otra campaña, actor falso por IA o GUI.
2. Archivo truncado, manipulado, traversal, symlink, versión incompatible y manifest falsificado.
3. Save importado con F11CharacterId, CAUSE=110501 o rango supuesto: no constituye autoridad.
4. Delegación revocada y expected_revision caducada entre consulta y ejecución.
5. Salida IA fuera de context y callback tardío tras restore: ninguna mutación.
6. Lector F11 con observador ajeno o salida precargada: borrar y denegar.
7. Servicio F11 de emisión inexistente: no fallback al ensayo.
8. Guardado parcialmente escrito: preservar última generación confirmada.

## Riesgos residuales

CT-01: falsificación deliberada por propietario local no resuelta sin raíz externa; no prometer antitrampas.  
CT-02: suplantación accidental en binding/restauración: responsabilidad H03.  
CT-03: filtración de proyecciones: H05/H07.  
CT-04: emisor F11 de ensayo usado en producto: bloqueante H07/F11.  
CT-05: fallo de publicación o compatibilidad Core: bloqueante H04.  
