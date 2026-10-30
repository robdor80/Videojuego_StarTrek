"""Collect executed F03 results; raw evidence remains external, publication is sanitized."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--root', type=Path, required=True)
p.add_argument('--core', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
root, core, out = a.root.resolve(), a.core.resolve(), a.output.resolve()
repo = Path(__file__).resolve().parents[3]
if out.exists():
    raise SystemExit('Refusing to replace an existing collection; use a new output path')
if repo in out.parents or core in out.parents:
    raise SystemExit('Collection must remain external to both source checkouts')
out.mkdir(parents=True)
small = out / 'review'
small.mkdir()
def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True, encoding='utf-8').strip()
def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest() if hasattr(hashlib, 'file_digest') else hashlib.sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def scrub(text):
    for old, replacement in [(os.environ.get('USERPROFILE', ''), '<USERPROFILE>'),
                             (os.environ.get('COMPUTERNAME', ''), '<MSI>')]:
        if old:
            for candidate in {old, old.replace('\\', '/'), old.replace('\\', '\\\\')}:
                text = text.replace(candidate, replacement)
    # Auth payloads must never become published evidence.
    text = re.sub(r'(?i)(authorization\s*[:=]\s*bearer\s+)\S+', r'\1<REDACTED>', text)
    return text
def junit(path):
    tree = ET.parse(path).getroot()
    cases = list(tree.iter('testcase'))
    failures = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
    skipped = sum(c.find('skipped') is not None or c.get('status') == 'notrun' for c in cases)
    return dict(total=len(cases), passed=len(cases)-failures-skipped, failed=failures, skipped=skipped)

native = sorted(root.glob('*-native.xml'))[-1]
ue = sorted(root.glob('*-ue-report/index.json'))[-1]
f02native = sorted((root / 'f02-regression').glob('*-native-tests.xml'))[-1]
f02ue = sorted((root / 'f02-regression').glob('*-ue-report/index.json'))[-1]
core_xml = root / 'evidence/core-tests-golden.xml'
unreal = json.loads(ue.read_text(encoding='utf-8-sig'))
results = dict(date_utc=datetime.now(timezone.utc).isoformat(),
    star_trek_source_commit=git(repo, 'rev-parse', 'HEAD'),
    star_trek_base='9b33f32caab21ce0eb1ecb74cd38739b45d2f035',
    core_commit=git(core, 'rev-parse', 'HEAD'),
    core_base='4f282863737bcd8f5add401202a9e1064c133672',
    native=junit(native), core=junit(core_xml), f02_native=junit(f02native),
    unreal={k: unreal[k] for k in ['succeeded', 'succeededWithWarnings', 'failed', 'notRun']},
    unreal_report_source=str(ue.relative_to(root)),
    scope='CORE_INTEGRADO in isolated branches only; Core PR dependency not merged; F03 not closed')
if results['native'] != dict(total=25, passed=25, failed=0, skipped=0):
    raise SystemExit('Native suite does not contain 25 executed successes')
if results['unreal'] != dict(succeeded=12, succeededWithWarnings=0, failed=0, notRun=0):
    raise SystemExit('Unreal suite did not pass all 12 tests without test warnings')
if results['core'] != dict(total=451, passed=447, failed=0, skipped=4):
    raise SystemExit('Core counts differ; inspect the actual suite before collecting')
write(small / 'results.json', results)
for name, source in [('native-tests.xml', native), ('core-tests.xml', core_xml),
                     ('f02-native-tests.xml', f02native), ('unreal-tests.json', ue),
                     ('f02-unreal-tests.json', f02ue),
                     ('core-timeline-debug.xml', root / 'evidence/core-timeline-debug-final.xml'),
                     ('core-timeline-allocation-debug.xml', root / 'evidence/core-timeline-allocation-debug-final.xml'),
                     ('original-files-verification.json', root / 'evidence/originals/original_files_verification.json')]:
    (small / name).write_text(scrub(source.read_text(encoding='utf-8-sig')), encoding='utf-8')
sources = []
for label, source_root, prefix in [('StarTrek', repo, 'desarrollo/integration/'), ('CoreRPG', core, '')]:
    for name in git(source_root, 'ls-files').splitlines():
        if label == 'StarTrek' and not name.startswith(prefix):
            continue
        if label == 'CoreRPG' and not name.startswith(('include/', 'src/', 'tests/', 'CMakeLists.txt')):
            continue
        path = source_root / name
        sources.append(dict(repository=label, path=name, bytes=path.stat().st_size, sha256=sha(path)))
write(small / 'source-manifest.json', sources)
staged = []
for source in (root / 'ue/Source').rglob('*'):
    if source.is_file():
        staged.append(dict(path=source.relative_to(root / 'ue').as_posix(), bytes=source.stat().st_size, sha256=sha(source)))
for source in (root / 'ue/ThirdParty/include').glob('*'):
    staged.append(dict(path=source.relative_to(root / 'ue').as_posix(), bytes=source.stat().st_size, sha256=sha(source)))
write(small / 'staged-source-manifest.json', staged)

# Large evidence: all dated build/test logs and reports, including failed attempts.
logs = sorted(set(root.glob('evidence/logs/*.log')) | set(root.glob('logs/*.log')) |
              set(root.glob('f02-regression/logs/*.log')) | set(root.glob('*-ue-report/index.json')))
with zipfile.ZipFile(out / 'F03-logs-and-results.zip', 'x', zipfile.ZIP_DEFLATED) as z:
    for source in logs:
        z.writestr(source.relative_to(root).as_posix(), scrub(source.read_text(encoding='utf-8-sig', errors='replace')))
    for source in small.iterdir():
        z.write(source, 'review/' + source.name)
    for source in (root / 'ue/Saved/F03Evidence').glob('*.f03'):
        z.write(source, 'saves/' + source.name)
    z.write(root / 'native/process-campaign.f03', 'saves/process-campaign.f03')

# Own binaries only, no engine binaries, PDBs, Intermediate or artistic assets.
compiled = list((root / 'native/Release').glob('*.dll')) + list((root / 'native/Release').glob('*.lib'))
compiled += [root / 'native/Release/f03_tests.exe']
compiled += list((root / 'ue/Binaries/Win64').glob('*.dll'))
compiled += list((root / 'ue/ThirdParty/Win64').glob('*.lib'))
with zipfile.ZipFile(out / 'F03-own-binaries.zip', 'x', zipfile.ZIP_DEFLATED) as z:
    for source in compiled:
        z.write(source, source.relative_to(root).as_posix())

index = []
for source in sorted(out.glob('*.zip')):
    with zipfile.ZipFile(source) as z:
        members = [dict(name=i.filename, bytes=i.file_size) for i in z.infolist()]
    index.append(dict(name=source.name, location=str(source), bytes=source.stat().st_size,
        sha256=sha(source), date_utc=results['date_utc'], publication_status='LOCAL_ONLY_PENDING_UPLOAD',
        description='Sanitized build/test logs, failures and saves' if 'logs' in source.name else 'Own Win64 lab binaries, no UE engine or art', members=members))
write(out / 'external-evidence-index.json', index)
print(json.dumps(results, ensure_ascii=False, indent=2))
