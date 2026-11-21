"""Real C consumer: process restart, mixed H04 catalog and bounded overflow."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(executable, *args):
    result = subprocess.run([str(executable), *map(str, args)], capture_output=True,
                            encoding="utf-8", timeout=90, check=False)
    if result.returncode:
        raise AssertionError(f"{args}: {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout.splitlines()


def main():
    consumer, naval_fixture, output = map(Path, sys.argv[1:])
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output, prefix="c02-") as directory:
        root = Path(directory) / "slots"
        root.mkdir(mode=0o700)
        before = run(consumer, "write", root)
        naval = run(naval_fixture, "naval", root)[0]
        # Each negative is a separate process and never activates an impostor.
        for mode, reason, provenance in (("commit", 18, 3), ("unregistered", 15, 2),
                                         ("core", 14, 3), ("format", 14, 3)):
            damaged = shutil.copytree(root, Path(directory) / mode)
            slot = damaged / "campaigns" / before[0] / "slots/alpha/v1"
            if mode == "commit":
                (slot / "COMMITTED").write_bytes(b"wrong")
            elif mode == "unregistered":
                (damaged / "registry" / before[0]).unlink()
            else:
                lines = (slot / "manifest").read_text().splitlines()
                lines[2 if mode == "core" else 0] = "ef" * 20 if mode == "core" else "TREKHOST4 3"
                envelope = ("\n".join(lines) + "\n").encode("ascii")
                (slot / "manifest").write_bytes(envelope)
                (slot / "COMMITTED").write_bytes(envelope)
            catalog = [row.split() for row in run(consumer, "catalog", damaged)]
            row = next(row for row in catalog if row[0] == before[0])
            assert int(row[3]) == reason and row[5] == "0" and int(row[6]) == provenance, row
            if mode != "format":
                assert row[1:3] == ["2", "2"], row
            if mode in ("core", "format"):
                assert row[4] == "0", row
            run(consumer, "reject", damaged, before[0], reason)
        after = run(consumer, "read", root, before[0])
        assert len(before) == len(after) == 6
        assert before[0] == after[0] and before[1] != after[1]
        assert before[2:] == after[2:]
        assert (root / "campaigns" / before[0] / "slots/alpha/v2/COMMITTED").is_file()
        assert naval != before[0]
        overflow = Path(directory) / "overflow"
        overflow.mkdir(mode=0o700)
        run(consumer, "overflow", overflow)
        print(f"C02 public ABI restart PASS: campaign {before[0]}, PERSON {before[2]}, "
              f"generations {before[1]} -> {after[1]}; mixed catalog and overflow PASS")


if __name__ == "__main__":
    main()
