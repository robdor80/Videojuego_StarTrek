"""Export executed JUnit/acceptance evidence; never synthesize a PASS.

Inputs are operator-selected output directories. Exported reports are standalone;
temporary paths are replaced with $OUTPUT and source paths with $REPO.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[3]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(__doc__)
    for name in ('native', 'core', 'f02', 'f03', 'historical'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--run-logs', required=True, type=Path)
    parser.add_argument('--history-runs', required=True, type=Path)
    parser.add_argument('--temp-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    require(not args.output.exists(), 'Choose a new evidence directory; do not overwrite')
    exports = {}
    summary = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'platform': platform.platform(), 'python': platform.python_version(),
               'source_base': 'f1ab2f33cccdd861077e59069addb8a12ff573d7',
               'source_commit_before_evidence': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
               'core_p04': (REPO / 'desarrollo/integration/f05/core-revision.txt').read_text().strip(),
               'core_f02': '4f282863737bcd8f5add401202a9e1064c133672',
               'core_f03': (REPO / 'desarrollo/integration/f03/core-revision.txt').read_text().strip(),
               'core_f04_history': (REPO / 'desarrollo/integration/f04/core-history-revision.txt').read_text().strip(),
               'oracle_origin_core': json.loads((REPO / 'desarrollo/integration/f04/tests/fixtures/history_reference_v1.json').read_text())['reference_core_revision'],
               'suites': {}, 'unreal': 'PENDIENTE', 'msi': 'PENDIENTE'}

    def scrub(value):
        return value.replace(str(args.temp_root.resolve()), '$OUTPUT').replace(str(REPO), '$REPO')

    for name in ('native', 'core', 'f02', 'f03', 'historical'):
        raw = getattr(args, name).read_bytes()
        root = ET.fromstring(raw)
        tests = root.findall('.//testcase')
        require(tests and len(tests) == int(root.attrib['tests']), f'{name}: incomplete JUnit')
        require(all(not root.findall('.//' + tag) for tag in ('failure', 'error', 'skipped')),
                f'{name}: failed or skipped tests')
        require(all(test.get('status') == 'run' for test in tests), f'{name}: tests not executed')
        require(all(int(root.get(tag, '0')) == 0 for tag in ('failures', 'disabled', 'skipped')),
                f'{name}: non-passing summary')
        names = [test.attrib['name'] for test in tests]
        summary['suites'][name] = {'tests': len(tests), 'failures': 0, 'skipped': 0,
                                  'raw_junit_sha256': digest(raw), 'cases': names}
        exports[name + '.xml'] = scrub(raw.decode()).encode()

    native = summary['suites']['native']['cases']
    for prefix, count in (('f05.p04_', 38), ('f05.p03_', 26), ('f05.p02_', 20)):
        require(sum(name.startswith(prefix) for name in native) == count, f'Missing {prefix} cases')
    require(sum(name.startswith('f05.') and not name.startswith(('f05.p02_', 'f05.p03_', 'f05.p04_'))
                for name in native) == 20, 'Missing P01 cases')
    require(summary['suites']['historical']['tests'] == 6, 'All six historical campaigns required')
    acceptance = {}
    for path in sorted(args.history_runs.glob('*/acceptance.json')):
        data = json.loads(path.read_bytes())
        key = f"{data['profile']}-{data['days']}"
        require(key not in acceptance, 'Use a single run of each historical campaign')
        require(data['completed'] == data['days'] and data['real_watches'] and
                data['all_blocks_equal_complete_history'] and data['reference_contract_verified'],
                'Historical run did not match original oracle')
        acceptance[key] = data
        exports['campaign-' + key + '.json'] = scrub(json.dumps(data, indent=2) + '\n').encode()
        for phase in ('campaign', 'resume', 'audit'):
            log = path.parent / (phase + '.log')
            require(log.is_file(), 'Missing actual historical phase log')
            exports[key + '-' + phase + '.log'] = scrub(log.read_text()).encode()
    require(set(acceptance) == {'1-365', '2-365', '3-365', '4-365', '5-365', '5-730'},
            'Missing actual historical acceptance')

    commands = {
        'documentation-unit': ['-m', 'unittest', 'discover', '-s', 'desarrollo/tools/validation', '-p', 'test_f05_reference.py', '-v'],
        'documentation-fixtures': ['desarrollo/tools/validation/f05_reference.py', '--fixture', 'desarrollo/validation/fixtures/f05/order_initiative_reference_v0.1.json'],
        'crossphase-reference': ['-m', 'unittest', 'discover', '-s', 'desarrollo/tools/simulation', '-p', 'test_f04_f05_f06_cross_phase.py', '-v'],
        'roadmap-governance': ['desarrollo/tools/validation/validate_roadmap_state.py'],
    }
    for name, command in commands.items():
        result = subprocess.run([sys.executable, *command], cwd=REPO, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        require(result.returncode == 0, f'{name}: failed\n{result.stdout}')
        exports[name + '.log'] = scrub(result.stdout).encode()
        summary[name] = {'command': ['python', *command], 'exit_code': result.returncode}

    for name in ('configure-final.log', 'build-verified.log', 'native-tests-final.log',
                 'core-tests.log', 'f02-tests.log', 'f03-tests.log', 'historical-final-tests.log',
                 'toolchain.txt'):
        path = args.run_logs / name
        require(path.is_file(), f'Missing actual log: {name}')
        exports[name] = scrub(path.read_text()).encode()

    initial = args.run_logs / 'historical-tests.log'
    if initial.is_file():
        # Optional audit of the initial pin mismatch, never counted as a PASS.
        exports['historical-initial-pin-check.log'] = scrub(initial.read_text()).encode()
        summary['initial_historical_attempt'] = 'Pin mismatch rejected before simulation; final results are in historical.xml'

    sources = set()
    for pattern in ('desarrollo/integration/f05/include/*.h', 'desarrollo/integration/f05/src/*.inc', 'desarrollo/integration/f05/src/*.cpp',
                    'desarrollo/integration/f05/tests/*.h', 'desarrollo/integration/f05/tests/*.cpp',
                    'desarrollo/integration/f05/unreal/Source/*/Private/*.cpp'):
        sources.update(REPO.glob(pattern))
    sources.update(REPO / p for p in (
        'desarrollo/integration/f04/src/f04_bridge.cpp', 'desarrollo/integration/f04/src/f04_history.inc',
        'desarrollo/integration/f04/tests/fixtures/history_reference_v1.json',
        'desarrollo/integration/f05/CMakeLists.txt', 'desarrollo/integration/f05/core-revision.txt',
        'desarrollo/integration/f05/collect_ai_evidence.py',
        'desarrollo/integration/f05/proposal-v1.schema.json',
        'sistemas/gameplay/chain_of_command/automatic_command_decision_registry_v0.1.json',
        'desarrollo/integration/f05/run_f05.ps1', '.github/workflows/f05-native-orders.yml'))
    exports['source-sha256.json'] = (json.dumps({str(p.relative_to(REPO)): digest(p.read_bytes().replace(b'\r\n', b'\n'))
                                               for p in sorted(sources)}, indent=2) + '\n').encode()
    exports['summary.json'] = (json.dumps(summary, indent=2) + '\n').encode()
    # Preserve exported checksums on Windows checkouts with core.autocrlf.
    exports['.gitattributes'] = b'* -text\n'
    exports['.gitignore'] = b'!*.log\n'
    args.output.mkdir(parents=True)
    for name, data in exports.items():
        (args.output / name).write_bytes(data)
    (args.output / 'SHA256.json').write_text(json.dumps({k: digest(v) for k, v in sorted(exports.items())}, indent=2) + '\n')
    print(json.dumps({name: data['tests'] for name, data in summary['suites'].items()}))


if __name__ == '__main__':
    main()
