# Consola de Sensores v0.3 · UX de puente

Estado: **PROTOTIPO OPERATIVO**

Ruta web de referencia: `academiaflota/holodeck/sensors-v03/`

## Objetivo

La v0.3 deja de presentar Sensores como una superficie de Academia o ejercicio y pasa a representar una **estación real de puente**. Reutiliza el Core funcional validado en v0.2, pero reorganiza la UX para operación continua.

## Distribución

- **Izquierda — Contactos**: contactos activos por defecto. Los perdidos se consultan en una vista propia para no ocupar la lista operacional.
- **Centro superior — Solución espacial**: dos visores simultáneos.
  - vista cenital: marcación del contacto seleccionado, línea de posición y flecha de curso;
  - vista de perfil: elevación positiva/negativa respecto al plano de la nave.
- **Centro medio — Computadora / Puente**: últimas comunicaciones operativas sin scroll infinito.
- **Centro inferior — Órdenes**: destino COMPUTADORA u OFICIAL AL MANDO, entrada por texto/voz y accesos rápidos.
- **Derecha — Situación**: estado de sensores, guardia, contacto seleccionado, seguimiento y vigilancias.
- **Pie — Herramientas DEV**: registro y escenarios de prueba, fuera de la lógica de juego final.

## Visor espacial

Hasta disponer de blueprints definitivos, la v0.3 usa siluetas de sustitución. El comportamiento funcional ya queda preparado:

- nave propia centrada con orientación fija;
- contacto seleccionado colocado por marcación;
- elevación representada en una segunda vista lateral;
- flecha de curso independiente de la posición;
- distancia, curso, velocidad, movimiento relativo y CPA resumidos bajo el visor;
- colores de prioridad/hostilidad derivados del estado, nunca de la especie o afiliación por sí sola.

Los blueprints futuros sustituirán las siluetas sin cambiar el contrato de datos.

## Reglas UX

- No existe scroll global de la página.
- El bloque central no crece con las comunicaciones.
- Solo se muestran comunicaciones recientes; el histórico completo permanece en registro.
- La lista activa de contactos no incluye contactos perdidos una vez concluida su transición visual.
- Las columnas laterales pueden usar scroll interno si el volumen de datos lo exige.
- La selección de un contacto actualiza simultáneamente visor espacial, ficha de situación y acciones rápidas.

## Funcionalidad heredada

La v0.3 conserva el comportamiento validado en v0.2:

- vigilancia pasiva 24/7 de corto y largo alcance;
- adquisición e identificación progresiva;
- detección de pérdidas explicables/anómalas;
- seguimiento normal/prioritario;
- vigilancia de curso;
- consultas y análisis;
- bloqueo de operaciones imposibles sobre contactos perdidos;
- texto y voz;
- Computer Gemini con routing económico;
- comunicación directa con el oficial al mando del puente;
- escenarios DEV de aceptación.

## Regla de arquitectura

La v0.3 cambia la **superficie**, no la autoridad:

**World State → Sensor Core determinista → estado observado → Computer/UX**

El visor no calcula ni inventa contactos. Solo representa datos ya resueltos por el Core.
