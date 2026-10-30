param([switch]$Apply)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'UnrealEditor*' -and $_.CommandLine -like "*$projectRoot*" }) { throw 'Cerrar este proyecto en Unreal antes de restaurar.' }
$manifestPath=Join-Path $projectRoot 'Saved\F07_Sutherland_Audit\Codex_Full_Bridge\rollback_manifest.json'
$manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$checked=@()
foreach ($file in $manifest.files) {
    $destination=[IO.Path]::GetFullPath((Join-Path $projectRoot $file.relative_path))
    $source=[IO.Path]::GetFullPath((Join-Path $manifest.backup_root $file.relative_path))
    if (-not $destination.StartsWith($projectRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Ruta fuera del proyecto.' }
    if (-not $source.StartsWith($manifest.backup_root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Ruta fuera del backup.' }
    if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $file.after_sha256) { throw "Cambios posteriores: $destination. No se ha restaurado nada." }
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $file.before_sha256) { throw "Backup no coincide: $source. No se ha restaurado nada." }
    $checked+=@{source=$source;destination=$destination}
}
if (-not $Apply) { Write-Output "Comprobados $($checked.Count) archivos. Sin escrituras. Usar -Apply para restaurarlos."; return }
foreach ($file in $checked) { Copy-Item -LiteralPath $file.source -Destination $file.destination -Force }
Write-Output "Restaurados $($checked.Count) archivos exclusivamente. Informes y herramientas conservados."
