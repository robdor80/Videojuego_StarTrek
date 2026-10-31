"""Verify frozen full-history expectations; never load campaign state from them."""
import argparse
import hashlib
import json
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[4]
MANIFEST = 'desarrollo/integration/f04/tests/fixtures/history_reference_v1.json'


class ReferenceError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReferenceError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_file(path):
    try:
        return path.read_bytes()
    except OSError as error:
        raise ReferenceError(f'Missing/unreadable reference input: {path}') from error


def checked_input(repo, name, expected):
    data = read_file(repo / name)
    require(sha256(data) == expected, f'Reference provenance SHA-256 mismatch: {name}')
    return data


def contract(profile, days, actual_core, repo=None):
    repo = repo or REPO
    manifest = json.loads(read_file(repo / MANIFEST))
    require(manifest['schema'] == 1, 'Unsupported reference manifest schema')
    require(actual_core in manifest['compatible_core_revisions'], 'Incompatible Core revision')
    require((repo / 'desarrollo/integration/f04/core-history-revision.txt').read_text().strip()
            == actual_core, 'Executed Core does not match proposed pin')
    for name, expected in manifest['contract_files'].items():
        data = read_file(repo / name).replace(b'\r\n', b'\n')
        require(sha256(data) == expected, f'Incompatible source/contract: {name}; regenerate and audit reference')
    key = f'{profile}-{days}'
    require(key in manifest['campaigns'], f'No audited reference for profile/duration {key}')
    entry = manifest['campaigns'][key]
    require(entry['profile'] == profile and entry['days'] == days, 'Reference profile/duration mismatch')
    for name, expected in manifest['provenance_files'].items():
        checked_input(repo, name, expected)
    acceptance = json.loads(checked_input(repo, entry['acceptance'], entry['acceptance_sha256']))
    require(acceptance['profile'] == profile and acceptance['days'] == days
            and acceptance['completed'] == days, 'Reference acceptance profile/duration mismatch')
    require(acceptance['real_watches'] and acceptance['all_blocks_equal_complete_history'],
            'Reference lacks full-history acceptance')
    require(acceptance['core_revision'] == actual_core
            and acceptance['reference_core_revision'] == manifest['reference_core_revision']
            and acceptance['reference_fixture_sha256'] == entry['sha256'], 'Reference provenance mismatch')
    return manifest, entry


def validate_rows(data, days):
    try:
        rows = [line.split() for line in data.decode('ascii').splitlines()]
        expected_days = list(range(7, days, 7)) + [days, days + 7]
        require(len(rows) == len(expected_days), 'Truncated or extra reference rows')
        previous = 0
        for row, expected_day in zip(rows, expected_days):
            require(len(row) == 3, 'Unsupported oracle row schema')
            day, issued, digest = row
            require(int(day) == expected_day and int(issued) > previous,
                    'Invalid oracle horizon or identity watermark')
            require(re.fullmatch('[0-9a-f]{64}', digest) is not None, 'Invalid oracle block SHA-256')
            previous = int(issued)
    except (UnicodeError, ValueError) as error:
        if isinstance(error, ReferenceError):
            raise
        raise ReferenceError('Invalid oracle row schema') from error


def verify(path, profile, days, actual_core, repo=None):
    manifest, entry = contract(profile, days, actual_core, repo)
    require(path.name == f'campaign-{profile}-{days}.oracle', 'Incorrect reference filename')
    data = read_file(path)
    require(sha256(data) == entry['sha256'], f'Oracle SHA-256 mismatch: {path}')
    validate_rows(data, days)
    return data, {
        'reference_fixture_sha256': entry['sha256'],
        'reference_core_revision': manifest['reference_core_revision'],
        'reference_origin': manifest['origin'],
        'reference_evidence_commit': manifest['evidence_commit'],
        'reference_manifest_schema': manifest['schema'],
        'reference_manifest_sha256': sha256(read_file((repo or REPO) / MANIFEST).replace(b'\r\n', b'\n')),
        'reference_profile': profile,
        'reference_days': days,
        'reference_contract_verified': True,
    }


def copy_verified(source, destination, profile, days, actual_core, repo=None):
    data, metadata = verify(source, profile, days, actual_core, repo)
    require(source.resolve() != destination.resolve(), 'Cannot overwrite original reference')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation: existing originals, backups and laboratory files stay intact.
    with destination.open('xb') as output:
        output.write(data)
    require(read_file(destination) == data, 'Reference copy readback mismatch')
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--profile', type=int, required=True)
    parser.add_argument('--days', type=int, required=True)
    args = parser.parse_args()
    actual_core = (REPO / 'desarrollo/integration/f04/core-history-revision.txt').read_text().strip()
    _, entry = contract(args.profile, args.days, actual_core)
    destination = args.directory / f'campaign-{args.profile}-{args.days}.oracle'
    metadata = copy_verified(REPO / entry['oracle'], destination, args.profile, args.days, actual_core)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
