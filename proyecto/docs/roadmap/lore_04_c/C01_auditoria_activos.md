# LORE-04C01 — Auditoría de instalaciones y causalidad espacial

**Estado:** CANDIDATO DOCUMENTAL SIN MERGE NI RUNTIME. **Época:** TNG/DS9/Voyager, continuidad no impuesta posterior al corte de campaña.

## 1. Activos preexistentes

El sistema de instalaciones y vida de estaciones tiene **15/15 paquetes de referencia**, y mundos/asentamientos **18/18**: `proyecto/docs/roadmap/procedural_facilities_and_station_life_status_v0.1.json`, `procedural_worlds_settlements_civilizations_first_contact_status_v0.1.json`. También: `sistemas/universe/generation/settlement_infrastructure_contract.json`, `facility_existence_and_construction_causality_v0.1.json`, `sistemas/gameplay/facilities/facility_identity_model.json`, `facility_topology_model.json`. No generar una estación nueva para cada misión.

## 2. Infraestructura justificada

Localización, población, función económica/civil, suministro, tecnología, jurisdicción, presupuesto o capacidad del operador y época deben explicar existencia de una instalación. Separar **diseño nominal** de **estado operativo real**; un hangar no se convierte en hospital ni un pequeño puesto médico en astillero pesado porque el usuario necesita uno. Identidad y topología, una vez materializadas, permanecen hasta que eventos autorizados las modifiquen.

## 3. Vida civil interior

Los habitantes, visitantes, tripulantes de buques acoplados y trabajadores se contabilizan por categoría y ubicación. La estación no adquiere la dotación del barco en el que amarran ni duplica pasajeros. Aplicar `facility_residency_tenancy_visitor_model_v0.1.json` y `facility_watch_and_work_schedule_contract_v0.1.json`. Tiempo de acceso, turnos, soporte vital y servicios son límites reales; no decorado.

## 4. Riesgos

No inferir equipamientos de la etiqueta «base estelar». No asumir que todas las civilizaciones usan la misma escala, transporte orbital o servicio público. Los nombres de instalaciones oficiales y sus fechas deben contrastarse con el catálogo canónico; mundos inventados se clasifican `GAME_ADDITION` pendiente de aprobación si se vuelven relevantes.

**Propiedad de datos:** solo CoreRPG altera WorldState y produce eventos duraderos. Información de fuentes: `mundo/sources/canon_policy.md`; distinción SCREEN_CANON / OFFICIAL_REFERENCE / INFERRED / GAME_ADDITION. `UNKNOWN` para hechos o leyes no acreditados.
