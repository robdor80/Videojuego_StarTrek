# LORE-01 B — Auditoría de diseño y fuentes (18-10-2026)

## 1. Estado anterior validado

- PR #25 LORE-01 A: fusionada `abcc4c77`; 25 especies, monografías y evidencias.
- PR #26 LORE-01 A.1: fusionada `a25122fa`; guías culturales de NPC que **no** otorgan personalidad universal ni deberes por origen.
- `sistemas/gameplay/diplomacy/major_faction_catalogue.json`: **8** potencias ya identificadas en diseño. Se reutilizan sus identificadores sin alterarlos.
- `sistemas/gameplay/organizations/profiles`, `sistemas/gameplay/diplomacy/faction_runtime_model.json`, `sistemas/gameplay/diplomacy/federation_relation_anchors.json`, `sistemas/gameplay/organizations/organization_runtime_contract.json`, `sistemas/ai/npc_behavior/faction_authority_guardrails.md`: contratos **existentes** y no reemplazados.
- `mundo/sources/canon_policy.md` exige canon audiovisual retenido, referencias oficiales y declaraciones de incertidumbre. No se utiliza `Enterprise`, `Discovery` ni `Picard` como evidencia de pantalla nueva en B.

## 2. Nueva cobertura

16 monografías y 16 libros de evidencias estructuradas. Nueve entidades fundamentales: Federación, Klingon, Romulanos, Cardassianos, Ferengi, Bajor, Dominio, Breen y Colectividad Borg especial. Siete adicionales: Maquis, Sección 31, Sindicato de Orión, Asamblea Tholiana, Hegemonía Gorn, gobierno tzenkethi poco documentado y Comisión de Simbiosis de Trill. Todos con diez dominios, bibliografía de episodios, contexto temporal, incertidumbres y efecto de credenciales NPC.

Se conservan instituciones que no deben confundirse con potencia: Consejo Federal, Alto Consejo Klingon, Tal Shiar, Orden Obsidiana, Consejo Detapa, FCA, Milicia Bajorana, Asamblea de Vedeks/Kai, administradores Vorta y militares Jem'Hadar. Otras entidades menores del siglo XXIV quedan **identificadas como ampliación progresiva**, no se dan por agotadas. No se han creado mapas, fronteras ni rutas.

## 3. Descubrimientos y precauciones

1. `DS9_THE_ADVERSARY`: golpe del Autarca tzenkethi **inventado por un infiltrado**; no convertir rumor falso en estado histórico. También advertir de la denominación «Coalición Tzenkethi», más frecuente en material complementario, que no acredita constitución por la simple palabra.
2. «Confederación Breen» no prueba mecanismo federal, ciudadanía, régimen sucesorio ni economía cuantificable. `ST_OFFICIAL_BREEN_EXPLAINER` mezcla `Discovery`; únicamente se utiliza su sección DS9.
3. «Sección 31» no debe actuar como gobierno, ni sus autodescripciones prueban legitimidad jurídica constitucional.
4. Sindicatos criminales no son especies, gobiernos ni estados soberanos; origen nacional no determina afiliación.
5. Fundación Borg: solo una red colectiva tecno-política que incorpora especies distintas; drones liberados son personas con historia propia. No hay acceso al portal IDEA-0011 desde Alfa para Borg.
6. Las cronologías distinguen hechos antes/después del inicio de partida y no aplican ni predicen automáticamente el futuro canónico.
7. Una potestad estatal acreditada no equivale a la facultad individual de todos sus ciudadanos u oficiales.

## 4. Lagunas abiertas sin inventar

Los regímenes exactos de elecciones, tribunales, presupuestos, sucesión y grados de control en muchas potencias no se conocen suficientemente. Las fechas por año no fijan hora y día exactos de cada acto. La red de colonias y sistemas estelares, movimiento de flotas, tratados ejecutables, rutas de comercio y motor de simulación todavía **no** están hechos. Cualquier futura invención que cambie geopolítica real requerirá el procedimiento de decisión del autor.

## 5. Alcance y aceptación

Solo documentos Markdown, libros JSON, ejemplos autorales y validador CI. `CONTENT_STATUS.md` se regulariza por la fusión previa A.1. No se cambia código de generación del universo, CoreRPG, UE5 ni acuerdos de las ideas. No autorizar `COMPLETE` hasta revisión del propietario, comprobación CI, fusión manual y auditoría de `main`.

**Antes de LORE-01 C**: obtener autorización expresa del propietario. Si se requieren datos puntuales de un tratado, proceso judicial o cronología por fecha exacta antes de hacer una misión, verificar escenas y registrar resultado con fuente primaria; la base actual es extensa pero no inspección fotograma por fotograma.

## 6. Verificación CI reproducible (18-10-2026)

**Primera ejecución de la nueva CI:** `39108683101` falló por una prueba demasiado literal: buscaba «falsa» cuando el expediente tzenkethi correctamente decía «falsedad». El **validador de expedientes ya pasaba**. Se corrigió el test, sin cambiar el hecho histórico.

**Ejecuciones posteriores verdes verificadas para HEAD `8fad163ecf79f36d1df8961abcb4532ba590b7a7`:**

- LORE-01 B PR: [GitHub Actions #39108736391](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/39108736391), **SUCCESS**.
- LORE-01 B push: [GitHub Actions #39108732447](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/39108732447), **SUCCESS**.
- LORE-01 A documental: [GitHub Actions #39108736375](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/39108736375), **SUCCESS**.
- `validate_lore01_b.py` -> 16 expedientes, referencias, ámbitos, identidades y guardas DLC coherentes.
- `test_lore01_b.py`: **14/14**; las seis suites de validación/regresión ejecutadas bajo el workflow nuevo incluyen A básica **8/8**, A profunda **7/7**, A.1 **11/11**, total **40/40 tests**.
- Fuentes `mundo/sources/source_registry/source_registry.json`: **421** después de añadir 27 sin borrar las 394 iniciales.
- La PR #27 está en **NEEDS_REVIEW** hasta la revisión/fusión expresas del propietario. Aunque las pruebas documentales son verdes, ninguna compila UE5 ni prueba el comportamiento runtime de CoreRPG; tampoco es auditoría audiovisual escena a escena.

En cada nuevo commit de la rama se repite CI antes del merge. La ejecución consignada corresponde al commit identificado y no certifica automáticamente futuros cambios.
