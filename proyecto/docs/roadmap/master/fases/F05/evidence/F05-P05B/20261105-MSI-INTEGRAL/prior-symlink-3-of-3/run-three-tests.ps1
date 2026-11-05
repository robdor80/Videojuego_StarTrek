# Only the three CoreRPG symlink tests. No build, configuration, certification or Git mutations.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$base = 'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\laboratorios\f05\p05b\20261105'
$core = Join-Path $base 'c'
$exe = Join-Path $base 'w\laboratorios\f05\p05b\r1\core-1\build\tests\Release\corerpg_content_json_tests.exe'
$git = 'C:\Program Files\Git\cmd\git.exe'
$expectedSha = '76a7b7b485616d8c4994f384a90f123bf333591d'
$expectedHash = '08447B7814E98415C05B13C328D920932949B3E0A9F424169CC0A967EAC44CFE'
$names = @(
 'RejectsResourceSymlinkEscapingPackRootWhenSupported',
 'RejectsManifestSymlinkEscapingPackRootWhenSupported',
 'AllowsPackRootSymlinkWhenSupported'
)
$tests = @($names | ForEach-Object { 'ContentPackLoaderSymlinkTest.' + $_ })
$run = Join-Path $PSScriptRoot ('results-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + $PID)
New-Item -ItemType Directory -Path $run | Out-Null
$summary = [ordered]@{ status='ERROR'; startedUtc=[DateTime]::UtcNow.ToString('o'); elevated=$false; computer=$env:COMPUTERNAME; tests=$tests; binary=$exe; core=$core; coreSha=$null; binarySha256=$null; testExitCode=$null; results=@(); error=$null }
$exitCode = 1
$oldTemp = $env:TEMP
$oldTmp = $env:TMP
$transcript = $false
try {
 Start-Transcript -Path (Join-Path $run 'transcript.log') | Out-Null
 $transcript = $true
 $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
 $principal = New-Object Security.Principal.WindowsPrincipal($identity)
 $summary.elevated = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
 if (!$summary.elevated) { throw 'Administrator token required. No tests executed.' }
 & "$env:SystemRoot\System32\whoami.exe" /priv | Out-File (Join-Path $run 'privileges.txt') -Encoding utf8
 $sha = (& $git -C $core rev-parse HEAD | Out-String).Trim()
 if ($LASTEXITCODE -ne 0 -or $sha -ne $expectedSha) { throw 'Unexpected CoreRPG commit.' }
 $summary.coreSha = $sha
 $before = (& $git -C $core status --porcelain=v1 --untracked-files=all | Out-String)
 if ($LASTEXITCODE -ne 0 -or ![string]::IsNullOrWhiteSpace($before)) { throw 'CoreRPG checkout is not clean.' }
 $hash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash
 $summary.binarySha256 = $hash
 if ($hash -ne $expectedHash) { throw 'Test executable hash changed.' }
 $temp = Join-Path $run 'temp'
 New-Item -ItemType Directory -Path $temp | Out-Null
 # Process-local temporary paths; no Windows policy or persistent environment changes.
 $env:TEMP = $temp
 $env:TMP = $temp
 $xmlPath = Join-Path $run 'gtest.xml'
 $arguments = @(
  ('--gtest_filter=' + ($tests -join ':'))
  ('--gtest_output=xml:' + $xmlPath)
  '--gtest_color=no'
 )
 $arguments | ConvertTo-Json | Set-Content (Join-Path $run 'arguments.json') -Encoding UTF8
 Push-Location $run
 try {
  & $exe @arguments 2>&1 | Tee-Object -FilePath (Join-Path $run 'tests.log')
  $summary.testExitCode = $LASTEXITCODE
 } finally { Pop-Location }
 [xml]$report = Get-Content -LiteralPath $xmlPath -Raw
 $cases = @($report.SelectNodes('//testcase'))
 $actual = @($cases | ForEach-Object { $_.classname + '.' + $_.name })
 if ($cases.Count -ne 3 -or @(Compare-Object $tests $actual).Count -ne 0) { throw 'Report does not contain exactly the three authorized tests.' }
 $summary.results = @($cases | ForEach-Object {
  [ordered]@{name=$_.classname + '.' + $_.name; status=$_.GetAttribute('status'); result=$_.GetAttribute('result'); failures=@($_.SelectNodes('failure')).Count; skipped=@($_.SelectNodes('skipped')).Count; seconds=$_.GetAttribute('time')}
 })
 $bad = @($summary.results | Where-Object { $_.status -ne 'run' -or $_.result -ne 'completed' -or $_.failures -ne 0 -or $_.skipped -ne 0 })
 $after = (& $git -C $core status --porcelain=v1 --untracked-files=all | Out-String)
 if ($LASTEXITCODE -ne 0 -or $after -cne $before -or (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash -ne $hash) { throw 'CoreRPG checkout or executable changed during tests.' }
 if ($summary.testExitCode -ne 0 -or $bad.Count -ne 0) { throw 'Tests failed or were skipped; see tests.log and gtest.xml.' }
 $summary.status = 'PASS'
 $exitCode = 0
} catch {
 $summary.error = $_.Exception.Message
 Write-Output ('ERROR: ' + $summary.error)
} finally {
 $env:TEMP = $oldTemp
 $env:TMP = $oldTmp
 $summary['endedUtc'] = [DateTime]::UtcNow.ToString('o')
 $summary | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $run 'summary.json') -Encoding UTF8
 Write-Output ('RESULT: ' + $summary.status + '; logs: ' + $run)
 if ($transcript) { Stop-Transcript | Out-Null }
}
exit $exitCode
