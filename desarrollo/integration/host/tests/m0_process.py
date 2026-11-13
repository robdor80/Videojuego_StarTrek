"""Independent writer/reader processes and objective H04 storage measurements."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid


def measure(root):
    campaign = (root / "campaign-id").read_text()
    generations = root / "campaigns" / campaign / "slots" / "alpha"
    seen = set()
    rows = []
    for generation in sorted(generations.glob("v*"), key=lambda p: int(p.name[1:])):
        files = [p for p in generation.rglob("*") if p.is_file()]
        objects = list((generation / "history").glob("*.obj"))
        hashes = [(hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size) for p in objects]
        rows.append({"generation": generation.name, "bytes": sum(p.stat().st_size for p in files),
                     "files": len(files), "objects": len(objects),
                     "object_bytes": sum(size for _, size in hashes),
                     "repeated_objects": sum(digest in seen for digest, _ in hashes),
                     "repeated_bytes": sum(size for digest, size in hashes if digest in seen)})
        seen.update(digest for digest, _ in hashes)
    assert len(rows) >= 3, "Must measure actual successive saves"
    return rows


def main():
    binary, base = sys.argv[1:]
    root = Path(base).resolve() / uuid.uuid4().hex
    root.mkdir(parents=True, mode=0o700)
    evidence = {}
    processes = []
    for scenario, suffix in (("completed", ""), ("pending", "_pending")):
        data = root / scenario
        data.mkdir(mode=0o700)
        for operation in ("write", "read"):
            command = [binary, operation + suffix, str(data)]
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                try:
                    stdout, stderr = process.communicate(timeout=100)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate()
                    raise
                processes.append({"pid": process.pid, "command": command, "returncode": process.returncode})
                (root / f"{scenario}-{operation}.log").write_text(stdout + stderr)
                print(f"{scenario} {operation} pid={process.pid}:\n{stdout}{stderr}", flush=True)
                assert process.returncode == 0, f"{scenario}/{operation} failed: {process.returncode}"
        evidence[scenario] = measure(data)
    (root / "measurements.json").write_text(json.dumps(evidence, indent=2) + "\n")
    assert len({p["pid"] for p in processes}) == 4, "Writer/reader must be fresh processes"
    (root / "processes.json").write_text(json.dumps(processes, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))
    print("PASS: distinct writer/reader processes, completed and pending orders; measurements:", root)


if __name__ == "__main__":
    main()
