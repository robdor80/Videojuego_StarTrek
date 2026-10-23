# F07-P03 — Selección de puente piloto

**DEC-0003 · aprobada elección por el autor el 13-10-2026, viabilidad pendiente.**

- **USS Sutherland** seleccionado para ensayo interno v0.0.1 de Sensores (no Clase Valhalla ni producto final). Material original: star_trek_sutherland_bridge.glb. «Sunderland» es posible lapsus nominal del mismo activo, no segundo puente certificado.
- **USS Kelvin fuera de v0.0.1**, en desarrollo, reservado para posibles aplicaciones futuras Sovereign/Odyssey. No sustituirlo sin autorización, aunque el Sutherland falle.
- Motivo técnico: auditoría Sutherland revela ~19,5 mil triángulos y 170 mallas, frente a complejidad y trabajo pendiente Kelvin; **no demuestra tránsito ni rendimiento**.

Puertas: verificar hash y licencia de la copia concreta; importar en mapa aislado UE5 sin tocar Kelvin; confirmar escala, ruta acceso/turboascensor a puesto Sensores y colisiones sin bloqueantes; activar una superficie 3D interactiva y volver a primera persona; materiales legibles; telemetría real; revisar derechos y atribución antes de distribuir.

Si falla una puerta se registra como incidencia, no se declara UE5_JUGABLE. Fuente auditada: F02/AUDITORIA_GLB_USS_SUTHERLAND_2026-10-12.md.

## Reconciliación de viabilidad — 23-10-2026

La selección **Sutherland como puente piloto v0.0.1** continúa aprobada, sin convertir Kelvin/New Bridge en sustituto del piloto. La frase «no demuestra tránsito ni rendimiento» del documento original era cierta para la auditoría estática del 13-10-2026; **posteriormente se comunicaron importación UE5, recorridos reales, puertas y colisiones en el MSI**.

Estos avances se anotan en [reconciliación de evidencias](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md) como resultados reportados pendientes de cotejo: la evidencia primaria (mapa, logs, vídeos, hashes) no está todavía integrada en el repositorio. El sentado de NPC no está aprobado, la consola Sensores requiere prueba específica y no constan telemetría ni build verificadas. **P03 sigue cerrada por elección**, no por viabilidad total acreditada.
