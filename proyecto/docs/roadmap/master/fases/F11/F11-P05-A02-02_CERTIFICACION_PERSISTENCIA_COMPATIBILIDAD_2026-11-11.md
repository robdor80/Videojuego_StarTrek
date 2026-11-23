# F11-P05-A02-02 — Certificación de persistencia y compatibilidad

**Fecha de apertura:** 11-11-2026.  
**Alcance certificado mediante evidencia A02-01:** únicamente el primer ascenso
**alférez 1101 → teniente júnior 1102** dentro de la misma sesión F04/CoreRPG.
**Estado del corte A02-02:** auditoría de evidencias comprobada; la nueva CI
independiente de esta PR debe finalizar en verde antes de aceptar su cierre.
No declarar **F11 COMPLETADA** ni **UE5 JUGABLE** con este documento.

## 1. Base exacta: no inferir compatibilidad de la palabra «fusionado»

- PR de implementación: [#106](https://github.com/robdor80/Videojuego_StarTrek/pull/106), fusionada el 11-11-2026.
- HEAD A02-01 auditado: `620badb781a3b5505325621e7c12109bd4379d39`.
- Commit real de fusión en main: `d54457f20712849902b3815cc20a68ac813bcc4d`.
- **Tree Git de ambos: `7538df58a95c2634cc8027c4a51adc51dd0994b6`**. La igualdad de árbol, comprobada contra el API Git, acredita igualdad completa de archivos, no similitud por nombre ni un mero resultado de CI ajeno.
- CoreRPG F05/F11: `76a7b7b485616d8c4994f384a90f123bf333591d`.
- Core F04 estable: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.
- Core F04 histórico: `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`.

No se ha cambiado CoreRPG, sus pins, el esquema de F04 legacy, la semántica F05
ni los manifiestos/oráculos históricos para aprobar este corte.

## 2. Evidencia ya ejecutada sobre el árbol fusionado

Los **siete workflows del HEAD A02-01** finalizaron en `success`;
el árbol fusionado es idéntico. Estas son ejecuciones previas, **no**
resultados atribuidos a la nueva PR A02-02:

| Campaña de CI A02-01 | Run | Estado comprobado |
|---|---:|---|
| F11 nativo Linux/GNU y Windows/MSVC, 13 casos en cada sistema | [43006225597](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225597) | SUCCESS |
| F04 operaciones nativas | [43006225598](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225598) | SUCCESS |
| F04 historia persistente, seis campañas | [43006225602](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225602) | SUCCESS |
| F05/P05A y regresiones Core/F04/F05 Linux/Windows | [43006225647](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225647) | SUCCESS |
| F11 referencia offline | [43006225793](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225793) | SUCCESS |
| Gobernanza F00–F15 | [43006225630](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225630) | SUCCESS |
| F14 referencia no jugable | [43006225784](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43006225784) | SUCCESS |

Documentación de reauditoría: [REAUDIT.md](../../../../../../desarrollo/integration/f11/REAUDIT.md);
evidencia estructurada de plataformas:
[`CI_EVIDENCE.json`](../../../../../../desarrollo/integration/f11/CI_EVIDENCE.json).

## 3. Matriz de garantías (qué se observa realmente)

| Puerta | Garantía exigida | Evidencia ejecutable |
|---|---|---|
| G1 — Autoridad | Solo comisión válida, concesión de Personal de Flota y orden institucional autorizan el ascenso; revocaciones de concesión y orden en ticks 0, 1 y 99 deniegan en el mismo tick | `f11.authority`, `f11.negatives` |
| G2 — Expediente | Un evento `promotion` con `promotion_event_id` Core estable, orden, causa, comisión, evaluación, identidad, grado anterior/nuevo y `effective_at` | `f11.promotion`, `f11.identity` |
| G3 — Atomicidad | Grado y expediente cambian juntos; cinco puntos de fallo simulado no dejan efectos parciales, revisión ni RNG alterados | `f11.atomic`, `f11.corrupt` |
| G4 — Idempotencia | Reintento con la misma key devuelve recibo original sin segundo ascenso; payload distinto = conflicto; revocación posterior no borra hechos legales | `f11.idempotency`, `f11.authority` |
| G5 — Persistencia real | Guardar/cargar en procesos separados, identidad de 128 bits intacta y mismo evento; recuperación tras consolidación segmentada y orden caducada | `f11.process_save`, `f11.process_load`, `f11.history` |
| G6 — Compatibilidad legacy | SCHEMA 1/2 y rangos 0/1/8/10 preservados; ningún personaje legacy asciende por conversión implícita | `f11.legacy`, `f11.abi` |
| G7 — Frontera de producto | El puente de producto funciona con commit/carga/replay y **no exporta** emisor de ensayo, revocación ni fallos de laboratorio | `f11.product_bridge` |
| G8 — Historia congelada | Seis campañas completas, comparación con oráculos previos de pasado íntegro, recuperación y futuro en proceso nuevo; no aceptar falso PASS por CAPACITY | `history_reference_v2.json`, seis campañas F04 histórico, suite de integración F05 |
| G9 — Regresiones transversales | No cambiar la autoridad F05, la plaza, nave, departamento, cualificaciones, turno ni mando por subir de grado | `f11.promotion`, suite nativa F05 y F04 |
| G10 — Procedencia verificable | Ninguna modificación de fuentes de juego, pins, oráculos, acceptance ni evidencias congeladas desde la fusión #106 | `f11_p05_a02_02_certify.py` |

En la reauditoría original de las seis campañas se reconstruyeron **370 bloques**
con **1.948.872 hechos** completos. Se conservaron byte a byte los oráculos
v1, acceptance, procedencia y datos anteriores; el manifiesto v2
solo se aprobó después de reejecutar las seis campañas. El guard rechaza
alteraciones no autorizadas, incluso informes alterados y rehasheados.

**Distinción esencial:** el evento legal `effective_at` está persistido;
la ceremonia o comunicación diferida `presented_at` **NO** está implementada.
Su cola/acuse pertenece a **F11-P05-C**, las escenas a **P05-D** y el E2E
jugable a **P05-E**, conforme a la [issue #104](https://github.com/robdor80/Videojuego_StarTrek/issues/104).

## 4. Nueva certificación A02-02: procedimiento de CI

El workflow [`f11-a02-02-certification.yml`](../../../../../../.github/workflows/f11-a02-02-certification.yml)
incluye puertas independientes:

1. Guard no mutador de integridad de código y las seis referencias históricas,
   340 pruebas F11 de referencia y gobernanza de roadmap.
2. Compilación real F11 GNU y MSVC, **13/13** casos distintos, sin SKIP.
3. Compilación/regresiones F04 estable y F05, Linux y Windows, sin omitir
   resultados fallidos ni reutilizar directorios de salida.
4. **Seis** campañas históricas con el pin independiente 89a0… en Linux y
   Windows, guardado segmentado, comparación de oráculos y recuperación.

Los builds, guardados de pruebas, JUnit y logs se conservan como artefactos
temporales de GitHub Actions dentro de `laboratorios/`, no como dependencias
del código ni archivos de producción. La CI solo se considera acreditada si
todos los jobs obligatorios finalizan en `success`; los casos `SKIP` de
plataforma se informan y **no cuentan como PASS**.

Ejecutar el guard de procedencia desde la raíz del repositorio:

```sh
python desarrollo/tools/validation/f11_p05_a02_02_certify.py
```

Este script **no** ejecuta Core y no debe presentarse como sustituto del CTest.
Certifica exclusivamente que se está probando el mismo código auditado y que
las pruebas históricas originales y sus dependencias no han sido sustituidas.

## 5. Exclusiones que no pueden maquillarse como «certificadas»

- Emisión institucional real en el **Host de producto**: todavía no cableada;
  el emisor usado para las pruebas vive únicamente en una biblioteca nativa
  privada de ensayo.
- Traslado y coordinación de identidad entre distintas naves: pendiente P05-B3.
- Presentaciones pendientes, notificaciones y ceremonias: pendientes P05-C/D.
- UE5.8.2, NullRHI/D3D12 e interacción manual en el MSI: **NO EJECUTADOS**.
- Otros rangos, puestos, ofertas de destino, acceso a la Enterprise-D:
  **NO** cubiertos por este certificado.

**Criterio de cierre de A02-02:** matriz G1–G10 respaldada por prueba real
y nueva CI completa en verde. Si falla cualquier plataforma o campaña, dejar
el paso **ABIERTO** y conservar logs; nunca modificar los oráculos para
disimular una divergencia. Mantener F11 global **PLANIFICADA**, sin tocar
`ESTADO_GLOBAL.json` ni fusionar esta PR por el mero hecho de existir.
