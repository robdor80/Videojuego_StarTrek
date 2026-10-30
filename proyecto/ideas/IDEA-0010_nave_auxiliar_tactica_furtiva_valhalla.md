# IDEA-0010 — Nave auxiliar táctica y furtiva integrada en la Clase Valhalla

> **ACLARACIÓN OPERATIVA EXPRESA DEL AUTOR:** Valhalla transporta los Marines, Defiant (tripulación técnica/naval de Flota destinada en Valhalla) los acerca a su objetivo. **Hijos de Odín NO pilotan ni gobiernan ninguna de las dos naves: son soldados de operaciones especiales, como los SEAL transportados por un submarino**. No asignarles puestos de puente/timón/navegación ni confundir dotaciones.

> **DECISIÓN POSTERIOR DEL AUTOR (31-10-2026) — MÁXIMA PRIORIDAD CONCEPTUAL:** **Proyecto Defiant = nave militar furtiva de clase Defiant + Marines «Hijos de Odín»**. La Defiant tendrá **tripulación naval especializada propia**; los **Hijos de Odín son soldados** de Flota, no personal de seguridad renombrado. Ambas dotaciones se contabilizarán dentro de los 1.800 miembros de Flota de Valhalla, separadas de los 400 civiles y sin duplicación entre naves. La idea provisional de **60 Marines + 40 tripulantes Defiant** no es cifra aún ratificada: F04 ajustará mínimos, descansos y estructura. Doctrina de Flota en continuidad propia: exploración/diplomacia más fuerza militar efectiva, operaciones encubiertas y disuasión ofensiva, con autorizaciones y consecuencias. **[Acta general DEC-0017–0019](../docs/decisions/valhalla_proyecto_defiant_hijos_de_odin_doctrina_2387.md).** Prevalece sobre eufemismos o la tesis histórica «no es militar». Se preservan los acuerdos sobre camuflaje romulano, yate descartado, acceso simulado y clase Defiant; apartados antiguos más prudentes son historial de diseño superado.


> **ACTUALIZACIÓN DE AUTOR (21-10-2026) — PREVALECE SOBRE EL TEXTO HISTÓRICO INFERIOR.** El autor ha decidido que la nave auxiliar será de **clase Defiant**, con nombre individual aún pendiente, dotación mínima, armamento y blindaje elevados para su tamaño y **camuflaje romulano excelente aprobado** (sujeto a fallos y contramedidas, no infalible). Coexiste con la Valhalla en la continuidad propia sin límite de año de canon televisivo. Véase [addendum de Valhalla y Defiant](../../mundo/lore/technology/valhalla_creative_addendum_2026-10-21.md). Se mantiene cancelado el yate de IDEA-0004 y el atraque simulado sin hangar físico Defiant. Las secciones antiguas que hablen de «inspirada, no clase Defiant», de camuflaje por aprobar, o de identidad original incompatible son **históricas y supersedidas**, no decisiones vigentes.


**Proyecto:** Videojuego Star Trek RPG 3D  
**Fecha de decisión:** 2026-10-17  
**Estado:** **APROBADA CONCEPTUALMENTE — PRIORIDAD PARA VALHALLA; NO IMPLEMENTADA**  
**Autoridad de la decisión:** sustitución expresa por el autor de la IDEA-0004 (yate del capitán).  
**Objeto:** nave auxiliar original inspirada visual y funcionalmente en la Defiant, con identidad, nombre, clase y matrícula propios aún por definir. **No es la USS Defiant canónica.**  
**Destino:** `/ideas` de `robdor80/Videojuego_StarTrek`.  
**Ámbitos:** Clase Valhalla · naves auxiliares · operaciones especiales · infiltración · reconocimiento · combate · acoplamiento · puentes 3D · CoreRPG/UE5.

## 1. Decisión creativa vigente y sustitución de IDEA-0004

**La Clase Valhalla NO incorporará como equipamiento elegido un yate clásico del capitán.** Su función y emplazamiento previsto se sustituyen conceptualmente por una **nave auxiliar táctica de tamaño compacto relativo a una nave capital**, inspirada en las líneas generales de la clase Defiant de `Star Trek: Deep Space Nine`.

El autor posee:
- Un **modelo 3D exterior de una nave tipo Defiant**.
- Un **modelo 3D del puente de la Defiant, actualmente blanco y sin texturas**.

Estos son **activos candidatos aportados por el autor**, cuya integridad, geometría, procedencia, licencia, escala, pivotes, materiales e importación en Blender y UE5 **no han sido verificados por este registro**.

Se desea reutilizarlos para crear una nave que pueda salir desde la Valhalla, cumplir misiones, operar separada —incluso junto a la Valhalla en combate— y regresar sin romper el estado del mundo.

La [IDEA-0004 — Yate del capitán](IDEA-0004_yate_del_capitan_desacople_simulado.md) pasa a estado **DESCARTADA / SUSTITUIDA**, conservando su documentación únicamente como historial. **No se mantiene como propuesta activa para Sovereign ni para Valhalla**, salvo que el autor reabra expresamente el diseño en el futuro. Los principios técnicos generales reutilizables de desacople, transiciones y persistencia se conservan en IDEA-0003 e IDEA-0010.

## 2. Rol jugable y experiencia deseada

La Valhalla es la **nave nodriza**, hogar y centro de mando principal del jugador. La nueva nave auxiliar es una plataforma pequeña y especializada respecto de ella, pensada para operaciones que una gran nave capital no puede acometer discretamente o para las que es imprudente exponerla.

Casos de uso propuestos:
- Reconocimiento discreto de zonas, instalaciones o cuerpos planetarios.
- Inserción, cobertura y extracción de equipos pequeños de **3–4 operativos** cuando la misión y el equipamiento lo permitan.
- Seguimiento de objetivos, incursiones e infiltración dentro de órdenes y reglas legítimas de misión.
- Rescate o evacuación selectiva con plazas/capacidades efectivas.
- Ataques rápidos, cobertura, apoyo o coordinación táctica con Valhalla u otras naves.
- Misiones especiales y arcos narrativos diseñados en los Season Packs.

**No equivale a una lanzadera decorativa ni a un crucero sustituto de la Valhalla.** La tripulación reducida de una misión de inserción **no implica** que una nave Defiant de tamaño íntegro pueda operar indefinidamente con cuatro tripulantes: dotación mínima, automatización, turnos y maniobras son requisitos a definir y probar.

El jugador podría embarcar o mandar la misión si su rango, puesto, aptitud y delegación de autoridad lo permiten; también pueden operarla los NPC por cuenta propia y con consecuencias persistentes.

## 3. Diseño exterior, interior y aprovechamiento de activos

- **Inspiración:** silueta compacta y contundente, vocación táctica, puente especializado, habitabilidad austera.
- **Identidad original:** nombre, clase, matrícula, esquema de casco y distintivos propios, no simplemente renombrar un buque existente.
- **Exterior:** partir de una copia controlada del modelo 3D disponible; mantener original intacto hasta verificar licencias, escalas y posibles modificaciones.
- **Puente:** utilizar el modelo blanco como base, revisar geometría, circulación, puestos, materiales PBR, iluminación, consolas funcionales, puertas, colisiones y rendimiento.
- **Interiores adicionales:** únicamente los necesarios para acceso y operaciones; ampliar modularmente según revisión visual y capacidades reales de volumen.
- **Tripulación y equipos:** ubicaciones y asientos reales; no añadir arbitrariamente camarotes o corredores incompatibles con un casco compacto.
- **Dos perfiles gráficos:** Fluidez y Calidad, con mediciones reales en el MSI.
- **Sin construcción inmediata:** este registro no afirma que los GLB/FBX, UE5 ni el puente sean jugables.

## 4. Decisión definitiva de arquitectura: alojamiento NO físico, transición simulada

**ACLARACIÓN EXPRESA DEL AUTOR (17-10-2026): el alojamiento de la auxiliar en Valhalla será SIMULADO, igual que el gran hangar y las cubiertas.** No hay que construir un hangar real ni encajar físicamente en el casco exterior el volumen del modelo Defiant. Esta regla **sustituye** las alternativas anteriores de miniaturizar, ampliar la bahía o construir un puerto capaz de contener físicamente toda la nave.

### Ruta principal de acceso aprobada

```text
PUENTE PRINCIPAL DE LA VALHALLA
        ↓
TURBOASCENSOR → destino «Nave auxiliar táctica»
        ↓
TRANSICIÓN / STREAMING DE ESCENA DISIMULADA
        ↓
INTERIOR 3D INDEPENDIENTE DE LA AUXILIAR
(puente tipo Defiant como espacio principal inicial)
        ↓
ORDEN DE SALIDA Y DESACOPLE
        ↓
ESPACIO EXTERIOR: NAVE AUXILIAR OPERATIVA
```

- **Acceso directo** desde el puente principal de Valhalla a través de un turboascensor, sin atravesar un gran hangar, corredores intermedios ni pasarelas físicas modeladas que unan ambas mallas.
- El turboascensor actuará como **puerta de cambio de escena/streaming**, conservando la identidad y posición de personajes y vehículo según la lógica del juego.
- Una vez en la auxiliar, el jugador podrá desplazarse por el **puente 3D existente** y por interiores adicionales que lleguen a construirse; en la versión inicial no hay obligación de crear toda la nave.
- El acceso se habilita **solo cuando la auxiliar está atracada y existen autorización, estado seguro y comunicación física de acceso lógica**; al desacoplar se bloquea ese trayecto. Un turboascensor de la Valhalla no «teletransporta» al jugador hacia una nave que ya está lejos.
- La ruta de regreso funciona en sentido inverso tras el reacoplamiento validado; personas, carga y puesto de servicio conservan continuidad.
- La auxiliar sigue siendo **una nave con tamaño y funcionamiento propios**, aunque su interior se cargue como escenario modular fuera de la geometría de Valhalla.

### Representación exterior sin bahía física

El punto de salida, retorno y eventual imagen de la nave acoplada puede utilizar un **anclaje exterior virtual relativo al casco** y una **transición cinematográfica/híbrida**. No se modelará una cavidad que deba albergar la nave completa. El diseñador deberá evitar mostrar intersecciones imposibles o escalas contradictorias en planos donde ambas naves sean visibles, eligiendo cámaras/transiciones creíbles.

La antigua preferencia por una zona ventral cercana al antiguo lugar del yate queda como **orientación artística provisional**, no una dimensión ni un compartimento físico aprobado. Si las vistas externas del acople revelan conflictos de escala, se resolverán por presentación/posición visual, no reconstruyendo por defecto el casco de Valhalla.

El hecho de que una Defiant completa tenga un tamaño considerable **deja de ser un bloqueo de construcción de interiores** gracias a la transición simulada. No obstante, **tamaño exterior, distancia de seguridad, colisiones y maniobras aparentes** siguen necesitando consistencia en las escenas donde ambos modelos se ven a la vez.

Esta elección hereda la filosofía de [IDEA-0003 — Hangares independientes y atraque simulado](IDEA-0003_hangares_independientes_atraque_simulado.md); se aplicará también a las cubiertas modulares de Valhalla.

## 5. Sistemas furtivos y armamento: capacidades condicionadas

Objetivos de diseño propuestos:
- **Baja detectabilidad:** opciones de reducción de firma, emisiones controladas, procedimientos de silencio e infiltración basados en reglas/sensores del juego.
- **Camuflaje óptico/sensórico completo (*cloaking*)** como posibilidad, **no equipamiento aprobado automáticamente**.
- **Blindaje ablativo** para la nave auxiliar si el balance y compatibilidad tecnológica lo permiten. La aprobación del blindaje de Valhalla en IDEA-0005 **no lo extiende por sí sola** a todos los vehículos secundarios.
- **Armas y maniobras ágiles** en su rango de uso, sin invulnerabilidad, munición infinita ni potencia equivalente a una nave capital.
- **Propulsión, sensores, escudos, autonomía, energía, mantenimiento y reparaciones** según sus características definitivas, sin números inventados.

**Canon y continuidad:** la USS Defiant de DS9 dispuso de un dispositivo de ocultación prestado por los romulanos bajo condiciones específicas; ello no implica que cualquier nave de la Flota, ni nuestra nave original, pueda equiparlo sin reglas. Esta capacidad se tratará como `GAME_ADDITION` o licencia tecnológica expresamente autorizada por el canon propio, con límites políticos, legales y técnicos en la época elegida.

Un buque furtivo no debe ser indetectable por decreto: el resultado depende de sistemas activos, entorno, tácticas y capacidades de los sensores adversarios.

## 6. Mando, dotación y vida de la nave auxiliar

- Entidad persistente única, asignación a Valhalla, matrícula/ID, ubicación, estado técnico, daño, recursos, personal, carga, armamento y misión.
- Equipo pequeño de incursión frente a **dotación operativa** completa: no equiparar sin pruebas ambas magnitudes.
- El capitán de Valhalla decide en su ámbito si autoriza la salida y designa al oficial o equipo responsable; no asume que todo subordinado deba estar siempre disponible.
- La tripulación embarcada deja de ocupar físicamente su puesto previo mientras dure la operación. Deben organizarse suplencias, guardias y cadena de mando.
- Puede efectuar misiones sin jugador y mantener actividad fuera de cámara.
- Los daños, abandono, pérdida o destrucción generan consecuencias reales; la nave **no reaparece gratuitamente en su atraque** al volver el jugador.
- Un oficial de rango inferior puede dirigir la misión por nombramiento válido; la cabina pequeña no convierte automáticamente al protagonista en capitán de la Valhalla.
- La Valhalla mantiene su funcionamiento y su vida cotidiana aun cuando la auxiliar esté de misión.

## 7. Desacople, navegación y regreso

Compartir [IDEA-0009 — Órdenes y maniobras universales](IDEA-0009_ordenes_protocolos_maniobras_universales.md) para:
- autorizaciones, aproximación, preparación y salida;
- **anclaje exterior virtual** relativo a Valhalla, con posición, velocidad y orientación coherentes durante las escenas vistas desde fuera;
- piloto automático, evasión, persecución y navegación individual sin secuencias fijas durante las operaciones ordinarias;
- **transición 3D simulada, no alojamiento físico:** turboascensor desde puente principal → interior independiente → salida cinematográfica/controlada a espacio exterior;
- coordinación de fuego/autodefensa con nave nodriza, sin control remoto omnisciente cuando estén incomunicadas;
- separación del platillo de Valhalla: definir a **qué sección pertenece el anclaje lógico y el acceso por turboascensor**; al separarse las secciones no se duplica el vehículo.

La ruta del turboascensor entre Valhalla y la auxiliar se habilita **solo si está realmente acoplada**. Al desacoplarse se cierra, sin acceso directo remoto. El reacoplamiento exige condiciones válidas y restaura el recorrido. UE5 representa la transición, pero CoreRPG/Host y reglas Star Trek autorizan posición, ocupantes y estado. No duplicar vehículos/personajes ni forzar acople si la maniobra falla.

## 8. Integración con temporadas narrativas y carreras

Los [Season Packs — IDEA-0006](IDEA-0006_temporadas_narrativas_misiones_episodicas.md) podrán incorporar episodios de reconocimiento, rescate, inserción, infiltración, vigilancia o apoyo, condicionados por el estado auténtico de la nave, del equipo, la política de la Flota y los requisitos del mundo.

La nave auxiliar aporta roles jugables distintos: oficial de sensores, jefe de misión, navegante, táctico, científico invitado, miembro de equipo de desembarco o mando legítimo. El jugador puede seguir siendo oficial en la Valhalla sin comandar la auxiliar en todas las operaciones.

Cada misión debe funcionar incluso si falla el camuflaje, se avería la nave o se aborta la inserción: los paquetes narrativos no prometen un desenlace.

## 9. Arquitectura y reparto de responsabilidades

| Sistema | Responsabilidad futura |
|---|---|
| **CoreRPG** | Identidad, persistencia, eventos, capacidades genéricas, ocupantes, recursos, estado y consecuencias en contratos existentes/validados, sin incorporar reglas Star Trek exclusivas. |
| **Videojuego StarTrek** | Definición de clase auxiliar, doctrina, autorización, configuración furtiva, armamento, dotación, permisos, misiones y reglas de acoplamiento a Valhalla. |
| **UE5 3D** | Modelos, puente, materiales, iluminación, cámaras, movimientos visuales, efectos, transiciones, colisiones e interfaces; sin reescribir resultados autoritativos. |
| **Blender** | Auditar mallas, orientación, escala, PBR, espacio habitable y variante de casco/puerto, manteniendo los originales. |
| **IA** | Interpretación y diálogo subordinados a permisos/información, no concede ocultación infalible ni resultados ficticios. |

**Áreas/fases candidatas:** F02/F03 integración y persistencia; F04/F05 tripulación y mando; F07/F14 activos y 3D; F09 consola/maniobras; F11 carrera y disponibilidad; F13 operaciones/misiones; F15 validaciones y QA. Sin reabrir fases cerradas ni modificar su estado por registrar una idea.

## 10. Plan incremental propuesto

1. **AUX-01 — Inventario físico:** identificar archivos locales exactos del exterior y puente tipo Defiant; comprobar formatos, topología, licencias, materiales, dimensiones y posibilidad de reutilización.
2. **AUX-02 — Alojamiento simulado y acceso directo:** diseñar la selección «Nave auxiliar táctica» en el turboascensor del puente principal de Valhalla, el cambio de escena y el anclaje exterior virtual sin cavidad física. Revisar vistas externas, colisiones aparentes y comportamiento al separar el platillo.
3. **AUX-03 — Identidad y perfil:** definir nombre/clase/matrícula, dotación mínima, plantilla de tripulación, equipamiento, consumos, autonomía y límites de operación.
4. **AUX-04 — Prototipo exterior 3D:** hacer copia de trabajo en Blender/UE5, PBR, pivotes, iluminación, LOD/colisiones y cámara exterior.
5. **AUX-05 — Puente modular:** texturizar el puente blanco por etapas y conectar primero una consola funcional básica con el mismo sistema que las otras naves.
6. **AUX-06 — Atraque, turboascensor y persistencia:** probar puente principal Valhalla → turboascensor → interior Defiant modular, autorización, bloqueo al desacoplar, regreso tras reacoplamiento y recuperación save/load sin duplicados.
7. **AUX-07 — Operaciones especiales:** pruebas de aproximación silenciosa, detección, despliegue de equipo, regreso y efectos de fallo; solo después evaluar camuflaje avanzado, ablativo y combate en coordinación.
8. **AUX-08 — Validación MSI:** pruebas de misión narrativa, NPCs, sectores espaciales, persistencia y rendimiento, incluyendo operación simultánea Valhalla/auxiliar.

**Estos hitos son planificación conceptual, no código implementado.** Antes de lanzar el trabajo se validarán dependencias reales de CoreRPG, UE5 y activos.

## 11. Criterios de aceptación y decisiones abiertas

### Criterios mínimos de la primera versión jugable

1. Activo exterior e interior de puente legalmente utilizables y técnicamente auditados en Blender/UE5.
2. Transición simulada válida desde el turboascensor del puente principal, **sin cavidad ni hangar físico**, con maniobra exterior coherente y sin mostrar penetraciones imposibles del casco.
3. Nave auxiliar persistente independiente, con tripulantes y carga sin duplicados.
4. Acceso directo puente Valhalla → turboascensor → puente/interior de la auxiliar; salida con transición segura, navegación exterior, bloqueo del turboascensor durante el vuelo y regreso solo tras reacoplamiento.
5. Al menos una misión de reconocimiento/infiltración que pruebe el valor de la auxiliar sin requerir camuflaje infalible.
6. Límites efectivos de autonomía, daño y recursos para no sustituir a Valhalla.
7. Órdenes, maniobras y sensores usan sistemas generales y no lógica exclusiva de Defiant.
8. Separación del platillo, permiso de atraque, imposibilidad física y fallos de maniobra no generan duplicaciones.
9. Fluidez y Calidad contrastadas en MSI antes de declarar jugabilidad real.

### Cuestiones todavía no aprobadas

- Nombre, matrícula y clase definitivos de la auxiliar.
- Diseño del anclaje exterior visual y encuadres/cinemáticas que ocultarán la falta de alojamiento físico, manteniendo escala creíble en escenas compartidas.
- Número **mínimo** de tripulantes y nivel de automatización.
- Qué partes del puente blanco y del exterior permiten reutilización sin alterar escala/diseño.
- Camuflaje completo o tecnologías furtivas menos extremas y qué restricciones legales/temporales aplican.
- Armamento, blindaje específico, autonomía exacta y capacidad de desembarco/aterrizaje.
- Asignación lógica del anclaje/turboascensor a platillo o sección motriz y efecto sobre la separación.

## 12. Vinculaciones y estado administrativo

- **Sustituye:** [IDEA-0004 — Yate del capitán (DESCARTADA)](IDEA-0004_yate_del_capitan_desacople_simulado.md).
- **Comparte infraestructura con:** [IDEA-0003 — Hangares](IDEA-0003_hangares_independientes_atraque_simulado.md), [IDEA-0008 — Entornos espaciales](IDEA-0008_entornos_espaciales_modulares.md), [IDEA-0009 — Maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md), [IDEA-0006 — Temporadas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md).
- **Armamento y blindaje:** [IDEA-0005 — Tecnología avanzada de Valhalla](IDEA-0005_blindaje_ablativo_y_torpedos_transfasicos_valhalla.md), con diseño y autorizaciones independientes para la auxiliar.
- **Gobierno creativo:** [Acta F01 de Valhalla](../docs/roadmap/master/fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md).
- **Fuentes de contraste:** [StarTrek.com: Defiant y datos de diseño](https://www.startrek.com/news/deep-cut-ds9-25th-anniversary-ships); [StarTrek.com: propósito de Defiant](https://www.startrek.com/news/designing-the-defiant); [Ex Astris Scientia: yate Cousteau](https://www.ex-astris-scientia.org/schematics/starfleet_shuttles.htm). Son referencias de escala y lore, no pruebas de nuestros modelos.

**Resultado:** nueva IDEA-0010 aprobada conceptualmente y preferida oficialmente **en sustitución integral de IDEA-0004**. Sus capacidades, modelo e integración quedan pendientes de desarrollo y prueba. El registro de esta decisión **no modifica los activos originales ni certifica una nave ya jugable en UE5**.
