# D02 — Estado inicial y semántica del corte de campaña

## 1. Parámetros no intercambiables
- `campaign_start_year_proposed=2383` es **decisión editorial aprobada como propuesta**; `campaign_start_exact_date=null`. El comienzo efectivo `D` será un instante/versionado concreto únicamente cuando el autor y el runtime lo configuren; hasta entonces NO interpolar el 1 de enero ni el 31 de diciembre.
- `reference_year` y `precision` describen evidencia intradiegética, no la fecha de emisión del episodio ni una fecha exacta escondida.
- `event_effective_time` de una campaña existe solo para eventos realmente confirmados por CoreRPG.
- `observation_time` y `learned_at` son independientes del momento del hecho. Un rumor, informe tardío o secreto no forma parte automáticamente del conocimiento de cada ciudadano.

## 2. Clasificación del corte
| Relación temporal | Tratamiento documental |
|---|---|
| Historia anterior demostrable a `D` | `HISTORICAL_ESTABLISHED`, inicializar *estado derivado*, no volver a ejecutar evento |
| Mismo año sin orden intranual demostrado | `UNRESOLVED_SAME_YEAR`; abstenerse de marcar hecho sucedido/no sucedido por pura comparación del año |
| Intervalo cruza `D`, conflicto activo verificable | `ONGOING_AT_START`; inicializar únicamente situación y efectos acreditados a `D`, no final |
| Posterior a `D` | `FUTURE_REFERENCE_ONLY`, nunca agendar por calendario |
| Fecha o fuente insuficiente | `UNKNOWN_OR_CONTESTED`, preservar incertidumbre; ampliar fuentes o elevar reserva |
| Información incorrecta o desinformación | `FALSE_CLAIM_OR_RUMOR`, modelar afirmación y su circulación, **no** un golpe real |

Dos años de ancla aproximada iguales **no** justifican orden relativo. Un evento "2367 aproximado" entra históricamente en una campaña de 2383 si el hecho está confirmado, pero su recuerdo no es universal. Las campañas hipotéticas en años próximos al evento requieren evaluación por intervalo y evidencia adicional.

## 3. Procedimiento conceptual de inicialización
1. Validar época única jugable (`tng_ds9_voyager`) y fecha de comienzo permitida; épocas Pike/Kirk solo como fuentes históricas.
2. Fijar un **cutoff inmutable por campaña** `D` cuando exista precisión suficiente; guardar procedencia/versión de catálogos.
3. Resolver historia anclada bajo reglas anteriores. Nunca importar filas etiquetadas `FUTURE_REFERENCE_ONLY` como órdenes/efectos.
4. Derivar situación de entidades existentes, pérdidas confirmadas, acuerdos vigentes, cargos y tecnologías justificadas sin crear duplicados ni cambiar el canon anterior.
5. Mantener separados estado real, distribución de información, secretos y rumores.
6. Ejecutar comprobaciones de consistencia sobre fechas, identidades, referencias, accesos y privacidad; fallar de forma segura si una ambigüedad afecta un hecho crítico.
7. Crear identificador exclusivo del guardado y prefijo histórico congelado; solo CoreRPG confirma arranque y posterior evolución.

## 4. Línea base de 2383
Guerra del Dominio finalizada; regreso histórico de Voyager; Picard almirante; Riker capitán de USS Titan; Rómulo existe y NO se considera destruido; crisis de Shinzon 2379 es antecedente admisible. Valhalla es adición del videojuego: calendario proyectado desde 2379 y objetivo de servicio 2383; la fecha exacta de incorporación no existe y su presencia en servicio **dentro de ese año** requiere orden acreditado. Graduación de Academia hacia 2387 es horizonte de carrera, no ascenso ni puesto forzoso. La Forge no recibe destino inventado.

## 5. Casos que deben rechazarse
`same-year 2383 => evento necesariamente pasado`; `approximate year => 01-01`; `Roman supernova 2387 => Rómulo ya destruido 2383`; `falso golpe tzenkethi => hecho político`; `rumor público => todos los NPC saben la verdad`; `clase disponible => unidad concreta ya registrada`. Todos violan o el corte o la procedencia.
