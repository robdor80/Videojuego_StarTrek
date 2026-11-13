# LORE-05D — Naves, instalaciones y organizaciones

**13 de noviembre de 2026.** Desarrollo documental para la continuidad propia TNG/DS9/VOY (inicio Academia 2383). No supone runtime ni amplía el canon.

## Inventario entregado
- [Catálogo de 8 naves individuales, 12 instalaciones, 8 facciones y 2 instituciones federativas](../../../../mundo/lore/operations/lore05d_entities_v0.1.json).
- [Guía narrativa y límites de identidad, mando, jurisdicción y cronología](../../../../mundo/lore/operations/LORE05D_NAVES_INSTALACIONES_ORGANIZACIONES_20261113.md).
- [18 casos de aceptación narrativa](../../../../mundo/lore/operations/lore05d_validation_cases_v0.1.json).
- `desarrollo/tools/validation/validate_lore05_d.py`, `test_lore05_d.py`, CI `.github/workflows/lore05-d-documentary.yml`.

## Límites no negociables
- `NCC-1701-D` = nave individual Galaxy, reconstruida por Proyecto Valhalla sin renombrarla ni convertirla en clase nueva. Objetivo 2387 no garantizado.
- Defiant `NX-74205` fue destruida en 2375; la posterior São Paulo rebautizada Defiant es otro casco, no se le asigna aquí ship_id porque aún no tiene registro individual.
- Odyssey y Sovereign son clases, NO individuos nacidos automáticamente. Las naves históricas (Pike, Kirk, etc.) no se ponen en servicio en 2383.
- En las instalaciones, `tipo != diseño != unidad != propietario != operador != personal actual`. No se copian nombres únicos, inventarios ni dotaciones.
- Gobierno civil de Federación, Flota Estelar, autoridad local, departamentos, ciudadanía y afiliación personal no se confunden.
- Las escenas propuestas no son misiones activas; ni CoreRPG, ni F11, ni HOST, ni UE5 ni PADD se modifican. DLC Delta permanece bloqueado.

## Fuentes de verdad
Catálogos preexistentes de naves y clases, estaciones e instalaciones, ocho facciones y perfiles de organización, decisiones DEC-0020, LORE-05B, LORE-05C. El JSON de 05D los referencia, no los sustituye.

## Cierre
Validar IDs cruzados, 18 casos, prohibiciones por cronología, fronteras Core/HOST y pruebas adversariales. Ejecutar CI del último HEAD y someter PR a fusión. El resultado será **COMPLETE_DOCUMENTARY**, nunca certificación runtime.
