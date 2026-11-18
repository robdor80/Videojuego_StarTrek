# Sistema 12 — Corrección autoral funcional (18-11-2026)

**Estado:** necesidades aprobadas por el autor en conversación; diseño S12 completo aún pendiente de ratificación. **Esta adenda no fusiona ni certifica S12.**

El usuario especifica que **un sistema es algo funcional**, no una fase de decoración/arte. Las texturas, mobiliario, pasillos físicos y montaje de salas pertenecen al trabajo de Blender/Unreal/NAP y otras fases, **no constituyen funcionalidades S12**.

## Cinco funciones prioritarias

1. **Puertas operativas y detección de personas.** Recuperar el prototipo Sutherland de Quinn (ensayos reportados de puertas y colisiones): los accesos ordinarios designados automáticos detectan a jugador **y NPC**, abren y cierran con antipinzamiento/seguridad; un camarote o despacho privado **se pulsa** desde el exterior, no se abre solo por proximidad. **S18** identifica a quien pulsa y devuelve permiso/llamada/denegación; **S12** ejecuta panel, mecanismo, colisiones, sonido, estados físicos. No presumir que un sensor de proximidad equivale a autenticación.
2. **Turboascensores funcionales.** Puertas abren y cierran, el jugador/NPC entra, indica destino por voz en castellano o LCARS: «al puente», «a la cantina», «a mi camarote». Resolver destino **por referencia personal/ubicación de Core**, comprobar permisos con **S18 donde corresponda**, capacidad y ruta. Seleccionar **la parada de ascensor existente más cercana y operativamente conveniente al destino**, NO la puerta del destino. Tras salir, el personaje camina el trayecto restante. Evitar inventar paradas por comodidad. Soportar mapas/escenas independientes mediante transiciones que consuman tiempo.
3. **Geolocalización interior.** Consultar cubierta/sección/compartimento/localización para jugador y NPC, conforme a conocimiento y autorizaciones reales del ordenador; estado persistente, cambios por tránsito legítimo, daños y transferencias. Privacidad de ubicación según S18/reglas del ordenador.
4. **Planos/mapas LCARS.** Desplegar en cualquier pantalla autorizada la nave, sus cubiertas, salas, camarotes y ascensores, señalar dónde estamos y cómo llegar hasta un lugar; fuente = topología Core, no una imagen estática inventada. La habitación privada se identifica de acuerdo con permisos. No añadir geometría física ni texturas a S12.
5. **Rutas de NPC.** Navegación sobre grafo de compartimentos, puertas y turboascensores reales, con horarios F12, espera, capacidad, permisos S18, atascos, daño y rutas alternativas; los NPC caminan en UE5 cerca del jugador y se desplazan con coste temporal coherente fuera de escena, sin teletransportarse ni duplicarse.

## Desglose de responsabilidades ratificado

| Ámbito | Propietario |
|---|---|
| Identidad auténtica de quien pulsa, residente/invitado, permisos, excepciones | **S18** |
| Detector, pulsador, apertura mecánica, animación, colisión | **S12 + UE5** |
| Localización/tiempo/identidad persistentes, grafo de la nave | **CoreRPG**, consumido desde S12/HOST |
| Voz y selección flexible de destino | Ordenador/HOST, enrutamiento determinista o IA central opcional; ejecución del turboascensor **S12** |
| Horarios y vida social de NPC | Fase técnica **F12** |
| Mallas, decoración, texturas, construcción de escenarios | **Trabajo artístico fuera de Sistema 12** |

**Prueba estrella:** jugador o NPC cruza una puerta automática; jugador pulsa su camarote y abre; NPC sin autorización pulsa y suena timbre; jugador sube al ascensor y dice «a mi camarote», baja en **parada real más próxima** y recorre el pasillo; LCARS muestra el mapa y un NPC puede realizar el mismo recorrido con horario y acceso válidos.

Las referencias históricas de Sutherland requieren auditoría del Blueprint/código real y logs antes de considerarlas probadas para Enterprise-D.
