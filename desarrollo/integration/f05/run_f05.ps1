param(
 [ValidateSet('Native','Stage','Unreal','TestUnreal','All')][string]$Stage='All',
 [Parameter(Mandatory=$true)][string]$CoreSource,
 [Parameter(Mandatory=$true)][string]$BuildRoot,
 [string]$Generator='Visual Studio 18 2026',
 [ValidateSet('P01','P02','All')][string]$Suite='All',
 [string]$EngineRoot='C:/Program Files/Epic Games/UE_5.8'
)
$ErrorActionPreference='Stop'
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$CoreSource=(Resolve-Path -LiteralPath $CoreSource).Path
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
$Allowed=Join-Path $Repo 'laboratorios'
if(!$BuildRoot.StartsWith($Allowed+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'F05 outputs must be inside the repository laboratory directory'}
if($BuildRoot -match '[^\x00-\x7F]'){throw 'Unreal staging requires an ASCII path'}
if(Test-Path $BuildRoot){if(!(Test-Path (Join-Path $BuildRoot '.f05-p01-generated'))){throw 'Unrelated existing output directory rejected; choose a new task directory'}}
New-Item -ItemType Directory -Force $BuildRoot,(Join-Path $BuildRoot 'logs'),(Join-Path $BuildRoot 'system-temp') | Out-Null
Set-Content (Join-Path $BuildRoot '.f05-p01-generated') 'F05-P01 disposable generated files only'
$PreviousTemp=$env:TEMP;$PreviousTmp=$env:TMP
$PreviousReferenceTemp=$env:F04_TEST_TEMP_ROOT
$env:F04_TEST_TEMP_ROOT=Join-Path $BuildRoot 'reference-tests'
$env:TEMP=Join-Path $BuildRoot 'system-temp';$env:TMP=$env:TEMP
$Run=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
function Logged([string]$Name,[string]$Exe,[string[]]$Arguments){
 & $Exe @Arguments 2>&1 | Tee-Object -FilePath (Join-Path $BuildRoot "logs/$Run-$Name.log")
 if($LASTEXITCODE -ne 0){throw "$Name failed: $LASTEXITCODE"}
}
try {
 $Pin=(Get-Content (Join-Path $PSScriptRoot 'core-revision.txt') -Raw).Trim()
 $Actual=(& git -C $CoreSource rev-parse HEAD).Trim()
 if($LASTEXITCODE -ne 0 -or $Actual -ne $Pin){throw "Expected Core $Pin; use a detached checkout without changing main"}
 $Native=Join-Path $BuildRoot 'native';$Lab=Join-Path $BuildRoot 'ue'
 if($Stage -in @('Native','All')){
  Logged 'configure' 'cmake' @('-S',$PSScriptRoot,'-B',$Native,'-G',$Generator,'-A','x64',"-DCORERPG_SOURCE_DIR=$CoreSource")
  Logged 'build' 'cmake' @('--build',$Native,'--config','Release','--parallel','4')
  Logged 'native-tests' 'ctest' @('--test-dir',$Native,'-C','Release','--no-tests=error','--output-on-failure','-E','history_campaign_|persistence_baseline_|persistence_resume_','--output-junit',(Join-Path $BuildRoot "$Run-native.xml"),'-j','2')
 }
 if($Stage -in @('Stage','All')){
  if((Test-Path $Lab) -and !(Test-Path (Join-Path $Lab '.f05-p01-ue'))){throw 'Unrelated UE project rejected'}
  New-Item -ItemType Directory -Force $Lab | Out-Null
  Set-Content (Join-Path $Lab '.f05-p01-ue') 'Generated F05 P01 harness, no artistic assets'
  Copy-Item (Join-Path $PSScriptRoot 'unreal/*') $Lab -Recurse -Force
  foreach($Dir in @('ThirdParty/include','ThirdParty/Win64','Binaries/Win64')){New-Item -ItemType Directory -Force (Join-Path $Lab $Dir) | Out-Null}
  Copy-Item (Join-Path $PSScriptRoot '../f04/include/f04_bridge.h') (Join-Path $Lab 'ThirdParty/include') -Force
  Copy-Item (Join-Path $PSScriptRoot 'include/f05_delegation.h') (Join-Path $Lab 'ThirdParty/include') -Force
  Copy-Item (Join-Path $PSScriptRoot 'include/f05_orders.h') (Join-Path $Lab 'ThirdParty/include') -Force
  Set-Content (Join-Path $Lab 'ThirdParty/include/f05_core_revision.h') -Encoding ascii ('#define F05_EXPECTED_CORE_SHA "'+$Pin+'"')
  foreach($Ext in @('lib','dll')){Copy-Item (Join-Path $Native "f04/Release/TrekF04Bridge.$Ext") (Join-Path $Lab 'ThirdParty/Win64') -Force}
  Copy-Item (Join-Path $Native 'f04/Release/TrekF04Bridge.dll') (Join-Path $Lab 'Binaries/Win64') -Force
 }
 $Project=Join-Path $Lab 'F05OrdersLab.uproject'
 if($Stage -in @('Unreal','TestUnreal','All')){
  $Version=Get-Content (Join-Path $EngineRoot 'Engine/Build/Build.version') -Raw | ConvertFrom-Json
  if($Version.MajorVersion -ne 5 -or $Version.MinorVersion -ne 8 -or $Version.PatchVersion -ne 2){throw 'MSI validation requires the actual UE 5.8.2 installation'}
 }
 if($Stage -in @('Unreal','All')){Logged 'ue-build' (Join-Path $EngineRoot 'Engine/Build/BatchFiles/Build.bat') @('F05OrdersLabEditor','Win64','Development',"-Project=$Project",'-WaitMutex','-NoHotReload','-MaxParallelActions=4')}
 if($Stage -in @('TestUnreal','All')){
  $Prefix=if($Suite -eq 'All'){'F05.'}else{"F05.$Suite"}
  $Expected=if($Suite -eq 'All'){6}else{3}
  $Report=Join-Path $BuildRoot "$Run-ue-report"
  Logged 'ue-tests' (Join-Path $EngineRoot 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe') @($Project,'-unattended','-nop4','-nosplash','-NullRHI','-nosound','-NoLiveCoding',"-ExecCmds=Automation RunTests $Prefix",'-TestExit=Automation Test Queue Empty',"-ReportExportPath=$Report",'-stdout','-FullStdOutLogOutput')
  $Result=Get-Content (Join-Path $Report 'index.json') -Raw | ConvertFrom-Json
  if($Result.failed -gt 0 -or $Result.notRun -gt 0 -or ($Result.succeeded+$Result.succeededWithWarnings) -ne $Expected){throw "Expected $Expected passing $Prefix Unreal tests"}
 }
} finally {$env:TEMP=$PreviousTemp;$env:TMP=$PreviousTmp;$env:F04_TEST_TEMP_ROOT=$PreviousReferenceTemp}
