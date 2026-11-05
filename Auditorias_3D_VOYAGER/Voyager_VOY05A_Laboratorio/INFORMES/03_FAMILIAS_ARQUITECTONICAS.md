# VOY-05A — Familias y repeticiones

| Familia | Registros | Interpretación |
| --- | --- | --- |
| AR_BOCA_MODULAR | 69 | Bocas de conexión de tramos, marcos/nichos y desvíos; no hojas suministradas en la boca. |
| AR_HUECO_HABITACION | 18 | Entradas de envolventes de habitación, sala, sanitario o puente simplificado; dos aberturas estructurales E. |
| AR_CONDUCTO_BAJO | 27 | Secciones técnicas de altura insuficiente para marcha de pie; no trasladar automáticamente el mecanismo humano. |
| AR_TURBOLIFT | 4 | Gargantas de cabina/acceso con perfil menor; ninguna cabina demuestra transporte funcional. |
| AR_MANTENIMIENTO | 26 | Conexiones técnicas de pie y entre tramos de mantenimiento; algunas están elevadas en el catálogo. |
| AR_EJE_VERTICAL | 18 | 18 extremos de 9 conductos verticales; requieren otro tratamiento de circulación y protección. |
| AR_REGISTRO_TECHO | 1 | Un hueco con tapa geométrica dentro de Mesh54, sin articulación identificada. |
| AR_PUERTA_BIPARTIDA | 18 | 18 cierres modulares de aspecto bipartido; 16 integrados y dos placas D. |
| AR_CIERRE_ASIMETRICO | 2 | Dos cierres complementarios/asimétricos Mesh27/53; movimiento E. |
| AR_PUENTE_DETALLADO | 4 | Tres parejas de hojas y acceso abierto de cabina del puente detallado. |

**Tipo arquitectónico** define perfil, uso y montaje. **Tipo mecánico** describe trayectoria. **Tipo visual** define forma visible y materiales. Un turbolift y una habitación pueden compartir un mecanismo doble lineal sin compartir perfil, dimensión, hojas ni controles.

Cierres observados: 3 del puente detallado, 18 bipartidos modulares y 2 asimétricos. Hay también una tapa. No se ha confirmado un diseño inequívoco de puerta humana simple corredera ni una bisagra funcional. No se inventan esas familias. Las superficies de cierre son geometría, aunque incluyan franjas y placas; no se han contado simples pantallas negras o paneles de servicio como puertas.

Repetición de aspecto y frente: Mesh14/25/26/51/54/52/80/93 comparten frentes cercanos a 1,034×2,194 m. Mesh28/57 presentan la misma pauta residencial inclinada, con frente de 2,524 m de alto. Mesh27/53 comparten cierre asimétrico de unos 2,221×2,526 m. Mesh55 presenta un frente mayor, 2,068×2,525 m. Las tres parejas del puente tienen dimensiones muy próximas, seis hojas con trim distinto según orientación.

`grupos_dimensionales.json` contiene **27 grupos** a 1 mm. Son candidatos de reutilización por envolvente, no pruebas de igualdad de topología/UV. La huella de nube de vértices tras quitar solo traslación no produjo duplicados exactos entre las 83 mallas completas. Eso no demuestra que todos sus subcomponentes sean distintos. La identidad de una puerta completa fusionada no puede certificarse antes de definir sus caras: se mantiene esa reserva y se propone hacerlo en B.

Previsión mecánica: **un algoritmo parametrizable doble lineal** puede cubrir 21 cierres candidatos si se construyen cavidades compatibles; se necesitan definiciones de forma/recorrido particulares. Los dos asimétricos y la tapa no se adjudican a ese mecanismo. Los 163 registros restantes sin hojas no necesitan un mecanismo hasta decidir dónde instalar puertas.

Conectividad confirmada por geometría: Mesh12/13/18 rectos; Mesh41 curva de 90°; Mesh40/92 T; Mesh38 cruce de cuatro vías. **Mesh2 es una Y**, tres bocas y dos brazos diagonales, con bordes no cíclicos que requieren saneado. Mesh52/80 tienen dos extremos y acceso interior adicional, más cierres laterales: su planta quebrada no los convierte automáticamente en una Y. Mesh56 es una T de conducto bajo (normales cardinales), no una Y de pasillo humano.
