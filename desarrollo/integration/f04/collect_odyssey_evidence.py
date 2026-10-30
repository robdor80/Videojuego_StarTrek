"""Export a fresh synthetic fixture from the built DLL; never author a live save.

The TSV oracle is the independently transcribed approved user table. Runtime
plazas, duties, gaps, identities and coverage are queried from Core projections.
"""
import argparse
import csv
import ctypes as C
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

U, W, P = C.c_uint64, C.c_uint32, C.c_void_p


def struct(name, fields, tail=()):
    return type(name, (C.Structure,), {'_fields_': [(k, U) for k in fields.split()] + list(tail)})


Ref = struct('Ref', 'scope id')
Population = struct('Population', 'ship_identity seed crew residents passengers maximum')
Stats = struct('Stats', 'entities revision now crew civilians passengers slots vacancies commander pending events pattern alert')
Handles = type('Handles', (C.Structure,), {'_fields_': [(k, Ref) for k in 'ship captain head ensign watch doctor relief civilian passenger admiral'.split()] + [(k, U) for k in 'sensors engineering bridge'.split()]})
Request = type('Request', (C.Structure,), {'_fields_': [('actor', Ref), ('revision', U), ('op', W), ('value', W)] + [(k, U) for k in 'target aux start end cause'.split()]})
Result = type('Result', (C.Structure,), {'_fields_': [('code', W), ('reserved', W), ('record', U), ('revision', U)]})
Position = struct('Position', 'id stable_id department section ordinal person qualification qualification_mask responsibility stations coverage alpha duty_record', [('on_duty', W), ('at_station', W)])
Section = struct('Section', 'id department total alpha qualification stations coverage', [(k, C.c_char_p) for k in ['name', 'responsibilities', 'equipment']])
Duty = struct('Duty', 'id person slot start end stopped_at plan cause', [(k, W) for k in 'ordinary temporary state reserved'.split()])
Gap = struct('Gap', 'id start end department station missing plan')
Person = struct('Person', 'id category rank department', [(k, W) for k in 'available on_duty localized at_console'.split()])
Candidate = struct('Candidate', 'person nominal_slot')
Coverage = struct('Coverage', 'station start end first_gap person', [('covered', W), ('reserved', W)])
DEPARTMENTS = {3: 'Mando y navegación', 2: 'Ingeniería y mantenimiento', 1: 'Ciencias y sensores', 5: 'Operaciones y comunicaciones', 6: 'Seguridad y táctica', 7: 'Lanzaderas y logística', 4: 'Medicina'}


def row(s):
    return {k: (v.decode('utf-8') if isinstance(v, bytes) else v) for k, _ in s._fields_ if (v := getattr(s, k)) is not None}


def ok(code):
    assert code == 0, f'F04 code {code}'


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--build-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--roster', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    repo = Path(__file__).resolve().parents[3]
    dll = args.build_root / 'native/Release/TrekF04Bridge.dll'
    lib = C.CDLL(str(dll.resolve()))
    signatures = {
        'f04_create_population': [W, C.c_char_p, C.POINTER(Population), C.POINTER(P)],
        'f04_handles': [P, C.POINTER(Handles)], 'f04_stats': [P, C.POINTER(Stats)],
        'f04_execute': [P, C.POINTER(Request), C.POINTER(Result)],
        'f04_destroy': [P], 'f04_advance': [P, U, U, C.POINTER(U)],
        'f04_positions_page': [P, Ref, U, C.POINTER(Position), U, C.POINTER(U), C.POINTER(U)],
        'f04_template_sections': [U, C.POINTER(Section), U, C.POINTER(U)],
        'f04_duties_page': [P, Ref, U, C.POINTER(Duty), U, C.POINTER(U), C.POINTER(U)],
        'f04_roster_gaps_page': [P, Ref, U, C.POINTER(Gap), U, C.POINTER(U), C.POINTER(U)],
        'f04_service_coverage': [P, Ref, U, U, C.POINTER(Coverage), U, C.POINTER(U)],
        'f04_manifest': [P, Ref, C.POINTER(Person), U, C.POINTER(U)],
        'f04_relief_candidates_page': [P, Ref, U, U, U, U, C.POINTER(Candidate), U, C.POINTER(U), C.POINTER(U)],
        'f04_save': [P, P, U, C.POINTER(U)], 'f04_load': [P, P, U]
    }
    for name, signature in signatures.items():
        getattr(lib, name).argtypes = signature
    lib.f04_core_sha.restype = C.c_char_p

    def dump(name, data):
        (args.output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    summaries, timings = [], []
    for days in [1, 7, 14, 28]:
        session = P()
        begin = time.perf_counter()
        ok(lib.f04_create_population(1, b'odyssey', C.byref(Population(67001, 404, 1600, 0, 0, 0)), C.byref(session)))
        people_created = time.perf_counter()
        handles = Handles()
        ok(lib.f04_handles(session, C.byref(handles)))
        observer = Ref(handles.ship.scope, 3)

        def op(kind, aux=0, start=0, end=0, value=0, target=0):
            stats, result = Stats(), Result()
            ok(lib.f04_stats(session, C.byref(stats)))
            ok(lib.f04_execute(session, C.byref(Request(Ref(observer.scope, stats.commander), stats.revision, kind, value, target, aux, start, end, 40401)), C.byref(result)))

        def page(name, cls):
            n, total = U(), U()
            ok(getattr(lib, name)(session, observer, 0, None, 0, C.byref(n), C.byref(total)))
            result = (cls * total.value)()
            ok(getattr(lib, name)(session, observer, 0, result, total, C.byref(n), C.byref(total)))
            assert n.value == total.value
            return [row(x) for x in result]

        try:
            op(25, aux=8191, value=4)
            positions_created = time.perf_counter()
            op(26)
            created = time.perf_counter()
            manifest, manifest_count = (Person * 1600)(), U()
            ok(lib.f04_manifest(session, observer, manifest, 1600, C.byref(manifest_count)))
            assert manifest_count.value == 1600
            manifested = time.perf_counter()
            op(31, aux=0 if days == 1 else 1, end=days * 86400, value=1 if days == 1 else 2)
            planned = time.perf_counter()
            coverage, n = (Coverage * 8)(), U()
            ok(lib.f04_service_coverage(session, observer, 0, days * 86400, coverage, 8, C.byref(n)))
            assert n.value == 8 and all(c.covered and c.first_gap == c.end for c in coverage)
            covered = time.perf_counter()
            duties, gaps = page('f04_duties_page', Duty), page('f04_roster_gaps_page', Gap)
            people = defaultdict(list)
            for d in duties:
                people[d['person']].append(d)
            max7, min_gap, changing = 0, days * 86400, 0
            for person, work in people.items():
                work.sort(key=lambda d: d['start'])
                assert len({d['start'] // 86400 for d in work}) == len(work)
                changing += len({d['start'] % 86400 for d in work}) > 1
                for i, d in enumerate(work):
                    rolling = sum(0 <= d['start'] - a['start'] < 7 * 86400 for a in work)
                    max7 = max(max7, rolling)
                    if i:
                        min_gap = min(min_gap, d['start'] - work[i-1]['end'])
            assert max7 <= 5 and (days == 1 or min_gap >= 43200)
            summary = {'days': days, 'shifts': len(duties), 'target_shifts': 1035 * days,
                       'quota_missing': sum(g['missing'] for g in gaps if not g['station']),
                       'critical_gap_records': sum(bool(g['station']) for g in gaps),
                       'critical_service_windows': 8 * 3 * days, 'critical_coverage': [row(c) for c in coverage],
                       'max_rolling7': max7, 'min_gap_seconds': min_gap if days > 1 else None,
                       'people_changing_watch': changing, 'person_days_without_duty': 1600 * days - len(duties),
                       'captain_shifts': len(people[3]), 'gaps_by_department': dict(Counter({dept: sum(g['missing'] for g in gaps if not g['station'] and g['department'] == dept) for dept in DEPARTMENTS}))}
            state = Stats();ok(lib.f04_stats(session, C.byref(state)))
            summary['core_entities_after_plan'] = state.entities
            windows = []
            for index in range(days * 3):
                checks, count = (Coverage * 8)(), U()
                ok(lib.f04_service_coverage(session, observer, index * 28800, (index+1) * 28800, checks, 8, C.byref(count)))
                assert count.value == 8 and all(c.covered and c.first_gap == c.end for c in checks)
                windows.extend(row(c) for c in checks)
            summary['critical_windows_verified'] = sum(c['covered'] for c in windows)
            dump(f'critical-windows-{days}-days.json', windows)
            summaries.append(summary)
            if days == 1:
                positions = page('f04_positions_page', Position)
                sections, n = (Section * 72)(), U()
                ok(lib.f04_template_sections(4, sections, 72, C.byref(n)))
                sections = [row(s) for s in sections]
                assert len(positions) == len({p['person'] for p in positions}) == len({p['stable_id'] for p in positions}) == 1600
                oracle = [[int(x) for x in line.split()] for line in (Path(__file__).parent / 'tests/fixtures/odyssey_approved.tsv').read_text().splitlines()]
                by_slot = {d['slot']: ['Gamma', 'Alpha', 'Beta'][d['start'] // 28800] for d in duties}
                counts = Counter(by_slot.values())
                assert counts == {'Alpha': 500, 'Beta': 330, 'Gamma': 205}
                for section, total, a, b, g, off in oracle:
                    members = [p for p in positions if p['section'] == section]
                    got = Counter(by_slot.get(p['id'], 'Fuera') for p in members)
                    assert len(members) == total and [got[k] for k in ['Alpha', 'Beta', 'Gamma', 'Fuera']] == [a, b, g, off]
                document = ['# F04-ODYSSEY-01 — Las 1600 plazas identificadas', '',
                            'Consultas reales de la DLL. Identidad de plaza: nave / perfil 4 / clave estable. Las personas son una fixture sintética explícita; no se inventan nombres, rangos, especies ni biografías.', '',
                            '| Clave | Departamento | Sección | Ordinal | Persona Core | Máscara de competencias | Responsabilidad ABI | Día de referencia |',
                            '|---|---|---:|---:|---:|---:|---:|---|']
                for p in positions:
                    document.append(f'| 4:{p["stable_id"]} | {DEPARTMENTS[p["department"]]} | {p["section"]} | {p["ordinal"]} | {p["person"]} | {p["qualification_mask"]} | {p["responsibility"]} | {by_slot.get(p["id"], "Fuera")} |')
                document += ['', 'Responsabilidades: 1 capitán; 2 jefe; 4 médico jefe; 5 primer oficial; 6 segundo oficial; 8 adjunto; 0 sin nombramiento permanente de jefatura. No representan rangos. WATCH=3 y DUTY_HEAD=9 son nombramientos por ventana, separados de estas plazas.', '', '[Organización y límites](F04-ODYSSEY-01_ORGANIZACION_Y_TRES_GUARDIAS.md).', '']
                args.roster.write_text('\n'.join(document), encoding='utf-8')
                dump('reference-snapshot.json', {'core_sha': lib.f04_core_sha().decode(), 'sections': sections, 'positions': positions, 'duties': duties, 'coverage': [row(c) for c in coverage]})
            if days == 28:
                with (args.output / 'roster-28-days.csv').open('w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=duties[0].keys());writer.writeheader();writer.writerows(duties)
                dump('gaps-28-days.json', gaps)
                dump('daily-counts-28-days.json', [{'day': d, **{label: sum(x['start'] == d * 86400 + index * 28800 for x in duties) for index, label in enumerate(['Gamma', 'Alpha', 'Beta'])}, 'off': 1600 - sum(x['start'] // 86400 == d for x in duties)} for d in range(28)])
            start = time.perf_counter()
            size = U()
            assert lib.f04_save(session, None, 0, C.byref(size)) == 15
            archive = (C.c_uint8 * size.value)()
            ok(lib.f04_save(session, archive, size, C.byref(size)))
            saved = time.perf_counter()
            ok(lib.f04_load(session, archive, size))
            loaded = time.perf_counter()
            processed = U()
            ok(lib.f04_advance(session, days * 86400 - 1, 4096, C.byref(processed)))
            advanced = time.perf_counter()
            timings.append({'days': days, 'create_people_and_positions_ms': (created-begin)*1000,
                            'create_people_ms': (people_created-begin)*1000, 'install_positions_ms': (positions_created-people_created)*1000,
                            'bootstrap_assignments_ms': (created-positions_created)*1000,
                            'manifest_ms': (manifested-created)*1000, 'plan_ms': (planned-manifested)*1000, 'coverage_ms': (covered-planned)*1000,
                            'save_ms': (saved-start)*1000, 'load_ms': (loaded-saved)*1000,
                            'advance_ms': (advanced-loaded)*1000, 'archive_bytes': size.value})
            if days == 1:
                ok(lib.f04_handles(session, C.byref(handles)))
                observer = Ref(handles.ship.scope, 3)
                tick = days * 86400 - 1
                checks, count = (Coverage * 8)(), U()
                ok(lib.f04_service_coverage(session, observer, tick, tick+1, checks, 8, C.byref(count)))
                outgoing = next(c.person for c in checks if c.station == 4)
                target = next(d['id'] for d in duties if d['person'] == outgoing and d['start'] <= tick < d['end'])
                begin_incident = time.perf_counter()
                op(5, start=tick, end=tick+1, value=2, target=outgoing)
                absent = time.perf_counter()
                ok(lib.f04_service_coverage(session, observer, tick, tick+1, checks, 8, C.byref(count)))
                assert not next(c.covered for c in checks if c.station == 4)
                candidates, written, total = (Candidate * 1600)(), U(), U()
                start_search = time.perf_counter()
                ok(lib.f04_relief_candidates_page(session, observer, target, tick, tick+1, 0, candidates, 1600, C.byref(written), C.byref(total)))
                searched = time.perf_counter()
                assert written.value == total.value > 0
                op(32, aux=candidates[0].person, start=tick, end=tick+1, target=target)
                substituted = time.perf_counter()
                ok(lib.f04_service_coverage(session, observer, tick, tick+1, checks, 8, C.byref(count)))
                assert all(c.covered for c in checks)
                state = Stats();ok(lib.f04_stats(session, C.byref(state)));assert state.crew == 1600
                dump('incident-performance.json', {'scenario':'sensor sickness and legitimate temporary cover after load at tick 86399',
                     'absence_ms':(absent-begin_incident)*1000, 'candidate_query_ms':(searched-start_search)*1000,
                     'cover_ms':(substituted-searched)*1000, 'real_candidates':total.value,
                     'outgoing':outgoing,'incoming':candidates[0].person,'crew_after':state.crew,
                     'coverage_restored':all(c.covered for c in checks), 'historical_gaps':page('f04_roster_gaps_page', Gap)})
        finally:
            ok(lib.f04_destroy(session))
    dump('simulations.json', summaries)
    dump('performance.json', timings)
    dump('dll-provenance.json', {'base': subprocess.check_output(['git', 'merge-base', 'HEAD', 'origin/main'], cwd=repo, text=True).strip(), 'core_sha': lib.f04_core_sha().decode(), 'dll_sha256': hashlib.sha256(dll.read_bytes()).hexdigest()})
    contract = json.loads((Path(__file__).parent / 'tests/fixtures/odyssey_facilities_contract.json').read_text())
    inherited = json.loads((repo / contract['contract_ref']).read_text())
    assert contract['clock'] == inherited['clock'] == 'CoreRPG.Timeline'
    assert contract['reference_configuration']['facility_count'] is None and not contract['reference_configuration']['facilities']
    assert not contract['runtime_reservations_implemented'] and not inherited['runtime_reservations_implemented']
    print(json.dumps({'simulations': summaries, 'performance': timings}, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
