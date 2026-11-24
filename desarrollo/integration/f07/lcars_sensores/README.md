# F07 — Consola LCARS de Sensores (panorámica)

**Estado:** interfaz implementada en rama aislada. **Todavía no integrada en Unreal ni conectada al CoreRPG real.** No modificar F04/F05/F06, el proyecto de la Sutherland ni archivos originales.

## Diseño aprobado

- Azul/cian, contraste claro y sin atrezzo de información. Destino de laboratorio: consola inclinada horizontal de la USS Sutherland, aprox. **120 × 20 cm** como ejemplo de proporción **6:1** (NO medida verificada).
- Pestañas operativas: **Sensores** (mapa y selección), **Análisis** (resultados focales reales disponibles), **Contactos** (búsqueda), **Sectores** (cuadrantes observados) y **Registros** (avisos).
- Modos de **vista**, no falsas órdenes: GENERAL adapta escala, LARGO ALCANCE duplica el radio visual, DETALLE hace zoom y ANOMALÍAS filtra observaciones. No cambian escaneos F06.
- Filtros de naves, objetos, cuerpos y energía; afectan a mapa y listas.
- **SEGUIR** pide seguimiento, **CENTRAR** cambia el centro de la vista, **ANALIZAR** abre las observaciones y **IDENTIFICAR** solicita barrido focal. Toda orden real debe estar autorizada por Core; una aceptación no equivale a un resultado.
- Ratón y teclado exclusivamente. Teclas: 1–5 vistas, flechas izquierda/derecha contactos, C centrar, T seguimiento, A análisis, F identificación, Esc mapa, ? ayuda.
- Arquitectura independiente del puente Sutherland; más adelante soportará pantalla superior y controles inferiores de las cinco estaciones técnicas de la Enterprise-D.

## Probar sin Codex

En Windows, doble clic en **Abrir_Consola_F07.cmd** (Python 3 instalado). El servidor usa únicamente localhost 127.0.0.1 y abre el navegador. Al cerrar el terminal, se detiene. Alternativa: python preview.py.

**IMPORTANTE:** arranca en **DEMOSTRACIÓN**; cinco contactos son sintéticos, no salen del Sistema Aster ni existen en Core. SEGUIR cambia únicamente la demo; IDENTIFICAR registra una petición simulada sin modificar clase, confianza, mundo o identidad. El visor muestra SIN MODELO hasta disponer de un modelo certificado. Ninguna operación demo escribe CoreRPG.

Ejecutar las pruebas en la raíz del repositorio:

    node --test desarrollo/integration/f07/lcars_sensores/tests/*.test.mjs

## Contrato de integración real F06 → F07

El Host nativo futuro, **nunca el HTML**, autenticará F04Session, observador, operador, estación, autorización, reloj y revisión. Las vistas deben usar únicamente consultas de observador de la MISMA sesión F04/F05/F06:

| Campo mostrado | Fuente prevista |
|---|---|
| Nave, estación, tick y revisión | Sesión F04/CoreRPG |
| Estado real matrices | f06_array_status / f06_diagnostics y sección conectada |
| Contactos activos/perdidos | f06_contacts_page con F04Ref observador |
| Posiciones y distancias | F06ContactView.observed_*_milli_au y distance_milli_au |
| Categoría, confianza y clase | F06ContactView.observed_category, confidence_permille, class_id |
| Transpondedor | F06ContactView.transponder_id **solo si ya fue resuelto** |
| Avisos | f06_notices_page |
| Resultados focales | f06_results_page y comparación autorizada |
| Seguimiento | f06_tracking_status y f06_set_tracking, ocupación real |
| Identificación | f06_begin_timed_scan o f06_focus según la acción Core |
| Solicitud a Ciencia | f06_science_handoff (petición, NO informe terminado) |

No usar jamás ninguna función f06_host_* desde navegador, Blueprint de widgets, diálogos o redes no confiables. F13 materializa verdad mundial; la consola no descubre ni crea entidades por sí misma. science_truth de las fixtures Aster es privado y no se transmite.

### Entrada: proyección autorizada

La interfaz ofrece **window.F07Console.applyObserverSnapshot(snapshot)**. El contrato exacto (f07.observer.v1) es:

    {
      "schema":"f07.observer.v1",
      "session":{"ship_label":"USS SUTHERLAND","station_label":"SENSORES",
                 "tick":28800,"revision":120,"source":"CORE_F06",
                 "sensors_online":true},
      "capabilities":{"track":true,"focus":true,"science":false},
      "contacts":[{"id":"C-001","status":"active","position_milli_au":[500,-120,0],
                   "distance_milli_au":514,"confidence_permille":680,
                   "observed_category":1,"class_id":0,"class_label":null,
                   "transponder_id":null,"last_seen":28800,
                   "tracking_mode":0,"model":null}],
      "notices":[],"results":[]
    }

IDs siempre derivados de **contactos observados**, jamás IDs mundiales. El JavaScript rechaza esquema inválido, duplicados, revisiones Core antiguas, valores no finitos y categorías fuera del contrato; copia solo campos expresamente permitidos y suprime identidad/clase no observada. Esto es defensa de interfaz, NO reemplaza el filtrado y la autorización del Host. **No entregar secretos a JS pensando que la UI los ocultará**.

### Salida: intención no privilegiada

**window.F07Console.setCommandHandler(async intent => result)** instala la función que atiende intents. Ejemplo:

    {"protocol":"f07.intent.v1","command":"tracking",
     "contact_id":"C-001","expected_revision":120,"mode":1}

Se emiten tracking, focus o science; science añade analysis_kind:1. La respuesta es {accepted:true/false,reason?:string,snapshot?:projection}. Una aceptación espera una nueva proyección oficial antes de modificar el contacto. El Host recibe su propio F04Ref autenticado y genera allí sus claves idempotentes: el navegador no proporciona autoridad, actores privilegiados ni referencias host. Revalidar a cada llamada.

## Visualización 3D con certificación

El inventario F06 de 25 GLB es solo **metadatos candidatos**, NO modelos verificados. Ninguna nave 3D está aprobada para el visor F07 por el momento. Para habilitarlo:

1. Certificar derechos, geometría, clase, materiales, escala, rendimiento e importación UE5 del recurso real.
2. Confirmar mediante observaciones Core que se conoce la clase (class_id mayor que 0) y que el modelo corresponde a lo conocido. El Host publica model:{verified:true,asset_id:"recurso_aprobado",render_slot:"slot_ue"}.
3. Renderizar el modelo REAL mediante SceneCapture2D y render target en Unreal dentro del panel. El frontend ofrece **applyVerifiedModelFrame({asset_id,data_url})** para recibir fotogramas PNG/JPEG base64 (máximo 2,5 MB), exclusivamente si asset_id corresponde al contacto seleccionado y al certificado. En producción es mejor un render target/Widget Slate nativo que enviar frames como PNG repetidos. Esa integración sigue pendiente.

La bandera verified es una atestación **del Host** tras validación externa y no una elección de JavaScript. Una clase conocida, por sí sola, nunca activa un recurso.

## Pendiente en MSI/Unreal

1. Cerrar y seleccionar commit definitivo F06; compilar un adaptador nativo F04/F06→proyección filtrada y comandos con permisos.
2. Medir UV, píxeles reales, ancho/alto y perspectiva de una consola inclinada Sutherland. 120×20 cm fue un ejemplo, no un dato físico auditado.
3. Conectar WidgetComponent/Slate/WebBrowser según compatibilidad UE5 y los eventos de ratón/teclado. Verificar el input en el juego, no solo en navegador.
4. Mantener autonomía del barrido pasivo y del reloj Core: no presentar efectos instantáneos o energía inventada.
5. Integrar visor 3D certificado; antes, SIN MODELO.
6. Ejecutar pruebas UE NullRHI/D3D12, lectura, rendimiento y aceptación visual en la Sutherland.

## Aislamiento

Los únicos archivos definitivos nuevos están en **desarrollo/integration/f07/lcars_sensores/** y en su workflow exclusivo. F07 nace de main; F06 continúa en ramas separadas. No hay dependencias hacia laboratorios ignorados. Se han dejado intactos los originales y las fases anteriores.
