"""Collect actual bridge projections and test reports; never edits a campaign in play."""
import argparse
import ctypes as C
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--build-root', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--roster', type=Path, required=True)
args = parser.parse_args()
root = args.build_root.resolve()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
repo = Path(__file__).resolve().parents[3]
U = C.c_uint64
W = C.c_uint32

class Ref(C.Structure):
    _fields_ = [('scope', U), ('id', U)]

class Population(C.Structure):
    _fields_ = [(k, U) for k in 'ship_identity seed crew residents passengers maximum'.split()]

class Stats(C.Structure):
    _fields_ = [(k, U) for k in 'entities revision now crew civilians passengers slots vacancies commander pending events pattern alert'.split()]

class Request(C.Structure):
    _fields_ = [('actor', Ref), ('revision', U), ('op', W), ('value', W)] + [(k, U) for k in 'target aux start end cause'.split()]

class Result(C.Structure):
    _fields_ = [('code', W), ('reserved', W), ('record', U), ('revision', U)]

class Position(C.Structure):
    _fields_ = [(k, U) for k in 'id stable_id department section ordinal person qualification qualification_mask responsibility stations coverage alpha duty_record'.split()] + [('on_duty', W), ('at_station', W)]

class Section(C.Structure):
    _fields_ = [(k, U) for k in 'id department total alpha qualification stations coverage'.split()] + [(k, C.c_char_p) for k in ['name', 'responsibilities', 'equipment']]

class Organization(C.Structure):
    _fields_ = [(k, U) for k in 'template_id departments sections positions assigned vacant on_duty alpha_expected alpha_present alpha_deficit continuous_candidates continuous_required continuous_covered urgent_response'.split()] + [('coverage_validated', W), ('reserved', W)]

def row(value):
    return {k: (getattr(value, k).decode('utf-8') if isinstance(getattr(value, k), bytes) else getattr(value, k)) for k, _ in value._fields_}

dll_path = root / 'native/Release/TrekF04Bridge.dll'
lib = C.CDLL(str(dll_path))
P = C.c_void_p
lib.f04_create_population.argtypes = [W, C.c_char_p, C.POINTER(Population), C.POINTER(P)]
lib.f04_stats.argtypes = [P, C.POINTER(Stats)]
lib.f04_execute.argtypes = [P, C.POINTER(Request), C.POINTER(Result)]
lib.f04_advance.argtypes = [P, U, U, C.POINTER(U)]
lib.f04_positions_page.argtypes = [P, Ref, U, C.POINTER(Position), U, C.POINTER(U), C.POINTER(U)]
lib.f04_template_sections.argtypes = [U, C.POINTER(Section), U, C.POINTER(U)]
lib.f04_organization_stats.argtypes = [P, Ref, C.POINTER(Organization)]
lib.f04_destroy.argtypes = [P]
lib.f04_core_sha.restype = C.c_char_p

def ok(code):
    if code != 0:
        raise RuntimeError(f'Bridge returned {code}')

session = P()
ok(lib.f04_create_population(1, b'intrepid', C.byref(Population(66001, 404, 160, 0, 0, 0)), C.byref(session)))
try:
    # Fresh trusted fixture: each new session consumes a scope, first here is 1.
    # Obtain it from the existing handles ABI instead of assuming it.
    class Handles(C.Structure):
        _fields_ = [(k, Ref) for k in 'ship captain head ensign watch doctor relief civilian passenger admiral'.split()] + [(k, U) for k in 'sensors engineering bridge'.split()]
    lib.f04_handles.argtypes = [P, C.POINTER(Handles)]
    handles = Handles()
    ok(lib.f04_handles(session, C.byref(handles)))
    observer = handles.captain
    def op(kind, aux=0, start=0, end=0, value=0):
        stats = Stats()
        ok(lib.f04_stats(session, C.byref(stats)))
        result = Result()
        ok(lib.f04_execute(session, C.byref(Request(observer, stats.revision, kind, value, 0, aux, start, end, 40401)), C.byref(result)))
    op(25, aux=8191, value=2)  # INSTALL_TEMPLATE, additive ABI 1
    op(26)                   # BOOTSTRAP_TEMPLATE, explicit synthetic fixture
    op(30, aux=1, start=28800, end=57600)  # PLAN_ALPHA
    processed = U()
    ok(lib.f04_advance(session, 28800, 4096, C.byref(processed)))
    organization = Organization()
    ok(lib.f04_organization_stats(session, observer, C.byref(organization)))
    positions, written, total = (Position * 160)(), U(), U()
    ok(lib.f04_positions_page(session, observer, 0, positions, 160, C.byref(written), C.byref(total)))
    sections, count = (Section * 34)(), U()
    ok(lib.f04_template_sections(2, sections, 34, C.byref(count)))
    assert written.value == total.value == 160 and count.value == 34
    data = [row(p) for p in positions]
    assert len({p['person'] for p in data}) == 160
    assert len({p['person'] for p in data if p['on_duty']}) == 64
    snapshot = {'synthetic_fixture': True, 'ship_identity': 66001, 'core_sha': lib.f04_core_sha().decode(), 'organization': row(organization), 'sections': [row(s) for s in sections], 'positions': data}
finally:
    ok(lib.f04_destroy(session))

departments = {3: 'Mando y navegación', 2: 'Ingeniería y mantenimiento', 1: 'Ciencias y sensores', 5: 'Operaciones y comunicaciones', 6: 'Seguridad y táctica', 7: 'Lanzaderas y logística', 4: 'Medicina'}
document = ['# F04-INTREPID-01 — Plantilla de 160 plazas', '',
            'Generada desde las consultas de la DLL validada. Clave: `perfil:sección*100+ordinal`, dentro de la nave. Son plazas, sin nombres, biografías ni rangos inventados. Alpha: 08:00–16:00.', '',
            '| Departamento | Total | Alpha |', '|---|---:|---:|']
for dept, label in departments.items():
    selected = [p for p in data if p['department'] == dept]
    document.append(f'| {label} | {len(selected)} | {sum(p["alpha"] for p in selected)} |')
document += ['| **Total** | **160** | **64** |', '', '| Sección | Departamento ABI | Total | Alpha | Función | Equipamiento lógico |', '|---|---:|---:|---:|---|---|']
for s in snapshot['sections']:
    document.append(f'| {s["id"]}. {s["name"]} | {s["department"]} | {s["total"]} | {s["alpha"]} | {s["responsibilities"]} | {s["equipment"]} |')
document += ['', '| Clave estable | Departamento | Sección / ordinal | Cualificaciones (máscara) | Responsabilidad ABI | Alpha |', '|---|---|---|---|---|---|']
for p in data:
    document.append(f'| 2:{p["stable_id"]} | {departments[p["department"]]} | {p["section"]} / {p["ordinal"]} | {p["qualification_mask"]} | {p["responsibility"] or "—"} | {"Sí" if p["alpha"] else "—"} |')
document += ['', 'Las máscaras usan los IDs de F04Dept/F04Qualification de `f04_bridge.h`. Las responsabilidades son nombramientos separados: CAPTAIN=1, HEAD=2, DOCTOR=4, FIRST=5 y DEPUTY=8; WATCH=3 se programa por ventana. No son rangos. Las referencias funcionales no representan 160 consolas físicas.', '', 'Véase [organización y límites](F04-INTREPID-01_ORGANIZACION.md).', '']
args.roster.write_text('\n'.join(document), encoding='utf-8')
(out / 'alpha-snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding='utf-8')

def sanitize(text):
    return re.sub(r'C:[/\\]Users[/\\][^/\\\s<>";]+', '<USER_HOME>', text, flags=re.I)

summary = {'core_sha': snapshot['core_sha'], 'dll_sha256': hashlib.sha256(dll_path.read_bytes()).hexdigest(), 'native': {}}
for name, filename in [('f04', 'native.xml'), ('f02', 'f02.xml'), ('f03', 'f03.xml'), ('core', 'core.xml')]:
    source = root / 'evidence' / filename
    cases = ET.fromstring(source.read_bytes()).findall('.//testcase')
    failures = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
    skipped = [c.attrib['name'] for c in cases if c.find('skipped') is not None]
    summary['native'][name] = {'defined': len(cases), 'passed': len(cases)-failures-len(skipped), 'failed': failures, 'skipped': skipped}
    (out / (name+'.xml')).write_text(sanitize(source.read_text(encoding='utf-8')), encoding='utf-8')
reports = sorted(root.glob('*-ue-report/index.json'))
report = json.loads(reports[-1].read_text(encoding='utf-8-sig'))
summary['unreal'] = {k: report[k] for k in ['succeeded', 'succeededWithWarnings', 'failed', 'notRun']}
(out / 'unreal.json').write_text(json.dumps({'summary': summary['unreal'], 'tests': [{k: t[k] for k in ['fullTestPath', 'state', 'warnings', 'errors']} for t in report['tests']]}, indent=2), encoding='utf-8')
for name in ['f04-reference', 'miranda-reference', 'f03-reference', 'f02-reference', 'f04-fixture', 'roadmap']:
    (out / (name+'.txt')).write_text(sanitize((root/'evidence'/(name+'.log')).read_text(encoding='utf-8', errors='replace')), encoding='utf-8')
contract = json.loads((Path(__file__).parent/'tests/fixtures/intrepid_facilities_contract.json').read_text(encoding='utf-8'))
assert contract['clock'] == 'CoreRPG.Timeline' and not contract['runtime_reservations_implemented']
assert all((repo/path).is_file() for path in contract['references'].values())
facilities = contract['reference_configuration']['facilities']
assert len(facilities) == len({f['id'] for f in facilities}) == 2
assert all(f['availability'] == 'unavailable' and f['capacity'] is None and not f['occupant_refs'] for f in facilities)
summary['facilities_contract'] = 'JSON parsed; references and safe unconfigured defaults checked; runtime not implemented'
(out / 'results.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
