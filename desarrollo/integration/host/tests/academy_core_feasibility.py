"""Exercise the pinned Core campus fixture with independent writer and reader processes."""
from pathlib import Path
import shutil
import subprocess
import sys
from uuid import uuid4


def run(binary, mode, archive):
    subprocess.run([binary, mode, str(archive)], check=True, timeout=20)


def main():
    binary, output = sys.argv[1:]
    root = Path(output) / uuid4().hex
    root.mkdir(parents=True)
    archive = root / "academy"
    run(binary, "write", archive)
    run(binary, "read", archive)

    damaged = root / "damaged"
    shutil.copytree(archive, damaged)
    # CRPGROOT v1 ends with the 32-byte hash of the active manifest.
    manifest_hash = (damaged / "CURRENT").read_bytes()[-32:].hex()
    manifest = damaged / f"{manifest_hash}.obj"
    data = bytearray(manifest.read_bytes())
    data[-1] ^= 1
    manifest.write_bytes(data)
    run(binary, "reject", damaged)


if __name__ == "__main__":
    main()
