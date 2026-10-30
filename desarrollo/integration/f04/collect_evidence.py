"""Publish small sanitized results. Original inventories, art and binaries stay local."""
import argparse, hashlib, json, pathlib, re, xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('--build-root',type=pathlib.Path,required=True)
parser.add_argument('--output',type=pathlib.Path,required=True)
args=parser.parse_args()
root=args.build_root; source=root/'evidence';out=args.output;out.mkdir(parents=True,exist_ok=True)
def sanitize(text):
    text=re.sub(r'C:[/\\]Users[/\\][^/\\\s<>";]+', '<USER_HOME>', text, flags=re.I)
    text=text.replace('C:\\F04','<F04_BUILD>').replace('C:/F04','<F04_BUILD>')
    return text
summary={}
for label,filename in [('core','core.xml'),('f04','native.xml'),('f02','f02-native.xml'),('f03','f03-native.xml')]:
    p=source/filename;node=ET.fromstring(p.read_bytes());cases=node.findall('.//testcase')
    failed=sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
    skipped=sum(c.find('skipped') is not None for c in cases)
    summary[label]={'defined':len(cases),'passed':len(cases)-failed-skipped,'failed':failed,'skipped':skipped}
    (out/(label+'.xml')).write_text(sanitize(p.read_text(encoding='utf-8')),encoding='utf-8')
reports=sorted(root.glob('*-ue-report/index.json'))
if not reports:raise SystemExit('Unreal report missing')
report=json.loads(reports[-1].read_text(encoding='utf-8-sig'))
tests=[{'name':t['fullTestPath'],'state':t['state'],'duration':t.get('duration',0),'warnings':t.get('warnings',0),'errors':t.get('errors',0)} for t in report['tests']]
summary['unreal']={k:report[k] for k in ['succeeded','succeededWithWarnings','failed','notRun']}
(out/'unreal.json').write_text(json.dumps({'summary':summary['unreal'],'tests':tests},indent=2),encoding='utf-8')
unit_results={}
for name in ['f04-reference','miranda','f03-reference','f02-reference']:
    log=(source/(name+'.log')).read_text(encoding='utf-8',errors='replace')
    count=re.search(r'Ran (\d+) tests?',log)
    unit_results[name]={'tests':int(count[1]),'success':bool(re.search(r'\bOK\b',log))}
    (out/(name+'.txt')).write_text(sanitize(log),encoding='utf-8')
summary['reference_unittests']=unit_results
summary['f04_scenarios']=39
for name in ['f04-fixture','governance','f03-contracts','f02-contracts','f02-plan','internal-references','internal-references-baseline']:
    p=source/(name+'.log');(out/(name+'.txt')).write_text(sanitize(p.read_text(encoding='utf-8',errors='replace')),encoding='utf-8')
baseline=(source/'internal-references-baseline.log').read_bytes()
current=(source/'internal-references.log').read_bytes()
summary['general_reference_validator']={'success':False,'issues':564,'baseline_issues':564,'byte_identical_output':baseline==current}
protected=json.loads((source/'protected_result.json').read_text(encoding='utf-8'))
summary['protection']={k:protected[k] for k in ['before','after','method']}
summary['protection'].update({k:len(protected[k]) for k in ['missing','changed','new']})
failures=[]
for name in ['native-build-first','native-first','native-second','native-third','native-final']:
    p=source/(name+'.log')
    text=p.read_text(encoding='utf-8',errors='replace')
    failures.append({'attempt':name,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'excerpt':sanitize('\n'.join(text.splitlines()[-65:]))})
(out/'original-failures.json').write_text(json.dumps(failures,indent=2),encoding='utf-8')
(out/'source-audit.json').write_bytes((source/'audit-source-inventory.json').read_bytes())
(out/'results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
