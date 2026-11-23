"""Negative contract tests for equipment reference generation."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from generate_equipment_catalog import build,SOURCE


def run(output):
    output.mkdir(parents=True,exist_ok=True)
    original=json.loads(SOURCE.read_text(encoding='utf-8'))
    assert 'F06_EQUIPMENT_CATALOG' in build()
    cases=[]
    for kind in ('status','version','boolean_version','slot_order','duplicate','zero_class',
                 'boolean_count','negative','overflow','short_count','missing_class'):
        candidate=deepcopy(original)
        if kind=='status':candidate['status']='CANON'
        elif kind=='version':candidate['version']=2
        elif kind=='boolean_version':candidate['version']=True
        elif kind=='slot_order':candidate['slots'].reverse()
        elif kind=='duplicate':candidate['classes'].append(candidate['classes'][0])
        elif kind=='zero_class':candidate['classes'][0]['class_id']=0
        elif kind=='boolean_count':candidate['classes'][0]['count'][0]=True
        elif kind=='negative':candidate['classes'][0]['count'][0]=-1
        elif kind=='overflow':candidate['classes'][0]['count'][0]=65
        elif kind=='short_count':candidate['classes'][0]['count'].pop()
        elif kind=='missing_class':candidate['classes'].pop()
        path=output/f'{kind}.json';path.write_text(json.dumps(candidate))
        try:build(path)
        except ValueError:cases.append(kind)
        else:raise AssertionError(kind)
    assert len(cases)==11
    print('PASS equipment catalog integrity: canonical labeling, version, semantic slots, IDs, types and ranges')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True)
    run(p.parse_args().output_dir)
