"""Reaudit a source-only contract transition against immutable audited oracles.

Does not change manifests or relax history_reference's production guard. The
old contract is verified against its Git revision; candidate native executables
must then match all six complete-history oracles, recover in another process,
and reconstruct every original persisted payload before a transition is emitted.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import time

from history_reference import REPO, copy_verified, require, sha256, verify

OLD_MANIFEST = 'desarrollo/integration/f04/tests/fixtures/history_reference_v1.json'
BASELINE = '5c6133b402631459a4e345cb35cf45a8812a5ce5'
CORE = '89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98'
CHANGED = {'desarrollo/integration/f04/src/f04_bridge.cpp',
           'desarrollo/integration/f04/src/f04_history.inc',
           'desarrollo/integration/f04/CMakeLists.txt'}


def git_bytes(revision, path):
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'{revision}:{path}'])


def contracts(manifest):
    return {name: sha256((REPO / name).read_bytes().replace(b'\r\n', b'\n'))
            for name in manifest['contract_files']}


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.startswith('{')]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bin', type=Path, required=True)
    p.add_argument('--core-source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=2)
    args = p.parse_args()
    require(args.jobs in (1, 2, 3), 'Bounded audit concurrency required')
    args.output.mkdir(parents=True, exist_ok=False)
    baseline = args.output / 'baseline'
    original_bytes = git_bytes(BASELINE, OLD_MANIFEST)
    require((REPO / OLD_MANIFEST).read_bytes() == original_bytes, 'Original manifest changed')
    manifest = json.loads(original_bytes)
    before = contracts(manifest)
    require({name for name, digest in before.items()
             if digest != manifest['contract_files'][name]} == CHANGED,
            'Unexpected source transition: expected only three additive F11 hooks')
    names = {OLD_MANIFEST, *manifest['contract_files'], *manifest['provenance_files']}
    for entry in manifest['campaigns'].values():
        names.update((entry['oracle'], entry['acceptance']))
    preserved = {}
    for name in sorted(names):
        data = git_bytes(BASELINE, name)
        destination = baseline / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        if name not in manifest['contract_files']:
            require((REPO / name).read_bytes() == data, f'Original evidence changed: {name}')
            preserved[name] = sha256(data)
    actual_core = subprocess.check_output(['git', '-C', str(args.core_source), 'rev-parse', 'HEAD'], text=True).strip()
    require(actual_core == CORE, 'Historical Core pin mismatch')
    require(not subprocess.check_output(['git', '-C', str(args.core_source), 'status', '--porcelain']), 'Core checkout dirty')
    suffix = '.exe' if (args.bin / 'f04_history_campaign.exe').exists() else ''
    executables = {phase: args.bin / (name + suffix) for phase, name in
                   [('campaign', 'f04_history_campaign'), ('resume', 'f04_history_campaign'), ('audit', 'f04_history_audit')]}
    require(subprocess.check_output([str(executables['campaign']), 'sha'], text=True).strip() == CORE,
            'Executed library has wrong historical Core')
    binaries = {exe.name: sha256(exe.read_bytes()) for exe in set(executables.values())}
    libraries = list(args.bin.glob('*TrekF04Bridge*'))
    require(libraries, 'Candidate bridge library missing')
    binaries.update({lib.name: sha256(lib.read_bytes()) for lib in libraries if lib.is_file()})

    def run(entry):
        profile, days = entry['profile'], entry['days']
        case = args.output / f'{profile}-{days}'
        case.mkdir()
        campaign = case / f'campaign-{profile}-{days}'
        oracle = Path(str(campaign) + '.oracle')
        # No bypass: invoke the unchanged strict verifier against the complete
        # prior source contract, then test candidate behavior against its bytes.
        metadata = copy_verified(REPO / entry['oracle'], oracle, profile, days, CORE, baseline, manifest_name=OLD_MANIFEST)
        started = time.perf_counter()
        durations = {}
        for phase in ('campaign', 'resume', 'audit'):
            command = [str(executables[phase])]
            if phase == 'campaign':
                command += ['run', str(profile), str(days), str(campaign)]
            elif phase == 'resume':
                command += ['resume', str(campaign)]
            else:
                command += [str(campaign)]
            print(f'{profile}-{days}: {phase}', flush=True)
            phase_start = time.perf_counter()
            with (case / f'{phase}.log').open('w') as log:
                result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=3300)
            require(result.returncode == 0, f'{profile}-{days}: {phase} failed, inspect retained log')
            durations[phase] = time.perf_counter() - phase_start
        observations = rows(case / 'campaign.log')
        acceptance = next(x for x in observations if x.get('kind') == 'acceptance')
        blocks = [x for x in observations if x.get('kind') == 'block']
        payload = next(x for x in rows(case / 'audit.log') if x.get('kind') == 'persisted_payload_audit')
        require(acceptance['completed'] == days and acceptance['real_watches'] and acceptance['all_blocks_equal_complete_history'], 'Incomplete campaign')
        require(len(blocks) == (days + 6) // 7 and all(x['oracle_equal'] for x in blocks), 'Missing full-history comparison')
        require(payload['blocks'] == len(blocks) and payload['all_original_block_hashes_equal'], 'Incomplete past payload audit')
        replay = next(x for x in rows(case / 'resume.log') if x.get('kind') == 'fresh_process')
        require(replay['completed'] == days and replay['future_equal'], 'Fresh-process future not verified')
        verify(REPO / entry['oracle'], profile, days, CORE, baseline, manifest_name=OLD_MANIFEST)
        verify(oracle, profile, days, CORE, baseline, manifest_name=OLD_MANIFEST)
        result = {'profile': profile, 'days': days, 'core_revision': CORE,
                  'oracle_sha256': metadata['reference_fixture_sha256'], 'acceptance': acceptance,
                  'persisted_payload_audit': payload, 'fresh_process_future_equal': True,
                  'future_day': days + 7, 'phase_seconds': durations,
                  'elapsed_seconds': time.perf_counter() - started,
                  'logs': {f'{phase}.log': sha256((case / f'{phase}.log').read_bytes())
                           for phase in ('campaign', 'resume', 'audit')}}
        (case / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
        print(f'{profile}-{days}: PASS', flush=True)
        return result

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        results = list(executor.map(run, manifest['campaigns'].values()))
    require(contracts(manifest) == before, 'Candidate source changed during audit')
    for name, digest in preserved.items():
        require(sha256((REPO / name).read_bytes()) == digest, f'Original evidence changed during audit: {name}')
    for exe in set(executables.values()) | set(libraries):
        if exe.is_file():
            require(sha256(exe.read_bytes()) == binaries[exe.name], 'Native binary changed during audit')
    summary = {'schema': 1, 'baseline_revision': BASELINE, 'core_revision': CORE,
               'original_manifest_sha256': sha256(original_bytes),
               'candidate_contract_files': before, 'previous_contract_files': manifest['contract_files'],
               'preserved_evidence_files': preserved, 'native_binaries': binaries,
               'campaigns': results, 'all_six_campaigns_passed': True,
               'guard_disabled': False}
    (args.output / 'transition.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('PASS: six complete campaigns, persisted past and fresh-process future; source transition may now be versioned', flush=True)


if __name__ == '__main__':
    main()
