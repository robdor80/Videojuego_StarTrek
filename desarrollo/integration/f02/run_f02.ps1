param(
    [ValidateSet('Native','Stage','Unreal','TestUnreal','Demo','All')][string]$Stage='All',
    [Parameter(Mandatory=$true)][string]$CoreSource,
    [Parameter(Mandatory=$true)][string]$BuildRoot,
    [string]$EngineRoot='C:\Program Files\Epic Games\UE_5.8',
    [string]$Generator='Visual Studio 18 2026'
)
$ErrorActionPreference='Stop'
$SourceRoot=$PSScriptRoot
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
$CoreSource=(Resolve-Path -LiteralPath $CoreSource).Path
if ($BuildRoot.StartsWith($CoreSource+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'BuildRoot must be outside CoreRPG to preserve its original checkout'
}
New-Item -ItemType Directory -Force -Path $BuildRoot | Out-Null
$LogDir=Join-Path $BuildRoot 'logs'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Run=Get-Date -Format 'yyyyMMdd-HHmmss'
function Invoke-Logged([string]$Name,[string]$Exe,[string[]]$Arguments) {
    $Log=Join-Path $LogDir ($Run+'-'+$Name+'.log')
    Write-Host ('RUN '+$Exe+' '+($Arguments -join ' '))
    & $Exe @Arguments 2>&1 | Tee-Object -FilePath $Log
    if ($LASTEXITCODE -ne 0) { throw "$Name failed: exit $LASTEXITCODE; see $Log" }
}
$Native=Join-Path $BuildRoot 'native'
$Lab=Join-Path $BuildRoot 'ue'
if ($Stage -in @('Native','All')) {
    Invoke-Logged 'configure' 'cmake' @('-S',$SourceRoot,'-B',$Native,'-G',$Generator,'-A','x64',"-DCORERPG_SOURCE_DIR=$CoreSource")
    Invoke-Logged 'build' 'cmake' @('--build',$Native,'--config','Release','--parallel','4')
    Invoke-Logged 'test' 'ctest' @('--test-dir',$Native,'-C','Release','--output-on-failure','--output-junit',(Join-Path $BuildRoot ($Run+'-native-tests.xml')))
}
if ($Stage -in @('Stage','All')) {
    if ((Test-Path -LiteralPath $Lab) -and !(Test-Path -LiteralPath (Join-Path $Lab '.f02-isolated-lab'))) {
        throw 'Refusing to stage over an existing unrelated Unreal project'
    }
    New-Item -ItemType Directory -Force -Path $Lab | Out-Null
    Set-Content -LiteralPath (Join-Path $Lab '.f02-isolated-lab') -Value 'F02 generated isolated lab'
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'unreal/Source') -Destination $Lab -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'unreal/Config') -Destination $Lab -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'unreal/F02CoreLab.uproject') -Destination $Lab -Force
    $ThirdParty=Join-Path $Lab 'ThirdParty'
    New-Item -ItemType Directory -Force -Path (Join-Path $ThirdParty 'include'),(Join-Path $ThirdParty 'Win64'),(Join-Path $Lab 'Binaries/Win64') | Out-Null
    Copy-Item -LiteralPath (Join-Path $SourceRoot 'include/f02_bridge.h') -Destination (Join-Path $ThirdParty 'include') -Force
    foreach ($Extension in @('lib','dll')) {
        Copy-Item -LiteralPath (Join-Path $Native "Release/TrekF02Bridge.$Extension") -Destination (Join-Path $ThirdParty 'Win64') -Force
    }
    Copy-Item -LiteralPath (Join-Path $Native 'Release/TrekF02Bridge.dll') -Destination (Join-Path $Lab 'Binaries/Win64') -Force
}
$Project=Join-Path $Lab 'F02CoreLab.uproject'
if ($Stage -in @('Unreal','All')) {
    Invoke-Logged 'unreal-build' (Join-Path $EngineRoot 'Engine/Build/BatchFiles/Build.bat') @('F02CoreLabEditor','Win64','Development',"-Project=$Project",'-WaitMutex','-NoHotReload','-MaxParallelActions=4')
}
if ($Stage -in @('TestUnreal','All')) {
    $Report=Join-Path $BuildRoot ($Run+'-ue-report')
    Invoke-Logged 'unreal-tests' (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe') @($Project,'-unattended','-nop4','-nosplash','-NullRHI','-nosound','-NoLiveCoding','-ExecCmds=Automation RunTests F02.Core','-TestExit=Automation Test Queue Empty',"-ReportExportPath=$Report",'-stdout','-FullStdOutLogOutput')
    $Index=Join-Path $Report 'index.json'
    if (!(Test-Path -LiteralPath $Index)) { throw 'No Unreal automation report produced' }
    $Result=Get-Content -LiteralPath $Index -Raw | ConvertFrom-Json
    if ($Result.failed -gt 0 -or $Result.succeeded -ne 5) { throw 'Unreal automation suite did not pass all five tests' }
}
if ($Stage -eq 'Demo') {
    Invoke-Logged 'unreal-demo' (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor.exe') @($Project,'/Engine/Maps/Entry','-game','-windowed','-ResX=1280','-ResY=720','-dx11','-nosound','-NoLiveCoding','-F02AutoQuit','-unattended','-stdout','-FullStdOutLogOutput')
}
