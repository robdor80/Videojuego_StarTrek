# VOY-05A — Independencia y separación

Los grados del inventario corresponden a la **viabilidad del sistema completo** o, en bocas sin puerta, a su interfaz arquitectónica. No son aprobaciones funcionales. A = independiente hoy; B = organización/intervención menor; C = geometría/contexto importante; D = reconstrucción recomendada; E = evidencia insuficiente.

| Grupo de cierres | Cantidad | Grado | Motivo |
| --- | --- | --- | --- |
| Puente detallado | 3 | C (hojas B) | Grupos de hoja ya identificables; marco y alojamiento no modulares. |
| Cierres modulares integrados | 17 | C | Comparten malla y conectividad soldada con arquitectura o marco. |
| Placas Mesh53/55/93 | 3 | D | Objeto separado, pero hojas/marco fusionados, espesor global limitado y sin alojamiento. |

Total cierres: 20 C y 3 D. **A completos = 0; parejas con hojas recuperables independientes del puente = 3.** La tapa Mesh54 es C: isla desconectada dentro de la misma malla, no objeto funcional. Los grados B de las bocas abiertas describen conservar y montar un inserto; no suman puertas independientes.

Se examinó conectividad con soldadura diagnóstica de 10 µm, sin modificar ninguna malla. Mesh14/25/26/27/28/51/53/55/57/93 forman una componente principal común de arquitectura y cierre; Mesh54 tiene una segunda isla correspondiente a la tapa. La conectividad es evidencia de integración, pero ni una sola componente impide por sí misma una futura separación, ni múltiples islas prueban componentes semánticamente correctos.

Para B: duplicar el módulo fuente, crear grupos de caras de hoja, marco, remate y mamparo; preservar materiales y todos los UV; guardar correspondencia cara original→pieza nueva. La operación debe producir una arquitectura utilizable con puerta retirada, sin dejar una pared tapando el hueco o un vacío alrededor del marco. Cerrar espesores y conservar una copia íntegra como referencia oculta y explícita, sin superponerla al resultado.

En el puente, recoger todos los fragmentos de cada lista `leaf_dimensions.objects`: franjas, tiras y adornos no deben quedarse flotando. Doorpanel es un control; no una hoja. El pivote actual no se acepta como raíz modular. No se han creado pivotes, jerarquías móviles, separación definitiva ni animaciones en A.

Evidencias: `coleccion_componentes.json`, topología en los siete `*_auditoria.json`, [marcos y placas](../CAPTURAS/LAM_FINAL_05_MARCOS_Y_PLACAS.jpg), planos frontales y manifest de captura. La tolerancia de soldadura sirve para diagnosticar costuras de importación; no es tolerancia de fabricación ni de colisión.
