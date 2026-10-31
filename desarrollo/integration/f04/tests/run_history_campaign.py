"""Acceptance, not a capacity diagnostic: every phase must finish successfully."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import time
import uuid
from history_reference import copy_verified, verify, require

p = argparse.ArgumentParser()
p.add_argument('--bin', required=True)
p.add_argument('--root', required=True)
p.add_argument('--profile', type=int, required=True)
p.add_argument('--days', type=int, required=True)
p.add_argument('--reference-fixtures', type=Path)
p.add_argument('--oracle-timeout', type=int, default=3300,
               help='Deep-audit oracle generation limit; never changes productive phase limits')
args = p.parse_args()
root = Path(args.root) / (datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8])
root.mkdir(parents=True)
save = root / f'campaign-{args.profile}-{args.days}'
exe = Path(args.bin)
start = time.perf_counter()
actual_core = subprocess.check_output([str(exe / 'f04_history_campaign.exe'),'sha'],text=True).strip()
require(actual_core == Path(__file__).parents[1].joinpath('core-history-revision.txt').read_text().strip(),
        'Executed Core does not match proposed pin')
phases = [
    ('oracle', [str(exe / 'f04_reference_campaign.exe'), 'run', str(args.profile), str(args.days), str(save)]),
    ('campaign', [str(exe / 'f04_history_campaign.exe'), 'run', str(args.profile), str(args.days), str(save)]),
    ('resume', [str(exe / 'f04_history_campaign.exe'), 'resume', str(save)]),
    ('audit', [str(exe / 'f04_history_audit.exe'), str(save)]),
]
reference_fixture = None
reference_metadata = {}
if args.reference_fixtures:
    reference_fixture=args.reference_fixtures/f'campaign-{args.profile}-{args.days}.oracle'
    reference_metadata = copy_verified(reference_fixture, Path(str(save)+'.oracle'),
                                       args.profile, args.days, actual_core)
    phases=phases[1:]
phase_seconds = {}
for phase, command in phases:
    print(f'{phase}: profile={args.profile} days={args.days} evidence={root}', flush=True)
    phase_start = time.perf_counter()
    with (root / f'{phase}.log').open('w', encoding='utf-8') as output:
        result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                timeout=args.oracle_timeout if phase == 'oracle' else 3300)
    phase_seconds[phase] = time.perf_counter() - phase_start
    if result.returncode:
        print((root / f'{phase}.log').read_text(encoding='utf-8'), flush=True)
        raise SystemExit(result.returncode)
blocks = [json.loads(line) for line in (root / 'campaign.log').read_text().splitlines() if line.startswith('{')]
acceptance = next(row for row in blocks if row.get('kind') == 'acceptance')
require(acceptance['completed'] == args.days and acceptance['real_watches'], 'Actual-watch horizon incomplete')
require(acceptance['all_blocks_equal_complete_history'], 'Complete-history divergence')
acceptance['storage_bytes_retaining_previous_generations'] = sum(f.stat().st_size for f in save.iterdir() if f.is_file())
acceptance['phases_elapsed_seconds'] = time.perf_counter() - start
acceptance['core_revision'] = Path(__file__).parents[1].joinpath('core-history-revision.txt').read_text().strip()
require(acceptance['core_revision'] == actual_core, 'Proposed Core pin changed during campaign')
acceptance['core_revision'] = actual_core
if reference_fixture:
    # Detect changes during simulation and prove both original and consumed bytes remain valid.
    verify(reference_fixture, args.profile, args.days, actual_core)
    verify(Path(str(save)+'.oracle'), args.profile, args.days, actual_core)
    acceptance.update(reference_metadata)
acceptance['reference_mode'] = 'verified_fixture' if reference_fixture else 'regenerated'
acceptance['phase_seconds'] = phase_seconds
(root / 'acceptance.json').write_text(json.dumps(acceptance, indent=2) + '\n')
print(json.dumps(acceptance), flush=True)
