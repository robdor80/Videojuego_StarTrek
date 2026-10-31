# Corrección y optimización de CI — F04-PERSISTENCIA-03

Medición trazable de la primera corrección, antes de reutilizar las cinco
referencias adicionales. HEAD ejecutado:
`f2dcb907f3518020dbcfe3bc55eff226ebbef8f4`.
[Actions 41207950499](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41207950499):
**seis campañas PASS**. Los cuatro workflows de ese HEAD finalizaron en verde.
Esta evidencia no atribuye resultados futuros al HEAD que añade esta documentación
ni al posterior camino rápido de seis referencias: consultar sus Actions reales
en la PR #76. Las fuentes productivas y el ejecutor nativo no se modifican.

## Diagnóstico y medidas

La ejecución 41199067055 agotó 3.300 segundos generando únicamente el oráculo
Valhalla 730. No llegó a iniciar su campaña real. El archivo parcial conservado
no es una referencia aceptable y no se ha usado como tal.

Se verificó la referencia original de 730 del commit auditado `19aaf974`, usando
SHA-256 real, procedencia, aceptación, contratos, perfil, duración y filas. SHA-256:
`4f5b5b096e07e4e9fc2b504cb8b4e86d898655d60e99a678b567ded58140f204`.
El runner existente la consume mediante `F04_HISTORY_REFERENCE_FIXTURES` y una
copia exclusiva temporal; falla si falta, está alterada o resulta incompatible.

Las cinco campañas de 365 conservaron inicialmente la regeneración íntegra.
En esta nueva ejecución sus cinco archivos completos son idénticos byte por byte
a los originales auditados: `oracle-equivalence.json` contiene las seis huellas.
La procedencia y el contrato de esa ejecución están preservados en
`reference-manifest-f2dcb907.json`. No se alteraron valores esperados para aceptar
resultados distintos. Esa comparación completa justifica reutilizar también esas
cinco referencias mediante exactamente el mismo mecanismo, en el HEAD posterior.

## Tiempos medidos de la primera corrección

Segundos. Total es la prueba CTest; no incluye compilación ni el trabajo de las
regresiones. La columna oráculo de 730 vale cero porque esa fase **no se ejecutó**.
Los demás valores son medidas reales de procesos nuevos, no estimaciones.

| Perfil | Días | Generar oráculo | Simulación real | Recuperar y continuar | Auditar | Total CTest | Resultado |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 365 | 30.2 | 13.5 | 0.3 | 2.0 | 46.7 | PASS |
| 2 | 365 | 48.6 | 17.3 | 0.4 | 2.3 | 69.1 | PASS |
| 3 | 365 | 275.6 | 80.7 | 1.7 | 20.9 | 380.1 | PASS |
| 4 | 365 | 904.2 | 186.2 | 3.9 | 77.6 | 1172.7 | PASS |
| 5 | 365 | 1177.7 | 257.0 | 5.5 | 113.1 | 1553.9 | PASS |
| 5 | 730 | 0.0 | 729.5 | 9.2 | 227.7 | 966.6 | PASS |

Las seis pruebas suman **4.189,1 segundos de runner**, frente a 6.609,8 de la
base fallida: **2.420,7 segundos menos (40 min 20,7 s; 36,6%)**. Al ejecutarse en
paralelo, esta suma no es tiempo de pared. Además, la base no completó 730:
no se inventa el tiempo que habría necesitado una regeneración completa.
Las oscilaciones de hardware/carga de runner no son ahorro atribuible al código.

Solo las cinco regeneraciones repetidas consumieron **2.436,2 segundos** en esta
medición. Ese es el trabajo redundante demostrado que el camino rápido posterior
omite. Cada una de sus simulaciones productivas, recuperaciones y auditorías se
mantiene íntegra y debe pasar nuevamente en la CI del HEAD final.

## Garantías verificadas

- Seis campañas auténticas completas: cinco clases durante 365 días y Valhalla
  durante 730; 1.800 tripulantes y 400 civiles para Valhalla.
- Guardias, ausencias, descansos, cancelaciones y suplencias reales; mismos IDs,
  RNG/reloj, decisiones y payload original en todos los bloques.
- Recuperación en proceso independiente y continuación futura idéntica.
- Auditor independiente de todos los originales publicados: **1.948.872 hechos**
  entre las seis campañas. Valhalla 730: 866.849 hechos en 105 bloques,
  858.295 archivados, máximo 21.218 entidades residentes y 6.662.421 bytes activos.
- Personas/competencias/relaciones estáticas inmutables comprobadas en cada bloque;
  presupuesto productivo intacto de 65.536 residentes.
- Regresiones F04 propuestas **272/272**, sin omisiones. Incluyen la batería de
  **17 pruebas de referencias** y un proceso nativo que rechaza un digest divergente.
- Referencia válida, seis registros, hash incorrecto, ausencia, truncado, otro
  perfil/duración, Core/contratos/esquema incompatibles, procedencia alterada,
  preservación del original y respaldos, y divergencia nativa: cubiertos.
- Invocación real del runner con Python `-O`: referencia corrupta rechazada antes
  de generar o simular, sin alterar originales (`negative-runner-optimized.json`).
- Local MSI: 272 regresiones PASS y Valhalla 730 completo en 583,8 segundos,
  incluyendo auditoría. La CI mide su propio entorno y sus propios tiempos.

## Reproducción y auditoría profunda

Los comandos completos están en `desarrollo/integration/f04/HISTORY.md`.
El modo rápido verifica, prepara una copia y simula todos los hechos. El modo
profundo omite fixtures y regenera cada oráculo de forma independiente; se activa
mediante `regenerate_oracles=true` en workflow_dispatch, o en un build local nuevo
con `F04_HISTORY_ORACLE_TIMEOUT_SECONDS=18000`. Solo amplía el presupuesto de esa
regeneración lenta y su techo CTest; las fases productivas mantienen 3.300s.
Los seis trabajos permanecen aislados, fail-fast desactivado. Nunca sobrescribir
originales ni registrar referencias incompatibles sin regeneración y auditoría.

## Alcance de archivos

Cambios limitados a `.github/workflows/f04-history-persistence.yml`,
`desarrollo/integration/f04/CMakeLists.txt`, `HISTORY.md`,
`tests/run_history_campaign.py`, `tests/history_reference.py`,
`tests/history_reference_tests.py`, `tests/fixtures/history_reference_v1.json`,
el documento F04-PERSISTENCIA-03 y este nuevo paquete de evidencias.
CoreRPG #13 permanece en `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`.
Pin estable intacto: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.
Sin cambios de producto, Unreal, recursos 3D, respaldos, main, ni otras fases.
Ambas PR permanecen Draft y no se fusionan.

`SHA256.json` inventaría los bytes de este paquete; las evidencias históricas
anteriores permanecen intactas. Los logs/XML/aceptaciones y metadatos de Actions
permiten verificar cada afirmación sin confiar solo en este resumen.
