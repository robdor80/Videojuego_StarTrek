# Protocolo de informes durante la guardia del puente v0.1

Estado: **FOUNDATION FIXED**

## Regla principal

Las estaciones del puente informan al **oficial que tenga el mando del puente en ese momento**, no automáticamente al capitán titular de la nave.

Flujo normal:

ESTACIÓN → OFICIAL AL MANDO DEL PUENTE / OFICIAL DE GUARDIA → CAPITÁN, si procede.

El capitán recibe el informe directamente cuando:

- está personalmente al mando del puente;
- una orden permanente exige notificación;
- el oficial al mando decide escalar;
- la gravedad activa un protocolo de llamada o emergencia.

Las novedades rutinarias pueden ser resueltas por el mando de guardia sin interrumpir al capitán.

## Aplicación a Sensores

El oficial de Sensores comunica contactos, anomalías, degradaciones y otros hallazgos relevantes al mando operativo presente. Ese mando decide si mantener vigilancia, ordenar análisis adicional, cambiar prioridades o avisar al capitán.

El sistema no debe tratar al capitán como receptor obligatorio de todo informe.

## Interacción directa desde una estación

Las consolas que lo requieran pueden ofrecer un canal explícito **COMPUTADORA / OFICIAL AL MANDO** para distinguir entre dar una orden al sistema y hablar con una persona del puente.

- En modo **COMPUTADORA**, texto y voz se interpretan como órdenes o consultas al sistema de la nave.
- En modo **OFICIAL AL MANDO**, texto y voz se consideran diálogo pronunciado por el personaje al oficial que tenga realmente el mando del puente en ese momento.
- El destinatario se resuelve desde el estado vivo de la nave; no se asume que siempre sea el capitán.
- Hablar al oficial al mando no debe ejecutar automáticamente una acción de Sensores.
- La respuesta del oficial pertenece al sistema de diálogo/NPC del puente; la consola solo enruta el mensaje y aporta el contexto operativo necesario.
