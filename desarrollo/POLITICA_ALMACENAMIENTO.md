# Almacenamiento y protección de Git

Git conserva código, herramientas, configuración, contratos, lore, documentación y metadatos ligeros. Los originales 3D, texturas PBR, paquetes descargados y experimentos permanecen en disco y requieren respaldo fuera de GitHub. No se usa Git LFS.

## Exclusiones

`.gitignore` conserva `/_ST/` y `/3D Star Trek/`. La biblioteca `assets/` admite expresamente metadatos, índices y licencias. Modelos 3D y archivos Blender se excluyen en cualquier ruta, incluido `juego/`. Se excluyen paquetes comprimidos, texturas PBR y cachés `Intermediate`, `Saved`, `DerivedDataCache`, `.vs` y Python. Los laboratorios y respaldos históricos son locales.

`Source/`, `Config/`, `Plugins/` y `Content/` no se excluyen en bloque. `.uasset` y `.umap` pueden versionarse en el juego, sujetos al tamaño y a revisión de dependencias. `Plugins/Binaries` no se descarta globalmente: un plugin precompilado puede necesitarlo para restaurarse. Los binarios regenerables de la raíz del proyecto principal sí están excluidos.

## Comprobación previa al commit

```powershell
python desarrollo/tools/install_git_guard.py
python desarrollo/tools/git_binary_guard.py
python desarrollo/tools/test_git_binary_guard.py
git hook run pre-commit
```

La instalación configura únicamente `core.hooksPath` local. El instalador detecta hooks previos y exige integrarlos antes de sustituirlos. La comprobación versionada inspecciona TODOS los blobs del índice, incluso los añadidos con `git add -f`, con espacios, tildes o extensiones en mayúsculas. Usa los tamaños del índice: una copia de trabajo pequeña no oculta un blob pesado ya preparado.

Bloquea archivos individuales de más de 26.214.400 bytes (25 MiB), formatos 3D aunque sean pequeños, binarios en `assets/`, laboratorios y cachés. Los 25 MiB exactos están permitidos para formatos admitidos. El hook es local y debe instalarse en cada clon o equipo; no constituye una regla remota de GitHub.

`desarrollo/manifests/git_storage_exceptions.json` comienza vacío. Solo una decisión humana explícita y justificada permite una excepción de tamaño: registrar `path`, `size`, `sha256`, `reason` y `approved_by`, y preparar ese manifiesto en el mismo índice. El contenido exacto debe coincidir con tamaño y hash. Una excepción de tamaño no autoriza modelos 3D ni contenido de laboratorios. Revisar primero el respaldo externo y la necesidad real de almacenar el archivo en GitHub.

## Índice e historial

`.gitignore` no retira archivos ya versionados. La reorganización usa `git rm --cached` después de verificar su copia y registrar SHA-256. Los originales existentes se conservan físicamente en el MSI. Tres imágenes ya faltaban antes de esta tarea: sus blobs se guardaron fuera del repositorio y no se recrearon en la biblioteca.

La futura fusión de estos cambios retirará los archivos relacionados en `manifests/reorganizacion_20261027/indice_retirado.json` de la versión corriente de GitHub. Permanecerán en el MSI y en el historial Git previo. No se ha reescrito historial, creado un commit, hecho push ni merge.

## Restauración y respaldo

`manifests/reorganizacion_20261027/inventario_integridad.jsonl` relaciona ruta original, ruta actual, tamaño, SHA-256 original y actual, y copia local verificada. `recursos_unreal_locales.json` identifica los proyectos históricos, sus recursos y condiciones de recuperación. Restaurar los árboles completos conserva los archivos de configuración y recursos asociados; las dependencias de paquetes Unreal todavía requieren comprobación en el editor.

La copia `C:\Users\andro\Documents\StarTrek_Respaldo_Reorganizacion_20261027\files` está fuera del repositorio, en el mismo MSI. Todos los campos de respaldo externo están pendientes: no hay una unidad externa o nube verificada. Copiar y verificar estos recursos en un soporte independiente antes de considerar completo el respaldo. El proyecto definitivo todavía no es funcional y no se declara completamente respaldado.
