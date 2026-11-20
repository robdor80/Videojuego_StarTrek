# Copia completa y verificable del contenido artístico de StarTrekRPG.
# No modifica el proyecto ni elimina copias anteriores.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$DestinationRoot,
    [string]$ProjectDir = (Split-Path -Parent $PSScriptRoot)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-SafeContentFiles([string]$Root) {
    $pending = [System.Collections.Generic.Stack[string]]::new()
    $pending.Push($Root)
    $files = [System.Collections.Generic.List[object]]::new()
    while ($pending.Count -gt 0) {
        $dir = $pending.Pop()
        foreach ($entry in (Get-ChildItem -LiteralPath $dir -Force)) {
            if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Enlace simbolico o junction no permitido dentro de Content: $($entry.FullName)"
            }
            if ($entry.PSIsContainer) {
                $pending.Push($entry.FullName)
            } else {
                $files.Add($entry)
            }
        }
    }
    return @($files | Sort-Object FullName)
}

$project = (Resolve-Path -LiteralPath $ProjectDir).Path
if (!(Test-Path -LiteralPath (Join-Path $project 'StarTrekRPG.uproject') -PathType Leaf)) {
    throw 'ProjectDir no contiene StarTrekRPG.uproject.'
}
$contentRoot = Join-Path $project 'Content'
if (!(Test-Path -LiteralPath $contentRoot -PathType Container)) {
    throw "La carpeta Content no existe: $contentRoot"
}

$destination = [IO.Path]::GetFullPath($DestinationRoot)
if ([string]::Equals([IO.Path]::GetPathRoot($project),
        [IO.Path]::GetPathRoot($destination),
        [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Selecciona una unidad de destino distinta a la del proyecto (HDD, SSD externo o ruta de red).'
}

$files = @(Get-SafeContentFiles -Root $contentRoot)
if ($files.Count -eq 0) {
    throw 'Content no contiene archivos: no se crea una copia vacia.'
}
New-Item -ItemType Directory -Path $destination -Force | Out-Null

$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
$suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
$name = "StarTrekRPG-Content-$stamp-$suffix"
$staging = Join-Path $destination "$name.incomplete"
$final = Join-Path $destination $name
if ((Test-Path -LiteralPath $staging) -or (Test-Path -LiteralPath $final)) {
    throw 'La ruta de la copia ya existe. No se sobreescribira.'
}

$backupContent = Join-Path $staging 'Content'
New-Item -ItemType Directory -Path $backupContent -Force | Out-Null
$prefix = $contentRoot.TrimEnd([char[]]@('\', '/')) + [IO.Path]::DirectorySeparatorChar
$entries = [System.Collections.Generic.List[object]]::new()
[long]$totalBytes = 0

try {
    foreach ($file in $files) {
        if (!$file.FullName.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Ruta fuera de Content: $($file.FullName)"
        }
        $relative = $file.FullName.Substring($prefix.Length)
        $target = Join-Path $backupContent $relative
        $parent = Split-Path -Parent $target
        New-Item -ItemType Directory -Path $parent -Force | Out-Null

        # Hash antes y despues para detectar cambios durante la copia.
        $before = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
        Copy-Item -LiteralPath $file.FullName -Destination $target -ErrorAction Stop
        $copied = Get-Item -LiteralPath $target
        $after = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
        $sourceAfter = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
        if ($before -ne $after -or $sourceAfter -ne $after -or $file.Length -ne $copied.Length) {
            throw "La copia no coincide con el original: $relative"
        }

        $entries.Add([pscustomobject]@{
            path = $relative.Replace('\', '/')
            bytes = [long]$copied.Length
            sha256 = $after
        })
        $totalBytes += [long]$copied.Length
    }

    $manifest = [pscustomobject]@{
        version = 1
        project = 'StarTrekRPG'
        created_utc = (Get-Date).ToUniversalTime().ToString('o')
        source_project = $project
        file_count = $entries.Count
        total_bytes = $totalBytes
        files = @($entries.ToArray())
    }
    $manifestPath = Join-Path $staging 'manifest.json'
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
    $manifestHash = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash
    [pscustomobject]@{
        version = 1
        manifest_sha256 = $manifestHash
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $staging 'COMPLETE.json') -Encoding UTF8

    Rename-Item -LiteralPath $staging -NewName $name -ErrorAction Stop
    Write-Output "COPIA COMPLETADA: $final"
    Write-Output "Archivos: $($entries.Count); bytes: $totalBytes; SHA256 verificados."
    Write-Output "Verifica periodicamente con Build/Verify-ContentBackup.ps1 -SnapshotDir '$final'."
} catch {
    Write-Warning "Copia incompleta conservada para diagnostico: $staging"
    throw
}
