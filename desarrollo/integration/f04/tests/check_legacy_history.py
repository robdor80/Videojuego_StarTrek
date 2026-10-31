"""Explicit non-destructive migration of old DLL saves, then fresh-process recovery."""
import argparse
import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

p=argparse.ArgumentParser()
p.add_argument('--dll',required=True)
p.add_argument('--fixtures')
p.add_argument('--output')
p.add_argument('--resume')
p.add_argument('--old-dll')
a=p.parse_args()
lib=C.CDLL(str(Path(a.dll).resolve()))
P=C.c_void_p
U=C.c_uint64
spec={
 'f04_create':([C.c_uint32,C.c_char_p,C.POINTER(P)],C.c_uint32),
 'f04_destroy':([P],C.c_uint32),
 'f04_load':([P,P,U],C.c_uint32),
 'f04_history_export_active':([P,P,U,C.POINTER(U)],C.c_uint32),
 'f04_history_migrate':([P,C.c_char_p,P,U],C.c_uint32),
 'f04_history_open':([P,C.c_char_p],C.c_uint32),
 'f04_history_publish':([P,C.c_uint32],C.c_uint32),
 'f04_advance':([P,U,U,C.POINTER(U)],C.c_uint32),
}
for name,(args,result) in spec.items():
    f=getattr(lib,name);f.argtypes=args;f.restype=result
def session():
    s=P();assert lib.f04_create(1,b'miranda',C.byref(s))==0;return s
def active(s):
    n=U();assert lib.f04_history_export_active(s,None,0,C.byref(n))==15
    data=(C.c_ubyte*n.value)();assert lib.f04_history_export_active(s,data,n,C.byref(n))==0
    return bytes(data)
def hash(data):return hashlib.sha256(data).hexdigest()
if a.resume:
    directory=Path(a.resume);meta=json.loads(directory.with_suffix('.migration.json').read_text())
    s=session()
    try:
        assert lib.f04_history_open(s,str(directory).encode('utf-8'))==0
        assert hash(active(s))==meta['source_sha256']
        processed=U();assert lib.f04_advance(s,meta['future_tick'],4096,C.byref(processed))==0
        assert hash(active(s))==meta['future_sha256']
    finally: assert lib.f04_destroy(s)==0
    print('fresh process migration future PASS')
    raise SystemExit(0)
assert a.fixtures and a.output
root=Path(a.output);root.mkdir(parents=True,exist_ok=False)
results={}
old=None
if a.old_dll:
    old=C.CDLL(str(Path(a.old_dll).resolve()))
    for name in ['f04_create','f04_destroy','f04_load']:
        getattr(old,name).argtypes=spec[name][0];getattr(old,name).restype=spec[name][1]
    old.f04_save.argtypes=spec['f04_history_export_active'][0];old.f04_save.restype=C.c_uint32
for profile,name in enumerate(['miranda','intrepid','sovereign','odyssey','valhalla'],1):
    source=Path(a.fixtures)/(name+'.f04');original=source.read_bytes();future=Path(str(source)+'.future').read_bytes()
    directory=root/name;s=session()
    try:
        data=C.create_string_buffer(original);assert lib.f04_load(s,data,len(original))==0
        uuid=C.create_string_buffer(bytes([profile])+bytes(15))
        assert lib.f04_history_migrate(s,str(directory).encode('utf-8'),uuid,16)==0
        assert active(s)==original
        assert source.read_bytes()==original
        meta={'source_sha256':hash(original),'future_sha256':hash(future),'future_tick':struct.unpack_from('<Q',future,20)[0]}
        directory.with_suffix('.migration.json').write_text(json.dumps(meta,indent=2)+'\n')
        if old:
            previous=P();assert old.f04_create(1,b'miranda',C.byref(previous))==0
            try:
                assert old.f04_load(previous,data,len(original))==0
                pointer=(directory/'CURRENT').read_bytes();root_bytes=C.create_string_buffer(pointer)
                assert old.f04_load(previous,root_bytes,len(pointer))==14
                n=U();assert old.f04_save(previous,None,0,C.byref(n))==15
                unchanged=(C.c_ubyte*n.value)();assert old.f04_save(previous,unchanged,n,C.byref(n))==0
                assert bytes(unchanged)==original
            finally:assert old.f04_destroy(previous)==0
    finally:assert lib.f04_destroy(s)==0
    result=subprocess.run([sys.executable,__file__,'--dll',a.dll,'--resume',str(directory)],check=True,capture_output=True,text=True)
    results[name]={**meta,'source_unchanged':True,'active_projection_identical':True,'fresh_process_future_identical':True,'old_reader_rejects_history_without_mutation':bool(old),'resume':result.stdout.strip()}
(root/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
