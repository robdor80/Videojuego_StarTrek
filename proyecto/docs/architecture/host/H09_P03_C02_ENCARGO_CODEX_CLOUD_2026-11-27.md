# HOST H09-P03-C02 — Encargo nativo propuesto para Codex Cloud (NO ejecutado)

**Modelo recomendado:** Sol 6.2 — **razonamiento Medium**.  
**Repositorio:** `robdor80/Videojuego_StarTrek`. **Base:** `main` tras C01/PR #231.  
**Estado:** PREPARADO POR CHATGPT. El propietario decide cuándo iniciar el consumo de cuota. Este documento **no** autoriza iniciar H09-P03-E, cambiar el pin de CoreRPG ni fusionar resultados.

## Prompt completo

STAR TREK RPG — HOST H09-P03-C02 (capacidad mínima de ubicación, carta y propuesta; NO movimiento)  
MODELO: Sol 6.2. RAZONAMIENTO: Medium. REPOSITORIO: robdor80/Videojuego_StarTrek.  
Crear rama propia y PR **Draft** sin fusionar; no tocar `main` directamente.

**Lecturas obligatorias previas:**
- `AGENTS.md` y reglas vigentes de trabajo/laboratorios.
- `proyecto/docs/architecture/host/H09_P03_C01_FACTIBILIDAD_CORE_2026-11-27.md` (resultado de PR #231, ya fusionado).
- `proyecto/docs/architecture/host/H09_P03_C02_DISENO_DOMINIO_NAVAL_2026-11-27.md`.
- `proyecto/docs/architecture/host/H09_P03_C02_CONTRATO_DOMINIO_NAVAL_v1.json`.
- `proyecto/docs/architecture/host/H09_P03_CONTRATO_NAVEGACION_CONN_v1.json`.
- `proyecto/docs/architecture/host/H09_P01_REGISTRO_CONSOLAS_v1.json`.
- `sistemas/gameplay/navigation/README.md` y `navigation_order_contract.json`.
- `sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_navigation_route_proposal_v0.1.json`.

**Objetivo acotado:**
1. **P0 ANTES DE PROGRAMAR:** comprobar la costura exacta de `F04Session`/`Campaign`, catálogo, bootstrap, `schema`, `HistoryPersistence`, identidad de nave, acceso por observador, generación y hilo dueño. Verificar si los hechos tipados de localización discreta y publicación de carta pueden convivir con la composición del **CoreRPG fijado en 76a7b7b485616d8c4994f384a90f123bf333591d**. El estado nativo de partida existente no tiene origen ni carta conocida. No inventar inicio en Tierra ni mutar estados de partidas viejas.
2. Entregar una propuesta de **diff mínimo de producto** (rutas exactas y firmas C++ recomendadas) y matriz de compatibilidad del guardado. Si exige ampliar CoreRPG, cambiar pin, romper esquema histórico, insertar Timeline naval de forma no respaldada o modificar F11: **detener implementación** de esa ruta y entregar informe técnico de bloqueo con alternativa concreta; solicita decisión diferenciada del propietario. La autorización de evaluar una extensión **no** autoriza automáticamente esos cambios.
3. Solo si P0 acredita una costura compatible bajo el pin y no requiere decisión pendiente, implementar `read_own_location` y `read_authorized_chart` internos sobre el **único Core WorldState y conocimiento del observador**. La ubicación desconocida debe ser null y las cartas no se hacen conocidas por estar en JSON de autoría. Ninguna ABI Unreal nueva ni APIs de maniobra.
4. Tras verificar P1, evaluar e implementar `propose_known_route` de lectura pura sobre **origen y destinos conocidos**, con perfiles existentes y aristas autorizadas. Las distancias/ETA desconocidas quedan null, y los errores no enumeran destinos ocultos. Propuesta efímera, no orden, sin alterar tick, RNG, archivo, recursos ni posición. Revalidar scope, generación y revisiones; invalidar en SAVE/RESTORE/CLOSE y cambios de conocimiento/autorización.
5. Implementar pruebas nativas para CN2-01…CN2-14 **solo cuando las capacidades existan**, con fixtures de campaña vieja/nueva, visibilidad por observador y comparación de bytes canónicos Core antes/después de propuestas y rechazos. Comparar la matriz N3-01…N3-14 sin inventar PASS. Ejecutar CI Linux/Windows y sanitizadores aplicables.
6. Si P0 permite únicamente lectura de `UNKNOWN` pero no publicar carta sin ampliar esquema: entregar esa capacidad **solo si es útil y genuinamente compatible**, documentar alcance y bloquear propuestas. No simular progreso o geografía con caché ni usar `F04_MOVE` para mover naves.
7. NO modificar CoreRPG, pin ni pruebas históricas. No implementar `CONN_MANEUVER_ORDER`, warp, impulso, progresión de viajes, F06, H09-P02, H09-P03-E/F, H09-P04 ni código UE que dependa del MSI. No tocar F11. Sin atajos autoritativos para IA.
8. Temporales únicamente en `laboratorios/` y limpieza propia conforme a `AGENTS.md`, con informe permanente liviano en `proyecto/docs/architecture/host/H09_P03_C02_C01_RESULTADO_CODEX_*.md`.

**Entrega:** rama y PR Draft sin fusionar, SHA, diff preciso, qué se probó realmente (nativo vs documental), CI, incompatibilidades y puntos que requieren decisión del propietario. Si se confirma bloqueo estructural, el informe de bloqueo es válido y **preferible a introducir una implementación incorrecta**.

**No declarar H09-P03 cerrada ni la navegación funcional en UE/MSI.**
