# Ideas — Videojuego Star Trek RPG 3D

Este directorio es la **bandeja de entrada de ideas** del videojuego. Sirve para capturar propuestas sin interrumpir la fase de desarrollo que esté en curso.

## Reglas

1. Toda idea nueva se anota primero en [BUZON.md](./BUZON.md) con fecha, descripción y origen.
2. **Anotar una idea no equivale a aprobarla, convertirla en canon ni autorizar su implementación.**
3. Antes de desarrollarla, se revisa si ya existe una regla, contrato, asset o tarea equivalente en el repositorio.
4. Las ideas se clasifican según su destino: **Star Trek específico**, **candidato compartido con Core RPG**, **UE5/visual**, **Academia web**, **NAP/recursos** o **pendiente de clasificar**.
5. Una vez estudiada, se asigna a la fase y paso correspondientes del futuro plan maestro, respetando dependencias y criterios de cierre. Si afecta al canon o a decisiones de autor, exige aprobación expresa.
6. No adelantar trabajo de otra fase por el mero hecho de que haya surgido una idea.
7. Nunca se pierden las decisiones: si una idea se acepta, descarta o aplaza, conservar su registro y motivo.
8. No mover ni duplicar contratos existentes para introducir una idea; enlazar a sus ubicaciones originales.

## Estados de una idea

- `CAPTURADA`: registrada, sin analizar.
- `EN_ESTUDIO`: búsqueda de duplicados, encaje y dependencias.
- `NECESITA_DECISION`: exige decisión del autor.
- `PLANIFICADA`: asignada a fase y paso, no iniciada.
- `EN_DESARROLLO`: trabajándose dentro de la fase autorizada.
- `INTEGRADA`: incorporada y validada según su objetivo.
- `APLAZADA`: se conserva para otra etapa.
- `DESCARTADA`: se explica la razón; no se borra su rastro.

## Ficha mínima para nuevas ideas

```md
### IDEA-XXXX — Título
- Fecha: AAAA-MM-DD
- Estado: CAPTURADA
- Propuesta: explicación en lenguaje normal
- Motivación / experiencia que se busca:
- Sistemas relacionados: pendiente de auditar
- Tipo de destino: pendiente de clasificar
- Fase / paso: SIN ASIGNAR
- ¿Afecta al canon o requiere aprobación?: por determinar
- Referencias / decisiones:
```

## Límite importante

El repositorio `Videojuego_StarTrek` define las reglas, contenido y contratos específicos de Star Trek. Los servicios genéricos autoritativos pertenecen a **Core RPG** y la ejecución/presentación 3D a **Unreal Engine 5**.

La fase Core RPG **4.10 (Actions + Simulation)** es una oportunidad para evaluar e integrar capacidades reutilizables de acciones, órdenes, autoridad y delegación; no se debe dar por hecho que todo el sistema universal estará disponible en esa versión.

## Registro

Consultar [BUZON.md](./BUZON.md). Las fases definitivas se enlazarán cuando el plan maestro global haya sido debatido y aprobado.
