# LORE-02 D — Auditoría científica y decisiones de autoría

Fecha: 2026-10-21. Base auditada: Star Trek `main` en `1bf8f356228bc3e9bf569b22992fdf436e3e705f`; CoreRPG `main` en `4f282863737bcd8f5add401202a9e1064c133672`.

## Alcance real

Ciencia, fenómenos y experimentación de TNG/DS9/VOY para diseño futuro. Ninguna ficha concede datos físicos reales, números universales, teletransportes, saltos temporales, inventario, navegación, experiencia médica, órdenes o encuentros de contenido reservado. Los episodios son precedentes **de casos particulares**. No hay imposición de misterio, amenaza, misión ni resolución.

## Evidencia y contraste

La fuente audiovisual retenida prima sobre referencias oficiales, licenciadas y fuentes secundarias. Se incorporan al registro episodios con fenómenos de interés: `TNG_CAUSE_AND_EFFECT`, `TNG_PARALLELS`, `VOY_BLINK_OF_AN_EYE`, `VOY_THE_CLOUD`, `VOY_ONE_SMALL_STEP`, `TNG_TIMESCAPE`, `TNG_WHERE_NO_ONE_HAS_GONE_BEFORE`, `VOY_OMEGA_DIRECTIVE`, `TNG_REMEMBER_ME`, `TNG_IDENTITY_CRISIS`. Los episodios existentes como `DS9_EMISSARY`, `DS9_PLAYING_GOD`, `TNG_GALAXYS_CHILD`, `VOY_SCIENTIFIC_METHOD` y `VOY_THIRTY_DAYS_REFERENCE` ya tenían ficha en el registro.

Referencias oficiales contrastadas en StarTrek.com:
- Temporalidad en **Cause and Effect**: https://www.startrek.com/news/cause-and-effect-the-star-trek-tng-episode-that-stuck-with-me
- Convergencia de realidades **Parallels**: https://www.startrek.com/news/what-the-helm-astonishing-viewscreen-reveals
- Diferencial planeta/orbita en **Blink of an Eye**: https://www.startrek.com/news/moon-to-delta-quadrant-nasa-imprint-on-star-trek-voyager
- Perspectiva científica y cultural de **Emissary**: https://www.startrek.com/news/deep-space-nine-modern-balance-science-religion

Los ejemplos científicos cotidianos (púlsar, nube, espectro o tormenta) se conservan como **INFERRED** o **GAME_ADDITION**; su etiqueta no confirma intensidad, fórmula ni secuencia de interacción Trek canónica. Cada ficha documenta `claim_class`, `source_ids` y alcance. `GAME_ADDITION` declara su autoría en el propio registro.

## Fronteras ya presentes, sin modificación

- LORE-01 C: `lore/astrography/atlas/anchor_atlas_v0.1.json`, coordenadas/anclas y discrepancias no aportan descubrimiento automático.
- LORE-01 E: `lore/operations/cross_layer_reference_v0.1.json` y consulta por época, jurisdicción, actor y conocimiento.
- LORE-02 A: `lore/technology/lore02_a_system_atlas_v0.2.json` y matriz de era para prestaciones instaladas, sin universalizar.
- LORE-02 B: `lore/equipment/lore02_b_equipment_catalogue_v0.1.json` para instrumentos y sondas; ningún spawn de objeto.
- LORE-02 C: `lore/medicine/lore02_c_facilities_staff_v0.1.json` para equipos sanitarios, privacidad y derivación.
- Ciencia/sensores: `lore/science/scientific_domain_contract.json` y `gameplay/science/sensor_analysis_model.json` con lecturas, hipótesis y discrepancias.
- CoreRPG: ADR-0004 Knowledge/Visibility, ADR-0005 Action/Simulation, ADR-0007 Context Builder; el Core no ejecuta protocolos Trek, ni admite este JSON como pack 0.1.0 sin adaptador futuro. UE5 pinta los eventos; IA no recibe verdad privilegiada ni muta mundo.

## Interpretación operativa futura, NO IMPLEMENTADA

Un pipeline posible tras aprobar todos los LORE es: instancia verdadera de fenómeno en Core → dispositivo y permiso en Host → lectura limitada y registrada → proyección de hechos al observador → hipótesis individuales contrastadas → acción validada en Host/Core → revisión y posible informe → consecuencias persistentes. Una hipótesis puede ser falsa, indeterminada o parcialmente verdadera; varias hipótesis pueden coexistir. La evidencia puede cambiar sin forzar resolución. Una sonda puede contaminar una muestra, destruir un organismo o quedarse incomunicada, pero sólo si las reglas activas y el estado real lo producen.

## Conflictos y aspectos que quedan abiertos

1. **Extrapolación temporal:** casos únicos (TNG/VOY) no convierten los viajes entre realidades ni el futuro en equipamiento disponible. Omega no se universaliza ni elimina clasificación institucional.
2. **Fenómeno vs. lugar:** un agujero de gusano registrado en astrogeografía puede figurar como objeto en ciencia sólo con su identificador de tipo; no se añade una ruta espacial nueva.
3. **Subespacio vs. física real:** el canon no proporciona un modelo universal coherente. La ficha guarda condiciones cualitativas y ejemplos, no ecuaciones.
4. **Datos contradictorios:** conservar ambas mediciones, instrumentos, observadores y procedencia; no resolverlas silenciosamente.
5. **Peligros posibles:** la investigación no implica combate ni misión obligatoria; la protección ética y la Primera Directiva pueden prevalecer.
6. **Limitación de revisión:** no hay comprobación escena por escena con timecode; los capítulos y referencias contrastadas permiten auditoría posterior de detalles particulares.
7. **CoreRPG pendiente:** integración concreta de esquema Star Trek, eventos físicos de fenómeno, autorización clínica/científica, persistencia específica y visualización UE5 se diseñarán sólo tras los LORE; no se implementan aquí.

## Criterios de salida

Validadores documentales, cruces de origen/IDs entre fases, pruebas adversariales, regresiones A/B/C/LORE-01/roadmap y GitHub Actions. Antes de la aprobación humana permanecen `NEEDS_REVIEW` y `LORE-02 D IN_PROGRESS`; `main` no cambia.
