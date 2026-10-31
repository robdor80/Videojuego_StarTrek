"""Package baseline diagnostics; never label reproduced capacity as archival acceptance.

Run the commands in F04-PERSISTENCIA-03_CAMPANAS_LARGAS.md first. Large campaign
fixtures stay in the external build directory. This tool only copies evidence.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = '45f7816c9aa996bfd678b11b4f9fa1a4b9632021'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--build-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)

    def dump(name, data):
        (a.output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def copy_log(path):
        raw = path.read_bytes()
        try:
            content = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            content = raw.decode('cp1252')  # Windows CTest localized timestamps.
        normalized = '\n'.join(line.rstrip() for line in content.splitlines()) + '\n'
        (a.output / path.name).write_bytes(normalized.encode('utf-8'))

    suites, records = {}, []
    for name in ['core', 'f02', 'f03', 'f04-existing', 'persistence']:
        path = a.build_root / (name + '.xml')
        tree = ET.parse(path).getroot()
        suite = tree if tree.tag == 'testsuite' else tree.find('testsuite')
        assert suite is not None and int(suite.attrib.get('failures', 0)) == 0
        suites[name] = dict(suite.attrib)
        shutil.copyfile(path, a.output / path.name)
    # CTest's default JUnit truncates passing stdout at 1024 bytes. Preserve and
    # read its complete LastTest.log, copied immediately after the diagnostic run.
    full_log = a.build_root / 'persistence-full.txt'
    for line in full_log.read_bytes().splitlines():
        if line.startswith(b'{'):
            records.append(json.loads(line.decode('utf-8')))
    copy_log(full_log)
    assert int(suites['f04-existing']['tests']) == 243
    assert int(suites['persistence']['tests']) == 27
    measurements = [r for r in records if r['kind'] == 'measurement']
    outcomes = [r for r in records if r['kind'] == 'baseline_outcome']
    assert len(measurements) == 15 and len(outcomes) == 6
    assert all(not r['acceptance_achieved'] for r in outcomes)
    for r in measurements:
        r['added_per_day_average'] = r['added'] / r['days']
    dump('measurements.json', measurements)
    dump('campaigns.json', records)
    dump('acceptance.json', {
        'status': 'BLOCKED_REQUIRES_GENERIC_CORE_AUTHORIZATION',
        'implemented_archival': False, 'archived_records': 0,
        'passed_diagnostics_are_not_acceptance': True,
        'baseline_outcomes': outcomes,
        'not_executed': ['archival fault injection', 'segmented recovery',
                         'consolidated history lookup', 'successful 730-day campaign'],
    })
    ue = sorted(a.build_root.glob('*-ue-report/index.json'))[-1]
    report = json.loads(ue.read_text(encoding='utf-8-sig'))
    assert report['succeeded'] + report['succeededWithWarnings'] == 25
    assert report['failed'] == report['notRun'] == 0
    suites['unreal'] = {k: report[k] for k in ['succeeded', 'succeededWithWarnings', 'failed', 'notRun', 'totalDuration']}
    shutil.copyfile(ue, a.output / 'unreal-report.json')
    dump('test-summary.json', suites)
    old = (a.build_root / 'references-base.txt').read_text(encoding='utf-8-sig')
    new = (a.build_root / 'references-current.txt').read_text(encoding='utf-8-sig')
    issues = lambda s: [line for line in s.splitlines() if line.startswith(' - ')]
    assert issues(old) == issues(new)
    dump('reference-regression.json', {'base': BASE, 'base_issues': len(issues(old)),
                                      'current_issues': len(issues(new)), 'new_issues': 0,
                                      'identical_ordered_errors': True})
    for pattern in ['*-tests.txt', 'test_*.txt', 'authority.txt', 'roadmap.txt',
                    'references-current.txt', 'native-build.txt', 'unreal-build.txt']:
        for path in a.build_root.glob(pattern):
            copy_log(path)
    sources = {}
    for phase in ['f02', 'f03', 'f04']:
        for path in (ROOT / 'desarrollo/integration' / phase).rglob('*'):
            if path.is_file() and path.suffix in ['.h', '.cpp', '.inc']:
                rel = path.relative_to(ROOT).as_posix()
                baseline = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{rel}']) if path.name != 'persistence_audit.cpp' else None
                if baseline is not None:
                    assert baseline.replace(b'\r\n', b'\n') == path.read_bytes().replace(b'\r\n', b'\n'), rel
                sources[rel] = digest(path)
    cores = {}
    for path in map(Path, ['C:/F04/CoreRPG', 'C:/F04/core-f02', 'C:/F04/core-f03']):
        cores[str(path)] = {'head': git(path, 'rev-parse', 'HEAD'), 'status': git(path, 'status', '--porcelain')}
        assert not cores[str(path)]['status']
    native = a.build_root / 'native/Release/TrekF04Bridge.dll'
    staged = a.build_root / 'ue/Binaries/Win64/TrekF04Bridge.dll'
    assert digest(native) == digest(staged)
    dump('provenance.json', {'base': BASE, 'branch': git(ROOT, 'branch', '--show-current'),
        'cores': cores, 'engine': json.loads(Path('C:/Program Files/Epic Games/UE_5.8/Engine/Build/Build.version').read_text()),
        'native_dll_sha256': digest(native), 'staged_dll_sha256': digest(staged), 'source_sha256': sources,
        'production_sources_equal_to_base': True,
        'main_status': git(Path('C:/Users/andro/Documents/GitHub/Videojuego_StarTrek'), 'status', '--porcelain'),
        'timing_scope': 'single MSI run; other build/test processes may overlap; process working set, not isolated Core allocation',
        'archival_implemented': False})
    if (a.build_root / 'compatibility.json').exists():
        shutil.copyfile(a.build_root / 'compatibility.json', a.output / 'compatibility.json')
    dump('campaign-file-hashes.json', {path.name: {'bytes': path.stat().st_size, 'sha256': digest(path)}
         for path in (a.build_root / 'native').glob('persistence-*.f04*')})
    print(json.dumps(suites, indent=2))


if __name__ == '__main__':
    main()
