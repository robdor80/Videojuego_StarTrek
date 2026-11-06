"""Registro de conservación VOY-02. Solo lee el laboratorio y escribe en TRASPASO.
No abre Blender/Unreal, no mide geometría, no reconstruye resultados ni borra archivos.
"""
import csv, datetime, hashlib, json, os, subprocess, zipfile
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

baseline = json.loads((ROOT / 'DATOS/entradas_antes.json').read_text(encoding='utf-8'))
checks = []
for row in baseline:
    p = Path(row['source'])
    result = {'source': str(p), 'expected_sha256': row['sha256'], 'exists': p.is_file()}
    if p.is_file():
        result.update(sha256=digest(p), bytes=p.stat().st_size, mtime_ns=p.stat().st_mtime_ns)
        result['hash_matches'] = result['sha256'] == row['sha256']
        result['metadata_matches'] = result['bytes'] == row['bytes'] and result['mtime_ns'] == row['mtime_ns']
    if row.get('copy'):
        q = Path(row['copy'])
        result['copy'] = str(q)
        result['copy_matches'] = q.is_file() and digest(q) == row['sha256']
    checks.append(result)
save('COMPROBACION_ENTRADAS.json', {'time': datetime.datetime.now().astimezone().isoformat(), 'entries': len(checks), 'all_original_hashes_match': all(x.get('hash_matches', False) for x in checks), 'all_original_metadata_match': all(x.get('metadata_matches', False) for x in checks), 'all_recorded_copies_match': all(x.get('copy_matches', True) for x in checks), 'scope': '115 entradas registradas al preparar VOY-02; no es un hash completo de Sutherland ni de todos los repositorios.', 'results': checks})

inventory = []
formats = []
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or HERE in p.parents:
        continue
    st = p.stat()
    inventory.append({'relative_path': p.relative_to(ROOT).as_posix(), 'absolute_path': str(p), 'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns, 'sha256': digest(p)})
    if p.parent.name == 'DATOS' and p.suffix in ['.json', '.npz'] or p.parent.name == 'CAPTURAS' and p.suffix == '.png':
        check = {'file': str(p), 'check': 'file readability only; not validation of numerical conclusions'}
        try:
            if p.suffix == '.json':
                json.loads(p.read_text(encoding='utf-8'))
            elif p.suffix == '.npz':
                with zipfile.ZipFile(p) as z:
                    assert z.testzip() is None
            else:
                with Image.open(p) as im:
                    check['resolution'] = list(im.size)
                    im.verify()
            check['readable'] = True
        except Exception as e:
            check.update(readable=False, error=str(e))
        formats.append(check)
with (HERE / 'INVENTARIO_ARCHIVOS.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=['relative_path', 'absolute_path', 'bytes', 'mtime_ns', 'sha256'])
    w.writeheader()
    w.writerows(inventory)

ps = "Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(blender|python|pythonw|UnrealEditor|UnrealEditor-Cmd|UnrealBuildTool)(\\.exe)?$' } | Select-Object ProcessId,ParentProcessId,Name,CreationDate,CommandLine | ConvertTo-Json -Depth 4 -Compress"
proc = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
processes = json.loads(proc.stdout) if proc.stdout.strip() else []
if isinstance(processes, dict):
    processes = [processes]
processes = [x for x in processes if x['ProcessId'] != os.getpid()]
git = {}
for label, path in [('workspace', r'C:\Users\andro\Documents\ChatGPT\UE5 y Blender'), ('Videojuego_StarTrek', r'C:\Users\andro\Documents\GitHub\Videojuego_StarTrek')]:
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    status = subprocess.run(['git', '-C', path, 'status', '--short', '--branch'], capture_output=True, text=True, env=env)
    head = subprocess.run(['git', '-C', path, 'rev-parse', 'HEAD'], capture_output=True, text=True, env=env)
    git[label] = {'path': path, 'status_exit': status.returncode, 'status': status.stdout.strip(), 'head': head.stdout.strip() if head.returncode == 0 else None}
save('ESTADO_PARADA.json', {'time': datetime.datetime.now().astimezone().isoformat(), 'laboratory': str(ROOT), 'inventory_excludes': 'TRASPASO (documentos nuevos de conservación)', 'files': len(inventory), 'bytes': sum(x['bytes'] for x in inventory), 'originals_all_hashes_match': all(x.get('hash_matches', False) for x in checks), 'format_checks': formats, 'remaining_relevant_processes': processes, 'process_check_exit': proc.returncode, 'git_read_only': git, 'last_completed_operation': '12_capturas.py: 33 capturas; Blender quit. Encuadres pendientes de corrección.', 'stop_point': 'Antes de cambiar cámaras/maniquíes o repetir renders. Sin nuevas mediciones ni implementación desde la orden de parada.', 'blend_reopen_validation': 'Pendiente; no se abre Blender durante el traspaso.'})
print(json.dumps({'files_preserved': len(inventory), 'baseline_entries': len(checks), 'originals_match': all(x.get('hash_matches', False) for x in checks), 'copies_match': all(x.get('copy_matches', True) for x in checks), 'format_files_checked': len(formats), 'format_read_errors': sum(not x['readable'] for x in formats), 'relevant_processes': processes}, ensure_ascii=False))
