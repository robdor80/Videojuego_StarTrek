"""Validate the saved checkpoint before a separately requested normal Windows shutdown."""
import ast,ctypes,datetime,hashlib,json,os,time
from pathlib import Path
from ctypes import wintypes
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'VERIFICACION/manifiesto_parada.json').read_text(encoding='utf8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
checked=[]
for x in manifest['files']:
 p=R/x['file'];actual=sha(p) if p.is_file() else None
 checked.append(dict(file=x['file'],ok=actual==x['sha256']))
assert all(x['ok'] for x in checked),'Checkpoint changed: do not shut down'
def snapshot():return {str(p.relative_to(R)):(p.stat().st_size,p.stat().st_mtime_ns) for p in R.rglob('*') if p.is_file()}
s1=snapshot();time.sleep(2);s2=snapshot()
assert s1==s2,'Lab files changing: do not shut down'
kernel=ctypes.WinDLL('kernel32',use_last_error=True)
kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
kernel.CreateFileW.restype=wintypes.HANDLE
kernel.CloseHandle.argtypes=[wintypes.HANDLE]
busy=[]
for relative in s2:
 handle=kernel.CreateFileW(str(R/relative),0x80000000,0,None,3,0x80,None)
 if handle==ctypes.c_void_p(-1).value:busy.append(dict(file=relative,error=ctypes.get_last_error()))
 else:kernel.CloseHandle(handle)
assert not busy,'Open lab handles: do not shut down'
for p in (R/'SCRIPTS').glob('*.py'):ast.parse(p.read_text(encoding='utf8'))
for p in (R/'DATOS').glob('*.json'):json.loads(p.read_text(encoding='utf8'))
reopen=json.loads((R/'VERIFICACION/parada_reapertura_copias.json').read_text(encoding='utf8'))
assert all(x['read_ok'] and all(i['exists'] for i in x['images']) for x in reopen)
report=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),computer=os.environ.get('COMPUTERNAME'),checkpoint_hashes=checked,lab_stable=True,stable_files=len(s2),exclusive_read_all_files=True,open_handles=busy,blender_recovery='Prior successful independent reopen remains applicable: scene and dependency hashes unchanged',safe_to_request_normal_shutdown=True,shutdown_executed_by_this_script=False)
def save(p,txt):
 with p.open('w',encoding='utf8') as f:f.write(txt);f.flush();os.fsync(f.fileno())
save(R/'VERIFICACION/preapagado.json',json.dumps(report,indent=2))
state=R/'ESTADO_REANUDACION.md'
addition='\n\n## Comprobación adicional previa al apagado del MSI\n\n'+report['timestamp_utc']+' — A petición expresa del usuario, se verificaron los '+str(len(checked))+' archivos del manifiesto de parada mediante SHA-256: todos coinciden. El laboratorio permaneció estable durante la comprobación; todos sus archivos admitieron apertura exclusiva de lectura, sin bloqueos de escritura detectados. Las dos escenas y sus dependencias conservan los hashes con los que fueron reabiertas correctamente. Scripts y JSON vuelven a ser legibles.\n\nSe prepara una solicitud de apagado completo normal de Windows mediante `shutdown.exe /s /t 0`, sin `/f`, sin `/hybrid` y sin reinicio. Este texto registra la preparación, no certifica que el hardware se haya apagado. Si Windows muestra una aplicación bloqueante, no forzar su cierre. La reanudación técnica de VOY-05B continúa pendiente de autorización. Evidencia: `VERIFICACION/preapagado.json`.\n'
save(state,state.read_text(encoding='utf8')+addition)
files=[dict(file=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifiesto_parada.json']
new=dict(timestamp_utc=report['timestamp_utc'],scope='All lab files except this manifest itself; refreshed before normal shutdown request',files=files)
save(R/'VERIFICACION/manifiesto_parada.json',json.dumps(new,indent=2))
assert json.loads((R/'VERIFICACION/manifiesto_parada.json').read_text(encoding='utf8'))==new
print(json.dumps(dict(checkpoint_files_verified=len(checked),all_hashes_match=True,lab_stable=True,no_open_lab_handles=True,state_updated=True,refreshed_manifest_files=len(files),ready_for_normal_shutdown=True),indent=2))
