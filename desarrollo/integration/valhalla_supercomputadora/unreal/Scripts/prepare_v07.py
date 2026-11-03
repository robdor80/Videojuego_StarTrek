"""Prepare a NEW V07 project from the preserved V06 delivery; never edit the donor."""
import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-project', type=Path, required=True)
    parser.add_argument('--target', type=Path, required=True)
    args = parser.parse_args()
    template = Path(__file__).resolve().parents[1]
    repository = template.parents[3]
    source = args.source_project.resolve().parent
    target = args.target.resolve()
    if not args.source_project.is_file() or not (source/'Content/Valhalla/Maps/L_Supercomputadora_V06_Quinn.umap').is_file():
        raise SystemExit('Expected the independent, preserved V06 delivery')
    if target.exists() or not target.is_relative_to(repository) or target.is_relative_to(source) or source.is_relative_to(target):
        raise SystemExit('Target must be NEW, inside this repository and separate from V06')
    shutil.copytree(source/'Content', target/'Content')
    shutil.copytree(source/'Config', target/'Config')
    for folder in ['Source', 'Plugins', 'Scripts']:
        shutil.copytree(template/folder, target/folder,
                        ignore=shutil.ignore_patterns('Binaries', 'Intermediate', '__pycache__'))
    project = json.loads(args.source_project.read_text(encoding='utf8'))
    project['Description'] = 'USS Enterprise NCC-1701-D - V07 cierre practico; auditoria final pendiente'
    (target/'ValhallaComputer.uproject').write_text(json.dumps(project, indent=2)+'\n', encoding='utf8')
    engine_config = target/'Config/DefaultEngine.ini'
    config = engine_config.read_text(encoding='utf8').split('[/Script/AndroidFileServerEditor.')[0]
    config = config.replace('/Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn',
                            '/Game/ValhallaV07/Maps/L_Supercomputadora_V07')
    engine_config.write_text(config, encoding='utf8')
    shutil.copy2(template/'README_V07.md', target/'README_V07.md')
    print(target/'ValhallaComputer.uproject')


if __name__ == '__main__':
    main()
