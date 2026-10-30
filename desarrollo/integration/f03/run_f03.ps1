param(
    [ValidateSet('Native','Stage','Unreal','TestUnreal','All')][string]$Stage='All',
    [Parameter(Mandatory=$true)][string]$CoreSource,
    [Parameter(Mandatory=$true)][string]$BuildRoot,
    [Parameter(Mandatory=$true)][string]$F02NativeBuild,
    [string]$F02CoreSource='C:/Users/andro/Documents/GitHub/CoreRPG',
    [string]$EngineRoot='C:/Program Files/Epic Games/UE_5.8'
)
$ErrorActionPreference='Stop'
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
$SourceRoot=$PSScriptRoot
$Repo=(Resolve-Path (Join-Path $SourceRoot '../../..')).Path
$CoreSource=(Resolve-Path -LiteralPath $CoreSource).Path
foreach($Protected in @($Repo,$CoreSource,$F02CoreSource)) {
    $P=[IO.Path]::GetFullPath($Protected)
    if($BuildRoot.Equals($P,[StringComparison]::OrdinalIgnoreCase) -or $BuildRoot.StartsWith($P+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
        throw 'BuildRoot must be outside source checkouts'
    }
}
if($BuildRoot -match '[^\x00-\x7F]') { throw 'UE build path must be ASCII' }
New-Item -ItemType Directory -Force -Path $BuildRoot,(Join-Path $BuildRoot 'logs') | Out-Null
$Run=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
function Logged([string]$Name,[string]$Exe,[string[]]$Arguments) {
    $Log=Join-Path $BuildRoot ('logs/'+$Run+'-'+$Name+'.log')
    Write-Host ('RUN '+$Exe+' '+($Arguments -join ' '))
    & $Exe @Arguments 2>&1 | Tee-Object -FilePath $Log
    if($LASTEXITCODE -ne 0) { throw "$Name failed with exit $LASTEXITCODE; $Log" }
}
$Native=Join-Path $BuildRoot 'native'
if($Stage -in @('Native','All')) {
    Logged 'configure' 'cmake' @('-S',$SourceRoot,'-B',$Native,'-G','Visual Studio 18 2026','-A','x64',"-DCORERPG_SOURCE_DIR=$CoreSource")
    Logged 'build' 'cmake' @('--build',$Native,'--config','Release','--parallel','4')
    Logged 'tests' 'ctest' @('--test-dir',$Native,'-C','Release','--no-tests=error','--output-on-failure','--output-junit',(Join-Path $BuildRoot ($Run+'-native.xml')))
}
$Lab=Join-Path $BuildRoot 'ue'
if($Stage -in @('Stage','All')) {
    if((Test-Path -LiteralPath $Lab) -and !(Test-Path -LiteralPath (Join-Path $Lab '.f03-isolated-lab'))) { throw 'Existing unrelated lab rejected' }
    # F02 runner only stages its own generated project; original projects are never touched.
    & (Join-Path $Repo 'desarrollo/integration/f02/run_f02.ps1') -Stage Stage -CoreSource $F02CoreSource -BuildRoot $BuildRoot -NativeBuild $F02NativeBuild
    Set-Content -LiteralPath (Join-Path $Lab '.f03-isolated-lab') -Value 'F03 isolated extension of F02'
    Copy-Item -Path (Join-Path $SourceRoot 'unreal/Public/*') -Destination (Join-Path $Lab 'Source/F02CoreLab/Public') -Force
    Copy-Item -Path (Join-Path $SourceRoot 'unreal/Private/*') -Destination (Join-Path $Lab 'Source/F02CoreLab/Private') -Force
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'unreal/F02CoreLab.Build.cs') -Destination (Join-Path $Lab 'Source/F02CoreLab') -Force
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'include/f03_bridge.h') -Destination (Join-Path $Lab 'ThirdParty/include') -Force
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'core-revision.txt') -Destination (Join-Path $Lab 'ThirdParty') -Force
    $CorePin=(Get-Content -LiteralPath (Join-Path $SourceRoot 'core-revision.txt') -Raw).Trim()
    Set-Content -LiteralPath (Join-Path $Lab 'ThirdParty/include/f03_core_revision.h') -Encoding ascii -Value ('#define F03_EXPECTED_CORE_SHA "'+$CorePin+'"')
    foreach($Extension in @('lib','dll')) { Copy-Item -LiteralPath (Join-Path $Native "Release/TrekF03Bridge.$Extension") -Destination (Join-Path $Lab 'ThirdParty/Win64') -Force }
    Copy-Item -LiteralPath (Join-Path $Native 'Release/TrekF03Bridge.dll') -Destination (Join-Path $Lab 'Binaries/Win64') -Force
}
$Project=Join-Path $Lab 'F02CoreLab.uproject'
if($Stage -in @('Unreal','All')) {
    Logged 'unreal-build' (Join-Path $EngineRoot 'Engine/Build/BatchFiles/Build.bat') @('F02CoreLabEditor','Win64','Development',"-Project=$Project",'-WaitMutex','-NoHotReload','-MaxParallelActions=4')
}
if($Stage -in @('TestUnreal','All')) {
    $Report=Join-Path $BuildRoot ($Run+'-ue-report')
    Logged 'unreal-tests' (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe') @($Project,'-unattended','-nop4','-nosplash','-NullRHI','-nosound','-NoLiveCoding',
        '-ExecCmds=Automation RunTests F0','-TestExit=Automation Test Queue Empty',"-ReportExportPath=$Report",'-stdout','-FullStdOutLogOutput')
    $Result=Get-Content -LiteralPath (Join-Path $Report 'index.json') -Raw | ConvertFrom-Json
    if($Result.failed -gt 0 -or $Result.notRun -gt 0 -or ($Result.succeeded+$Result.succeededWithWarnings) -ne 12) { throw 'Expected exactly twelve passing F02 + F03 tests' }
}
