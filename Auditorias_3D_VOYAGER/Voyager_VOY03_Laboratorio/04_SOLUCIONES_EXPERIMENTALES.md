# VOY-03 — Soluciones experimentales

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Alternativa recomendada: A, sin modificar geometría

El problema original era una prueba incapaz de resolver los apoyos compuestos de la escalera, no la ausencia demostrada de una conexión. La modificación experimental afecta al comprobador y a la trayectoria candidata: inventario por función real de pieza, envolvente inferior de cápsula, rechazo de contactos laterales, rechazo de diagonales y barrido completo. Objetos arquitectónicos modificados: ninguno. Diferencia de vértices, caras y matrices respecto a las copias de referencia: cero. No hay cambios globales de escala.

El archivo final comparte los mismos 645 componentes en referencia, diagnóstico, experimento A y recorrido completo. Las curvas, cámaras y cápsulas añadidas son auxiliares y no participan en colisiones. Se omitieron de la selección física 24 piezas de torso/pelvis/piernas de los antiguos maniquíes diagnósticos VOY-02: eran ayudas de representación, no mobiliario ni arquitectura. Los tres muebles de referencia del camarote sí se conservan y se contrastan como obstáculos, igual que sus datos numéricos.

## Comparativa de opciones, en el orden solicitado

| Opción | ¿Ejecutada? | Resultado | Consecuencia visual / traslado futuro |
| --- | --- | --- | --- |
| A · geometría existente | Sí | Todas las rutas objetivo superadas | Conserva arquitectura; necesita colisión y movimiento real posteriores |
| B · ajuste menor de piezas | No necesaria | No ensayada; no se atribuye un aprobado | Evitar cambios sin defecto geométrico demostrado |
| C · reconstruir peldaños | No necesaria | No ensayada | Las huellas reales ya resuelven el itinerario |
| D · adaptador nuevo | No necesaria | No ensayada | No se añade rampa, piso invisible ni nueva transición |
| E · circulación alternativa | No necesaria como solución arquitectónica | No ensayada | La ruta usa accesos y escaleras existentes; el replanteo local de búsqueda no es una reforma |

El conjunto sí reutiliza adaptadores de VOY-02, incluido AD_PUENTE revisado R1. Eso es el estado de referencia, no una adaptación creada en VOY-03. La opción A se refiere a no cambiar ese estado de trabajo.

## Ensayos rechazados y correcciones

1. Primer inventario incompleto de apoyos: no conectaba el grafo. Se preserva `busqueda_original_A0_sin_narices.json`.
2. Inventario con narices laterales pero remates centrales incompletos: diagnóstico intermedio conservado en `busqueda_original_A1_sin_1810_1811.json`.
3. Diagonal junto a Mesh_2096: libre en nodos y bloqueada entre ellos. Se conserva la coordenada y se prohíbe la arista en el grafo.
4. Barrido con tolerancia absoluta incorrecta: falso Mesh_1944 y fallo BVH en una arista compartida. Versiones antiguas en REFERENCIAS y resultados negativos en `barridos_A0_errores_numericos.json`. No se corrigió moviendo una pieza.
5. Candidato de esquina: el barrido libre no garantizaba apoyo vertical; se descarta tras certificado continuo. Se preservan `rutas_A2_atajo_esquina.json`, `barridos_A1_sin_apoyo_continuo.json` y `apoyo_A0_esquina_negativa.json`.
6. Ruta final: componente vertical de apoyo ≥0,50 y todos los intervalos certificados sobre triángulos reales. Los cambios y decisiones están en `incidencias.json`, `soluciones.json` y `cambios_experimentales.json`.

No se borraron coincidencias, consolas o barandillas. Los recortes de techo/pared para capturas se realizaron después de guardar, en copias temporales en memoria; todos los ensayos usan la geometría completa. No existe suelo invisible de ensayo ni definitivo.

[Antes/después de trayectoria](LAMINAS/05_atajo_descartado_y_ruta_final.png) · [Comparativa de la misma escalera](LAMINAS/07_comparativa_sin_reparacion.png).
