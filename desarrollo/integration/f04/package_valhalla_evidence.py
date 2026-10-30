"""Bundle completed local runs and record source/binary provenance for audit."""
import argparse
import hashlib
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True).strip()
def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--build-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    def dump(name,data):(a.output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    suites={}
    for name in ['core','f02','f03','f04','capacity-atomic']:
        path=a.build_root/(name+'.xml');tree=ET.parse(path).getroot();suite=tree if tree.tag=='testsuite' else tree.find('testsuite')
        suites[name]=dict(suite.attrib);assert int(suite.attrib.get('failures',0))==0
        shutil.copyfile(path,a.output/path.name)
    for src,dst in [('f04-tests.txt','native.txt'),('core-tests.txt','core.txt'),('unreal-tests.txt','nullrhi.txt'),('capacity-atomic.txt','capacity-atomic.txt')]:shutil.copyfile(a.build_root/src,a.output/dst)
    ue=sorted(a.build_root.glob('*-ue-report/index.json'))[-1];report=json.loads(ue.read_text(encoding='utf-8-sig'))
    assert report['succeeded']+report['succeededWithWarnings']==23 and report['failed']==report['notRun']==0
    shutil.copyfile(ue,a.output/'unreal-report.json')
    buildlog=sorted((a.build_root/'logs').glob('*-ue-build.log'))[-1]
    (a.output/'unreal-build.txt').write_text('\n'.join(line.rstrip() for line in buildlog.read_text(encoding='utf-8-sig').splitlines())+'\n',encoding='utf-8')
    suites['unreal']={k:report[k] for k in ['succeeded','succeededWithWarnings','failed','notRun','totalDuration']};dump('test-summary.json',suites)
    before=(a.build_root/'references-base.txt').read_text(encoding='utf-8-sig');after=(a.build_root/'references-current.txt').read_text(encoding='utf-8-sig')
    errors=lambda text:[s for s in text.splitlines() if s.startswith(' - ')]
    old,new=errors(before),errors(after);assert old==new
    shutil.copyfile(a.build_root/'references-current.txt',a.output/'references.txt')
    dump('reference-regression.json',{'base':'78fa53f99c384f4111f42d61d71fa2510b56f6b5','base_issues':len(old),'current_issues':len(new),'new_issues':0,'identical_ordered_errors':old==new})
    native=a.build_root/'native/Release/TrekF04Bridge.dll';staged=a.build_root/'ue/Binaries/Win64/TrekF04Bridge.dll';assert digest(native)==digest(staged)
    sources={str(path.relative_to(ROOT)).replace('\\','/'):digest(path) for path in (ROOT/'desarrollo/integration/f04').rglob('*') if path.is_file() and path.suffix in ['.h','.cpp','.inc']}
    cores={str(path):{'sha':git(path,'rev-parse','HEAD'),'status':git(path,'status','--porcelain')} for path in map(Path,['C:/F04/CoreRPG','C:/F04/core-f02','C:/F04/core-f03'])}
    assert all(not c['status'] for c in cores.values())
    dump('build-provenance.json',{'base':'78fa53f99c384f4111f42d61d71fa2510b56f6b5','branch':git(ROOT,'branch','--show-current'),
      'cores':cores,'engine':json.loads(Path('C:/Program Files/Epic Games/UE_5.8/Engine/Build/Build.version').read_text()),
      'compiler':'MSVC 19.51.36256 / Visual Studio 18 2026 / x64 Release','native_dll_sha256':digest(native),'unreal_dll_sha256':digest(staged),
      'source_sha256':sources,'main_status':git(Path('C:/Users/andro/Documents/GitHub/Videojuego_StarTrek'),'status','--porcelain'),
      'scope':'Only F04 integration code, tests and F04 documentation/evidence. No Core/3D/art/backups changes.'})
    print(json.dumps(suites,indent=2))

if __name__=='__main__':main()
