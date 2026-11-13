"""Prepare an H04 fixture in a separate process, then run the C-only consumer."""

import os
from pathlib import Path
import subprocess
import sys
import uuid


def main():
    writer, consumer, base = sys.argv[1:]
    root = Path(base).resolve() / uuid.uuid4().hex
    root.mkdir(parents=True, mode=0o700)
    print("Preparing H05 FIXTURE in an independent process", flush=True)
    subprocess.run([writer, "write", os.fspath(root)], check=True, timeout=60)
    campaign = (root / "campaign-id").read_text()
    order, *scan, operation = (root / "request").read_text().split()
    # The existing fixture binds its captain (PERSON 3) and submits F04_SCAN.
    assert operation == "12", operation
    subprocess.run([consumer, "roundtrip", os.fspath(root), campaign, order, "3", *scan],
                   check=True, timeout=60)
    assert (root / "campaigns" / campaign / "slots" / "h06" / "v1" / "COMMITTED").is_file()


if __name__ == "__main__":
    main()
