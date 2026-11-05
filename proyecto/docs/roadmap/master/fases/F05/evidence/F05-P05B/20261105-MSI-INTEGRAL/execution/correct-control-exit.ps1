# Stop only the hung engine-only control from this task; preserve all logs.
$ErrorActionPreference='Stop'
$child=Get-CimInstance Win32_Process -Filter 'ProcessId=40164'
if(!$child -or $child.ParentProcessId -ne 42808 -or $child.Name -ne 'UnrealEditor-Cmd.exe' -or $child.CommandLine -notlike '*P:\laboratorios\control\EngineControl.uproject*') { throw 'Control process identity mismatch; no process stopped' }
$child | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json | Set-Content (Join-Path $PSScriptRoot 'hung-control-process.json')
Stop-Process -Id 40164 -Force
Wait-Process -Id 42808 -Timeout 30
& (Join-Path $PSScriptRoot 'execute-official-v2.ps1')
exit $LASTEXITCODE
