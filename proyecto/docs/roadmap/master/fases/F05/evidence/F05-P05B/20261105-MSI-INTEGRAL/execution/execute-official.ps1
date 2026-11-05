# Bounded elevated execution: two engine-only startup controls, then ONE official
# P05B invocation (which itself performs two clean repetitions). No retries.
$ErrorActionPreference = 'Stop'
$task = $PSScriptRoot
$repo = Join-Path $task 'w'
$core = Join-Path $task 'c'
$expected = '027bb1d680da1f3317dac00d23ef06e0640c14ba'
$engine = 'C:\Program Files\Epic Games\UE_5.8'
$state = [ordered]@{status='INCOMPLETE';stage='preflight';startedUtc=[DateTime]::UtcNow.ToString('o');expectedHead=$expected;elevated=$false;control=@();error=$null}
$mapped = $false
$transcript = $false
$previousTemp=$env:TEMP; $previousTmp=$env:TMP; $previousTmpDir=$env:TMPDIR
function Save-State { $state | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $task 'execution-state.json') -Encoding UTF8 }
$code=1
try {
 Start-Transcript -LiteralPath (Join-Path $task 'execution.log') | Out-Null
 $transcript=$true
 $principal = [Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
 $state.elevated=$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
 if(!$state.elevated){throw 'Administrator token required; official procedure not started'}
 if(Test-Path 'P:\'){throw 'Drive P: already exists; no mapping changed'}
 & "$env:SystemRoot\System32\subst.exe" 'P:' $repo
 if($LASTEXITCODE){throw 'Short path mapping failed'}
 $mapped=$true
 Set-Location 'P:\'
 New-Item -ItemType Directory -Path (Join-Path $task 'system-temp') | Out-Null
 $env:TEMP=Join-Path $task 'system-temp';$env:TMP=$env:TEMP;$env:TMPDIR=$env:TEMP
 & 'C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 -SkipAutomaticLocation
 if((& git rev-parse HEAD).Trim() -ne $expected){throw 'Unexpected HEAD'}
 if((& git status --porcelain | Out-String).Trim()){throw 'Dirty Star Trek checkout'}
 if((& git -C $core rev-parse HEAD).Trim() -ne '76a7b7b485616d8c4994f384a90f123bf333591d'){throw 'Unexpected Core pin'}
 if((& git -C $core status --porcelain | Out-String).Trim()){throw 'Dirty Core checkout'}
 & "$env:SystemRoot\System32\whoami.exe" /priv | Set-Content (Join-Path $task 'privileges.txt')
 [ordered]@{utc=[DateTime]::UtcNow.ToString('o');powershell=$PSVersionTable.PSVersion.ToString();computer=$env:COMPUTERNAME;repoPhysical=$repo;repoShort='P:\';core=$core;head=$expected;engine=(Get-Content (Join-Path $engine 'Engine/Build/Build.version') -Raw | ConvertFrom-Json);msvc=$env:VCToolsVersion;sdk=$env:WindowsSDKVersion;gpu=@(Get-CimInstance Win32_VideoController | Select-Object Name,DriverVersion,Status);tools=@(Get-Command cmake,ctest,python,cl,dumpbin,git | Select-Object Name,Source)} | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $task 'environment.json') -Encoding UTF8
 & cmake --version; & ctest --version; & python --version; & cl 2>&1 | Out-Host
 # Check actual file AND directory symlink creation before expensive compilation.
 $probe=Join-Path $task 'privilege-probe'
 New-Item -ItemType Directory -Path $probe,(Join-Path $probe 'target-dir') | Out-Null
 Set-Content (Join-Path $probe 'target.txt') 'P05B symlink privilege probe'
 New-Item -ItemType SymbolicLink -Path (Join-Path $probe 'file-link') -Target (Join-Path $probe 'target.txt') | Out-Null
 New-Item -ItemType SymbolicLink -Path (Join-Path $probe 'dir-link') -Target (Join-Path $probe 'target-dir') | Out-Null
 Get-Item (Join-Path $probe 'file-link'),(Join-Path $probe 'dir-link') | Select-Object FullName,LinkType,Target | ConvertTo-Json | Set-Content (Join-Path $task 'privilege-probe.json')
 $state.stage='engine-only-controls'; Save-State
 $control='P:\laboratorios\control'
 New-Item -ItemType Directory -Path $control | Out-Null
 $project=Join-Path $control 'EngineControl.uproject'
 '{"FileVersion":3,"EngineAssociation":"5.8","Category":"Diagnostic","Description":"Engine-only startup control; no project modules or F05 automation"}' | Set-Content $project -Encoding ascii
 foreach($backend in @('NullRHI','Hardware')){
  $log=Join-Path $control ($backend+'-engine.log')
  $console=Join-Path $control ($backend+'-console.log')
  $arguments=@($project,'-unattended','-nop4','-nosplash','-nosound','-NoLiveCoding','-ExecCmds=Quit','-stdout','-FullStdOutLogOutput',('-abslog='+$log))
  if($backend -eq 'NullRHI'){$arguments+= '-NullRHI'}
  $arguments | ConvertTo-Json | Set-Content (Join-Path $control ($backend+'-arguments.json'))
  & (Join-Path $engine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe') @arguments 2>&1 | Tee-Object -FilePath $console
  $controlExit=$LASTEXITCODE
  $conditions=@(Select-String -LiteralPath $log -SimpleMatch 'LogAutomationTest: Error: Condition failed').Count
  $state.control+=@{backend=$backend;exitCode=$controlExit;conditionFailed=$conditions;log=$log}
  Save-State
  if($controlExit -ne 0){throw "Engine-only control $backend failed with $controlExit; no retries"}
 }
 $state.stage='official-two-clean-repetitions'; Save-State
 & 'P:\desarrollo\integration\f05\run_p05b_msi.ps1' -ExpectedTrekSha $expected -CoreSource $core -BuildRoot 'P:\laboratorios\o' -EngineRoot $engine -Generator 'Visual Studio 18 2026'
 $acceptance=Get-Content 'P:\laboratorios\o\acceptance.json' -Raw | ConvertFrom-Json
 if($acceptance.result -ne 'PASS_AUTOMATED' -or @($acceptance.runs).Count -ne 2){throw 'Official runner did not complete both repetitions'}
 $state.status='PASS_AUTOMATED_PENDING_INDEPENDENT_AUDIT'
 $state.stage='completed'
 $code=0
} catch {
 $state.error=$_.Exception.ToString()
 Write-Output ('STOP: '+$state.error)
} finally {
 $state['endedUtc']=[DateTime]::UtcNow.ToString('o'); Save-State
 $env:TEMP=$previousTemp;$env:TMP=$previousTmp;$env:TMPDIR=$previousTmpDir
 Set-Location $task
 if($mapped){ & "$env:SystemRoot\System32\subst.exe" 'P:' /D }
 if($transcript){Stop-Transcript | Out-Null}
}
exit $code
