"""Bounded process-loss protocol; each invocation has an independent storage root."""
import pathlib
import subprocess
import sys
import uuid

binary, destination = sys.argv[1:]
root = pathlib.Path(destination) / uuid.uuid4().hex

def run(*args, expected=0):
    result = subprocess.run([binary, *map(str, args)], timeout=25, capture_output=True, text=True)
    assert result.returncode == expected, (args, result.returncode, result.stdout, result.stderr)

run('write', root / 'normal')
run('read', root / 'normal')
for point in ('partial_write', 'before_snapshot', 'after_snapshot', 'after_manifest', 'before_publish', 'after_publish', 'before_ack'):
    folder = root / point
    run('write', folder)
    run('crash', folder, point, expected=73)
    run('read', folder)
    print('PASS process loss:', point)
