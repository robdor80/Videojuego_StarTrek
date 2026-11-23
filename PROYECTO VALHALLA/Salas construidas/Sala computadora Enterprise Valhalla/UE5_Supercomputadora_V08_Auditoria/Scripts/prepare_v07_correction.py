"""Prepare a new V07 correction from the preserved functional V07; never replace an existing folder."""
import argparse,json,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source-project',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args()
source=a.source_project.resolve();source=source.parent if source.is_file() else source
target=a.target.resolve();assert source.is_dir() and not target.exists() and source not in target.parents
integration=Path(__file__).resolve().parent.parent
ignore=shutil.ignore_patterns('Saved','Intermediate','DerivedDataCache','__pycache__','*.pdb')
shutil.copytree(source,target,ignore=ignore)
for name in ('Source','Plugins','Scripts','Binaries'):shutil.copytree(integration/name,target/name,dirs_exist_ok=True,ignore=ignore)
for name in ('DefaultEngine.ini','DefaultEngine.ini.example'):
 f=target/'Config'/name
 if f.exists():f.write_text(f.read_text(encoding='utf-8-sig').replace('=/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional','=/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Corregida'),encoding='utf8')
for name in ('README_V07.md','README_V07_CORREGIDA.md'):
 f=integration/name
 if f.is_file():shutil.copyfile(f,target/name)
print(target)
