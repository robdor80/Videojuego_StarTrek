"""Create a new portable V07 completion project; originals are always read only."""
import argparse
import json
import shutil
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-project',required=True)
    parser.add_argument('--target',required=True)
    args=parser.parse_args()
    source=Path(args.source_project).resolve()
    if source.is_file():source=source.parent
    target=Path(args.target).resolve()
    assert source.is_dir() and not target.exists()
    assert source not in target.parents,'Use a sibling or an authorized isolated copy'
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('Saved','Intermediate','DerivedDataCache','__pycache__','*.pdb'))
    integration=Path(__file__).resolve().parent.parent
    for name in ('Source','Plugins','Scripts'):
        shutil.copytree(integration/name,target/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    config=target/'Config/DefaultEngine.ini'
    config.write_text(config.read_text(encoding='utf-8-sig').replace(
        '=/Game/ValhallaV07/Maps/L_Supercomputadora_V07\n',
        '=/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional\n'),encoding='utf8')
    project=target/'ValhallaComputer.uproject'
    data=json.loads(project.read_text(encoding='utf-8-sig'))
    data['Description']='USS Enterprise NCC-1701-D - V07 funcional; seis accesos de memoria y cubiertas de escalera'
    project.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    print(target)


if __name__=='__main__':main()
