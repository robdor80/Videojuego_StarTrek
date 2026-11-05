# VOY-05A — Riesgos y reservas

La auditoría técnica queda **con reservas**, no bloqueada para estudiar B. Los recursos están accesibles y existe inventario visual. La entrega remota depende de su verificación independiente. Ningún resultado autoriza comenzar las otras subfases.

| Riesgo/reserva | Evidencia | Consecuencia y siguiente resolución |
| --- | --- | --- |
| Escala física provisional | Puente ≈0,758×1,776 m; 1,10 experimental | Resolver dimensiones objetivo antes de normalizar huecos |
| Cierres fusionados | Conectividad soldada y caras frontales | Definir pertenencia de caras en B; no basta separar materiales |
| Marcos/espesores E | No hay pieza semántica delimitada | Medir sección completa tras definir componentes; no usar bbox de pasillo |
| Cavidades sin certificar | Paredes abiertas y antecedentes VOY-02 | Diseñar alojamiento físico; resolver suelo/dintel y vistas oblicuas |
| Diferencias entre formatos | Contraste de vértices y MAX residual | Trabajar con fuente trazada; no mezclar silenciosamente versiones |
| Y Mesh2 y bordes ramificados | Dos perfiles diagonales no cíclicos | Sanear antes de montar puertas o certificar unión |
| Tres registros E | AC_Mesh7_00, AC_Mesh103_05, BR_04 | Confirmar función o vano mínimo; no asignar puerta final |
| Espacios sin destino | Catálogo de partes, no nave ensamblada | No habilitar tránsito hacia habitaciones supuestas |
| Niveles diferentes | Cotas 0,238/1,110/3,279 m | Definir transformaciones de montaje, suelo y transiciones |
| Exactitud numérica ≠ física | Contornos y rayos discretos | En D verificar barridos, colisión, ocupante y soporte continuo |
| Alcance de repetición limitado | 27 grupos por envolvente; no piezas separadas | Comparar geometría completa/UV una vez definidas las caras en B |

Las categorías de salas describen geometría disponible. No hay evidencia de camarote final aprobado, habitación funcional equipada, puertas animadas o interiores Valhalla creados. Las variantes MAX con geometría residual no se convierten en nuevos accesos sin revisión semántica. El `.max` nativo se conserva sin inspección en su aplicación original; la conversión Blender sí fue enumerada y contrastada.

Las capturas son renders de Blender de los modelos reales, con colores de diagnóstico y en algunos casos recorte frontal/corte desechable. No demuestran PBR, colisión ni tránsito. El texto y las líneas amarillas identifican contornos medidos; no reconstruyen superficies ausentes.
