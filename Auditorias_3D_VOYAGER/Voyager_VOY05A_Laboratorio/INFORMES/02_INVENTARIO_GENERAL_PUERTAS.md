# VOY-05A — Inventario general

**187 registros de interfaces/cierres de catálogo**, no 187 mecanismos. Se separan 23 cierres representados de las bocas abiertas. Se contabilizan ambos extremos de un tramo o eje porque tienen posiciones y normales distintas; `shaft_pair` vincula los dos extremos de cada eje vertical. La tapa Mesh54 se cuenta una sola vez, evitando sumar su perímetro como un segundo hueco.

Los identificadores `AC_MeshN_XX` derivan del borde fuente `L_MeshN_XX`; `PT_MeshN_XX` identifica los cierres confirmados visualmente; BR_01/02/03 enlazan D_IZQ/D_DER/D_POST; BR_04 corresponde al acceso de cabina. Son estables para esta versión, vinculados a los hashes fuente. No se deben renumerar al separar geometría posteriormente.

El JSON incluye archivo, escena, colecciones, nombres de malla, transformaciones completas por objeto, coordenadas de perfil, normal, tangente, cotas, medidas, escala, materiales, UV, grado, obstáculos y capturas. Los grupos móviles del puente se enumeran íntegros. Una fila sin medidas libres conserva envolvente frontal y explica el método. `null` significa E/no determinado, nunca cero. El CSV replica los mismos campos; las listas y matrices se serializan como JSON dentro de la celda.

| ID | Contexto/objeto | Clase | Dimensión m | Grado | Evidencia |
| --- | --- | --- | --- | --- | --- |
| AC_Mesh1_00 | Mesh1 | hueco_o_boca | 2.2210 × 2.6701 | B | [imagen](../CAPTURAS/AC_Mesh1_00.png) |
| AC_Mesh10_00 | Mesh10 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh10_00.png) |
| AC_Mesh10_01 | Mesh10 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh10_01.png) |
| AC_Mesh103_01 | Mesh103 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh103_01.png) |
| AC_Mesh103_02 | Mesh103 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh103_02.png) |
| AC_Mesh103_05 | Mesh103 | abertura_estructural_funcion_no_confirmada | 1.8395 × 2.3591 | E | [imagen](../CAPTURAS/AC_Mesh103_05.png) |
| AC_Mesh11_03 | Mesh11 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh11_03.png) |
| AC_Mesh11_04 | Mesh11 | hueco_o_boca | 1.1820 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh11_04.png) |
| AC_Mesh12_00 | Mesh12 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh12_00.png) |
| AC_Mesh12_01 | Mesh12 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh12_01.png) |
| AC_Mesh13_00 | Mesh13 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh13_00.png) |
| AC_Mesh13_01 | Mesh13 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh13_01.png) |
| AC_Mesh14_00 | Mesh14 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh14_00.png) |
| AC_Mesh14_01 | Mesh14 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh14_01.png) |
| AC_Mesh15_00 | Mesh15 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh15_00.png) |
| AC_Mesh15_01 | Mesh15 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh15_01.png) |
| AC_Mesh16_00 | Mesh16 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh16_00.png) |
| AC_Mesh16_03 | Mesh16 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh16_03.png) |
| AC_Mesh16_04 | Mesh16 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh16_04.png) |
| AC_Mesh17_00 | Mesh17 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh17_00.png) |
| AC_Mesh18_00 | Mesh18 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh18_00.png) |
| AC_Mesh18_01 | Mesh18 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh18_01.png) |
| AC_Mesh19_00 | Mesh19 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh19_00.png) |
| AC_Mesh19_02 | Mesh19 | conducto_bajo_o_escotilla | 0.8770 × 0.7681 | B | [imagen](../CAPTURAS/AC_Mesh19_02.png) |
| AC_Mesh2_00 | Mesh2 | hueco_o_boca | 2.9614 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh2_00.png) |
| AC_Mesh2_01 | Mesh2 | hueco_o_boca | 2.9614 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh2_01.png) |
| AC_Mesh2_07 | Mesh2 | hueco_o_boca | 2.9613 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh2_07.png) |
| AC_Mesh20_00 | Mesh20 | conducto_bajo_o_escotilla | 1.1696 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh20_00.png) |
| AC_Mesh20_07 | Mesh20 | conducto_bajo_o_escotilla | 1.1696 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh20_07.png) |
| AC_Mesh21_00 | Mesh21 | conducto_bajo_o_escotilla | 1.1764 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh21_00.png) |
| AC_Mesh21_07 | Mesh21 | conducto_bajo_o_escotilla | 1.1764 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh21_07.png) |
| AC_Mesh24_00 | Mesh24 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh24_00.png) |
| AC_Mesh24_01 | Mesh24 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh24_01.png) |
| AC_Mesh25_00 | Mesh25 | hueco_o_boca | 2.9705 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh25_00.png) |
| AC_Mesh25_01 | Mesh25 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh25_01.png) |
| AC_Mesh26_00 | Mesh26 | hueco_o_boca | 2.9705 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh26_00.png) |
| AC_Mesh26_01 | Mesh26 | hueco_o_boca | 2.9705 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh26_01.png) |
| AC_Mesh27_00 | Mesh27 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh27_00.png) |
| AC_Mesh28_01 | Mesh28 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh28_01.png) |
| AC_Mesh28_02 | Mesh28 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh28_02.png) |
| AC_Mesh29_00 | Mesh29 | conducto_bajo_o_escotilla | 0.9867 × 0.8778 | B | [imagen](../CAPTURAS/AC_Mesh29_00.png) |
| AC_Mesh29_02 | Mesh29 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh29_02.png) |
| AC_Mesh29_03 | Mesh29 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh29_03.png) |
| AC_Mesh3_00 | Mesh3 | hueco_o_boca | 2.2210 × 2.6701 | B | [imagen](../CAPTURAS/AC_Mesh3_00.png) |
| AC_Mesh35_00 | Mesh35 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh35_00.png) |
| AC_Mesh37_00 | Mesh37 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh37_00.png) |
| AC_Mesh37_01 | Mesh37 | hueco_o_boca | 1.0341 × 2.1935 | B | [imagen](../CAPTURAS/AC_Mesh37_01.png) |
| AC_Mesh38_00 | Mesh38 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh38_00.png) |
| AC_Mesh38_03 | Mesh38 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh38_03.png) |
| AC_Mesh38_04 | Mesh38 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh38_04.png) |
| AC_Mesh38_09 | Mesh38 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh38_09.png) |
| AC_Mesh39_00 | Mesh39 | conducto_bajo_o_escotilla | 1.1764 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh39_00.png) |
| AC_Mesh39_01 | Mesh39 | conducto_bajo_o_escotilla | 1.1764 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh39_01.png) |
| AC_Mesh4_00 | Mesh4 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh4_00.png) |
| AC_Mesh40_00 | Mesh40 | hueco_o_boca | 2.9613 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh40_00.png) |
| AC_Mesh40_01 | Mesh40 | hueco_o_boca | 2.9613 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh40_01.png) |
| AC_Mesh40_04 | Mesh40 | hueco_o_boca | 2.9613 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh40_04.png) |
| AC_Mesh41_00 | Mesh41 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh41_00.png) |
| AC_Mesh41_03 | Mesh41 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh41_03.png) |
| AC_Mesh42_00 | Mesh42 | hueco_o_boca | 2.0666 × 2.5969 | B | [imagen](../CAPTURAS/AC_Mesh42_00.png) |
| AC_Mesh42_01 | Mesh42 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh42_01.png) |
| AC_Mesh45_00 | Mesh45 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh45_00.png) |
| AC_Mesh45_01 | Mesh45 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh45_01.png) |
| AC_Mesh5_00 | Mesh5 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh5_00.png) |
| AC_Mesh50_00 | Mesh50 | hueco_o_boca | 2.0483 × 2.5969 | B | [imagen](../CAPTURAS/AC_Mesh50_00.png) |
| AC_Mesh51_00 | Mesh51 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh51_00.png) |
| AC_Mesh52_00 | Mesh52 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh52_00.png) |
| AC_Mesh52_06 | Mesh52 | hueco_o_boca | 2.2210 × 2.6701 | B | [imagen](../CAPTURAS/AC_Mesh52_06.png) |
| AC_Mesh52_09 | Mesh52 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh52_09.png) |
| AC_Mesh54_00 | Mesh54 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh54_00.png) |
| AC_Mesh54_01 | Mesh54 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh54_01.png) |
| AC_Mesh56_00 | Mesh56 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh56_00.png) |
| AC_Mesh56_01 | Mesh56 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh56_01.png) |
| AC_Mesh56_14 | Mesh56 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh56_14.png) |
| AC_Mesh57_00 | Mesh57 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh57_00.png) |
| AC_Mesh57_01 | Mesh57 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh57_01.png) |
| AC_Mesh58_00 | Mesh58 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh58_00.png) |
| AC_Mesh58_01 | Mesh58 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh58_01.png) |
| AC_Mesh59_00 | Mesh59 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh59_00.png) |
| AC_Mesh59_01 | Mesh59 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh59_01.png) |
| AC_Mesh59_02 | Mesh59 | hueco_o_boca | 2.0483 × 2.5969 | B | [imagen](../CAPTURAS/AC_Mesh59_02.png) |
| AC_Mesh6_00 | Mesh6 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh6_00.png) |
| AC_Mesh62_00 | Mesh62 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh62_00.png) |
| AC_Mesh62_01 | Mesh62 | hueco_o_boca | 2.9712 × 2.8164 | C | [imagen](../CAPTURAS/AC_Mesh62_01.png) |
| AC_Mesh63_00 | Mesh63 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh63_00.png) |
| AC_Mesh63_01 | Mesh63 | conducto_bajo_o_escotilla | 1.1751 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh63_01.png) |
| AC_Mesh64_00 | Mesh64 | hueco_o_boca | 2.9614 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh64_00.png) |
| AC_Mesh64_01 | Mesh64 | conducto_bajo_o_escotilla | 1.2671 × 1.1018 | B | [imagen](../CAPTURAS/AC_Mesh64_01.png) |
| AC_Mesh64_02 | Mesh64 | conducto_bajo_o_escotilla | 1.2671 × 1.1018 | B | [imagen](../CAPTURAS/AC_Mesh64_02.png) |
| AC_Mesh65_00 | Mesh65 | hueco_o_boca | 1.3231 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh65_00.png) |
| AC_Mesh65_03 | Mesh65 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh65_03.png) |
| AC_Mesh66_00 | Mesh66 | conducto_bajo_o_escotilla | 1.1708 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh66_00.png) |
| AC_Mesh66_03 | Mesh66 | conducto_bajo_o_escotilla | 1.1708 × 0.9144 | B | [imagen](../CAPTURAS/AC_Mesh66_03.png) |
| AC_Mesh67_02 | Mesh67 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh67_02.png) |
| AC_Mesh68_00 | Mesh68 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh68_00.png) |
| AC_Mesh69_00 | Mesh69 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh69_00.png) |
| AC_Mesh69_01 | Mesh69 | conducto_bajo_o_escotilla | 1.2671 × 1.1018 | B | [imagen](../CAPTURAS/AC_Mesh69_01.png) |
| AC_Mesh7_00 | Mesh7 | abertura_estructural_funcion_no_confirmada | 1.8395 × 2.3591 | E | [imagen](../CAPTURAS/AC_Mesh7_00.png) |
| AC_Mesh7_01 | Mesh7 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh7_01.png) |
| AC_Mesh7_02 | Mesh7 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh7_02.png) |
| AC_Mesh7_03 | Mesh7 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh7_03.png) |
| AC_Mesh7_04 | Mesh7 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh7_04.png) |
| AC_Mesh70_00 | Mesh70 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh70_00.png) |
| AC_Mesh71_02 | Mesh71 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh71_02.png) |
| AC_Mesh71_03 | Mesh71 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh71_03.png) |
| AC_Mesh72_01 | Mesh72 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh72_01.png) |
| AC_Mesh72_03 | Mesh72 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh72_03.png) |
| AC_Mesh73_02 | Mesh73 | hueco_o_boca | 1.0341 × 2.1935 | B | [imagen](../CAPTURAS/AC_Mesh73_02.png) |
| AC_Mesh74_01 | Mesh74 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh74_01.png) |
| AC_Mesh74_03 | Mesh74 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh74_03.png) |
| AC_Mesh75_01 | Mesh75 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh75_01.png) |
| AC_Mesh75_04 | Mesh75 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh75_04.png) |
| AC_Mesh76_01 | Mesh76 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh76_01.png) |
| AC_Mesh76_06 | Mesh76 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh76_06.png) |
| AC_Mesh77_01 | Mesh77 | hueco_o_boca | 1.3231 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh77_01.png) |
| AC_Mesh77_04 | Mesh77 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh77_04.png) |
| AC_Mesh78_01 | Mesh78 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh78_01.png) |
| AC_Mesh78_06 | Mesh78 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh78_06.png) |
| AC_Mesh79_00 | Mesh79 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh79_00.png) |
| AC_Mesh80_00 | Mesh80 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh80_00.png) |
| AC_Mesh80_07 | Mesh80 | hueco_o_boca | 2.2210 × 2.6701 | B | [imagen](../CAPTURAS/AC_Mesh80_07.png) |
| AC_Mesh80_14 | Mesh80 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh80_14.png) |
| AC_Mesh81_00 | Mesh81 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh81_00.png) |
| AC_Mesh82_00 | Mesh82 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh82_00.png) |
| AC_Mesh83_02 | Mesh83 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh83_02.png) |
| AC_Mesh84_01 | Mesh84 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh84_01.png) |
| AC_Mesh84_04 | Mesh84 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh84_04.png) |
| AC_Mesh84_06 | Mesh84 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh84_06.png) |
| AC_Mesh9_03 | Mesh9 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh9_03.png) |
| AC_Mesh9_04 | Mesh9 | hueco_o_boca | 1.0798 × 2.2034 | B | [imagen](../CAPTURAS/AC_Mesh9_04.png) |
| AC_Mesh91_00 | Mesh91 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh91_00.png) |
| AC_Mesh91_01 | Mesh91 | conducto_bajo_o_escotilla | 1.2671 × 1.1018 | B | [imagen](../CAPTURAS/AC_Mesh91_01.png) |
| AC_Mesh91_02 | Mesh91 | conducto_bajo_o_escotilla | 1.2671 × 1.1018 | B | [imagen](../CAPTURAS/AC_Mesh91_02.png) |
| AC_Mesh92_00 | Mesh92 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh92_00.png) |
| AC_Mesh92_01 | Mesh92 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh92_01.png) |
| AC_Mesh92_02 | Mesh92 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh92_02.png) |
| AC_Mesh94_00 | Mesh94 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh94_00.png) |
| AC_Mesh94_01 | Mesh94 | hueco_o_boca | 1.0341 × 2.1936 | B | [imagen](../CAPTURAS/AC_Mesh94_01.png) |
| AC_Mesh95_00 | Mesh95 | hueco_o_boca | 2.9613 × 2.8164 | B | [imagen](../CAPTURAS/AC_Mesh95_00.png) |
| AC_Mesh96_02 | Mesh96 | hueco_o_boca | 1.3231 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh96_02.png) |
| AC_Mesh96_03 | Mesh96 | hueco_o_boca | 1.3231 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh96_03.png) |
| AC_Mesh97_02 | Mesh97 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh97_02.png) |
| AC_Mesh97_04 | Mesh97 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh97_04.png) |
| AC_Mesh97_07 | Mesh97 | hueco_o_boca | 1.3232 × 2.3252 | B | [imagen](../CAPTURAS/AC_Mesh97_07.png) |
| AC_Mesh16_01 | Mesh16 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh16_01.png) |
| AC_Mesh16_02 | Mesh16 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh16_02.png) |
| AC_Mesh65_01 | Mesh65 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh65_01.png) |
| AC_Mesh65_02 | Mesh65 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh65_02.png) |
| AC_Mesh67_00 | Mesh67 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh67_00.png) |
| AC_Mesh67_01 | Mesh67 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh67_01.png) |
| AC_Mesh73_00 | Mesh73 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh73_00.png) |
| AC_Mesh73_01 | Mesh73 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh73_01.png) |
| AC_Mesh76_03 | Mesh76 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh76_03.png) |
| AC_Mesh76_04 | Mesh76 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh76_04.png) |
| AC_Mesh78_03 | Mesh78 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh78_03.png) |
| AC_Mesh78_04 | Mesh78 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh78_04.png) |
| AC_Mesh79_01 | Mesh79 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh79_01.png) |
| AC_Mesh79_02 | Mesh79 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh79_02.png) |
| AC_Mesh82_01 | Mesh82 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh82_01.png) |
| AC_Mesh82_02 | Mesh82 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh82_02.png) |
| AC_Mesh83_00 | Mesh83 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh83_00.png) |
| AC_Mesh83_01 | Mesh83 | boca_vertical | 1.3248 × 1.5240 | C | [imagen](../CAPTURAS/AC_Mesh83_01.png) |
| AC_Mesh54_TECHO | Mesh54 | registro_techo_con_tapa | 1.0808 × 1.1702 | C | [imagen](../CAPTURAS/AC_Mesh54_TECHO.png) |
| PT_Mesh14_01 | Mesh14 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh14_01.png) |
| PT_Mesh14_02 | Mesh14 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh14_02.png) |
| PT_Mesh25_01 | Mesh25 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh25_01.png) |
| PT_Mesh26_01 | Mesh26 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh26_01.png) |
| PT_Mesh54_01 | Mesh54 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh54_01.png) |
| PT_Mesh54_02 | Mesh54 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh54_02.png) |
| PT_Mesh51_01 | Mesh51 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh51_01.png) |
| PT_Mesh51_02 | Mesh51 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh51_02.png) |
| PT_Mesh28_01 | Mesh28 | puerta_cerrada | 1.0341 × 2.5237 (frente) | C | [imagen](../CAPTURAS/PT_Mesh28_01.png) |
| PT_Mesh28_02 | Mesh28 | puerta_cerrada | 1.0341 × 2.5237 (frente) | C | [imagen](../CAPTURAS/PT_Mesh28_02.png) |
| PT_Mesh57_01 | Mesh57 | puerta_cerrada | 1.0341 × 2.5237 (frente) | C | [imagen](../CAPTURAS/PT_Mesh57_01.png) |
| PT_Mesh57_02 | Mesh57 | puerta_cerrada | 1.0341 × 2.5237 (frente) | C | [imagen](../CAPTURAS/PT_Mesh57_02.png) |
| PT_Mesh52_01 | Mesh52 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh52_01.png) |
| PT_Mesh52_02 | Mesh52 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh52_02.png) |
| PT_Mesh80_01 | Mesh80 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh80_01.png) |
| PT_Mesh80_02 | Mesh80 | puerta_cerrada | 1.0341 × 2.1935 (frente) | C | [imagen](../CAPTURAS/PT_Mesh80_02.png) |
| PT_Mesh27_01 | Mesh27 | puerta_cerrada | 2.2210 × 2.5263 (frente) | C | [imagen](../CAPTURAS/PT_Mesh27_01.png) |
| PT_Mesh53_01 | Mesh53 | puerta_cerrada | 2.2210 × 2.5263 (frente) | D | [imagen](../CAPTURAS/PT_Mesh53_01.png) |
| PT_Mesh55_01 | Mesh55 | puerta_cerrada | 2.0681 × 2.5249 (frente) | D | [imagen](../CAPTURAS/PT_Mesh55_01.png) |
| PT_Mesh93_01 | Mesh93 | puerta_cerrada | 1.0341 × 2.1935 (frente) | D | [imagen](../CAPTURAS/PT_Mesh93_01.png) |
| BR_01 | D_IZQ | puerta_cerrada | 0.7572 × 1.7756 | C | [imagen](../CAPTURAS/BR_01.png) |
| BR_02 | D_DER | puerta_cerrada | 0.7572 × 1.7756 | C | [imagen](../CAPTURAS/BR_02.png) |
| BR_03 | D_POST | puerta_cerrada | 0.7583 × 1.7756 | C | [imagen](../CAPTURAS/BR_03.png) |
| BR_04 | cabina | acceso_turbolift_sin_hojas | 0.7583 × 1.7756 | E | [imagen](../CAPTURAS/BR_04.png) |

La selección de bordes está en `DATOS/decisiones_bordes.json`; los bordes descartados siguen disponibles en `DATOS/bordes_abiertos.json`. Se excluyeron pequeñas ranuras de luces/controles, ventanas inclinadas y perímetros exteriores de placas. Los 332 rayos cardinales (`puertos_sondeo_actual.json`) producen 74 candidatos centrales; sirven de contraste, no de inventario exhaustivo. Los bordes y la revisión visual añaden entradas desplazadas y diagonales.
