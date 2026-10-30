param(
 [ValidateSet('Native','Stage','Unreal','TestUnreal','All')][string]$Stage='All',
 [Parameter(Mandatory=$true)][string]$CoreSource,
 [Parameter(Mandatory=$true)][string]$BuildRoot,
 [Parameter(Mandatory=$true)][string]$F02NativeBuild,
 [Parameter(Mandatory=$true)][string]$F03NativeBuild,
 [Parameter(Mandatory=$true)][string]$F02CoreSource,
 [string]$EngineRoot='C:/Program Files/Epic Games/UE_5.8'
)
$ErrorActionPreference='Stop'
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
foreach($Source in @($Repo,$CoreSource,$F02CoreSource)) {
 $Protected=[IO.Path]::GetFullPath($Source)
 if($BuildRoot.Equals($Protected,[StringComparison]::OrdinalIgnoreCase) -or $BuildRoot.StartsWith($Protected+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'BuildRoot must be outside source checkouts'}
}
if($BuildRoot -match '[^\x00-\x7F]'){throw 'UE requires ASCII staging path on this MSI'}
New-Item -ItemType Directory -Force $BuildRoot,(Join-Path $BuildRoot 'logs') | Out-Null
$Run=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
function Logged([string]$Name,[string]$Exe,[string[]]$Arguments){
 & $Exe @Arguments 2>&1 | Tee-Object -FilePath (Join-Path $BuildRoot ('logs/'+$Run+'-'+$Name+'.log'))
 if($LASTEXITCODE -ne 0){throw "$Name failed: $LASTEXITCODE"}
}
$Native=Join-Path $BuildRoot 'native'
if($Stage -in @('Native','All')){
 Logged 'configure' 'cmake' @('-S',$PSScriptRoot,'-B',$Native,'-G','Visual Studio 18 2026','-A','x64',"-DCORERPG_SOURCE_DIR=$CoreSource")
 Logged 'build' 'cmake' @('--build',$Native,'--config','Release','--parallel','4')
 Logged 'tests' 'ctest' @('--test-dir',$Native,'-C','Release','--no-tests=error','--output-on-failure','--output-junit',(Join-Path $BuildRoot ($Run+'-native.xml')))
}
$Lab=Join-Path $BuildRoot 'ue'
if($Stage -in @('Stage','All')){
 if((Test-Path -LiteralPath $Lab) -and !(Test-Path -LiteralPath (Join-Path $Lab '.f04-isolated-lab'))){throw 'Existing unrelated lab rejected'}
 & (Join-Path $Repo 'desarrollo/integration/f02/run_f02.ps1') -Stage Stage -CoreSource $F02CoreSource -BuildRoot $BuildRoot -NativeBuild $F02NativeBuild
 Set-Content -LiteralPath (Join-Path $Lab '.f04-isolated-lab') -Value 'F04 generated isolated lab'
 $F03=Join-Path $Repo 'desarrollo/integration/f03'
 Copy-Item -Path (Join-Path $F03 'unreal/Public/*') -Destination (Join-Path $Lab 'Source/F02CoreLab/Public') -Force
 Copy-Item -Path (Join-Path $F03 'unreal/Private/*') -Destination (Join-Path $Lab 'Source/F02CoreLab/Private') -Force
 foreach($F in @('F04CampaignSubsystem.h')){Copy-Item -LiteralPath (Join-Path $PSScriptRoot "unreal/$F") -Destination (Join-Path $Lab 'Source/F02CoreLab/Public') -Force}
 foreach($F in @('F04CampaignSubsystem.cpp','F04Automation.cpp','F02CoreLab.cpp')){Copy-Item -LiteralPath (Join-Path $PSScriptRoot "unreal/$F") -Destination (Join-Path $Lab 'Source/F02CoreLab/Private') -Force}
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'unreal/F02CoreLab.Build.cs') -Destination (Join-Path $Lab 'Source/F02CoreLab') -Force
 foreach($Phase in @('f03','f04')){
  $Source=Join-Path $Repo "desarrollo/integration/$Phase"
  Copy-Item -LiteralPath (Join-Path $Source "include/${Phase}_bridge.h") -Destination (Join-Path $Lab 'ThirdParty/include') -Force
  $Pin=(Get-Content -LiteralPath (Join-Path $Source 'core-revision.txt') -Raw).Trim()
  Set-Content -LiteralPath (Join-Path $Lab "ThirdParty/include/${Phase}_core_revision.h") -Encoding ascii -Value ('#define '+$Phase.ToUpper()+'_EXPECTED_CORE_SHA "'+$Pin+'"')
  $Binary=if($Phase -eq 'f03'){$F03NativeBuild}else{$Native}
  $Bridge=if($Phase -eq 'f03'){'TrekF03Bridge'}else{'TrekF04Bridge'}
  foreach($Ext in @('lib','dll')){Copy-Item -LiteralPath (Join-Path $Binary "Release/$Bridge.$Ext") -Destination (Join-Path $Lab 'ThirdParty/Win64') -Force}
  Copy-Item -LiteralPath (Join-Path $Binary "Release/$Bridge.dll") -Destination (Join-Path $Lab 'Binaries/Win64') -Force
 }
}
$Project=Join-Path $Lab 'F02CoreLab.uproject'
if($Stage -in @('Unreal','All')){Logged 'ue-build' (Join-Path $EngineRoot 'Engine/Build/BatchFiles/Build.bat') @('F02CoreLabEditor','Win64','Development',"-Project=$Project",'-WaitMutex','-NoHotReload','-MaxParallelActions=4')}
if($Stage -in @('TestUnreal','All')){
 $Report=Join-Path $BuildRoot ($Run+'-ue-report')
 Logged 'ue-tests' (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe') @($Project,'-unattended','-nop4','-nosplash','-NullRHI','-nosound','-NoLiveCoding','-ExecCmds=Automation RunTests F0','-TestExit=Automation Test Queue Empty',"-ReportExportPath=$Report",'-stdout','-FullStdOutLogOutput')
 $Result=Get-Content -LiteralPath (Join-Path $Report 'index.json') -Raw | ConvertFrom-Json
 if($Result.failed -gt 0 -or $Result.notRun -gt 0 -or ($Result.succeeded+$Result.succeededWithWarnings) -ne 23){throw 'Expected 23 passing F02/F03/F04 Actor and UWorld tests'}
}
