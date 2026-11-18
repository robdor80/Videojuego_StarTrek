# Navegación / Astrometría

Familia funcional existente: navigation (Navegación/Astrometría). No crear una consola global nueva ni duplicar Navegación.

## Sistema 11 — Astrometría 360° (18-11-2026)

**Aprobado en diseño, NO implementado en UE5, HOST ni CoreRPG.** Ver [Diseño S11](../../../astrometrics/S11_ASTROMETRIA_360_DISENO_v1.md) y la decisión [DEC-0023](../../../../../proyecto/docs/decisions/s11_astrometria_360_2026-11-18.md).

Astrometría consulta y presenta galaxia/cuadrante, región/sector, sistema estelar y cuerpo celeste en un holograma 3D interactivo. Puede presentar datos científicos, capas y rutas candidatas. Una propuesta de ruta no altera NavigationState: la validación y ejecución de movimiento pertenecen al sistema Navegación/CONN y a la cadena de mando.

El mismo conjunto de información está disponible a través de sala 360°, LCARS y PADD ligero, con permisos correspondientes. No se emite información no conocida ni se repiten escaneos ordinarios sin necesidad. Los perfiles visuales dependen de nave y refit: la superioridad sensorial de Enterprise-D no se copia a todas las clases.

