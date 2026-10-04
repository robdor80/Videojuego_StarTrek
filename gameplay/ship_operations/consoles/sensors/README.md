# Consola funcional — Sensores

Estado: **DRAFT v0.1 / IN_PROGRESS**

La consola de Sensores permite **detectar, buscar, localizar, medir, seguir y volver a observar** elementos del universo materializado.

No interpreta en profundidad la naturaleza científica de un fenómeno: esa responsabilidad corresponde a Ciencia. Sensores obtiene y organiza observaciones; Ciencia las interpreta.

## Principio de diseño

Una orden verbal debe poder traducirse a una secuencia navegable de menús.

Ejemplo:

> «Alférez, barrido de largo alcance del sector 041. Prioridad a emisiones subespaciales.»

Ruta funcional:

```text
SENSORES
└── BARRIDOS
    └── LARGO ALCANCE
        ├── ÁREA
        │   └── SECTOR
        │       └── 041
        ├── PRIORIDAD
        │   └── SUBESPACIO
        └── EJECUTAR
```

La consola construye una operación estructurada y la entrega al motor de resolución de sensores. El mundo ya existe antes del escaneo.

## Árbol funcional maestro v0.1

```text
SENSORES
│
├── 01. ESTADO DE SENSORES
│   ├── Estado general
│   ├── Matrices disponibles
│   ├── Alcance efectivo
│   ├── Resolución disponible
│   ├── Potencia asignada
│   ├── Integridad / daños
│   ├── Interferencias detectadas
│   └── Operación en curso
│
├── 02. BARRIDOS
│   │
│   ├── Corto alcance
│   ├── Largo alcance
│   ├── Focalizado
│   │
│   └── CONFIGURAR BARRIDO
│       ├── Modo
│       │   ├── Pasivo
│       │   └── Activo
│       │
│       ├── Área / objetivo
│       │   ├── Espacio circundante
│       │   ├── Sector
│       │   ├── Sistema estelar
│       │   ├── Coordenadas
│       │   ├── Vector
│       │   └── Contacto conocido
│       │
│       ├── Resolución
│       │   ├── General
│       │   ├── Estándar
│       │   └── Alta
│       │
│       ├── Filtros
│       │   ├── Todas las firmas
│       │   ├── Electromagnética
│       │   ├── Subespacial
│       │   ├── Gravimétrica
│       │   ├── Térmica
│       │   ├── Radiación ionizante
│       │   ├── Partículas
│       │   ├── Biológica
│       │   ├── Firma warp
│       │   └── Transpondedor artificial
│       │
│       ├── Prioridad
│       │   ├── Ninguna
│       │   └── [una firma seleccionada]
│       │
│       ├── Duración
│       │   ├── Rápida
│       │   ├── Estándar
│       │   ├── Extendida
│       │   └── Personalizada
│       │
│       ├── Revisar configuración
│       ├── EJECUTAR
│       └── CANCELAR
│
├── 03. BÚSQUEDA / LOCALIZACIÓN
│   ├── Nave
│   ├── Lanzadera
│   ├── Sonda / baliza
│   ├── Forma de vida
│   ├── Objeto artificial
│   ├── Fuente de energía
│   ├── Firma warp
│   ├── Emisión subespacial
│   ├── Señal / transpondedor
│   ├── Radiación / partículas
│   └── Firma definida
│       ├── Área de búsqueda
│       ├── Sensibilidad
│       ├── Resolución
│       ├── Criterios
│       └── INICIAR BÚSQUEDA
│
├── 04. CONTACTOS
│   ├── Todos
│   ├── No identificados
│   ├── Identificados
│   ├── Marcados
│   ├── Perdidos recientemente
│   └── [CONTACTO]
│       ├── Posición estimada
│       ├── Distancia
│       ├── Vector
│       ├── Velocidad estimada
│       ├── Firmas detectadas
│       ├── Confianza de lectura
│       ├── Clasificación disponible
│       └── Acciones
│           ├── Barrido focalizado
│           ├── Aumentar resolución
│           ├── Iniciar seguimiento
│           ├── Marcar contacto
│           ├── Comparar lecturas
│           └── Enviar datos a...
│
├── 05. SEGUIMIENTO
│   ├── Contactos seguidos
│   ├── Fijar contacto
│   ├── Seguimiento múltiple
│   ├── Seguir firma concreta
│   ├── Actualizar posición
│   ├── Estimar rumbo
│   ├── Estimar velocidad
│   ├── Predecir trayectoria
│   └── Recuperar contacto perdido
│
├── 06. LECTURA SENSORIAL
│   ├── Intensidad de señal
│   ├── Tipo de firma
│   ├── Banda / frecuencia
│   ├── Firma energética
│   ├── Firma subespacial
│   ├── Masa aproximada
│   ├── Dimensiones aproximadas
│   ├── Vector / velocidad
│   ├── Formas de vida detectables
│   └── Coincidencia con patrones conocidos
│
├── 07. INTERFERENCIAS / COMPENSACIÓN
│   ├── Estado de interferencias
│   ├── Tipo de interferencia
│   ├── Compensación automática
│   ├── Ajuste manual
│   ├── Cambiar banda / frecuencia
│   ├── Aumentar potencia
│   ├── Reducir resolución
│   ├── Prolongar integración
│   └── Intentar recuperar señal
│
├── 08. CONFIGURACIÓN
│   ├── Sensibilidad
│   ├── Resolución predeterminada
│   ├── Potencia de sensores
│   ├── Matriz / conjunto sensor
│   ├── Frecuencia / banda
│   ├── Frecuencia de actualización
│   ├── Filtros predeterminados
│   ├── Prioridades predeterminadas
│   └── Perfiles / preajustes
│
├── 09. RESULTADOS
│   ├── Operación actual
│   ├── Último barrido
│   ├── Resultados recientes
│   ├── Lecturas guardadas
│   ├── Comparar lecturas
│   ├── Repetir operación
│   └── Enviar datos a...
│       ├── Ciencia
│       ├── Táctica
│       ├── Operaciones
│       ├── CONN / Navegación
│       ├── Mando
│       └── Ordenador / Base de datos
│
└── 10. DIAGNÓSTICO
    ├── Autodiagnóstico de sensores
    ├── Estado por matriz
    ├── Calibración
    ├── Rendimiento
    ├── Errores / degradación
    └── Solicitar soporte de Ingeniería
```

## Separación con otras consolas

**Sensores sí hace:** detectar, localizar, medir, seguir, filtrar, mejorar una lectura y entregar datos.

**Sensores no hace:**

- explicar científicamente una anomalía compleja → **Ciencia**;
- disparar o fijar armas → **Táctica**;
- trazar el rumbo de la nave → **CONN / Navegación**;
- reparar físicamente una matriz dañada → **Ingeniería**;
- decidir prioridades generales de recursos de toda la nave → **OPS**.

## Estado de backend

El núcleo de `BARRIDOS` ya puede mapearse al contrato de `sensor_scan_request` y al motor de resolución v0.1.

Las ramas de seguimiento persistente, compensación avanzada, comparación histórica y diagnóstico requerirán extensiones de backend posteriores. Se definen ahora para que la arquitectura de consola no nazca limitada a la v0.0.1.

## Regla UX

Academia y naves operativas deberán exponer este mismo árbol conceptual, pero pueden:

- reorganizar visualmente los controles;
- ocultar funciones no disponibles en esa nave/era;
- añadir accesos rápidos;
- usar etiquetas o agrupaciones diferentes.

La operación subyacente no cambia.
