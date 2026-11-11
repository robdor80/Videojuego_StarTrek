"""Build and execute exactly the 13 F11 C++ cases, retaining native evidence."""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[3]
CASES = {'f11.' + name for name in ('promotion', 'negatives', 'authority', 'identity',
         'idempotency', 'atomic', 'corrupt', 'legacy', 'history', 'abi',
         'process_save', 'process_load', 'product_bridge')}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--core-source', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--parallel', type=int, default=3)
    args = p.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    expected = (REPO / 'desarrollo/integration/f05/core-revision.txt').read_text().strip()
    sha = subprocess.check_output(['git', '-C', str(args.core_source), 'rev-parse', 'HEAD'], text=True).strip()
    if sha != expected or subprocess.check_output(['git', '-C', str(args.core_source), 'status', '--porcelain']):
        raise RuntimeError('F11 requires a clean checkout of the unchanged F05 Core pin')
    env = {**os.environ, 'PYTHONPYCACHEPREFIX': str(out / 'pycache'),
           'F04_TEST_TEMP_ROOT': str(out / 'reference-temp')}
    record = {'schema': 1, 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'platform': platform.platform(), 'core_revision': sha, 'commands': [], 'result': 'INCOMPLETE'}

    def run(name, command):
        record['commands'].append(command)
        with (out / f'{name}.log').open('w', encoding='utf-8') as log:
            result = subprocess.run(command, cwd=REPO, env=env, stdout=log, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'{name} failed ({result.returncode}); inspect retained log')

    try:
        run('configure', ['cmake', '-S', str(REPO / 'desarrollo/integration/f11'), '-B', str(out / 'build'),
                          '-DCMAKE_BUILD_TYPE=Release', '-DCORERPG_SOURCE_DIR=' + str(args.core_source.resolve())])
        compilers = list((out / 'build/CMakeFiles').glob('*/CMakeCXXCompiler.cmake'))
        if len(compilers) != 1:
            raise RuntimeError('Missing native compiler evidence')
        compiler = compilers[0].read_text()
        record['compiler_id'] = re.search(r'set\(CMAKE_CXX_COMPILER_ID "([^"]+)"\)', compiler).group(1)
        record['compiler_version'] = re.search(r'set\(CMAKE_CXX_COMPILER_VERSION "([^"]+)"\)', compiler).group(1)
        if os.name == 'nt' and record['compiler_id'] != 'MSVC':
            raise RuntimeError('Windows CI must actually compile with MSVC')
        run('build', ['cmake', '--build', str(out / 'build'), '--config', 'Release', '--parallel', str(args.parallel),
                      '--target', 'f11_tests', 'f11_product_tests'])
        run('tests', ['ctest', '--test-dir', str(out / 'build'), '-C', 'Release', '-R', '^f11[.]',
                      '--no-tests=error', '--output-on-failure', '--output-junit', str(out / 'tests.xml')])
        root = ET.parse(out / 'tests.xml').getroot()
        cases = root.findall('.//testcase')
        if len(cases) != 13 or {c.get('name') for c in cases} != CASES:
            raise RuntimeError('Expected all 13 distinct native F11 cases')
        if any(root.findall('.//' + tag) for tag in ('failure', 'error', 'skipped')) or any(c.get('status') != 'run' for c in cases):
            raise RuntimeError('Native F11 failure, skip or unexecuted case')
        record.update(result='PASS', tests=13, cases=sorted(CASES))
    finally:
        (out / 'run.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'result': 'PASS', 'tests': 13, 'compiler': record['compiler_id']}))


if __name__ == '__main__':
    main()
