# IDEA-0010 — Nave auxiliar táctica y furtiva integrada en la Clase Valhalla

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

## 4. Problema geométrico prioritario: NO cabe una Defiant completa en el alojamiento de un yate

Se aprueba **la zona ventral prevista inicialmente para el yate como ubicación conceptual preferida**, pero **no se aprueba todavía una solución geométrica concreta**.

Referencia de escala: el artículo de StarTrek.com sobre la Defiant describe una longitud aproximada de **170,68 m**, cuatro cubiertas y una tripulación de alrededor de 40. Como contraste, las referencias técnicas no oficiales de la nave auxiliar Cousteau sitúan el yate de la Enterprise-E en aproximadamente 33,5 m de largo. La Defiant no es una lanzadera de cuatro plazas y **no debe fingirse que entra físicamente en un hueco pensado para un yate**.

**Alternativas de estudio, todavía sin decidir:**

| Alternativa | Descripción | Implicación |
|---|---|---|
| **A — Diseño compacto derivado** | Crear una nueva nave táctica, de escala físicamente compatible con una instalación ventral de Valhalla, inspirada en la Defiant, reaprovechando y adaptando mallas/puente si procede. | Puede perder las dimensiones exactas del activo original; hay que adaptar puente, volumen e interiores con coherencia. |
| **B — Alojamiento/puerto mayor** | Diseñar en la Valhalla un hangar de operaciones especiales o estación de acople exterior capaz de recibir una nave de dimensiones Defiant. | Requiere revisar arquitectura ventral, profundidad, cubiertas, interferencias y operación de platillo separado. |
| **C — Atraque exterior especializado** | Acoplamiento al casco en un puerto o pilón adecuado, sin encerrar toda la nave en un hueco. | Resuelve parte del conflicto geométrico pero cambia silueta, accesos y exposición visual; debe validarse. |

El [sistema de hangares y atraque simulado — IDEA-0003](IDEA-0003_hangares_independientes_atraque_simulado.md) puede **ocultar la transición 3D**, pero **no altera el tamaño real ni autoriza interpenetrar cascos**. Distancias relativas, acceso interno, anclaje, maniobras y seguridad deben ser verosímiles.

**No elegir silenciosamente miniaturización ni agrandar el casco antes de revisar dimensiones de ambos modelos.** La selección definitiva de A/B/C queda pendiente de comprobación y aprobación artística del autor si modifica significativamente el exterior de Valhalla.

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
- punto de anclaje relativo al casco de Valhalla, velocidad y orientación coherentes;
- piloto automático, evasión, persecución y navegación individual, sin secuencias fijas en el control normal;
- entrada/salida cinematográfica si se usan entornos separados, sin duplicar la entidad;
- coordinación de fuego/autodefensa con nave nodriza, sin control remoto omnisciente cuando estén incomunicadas;
- separación del platillo de Valhalla: determinar **en qué sección** se sitúa físicamente el puerto y cómo se comporta cuando las dos mitades operan separadas.

El método de transición visual de [IDEA-0003](IDEA-0003_hangares_independientes_atraque_simulado.md) puede reutilizarse; el hecho del acoplamiento debe ser validado por el sistema autoritativo, no por una animación.

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
2. **AUX-02 — Estudio de integración Valhalla:** medir sección ventral, platillo, altura de cubiertas, colisiones, anclajes, separabilidad del platillo y alternativas A/B/C. Preparar comparación visual a escala antes de decisión artística.
3. **AUX-03 — Identidad y perfil:** definir nombre/clase/matrícula, dotación mínima, plantilla de tripulación, equipamiento, consumos, autonomía y límites de operación.
4. **AUX-04 — Prototipo exterior 3D:** hacer copia de trabajo en Blender/UE5, PBR, pivotes, iluminación, LOD/colisiones y cámara exterior.
5. **AUX-05 — Puente modular:** texturizar el puente blanco por etapas y conectar primero una consola funcional básica con el mismo sistema que las otras naves.
6. **AUX-06 — Atraque y persistencia:** acceso interior, autorización, acoplamiento y desacople seguros, recuperables en save/load y con entidad única.
7. **AUX-07 — Operaciones especiales:** pruebas de aproximación silenciosa, detección, despliegue de equipo, regreso y efectos de fallo; solo después evaluar camuflaje avanzado, ablativo y combate en coordinación.
8. **AUX-08 — Validación MSI:** pruebas de misión narrativa, NPCs, sectores espaciales, persistencia y rendimiento, incluyendo operación simultánea Valhalla/auxiliar.

**Estos hitos son planificación conceptual, no código implementado.** Antes de lanzar el trabajo se validarán dependencias reales de CoreRPG, UE5 y activos.

## 11. Criterios de aceptación y decisiones abiertas

### Criterios mínimos de la primera versión jugable

1. Activo exterior e interior de puente legalmente utilizables y técnicamente auditados en Blender/UE5.
2. Tamaño y acoplamiento visual creíbles y aprobados sin fingir que cabe una Defiant de 170 m en un hueco de yate.
3. Nave auxiliar persistente independiente, con tripulantes y carga sin duplicados.
4. Embarque desde Valhalla, salida con transición segura, navegación exterior y regreso completo cuando proceda.
5. Al menos una misión de reconocimiento/infiltración que pruebe el valor de la auxiliar sin requerir camuflaje infalible.
6. Límites efectivos de autonomía, daño y recursos para no sustituir a Valhalla.
7. Órdenes, maniobras y sensores usan sistemas generales y no lógica exclusiva de Defiant.
8. Separación del platillo, permiso de atraque, imposibilidad física y fallos de maniobra no generan duplicaciones.
9. Fluidez y Calidad contrastadas en MSI antes de declarar jugabilidad real.

### Cuestiones todavía no aprobadas

- Nombre, matrícula y clase definitivos de la auxiliar.
- Elección entre variante compacta, alojamiento amplio o puerto externo.
- Número **mínimo** de tripulantes y nivel de automatización.
- Qué partes del puente blanco y del exterior permiten reutilización sin alterar escala/diseño.
- Camuflaje completo o tecnologías furtivas menos extremas y qué restricciones legales/temporales aplican.
- Armamento, blindaje específico, autonomía exacta y capacidad de desembarco/aterrizaje.
- Ubicación final respecto al platillo y la sección motriz y efecto sobre su separación.

## 12. Vinculaciones y estado administrativo

- **Sustituye:** [IDEA-0004 — Yate del capitán (DESCARTADA)](IDEA-0004_yate_del_capitan_desacople_simulado.md).
- **Comparte infraestructura con:** [IDEA-0003 — Hangares](IDEA-0003_hangares_independientes_atraque_simulado.md), [IDEA-0008 — Entornos espaciales](IDEA-0008_entornos_espaciales_modulares.md), [IDEA-0009 — Maniobras](IDEA-0009_ordenes_protocolos_maniobras_universales.md), [IDEA-0006 — Temporadas](IDEA-0006_temporadas_narrativas_misiones_episodicas.md).
- **Armamento y blindaje:** [IDEA-0005 — Tecnología avanzada de Valhalla](IDEA-0005_blindaje_ablativo_y_torpedos_transfasicos_valhalla.md), con diseño y autorizaciones independientes para la auxiliar.
- **Gobierno creativo:** [Acta F01 de Valhalla](../docs/roadmap/master/fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md).
- **Fuentes de contraste:** [StarTrek.com: Defiant y datos de diseño](https://www.startrek.com/news/deep-cut-ds9-25th-anniversary-ships); [StarTrek.com: propósito de Defiant](https://www.startrek.com/news/designing-the-defiant); [Ex Astris Scientia: yate Cousteau](https://www.ex-astris-scientia.org/schematics/starfleet_shuttles.htm). Son referencias de escala y lore, no pruebas de nuestros modelos.

**Resultado:** nueva IDEA-0010 aprobada conceptualmente y preferida oficialmente **en sustitución integral de IDEA-0004**. Sus capacidades, modelo e integración quedan pendientes de desarrollo y prueba. El registro de esta decisión **no modifica los activos originales ni certifica una nave ya jugable en UE5**.
