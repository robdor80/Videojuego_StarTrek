# LORE-05F — Matriz de deuda, autoridad y aceptación posterior
**Fecha:** 13/11/2026 · **Uso:** traspaso de diseños a fases de producto. Los ítems de esta tabla NO están implementados por crear el documento.

| ID | Dependencia pendiente | Propietario propuesto | Puerta verificable | Prohibición mientras tanto |
|---|---|---|---|---|
| HOF-01 | Migrar `valhalla` histórica a la identidad de la Enterprise-D individual sin romper guardados ni duplicar naves | F04 / F05 / CoreRPG / HOST | Pruebas de identidad, clases, migración y carga de partida | No renombrar `class_id=valhalla` en masa |
| HOF-02 | Revisar las 16 VAL-TEC, dotación 1.800+400, auxiliar Defiant y separación de secciones frente a capacidades Galaxy reales | F04 / F06 / F07 | Matriz técnica, compatibilidad, instalación por buque y verificaciones 3D | No declararlas instaladas |
| HOF-03 | Determinar casco secundario y astillero, fecha de alta real y disponibilidad de la Enterprise-D | Campaña / F04 / CoreRPG, decisión creativa cuando proceda | Evento fechado con piezas, autorización y reconstrucción terminada | No fijar Syracuse 2401 para 2387 |
| HOF-04 | Academia 2383–2387, graduación y destino efectivo al salir de la Academia | F10 / F11 / HOST / CoreRPG | Registro y orden válidos, vacante y pruebas de progresión | Sin plaza o mando automático |
| HOF-05 | Entrega presencial de galones por Picard al legítimo nuevo capitán | F11 (autoridad), Narrativa/UE5 (escena), HOST (servicios) | Ascenso aprobado primero; evento presencial compatible con agenda y ubicación | La escena no concede el rango |
| HOF-06 | Data: recuperación de identidad, B-4, archivos positrónicos y ética (2390–2395 condicional) | Narrativa / Ciencia / CoreRPG | Arco de investigación y suceso de retorno persistente, reconocido oficialmente | No crear Data vivo en 2383 |
| HOF-07 | Sisko: eventual retorno 2388–2392, relación con Profetas y reincorporación | Narrativa / CoreRPG / F11 | Evento de regreso y posterior nombramiento independiente | No ponerlo en servicio activo en 2383 |
| HOF-08 | Siete: fechar cronología alternativa, edad (~35), encuentros y evolución de rango | Autor/narrativa / F11 / CoreRPG | Modelo de calendario coherente con tiempo real, sin congelación de edad | 2358/2393 sigue siendo aproximado |
| HOF-09 | Geordi: ascenso dentro de 2383–2387 y dirección de Valhalla, sin confundir con mando naval | F11 / Narrativa / CoreRPG | Orden y fecha aceptadas; puesto técnico independiente | No contraalmirante por defecto en 2380 |
| HOF-10 | Guinan, Ten Forward y acceso a cubierta E | F04 / vida a bordo / UE5 / CoreRPG | Enterprise-D operativa, compartimento validado, servicio/contratos/agendas reales | No Ten Forward operativo en nave en obras |
| HOF-11 | Assets de NPC y cubiertas, licencia, semejanza, rigging y audio | Blender / UE5 / producción artística | Inventario lícito y prueba visual | No prometer modelos inexistentes |
| HOF-12 | Estado político 2383: Bajor/DS9, Cardassia, Romulus, instalaciones y servicios | CoreRPG / P2 / diplomacia | Estado fechado, jurisdicción, permisos, recursos y proveedores reales | No usar catálogo como simulación |
| HOF-13 | Exploración/primer contacto y traductor con incertidumbre persistente | F06 / sistemas propietarios / CoreRPG / HOST | Pruebas causales de observación, conocimiento, consentimiento y latencia | IA no inventa física ni soberanía |
| HOF-14 | PADD externo basado en información conocida y autorizada | PADD / HOST / CoreRPG | Tests de no filtración y revocación de permisos | Prohibido exportar secretos |
| HOF-15 | DLC Delta: idiomas, rutas y encuentros bajo desbloqueos explícitos | Diseño de DLC / CoreRPG / F04 | Manifest de producto y autorizaciones en la fase de DLC | No habilitar Kazon/Talaxiano por overlay |
| HOF-16 | Resolver estatus administrativos históricos (precierre B y CI de C/D HEAD) | Gobierno del repositorio / LORE-05F | Acta de 05F y registros GitHub verificados | No reescribir evidencias anteriores como si fuesen actuales |

## Orden de aplicación recomendado
Primero respetar y probar **IDs, autoridad CoreRPG, F11/HOST y compatibilidad histórica**. Después conectar los catálogos a estado vivo, observación y permisos. Finalmente construir escenas, activos, diálogos, UI/PADD, eventos de campaña y pruebas de integración.

Las fases de propietario deberán mantener su propia PR, plan de pruebas y cierre; LORE-05F **no les transfiere control del estado ni define un segundo motor**.

## Fuentes de gobierno
- [DEC-0020](../../decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md)
- [Acta transversal](ACTA_AUDITORIA_TRANSVERSAL_20261113.md)
- [Estado de contenido](../../../../CONTENT_STATUS.md)
- [Arquitectura HOST](../../architecture/host/README.md)
