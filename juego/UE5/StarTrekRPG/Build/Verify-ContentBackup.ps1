# Verificacion independiente de una copia de Content. Solo lectura.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$SnapshotDir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath $SnapshotDir).Path
$markerPath = Join-Path $root 'COMPLETE.json'
$manifestPath = Join-Path $root 'manifest.json'
$contentRoot = Join-Path $root 'Content'
foreach ($required in @($markerPath, $manifestPath)) {
    if (!(Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Copia incompleta: falta $required"
    }
}
if (!(Test-Path -LiteralPath $contentRoot -PathType Container)) {
    throw "Copia incompleta: falta $contentRoot"
}

$marker = Get-Content -LiteralPath $markerPath -Raw -Encoding UTF8 | ConvertFrom-Json
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($marker.version -ne 1 -or $manifest.version -ne 1 -or $manifest.project -ne 'StarTrekRPG') {
    throw 'Formato de manifiesto no reconocido.'
}
$hash = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash
if ($hash -ne $marker.manifest_sha256) {
    throw 'El manifiesto ha cambiado: hash SHA256 incorrecto.'
}
$items = @($manifest.files)
if ($items.Count -ne [int]$manifest.file_count) {
    throw 'El numero de archivos no coincide con el manifiesto.'
}
$prefix = $contentRoot.TrimEnd([char[]]@('\', '/')) + [IO.Path]::DirectorySeparatorChar
$known = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
[long]$sum = 0
foreach ($entry in $items) {
    $relative = [string]$entry.path
    if ([string]::IsNullOrWhiteSpace($relative) -or
        [IO.Path]::IsPathRooted($relative) -or
        $relative.Contains(':') -or
        $relative.Contains('\') -or
        $relative.StartsWith('/') -or
        $relative.Split('/') -contains '..' -or
        $relative.Split('/') -contains '.') {
        throw "Ruta invalida en manifiesto: $relative"
    }
    if (!$known.Add($relative)) {
        throw "Ruta duplicada en manifiesto: $relative"
    }
    $filePath = [IO.Path]::GetFullPath((Join-Path $contentRoot ($relative.Replace('/', '\'))))
    if (!$filePath.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Ruta fuera de Content: $relative"
    }
    if (!(Test-Path -LiteralPath $filePath -PathType Leaf)) {
        throw "Falta un archivo en la copia: $relative"
    }
    $file = Get-Item -LiteralPath $filePath
    if (($file.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Enlace simbolico no permitido en la copia: $relative"
    }
    if ($file.Length -ne [long]$entry.bytes) {
        throw "Tamano distinto: $relative"
    }
    $actualHash = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash
    if ($actualHash -ne [string]$entry.sha256) {
        throw "Hash SHA256 incorrecto: $relative"
    }
    $sum += [long]$file.Length
}
$present = @(Get-ChildItem -LiteralPath $contentRoot -File -Recurse -Force)
if ($present.Count -ne $items.Count -or $sum -ne [long]$manifest.total_bytes) {
    throw 'El total de archivos o bytes de la copia no coincide con el manifiesto.'
}
Write-Output "VERIFICACION CORRECTA: $root"
Write-Output "Archivos: $($items.Count); bytes: $sum; SHA256 de cada archivo OK."
