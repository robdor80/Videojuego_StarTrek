"""Validate the evidence binding for the F11 source-contract transition."""
import json
from pathlib import Path

CHANGED = {'desarrollo/integration/f04/src/f04_bridge.cpp',
           'desarrollo/integration/f04/src/f04_history.inc',
           'desarrollo/integration/f04/CMakeLists.txt'}


def validate(manifest, repo, require, checked_input):
    update = manifest.get('source_contract_update_f11_a02_01')
    require(isinstance(update, dict), 'Missing F11 reaudit transition')
    provenance = manifest['provenance_files']
    previous_name, evidence_name = update['previous_manifest'], update['evidence']
    previous_bytes = checked_input(repo, previous_name, provenance[previous_name])
    previous = json.loads(previous_bytes)
    proof = json.loads(checked_input(repo, evidence_name, provenance[evidence_name]))
    require(proof['original_manifest_sha256'] == provenance[previous_name], 'F11 reaudit original manifest mismatch')
    require(proof['all_six_campaigns_passed'] is True and proof['guard_disabled'] is False,
            'F11 reaudit requires all six campaigns with protection intact')
    require(proof['core_revision'] in manifest['compatible_core_revisions'], 'F11 reaudit Core mismatch')
    require(proof['candidate_contract_files'] == manifest['contract_files'] and
            proof['previous_contract_files'] == previous['contract_files'], 'F11 reaudit source binding mismatch')
    require(manifest['campaigns'] == previous['campaigns'], 'F11 reaudit must preserve original oracles and acceptance')
    changed = {name for name, digest in manifest['contract_files'].items()
               if previous['contract_files'].get(name) != digest}
    require(changed == CHANGED and set(manifest['contract_files']) == set(previous['contract_files']),
            'F11 reaudit unexpected source transition')
    require(update['previous_contract_sha256'] == {name: previous['contract_files'][name] for name in CHANGED},
            'F11 reaudit previous hashes mismatch')
    for name, digest in previous['provenance_files'].items():
        require(provenance.get(name) == digest, 'F11 reaudit changed previous provenance')
    preserved = {previous_name: provenance[previous_name], **previous['provenance_files']}
    for entry in previous['campaigns'].values():
        preserved.update({entry['oracle']: entry['sha256'], entry['acceptance']: entry['acceptance_sha256']})
    require(proof['preserved_evidence_files'] == preserved, 'F11 reaudit missing original evidence')
    for name, digest in preserved.items():
        checked_input(repo, name, digest)
    results = proof['campaigns']
    require(len(results) == 6 and {f"{row['profile']}-{row['days']}" for row in results} == set(previous['campaigns']),
            'F11 reaudit missing or duplicate campaign')
    evidence_root = Path(evidence_name).parent
    for row in results:
        profile, days = row['profile'], row['days']
        key = f'{profile}-{days}'
        entry = previous['campaigns'][key]
        require(row['oracle_sha256'] == entry['sha256'] and row['fresh_process_future_equal'] is True and
                row['future_day'] == days + 7, 'F11 reaudit incomplete future proof')
        oracle = checked_input(repo, entry['oracle'], entry['sha256']).decode('ascii').splitlines()
        expected = [line.split() for line in oracle]
        logs = {}
        for phase in ('campaign', 'resume', 'audit'):
            name = str(evidence_root / key / f'{phase}.log').replace('\\', '/')
            require(provenance.get(name) == row['logs'][f'{phase}.log'], 'F11 reaudit log binding mismatch')
            data = checked_input(repo, name, provenance[name]).decode('utf-8')
            logs[phase] = [json.loads(line) for line in data.splitlines() if line.startswith('{')]
        blocks = [x for x in logs['campaign'] if x.get('kind') == 'block']
        require(len(blocks) == (days + 6) // 7, 'F11 reaudit incomplete block coverage')
        for block, original in zip(blocks, expected[:-1]):
            require(block['completed'] == int(original[0]) and block['issued'] == int(original[1]) and
                    block['oracle_equal'] is True, 'F11 reaudit block mismatch')
        acceptance = next(x for x in logs['campaign'] if x.get('kind') == 'acceptance')
        payload = next(x for x in logs['audit'] if x.get('kind') == 'persisted_payload_audit')
        replay = next(x for x in logs['resume'] if x.get('kind') == 'fresh_process')
        require(acceptance == row['acceptance'] and acceptance['completed'] == days and
                acceptance['all_blocks_equal_complete_history'] is True and acceptance['real_watches'] is True,
                'F11 reaudit acceptance mismatch')
        require(payload == row['persisted_payload_audit'] and payload['blocks'] == len(blocks) and
                payload['all_original_block_hashes_equal'] is True, 'F11 reaudit incomplete persisted past')
        require(replay['profile'] == profile and replay['completed'] == days and replay['future_equal'] is True,
                'F11 reaudit incomplete fresh-process replay')
        resume_name = str(evidence_root / key / f'campaign-{key}.resume').replace('\\', '/')
        resume = checked_input(repo, resume_name, provenance[resume_name]).decode('ascii').split()
        require(len(resume) == 5 and [int(x) for x in resume[:4]] ==
                [profile, days, len(blocks), int(expected[-2][1])] and resume[4] == expected[-1][2],
                'F11 reaudit frozen future digest mismatch')
