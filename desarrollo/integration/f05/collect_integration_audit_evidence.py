"""Publish existing executed P05A evidence, never inferred results or overwrites."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[3]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser(__doc__)
    for suite in ('f05', 'core', 'f02', 'f03', 'f04', 'history'):
        p.add_argument('--' + suite, required=True, type=Path)
    p.add_argument('--logs', required=True, type=Path)
    p.add_argument('--temp-root', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    require(not args.output.exists(), 'Choose a new permanent evidence directory')
    exports = {}
    summary = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'source_commit_before_evidence': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
               'source_base': '1ff057456a135f00b5c665f753fd7577f866c155',
               'suites': {}, 'unreal': 'NO_EJECUTADO', 'msi': 'PENDIENTE',
               'excluded_diagnostics': '11 original monolithic long-horizon capacity/resume diagnostics, not run or counted'}

    def scrub(raw):
        return raw.decode('utf-8').replace(str(args.temp_root.resolve()), '$OUTPUT').replace(str(REPO), '$REPO').encode('utf-8')

    for suite in ('f05', 'core', 'f02', 'f03', 'f04', 'history'):
        root = getattr(args, suite)
        metadata = json.loads((root / 'run.json').read_text())
        raw = (root / 'tests.xml').read_bytes()
        tree = ET.fromstring(raw)
        tests = tree.findall('.//testcase')
        require(metadata['result'] == 'PASS' and len(tests) == metadata['tests'] == int(tree.get('tests')), suite + ': incomplete run')
        require(tests and all(t.get('status') == 'run' for t in tests), suite + ': unexecuted cases')
        require(not any(tree.findall('.//' + tag) for tag in ('failure', 'error', 'skipped')), suite + ': failed/skipped')
        summary['suites'][suite] = {'tests': len(tests), 'failures': 0, 'skipped': 0, 'core': metadata['core'],
                                   'raw_junit_sha256': digest(raw), 'cases': [t.get('name') for t in tests]}
        exports[suite + '.xml'] = scrub(raw)
        exports[suite + '-run.json'] = scrub((root / 'run.json').read_bytes())
        for log in root.glob('*.log'):
            exports[suite + '-' + log.name] = scrub(log.read_bytes())
        for compiler in (root / 'build/CMakeFiles').glob('*/CMakeCXXCompiler.cmake'):
            exports[suite + '-compiler.cmake'] = scrub(compiler.read_bytes())
        require(suite + '-compiler.cmake' in exports, suite + ': actual compiler metadata required')
    names = summary['suites']['f05']['cases']
    for prefix, count in {'f05.p02_': 20, 'f05.p03_': 26, 'f05.p04_': 38, 'f05.p05a_': 30}.items():
        require(sum(n.startswith(prefix) for n in names) == count, 'Missing ' + prefix)
    require(len(names) == 395 and sum(n.startswith('f04.') for n in names) == 261, 'Complete F04/F05 selection required')
    require(summary['suites']['history']['tests'] == 6, 'Six campaigns required')
    campaigns = {}
    for path in (args.history / 'build/history-runs').glob('*/acceptance.json'):
        d = json.loads(path.read_text())
        key = f"{d['profile']}-{d['days']}"
        require(key not in campaigns, 'Duplicate campaign')
        require(d['completed'] == d['days'] and d['real_watches'] and d['all_blocks_equal_complete_history'] and d['reference_contract_verified'], 'Invalid historical acceptance')
        campaigns[key] = d
        exports['campaign-' + key + '.json'] = scrub(path.read_bytes())
        for phase in ('campaign', 'resume', 'audit'):
            exports[key + '-' + phase + '.log'] = scrub((path.parent / (phase + '.log')).read_bytes())
    require(set(campaigns) == {'1-365', '2-365', '3-365', '4-365', '5-365', '5-730'}, 'Missing campaign acceptance')
    summary['campaigns'] = {k: {'completed': d['completed'], 'core': d['core_revision'], 'reference_fixture_sha256': d['reference_fixture_sha256']} for k, d in campaigns.items()}
    commands = {
        'documentation-unit': ['-m', 'unittest', 'discover', '-s', 'desarrollo/tools/validation', '-p', 'test_f05_reference.py', '-v'],
        'documentation-fixtures': ['desarrollo/tools/validation/f05_reference.py', '--fixture', 'desarrollo/validation/fixtures/f05/order_initiative_reference_v0.1.json'],
        'crossphase-reference': ['-m', 'unittest', 'discover', '-s', 'desarrollo/tools/simulation', '-p', 'test_f04_f05_f06_cross_phase.py', '-v'],
        'roadmap-governance': ['desarrollo/tools/validation/validate_roadmap_state.py'],
        'unreal-static': ['desarrollo/integration/f05/check_unreal_preparation.py'],
    }
    summary['documentation'] = {}
    for name, command in commands.items():
        result = subprocess.run([sys.executable, *command], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
                                     **{k: str(args.temp_root.resolve() / 'system-temp') for k in ('TMPDIR', 'TMP', 'TEMP')}})
        require(result.returncode == 0, name + ': failed\n' + result.stdout.decode())
        exports[name + '.log'] = scrub(result.stdout)
        summary['documentation'][name] = {'command': ['python', *command], 'exit_code': result.returncode}
    exports['defects-before.log'] = scrub((args.logs / 'defects-before.log').read_bytes())
    before = args.temp_root / 'native/defects-before.xml'
    failed = ET.fromstring(before.read_bytes())
    require(len(failed.findall('.//failure')) == 2 and len(failed.findall('.//testcase')) == 2, 'Two actual pre-fix reproductions required')
    exports['defects-before.xml'] = scrub(before.read_bytes())
    summary['pre_fix_reproduction'] = {'tests': 2, 'failed': 2, 'counted_as_pass': False}
    sources = set()
    for phase in ('f02', 'f03', 'f04', 'f05'):
        sources.update(p for p in (REPO / 'desarrollo/integration' / phase).rglob('*')
                       if p.is_file() and p.suffix in ('.h', '.hpp', '.cpp', '.inc', '.py', '.ps1', '.cs', '.txt', '.json', '.uproject'))
    sources.add(REPO / '.github/workflows/f05-native-orders.yml')
    exports['source-sha256.json'] = (json.dumps({str(s.relative_to(REPO)): digest(s.read_bytes().replace(b'\r\n', b'\n')) for s in sorted(sources)}, indent=2) + '\n').encode()
    exports['summary.json'] = (json.dumps(summary, indent=2) + '\n').encode()
    exports['.gitattributes'] = b'* -text\n'
    exports['.gitignore'] = b'!*.log\n'
    args.output.mkdir(parents=True)
    for name, raw in exports.items():
        (args.output / name).write_bytes(raw)
    (args.output / 'SHA256.json').write_text(json.dumps({name: digest(data) for name, data in sorted(exports.items())}, indent=2) + '\n')
    print(json.dumps({k: v['tests'] for k, v in summary['suites'].items()}))


if __name__ == '__main__':
    main()
