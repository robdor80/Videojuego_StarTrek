# A01 — Auditoría de actualidad documental LORE-01–05

> **Nota de vigencia (23-11-2026):** este es un corte histórico anterior a la revisión personal del autor. Las decisiones posteriores de DECISIONES_RATIFICADAS_20261123.md y C11/C12/C14/C15 actualizados **prevalecen**; no reinstaurar genealogía, guion ni misiones VAL-N01–VAL-N08 citados indirectamente en informes antiguos.

**Corte:** 22-11-2026 · **Línea base:** `main@8e9c7064`. Este documento es una **reconciliación focalizada**, no una afirmación de haber leído línea por línea todo el repositorio ni de haber ejecutado todos los validadores anteriores.

## Hechos de GitHub contrastados

- LORE-01–04 tienen cierres documentales históricos y planes trazables; LORE-05A–F tiene cierre documental #124–#131. Que un bloque se haya cerrado no convierte sus catálogos en módulos ejecutables.
- #169 incorporó DEC-0022; #188–#192 implementan partes nativas de creación única, PERSON, H03 y H04; #193–#197 aportan fachada, integración SDK y menú C-04; #198 deja protocolo C-05/M1. Las diez PR #189–#198 aparecen **fusionadas** en el corte.
- El control `proyecto/docs/architecture/host/H06_CONTROL_UNICO_ESTADO_2026-11-21.md` distingue nativo probado de UE/MSI pendiente. **M1 y C-05 no certificados**. Ni `S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md` ni `s04_fixed_protagonist_contract_v2.json` reflejan solos toda la implementación posterior.
- #175 y #178 permanecían abiertas al corte y sus cambios no se asumen presentes en `main`.

## Matriz de hallazgos y resolución

| ID | Fuente antigua / contradicción | Prevalece | Acción documental segura |
|---|---|---|---|
| LOR-01 | `CONTENT_STATUS.md` marca TODO en `sistemas/universe/chronology/historical_events/`, mientras LORE-03A documenta `mundo/lore/historical_events/`: **rutas diferentes**, no contradicción demostrada | Conservar la separación datos de referencia / implementación | No actualizar la fila TODO sin auditar ese consumidor técnico; sí enlazar la ampliación documental B03 |
| LOR-02 | Atlas `lore03_a_yearly_atlas_v0.2.md` todavía describe Valhalla como clase nueva | DEC-0020, 13-11 | Mantener atlas como evidencia temporal y agregar lector de precedencia; no migrar IDs |
| LOR-03 | `valhalla_tech_decisions_v0.1.json` contiene `class_identity=NEW_VALHALLA_CLASS...` | DEC-0020, DEC-0021 | Mantener JSON legado; tratar 16 VAL-TEC como candidatos a refit individual en matriz A02 |
| LOR-04 | S04 v2: cabecera «todavía no implementado» y campos `UNDECIDED` | PR #188–#198 y nueva autorización 22-11 | Anexos narrativos y nota de estado actual; **no tocar el JSON empotrado** |
| LOR-05 | Biografía v1 prohíbe inventar padres/educadores sin coautoría | Autorización expresa y posterior 22-11 | Resolver esos huecos solo en **anexo nuevo versionado**, `GAME_ADDITION`; preservar el contrato |
| LOR-06 | LORE-05B atribuye a Riker vicealmirante/cargo de flota; visión posterior lo sitúa como «capitán» recurrente de Enterprise-D | Separación rango, función y mando efectivo | Posible **capitán del buque en sentido funcional** tras orden/alta, sin degradación de rango ni retroactividad (C12) |
| LOR-07 | Fichas de Data, Sisko y Siete incluyen ventanas y posibles resultados futuros | Política de campaña emergente | Reescribir como **condiciones**, alternativas y puertas de hechos; nunca crear desenlaces inevitables |
| LOR-08 | H06 y S04 antiguas sugieren Academia 3D amplia | Decisión posterior 22-11 | Tutorial 2D narrativo; menú C-04 es infraestructura, no experiencia terminada |
| LOR-09 | `proyecto/docs/roadmap/lore_04_master_plan_v0.1.md` llama «propuesto» al año 2383 en introducción histórica | DEC-0020 y DEC-0022 | Nota de prevalencia en índice de operación: año aprobado, día/mes no |
| LOR-10 | Catálogos LORE-02 mantienen `NEEDS_REVIEW` aunque sus fases se cerraron documentalmente | Estado de fichas y actas de auditoría son dimensiones distintas | No reemplazar estado individual por `COMPLETE` sin per-record evidence; anexo de explotación A04 |
| LOR-11 | La restauración de Enterprise-D de 2401 y casco Syracuse podrían proyectarse al 2387 | Canon posterior y continuidad divergente | 2387 no usa ese casco por defecto y la misión no fuerza alta |
| LOR-12 | «estar en el catálogo» se confunde en algunos consumos hipotéticos con «estar operativo» | CoreRPG y capas de conocimiento | Restringir consultas a existencia + fecha + equipamiento + permiso + observación + estado vivo |

## Auditoría de precisión del 22-11-2026

La primera hipótesis LOR-01 se descartó tras comparar las **rutas completas**: el TODO de `CONTENT_STATUS.md` se refiere a `sistemas/universe/chronology/historical_events/`, no al atlas de `mundo/lore/historical_events/`. No se alteró el estado técnico por un falso positivo. Esto constituye una **corrección real de la auditoría**, no una deuda nueva.

## Precedencia temporal

1. Hecho de pantalla efectivamente anterior al comienzo `D`: ancla de pasado (con prueba de fecha).
2. Acuerdo autoral original: `GAME_ADDITION` mientras no lo supere una decisión posterior de idéntico alcance.
3. DEC-0020 y 0021: Enterprise-D Galaxy con Proyecto Valhalla; objetivo de sensores avanzado sujeto a instalación.
4. DEC-0022: protagonista único con linaje Khan; no creación libre.
5. Autorización 22-11: cerrar huecos ordinarios y creativos **documentalmente**, sin firmar actos por CoreRPG.
6. Hechos futuros después de `D`: solo se vuelven verdad mediante evento real de campaña.

## Cobertura de las cinco familias y controles diferidos

- **LORE-01:** especies, civilizaciones, diplomacia y cartografía existentes; expansión de lecturas clínicas/sociales sin cambiar taxonomías.
- **LORE-02:** 45 sistemas de A, 73 dispositivos de B, atlas clínico de 26 especies C, 20 fenómenos D; se conservan `NEEDS_REVIEW` sin falsificar controles exhaustivos.
- **LORE-03:** 40 referencias diplomáticas previas y 26 anclas nuevas; atlas temporal antiguo retenido; extensión futura condicionada.
- **LORE-04:** sociedad/economía/infraestructura/instituciones terminadas en diseño; no se activa economía viva o jurisdicción en runtime.
- **LORE-05:** 12 legendarios cerrados, 16 localizaciones y varias matrices ya fusionadas; este paquete **no añade NPC televisivos**.

**Pendiente de implementación:** pruebas en MSI, audio/escenas/activos, dotación y geometrías Galaxy, habilitación de enciclopedia y PADD, memoria y permisos NPC, avance de campaña, migraciones de contratos y accesos F11. No convertir deuda técnica en defecto del cierre documental histórico.
