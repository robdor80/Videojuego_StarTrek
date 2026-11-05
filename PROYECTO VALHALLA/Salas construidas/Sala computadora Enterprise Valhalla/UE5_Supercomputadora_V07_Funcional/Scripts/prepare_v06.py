"""Prepare a NEW local V06 workspace from an untouched V05 project.
Run with system Python, then build ValhallaComputerEditor before author_v06.py.
No engine assets or binaries are published with this source template.
"""
import argparse,json,shutil
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-project',type=Path,required=True)
    parser.add_argument('--engine',type=Path,required=True,help='Installed UE_5.8 directory')
    parser.add_argument('--target',type=Path,required=True,help='New authorized temporary directory inside this repository')
    args=parser.parse_args()
    template=Path(__file__).resolve().parents[1]
    repository=template.parents[3]
    source=args.source_project.resolve().parent
    target=args.target.resolve()
    if not args.source_project.is_file() or not (source/'Content/Valhalla/Maps/L_Supercomputadora_V05.umap').is_file():
        raise SystemExit('Expected the independent V05 source project')
    if target.exists() or not target.is_relative_to(repository) or target.is_relative_to(source):
        raise SystemExit('Target must be NEW, inside this repository and outside the source project')
    official=json.loads((template/'Scripts/v06_official_assets.json').read_text(encoding='utf8'))
    roots=[('Characters',args.engine/'Templates/TemplateResources/High/Characters/Content'),('Input',args.engine/'Templates/TemplateResources/High/Input/Content'),('ThirdPerson/Blueprints',args.engine/'Templates/TP_ThirdPersonBP/Content/ThirdPerson/Blueprints')]
    copies=[]
    for rel in official:
        matches=[base/Path(rel).relative_to(prefix) for prefix,base in roots if Path(rel).is_relative_to(prefix)]
        if len(matches)!=1 or not matches[0].is_file():raise SystemExit('Missing official installed resource: '+rel)
        copies.append((matches[0],target/'Content'/rel))
    shutil.copytree(source/'Content',target/'Content')
    for folder in ['Source','Config','Plugins','Scripts']:
        shutil.copytree(template/folder,target/folder,ignore=shutil.ignore_patterns('Binaries','Intermediate','__pycache__'))
    project=json.loads((template/'ValhallaComputer.uproject').read_text(encoding='utf8'))
    project['Description']='Valhalla V06 - official Quinn and protected constructed area'
    enabled={p['Name'] for p in project.get('Plugins',[])}
    for name in ['EnhancedInput','GameplayStateTree']:
        if name not in enabled:project.setdefault('Plugins',[]).append({'Name':name,'Enabled':True})
    (target/'ValhallaComputer.uproject').write_text(json.dumps(project,indent=2)+'\n',encoding='utf8')
    f=target/'Config/DefaultEngine.ini';text=f.read_text(encoding='utf8').split('[/Script/AndroidFileServerEditor.')[0]
    f.write_text(text.replace('L_Supercomputadora_V05','L_Supercomputadora_V06_Quinn'),encoding='utf8')
    f=target/'Config/DefaultInput.ini';text=f.read_text(encoding='utf8');text+='\nDefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput\nDefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent\n';f.write_text(text,encoding='utf8')
    for src,dst in copies:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    print(target/'ValhallaComputer.uproject')
if __name__=='__main__':main()
