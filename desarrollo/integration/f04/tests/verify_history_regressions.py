"""Build unchanged F02/F03 against the proposed Core in disposable source copies.
Only the copied pin checks differ; stable repository pins are never edited.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--core',required=True)
p.add_argument('--root',required=True)
a=p.parse_args()
integration=Path(__file__).parents[2]
root=Path(a.root)
root.mkdir(parents=True,exist_ok=True)
sha=subprocess.check_output(['git','-C',a.core,'rev-parse','HEAD'],text=True).strip()
assert sha==integration.joinpath('f04/core-history-revision.txt').read_text().strip()
def run(args,log):
    with log.open('w',encoding='utf-8') as f:
        r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
    if r.returncode: raise RuntimeError(log.read_text())
for phase,old in [('f02','4f282863737bcd8f5add401202a9e1064c133672'),('f03','9c53a33787de13d91eb2abe4da07033ee0fa1dc1')]:
    source=integration/phase
    copy=root/(phase+'-source')
    assert not copy.exists(), 'use a fresh verification root'
    shutil.copytree(source,copy)
    if phase=='f02':
        cmake=copy/'CMakeLists.txt'
        cmake.write_text(cmake.read_text().replace(old,sha))
        pin_assertion=copy/'tests/f02_tests.cpp'
        pin_assertion.write_text(pin_assertion.read_text().replace(old,sha))
    else:
        (copy/'core-revision.txt').write_text(sha+'\n')
    build=root/phase
    run(['cmake','-S',str(copy),'-B',str(build),'-G','Visual Studio 18 2026','-A','x64','-DCORERPG_SOURCE_DIR='+a.core],root/(phase+'-configure.log'))
    run(['cmake','--build',str(build),'--config','Release','--parallel','4'],root/(phase+'-build.log'))
    run(['ctest','--test-dir',str(build),'-C','Release','--output-on-failure','--output-junit',str(root/(phase+'.xml'))],root/(phase+'-tests.log'))
    print(phase,sha,'PASS',flush=True)
    (root/(phase+'-pin-override.json')).write_text(json.dumps({'phase':phase,'proposed_core':sha,'stable_core_unchanged':old,'scope':'disposable source copy: build pin check and exact-SHA test assertion only'},indent=2)+'\n')
