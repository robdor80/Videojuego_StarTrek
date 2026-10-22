# Arquitectura modular y recursos adicionales

La colección es una biblioteca desplegada en el espacio. El nativo BLEND agrupa cada módulo principalmente en una malla con varios materiales; la exportación GLB la divide por material. **317 mallas GLB no significan 317 módulos**: el nativo tiene 83 mallas, ocho de ellas en el grupo del puente. No se contó un `Recessed_*` como una habitación terminada solo por su nombre.

## Familias identificadas

- Rectos `Hallway_Strait_Small1`, `Hallway_Medium_Single1`, `Hallway_Strait_large1`: suelo, paredes/perfiles y techo representados.
- Curvas 90°, cruces T y cuatro vías, variantes circulares de diferentes radios y tramos con una/dos puertas.
- Accesos residenciales simétricos/asimétricos, nichos/control areas, puertas grandes/cargo y marcos laterales independientes.
- `Turbolift1`, accesos cortos/largos de turbolift, accesos Jefferies; la cabina es geometría estática.
- `J_Tube_*`: rectos corto/medio/largo, codo, T, inclinados, hatch y cruces verticales. Son conductos, no pasillos de pie.
- Mantenimiento horizontal/vertical, codos y cruces con diferencias de cota.
- `ConferenceRoom`, `Room___Head___Single_Restroom1`, bloques Group1–Group10 y volúmenes `Hallway_Primary_Secondary_Location_*`: existen formas de estancias/envolventes; mobiliario y calidad interior no se certifican por su etiqueta.

## Compatibilidad medida, no ensamblaje supuesto

Los tres rectos comparten anchura exterior aproximada **3,693 m**, altura exterior **3,114 m** y longitudes **1,316 / 2,195 / 4,389 m**. Un BVH de sus superficies arroja en el centro y a 10/50/90 % de longitud:

| Altura de muestra Z mundo | Anchura entre primeras superficies laterales |
|---|---|
| 0,10 m | 3,5344 m |
| 0,90 m | 3,3168 m |
| 1,70 m | 3,3271 m |
| 2,20 m | 3,1808 m |

El suelo central está en Z≈−0,019549 m y el techo interior en Z≈2,796803 m: altura central aproximada **2,81635 m**. Las muestras coinciden en los tres tramos. Esto apoya su uso conjunto y el carácter humano de la escala interpretada; no demuestra igualdad de todas las juntas/vértices ni paso de cápsula en recodos. No se montaron módulos ni se corrigieron sus posiciones.

`J_Tube_Long1` mide aproximadamente **1,175 × 1,829 × 0,914 m**; una sección horizontal a Z=0,9 m da ~1,002 m entre superficies laterales. Esa altura no permite paso normal de pie. El rayo vertical iniciado a Z=1,7 m cae sobre la cara exterior superior del tubo; se registra como tal, **no como suelo interior**.

Los módulos están separados en XY y algunos en Z; sus pivotes conservan el sistema de catálogo, sin sockets verificados. Longitudes no homogéneas con un grid de 1 m. No hay UV/material de continuidad garantizados, colisiones, navegación, luces ni puertas activas. Los marcos/recesos y conductos pueden reutilizarse, pero conectar el puente detallado con ellos exigirá un módulo adaptador y comparar vanos, cota de suelo y normal de conexión: ambos recursos proceden de familias distintas y no se demostró encaje directo.

## Inventario de módulos por nombre fuente

Dimensiones son envolventes mundo de objeto; no son anchos útiles ni aforo. La tabla incluye bloques secundarios no interpretados exhaustivamente.

| Grupo fuente | Malla | Triángulos | Dimensiones m |
|---|---|---|---|
| Group1 | Mesh1 | 962 | 5.741 × 8.078 × 4.021 |
| Group9 | Mesh10 | 984 | 18.293 × 11.116 × 2.763 |
| Group10 | Mesh11 | 470 | 10.084 × 8.832 × 3.094 |
| Hallway_Strait_Small1 | Mesh12 | 676 | 3.693 × 1.316 × 3.114 |
| Hallway_Strait_large1 | Mesh13 | 1004 | 3.693 × 4.389 × 3.114 |
| Hallway_Medium_Door_Double1 | Mesh14 | 516 | 3.547 × 2.195 × 3.114 |
| J_Tube_Long1 | Mesh15 | 88 | 1.175 × 1.829 × 0.914 |
| G_4_Way_Up_Dn_Lt_Rt_Junction___With_Hallway_access1 | Mesh16 | 2602 | 3.164 × 2.570 × 3.109 |
| Turbolift1 | Mesh17 | 3307 | 3.043 × 3.533 × 3.100 |
| Hallway_Medium_Single1 | Mesh18 | 684 | 3.693 × 2.195 × 3.114 |
| J_Tube_Access_hatch1 | Mesh19 | 249 | 1.175 × 0.219 × 0.914 |
| Group2 | Mesh2 | 1077 | 5.555 × 5.531 × 3.114 |
| J_tube_90__Turn1 | Mesh20 | 130 | 1.218 × 1.218 × 0.914 |
| J_tube_4__Degree_Slant_Long1 | Mesh21 | 82 | 1.892 × 1.970 × 0.914 |
| Hallway_4__Degree_Circlar_Medium1 | Mesh24 | 586 | 3.649 × 3.666 × 3.114 |
| Hallway_Medium_Door_Single1 | Mesh25 | 616 | 3.620 × 2.195 × 3.114 |
| Hallway_Small_DoorSingle1 | Mesh26 | 609 | 3.688 × 1.317 × 3.114 |
| Recessed_Large_Cargo_Type_Door1 | Mesh27 | 318 | 1.665 × 3.181 × 3.077 |
| Hallway_Residential_Quarters_Asymetrical1 | Mesh28 | 510 | 5.509 × 2.195 × 3.114 |
| Hallway_J_tube_Access_Singlec1 | Mesh29 | 518 | 3.620 × 2.195 × 3.114 |
| Group3 | Mesh3 | 342 | 15.255 × 7.925 × 5.725 |
| Corridor___Turbolift_access___Large1 | Mesh37 | 447 | 3.400 × 3.145 × 3.114 |
| Hallway_4_Way_Junction1 | Mesh38 | 764 | 3.641 × 3.641 × 3.114 |
| J_tube_4__Degree_Slant_Short1 | Mesh39 | 76 | 1.192 × 0.421 × 0.914 |
| Group4 | Mesh4 | 64 | 8.628 × 6.676 × 2.763 |
| Hallway_T_Junction1 | Mesh40 | 812 | 3.667 × 3.641 × 3.114 |
| Hallway_90__Degree_Turn1 | Mesh41 | 1001 | 3.667 × 3.667 × 3.114 |
| Corridor___Turbolift_access___Small1 | Mesh42 | 515 | 2.487 × 3.145 × 3.114 |
| Hallway_4__Degree_Circlar_Large1 | Mesh45 | 586 | 5.405 × 3.666 × 3.114 |
| Group5 | Mesh5 | 48 | 4.438 × 5.148 × 3.323 |
| Recessed_Control_Area___Medium1 | Mesh50 | 1462 | 1.592 × 2.268 × 3.077 |
| Recessed_Large___Double_Exits1 | Mesh51 | 976 | 1.499 × 3.327 × 3.077 |
| Hallway_Primary_Secondary_Location___island___EG__Holodeck_1 | Mesh52 | 2701 | 12.864 × 5.529 × 3.114 |
| Recessed_Large_Cargo_Type_Door_Edge1 | Mesh53 | 227 | 2.961 × 0.073 × 3.077 |
| Hallway_Small_Door_Double1 | Mesh54 | 473 | 3.547 × 1.317 × 3.114 |
| Recessed_large_Door_Edge1 | Mesh55 | 93 | 2.961 × 0.073 × 3.078 |
| J_tube_T___Section_Turn1 | Mesh56 | 136 | 1.221 × 1.267 × 0.914 |
| Hallway_Residential_Quarters_Symetrical1 | Mesh57 | 506 | 5.509 × 2.195 × 3.114 |
| J_Tube_Short1 | Mesh58 | 88 | 1.175 × 0.457 × 0.914 |
| T___Section_Hallway___1x2_1 | Mesh59 | 460 | 3.437 × 2.195 × 3.114 |
| Group6 | Mesh6 | 48 | 4.438 × 5.148 × 3.323 |
| Hallway_4__Degree_Circlar_Small1 | Mesh62 | 576 | 1.894 × 3.666 × 3.114 |
| J_Tube_Medium1 | Mesh63 | 88 | 1.175 × 0.914 × 0.914 |
| Recessed_Large___Double_JT_Exit1 | Mesh64 | 1409 | 1.574 × 3.620 × 3.077 |
| Vertical_Maintenance_TSEC_1_1 | Mesh65 | 1834 | 2.511 × 2.554 × 3.123 |
| J_tube_4__Degree_Slant_Medium1 | Mesh66 | 82 | 1.344 × 1.100 × 0.914 |
| G_2_Way_Up_Dn_Junction1 | Mesh67 | 2202 | 2.598 × 2.570 × 3.109 |
| Recessed_Large___No_Exits___Top_Details1 | Mesh68 | 824 | 1.574 × 3.181 × 3.077 |
| Recessed_Large___Single_JT_Exit1 | Mesh69 | 1104 | 1.574 × 3.400 × 3.077 |
| Group7 | Mesh7 | 1024 | 18.573 × 8.000 × 2.763 |
| Recessed_Large___Single_Exit1 | Mesh70 | 888 | 1.499 × 3.254 × 3.077 |
| Maintenance_Straight_Large | Mesh71 | 914 | 2.339 × 5.940 × 2.376 |
| Vertical_Maintenance_TSEC_3_1 | Mesh73 | 1550 | 2.409 × 2.270 × 3.299 |
| maintenance_straight | Mesh74 | 834 | 2.438 × 2.339 × 2.376 |
| Maintenance_90Degree | Mesh75 | 2174 | 3.022 × 3.022 × 2.478 |
| Vertical_Maintenance_Double1 | Mesh76 | 1952 | 2.612 × 2.453 × 2.860 |
| Maintenance_90Degree1 | Mesh77 | 2174 | 3.022 × 3.022 × 2.478 |
| Vertical_Maintenance_Double2 | Mesh78 | 1952 | 2.612 × 2.453 × 2.860 |
| Vertical_Maintenance_TSEC_2_1 | Mesh79 | 1590 | 2.409 × 2.064 × 3.141 |
| Group8 | Mesh8 | 87 | 4.766 × 2.624 × 0.770 |
| Hallway_Primary_Secondary_Location___open___EG__Holodeck_1 | Mesh80 | 2945 | 13.206 × 9.195 × 3.114 |
| Room___Head___Single_Restroom1 | Mesh81 | 64 | 4.959 × 5.247 × 2.816 |
| Vertical_Maintenance_TSEC_2_2 | Mesh82 | 1590 | 2.409 × 2.064 × 3.141 |
| Vertical_Maintenance_TSEC_3_2 | Mesh83 | 1550 | 2.409 × 2.270 × 3.299 |
| Maintenance_T_Section | Mesh84 | 2178 | 3.025 × 2.920 × 2.427 |
| ConferenceRoom | Mesh9 | 380 | 13.698 × 10.408 × 3.094 |
| Recessed_Large___Double_JT_Exit___Controls1 | Mesh91 | 1985 | 1.574 × 3.620 × 3.077 |
| Hallway_T_Junction_Doorway1 | Mesh92 | 635 | 3.639 × 3.641 × 3.114 |
| Recessed_Large_Turbolift_Door_Edge1 | Mesh93 | 93 | 2.961 × 0.073 × 3.077 |
| Corridor___JT_Access___Large1 | Mesh94 | 447 | 3.145 × 3.400 × 3.114 |
| Recessed_Large___No_Exits1 | Mesh95 | 734 | 1.574 × 3.181 × 3.077 |
| maintenance_straight1 | Mesh96 | 834 | 2.339 × 2.438 × 2.376 |
| Maintenance_T_Section1 | Mesh97 | 2178 | 3.025 × 2.920 × 2.427 |

Datos completos, también puente y grupos anónimos: [DATOS/componentes_blend.csv](DATOS/componentes_blend.csv). Rayos, hits/normales y longitudes: [DATOS/deep_blend.json](DATOS/deep_blend.json). Grado global **B** como kit geométrico; acabado final, interacción y ensamblaje todavía pendientes.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
