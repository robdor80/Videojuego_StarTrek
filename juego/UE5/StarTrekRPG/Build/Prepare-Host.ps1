param(
    [Parameter(Mandatory)][string]$CoreSource,
    [Parameter(Mandatory)][string]$BuildRoot,
    [string]$ProjectDir = (Split-Path -Parent $PSScriptRoot),
    [string]$Generator = 'Visual Studio 18 2026'
)

$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path
$CoreSource = (Resolve-Path -LiteralPath $CoreSource).Path
$BuildRoot = [IO.Path]::GetFullPath($BuildRoot)
$HostSource = Join-Path $Repo 'desarrollo/integration/host'
if (!(Test-Path -LiteralPath (Join-Path $ProjectDir 'StarTrekRPG.uproject'))) {
    throw 'Expected the StarTrekRPG descriptor in ProjectDir.'
}

$OldTemp = $env:TEMP
$OldTmp = $env:TMP
$OldTmpDir = $env:TMPDIR
try {
    $env:TEMP = Join-Path $BuildRoot 'tmp'
    $env:TMP = $env:TEMP
    $env:TMPDIR = $env:TEMP
    New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
    & cmake -S $HostSource -B $BuildRoot -G $Generator -A x64 "-DCORERPG_SOURCE_DIR=$CoreSource" -DTREK_HOST_TESTS=OFF
    if ($LASTEXITCODE) { throw 'HOST configure failed.' }
    & cmake --build $BuildRoot --config Release --parallel 3 --target TrekHost
    if ($LASTEXITCODE) { throw 'HOST Release build failed.' }

    $Stage = Join-Path $ProjectDir 'Binaries/Host'
    $HeaderDir = Join-Path $Stage 'include/trek/host'
    New-Item -ItemType Directory -Path $HeaderDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $HostSource 'include/trek/host/host_abi.h') -Destination $HeaderDir
    foreach ($Dll in @('TrekHost.dll', 'TrekF04Bridge.dll')) {
        Copy-Item -LiteralPath (Join-Path $BuildRoot "f05/f04/Release/$Dll") -Destination $Stage
    }
} finally {
    $env:TEMP = $OldTemp
    $env:TMP = $OldTmp
    $env:TMPDIR = $OldTmpDir
}
