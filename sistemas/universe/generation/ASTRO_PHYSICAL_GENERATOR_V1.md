# Generador astrofísico Star Trek v1 — física antes que biología

**Estado:** versión de referencia ejecutable. No supone una galaxia simulada, ni prueba UE5/MSI, ni la integración definitiva de F13. Respeta y NO reemplaza el generador histórico v0.0.1.

## Dos versiones con un mismo núcleo

- **General `game`**: secuencias principales O/B/A/F/G/K/M, sistemas simples y binarios circumbinarios aproximados, 3–9 planetas, lunas con límites de Hill, cinturones de asteroides, cometas, nueve familias planetarias, y su física, atmósferas, posibles océanos, biosfera y clase Star Trek candidata.
- **Aster `f06`**: adaptación de los **seis planetas y cuatro lunas** de la fixture F06 existente. Deriva sus perfiles sin escribir nada en la fuente original: el archivo enriquecido queda en el árbol de compilación ignorado. El compilador C++ recibe únicamente posiciones/firma/tipo general, nunca secretos científicos.
- Funciones especializadas de verdad del Host: `compact_object(seed, kind)` admite agujero negro, enana blanca, estrella de neutrones, púlsar y enana marrón como objetos individuales **sin inventar superficies ni planetas habitados**. `environmental_region(seed, kind)` admite nebulosa, remanente de supernova, disco protoplanetario y región de radiación; agujero de gusano y subespacio requieren procedencia explícita Star Trek.

## Catálogo de sector

`astro_sector_v1.py` agrupa 1–25 sistemas completos en una vecindad espacial, con posiciones 3D separadas en años luz, IDs estables y aparición ocasional (no obligatoria) de remanentes compactos o nebulosas. No simula una galaxia completa ni movimientos interestelares. CLI: `python desarrollo/tools/generation/astro_sector_v1.py --seed partida_001 --sector 041 --systems 4 --output laboratorios/astro/sector.json`. Pruebas: `python desarrollo/tools/generation/test_astro_sector_v1.py`.

## Orden causal innegociable

1. Semilla+sector+era+fecha y veto de reserva canónica. No se vuelve a inventar un planeta del canon.
2. Masa, luminosidad, radio, temperatura y vida de la estrella. En binarias, suma de luminosidades y distancia circumbinaria de seguridad aproximada.
3. Órbitas, flujo estelar, años orbitales y separación por radios mutuos de Hill. La línea del hielo deriva de la luminosidad.
4. Familia y masa planetaria -> radio, densidad y gravedad. Gaseosos: sin superficie accesible.
5. Temperatura de equilibrio (albedo+flujo) y, solo con suelo, efecto invernadero aproximado y presión. Composición gaseosa normalizada a 1.
6. Agua líquida/hielo, terreno, exposición y **habitabilidad potencial**, que no significa vida.
7. En otra semilla independiente: posibilidad de vida microbiana/compleja; vegetación y oxígeno abundante requieren procesos biológicos compatibles. La civilización y el primer contacto son capas distintas.
8. Solo ahora, **clasificación Star Trek candidata**, una traducción lúdica de la física, no un dato físico exacto ni etiqueta canon.
9. Persistencia autoritativa: una vez materializado en CoreRPG se carga y evoluciona; los escáneres y las IA no lo regeneran ni inventan datos ocultos.

## Familias y reglas anticontadicción

| Familia | Superficie | Agua/vida natural terrestre | Clase Star Trek candidata |
|---|---|---|---|
| Roca, supertierra | Sí | Condicional a presión, calor y agua | M/L/H/P/Y según física |
| Desierto, lava | Sí | Sin mares ni bosque natural por defecto | H/Y |
| Mundo oceánico | Sí | Requiere agua líquida estable y presión | M candidata |
| Roca helada | Sí | Superficie congelada, no bosque | P/L |
| Mini-Neptuno, gigante helado | No superficie abierta | No biomas de suelo ni árboles | J candidata, no clasificación definitiva |
| Gigante gaseoso | No superficie abierta | No suelos ni bosques | J |

El modelo incluye además rotación, oblicuidad, bloqueo por marea estimado, posible magnetosfera, recursos químicos genéricos y sistemas de anillos. Son semillas físicas de configuración, no resultados de evolución geológica avanzada.

El simulador comprueba gravedad, Kepler, flujo/temperatura, suma de gases, límites de órbitas y lunas, prohibición de vida en mundos inadecuados y separación de secretos científicos.

## Comandos de pruebas

```bash
python desarrollo/tools/generation/astro_physics_v1.py --seed partida_001 --profile game --output laboratorios/astro/sistema.json
python desarrollo/tools/generation/enrich_aster_f06_v1.py --source desarrollo/integration/f06/fixtures/aster_f06_qa.json --output laboratorios/astro/aster_host.json
python desarrollo/tools/generation/test_astro_physics_v1.py
```

CI: `.github/workflows/astro-physical-generator-v1.yml` en Windows y Linux. La fixture F06 sigue validándose con la compilación nativa compartida de CoreRPG.

## Coherencia y límites científicos

Las fórmulas de equilibrio radiativo, tercera ley de Kepler y estimaciones de masa-radio son **aproximaciones simplificadas**. No representan cálculo N-body, simulación climática tridimensional, evolución química real, estabilidad de órbitas durante millones de años ni probabilidades reales de biología extraterrestre. Un sistema puede necesitar ajuste por fuerzas de marea, migración, actividad estelar, tectónica, presión y efectos atmosféricos no incluidos. No se deben presentar estos datos como mediciones NASA.

- NASA, tipos de exoplanetas: https://science.nasa.gov/exoplanets/planet-types/
- NASA, sin superficie de los gigantes gaseosos: https://science.nasa.gov/exoplanets/gas-giant/
- NASA, zona habitable NO equivale a vida confirmada: https://science.nasa.gov/exoplanets/habitable-zone/
- NASA Exoplanet Archive, fórmulas para luminosidad, temperatura de equilibrio y flujo: https://exoplanetarchive.nexsci.services/docs/pscp_calc.html
- NASA, agujeros negros: https://ciencia.nasa.gov/universo/que-son-los-agujeros-negros/

## Integración futura pendiente

- **CoreRPG/F13**: materialización real, historial y cambios de estado; no tratar JSON como guardado real.
- **Ciencia/F07**: la composición y las formas de vida son verdad del Host; deben entregarse solo mediante resultados de escaneo/analítica legítimos.
- **Unreal**: modelos/UV/licencia/escala; no se han importado assets del MSI.
- **Canon**: sistemas conocidos se importan con fichas autorizadas, nunca se sobrescriben.
- **Lore**: las clases Star Trek aplicadas son aproximaciones de juego pendientes de aprobación; no reglas científicas NASA.

## Reglas de sostenibilidad

El generador está versionado: cambiar algoritmos o semillas de distribución exige nueva versión y migración explícita; no rerollear partidas ya materializadas. Las naves, ciudades, razas, política, anomalías exóticas y dinámicas climáticas pertenecen a otros subsistemas ya planificados, no se crean arbitrariamente para entretener al jugador.
