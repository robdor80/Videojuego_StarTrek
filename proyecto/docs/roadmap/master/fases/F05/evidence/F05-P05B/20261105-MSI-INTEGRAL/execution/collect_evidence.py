"""Validate both official repetitions and copy byte-identical evidence for PR 89."""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

TASK = Path(__file__).resolve().parent
REPO = TASK / 'w'
OUT = REPO / 'laboratorios/p'
DEST = REPO / 'proyecto/docs/roadmap/master/fases/F05/evidence/F05-P05B/20261105-MSI-INTEGRAL'
HEAD = '027bb1d680da1f3317dac00d23ef06e0640c14ba'
CORE = '76a7b7b485616d8c4994f384a90f123bf333591d'
CONDITION = 'LogAutomationTest: Error: Condition failed'
SKIP = 'ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt'

def read_json(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def text(p):
    raw = p.read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig', errors='replace')

def put(p, relative):
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(p, target)
    assert digest(p) == digest(target)

def junit(p):
    cases = ET.parse(p).getroot().findall('.//testcase')
    failed = [c.get('name') for c in cases if c.find('failure') is not None or c.find('error') is not None]
    skipped = [c.get('name') for c in cases if c.find('skipped') is not None]
    passed = [c.get('name') for c in cases if c.get('status') == 'run' and c.get('name') not in failed + skipped]
    return {'discovered': len(cases), 'passed': len(passed), 'skipped': skipped, 'failed': failed,
            'cases': [{'name': c.get('name'), 'status': c.get('status'), 'time': c.get('time'),
                       'outcome': 'SKIP' if c.get('name') in skipped else 'FAIL' if c.get('name') in failed else 'PASS'} for c in cases]}

def startup(log):
    data = text(log)
    lines = data.splitlines()
    conditions = [i+1 for i, line in enumerate(lines) if CONDITION in line]
    engine_init = [i+1 for i, line in enumerate(lines) if 'LogEngine: Initializing Engine...' in line]
    f05_queue = [i+1 for i, line in enumerate(lines) if 'Cmd: Automation RunTests F05.' in line or 'Test Started. Name=' in line]
    hardware = [line for line in lines if any(s in line for s in (
        'Using Default RHI:', 'Chosen D3D12 Adapter Id', 'Found D3D12 adapter 0:',
        'RHI D3D12 with Feature Level', 'Driver Version:', 'LogRHI:             Name:'))]
    return {'condition_failed_count': len(conditions), 'condition_failed_lines': conditions,
            'engine_initialization_lines': engine_init, 'f05_queue_lines': f05_queue,
            'bridge_ready': 'bridge ready=1' in data, 'hardware_evidence': hardware,
            'other_error_lines': [line for line in lines if ': Error:' in line and CONDITION not in line],
            'warning_lines': [line for line in lines if ': Warning:' in line]}, data

def main():
    state = read_json(TASK / 'execution-state-v3.json')
    acceptance = read_json(OUT / 'acceptance.json')
    assert state['status'] == 'PASS_AUTOMATED_PENDING_INDEPENDENT_AUDIT' and state['elevated']
    assert acceptance['result'] == 'PASS_AUTOMATED' and len(acceptance['runs']) == 2
    assert acceptance['trek'] == HEAD and acceptance['core'] == CORE
    assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    for record in read_json(TASK / 'runner-hashes-v3.json'):
        assert digest(Path(record['Path'])).upper() == record['Hash']
    expected = read_json(REPO / 'desarrollo/integration/f05/unreal/expected-tests.json')
    assert len(expected) == 12 and len(set(expected)) == 12
    summary = {'status': 'PASS_AUTOMATED_REVIEWED_PENDING_INDEPENDENT_AUDIT', 'tested_head': HEAD,
               'core': CORE, 'complete_clean_repetitions': 2, 'runs': [], 'engine_only_controls': [],
               'final_acceptance': 'PENDING_INDEPENDENT_AUDIT_AND_OWNER_ACT',
               'phase': 'F05 EN_CURSO; F06 BLOQUEADA; PR 89 DRAFT; NO MERGE',
               'source_changes_during_execution': False}
    for iteration in (1, 2):
        core = OUT / f'core-{iteration}'
        clean = OUT / f'clean-{iteration}'
        cr = junit(core / 'tests.xml')
        assert (cr['discovered'], cr['passed'], cr['skipped'], cr['failed']) == (483, 482, [SKIP], [])
        assert read_json(core / 'run.json')['result'] == 'PASS_COMPATIBLE_WITH_PLATFORM_SKIP'
        symlinks = [c for c in cr['cases'] if c['name'].startswith('ContentPackLoaderSymlinkTest.')]
        assert len(symlinks) == 3 and all(c['outcome'] == 'PASS' for c in symlinks)
        native_reports = list(clean.glob('*-native.xml'))
        assert len(native_reports) == 1
        nr = junit(native_reports[0])
        assert (nr['discovered'], nr['passed'], nr['skipped'], nr['failed']) == (395, 395, [], [])
        p05a = [c for c in nr['cases'] if c['name'].startswith('f05.p05a_')]
        assert len(p05a) == 30
        dll = read_json(clean / 'logs/dll-load.json')
        assert dll['core'] == CORE and len(dll['exports']) == 62
        dll_paths = [clean / 'native/f04/Release/TrekF04Bridge.dll', clean / 'ue/ThirdParty/Win64/TrekF04Bridge.dll', clean / 'ue/Binaries/Win64/TrekF04Bridge.dll']
        assert all(digest(p).upper() == dll['dll_sha256'] for p in dll_paths)
        assert digest(clean / 'native/f04/Release/TrekF04Bridge.lib') == digest(clean / 'ue/ThirdParty/Win64/TrekF04Bridge.lib')
        ubt_logs = list((clean / 'logs').glob('*-ue-build.log'))
        assert len(ubt_logs) == 1 and 'Result: Succeeded' in text(ubt_logs[0])
        ue_logs = sorted((clean / 'logs').glob('*-ue-tests.log'))
        reports = sorted(clean.glob('*-ue-report/index.json'))
        assert len(ue_logs) == len(reports) == 2
        native_build_logs = list((clean / 'logs').glob('*-build.log'))
        native_build_logs = [p for p in native_build_logs if not p.name.endswith('-ue-build.log')]
        assert len(native_build_logs) == 1
        row = {'iteration': iteration, 'core': cr, 'symlink_cases': symlinks, 'native': nr,
               'p05a_cases': p05a, 'dll': dll, 'dll_staged_hashes_match': True,
               'native_build_warnings': [line for line in text(native_build_logs[0]).splitlines() if 'warning' in line.lower()],
               'ubt': {'result': 'Succeeded', 'log': f'clean-{iteration}/logs/{ubt_logs[0].name}',
                       'warnings': [line for line in text(ubt_logs[0]).splitlines() if 'warning' in line.lower()]}, 'unreal': []}
        for log, report in zip(ue_logs, reports):
            result = read_json(report)
            info, data = startup(log)
            backend = 'NullRHI' if '-NullRHI' in data else 'D3D12 hardware'
            assert result['succeeded'] == 12 and result['succeededWithWarnings'] == result['failed'] == result['notRun'] == 0
            assert sorted(t['fullTestPath'] for t in result['tests']) == sorted(expected)
            assert all(t['state'] == 'Success' for t in result['tests'])
            assert info['bridge_ready'] and info['condition_failed_count'] == 14
            assert info['engine_initialization_lines'] and max(info['condition_failed_lines']) < min(info['engine_initialization_lines'])
            assert info['f05_queue_lines'] and max(info['condition_failed_lines']) < min(info['f05_queue_lines'])
            if backend == 'D3D12 hardware':
                assert 'Chosen D3D12 Adapter Id = 0' in data and 'Found D3D12 adapter 0: NVIDIA GeForce RTX 4070 Laptop GPU' in data
                assert 'RHI D3D12 with Feature Level SM5 is supported and will be used' in data
            row['unreal'].append({'backend': backend, 'succeeded': 12, 'succeeded_with_warnings': 0, 'failed': 0, 'not_run': 0,
                                  'tests': [{'name': t['fullTestPath'], 'state': t['state']} for t in result['tests']],
                                  'report': str(report.relative_to(OUT)).replace('\\', '/'),
                                  'log': str(log.relative_to(OUT)).replace('\\', '/'), 'startup': info})
        assert {u['backend'] for u in row['unreal']} == {'NullRHI', 'D3D12 hardware'}
        summary['runs'].append(row)
    for backend in ('NullRHI', 'Hardware'):
        log = REPO / 'laboratorios/control-v2' / (backend + '-engine.log')
        info, data = startup(log)
        assert info['condition_failed_count'] == 14 and not info['bridge_ready']
        assert "InternalLoadLibrary: 'F05OrdersLab'" not in data
        assert not re.search(r'Cmd: Automation RunTests|Test Started\. Name=', data)
        assert 'Cmd: QUIT_EDITOR' in data and 'LogExit: Exiting.' in data
        assert max(info['condition_failed_lines']) < min(info['engine_initialization_lines'])
        record = next(c for c in state['control'] if c['backend'] == backend)
        assert record['exitCode'] == 0
        summary['engine_only_controls'].append({'backend': backend, 'exit_code': 0, 'no_project_modules': True, 'no_f05_automation': True, **info})
    summary['startup_attribution'] = {
        'scope': 'Engine installation startup, reproduced without any F05 module or automation in both RHIs',
        'exact_assertion_call_site': 'Not determined: installed engine lacks implementation .cpp/PDB; no debugger trace collected',
        'local_header': 'Engine/Source/Runtime/Core/Public/Misc/LowLevelTestAdapter.h:130',
        'header_note': 'CHECK macro emits identical text; this does not prove which CHECK or module emits these 14 lines',
        'errors_suppressed_or_engine_modified': False,
        'acceptance_limit': 'PASS_AUTOMATED with disclosed engine-startup errors; not an error-free engine startup or phase closure'}
    # Only start copying after the independent validation above succeeds.
    DEST.mkdir(parents=True, exist_ok=False)
    (DEST / '.gitattributes').write_text('# Preserve raw runtime evidence bytes; do not rewrite log whitespace.\n* -text -whitespace\n', encoding='ascii')
    (DEST / '.gitignore').write_text('# Selected permanent certification evidence only. No laboratory or binary inclusion.\n!*.log\n!**/CMakeFiles/\n', encoding='ascii')
    for p in TASK.iterdir():
        if p.is_file() and p.suffix in ('.json', '.ps1', '.log', '.txt'):
            put(p, Path('execution') / p.name)
    put(REPO / 'desarrollo/integration/f05/run_p05b_msi.ps1', Path('execution/run_p05b_msi.ps1'))
    put(REPO / 'desarrollo/integration/f05/run_f05.ps1', Path('execution/run_f05.ps1'))
    put(REPO / 'desarrollo/integration/f05/run_integration_audit.py', Path('execution/run_integration_audit.py'))
    put(Path(__file__), Path('execution/collect_evidence.py'))
    for name in ('acceptance.json', 'windows.json', 'evidence-sha256.json'):
        put(OUT / name, Path(name))
    for iteration in (1, 2):
        core = OUT / f'core-{iteration}'
        clean = OUT / f'clean-{iteration}'
        for p in core.iterdir():
            if p.is_file(): put(p, p.relative_to(OUT))
        for p in (core / 'build/CMakeFiles').glob('*/CMakeCXXCompiler.cmake'):
            put(p, p.relative_to(OUT))
        for name in ('Testing/Temporary/LastTest.log', 'Testing/Temporary/CTestCostData.txt'):
            p = core / 'build' / name
            if p.exists(): put(p, p.relative_to(OUT))
        for p in clean.glob('*-native.xml'): put(p, p.relative_to(OUT))
        for p in (clean / 'logs').iterdir():
            if p.is_file(): put(p, p.relative_to(OUT))
        for p in (clean / 'native/CMakeFiles').glob('*/CMakeCXXCompiler.cmake'):
            put(p, p.relative_to(OUT))
        p = clean / 'native/Testing/Temporary/LastTest.log'
        put(p, p.relative_to(OUT))
        for report in clean.glob('*-ue-report'):
            for p in report.rglob('*'):
                if p.is_file(): put(p, p.relative_to(OUT))
        for p in (clean / 'ue/Saved/Logs').glob('*.log'):
            put(p, Path(f'clean-{iteration}/editor-logs') / p.name)
    for folder in ('control', 'control-v2'):
        for p in (REPO / 'laboratorios' / folder).iterdir():
            if p.is_file(): put(p, Path('engine-only') / folder / p.name)
    # Preserve the initial configuration failure separately; it is not one of
    # the two accepted repetitions and its Core result is not double-counted.
    initial = REPO / 'laboratorios/o'
    for relative in ('acceptance.json', 'core-1/run.json', 'core-1/tests.xml', 'core-1/tests.log'):
        put(initial / relative, Path('initial-incomplete') / relative)
    for p in (initial / 'clean-1/logs').glob('*-configure.log'):
        put(p, Path('initial-incomplete/clean-1/logs') / p.name)
    # Retain the already-successful narrow elevated run separately; no new execution.
    prior = TASK.parent / 'symlink-uac-20261105'
    for p in prior.rglob('*'):
        if p.is_file(): put(p, Path('prior-symlink-3-of-3') / p.relative_to(prior))
    header = Path('C:/Program Files/Epic Games/UE_5.8/Engine/Source/Runtime/Core/Public/Misc/LowLevelTestAdapter.h')
    summary['startup_attribution']['local_header_sha256'] = digest(header)
    (DEST / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    manifest = [{'path': p.relative_to(DEST).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in sorted(DEST.rglob('*')) if p.is_file()]
    (DEST / 'SHA256SUMS.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(manifest), 'bytes': sum(f['bytes'] for f in manifest), 'destination': str(DEST), 'status': summary['status']}))

if __name__ == '__main__':
    main()
