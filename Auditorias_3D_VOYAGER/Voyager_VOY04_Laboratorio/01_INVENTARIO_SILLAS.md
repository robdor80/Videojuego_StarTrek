# VOY-04 — Inventario funcional de sillas

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Identificación y sistema de coordenadas

La búsqueda cruza familias ChamferBox/Layer/MSB/Object/Box/Armrest con las piezas reales del puente y renders de contexto. Se encontraron tres cojines de estación, sus tres respaldos y los dos grupos de mando; no otra silla independiente. Las cotas se calcularon de nuevo con los vértices transformados de VOY-03, sin trasladar tamaños de Sutherland. Se usó rayo sobre el cojín para la superficie de asiento y sobre triángulos de apoyo identificados, evitando confundir base común, consola y suelo.

En el marco del puente, la proa es aproximadamente −Y y la vertical +Z. Mirando a proa, babor es aproximadamente +X. Así, MANDO_DER (+X histórico) se asocia contextualmente a capitán y MANDO_IZQ (−X) a primer oficial; LATERAL_DER se asocia a ciencia y LATERAL_IZQ a ingeniería. Son inferencias de disposición, no etiquetas semánticas del OBJ. No llamar Operaciones a cualquiera de las sillas por proximidad. [Roddenberry Archive](https://roddenberry.x.io/2371-uss-voyager-ncc-74656/) sitúa Operaciones/Táctica detrás y ciencia/ingeniería en los laterales bajos.

| ID geométrico | Asignación contextual | Piezas | Envolvente local ancho × fondo × alto m | Cojín Z | Suelo de referencia Z | Altura relativa |
| --- | --- | --- | --- | --- | --- | --- |
| NAVEGACION | CONN / navegación | 8 | 0.653 × 0.718 × 1.274 | 0.6299 | 0.0000 | 0.6299 m |
| LATERAL_DER | Ciencia, babor | 31 | 1.079 × 1.050 × 1.267 | 0.9263 | 0.3274 | 0.5989 m |
| LATERAL_IZQ | Ingeniería, estribor | 31 | 1.079 × 1.051 × 1.268 | 0.9263 | 0.3274 | 0.5989 m |
| MANDO_IZQ | Primer oficial, estribor | 11 | 0.724 × 0.727 × 0.885 | 0.9710 | 0.4794 | 0.4915 m |
| MANDO_DER | Capitán, babor | 11 | 0.724 × 0.727 × 0.885 | 0.9710 | 0.4794 | 0.4915 m |

En navegación, Object_75 está a Z≈0 bajo el pedestal; los pies de trabajo pisan Mesh_1728 a Z=0,023326 m. La altura original sobre ese suelo de pies es **0,606564 m**, distinta de 0,629890 m sobre Object_75. En mando, Mesh_2093 sostiene las carcasas a Z=0,865392 m y el suelo de pies está a Z=0,479442 m: no confundir la distancia cojín–base común con altura ergonómica.

Las envolventes incluyen soportes y, en los laterales, ruedas. No equivalen a ancho útil del cojín. Las orientaciones y matrices completas están en `inventario_medidas.json` / `objetos.json`; `orientacion_contraste.json` contrasta el eje heredado con el vector asiento–respaldo medido otra vez.

## Componentes y contactos por silla

### NAVEGACION

Posición de asiento (marco puente, metros): `[0.0032422509975731373, -3.324818770090739, 0.6298899146742544]`. Eje hacia delante: `[0.016400236786563754, -0.9998655070724985, 0.0]`. Apoyo inferior próximo: `Object_75`.

| Objeto | Función geométrica | Dimensiones locales m |
| --- | --- | --- |
| ChamferBox_22 | cojin_asiento | 0.5337 × 0.5337 × 0.0319 |
| Layer__3 | tapizado_respaldo | 0.6330 × 0.0615 × 0.4675 |
| MSB_30191 | pedestal_inferior_sin_guia_acreditada | 0.1057 × 0.1044 × 0.3661 |
| MSB_30192 | soporte_o_remate | 0.0997 × 0.1458 × 0.0302 |
| MSB_30193 | soporte_o_remate | 0.1308 × 0.1542 × 0.2852 |
| MSB_30194 | vástago_superior | 0.0967 × 0.0955 × 0.2115 |
| Object_76 | carcasa_respaldo | 0.6529 × 0.0794 × 0.4740 |
| Object_77 | carcasa_asiento | 0.5298 × 0.5298 × 0.0458 |

Hay 7 parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: `ChamferBox_22` / `MSB_30192`, `ChamferBox_22` / `Object_77`, `MSB_30191` / `MSB_30194`, `MSB_30192` / `MSB_30193`, `MSB_30192` / `Object_77`. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.

### LATERAL_DER

Posición de asiento (marco puente, metros): `[5.03149938583374, -3.289867321650187, 0.9262728792808268]`. Eje hacia delante: `[-0.5208034041144602, -0.8536766450259666, 0.0]`. Apoyo inferior próximo: `floorfront_1`.

| Objeto | Función geométrica | Dimensiones locales m |
| --- | --- | --- |
| ChamferBox_37 | cojin_asiento | 0.5337 × 0.5337 × 0.0319 |
| Layer__4 | tapizado_respaldo | 0.6331 × 0.0597 × 0.4675 |
| MSB0030110_MSB_30119 | base_rueda_soporte_inferior_revisar_desglose | 0.0123 × 0.2218 × 0.0373 |
| MSB0030110_MSB_30120 | base_rueda_soporte_inferior_revisar_desglose | 0.2126 × 0.0767 × 0.0373 |
| MSB0030110_MSB_30121 | base_rueda_soporte_inferior_revisar_desglose | 0.1369 × 0.1833 × 0.0373 |
| MSB0030110_MSB_30122 | base_rueda_soporte_inferior_revisar_desglose | 0.2118 × 0.0800 × 0.0373 |
| MSB0030116_MSB_30178 | base_rueda_soporte_inferior_revisar_desglose | 0.1132 × 0.0879 × 0.0504 |
| MSB0030116_MSB_30179 | base_rueda_soporte_inferior_revisar_desglose | 0.0768 × 0.1079 × 0.0504 |
| MSB0030116_MSB_30180 | base_rueda_soporte_inferior_revisar_desglose | 0.0805 × 0.1097 × 0.0504 |
| MSB0030116_MSB_30181 | base_rueda_soporte_inferior_revisar_desglose | 0.1010 × 0.0638 × 0.0504 |
| MSB0030117_MSB_30138 | base_rueda_soporte_inferior_revisar_desglose | 0.1041 × 0.0894 × 0.0884 |
| MSB0030117_MSB_30139 | base_rueda_soporte_inferior_revisar_desglose | 0.0830 × 0.1004 × 0.0884 |
| MSB0030117_MSB_30140 | base_rueda_soporte_inferior_revisar_desglose | 0.0799 × 0.0985 × 0.0884 |
| MSB0030117_MSB_30141 | base_rueda_soporte_inferior_revisar_desglose | 0.0916 × 0.0698 × 0.0884 |
| MSB0030119_MSB_30131 | base_rueda_soporte_inferior_revisar_desglose | 0.0624 × 0.0610 × 0.0494 |
| MSB0030119_MSB_30132 | base_rueda_soporte_inferior_revisar_desglose | 0.0618 × 0.0621 × 0.0494 |
| MSB0030119_MSB_30133 | base_rueda_soporte_inferior_revisar_desglose | 0.0623 × 0.0615 × 0.0494 |
| MSB0030119_MSB_30134 | base_rueda_soporte_inferior_revisar_desglose | 0.0623 × 0.0613 × 0.0494 |
| MSB_30195 | soporte_o_remate | 0.1209 × 0.1193 × 0.1284 |
| MSB_30196 | base_rueda_soporte_inferior_revisar_desglose | 0.1326 × 0.1861 × 0.0373 |
| MSB_30197 | soporte_o_remate | 0.1300 × 0.1536 × 0.2852 |
| MSB_30198 | soporte_o_remate | 0.0959 × 0.1452 × 0.0302 |
| MSB_30199 | soporte_o_remate | 0.1057 × 0.1043 × 0.0680 |
| MSB_30200 | vástago_superior | 0.0967 × 0.0954 × 0.2115 |
| MSB_30201 | base_rueda_soporte_inferior_revisar_desglose | 0.0621 × 0.0619 × 0.0494 |
| MSB_30202 | base_rueda_soporte_inferior_revisar_desglose | 0.1118 × 0.1103 × 0.0151 |
| MSB_30203 | base_rueda_soporte_inferior_revisar_desglose | 0.0770 × 0.0965 × 0.0884 |
| MSB_30204 | base_rueda_soporte_inferior_revisar_desglose | 0.0728 × 0.1063 × 0.0504 |
| MSB_30205 | base_rueda_soporte_inferior_revisar_desglose | 0.9987 × 0.9744 × 0.1082 |
| Object_120 | carcasa_asiento | 0.5299 × 0.5298 × 0.0458 |
| Object_121 | carcasa_respaldo | 0.6529 × 0.0778 × 0.4740 |

Hay 50 parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: `ChamferBox_37` / `MSB_30198`, `ChamferBox_37` / `Object_120`, `MSB0030110_MSB_30119` / `MSB_30202`, `MSB0030110_MSB_30119` / `MSB_30205`, `MSB0030110_MSB_30120` / `MSB_30202`. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.

### LATERAL_IZQ

Posición de asiento (marco puente, metros): `[-4.665246486663818, -3.1446953614552817, 0.9262729403407102]`. Eje hacia delante: `[-0.1871937382998412, -0.9823230142582074, 0.0]`. Apoyo inferior próximo: `floorfront_1`.

| Objeto | Función geométrica | Dimensiones locales m |
| --- | --- | --- |
| ChamferBox_38 | cojin_asiento | 0.5337 × 0.5337 × 0.0319 |
| Layer__5 | tapizado_respaldo | 0.6331 × 0.0606 × 0.4675 |
| MSB0030110_MSB_30123 | base_rueda_soporte_inferior_revisar_desglose | 0.0117 × 0.2218 × 0.0373 |
| MSB0030110_MSB_30124 | base_rueda_soporte_inferior_revisar_desglose | 0.2124 × 0.0772 × 0.0373 |
| MSB0030110_MSB_30125 | base_rueda_soporte_inferior_revisar_desglose | 0.1365 × 0.1836 × 0.0373 |
| MSB0030110_MSB_30126 | base_rueda_soporte_inferior_revisar_desglose | 0.2119 × 0.0795 × 0.0373 |
| MSB0030116_MSB_30182 | base_rueda_soporte_inferior_revisar_desglose | 0.1132 × 0.0877 × 0.0504 |
| MSB0030116_MSB_30183 | base_rueda_soporte_inferior_revisar_desglose | 0.1011 × 0.0641 × 0.0504 |
| MSB0030116_MSB_30184 | base_rueda_soporte_inferior_revisar_desglose | 0.0808 × 0.1098 × 0.0504 |
| MSB0030116_MSB_30185 | base_rueda_soporte_inferior_revisar_desglose | 0.0770 × 0.1081 × 0.0504 |
| MSB0030117_MSB_30142 | base_rueda_soporte_inferior_revisar_desglose | 0.1040 × 0.0893 × 0.0884 |
| MSB0030117_MSB_30143 | base_rueda_soporte_inferior_revisar_desglose | 0.0917 × 0.0700 × 0.0884 |
| MSB0030117_MSB_30144 | base_rueda_soporte_inferior_revisar_desglose | 0.0832 × 0.1005 × 0.0884 |
| MSB0030117_MSB_30145 | base_rueda_soporte_inferior_revisar_desglose | 0.0801 × 0.0986 × 0.0884 |
| MSB0030119_MSB_30135 | base_rueda_soporte_inferior_revisar_desglose | 0.0624 × 0.0609 × 0.0494 |
| MSB0030119_MSB_30136 | base_rueda_soporte_inferior_revisar_desglose | 0.0618 × 0.0622 × 0.0494 |
| MSB0030119_MSB_30137 | base_rueda_soporte_inferior_revisar_desglose | 0.0623 × 0.0613 × 0.0494 |
| MSB0030119_MSB_30138 | base_rueda_soporte_inferior_revisar_desglose | 0.0623 × 0.0615 × 0.0494 |
| MSB_30206 | soporte_o_remate | 0.1209 × 0.1193 × 0.1284 |
| MSB_30207 | base_rueda_soporte_inferior_revisar_desglose | 0.1331 × 0.1858 × 0.0373 |
| MSB_30208 | soporte_o_remate | 0.1303 × 0.1539 × 0.2852 |
| MSB_30209 | soporte_o_remate | 0.0952 × 0.1455 × 0.0302 |
| MSB_30210 | soporte_o_remate | 0.1057 × 0.1044 × 0.0680 |
| MSB_30211 | vástago_superior | 0.0967 × 0.0954 × 0.2115 |
| MSB_30212 | base_rueda_soporte_inferior_revisar_desglose | 0.0621 × 0.0619 × 0.0494 |
| MSB_30213 | base_rueda_soporte_inferior_revisar_desglose | 0.1118 × 0.1104 × 0.0151 |
| MSB_30214 | base_rueda_soporte_inferior_revisar_desglose | 0.0768 × 0.0964 × 0.0884 |
| MSB_30215 | base_rueda_soporte_inferior_revisar_desglose | 0.0725 × 0.1062 × 0.0504 |
| MSB_30216 | base_rueda_soporte_inferior_revisar_desglose | 0.9987 × 0.9752 × 0.1082 |
| Object_122 | carcasa_asiento | 0.5298 × 0.5298 × 0.0458 |
| Object_123 | carcasa_respaldo | 0.6529 × 0.0786 × 0.4740 |

Hay 50 parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: `ChamferBox_38` / `MSB_30209`, `ChamferBox_38` / `Object_122`, `MSB0030110_MSB_30123` / `MSB_30213`, `MSB0030110_MSB_30123` / `MSB_30216`, `MSB0030110_MSB_30124` / `MSB_30213`. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.

### MANDO_IZQ

Posición de asiento (marco puente, metros): `[-0.6862014532089233, 0.8245790600776672, 0.9709765515950378]`. Eje hacia delante: `[0.10291520291979947, -0.9946901331610646, 0.0]`. Apoyo inferior próximo: `Mesh_2093`.

| Objeto | Función geométrica | Dimensiones locales m |
| --- | --- | --- |
| Box_6 | carcasa_mando | 0.6938 × 0.7012 × 0.6338 |
| Box_7 | carcasa_mando | 0.5945 × 0.1963 × 0.2800 |
| Armrest_5 | reposabrazos_existente | 0.1304 × 0.4183 × 0.0533 |
| Armrest_6 | reposabrazos_existente | 0.1304 × 0.4183 × 0.0533 |
| ChamferBox_23 | cojin_respaldo | 0.4909 × 0.1173 × 0.1942 |
| ChamferBox_24 | cojin_respaldo | 0.5289 × 0.1328 × 0.2094 |
| ChamferBox_25 | cojin_respaldo | 0.5289 × 0.1335 × 0.2093 |
| ChamferBox_26 | cojin_respaldo | 0.5289 × 0.1264 × 0.2106 |
| ChamferBox_27 | cojin_asiento | 0.5288 × 0.2298 × 0.1067 |
| ChamferBox_28 | cojin_asiento | 0.5288 × 0.2302 × 0.1038 |
| ChamferBox_29 | cojin_asiento | 0.5288 × 0.2299 × 0.1063 |

Hay 18 parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: `Box_6` / `Box_7`, `Box_6` / `Armrest_5`, `Box_6` / `Armrest_6`, `Box_6` / `ChamferBox_23`, `Box_6` / `ChamferBox_24`. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.

### MANDO_DER

Posición de asiento (marco puente, metros): `[0.6968362331390381, 0.8245790600776672, 0.9709765369636645]`. Eje hacia delante: `[-0.10291523398899738, -0.9946901299465025, 0.0]`. Apoyo inferior próximo: `Mesh_2093`.

| Objeto | Función geométrica | Dimensiones locales m |
| --- | --- | --- |
| Box_8 | carcasa_mando | 0.6938 × 0.7012 × 0.6338 |
| Box_9 | carcasa_mando | 0.5945 × 0.1963 × 0.2800 |
| Armrest_7 | reposabrazos_existente | 0.1304 × 0.4183 × 0.0533 |
| Armrest_8 | reposabrazos_existente | 0.1304 × 0.4183 × 0.0533 |
| ChamferBox_30 | cojin_respaldo | 0.4909 × 0.1173 × 0.1942 |
| ChamferBox_31 | cojin_respaldo | 0.5289 × 0.1328 × 0.2094 |
| ChamferBox_32 | cojin_respaldo | 0.5289 × 0.1335 × 0.2093 |
| ChamferBox_33 | cojin_respaldo | 0.5289 × 0.1264 × 0.2106 |
| ChamferBox_34 | cojin_asiento | 0.5288 × 0.2298 × 0.1067 |
| ChamferBox_35 | cojin_asiento | 0.5288 × 0.2302 × 0.1038 |
| ChamferBox_36 | cojin_asiento | 0.5288 × 0.2299 × 0.1063 |

Hay 18 parejas de objetos con contactos/cruces de superficies en el estado original. Ejemplos: `Box_8` / `Box_9`, `Box_8` / `Armrest_7`, `Box_8` / `Armrest_8`, `Box_8` / `ChamferBox_30`, `Box_8` / `ChamferBox_31`. El detalle y los cruces transversales están en `contactos_internos_originales.json`; no se convierten estos contactos internos en articulaciones acreditadas.

## Interpretación funcional

Las tres sillas de estación no tienen reposabrazos independientes. Sus cojines y carcasas son piezas distintas, con espesor superficial y contactos de tapizado; separar esas capas no autoriza moverlas entre sí. Las laterales tienen cinco radios y conjuntos de ruedas, vástagos y remates: su apariencia permite proponer rodadura/giro, pero no acredita ejes/rodamientos ni recorrido despejado. Los 31 componentes no equivalen a 31 mecanismos.

Los sillones de mando tienen dos reposabrazos por silla, cojines segmentados y carcasa; no se localizaron bisagras funcionales de reposabrazos. La base Mesh_2093 es común y fija. Mover el sillón rígidamente sin estudiar esa base puede dejarlo flotante o provocar cruces. Las superficies abiertas, capas coincidentes y contactos cojinera/carcasa se conservan, con diagnóstico en `topologia.json`.

Las distancias a pantallas vecinas se conservan para todos los asientos en `near_screens` del inventario. Un centro vecino no demuestra alcance humano; solo el piloto recibe poses articuladas completas. Las capturas A muestran el contexto seleccionado y las versiones aisladas, no un despiece mecánico ya validado.
