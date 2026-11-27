"""Apply the HOST-only extension to a build copy of the frozen F04 bridge."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile


git, source, patch, output = sys.argv[1:]
source, patch, output = (Path(path).resolve() for path in (source, patch, output))
output.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="f04-bridge-", dir=output.parent) as temporary:
    staging = Path(temporary)
    candidate = staging / output.name
    candidate.write_bytes(source.read_bytes().replace(b"\r\n", b"\n"))
    extension = staging / "extension.patch"
    extension.write_bytes(patch.read_bytes().replace(b"\r\n", b"\n"))
    flags = ["apply", "--no-index", "--whitespace=error"]
    # Isolate the copy even when the build directory is inside the repository.
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(output.parent)}
    subprocess.run([git, *flags, str(extension)], cwd=staging, env=env, check=True)
    candidate.replace(output)
