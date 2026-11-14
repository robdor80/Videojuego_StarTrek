# H06-P06-A4 · Implementación de la autoridad interna F10

**Fecha** 14-11-2026. **Base** `bf56700ecfa0e29e45cb5b3532eec92c27d5015b`. **Rama** `codex/h06-p06-a4-biography-evidence`.

## IMPLEMENTADO

1. `RegisteredBiographyAuthority` recibe una instantánea inmutable de procedimientos registrados y de atestaciones producidas por código interno F10. El registro exige ID único, versión o revisión, emisor, tipo de origen y alcance por código y campo. Los tipos admitidos son regla aprobada, lectura de hecho ya confiable y fuente de antecedentes iniciales validada por F10.
2. El validador devuelve una vinculación privada a los colaboradores nativos solo después de comprobar estructura y restricciones deterministas. La autoridad recalcula la huella del borrador canónico y la del contexto HOST, que incluye escenario, era, año, campaña, generación y perfil. También exige versiones actuales de reglas y política. Ni la huella ni el ID por sí solos constituyen evidencia.
3. La autoridad comprueba la atestación exacta del código y campo, las versiones, el emisor y el origen contra el registro. Una decisión `SUPPORTED` puede cerrar esa comprobación. Una contradicción o revocación aplicable mantiene el asunto pendiente aunque exista otra atestación favorable. Las decisiones insuficientes o no aplicables por sí solas dejan el asunto pendiente. Una atestación sobre una colección debe cubrir todas sus entradas y sigue vinculada al borrador completo.
4. Una futura fuente F10 de antecedentes iniciales puede asociar su decisión al borrador sin requerir un PERSON. El registro carece de expedientes precargados y la evaluación carece de rutas para importar evidencia desde texto del jugador o del evaluador. Un `evidence_ref` bien formado sigue siendo una declaración. Los campos reservados de procedencia se rechazan incluso dentro de objetos.
5. El constructor nativo de composición admite únicamente la autoridad registrada. El constructor vacío representa ausencia de fuentes, y el constructor genérico permanece reservado al binario de pruebas. La instantánea incorpora versiones actuales de las fuentes y debe reemplazarse, junto con el validador, si cambian sus registros o sufren revocaciones. Los recibos de ensayo siguen ligados a la instancia emisora.
6. La lista de comprobaciones que admite este corte deja fuera madurez individual, fechas sin decisión y reglas de especie ausentes. El contrato de la PR #155 participa en el hash de fuentes y el identificador de la política semántica. El puerto `SemanticEvaluator` conserva su interfaz; `verify` devuelve `UNVERIFIED` hasta que exista comprobación semántica aprobada. El constructor de producto carece de un evaluador.

## PROBADO

Los casos de ensayo ejercitan el mismo constructor nativo que recibiría una instantánea real. Comprueban ámbito del registro, suplantación, cambios de versión, campaña, generación, edición del borrador, evidencias contradictorias y revocaciones. La generación de reglas verifica que cambiar el contenido del contrato de procedencia cambia la huella. Los casos previos de conjunción, vigencia, privacidad y restricciones de especie continúan en la misma suite.

## BLOQUEADO

Los borradores pendientes sin evaluador devuelven `REVIEW_UNAVAILABLE`. Las pruebas de atestación usan datos aislados dentro del ejecutable de tests. El modo de producto requiere registros aprobados y un futuro verificador de la procedencia semántica.

## PENDIENTE

Definir la política de madurez individual, acreditar fuentes iniciales concretas y decidir el proveedor semántico. CoreRPG sigue siendo la autoridad de publicación del mundo. El ABI de HOST mantiene la creación de PERSON, la admisión, el rango y los permisos fuera de este corte.
