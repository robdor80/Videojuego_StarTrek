"""Package reproducible authoritative-history evidence; never promote a partial campaign."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET

p=argparse.ArgumentParser(__doc__)
p.add_argument('--build-root',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--allow-incomplete',action='store_true')
a=p.parse_args()
source=Path(__file__).resolve().parent
repo=source.parents[2]
pin=(source/'core-history-revision.txt').read_text().strip()
out=a.output;out.mkdir(parents=True,exist_ok=True)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def dump(name,data):
    path=out/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def copy(path,name=None):
    target=out/(name or path.name);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.startswith('{')]
suites={}
copy(a.build_root/'core-ci.json')
for name,path in {'core':a.build_root/'core-tests.xml','f04':a.build_root/'f04-final.xml','f02':a.build_root/'regressions2/f02.xml','f03':a.build_root/'regressions2/f03.xml'}.items():
    tree=ET.parse(path).getroot();suite=tree if tree.tag=='testsuite' else tree.find('testsuite');assert suite is not None
    assert int(suite.attrib.get('failures',0))==0 and int(suite.attrib.get('errors',0))==0
    suites[name]=dict(suite.attrib);copy(path,name+'.xml')
reports=list((a.build_root/'Unreal').glob('*-ue-report/index.json'))
assert reports
report=max(reports,key=lambda x:x.stat().st_mtime)
ue=json.loads(report.read_text(encoding='utf-8-sig'))
assert ue['failed']==0 and ue['notRun']==0 and ue['succeeded']==26 and ue['succeededWithWarnings']==0
copy(report,'unreal-index.json')
for name in ['core-tests.log','core-final-build.log','f04-final.log','faults-final-tests.log','faults-final-build.log','ue-build.log','ue-tests-final.log','compatibility-final.json','compatibility-final.log','legacy-history2/results.json','legacy-history2.log','fast-oracle-equivalence.json','regressions2/f02-pin-override.json','regressions2/f03-pin-override.json','regressions2/f02-tests.log','regressions2/f03-tests.log','authority-final.log','roadmap-final.log','doc-f04.log','doc-miranda.log','doc-f03.log','doc-f02.log','doc-lore03.log']:
    copy(a.build_root/name,Path(name).as_posix())
copy(Path('C:/Program Files/Epic Games/UE_5.8/Engine/Build/Build.version'),'Unreal-Build.version.json')
assert 'PASS' in (a.build_root/'faults-final-tests.log').read_text()
required={(p,365) for p in range(1,6)}|{(5,730)}
campaigns={}
for root in [a.build_root/'history/history-runs',a.build_root/'oracle730/history-runs',a.build_root/'oracle730-final/history-runs']:
    for acceptance in sorted(root.glob('*/acceptance.json')):
        result=json.loads(acceptance.read_text());key=(result['profile'],result['days'])
        if key not in required:continue
        directory=acceptance.parent;assert result['core_revision']==pin
        assert result['completed']==result['days'] and result['real_watches'] and result['all_blocks_equal_complete_history']
        assert result['maximum_resident']<65536
        audit=rows(directory/'audit.log')[-1]
        assert audit['all_original_block_hashes_equal'] and audit['profile']==key[0] and audit['days']==key[1]
        assert rows(directory/'resume.log')[-1]['future_equal']
        records=rows(directory/'campaign.log');blocks=[r for r in records if r.get('kind')=='block']
        assert blocks[-1]['completed']==key[1] and all(r['oracle_equal'] for r in blocks)
        label=f'{key[0]}-{key[1]}'
        for path in directory.iterdir():
            if path.is_file():copy(path,'campaigns/'+label+'/'+path.name)
        storage=directory/f'campaign-{key[0]}-{key[1]}'
        inventory=[{'name':path.name,'bytes':path.stat().st_size,'sha256':sha(path)} for path in sorted(storage.iterdir()) if path.is_file()]
        for item in inventory:
            if item['name'].endswith('.obj'):assert item['name'][:-4]==item['sha256']
        dump('campaigns/'+label+'/storage-inventory.json',inventory)
        pointer=(storage/'CURRENT').read_bytes();assert pointer[:8]==b'CRPGROOT'
        result['trusted_manifest_sha256']=pointer[20:52].hex()
        result['payload_audit']=audit
        result['final']=blocks[-1]
        result['archive_ms_max']=max(r['archive_ms'] for r in blocks)
        result['block_ms_max']=max(r['block_ms'] for r in blocks)
        result['evidence']='campaigns/'+label
        campaigns[key]=result
missing=sorted(required-campaigns.keys())
if not a.allow_incomplete:assert not missing,missing
values=[campaigns[k] for k in sorted(campaigns)]
dump('campaigns.json',values)
dump('acceptance.json',{'status':'IMPLEMENTED_ACCEPTANCE_PASSED_PENDING_INDEPENDENT_REVIEW' if not missing else 'IMPLEMENTED_LONG_CAMPAIGN_VALIDATION_IN_PROGRESS','complete':not missing,'missing_campaigns':missing,'core_revision':pin,'stable_f04_core_pin_unchanged':(source/'core-revision.txt').read_text().strip(),'suites':suites,'unreal':{'passed':ue['succeeded'],'warnings':ue['succeededWithWarnings'],'failed':ue['failed'],'notRun':ue['notRun']},'campaigns':[{'profile':r['profile'],'days':r['days'],'completed':r['completed'],'facts_verified':r['payload_audit']['original_facts_verified']} for r in values],'no_merge':True,'no_integration04_or_closure05':True})
files=[source/'CMakeLists.txt',source/'core-history-revision.txt',source/'core-revision.txt',*source.glob('src/*'),*source.glob('include/*'),*source.glob('unreal/*'),*source.glob('tests/history*.cpp'),*source.glob('tests/*history*.py')]
dump('source-files.json',{str(path.relative_to(repo)).replace('\\','/'):sha(path) for path in files if path.is_file()})
dump('evidence-sha256.json',{str(path.relative_to(out)).replace('\\','/'):sha(path) for path in sorted(out.rglob('*')) if path.is_file() and path.name!='evidence-sha256.json'})
print(json.dumps({'complete':not missing,'campaigns':len(campaigns),'missing':missing,'output':str(out)},ensure_ascii=False))
