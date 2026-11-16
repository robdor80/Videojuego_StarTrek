# Integraciones de motores

Esta carpeta es un **mapa de integración**, no tres copias del mismo código.

- `corerpg/`: dependencia externa, versionada/pinneada; única autoridad del estado y reglas del universo.
- `host/`: fuentes actuales en `desarrollo/integration/host/`, con adaptadores en `desarrollo/integration/`; no mover hasta que un plan de migración con CMake, pruebas y compilación real lo apruebe.
- `unreal/`: proyecto principal en `juego/UE5/StarTrekRPG/`. Los módulos de presentación se implementan allí.

Cualquier movimiento real exige inventario de rutas, actualización de builds, CI y comprobación en Unreal. Prohibido duplicar implementaciones.
