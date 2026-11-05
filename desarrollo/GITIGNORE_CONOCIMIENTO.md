# Compartir conocimiento sin recursos pesados

La política de `.gitignore` permite documentación, inventarios, configuraciones compartibles y código dentro de cualquier proyecto, incluso junto a modelos. La incorporación requiere revisar el contenido: una extensión de texto no garantiza que el archivo sea publicable.

## Criterios

- Modelos, exportaciones 3D, texturas y paquetes originales permanecen locales, sin Git LFS. Se conservan los patrones anteriores de formatos 3D y se eliminan sus duplicados.
- Las imágenes de bibliotecas de recursos y auditorías permanecen locales. Los diagramas de documentación fuera de esas bibliotecas no se excluyen globalmente.
- Unreal conserva `Source`, descriptores, plugins, scripts y configuración compartible. Sus binarios, mapas y assets generados, cachés y estado del editor se ignoran. Los archivos que ya estaban versionados no se retiran por añadir estas reglas.
- Copias de seguridad, históricos y unidades experimentales prescindibles mantienen sus exclusiones. No se han movido ni borrado archivos.
- Se excluyen secretos conocidos por nombre, claves privadas y configuración local. También se revisa el contenido de cada selección; Git no puede detectar credenciales arbitrarias mediante `.gitignore`.
- El guardián del índice conserva el límite de **25 MiB**, la comprobación de blobs realmente preparados, las excepciones por hash y el bloqueo de modelos y paquetes. Las antiguas bibliotecas cerradas admiten ahora texto y código; siguen bloqueando sus binarios, incluso con adición forzada.
- Las reglas anidadas de F02 mantienen compilaciones y cachés locales. Se elimina únicamente `/ThirdParty/`, que impedía compartir fuentes, licencias y notas de dependencias.

## Conocimiento recuperado en esta entrega

Se incorporan **126 archivos ligeros existentes o derivados seguros, 864.736 bytes en total**, con un máximo individual de 73.148 bytes. No se incorporan todos los candidatos detectados.

| Carpeta | Información incorporada |
|---|---|
| `PROYECTO VALHALLA/Cubiertas Enterprise G/` | Catálogo modular, medidas y distribución conceptual de salas por cubiertas |
| `PROYECTO VALHALLA/Salas construidas/Sala computadora Enterprise Valhalla/UE5_Supercomputadora_V07_Funcional/` | Descripción técnica, inventarios y planes JSON, scripts, fuentes C++ y C#, descriptores y configuración compartible |
| `Auditorias_3D_VOYAGER/Voyager_Bridge_Recovery/informes/` | Auditoría documental de recuperación |
| `Auditorias_3D_VOYAGER/Voyager_Puente_2026-10-21/` | Inventario, geometría, materiales, interactividad, decisiones y planificación; datos seleccionados |
| `Auditorias_3D_VOYAGER/Voyager_VOY02_Laboratorio/` | Escalas, modularidad, conexión del puente, camarote y pruebas documentadas |
| `Auditorias_3D_VOYAGER/Voyager_VOY03_Laboratorio/` | Circulación, desniveles, cápsulas y recomendaciones |
| `Auditorias_3D_VOYAGER/Voyager_VOY04_Laboratorio/` | Sillas, ergonomía, consola, animaciones y preparación Unreal |
| `Auditorias_3D_VOYAGER/Voyager_VOY05A_Laboratorio/INFORMES/` | Puertas, familias arquitectónicas, dimensiones, compatibilidad Valhalla e interfaz modular |
| `Auditorias_3D_VOYAGER/Voyager_VOY05B_Laboratorio/` | Estado de reanudación y límites del trabajo |

Son informes históricos de evaluación: sus propuestas no certifican sistemas implementados. Algunos enlaces apuntan a recursos locales que deliberadamente no se publican. Las rutas personales de los documentos y tres inventarios publicados se han generalizado con `%USERPROFILE%`; los hashes de recursos inventariados se conservan. Estas referencias no son requisitos de ejecución del juego.

La configuración local `UE5_*/Config/DefaultEngine.ini` contiene un token de Android File Server y se excluye expresamente. La entrega funcional aporta `Config/DefaultEngine.ini.example`, sin esa sección. Para reconstruir la configuración, copiar la plantilla a `DefaultEngine.ini` y configurar credenciales nuevas sólo localmente. El archivo original del proyecto no se modifica. Los assets y modelos locales siguen siendo necesarios para abrir la escena completa: estas fuentes no constituyen una distribución autónoma del juego.

## Exclusiones y pendientes

Además de los formatos binarios, se mantienen exclusiones concretas para volcados JSON extensos de Enterprise, geometría numérica, trayectorias y auditorías Voyager. Las carpetas `FUENTES`, `REFERENCIAS`, `HERRAMIENTAS` y `VERIFICACION` de las auditorías contienen copias, dependencias o salidas crudas; no se publican en bloque. Sus informes propios permanecen accesibles.

Quedan para revisión posterior:

- Documentación, scripts y configuraciones de las versiones locales V05, V06 y V07 anteriores: evitar duplicar la entrega funcional y contrastar su vigencia.
- Otros CSV/JSON y scripts Voyager: seleccionar los necesarios según el informe y sus dependencias; resumir los volcados masivos antes de proponer su publicación.
- `PROYECTO VALHALLA/Clase Valhalla.docx`, su PDF y los planos gráficos de Enterprise-D: revisar contenido, tamaño y procedencia; extraer conocimiento técnico a Markdown si procede.
- Recursos de `assets/` como planos PDF, materiales exportados y el BIN de geometría: permanecen locales; publicar sus fichas e inventarios, no los recursos originales.
- `_ST/` y `3D Star Trek/` no están presentes en esta copia. Sus reglas ya permiten documentación y código, pero cualquier incorporación futura necesita revisión de contenido.

Para revisar candidatos pendientes, usar `git ls-files --others --exclude-standard` y preparar rutas explícitas. Evitar una adición global del árbol. `git check-ignore -v --no-index -- ruta` identifica la regla aplicable; el guardián se ejecuta con `python desarrollo/tools/git_binary_guard.py`.

## Logs ya versionados

La rama de trabajo inicial tenía los **67 logs** indicados: 19 de `F04-PERSISTENCIA-03-CI-OPTIMIZACION-20261031` y 48 de `F04-PERSISTENCIA-03-HISTORY`. La base `main` actual contiene **188**: esos mismos 67 y 121 adicionales de evidencias F05. Se han inspeccionado sus contenidos y se conservan todos en esta PR.

| Grupo | Archivos | Criterio |
|---|---:|---|
| F04, optimización CI | 19 | Evidencia de fallo inicial, campañas, auditoría y reanudación: conservar |
| F04, histórico | 48 | Resultados de campañas, compatibilidad, migración, regresiones y compilación: conservar; revisar tres salidas de compilación |
| F05-P03 | 22 | Evidencia de campañas y pruebas: conservar |
| F05-P04 | 30 | Evidencia de integración, pruebas, fallo del pin inicial y compilación: conservar |
| F05-P05A-CI-PRELIMINAR | 1 | Ejecución preliminar de CI: conservar como contexto |
| F05-P05A | 68 | Evidencia de validación: conservar |

Se propone revisar la retirada **sólo del índice**, sin borrar los archivos locales, de `core-final-build.log`, `faults-final-build.log` y `ue-build.log` dentro de `F04-PERSISTENCIA-03-HISTORY`. Son salidas de compilación, pero antes hay que comprobar sus referencias en informes/manifiestos y si documentan un entorno irreproducible. No se ejecuta esa retirada aquí. `legacy-history.log` y `legacy-history2.log` contienen comprobaciones de migración y se conservan. La regla general de logs evita incorporar nuevas ejecuciones; no afecta a los logs que Git ya sigue.

## Comprobación acotada

- 24 casos de reglas Git: documentos y código admitidos; modelos, cachés, secretos y unidades locales excluidos.
- 2.252 modelos existentes comprobados mediante `git check-ignore --no-index`: todos ignorados.
- Revisión de los candidatos visibles: ninguno supera 1 MiB tras excluir los falsos positivos detectados.
- Lectura de JSON seleccionados y búsqueda de indicadores de credenciales; configuración con token sustituida en la publicación por una plantilla segura.
- Dos comprobaciones dirigidas del guardián: conocimiento permitido y binarios/laboratorios bloqueados. Se valida además el índice completo antes del commit.

No se ejecutan Blender, Unreal, simulaciones ni compilaciones del juego para esta tarea.
