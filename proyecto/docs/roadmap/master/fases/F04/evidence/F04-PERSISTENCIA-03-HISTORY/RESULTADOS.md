# Resultados de persistencia histórica F04

Estado: aceptación completa demostrada; pendiente auditoría independiente.

Core propuesto: `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`; pin estable F04 sin modificar. Ambas PR permanecen Draft, sin fusión.

| Clase | Días | IDs finales | Archivados finales | Máximo residente | Máximo checkpoint activo B | Pico working set B | Disco B, generaciones conservadas | Máximo archivo ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Miranda | 365 | 41438 | 40309 | 1926 | 551836 | 12091392 | 30208059 | 269.98 |
| Intrepid | 365 | 47877 | 46556 | 2234 | 646257 | 13012992 | 35381483 | 272.243 |
| Sovereign | 365 | 179181 | 174137 | 8492 | 2587327 | 30961664 | 140155276 | 1026.53 |
| Odyssey | 365 | 385384 | 374435 | 18348 | 5649296 | 56401920 | 306161850 | 2681.78 |
| Valhalla | 365 | 437731 | 424908 | 21218 | 6662421 | 64196608 | 360642331 | 2861.58 |
| Valhalla | 730 | 870964 | 858295 | 21218 | 6662421 | 65495040 | 719423208 | 4997.88 |

Todos los bloques comparan los hechos originales, asignaciones y RNG/reloj con el oráculo de historial íntegro. Cada campaña continúa en otro proceso; el auditor reconstruye todos los bloques posteriores al bootstrap desde los segmentos y checkpoint y verifica sus hashes originales.

Los logs `campaigns/*/campaign.log` conservan métricas por bloque y tiempos de consulta/recuperación. La recuperación medida incluye la comprobación diagnóstica posterior; no es una latencia aislada de E/S. El pico de memoria incluye el ejecutable y buffers de prueba. Los objetos de partida permanecen en el laboratorio externo; `storage-inventory.json` registra sus bytes y SHA-256.

El coste de publicación/recuperación crece con la validación del historial conservado. El límite residente productivo sigue en 65.536. Los tamaños de disco incluyen checkpoints anteriores; no hay descarte de hechos ni limpieza automática de generaciones.

Los cinco recorridos de 365 días usaron el oráculo original. El de 730 usa el oráculo de prueba optimizado: originales completos residentes, carga vital recalculada, ventanas antiguas irrelevantes excluidas solo del cálculo temporal y validación global completa en ambos horizontes finales. El producto conserva la validación completa en cada transacción.

Regresiones: Core 479 PASS + 4 omisiones; F04 271/271; F02 15/15; F03 25/25; seis campañas largas PASS; Unreal 5.8.2 NullRHI 26/26 y cero warnings de test. Migración antigua no destructiva y mismo futuro en proceso nuevo: cinco clases. CI Core exacta: `core-ci.json`.

Integridad del paquete: `evidence-sha256.json` usa bytes exactos, protegidos de conversión EOL por `.gitattributes`; `source-files.json` normaliza CRLF a LF para comparar fuentes entre plataformas.
