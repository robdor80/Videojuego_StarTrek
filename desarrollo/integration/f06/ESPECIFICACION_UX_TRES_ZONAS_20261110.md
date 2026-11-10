# PLANIFICACIÓN 01 · F06 — Especificación funcional de la consola Aster (tres zonas)
**Fuente:** documento del usuario «Consolas sensores Roberto.pdf» (3 páginas, 10/11/2026) y pruebas de guardia con capturas e historial.  
**Estado:** especificación de diseño aprobada por la solicitud del usuario; **NO equivale a implementación ni aceptación de F06**.  
**Prioridad:** sustituye como objetivo de UX al reparto anterior de lista + expediente; preservar motor, simulación y comportamientos que ya funcionan.

## 1. Principio
La consola es un puesto de trabajo de un oficial de sensores de la USS Enterprise-D, no un monitor de depuración. Se organiza en **tres zonas claramente diferenciadas**:
- **Izquierda — OPERACIONES:** escoger modo de trabajo y objeto(s), con navegación comprensible.
- **Centro — ÁREA PRINCIPAL (la más grande):** vista del mapa espacial y datos operativos específicos del modo elegido, con selección reactiva.
- **Derecha — INFORMACIÓN COMPLEMENTARIA:** detalles del objeto, imágenes/modelos cuando existan, cálculos, consulta técnica útil y acciones contextualizadas.

Conservar la vigilancia automática en segundo plano, botones legibles y jerarquía cian/azul cuando corresponda. **No volver a llenar pantalla de IDs, confianza, transpondedores, registros de motor ni mensajes triviales**. Ningún aviso desplaza o hace inaccesibles controles inferiores. Mantener scroll del usuario en actualizaciones.

## 2. OPERACIONES (izquierda)
Hay cuatro entradas principales, exactamente estas:

### GENERAL
Lista de **todos los objetos detectables dentro del alcance**; agrupar y desplegar:
- Estrellas: nombre conocido.
- Planetas: número/nombre ordinal y clase conocida o provisional.
- Asteroides: cantidad observada.
- Naves: tipo/clase y organización si se puede establecer, distinguiendo diseño conocido de identidad real no comprobada sin mentir.
- Estaciones: nombre, tipo y organización cuando se conozcan.
- Sondas: tipo, organización y función cuando estén identificados.
- Otros objetos (lunas, nebulosas, lanzaderas, anomalías): mantener los datos útiles y coherentes del inventario actual.

### CONTACTOS
- Vista de **contactos nuevos** que han entrado en alcance (no otra copia de GENERAL).
- Al producirse una nueva detección relevante, Aster **avisa y selecciona automáticamente CONTACTOS**, con el nuevo contacto seleccionado y su ficha central visible.
- Mantener una referencia de contactos nuevos e históricos de la guardia, sin perder la posibilidad de consultar otro objeto. La selección no debe saltar ni el scroll resetearse con cada tick.
- Identificación de una nave detectable no camuflada en **2–5 segundos como máximo**, sin pedir estudio largo.

### SEGUIMIENTO
- Lista **solo de contactos que el oficial ha marcado para seguimiento**: p. ej., de nave klingon y lanzadera nuevas, solo marcar crucero klingon si es el que interesa.
- La pantalla central se dedica a su movimiento: trayectoria, rumbo estimado, acercamiento/alejamiento, cambios, posible interceptación con la Enterprise **y con otras naves detectadas**, y seguimiento continuo.
- Alertas de maniobra realmente visibles; persistir hasta atención/acuse, sin quedar sepultadas por confirmaciones de tareas. Separar una *proyección de interceptación* de la *intención hostil*, que no es deducible solo del rumbo.
- El cálculo respecto a otra nave requiere comparar trayectorias observadas de ambas (posiciones con tiempo y un mismo marco); nunca inferirlo de un solo punto. Indicar estado desconocido si los datos no bastan.

### ANÁLISIS
- Catálogo de **contactos sobre los que se ha pedido análisis detallado**; no un contador de tareas.
- Para cada nave estudiada: todos los resultados **realmente obtenibles**, ordenados por utilidad: ataque y armas, defensas, propulsión, sensores/comunicaciones, estado de sistemas, tripulación estimada si procede, anomalías y riesgos.
- **Duración máxima del análisis solicitado: 20 segundos reales a ×1**, con porcentaje de avance basado en trabajo de Core; la barra desaparece tras completar, permaneciendo el informe.
- Conservar y reutilizar informes dentro de WorldState y guardar/cargar. No presentar como escaneado lo que solo es una ficha teórica de la clase; etiquetar las capacidades conocidas y las verificadas de la unidad.
- La complejidad y profundidad de otros análisis científicos puede tener modalidades adicionales cuando sean diseñadas expresamente; el tope de 20 s aquí responde al análisis detallado solicitado para esta consola.

## 3. CENTRO: contenido dinámico, zona más grande
El centro **debe cambiar de verdad al elegir una operación**:
- GENERAL: mapa de todos los contactos dentro de alcance + inventario útil asociado.
- CONTACTOS: mapa y ficha operativa inmediata del nuevo contacto, su identificación, clase/tipo/organización cuando estén corroborados.
- SEGUIMIENTO: mapa y datos de navegación/seguimiento de contacto seleccionado, con alertas de maniobras en vivo, cambios de rumbo, posible interceptación propia y de terceros.
- ANÁLISIS: resultados profundos de objetos analizados; navegación entre varios expedientes sin perder resultados.

### Mapa
- Grande y legible, con **zoom ajustable** (y control de encuadre). Evitar el apelotonamiento actual.
- GENERAL presenta todos los objetos que proceda.
- Cuando se selecciona **un contacto**, ofrecer/fijar vista relativa **solo nuestra nave y ese contacto**, ocultando los demás para no confundir. Mostrar distancia y dirección relativa fiables; facilitar retorno a vista general.
- Cambiar operaciones/selecciones cambia la vista central y su mapa; no volver a un gráfico diminuto repetido en todos los modos.
- El usuario puede navegar/zoom sin que las actualizaciones del motor anulen su gesto.

## 4. DERECHA: detalle contextual útil
- GENERAL: información amplia del sistema Aster y situación del espacio en el que nos hallamos.
- CONTACTOS: identificación ampliada, detalles conocidos e imágenes del objeto **solo cuando existan recursos reales**.
- SEGUIMIENTO: cálculos precisos de trayectoria, máxima aproximación, posibles cursos de interceptación propios o hacia otra nave, incertidumbres relevantes.
- ANÁLISIS: información adicional, sistemas de la unidad escaneada, fichas de clase de Flota; **acción para enviar a TÁCTICA un informe profundo**.
- «Consultar datos técnicos» debe mostrar **en esta zona derecha**, no abrir una ventana de registros con tokens y claves del motor. Especificaciones navales consultables y contextualizadas: armamento, defensas, sensores, capacidad de propulsión, etc. No remitir al jugador a un archivo inexistente ni presentar IDs de entidades como contenido.

**Compartición de información con TÁCTICA:** el **feed de contactos y trayectorias** es común en tiempo real sin botón manual; el botón de ANÁLISIS envía/marca un *informe profundo* específico para la evaluación táctica. La consola táctica definitiva, sus permisos y visualización se integrarán en su fase; no declarar esa UI como terminada desde F06.

## 5. Casos de aceptación obligatorios
1. Inicio de guardia: GENERAL muestra correctamente estrella, planetas, asteroides, naves, estaciones y sondas según observaciones disponibles.
2. Detectar Vor'cha: alerta visible; identificación en <=5 s; pasa a CONTACTOS; mapa enfoca Enterprise+Vor'cha sin objetos innecesarios; reloj a ×1 por detección relevante; regreso a velocidad anterior a decisión del oficial.
3. Marcar Vor'cha en SEGUIMIENTO: aparece en lista propia, se actualiza rumbo y variación de distancia sin pulsar SEGUIR repetidamente.
4. Cambios de rumbo hacia Enterprise y hacia otra nave: se distinguen aviso de cambio, acercamiento y *posible* interceptación; ambos parten de datos observados, no inventados. La alerta no se pierde bajo confirmaciones.
5. D'deridex al revelarse: clase y ficha de tipo romulano conocidas; si el escenario suministra posiciones, rumbo calculado en segundos y seguimiento sostenido (no caducidad por falta artificial de snapshots).
6. GENERAL y mapa: zoom/resolución adecuados para objeto lejano; foco individual enseña solo Enterprise+objetivo; interacción estable durante tick automático.
7. ANALISIS: un informe real en <=20 s a ×1, con barra porcentual y resultados verificables; informe persistente sin barra eterna.
8. Panel derecho ofrece datos navales útiles de Intrepid, Vor'cha y D'deridex (sin «consultar catálogo») y no relleno de motor.
9. Compartición con Táctica: el feed observado coincide, el botón de informe profundo se distingue del feed; no prometer UI Táctica que aún no existe.
10. Guardar/recuperar la guardia no destruye selección de seguimientos, historial útil ni informes; pruebas Windows/Linux + validación visual MSI. Mantener F06 abierta hasta entonces.

## 6. Reorganización de implementación (sin romper CoreRPG)
1. **Contratos y estado UI:** diferenciar inventario, novedades, contactos seguidos y análisis solicitados; distinguir datos observados, inferidos y catálogo.
2. **Layout tres columnas:** migrar la jerarquía actual a izquierda; centro realmente principal y reactivo; derecha contextual con scroll interno; preservar pie y alertas.
3. **Mapa:** zoom/pan/reencuadre, overlay focal de dos contactos; actualizaciones no afectan al manejo del jugador.
4. **Seguimiento continuo:** ampliar modelo de trayectorias de Core/runner sin inventar movimiento, añadir comparación entre naves; separar detección de intención.
5. **Analítica y ficha técnica:** resultados profundos estructurados disponibles al oficial, reconocimiento rápido, archivo persistente, catálogo técnico correcto.
6. **Puente Táctica + pruebas:** feed común; acción de compartir informes; UX en MSI con escenarios automatizados.

**Alcance y límite:** el PDF es el contrato funcional de la nueva UX. El resto que funcione correctamente puede mantenerse. No se da por hecho que la interfaz, el cálculo de intercepción entre otras naves, el catálogo técnico exhaustivo o la UI táctica estén ya implementados.
