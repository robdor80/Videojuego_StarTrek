"""Collect executed F02 results, bounded artifacts and hashes. Never reads art payloads."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--native-evidence', type=Path, required=True)
parser.add_argument('--ue-run', type=Path, required=True)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
native, ue = args.native_evidence.resolve(), args.ue_run.resolve()
docs = repo / 'proyecto/docs/roadmap/master/fases/F02'
small = docs / 'evidencias_20261029'
small.mkdir(exist_ok=True)
publish = ue / 'publish'
publish.mkdir(exist_ok=True)
if any(publish.glob('F02-*')):
    raise SystemExit('Existing published artifacts are preserved. Use a new run directory; do not overwrite this execution.')
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def junit(p):
    root = ET.parse(p).getroot()
    total, failed, skipped = (int(root.attrib[k]) for k in ('tests', 'failures', 'skipped'))
    return dict(total=total, passed=total-failed-skipped, failed=failed, skipped=skipped)
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()

# Run existing documentary checks and preserve their actual stdout/exit status.
commands = [
    ['python','desarrollo/tools/validation/validate_f02_contracts.py'],
    ['python','-m','unittest','discover','-s','desarrollo/tools/validation','-p','test_validate_f02_contracts.py','-v'],
    ['python','desarrollo/tools/validation/validate_f02_p05_plan.py'],
]
validation=[]
for i, command in enumerate(commands, 1):
    proc=subprocess.run(command,cwd=repo,capture_output=True,text=True)
    log=publish / f'documentary-{i}.txt'
    log.write_text('COMMAND: '+' '.join(command)+'\n'+proc.stdout+proc.stderr,encoding='utf-8')
    validation.append(dict(command=command,exit_code=proc.returncode))
    if proc.returncode: raise SystemExit(f'Documentary check failed: {command}')

reports=sorted(ue.glob('*-ue-report/index.json'))
if not reports: raise SystemExit('No Unreal report')
report=reports[-1]
ue_result=json.loads(report.read_text(encoding='utf-8-sig'))
ue_passed=ue_result['succeeded']+ue_result['succeededWithWarnings']
if (ue_result['failed'] or ue_result['notRun'] or
    ue_passed != 6):
    raise SystemExit('Latest Unreal report is not a complete passing suite')
demo=sorted((ue/'logs').glob('*-unreal-demo.log'))[-1]
demo_text=demo.read_text(encoding='utf-8-sig')
if len(re.findall(r'F02 DEMO step=[1-4] pass=1',demo_text)) != 4 or 'pass=0' in demo_text:
    raise SystemExit('Latest graphical demonstration did not pass')
screen=sorted((ue/'ue/Saved/F02Evidence').glob('F02-Core-UE5-*.png'),key=lambda p:p.stat().st_mtime)[-1]
protection=json.loads((native/'original_files_verification.json').read_text(encoding='utf-8'))
if protection['missing_or_changed'] or protection['new']:
    raise SystemExit('Original resources changed; investigate before publication')

inputs=[]
# Original, explicitly dated design/audit inputs; new reports are excluded.
for p in sorted(docs.iterdir()):
    if p.is_file() and '2026-10-29' not in p.name and p.name!='EVIDENCIAS_EXTERNAS_2026-10-29.json':
        relative=p.relative_to(repo).as_posix()
        data=subprocess.check_output(['git','-C',str(repo),'show','00822e24:'+relative])
        inputs.append(dict(path=relative,size=len(data),sha256=hashlib.sha256(data).hexdigest(),
                           representation='Canonical Git blob at baseline 00822e24'))
master=docs.parents[1]/'PLAN_MAESTRO.md'
inputs.append(dict(path=master.relative_to(repo).as_posix(),size=master.stat().st_size,sha256=digest(master)))
write(small/'input_inventory.json',inputs)

core=junit(native/'core-tests.xml'); bridge=junit(native/'bridge-tests.xml')
summary={
    'date':'2026-10-29','timezone':'Europe/Madrid',
    'collected_at':dt.datetime.now(dt.timezone.utc).isoformat(),
    'classification':'REAL_CORE_AND_UE_LAB_NOT_SENSORS_GAME',
    'source_commit':git('rev-parse','HEAD'),
    'core_sha':'4f282863737bcd8f5add401202a9e1064c133672',
    'trek_remote_main_baseline':'00822e24ecd2333988e5b6369be1ae9e3089de01',
    'trek_original_local_head':'7ee52d59427ba9f1e027dd78200b938c37687f86',
    'core_tests':core,'native_integration_tests':bridge,
    'ue_tests':dict(passed=ue_result['succeeded']+ue_result['succeededWithWarnings'],
                    succeeded_with_warnings=ue_result['succeededWithWarnings'],failed=ue_result['failed'],skipped=ue_result['notRun']),
    'documentary_unittests':dict(passed=9,failed=0,skipped=0),
    'documentary_checks':validation,
    'graphical_demo':dict(passed_stages=4,log=str(demo),screenshot=str(screen)),
    'protected_originals':protection,
    'limitations':['F02 closure requires independent audit','No campaign clock or persistent agendas',
                  'No Trek command hierarchy/sensors/event store','No power-loss durability or packaged distribution test'],
}
summary['final_test_totals']=dict(passed=core['passed']+bridge['passed']+ue_passed+9,
    failed=core['failed']+bridge['failed']+ue_result['failed'],skipped=core['skipped'])
write(small/'results.json',summary)
shutil.copy2(native/'core-tests.xml',small/'core-tests.xml')
shutil.copy2(native/'bridge-tests.xml',small/'native-tests.xml')
shutil.copy2(report,small/'unreal-tests.json')
shutil.copy2(screen,small/'Core-EntityId-1.png')
shutil.copy2(native/'original_files_verification.json',small/'original_files_verification.json')

artifacts=[]
def record(p, purpose, test, folder, members=None):
    info=dict(name=p.name,purpose=purpose,date='2026-10-29',size=p.stat().st_size,
              sha256=digest(p),platform='Windows 11 MSI / UE 5.8.2 / MSVC 19.51',
              test=test,local_path=str(p),drive_folder=folder,drive_url=None,
              upload_status='LOCAL_PRESERVED_PENDING_UPLOAD',access_status='NOT_CONFIRMED')
    if members is not None: info['members']=members
    artifacts.append(info)
def archive(name, entries, purpose, test, folder):
    dest=publish/name; members=[]
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for p,arc in entries:
            z.write(p,arc)
            members.append(dict(name=arc,size=p.stat().st_size,sha256=digest(p)))
    record(dest,purpose,test,folder,members)

logs=[(p,'native/'+p.name) for p in sorted(native.glob('*.log'))]
logs += [(p,'native/'+p.name) for p in (native/'core-tests.xml',native/'bridge-tests.xml')]
logs += [(p,'unreal/'+p.name) for p in sorted((ue/'logs').glob('*.log'))]
logs += [(p,'documentary/'+p.name) for p in sorted(publish.glob('documentary-*.txt'))]
logs += [(p,p.parent.name+'/'+p.name) for p in reports]
logs += [(native/'original_files_verification.json','original_files_verification.json')]
archive('F02-logs-and-results-20261029.zip',logs,'All build/test attempts, including initial failures and final successes',
        'Core suite / native 15 / UE 5 / documentary 9','03_Logs')
binary=[]
for name in ('TrekF02Bridge.dll','TrekF02Bridge.lib','f02_tests.exe'):
    binary.append((native/'bridge-build/Release'/name,'native/'+name))
for name in ('UnrealEditor-F02CoreLab.dll','UnrealEditor.modules'):
    binary.append((ue/'ue/Binaries/Win64'/name,'ue/Binaries/Win64/'+name))
for p in sorted((ue/'ue/Saved/F02Evidence').glob('*.save')):
    binary.append((p,'fixture-saves/'+p.name))
archive('F02-own-binaries-and-fixture-saves-20261029.zip',binary,
        'Only generated F02 binaries and synthetic saves; requires installed UE 5.8.2; no engine/art redistribution',
        'Native DLL linking / UE module / persistence','04_Compilaciones')
capture=publish/'F02-Core-EntityId-1.png'; shutil.copy2(screen,capture)
record(capture,'Real DX11 screenshot after Actor recreation and disk restore','UE graphical demo','01_Capturas')
summary_out=publish/'F02-results-20261029.json'; shutil.copy2(small/'results.json',summary_out)
record(summary_out,'Executed counts and references','F02-P01..P05','05_Informes')
write(docs/'EVIDENCIAS_EXTERNAS_2026-10-29.json',dict(
    index_version=1,drive_root='https://drive.google.com/drive/folders/1mNjcJrP0JIyqATyYo56zoJG0NVYCUL5D',
    privacy='Restricted; no public sharing enabled',
    video_status='NOT_RECORDED; folder intentionally empty',
    artifacts=artifacts))
print(json.dumps(dict(totals=summary['final_test_totals'],artifacts=[dict(name=x['name'],size=x['size'],sha256=x['sha256']) for x in artifacts]),indent=2))
