# Archivos previos a F04-MIRANDA-01

Hex textual de los bytes originales generados por la DLL local de PR #66
(`C:/F04-scalable/native/Release/TrekF04Bridge.dll`), antes de esta ampliación.
No se generan con el serializador nuevo durante el test de compatibilidad.

DLL SHA-256: `c5a18b6b4ea4616387f7f080d8d44909441fffbd5bff3ce5e40d40312b5a5626`.
Core fijado: `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.

| Archivo | Productor | Bytes decodificados | SHA-256 de bytes decodificados |
|---|---|---:|---|
| schema1.hex | f04_create(1,"miranda") | 3975 | 0e14da324d28ab54fbca85d4f435535d6d03ef428346c494e9f176c0ef973406 |
| schema2.hex | f04_create_population(1,"miranda",{65001,404,3,0,0,0}) | 1350 | 171c55859b6e2d4763caa0a7be3ac5707f9f0c1a6a9bd715bf0d20442957874a |

`f04.organization_legacy` decodifica, carga y vuelve a guardar exactamente los
mismos bytes. También instala explícitamente la organización sobre el esquema 2,
creando 130 plazas vacantes y conservando sus tres personas.
