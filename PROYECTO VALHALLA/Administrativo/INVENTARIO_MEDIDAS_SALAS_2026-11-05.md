# Inventario de dimensiones de salas — Proyecto Valhalla

Fecha de medición: 2026-11-05. Herramienta: Blender 5.2.2 LTS.

Documento permanente de consulta para estudio y planificación, incluido el análisis por ChatGPT. Resume 27 archivos o variantes localizados en `PROYECTO VALHALLA/`. Las medidas se obtuvieron de copias aisladas; los originales no se modificaron. Los modelos binarios son recursos locales y pueden no estar disponibles en GitHub.

## Criterios para estudiar este inventario

- Usar las medidas como referencia de ocupación exterior aproximada, conservando las advertencias de cada archivo.
- No interpretar la superficie rectangular como área útil ni el volumen de envolvente como volumen habitable.
- No sumar variantes de una misma sala ni módulos de computadora como recintos independientes.
- No asumir que los nombres FINAL, V04 o V07 certifican por sí solos cuál es la versión aprobada para integración.
- Antes de distribuir salas en cubiertas, confirmar escala, orientación, geometría activa, accesos, altura libre y márgenes para estructura e instalaciones.
- Este inventario no certifica puertas, recorridos, colisiones ni el resultado importado en Unreal.

## Cómo interpretar las cifras

- Dimensiones exteriores de la caja alineada con los ejes del modelo: planta × planta × altura. No es el área útil ni el volumen interior; se incluyen paredes, equipamiento, líneas y geometría oculta. Una orientación diagonal puede aumentar esta reserva rectangular.
- Originales: vértices con transformaciones mundiales y evaluación de modificadores. Versiones de supercomputadora posteriores: mallas base de los objetos del archivo (incluidos posibles objetos no enlazados a la escena) y jerarquía de transformaciones, sin evaluar modificadores, animación ni instancias de colección; no certifican la envolvente máxima animada. Fotograma guardado.
- Originales medidos con configuración métrica y scale_length=1. Puente en IMPERIAL y scale_length=1 (coordenadas internas convertidas a metros); Voyager sin unidades, excluido de cualquier conclusión de ocupación real. En la lectura de bibliotecas adicionales se aplica 1 unidad=1 m, coherente con la exportación documentada de la supercomputadora (100 cm por unidad); queda por verificar individualmente esa configuración y los ejes de los modelos adicionales.
- Y vertical en las conversiones originales, comprobado con puertas de holocubierta de 2,41 m y figuras humanas de 1,75–2,01 m. 9-Forward y preparación de control de hangar también usan Y. En los otros archivos se infiere Z; revisar esa inferencia antes de integrar.
- Voyager contiene escalas incompatibles: ver observación individual. No se añade margen para pasillos exteriores, estructura de nave, instalaciones ni mantenimiento. Las alturas no determinan por sí solas el número de cubiertas.
- Las versiones y módulos no se suman: varias representan el mismo recinto. SKP sin conversión separada y recursos Unreal no se han medido directamente. El GLB de laboratorio y transporte se llama nx_class_starship_corridor: es un corredor, no acredita un laboratorio completo.

## Inventario medido (Voyager en unidades sin escala, no metros)

| Modelo | Planta (m) | Altura (m) | Reserva (m²) | Envolvente (m³) | Estado |
|---|---:|---:|---:|---:|---|
| enfermeria D | 24.64 × 38.70 | 3.04 | 953.4 | 2902.4 | Envolvente medida |
| Centro Tactico de Control | 5.71 × 11.69 | 3.95 | 66.8 | 263.7 | Envolvente medida |
| Centro Control Hangar Princiapl Galaxy D | 1124.63 × 701.35 | 6.17 | 788753.8 | 4867271.7 | Revisar geometría |
| Holodeck Galaxy | 6.08 × 10.76 | 4.90 | 65.4 | 320.8 | Envolvente medida |
| sala de transporte | 21.28 × 10.10 | 3.13 | 215.0 | 671.9 | Envolvente medida |
| sala de cartografia | 30.25 × 17.56 | 7.00 | 531.1 | 3717.0 | Envolvente medida |
| Reactor WARP D | 17.96 × 23.82 | 7.91 | 427.8 | 3383.7 | Envolvente medida |
| sala ingenieria galaxy d | 29.36 × 25.42 | 8.77 | 746.2 | 6546.2 | Envolvente medida |
| Sala nucleo Computadora Enterprise D | 53.50 × 37.57 | 9.29 | 2009.8 | 18667.6 | Envolvente medida |
| sala observacion | 26.04 × 11.41 | 3.93 | 297.1 | 1168.2 | Envolvente medida |
| Computadora_Circulo_Ajustado_V02 | 19.56 × 19.51 | 3.32 | 381.6 | 1265.4 | Envolvente medida |
| Computadora_Circulo_Completo_V01 | 19.56 × 19.51 | 3.32 | 381.6 | 1265.4 | Envolvente medida |
| Sala computadora completa (con circulos vacios) | 53.50 × 37.57 | 9.29 | 2009.8 | 18667.6 | Envolvente medida |
| Sala_computadora_Materiales_Recuperados | 53.50 × 37.57 | 9.29 | 2009.8 | 18667.6 | Envolvente medida |
| Sala_Supercomputadora_Enterprise_G_FINAL | 53.50 × 53.09 | 37.57 | 2839.9 | 106693.7 | Revisar geometría |
| Sala_Supercomputadora_V07_Funcional | 47.39 × 54.65 | 9.34 | 2589.9 | 24198.8 | Envolvente medida |
| Sala_Supercomputadora_Valhalla_Geometria_V04 | 53.50 × 53.09 | 37.57 | 2839.9 | 106693.7 | Revisar geometría |
| Sala_Supercomputadora_Valhalla_Geometria_V04E | 53.50 × 53.09 | 37.57 | 2839.9 | 106693.7 | Revisar geometría |
| Sala_Supercomputadora_Valhalla_Integrada_V03 | 53.50 × 53.09 | 37.57 | 2839.9 | 106693.7 | Revisar geometría |
| Sala_Supercomputadora_Valhalla_Puertas_V04B | 53.50 × 53.09 | 37.57 | 2839.9 | 106693.7 | Revisar geometría |
| Semicirculo_computadora | 57.76 × 39.50 | 3.71 | 2281.5 | 8456.9 | Envolvente medida |
| Semicirculo_computadora_Materiales_Recuperados | 57.76 × 39.50 | 3.71 | 2281.5 | 8456.9 | Envolvente medida |
| Galaxy Bridge - release | 20.83 × 17.66 | 5.54 | 367.9 | 2038.0 | Envolvente medida |
| PROTOTIPO 9-FORWARD LIMPIO | 37.65 × 46.71 | 7.43 | 1758.8 | 13072.7 | Envolvente medida |
| VALHALLA_Sala_Control_Hangar_PREPARACION | 1124.63 × 701.35 | 6.17 | 788753.8 | 4867271.7 | Revisar geometría |
| VALHALLA_HANGAR_Contorno_132x210 | 140.81 × 210.00 | 25.00 | 29570.1 | 739252.2 | Envolvente medida |

### Holocubierta Voyager: registro sin escala validada

| Archivo | Planta (u) | Altura (u) | Rectángulo (u²) | Envolvente (u³) |
|---|---:|---:|---:|---:|
| Holodeck_R1.blend | 58.20 × 157.80 | 53.69 | 9184.0 | 493103.3 |

`u` significa unidad del archivo, no metro. La configuración no declara unidades físicas. No utilizar estos valores para reservar espacio real.

## Procedencia y observaciones

### enfermeria D
`Modelos 3D\Salas originales\enfermeria D.blend`
Vertical: Y. Envolvente de toda la geometría.

### Centro Tactico de Control
`Modelos 3D\Salas originales\Centro Tactico de Control\Centro Tactico de Control.blend`
Vertical: Y. Envolvente de toda la geometría.

### Centro Control Hangar Princiapl Galaxy D
`Modelos 3D\Salas originales\hangares\Centro Control Hangar Princiapl Galaxy D.blend`
Vertical: Y. NO usar para dimensionar la sala: Group#4 aporta geometría de 907 × 701 m y está alejado del recinto. Si se excluye solo ese objeto del cálculo, el resto da 61,30 × 47,83 × 6,17 m (provisional, sin depurar otros elementos). No se ha eliminado geometría.

### Holodeck Galaxy
`Modelos 3D\Salas originales\holodeck\Holodeck Galaxy.blend`
Vertical: Y. Envolvente de toda la geometría.

### sala de transporte
`Modelos 3D\Salas originales\laboratorio y transportacion\sala de transporte.blend`
Vertical: Y. Envolvente de toda la geometría.

### sala de cartografia
`Modelos 3D\Salas originales\sala de cartografia\sala de cartografia.blend`
Vertical: Y. Envolvente de toda la geometría.

### Reactor WARP D
`Modelos 3D\Salas originales\sala del reactor D\Reactor WARP D.blend`
Vertical: Y. Envolvente de toda la geometría.

### sala ingenieria galaxy d
`Modelos 3D\Salas originales\sala ingenieria Galaxy D\sala ingenieria galaxy d.blend`
Vertical: Y. Envolvente de toda la geometría.

### Sala nucleo Computadora Enterprise D
`Modelos 3D\Salas originales\Sala nucleo computadora Enterprise D\Sala nucleo Computadora Enterprise D.blend`
Vertical: Y. Envolvente de toda la geometría.

### sala observacion
`Modelos 3D\Salas originales\sala observacion\sala observacion.blend`
Vertical: Y. Envolvente de toda la geometría.

### Computadora_Circulo_Ajustado_V02
`Salas construidas\Sala computadora Enterprise Valhalla\Computadora_Circulo_Ajustado_V02.blend`
Vertical: Z. Módulo de computadora; no sumar como sala independiente.

### Computadora_Circulo_Completo_V01
`Salas construidas\Sala computadora Enterprise Valhalla\Computadora_Circulo_Completo_V01.blend`
Vertical: Z. Módulo de computadora; no sumar como sala independiente.

### Sala computadora completa (con circulos vacios)
`Salas construidas\Sala computadora Enterprise Valhalla\Sala computadora completa (con circulos vacios).blend`
Vertical: Y. Envolvente de toda la geometría.

### Sala_computadora_Materiales_Recuperados
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_computadora_Materiales_Recuperados.blend`
Vertical: Y. Envolvente de toda la geometría.

### Sala_Supercomputadora_Enterprise_G_FINAL
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_Enterprise_G_FINAL.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal. ALERTA: la envolvente arroja 37,57 m de altura. Se sospecha mezcla de orientaciones o geometría auxiliar; la causa requiere revisión. No representa una altura útil validada.

### Sala_Supercomputadora_V07_Funcional
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_V07_Funcional.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal.

### Sala_Supercomputadora_Valhalla_Geometria_V04
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_Valhalla_Geometria_V04.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal. ALERTA: la envolvente arroja 37,57 m de altura. Se sospecha mezcla de orientaciones o geometría auxiliar; la causa requiere revisión. No representa una altura útil validada.

### Sala_Supercomputadora_Valhalla_Geometria_V04E
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_Valhalla_Geometria_V04E.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal. ALERTA: la envolvente arroja 37,57 m de altura. Se sospecha mezcla de orientaciones o geometría auxiliar; la causa requiere revisión. No representa una altura útil validada.

### Sala_Supercomputadora_Valhalla_Integrada_V03
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_Valhalla_Integrada_V03.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal. ALERTA: la envolvente arroja 37,57 m de altura. Se sospecha mezcla de orientaciones o geometría auxiliar; la causa requiere revisión. No representa una altura útil validada.

### Sala_Supercomputadora_Valhalla_Puertas_V04B
`Salas construidas\Sala computadora Enterprise Valhalla\Sala_Supercomputadora_Valhalla_Puertas_V04B.blend`
Vertical: Z. Envolvente de toda la geometría. Variante alternativa; no sumar entre versiones. Comprobar también la integración Unreal. ALERTA: la envolvente arroja 37,57 m de altura. Se sospecha mezcla de orientaciones o geometría auxiliar; la causa requiere revisión. No representa una altura útil validada.

### Semicirculo_computadora
`Salas construidas\Sala computadora Enterprise Valhalla\Semicirculo_computadora.blend`
Vertical: Y. Módulo de computadora; no sumar como sala independiente.

### Semicirculo_computadora_Materiales_Recuperados
`Salas construidas\Sala computadora Enterprise Valhalla\Semicirculo_computadora_Materiales_Recuperados.blend`
Vertical: Y. Módulo de computadora; no sumar como sala independiente.

### Galaxy Bridge - release
`Modelos 3D\Puente Clase Galaxia completo original\Galaxy Bridge - release.blend`
Vertical: Z. Envolvente de toda la geometría.

### PROTOTIPO 9-FORWARD LIMPIO
`Cubiertas Enterprise G\PROTOTIPO 9-FORWARD LIMPIO.blend`
Vertical: Y. Envolvente de toda la geometría.

### VALHALLA_Sala_Control_Hangar_PREPARACION
`Cubiertas Enterprise G\VALHALLA_Sala_Control_Hangar_PREPARACION.blend`
Vertical: Y. NO usar para dimensionar la sala: Group#4 aporta geometría de 907 × 701 m y está alejado del recinto. Si se excluye solo ese objeto del cálculo, el resto da 61,30 × 47,83 × 6,17 m (provisional, sin depurar otros elementos). No se ha eliminado geometría.

### VALHALLA_HANGAR_Contorno_132x210
`Cubiertas Enterprise G\VALHALLA_HANGAR_Contorno_132x210.blend`
Vertical: Z. Contorno nominal 132 × 210 m; envolvente completa 140,81 × 210 × 25 m por las paredes inclinadas. No es una sala terminada.

### Holodeck_R1
`Modelos 3D/Salas originales/holodeck/Voyager Holodeck.zip` → `Holodeck_R1.blend`
Vertical: Z. ESCALA SIN VALIDAR: unidad NONE, Z vertical, puerta Voyager de 20 m frente a puerta T-CLASS de 2,01 m. Mezcla de escalas y variantes. Cifras en unidades de archivo, no reservar como metros. Las dimensiones incompatibles observadas sugieren distintas escalas o variantes; no se ha establecido una conversión única.


## Alcance y límites de conservación

Este Markdown contiene el resumen numérico y la procedencia necesarios para estudiarlo por sí mismo. No depende de scripts, copias de modelos ni archivos de datos auxiliares. No incluye recursos 3D ni establece dependencias nuevas del juego.

Las cifras están redondeadas: planta y altura a dos decimales; superficies y volúmenes a uno. Los productos se calcularon antes del redondeo. Para recalcular o certificar la implantación será necesario volver a medir los modelos originales y resolver los casos advertidos.
