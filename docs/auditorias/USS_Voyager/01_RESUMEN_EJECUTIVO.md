# Auditoría técnica y artística USS Voyager

Fecha: 21/10/2026 (Europe/Madrid). Diagnóstico exclusivamente. **No se restauró, texturizó, animó, exportó un modelo preparado ni se abrió Unreal.**

## Decisión principal

Tenemos **dos familias distintas**: una colección modular de arquitectura simplificada y un puente detallado procedente de OBJ/MAX. La colección indicada por el usuario **sí incluye una carcasa de puente**, además de pasillos, pero no es la mejor base para un puente protagonista. Su aspecto blanco procede del contenido real: ocho materiales constantes y cero texturas.

La mejor base de recuperación es **`Voyager Bridge.obj` (fuente local: `FUENTE_OBJ/Voyager Bridge.obj`)**, junto con **VoyagerB.Mtl** y **VOYBRIDGETEX-1/Textures**. Una importación temporal con separación por grupos recupera **630 objetos**, **271.705 triángulos**, **UV0 en los 630** y **49 imágenes con rutas válidas**. El GLB de trabajo conserva esas imágenes embebidas y sirve como referencia visual portable; su única malla fusionada lo hace menos cómodo como máster de edición.

La conversión `Voyager_Bridge_MAX_Trabajo.blend` contiene 631 mallas MAX separadas más el OBJ heredado, pero no gana por estar más fragmentada: tiene pérdida de superficie de suelo, materiales sin texturas, escala diferente y elementos alejados. Se conserva como fuente secundaria de comparación, no como base automática.

## Qué significa para el proyecto

1. **Puente geométrico:** el detallado contiene arquitectura, techo, suelo/plataformas, escalones, dos sillones de mando, tres asientos de estaciones, consolas, pantallas, barandillas, puertas y cabina. No es un puente jugable validado. La colección es mucho más esquemática; su mobiliario principal no está modelado.
2. **Materiales:** en la colección no hay imágenes que recuperar. En el puente detallado hay 49 imágenes sanas; el GLB las muestra. La conversión MAX no las asigna a sus 90 materiales usados. El blanco tiene, por tanto, causas diferentes según archivo.
3. **Aprovechamiento:** imágenes A; OBJ de origen B como fuente; puente final C por preparación artística y funcional. Pasillos B. El suelo frontal de la conversión MAX es D en esa conversión: es mejor recuperar el del OBJ. MAX original y funcionamiento UE5, E.
4. **Módulos:** rectos, curvas, cruces T/4 vías, accesos, turbolift, conductos, mantenimiento y habitaciones/recesos tienen potencial. Son piezas separadas en una lámina de catálogo, no una nave ensamblada.
5. **Trabajo para Unreal 5.8.2:** agrupar por función, revisar escala humana y vanos, limpiar problemas localizados, conservar UV0 útil, preparar PBR/emisión, independizar mecanismos con pivotes y diseñar colisiones. Después haría falta un laboratorio aislado con pruebas reales de tránsito, puertas, NPC y rendimiento.
6. **Primer trabajo recomendado cuando se autorice:** preparar una copia del OBJ separado con un solo recorrido de prueba —acceso, suelo, consola y silla—, antes de invertir en texturizado de todo el puente. Resolver escala y colisiones del recorrido y comparar materiales con el GLB. No reconstruir desde cero el puente de la colección mientras exista esta fuente más completa.

## Limitaciones que cambian la decisión

La cota del conjunto OBJ es **13,150 × 13,011 × 3,840 m** tras conversión Y-up→Z-up, con unidades interpretadas como metros. No prueba ergonomía. La conversión MAX tiene diferencias de escala de ~1,5081 en una pieza contrastada; no se deben mezclar coordenadas sin calibración. Los recuentos de coincidencias/UV son indicadores numéricos, no una orden de borrado ni una prueba exhaustiva de intersecciones. No se abrió el MAX binario con un lector completo.

## Entrega

Los ocho informes solicitados están enlazados en el [índice público](README.md). Se publican diagnósticos numéricos en [DATOS](DATOS/README.md). Los scripts, logs y 55 imágenes permanecen en la entrega local; consultar el [catálogo de capturas](CAPTURAS/README.md). Consultar `09_METODO_FUENTES_LIMITACIONES.md` y [DATOS/hallazgos.csv](DATOS/hallazgos.csv) para métodos y gravedad. La auditoría termina aquí; no se inicia la siguiente fase.

Verificación final: **230/230 archivos de entrada sin cambios de SHA-256, tamaño y mtime_ns**; **55 PNG decodificados**, 0 errores de imagen. Este alcance no representa un snapshot completo de todos los proyectos del ordenador.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
