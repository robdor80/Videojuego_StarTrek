"""Read-only metadata/Git baseline for protected original project resources."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('stage',choices=['before','after'])
parser.add_argument('--original',type=Path,required=True)
parser.add_argument('--evidence',type=Path,required=True)
args=parser.parse_args()
root=args.original.resolve(); out=args.evidence.resolve()
if out==root or root in out.parents:
    raise SystemExit('Evidence must be outside the protected original tree')
out.mkdir(exist_ok=True,parents=True)
records=[]
for base,dirs,files in os.walk(root):
    dirs[:]=[d for d in dirs if d!='.git']
    for name in files:
        p=Path(base)/name; s=p.stat()
        records.append([p.relative_to(root).as_posix(),s.st_size,s.st_mtime_ns])
records.sort()
baseline=out/'original_files_before.json'
if args.stage=='before':
    if baseline.exists(): raise SystemExit('Refusing to overwrite an existing original baseline')
    baseline.write_text(json.dumps(records,ensure_ascii=False),encoding='utf-8')
    for name,command in [('git_status_before.txt',['status','--porcelain=v1','--branch']),
                          ('tracked_before.txt',['ls-files']),
                          ('ignored_before.txt',['ls-files','--others','--ignored','--exclude-standard']),
                          ('untracked_before.txt',['ls-files','--others','--exclude-standard'])]:
        (out/name).write_bytes(subprocess.check_output(['git','-C',str(root),*command]))
    print('Original baseline saved')
else:
    before=json.loads(baseline.read_text(encoding='utf-8'))
    before_set=set(map(tuple,before)); after_set=set(map(tuple,records))
    result=dict(before_count=len(before),after_count=len(records),
                missing_or_changed=[r for r in before if tuple(r) not in after_set],
                new=[r for r in records if tuple(r) not in before_set],
                method='relative path, size and nanosecond mtime; not a full content hash audit')
    (out/'original_files_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if result['missing_or_changed'] or result['new']: raise SystemExit(1)
