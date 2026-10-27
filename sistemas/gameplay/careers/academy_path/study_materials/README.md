# Starfleet Academy — Material de estudio v1.0

La primera capa completa de material académico ya está generada a partir del currículo autoritativo.

## Cobertura

- 60 manuales de asignatura/proceso.
- 7 manuales profesionales de rama.
- 67 bancos de evaluación.
- 67 guías de instructor.
- 1.864 preguntas/casos/prompts estructurados.

## Regla de fuente única

`curriculum/` define qué se enseña.

`study_materials/`, `assessment_banks/` e `instructor_guides/` desarrollan ese contenido.

PDF y web son salidas derivadas. No pueden introducir asignaturas, reglas o requisitos que no existan en la fuente académica.

## QA pendiente

La generación estructural está completa. Antes de considerar los manuales una edición final publicada, debe hacerse una pasada editorial y de procedencia para:
- enriquecer explicaciones donde el lore validado lo permita;
- detectar repeticiones;
- comprobar vocabulario por era;
- vincular fuentes internas;
- revisar bancos de preguntas y distractores cuando se conviertan a tipo test;
- preparar maquetación PDF y publicación web.
