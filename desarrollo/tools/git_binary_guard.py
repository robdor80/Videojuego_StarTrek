#!/usr/bin/env python3
"""Audit the actual Git index, including forced additions and partial staging."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import PurePosixPath

LIMIT = 25 * 1024 * 1024
MODELS = {'.blend', '.fbx', '.glb', '.gltf', '.obj', '.mtl', '.dae', '.usd',
          '.usda', '.usdc', '.usdz', '.abc', '.3ds', '.max', '.ma', '.mb',
          '.c4d', '.stl', '.ply', '.skp', '.lwo', '.lws', '.spp', '.sbsar'}
LIGHT = {'.md', '.txt', '.json', '.yaml', '.yml', '.csv', '.tsv', '.xml',
         '.toml', '.ini', '.cfg', '.license', '.spdx', '.url', '.gitkeep'}
POLICY = 'desarrollo/manifests/git_storage_exceptions.json'
LOCAL_ROOTS = ('laboratorios/', 'archivo_historico/', '3d star trek/',
               'auditorias_3d_voyager/', 'sutherland_pbr_lab/',
               'tabula rasa copia seguridad/', '_st/')

def git(*args, data=None):
    return subprocess.check_output(['git', *args], input=data)

def prohibited(path):
    p = PurePosixPath(path)
    low = path.casefold()
    suffix = p.suffix.casefold()
    if suffix in MODELS or suffix.startswith('.blend'):
        return 'formato 3D local'
    if suffix in {'.zip', '.7z', '.rar', '.tar', '.gz'}:
        return 'paquete comprimido local'
    for root in LOCAL_ROOTS:
        if low.startswith(root) and low != root + 'readme.md':
            return 'recurso local / laboratorio / respaldo'
    if low.startswith('assets/') and suffix not in LIGHT and p.name.casefold() not in {'.gitkeep', 'license', 'licence', 'copying', 'notice', 'authors', 'copyright'}:
        return 'binario de biblioteca assets'
    if any(part.casefold() in {'intermediate', 'saved', 'deriveddatacache', '__pycache__', '.vs'} for part in p.parts):
        return 'cache regenerable'
    if low.startswith('juego/ue5/startrekrpg/binaries/'):
        return 'binario Unreal regenerable del proyecto principal'
    if any(part.casefold() in {'textures', 'texturas_pbr', 'materiales_pbr'} for part in p.parts) and suffix not in LIGHT and p.name.casefold() not in {'.gitkeep', 'license', 'licence', 'copying', 'notice', 'authors', 'copyright'}:
        return 'recurso de texturas local'
    return None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Machine-readable report')
    args = parser.parse_args()
    try:
        subprocess.run(['git', 'rev-parse', '--show-toplevel'], check=True, stdout=subprocess.DEVNULL)
        # --full-name paths and :/path remain correct from any repository subdirectory.
        import os
        os.chdir(git('rev-parse', '--show-toplevel').decode().strip())
        entries = []
        for line in git('ls-files', '--stage', '-z').split(b'\0'):
            if not line:
                continue
            meta, path = line.split(b'\t', 1)
            mode, oid, stage = meta.decode().split()
            entries.append((mode, oid, stage, path.decode('utf-8', errors='surrogateescape')))
        exceptions = {}
        try:
            policy = json.loads(git('show', ':' + POLICY))
            for item in policy['exceptions']:
                if item['path'] in exceptions:
                    raise ValueError('duplicate exception path')
                if not all(isinstance(item.get(k), str) and item[k].strip() for k in ('path', 'sha256', 'reason', 'approved_by')):
                    raise ValueError('exception requires path, SHA-256, reason and explicit approver')
                exceptions[item['path']] = item
        except subprocess.CalledProcessError:
            raise ValueError('stage ' + POLICY + ' before committing')
        ids = sorted({oid for mode, oid, stage, path in entries if mode != '160000'})
        output = git('cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)', data=('\n'.join(ids) + '\n').encode()) if ids else b''
        sizes = {}
        for line in output.decode().splitlines():
            oid, kind, size = line.split()
            if kind != 'blob':
                raise ValueError('non-blob in index: ' + oid)
            sizes[oid] = int(size)
        errors = []
        for mode, oid, stage, path in entries:
            reason = prohibited(path)
            if stage != '0':
                errors.append({'path': path, 'reason': 'conflicto sin resolver'})
                continue
            if mode == '160000':
                continue
            size = sizes[oid]
            if reason:
                errors.append({'path': path, 'size': size, 'reason': reason})
            if size > LIMIT:
                item = exceptions.get(path)
                digest = hashlib.sha256(git('cat-file', 'blob', oid)).hexdigest() if item else None
                if not item or item.get('sha256') != digest or item.get('size') != size:
                    errors.append({'path': path, 'size': size, 'reason': '>25 MiB sin excepción explícita para ese contenido'})
        report = {'checked': len(entries), 'limit_bytes': LIMIT, 'errors': errors}
        if args.json:
            print(json.dumps(report, ensure_ascii=True, indent=2))
        else:
            for e in errors:
                print(f"BLOQUEADO: {e['path']}: {e['reason']}", file=sys.stderr)
            print(f"Git: {len(entries)} entradas revisadas, {len(errors)} infracciones.")
        return 1 if errors else 0
    except (subprocess.CalledProcessError, OSError, ValueError, KeyError, TypeError) as exc:
        print('No se puede validar el índice: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
