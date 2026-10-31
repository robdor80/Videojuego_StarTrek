"""Acceptance, not a capacity diagnostic: every phase must finish successfully."""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import time
import uuid

p = argparse.ArgumentParser()
p.add_argument('--bin', required=True)
p.add_argument('--root', required=True)
p.add_argument('--profile', type=int, required=True)
p.add_argument('--days', type=int, required=True)
args = p.parse_args()
root = Path(args.root) / (datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8])
root.mkdir(parents=True)
save = root / f'campaign-{args.profile}-{args.days}'
exe = Path(args.bin)
start = time.perf_counter()
for phase, command in (
    ('oracle', [str(exe / 'f04_reference_campaign.exe'), 'run', str(args.profile), str(args.days), str(save)]),
    ('campaign', [str(exe / 'f04_history_campaign.exe'), 'run', str(args.profile), str(args.days), str(save)]),
    ('resume', [str(exe / 'f04_history_campaign.exe'), 'resume', str(save)]),
    ('audit', [str(exe / 'f04_history_audit.exe'), str(save)]),
):
    print(f'{phase}: profile={args.profile} days={args.days} evidence={root}', flush=True)
    with (root / f'{phase}.log').open('w', encoding='utf-8') as output:
        result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, timeout=3300)
    if result.returncode:
        print((root / f'{phase}.log').read_text(encoding='utf-8'), flush=True)
        raise SystemExit(result.returncode)
blocks = [json.loads(line) for line in (root / 'campaign.log').read_text().splitlines() if line.startswith('{')]
acceptance = next(row for row in blocks if row.get('kind') == 'acceptance')
assert acceptance['completed'] == args.days and acceptance['real_watches']
assert acceptance['all_blocks_equal_complete_history']
acceptance['storage_bytes_retaining_previous_generations'] = sum(f.stat().st_size for f in save.iterdir() if f.is_file())
acceptance['phases_elapsed_seconds'] = time.perf_counter() - start
acceptance['core_revision'] = Path(__file__).parents[1].joinpath('core-history-revision.txt').read_text().strip()
(root / 'acceptance.json').write_text(json.dumps(acceptance, indent=2) + '\n')
print(json.dumps(acceptance), flush=True)
