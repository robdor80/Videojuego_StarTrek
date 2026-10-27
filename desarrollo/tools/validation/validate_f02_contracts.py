#!/usr/bin/env python3
"""Check F02 documentary provenance. No Core runtime or UE5 tests are run."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REG = Path('proyecto/docs/roadmap/master/fases/F02')


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def resolve(value, dotted_path: str):
    for key in dotted_path.split('.'):
        if not isinstance(value, dict) or key not in value:
            raise KeyError(dotted_path)
        value = value[key]
    return value


def unique(rows, key, label, errors):
    values = [row.get(key) for row in rows]
    if len(values) != len(set(values)) or not all(isinstance(x, str) and x for x in values):
        errors.append(f'{label}: duplicate/empty {key}')


def check(root: Path):
    errors = []
    stats = {'p02_sources': 0, 'p02_selectors': 0, 'p03_adapters': 0,
             'p03_source_paths': 0, 'p03_gaps': 0, 'p04_failures': 0,
             'p04_axes': 0, 'p04_tests': 0}
    try:
        p02 = read_json(root / REG / 'INVENTARIO_INTERCAMBIO_P02.json')
        p03 = read_json(root / REG / 'MAPA_ADAPTADORES_P03.json')
        p04 = read_json(root / REG / 'REGISTRO_FALLOS_COMPATIBILIDAD_P04.json')
    except (OSError, ValueError) as exc:
        return stats, [f'registry missing/invalid: {exc}']

    sources = p02.get('records', [])
    unique(sources, 'id', 'P02', errors)
    unique(sources, 'source_path', 'P02', errors)
    stats['p02_sources'] = len(sources)
    if len(sources) != 24:
        errors.append(f'P02 source count: expected 24, got {len(sources)}')
    for row in sources:
        name = row.get('source_path', '')
        path = root / name
        if not path.is_file():
            errors.append(f'P02 {name}: missing source')
            continue
        raw = path.read_bytes()
        expected = row.get('source_blob_sha')
        if blob_sha(raw) != expected and blob_sha(raw.replace(b'\r\n', b'\n')) != expected:
            errors.append(f'P02 {name}: Git blob SHA drift; re-audit before approving change')
        try:
            data = json.loads(raw)
            if data.get('schema_version') != row.get('source_schema_version'):
                errors.append(f'P02 {name}: schema_version drift')
            for selector in row.get('verified_source_selectors', []):
                stats['p02_selectors'] += 1
                try:
                    resolve(data, selector)
                except KeyError:
                    errors.append(f'P02 {name}: selector missing: {selector}')
        except (UnicodeError, ValueError, AttributeError) as exc:
            errors.append(f'P02 {name}: invalid source JSON: {exc}')
    if stats['p02_selectors'] != 73:
        errors.append(f'P02 selector count: expected 73, got {stats["p02_selectors"]}')

    adapters = p03.get('adapters', [])
    unique(adapters, 'id', 'P03', errors)
    stats['p03_adapters'] = len(adapters)
    if len(adapters) != 12:
        errors.append(f'P03 adapter count: expected 12, got {len(adapters)}')
    paths = {p for a in adapters for p in a.get('verified_source_refs', [])}
    stats['p03_source_paths'] = len(paths)
    for path in sorted(paths):
        if not (root / path).is_file():
            errors.append(f'P03 source path missing: {path}')
    if len(paths) != 19:
        errors.append(f'P03 source paths: expected 19, got {len(paths)}')
    gaps = {g for a in adapters for g in a.get('gap_refs', [])}
    stats['p03_gaps'] = len(gaps)
    expected_gaps = {f'P03-G{x:02d}' for x in range(1, 12)}
    if gaps != expected_gaps:
        errors.append(f'P03 gap coverage mismatch: {sorted(gaps ^ expected_gaps)}')
    if sum(a.get('first_internal_sensors_slice') == 'MUST' for a in adapters) != 8:
        errors.append('P03: must have eight mandatory first-slice adapters')

    axes = p04.get('compatibility_axes', [])
    decisions = p04.get('compatibility_decisions', [])
    failures = p04.get('failures', [])
    tests = p04.get('tests', [])
    for items, label in [(axes, 'axes'), (decisions, 'decisions'),
                         (failures, 'failures'), (tests, 'tests')]:
        unique(items, 'id', f'P04 {label}', errors)
    stats['p04_axes'] = len(axes)
    stats['p04_failures'] = len(failures)
    stats['p04_tests'] = len(tests)
    if (len(axes), len(decisions), len(failures), len(tests)) != (6, 10, 13, 16):
        errors.append('P04 counts changed: expected 6 axes, 10 decisions, 13 failures, 16 tests')
    test_ids = {t['id'] for t in tests if isinstance(t.get('id'), str)}
    adapter_ids = {a['id'] for a in adapters if isinstance(a.get('id'), str)}
    for failure in failures:
        refs = failure.get('test_refs', [])
        if not refs or any(t not in test_ids for t in refs):
            errors.append(f'P04 {failure.get("id")}: missing/unknown test reference')
    for test in tests:
        if test.get('adapter_ref') not in adapter_ids:
            errors.append(f'P04 {test.get("id")}: unknown adapter')
    for adapter in adapters:
        for ref in adapter.get('acceptance_test_refs', []):
            if ref not in test_ids:
                errors.append(f'P03 {adapter.get("id")}: unknown acceptance test {ref}')
    if set(p04.get('migration_preflight', [])) & set(p04.get('forbidden_shortcuts', [])):
        errors.append('P04: migration steps contradict forbidden shortcuts')
    if p04.get('classification') != 'DESIGN_AND_STATIC_VALIDATION_ONLY':
        errors.append('P04: do not claim an untested runtime policy is implemented')
    try:
        sensor = read_json(root / 'sistemas/gameplay/ship_operations/sensor_resolution/sensor_result_contract.json')
        forbidden = set(sensor.get('forbidden_player_fields', []))
        required = {'authoritative_entity_id', 'ground_truth', 'unrevealed_hidden_properties'}
        if not required.issubset(forbidden):
            errors.append('Sensor result: mandatory anti-leak fields missing')
    except (OSError, ValueError) as exc:
        errors.append(f'Sensor result contract invalid: {exc}')
    return stats, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3],
                        help='Star Trek repository root')
    args = parser.parse_args(argv)
    stats, errors = check(args.root)
    print('F02 static documentary check: ' + ', '.join(f'{k}={v}' for k,v in stats.items()))
    if errors:
        for error in errors:
            print('ERROR:', error, file=sys.stderr)
        return 1
    print('PASS: documentary registries and provenance match; NO Core/UE5/runtime test was run.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
