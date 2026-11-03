"""Run one real P05A/P05B native suite with its unchanged Core pin.

Each invocation requires a NEW output directory. Results and commands are
retained even on failure; no inferred PASS, remote provider or Unreal execution.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[3]
PINS = {
    'f02': '4f282863737bcd8f5add401202a9e1064c133672',
    'f03': (REPO / 'desarrollo/integration/f03/core-revision.txt').read_text().strip(),
    'f04': (REPO / 'desarrollo/integration/f04/core-revision.txt').read_text().strip(),
    'history': (REPO / 'desarrollo/integration/f04/core-history-revision.txt').read_text().strip(),
    'core': (REPO / 'desarrollo/integration/f05/core-revision.txt').read_text().strip(),
    'f05': (REPO / 'desarrollo/integration/f05/core-revision.txt').read_text().strip(),
}


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--suite', required=True, choices=PINS)
    p.add_argument('--core-source', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--generator')
    p.add_argument('--parallel', type=int, default=3)
    args = p.parse_args()
    out = args.output.resolve()
    out.relative_to((REPO / 'laboratorios').resolve())
    if out.exists():
        raise RuntimeError('Choose a NEW directory; prior laboratories are never overwritten')
    core = args.core_source.resolve()
    sha = subprocess.check_output(['git', '-C', str(core), 'rev-parse', 'HEAD'], text=True).strip()
    if sha != PINS[args.suite]:
        raise RuntimeError(f'Expected Core {PINS[args.suite]}, got {sha}')
    subprocess.run(['git', '-C', str(core), 'diff', '--exit-code', 'HEAD'], check=True)
    out.mkdir(parents=True)
    (out / 'system-temp').mkdir()
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
           **{k: str(out / 'system-temp') for k in ('TMP', 'TEMP', 'TMPDIR')},
           'F04_TEST_TEMP_ROOT': str(out / 'reference-temp')}
    record = {'suite': args.suite, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'platform': platform.platform(), 'python': platform.python_version(),
              'trek_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip(),
              'trek_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO, text=True)),
              'core': sha, 'commands': [], 'result': 'INCOMPLETE'}

    def run(name, command):
        record['commands'].append(command)
        print(name, flush=True)
        with (out / (name + '.log')).open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=REPO, env=env, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'{name} failed ({result.returncode}); inspect {out / (name + ".log")}')

    try:
        run('cmake-version', ['cmake', '--version'])
        run('ctest-version', ['ctest', '--version'])
        run('git-version', ['git', '--version'])
        source = core if args.suite == 'core' else REPO / 'desarrollo/integration' / ('f04' if args.suite == 'history' else args.suite)
        configure = ['cmake', '-S', str(source), '-B', str(out / 'build'), '-DCMAKE_BUILD_TYPE=Release']
        if args.generator:
            configure += ['-G', args.generator]
            if args.generator.startswith('Visual Studio'):
                configure += ['-A', 'x64']
        if args.suite == 'core':
            configure += ['-DBUILD_TESTING=ON', '-DCORERPG_BUILD_CONTENT_JSON=ON']
        else:
            configure += ['-DCORERPG_SOURCE_DIR=' + str(core)]
        if args.suite == 'history':
            for profile, days in ((1, 365), (2, 365), (3, 365), (4, 365), (5, 365), (5, 730)):
                run(f'oracle-{profile}-{days}', [sys.executable, str(REPO / 'desarrollo/integration/f04/tests/history_reference.py'),
                    '--profile', str(profile), '--days', str(days), '--directory', str(out / 'oracles')])
            configure += ['-DF04_ENABLE_HISTORY=ON', '-DF04_HISTORY_REFERENCE_FIXTURES=' + str(out / 'oracles')]
        run('configure', configure)
        build = ['cmake', '--build', str(out / 'build'), '--config', 'Release', '--parallel', str(args.parallel)]
        if args.suite == 'history':
            build += ['--target', 'f04_history_campaign', 'f04_history_audit']
        run('build', build)
        # CMake's actual detected compiler, version, toolset and architecture.
        record['compiler_files'] = []
        for path in (out / 'build/CMakeFiles').glob('*/CMakeCXXCompiler.cmake'):
            record['compiler_files'].append(str(path.relative_to(out)))
        test = ['ctest', '--test-dir', str(out / 'build'), '-C', 'Release', '--no-tests=error',
                '--output-on-failure', '--output-junit', str(out / 'tests.xml'), '-j', str(args.parallel)]
        if args.suite == 'history':
            test += ['-R', '^f04[.]history_campaign_']
        elif args.suite in ('f04', 'f05'):
            test += ['-E', 'history_campaign_|persistence_baseline_|persistence_resume_']
            record['excluded_diagnostics'] = 'Original monolithic 365/730-day capacity diagnostics and their resume fixtures; not executed or counted'
        run('tests', test)
        root = ET.parse(out / 'tests.xml').getroot()
        cases = root.findall('.//testcase')
        if not cases or any(root.findall('.//' + tag) for tag in ('failure', 'error', 'skipped')):
            raise RuntimeError('No complete passing JUnit')
        if any(c.get('status') != 'run' for c in cases):
            raise RuntimeError('JUnit contains unexecuted tests')
        expected_counts = {'core': 483, 'f02': 15, 'f03': 25, 'f04': 259, 'f05': 395, 'history': 6}
        if len(cases) != expected_counts[args.suite]:
            raise RuntimeError(f'Expected {expected_counts[args.suite]} tests for {args.suite}, got {len(cases)}')
        if args.suite == 'f05':
            names = [c.get('name') for c in cases]
            counts = {'f05.p02_': 20, 'f05.p03_': 26, 'f05.p04_': 38, 'f05.p05a_': 30}
            for prefix, count in counts.items():
                if sum(n.startswith(prefix) for n in names) != count:
                    raise RuntimeError('Missing native audit coverage: ' + prefix)
            if sum(n.startswith('f05.') and not n.startswith(tuple(counts)) for n in names) != 20:
                raise RuntimeError('Missing P01 cases')
        if args.suite == 'history' and len(cases) != 6:
            raise RuntimeError('All six historical campaigns are required')
        record.update(result='PASS', tests=len(cases), cases=[c.get('name') for c in cases])
    finally:
        (out / 'run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'suite': args.suite, 'tests': record['tests'], 'result': record['result']}))


if __name__ == '__main__':
    main()
