param(
 [Parameter(Mandatory=$true)][string]$ExpectedTrekSha,
 [Parameter(Mandatory=$true)][string]$CoreSource,
 [Parameter(Mandatory=$true)][string]$BuildRoot,
 [string]$Generator='Visual Studio 18 2026'
)
$ErrorActionPreference='Stop'
if(!$IsWindows){throw 'F06 MSI check must run on Windows'}
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$CoreSource=(Resolve-Path -LiteralPath $CoreSource).Path
$BuildRoot=[IO.Path]::GetFullPath($BuildRoot)
$Allowed=Join-Path $Repo 'laboratorios'
if(!$BuildRoot.StartsWith($Allowed+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){
 throw 'Build outputs must be inside laboratorios, never outside the project'
}
if(Test-Path -LiteralPath $BuildRoot){throw 'Use a NEW path; never overwrite previous acceptance evidence'}
if($BuildRoot -match '[^\x00-\x7F]'){throw 'Use an ASCII-only path for MSVC'}
$Head=(& git -C $Repo rev-parse HEAD).Trim()
if($LASTEXITCODE -or $Head -ne $ExpectedTrekSha){throw "Expected Star Trek $ExpectedTrekSha, got $Head"}
if((& git -C $Repo status --porcelain)){throw 'Star Trek checkout must be clean'}
$Pin=(Get-Content (Join-Path $Repo 'desarrollo/integration/f05/core-revision.txt') -Raw).Trim()
$Actual=(& git -C $CoreSource rev-parse HEAD).Trim()
if($LASTEXITCODE -or $Actual -ne $Pin){throw "Expected Core $Pin, got $Actual"}
& git -C $CoreSource diff --exit-code HEAD
if($LASTEXITCODE){throw 'Core tracked files are dirty'}
foreach($Tool in @('cmake','ctest','python')){Get-Command $Tool -ErrorAction Stop | Out-Null}
New-Item -ItemType Directory -Path $BuildRoot -Force | Out-Null
$Record=[ordered]@{
 phase='F06';status='INCOMPLETE';utc=[DateTime]::UtcNow.ToString('o')
 computer=$env:COMPUTERNAME;trek=$Head;core=$Pin
 ue_5_8_2='NOT_RUN';native='NOT_RUN';f05_smoke='NOT_RUN'
}
$Report=Join-Path $BuildRoot 'acceptance.json'
$Record | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Report
function Checked([string]$Label,[string]$Exe,[string[]]$Args) {
 & $Exe @Args 2>&1 | Tee-Object -FilePath (Join-Path $BuildRoot "$Label.log")
 if($LASTEXITCODE){throw "$Label failed with $LASTEXITCODE"}
}
try{
 $Native=Join-Path $BuildRoot 'build'
 Checked 'configure' cmake @('-S',$PSScriptRoot,'-B',$Native,'-G',$Generator,'-A','x64',
  "-DCORERPG_SOURCE_DIR=$CoreSource")
 Checked 'build' cmake @('--build',$Native,'--config','Release','--parallel','4')
 Checked 'f06-native' ctest @('--test-dir',$Native,'-C','Release','--no-tests=error',
  '--output-on-failure','-R','^f06[.]','--output-junit',(Join-Path $BuildRoot 'f06.xml'))
 [xml]$F06=Get-Content (Join-Path $BuildRoot 'f06.xml') -Raw
 $Cases=@($F06.testsuite.testcase)
 if($Cases.Count -lt 16 -or @($Cases | Where-Object {$_.failure -or $_.error -or $_.skipped}).Count){
  throw 'Expected 16 or more successful native F06 tests'
 }
 $Record.native='PASS'
 Checked 'f05-smoke' ctest @('--test-dir',$Native,'-C','Release','--no-tests=error',
  '--output-on-failure','-R','^f05[.](scenario|determinism|duplicate|stale|corrupt)$',
  '--output-junit',(Join-Path $BuildRoot 'f05.xml'))
 $Record.f05_smoke='PASS'
 $Dll=Join-Path $Native 'f05/f04/Release/TrekF04Bridge.dll'
 if(!(Test-Path -LiteralPath $Dll)){throw "Missing native bridge DLL $Dll"}
 $Record.dll_sha256=(Get-FileHash -LiteralPath $Dll -Algorithm SHA256).Hash
 $Record.native_count=$Cases.Count
 $Record.status='PASS_NATIVE_PENDING_UNREAL'
} catch {
 $Record.status='FAIL'
 throw
} finally {
 $Record | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Report
}
