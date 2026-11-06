# F06 acceptance: one Windows window, real Aster in CoreRPG, zero Codex.
# Safe: never touches 3D assets or modifies an existing CoreRPG checkout.
param(
 [string]$CoreSource = "",
 [string]$Generator = "Visual Studio 18 2026"
)
$ErrorActionPreference = "Stop"
$Repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../.."))
$Lab = Join-Path $Repo "laboratorios/f06/qa"
$Build = Join-Path $Lab "build"
$PinnedCore = (Get-Content (Join-Path $Repo "desarrollo/integration/f05/core-revision.txt") -Raw).Trim()
if ($PinnedCore -notmatch '^[0-9a-f]{40}$') { throw "Revision CoreRPG no valida" }
foreach ($Tool in @("git","cmake","python")) {
  Get-Command $Tool -ErrorAction Stop | Out-Null
}
$Candidates = @()
if ($CoreSource) { $Candidates += $CoreSource }
$Candidates += @(
 (Join-Path $Repo "../CoreRPG"),
 (Join-Path $env:USERPROFILE "Documents/GitHub/CoreRPG"),
 (Join-Path $Lab "deps/CoreRPG")
)
$FoundCore = $null
foreach ($Candidate in $Candidates) {
  if (-not (Test-Path -LiteralPath $Candidate -PathType Container)) { continue }
  $Revision = (& git -C $Candidate rev-parse HEAD 2>$null)
  if ($LASTEXITCODE -eq 0 -and $Revision.Trim() -eq $PinnedCore) {
    $FoundCore = (Resolve-Path -LiteralPath $Candidate).Path
    break
  }
}
if (-not $FoundCore) {
  if ($CoreSource) { throw "La copia de CoreRPG indicada no coincide con la revision fijada; no se modificara." }
  $FoundCore = Join-Path $Lab "deps/CoreRPG"
  if (Test-Path -LiteralPath $FoundCore) {
    throw "CoreRPG local distinto del pin: $FoundCore . No modifico el existente."
  }
  New-Item -ItemType Directory -Path (Split-Path -Parent $FoundCore) -Force | Out-Null
  Write-Host "Preparando CoreRPG exacto dentro de laboratorios (fuera de Git)..."
  & git clone --quiet https://github.com/robdor80/CoreRPG.git $FoundCore
  if ($LASTEXITCODE) { throw "No se pudo descargar CoreRPG" }
  & git -C $FoundCore checkout --quiet --detach $PinnedCore
  if ($LASTEXITCODE) { throw "No existe la revision CoreRPG aprobada" }
}
New-Item -ItemType Directory -Path $Lab -Force | Out-Null
Write-Host "Compilando el banco de pruebas real F06/Aster..."
$Configure = @("-S",$PSScriptRoot,"-B",$Build,
   "-DCORERPG_SOURCE_DIR=$FoundCore")
if ($Generator) { $Configure += @("-G",$Generator,"-A","x64") }
& cmake @Configure
if ($LASTEXITCODE) { throw "No se pudo configurar CMake; verifica Visual Studio C++ o el generador seleccionado" }
& cmake --build $Build --config Release --target f06_aster_runner --parallel 4
if ($LASTEXITCODE) { throw "Fallo la compilacion del banco F06" }
$Runner = Join-Path $Build "f05/f04/Release/f06_aster_runner.exe"
if (-not (Test-Path -LiteralPath $Runner)) {
  $Runner = Join-Path $Build "f05/f04/f06_aster_runner.exe"
}
if (-not (Test-Path -LiteralPath $Runner)) {
  throw "No se encuentra el ejecutable F06 despues de compilar"
}
Write-Host "Iniciando guardia de ocho horas (16 minutos reales a x30)..."
& python (Join-Path $PSScriptRoot "qa/aster_gui.py") --runner $Runner
if ($LASTEXITCODE) { throw "La ventana de F06 termino con un error" }
