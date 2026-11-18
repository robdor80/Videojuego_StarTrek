# Sistema 11 — Diseño funcional integral: Astrometría 360°

**Aprobación: 18-11-2026. Versión: 1.0. Estado: APROBADO EN DISEÑO, NO CERTIFICADO EN RUNTIME.**
**Nave: USS Enterprise NCC-1701-D / Galaxy Refit A2 / Proyecto Valhalla.**
**Referencias superiores: DEC-0023, DEC-0021 y DEC-0022.**

## A. Principio y experiencia de uso

Debe impresionar a primera vista y, a la vez, ser operativa a los diez segundos. Astrometría es una **gran sala de visualización holográfica tridimensional** que se explora en 360° desde una cámara o caminando alrededor de una proyección virtual. La misma información puede abrirse en consola LCARS, pantalla completa, o vista ligera remota en PADD.

El usuario puede pedir «Ordenador, muestra Vulcano», elegir el sistema, entrar en el planeta, consultar ciencia y comparar con Tierra. Una transición estética **se puede cancelar** y no bloquea datos disponibles. Debe poder usarse tanto para contemplar el universo como para preparar trabajo científico o una reunión.

## B. Escalas y geometría

| Escala | Vista | Información disponible |
|---|---|---|
| L1 galaxia/cuadrantes | Volumen de densidades/estructura galáctica agregada | Cuadrantes, regiones, posición de la nave, territorios conocidos |
| L2 región/sector | Estrellas catalogadas, nodos, rutas y fronteras | Bases, nebulosas, peligros, distancias, política y trayectos |
| L3 sistema estelar | Estrellas, cuerpos y órbitas visualmente diferenciados | Órbitas, planetas, estaciones y contactos legítimamente conocidos |
| L4 planeta/luna/objeto | Globo 3D con capas, señalizaciones y ficha | Atmósfera, temperatura, gravedad, terreno, océanos y datos conocidos |

**No** se representan como objetos individuales miles de millones de estrellas. En L1 se usan agregados; se individualiza lo que el jugador examina y lo que ya existe en el catálogo. El registro de identidad espacial es el mismo que usa el Universo Vivo.

Las medidas y distancias deben preservar el marco de coordenadas del dominio, con coordenadas de render locales y transformación estable. Cuando el dato Z no exista o no sea exacto, **NO asignar Z=0 en secreto**. Usar vista esquemática con etiqueta de confianza. Si se magnifican planetas/órbitas por legibilidad, indicar «escala visual no física».

## C. Interacciones y modos

Modos: **SALA_HOLOGRAMA_360**, **LCARS_PANTALLA_COMPLETA**, **PADD_COMPACTO**, **CONSOLA_REMOTA_AUTORIZADA**.

Acciones: mostrar destino, enfocar, girar en ejes X/Y/Z, ampliar/reducir, seleccionar objeto, ficha, comparar dos cuerpos, activar filtros, abrir rutas, preparar propuesta, presentar estudios, consultar registro histórico, visualizar predicción señalizada, restablecer vista y contemplación.

Entradas: teclado/ratón, mando, interacción in-world, UI LCARS y voz en castellano. El flujo normal no requiere OpenAI, servicio externo ni LLM ocupando VRAM. IA central solo interpreta intenciones complejas o resume datos filtrados si está configurada.

UX: una selección → una ficha completa; sin siete menús. Lista alternativa cuando se solapen cuerpos. Controles de accesibilidad: cámara fija o reducida, etiquetas legibles, contraste, proyección 2D/ortográfica y navegación sin voz.

## D. Hechos conocidos, Sensores y permisos

La representación solicita una **vista autorizada** a HOST/Core, nunca un snapshot interno con campos secretos. Cada dato tiene fuente, precisión, fecha y permisos cuando corresponde. Se diferencia «observado ahora», «registrado en carta», «transmitido por base de datos», «hipótesis» y «simulación».

La Enterprise-D Valhalla dispone de **sensores ordinarios extraordinariamente precisos y rápidos** mientras la configuración esté instalada/operativa (DEC-0021). Contacto ordinario alcanzable → resultado completo inmediato, automático o a petición, sin escaneos repetitivos. Registro remoto no significa observación física instantánea en otro cuadrante.

Nada de porcentajes azarosos de fallos ordinarios. Fenómenos excepcionales solo con causa legítima de trama. El cadete no ve secretos reservados por consultar Astrometría.

## E. Ciencia, comparaciones y conocimiento

Comparaciones de planetas/estrellas por variables que de verdad existan (composición, gravedad, temperatura, órbita, habitabilidad). Siempre incluir unidades/fuente y no inventar magnitudes ausentes. Análisis avanzado con Ciencia y resultados integrados al mismo expediente del contacto. Compartir presentación con oficiales autorizados sin filtrar conocimiento clasificado.

La vocación científica del protagonista puede reflejarse en interpretación, pero no garantiza toda investigación ni acceso secreto.

## F. Navegación, fronteras y tiempo

Astrometría consulta rutas del sistema existente de Navegación: rápida, segura, evitando espacios hostiles, con paradas de apoyo. Presenta ETA y riesgos **calculados por Navegación**, nunca números ficticios. Al pulsar «Enviar propuesta» genera un handoff estructurado. **No ejecuta warp, no cambia posición, no manda a oficiales por sí sola.**

Capas del universo: fronteras políticas variables, bases y colonias, anomalías, rutas comerciales y actividad legítimamente conocida. Las novedades llegan por observaciones/avisos; lo que CoreRPG conoce pero la nave aún no ha descubierto no aparece mágicamente.

Histórico: eventos realmente registrados. Futuro: **proyección hipotética con supuestos visibles**, jamás acceso a los hechos futuros de WorldState.

## G. Sala, estética y NPC

Galaxy Refit A2: gris perla, titanio, plata, azul pizarra, LCARS azul/cian, luz suave; holograma central envolvente y consolas discretas, compatible con interiores del Proyecto Valhalla. **Sin cubierta, dimensiones, puertas o ascensores fijados todavía:** se resolverá en diseño de interiores.

Los NPC científicos y oficiales pueden usar la sala según sus conocimientos, ubicación, tareas, rango y agenda. Un cadete presenta propuestas; capitán/oficial competente valida órdenes. No atar la sala al jugador ni exigir que esté en puente.

## H. Arquitectura y rendimiento

CoreRPG mantiene hechos y movimientos; Sensores detectan; Ciencia interpreta; Navegación calcula y ejecuta; HOST compone vistas permitidas y entrega deltas; UE5 presenta. **No introducir un segundo generador galáctico o segunda fuente de verdad**. El mapa debe usar LOD, instancias, culling, carga de sistema bajo demanda y origen de render relativo.

Medición pendiente sobre MSI RTX4070 8 GB: objetivo visual cercano a 60 FPS en exploración ordinaria y consultas disponibles con latencia objetivo inferior a 1 s. **No se han probado aún**. Añadir caída controlada de efectos a vista 2D sin perder consultas.

## I. Pruebas de aceptación para implementación

1. Cuatro escalas y vuelta al foco/posición, selección por ID persistente.
2. Holograma 360° auténtico y alternativa accesible.
3. Planetas ordinarios completos y legibles, sin retraso artificial.
4. Remotos desconocidos o clasificados no filtran verdad.
5. Z desconocida queda desconocida.
6. Comparación Tierra-Vulcano con campos/unidades reales.
7. Propuesta de ruta no cambia movimiento y respeta autoridad.
8. Universo Vivo actualiza lo conocido y conserva historia real.
9. Guardado/carga no duplica descubrimientos ni resetea contactos.
10. PADD y consola consultan información autorizada y rápida.
11. NPC trabajan independientemente.
12. Medir FPS, latencia, VRAM y memoria sin microcortes excesivos.

**Una prueba documental PASS no declara cumplida ninguna de estas condiciones runtime.**
