# Desarrollo por Sistemas Funcionales Completos

**Decisión de método — 2026-11-16.** Juego para uso personal exclusivo. **No se inicia la campaña para jugar mientras dure la construcción**; las sesiones de prueba de ingeniería no son partidas de ocio.

## Regla fundamental

**Un sistema activo cada vez**, con sus dependencias mínimas (HOST/CoreRPG/UE5) permitidas. No empezar sistemas vecinos por conveniencia. Puede haber trabajos de mantenimiento imprescindibles en motores comunes; deben quedar trazados al sistema activo.

Cada sistema debe pasar: (1) auditoría de reutilización; (2) alcance y decisiones de autor aprobados; (3) contratos/autoridad y dependencias; (4) implementación; (5) integración en la build real de Unreal cuando corresponda; (6) pruebas de reglas, E2E y regresión; (7) rendimiento medido en MSI y optimización; (8) informe de cierre y aceptación del autor. **CI verde o documentos terminados no equivalen a sistema terminado.**

No declarar `TERMINADO` salvo aceptación y evidencias de funcionamiento real de su alcance. Ampliaciones futuras son versiones nuevas, no invalidan un cierre honesto. Los sistemas sin componente 3D deben demostrar su operación real mediante consumidores integrados.

## Fronteras de autoridad y almacenamiento

- **CoreRPG:** fuente autoritativa de estado del universo y reglas; su checkout fijado es externo al repositorio Star Trek, no se duplica en `juego/`.
- **HOST:** ejecución y orquestación; fuentes actuales definitivas en `desarrollo/integration/host/`. En `juego/integraciones/host/` solo se documenta y vincula, nunca una copia divergente.
- **UE5:** proyecto real en `juego/UE5/StarTrekRPG/`; allí viven los componentes visuales, `Source/`, `Plugins/` y `Content/` que Unreal utiliza.
- **`sistemas/` de la raíz:** reglas, contratos y material de diseño ya existente. **No duplicar** estas fuentes en `juego/sistemas/`.
- **`juego/sistemas/`:** fichas de sistemas y punto de integración/aceptación, no un motor paralelo. Las fichas indican dónde reside su código real.
- **`assets/`:** biblioteca de origen; los recursos aprobados se importan a UE de manera controlada, conservando sus originales.
- **`mundo/lore/`:** material narrativo y conocimiento fuente, que se transforma en datos consumibles sin copiar las biblias enteras innecesariamente.
- **`laboratorios/`:** ensayos desechables, nunca dependencia productiva ni material a commitear.

## Estado y priorización

Catálogo inicial **propuesto**, no una orden de desarrollar los 38 sistemas ni aceptación individual de su alcance. Consultar `catalogo_sistemas.json`; los estados iniciales no pretenden invalidar los trabajos F00–F15, HOST, LORE o Planificación 2.

Para abrir un sistema, documentar sus vínculos exactos con componentes y PR existentes, sus bloqueos y su fase activa. Solo entonces establecer orden de construcción a partir de dependencias, no del número de carpeta.

## Criterio de parada

Cuando algo no dependa del sistema activo, añadirlo al catálogo o al buzón de ideas y seguir con el sistema actual. No abrir un frente nuevo sin una decisión explícita del autor.
