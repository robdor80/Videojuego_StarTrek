[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$AssetsRoot,
    [Parameter(Mandatory)][string]$EditorCmd,
    [string]$Project = (Join-Path $PSScriptRoot '../StarTrekRPG.uproject'),
    [string]$Timeline = (Join-Path $PSScriptRoot '../../../../audiovisual/presentation/guiones/STAR_TREK_LEGENDS_ACTO_I_TIMELINE.json')
)

$ErrorActionPreference = 'Stop'
$projectPath = (Resolve-Path -LiteralPath $Project).Path
$sourcePath = (Resolve-Path -LiteralPath $AssetsRoot).Path
$manifestPath = (Resolve-Path -LiteralPath $Timeline).Path
$commandlet = (Resolve-Path -LiteralPath $EditorCmd).Path
$ffmpeg = (Get-Command ffmpeg -CommandType Application | Select-Object -First 1).Source

$repository = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$lab = Join-Path $repository 'laboratorios/cinematics/acto-i'
New-Item -ItemType Directory -Force -Path $lab | Out-Null
$run = Join-Path $lab ('import-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $run | Out-Null

function Convert-ActOneWave {
    param([string]$Source, [string]$Target, [string[]]$Filter = @())
    $sourceFile = (Resolve-Path -LiteralPath (Join-Path $sourcePath $Source)).Path
    & $ffmpeg -nostdin -v error -xerror -i $sourceFile @Filter -map_metadata -1 -vn -c:a pcm_s16le -ar 48000 -ac 2 $Target
    if ($LASTEXITCODE -ne 0) {
        throw "FFmpeg failed for $Source ($LASTEXITCODE)."
    }
}

try {
    Convert-ActOneWave 'London calling.mp3' (Join-Path $run 'London.wav')
    Convert-ActOneWave 'Ode To Harrison.mp3' (Join-Path $run 'Ode.wav')
    # Join the last and first 300 ms of the approved 30 s recording.
    # The blended section ends exactly where the body begins.
    $loop = '[0:a]asplit=3[main][tail][head];[main]atrim=start=0.3:end=29.7,asetpts=PTS-STARTPTS[body];'
    $loop += '[tail]atrim=start=29.7,asetpts=PTS-STARTPTS[t];[head]atrim=end=0.3,asetpts=PTS-STARTPTS[h];'
    $loop += '[t][h]acrossfade=d=0.3:c1=hsin:c2=hsin[blend];[body][blend]concat=n=2:v=0:a=1[out]'
    Convert-ActOneWave 'Sonido ambiental sala consejo.wav' (Join-Path $run 'CouncilLoop.wav') @('-filter_complex', $loop, '-map', '[out]')

    $common = @($projectPath, '-run=ActOneAssetSetup', '-nullrhi', '-unattended', '-nop4', '-nosplash', '-NoZenAutoLaunch',
        '-ddc=NoZenLocalFallback', "-UserDir=$run", '-stdout', '-FullStdOutLogOutput')
    & $commandlet @common '-Apply' "-Timeline=$manifestPath" "-AssetsRoot=$sourcePath" "-WavRoot=$run" "-AbsLog=$run/import.log"
    if ($LASTEXITCODE -ne 0) {
        throw "Act I import failed ($LASTEXITCODE). See $run/import.log."
    }
    & $commandlet @common "-AbsLog=$run/verify.log"
    if ($LASTEXITCODE -ne 0) {
        throw "Act I could not reopen all assets ($LASTEXITCODE). See $run/verify.log."
    }
}
finally {
    foreach ($name in 'London.wav', 'Ode.wav', 'CouncilLoop.wav') {
        Remove-Item -LiteralPath (Join-Path $run $name) -ErrorAction SilentlyContinue
    }
}
Write-Output "Act I assets verified. Logs: $run"
