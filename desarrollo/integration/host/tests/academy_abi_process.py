"""Real C consumer: process restart, mixed H04 catalog and bounded paging."""
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
    pagination = sys.argv[1] == "pagination"
    consumer, naval_fixture, output = map(Path, sys.argv[2:] if pagination else sys.argv[1:])
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output, prefix="c02-") as directory:
        if pagination:
            check_pagination(consumer, naval_fixture, Path(directory))
            return
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
              f"generations {before[1]} -> {after[1]}; mixed catalog and 65-version paging PASS")


def check_pagination(consumer, naval_fixture, base):
    root = base / "many"
    root.mkdir(mode=0o700)
    campaigns = [run(consumer, "write_many", root, count) for count in (65, 70, 6)]
    run(consumer, "add_slot", root, campaigns[2][0], "beta", 3)
    naval = run(naval_fixture, "naval", root)[0]
    expected = {(c[0], "alpha", v) for c, count in zip(campaigns, (65, 70, 6))
                for v in range(1, count + 1)} | {(naval, "alpha", 1)} | {
                    (campaigns[2][0], "beta", v) for v in range(1, 4)}
    rows = [row.split() for row in run(consumer, "catalog", root)]
    keys = [(row[0], row[8], int(row[7])) for row in rows]
    assert len(keys) == len(set(keys)) == 145 and set(keys) == expected
    assert keys == sorted(keys, key=lambda k: (k[0], k[1], -k[2]))
    assert all(row[3:7] == ["0", "1", "1", "1"] for row in rows)
    assert rows == [row.split() for row in run(consumer, "catalog", root)]
    # Resume an early, a boundary and a late historical version in new processes.
    for campaign, version in ((campaigns[0], 1), (campaigns[0], 64), (campaigns[0], 65),
                              (campaigns[1], 2), (campaigns[1], 70)):
        restored = run(consumer, "history", root, campaign[0], version)
        assert restored[0] == campaign[0] and restored[2:] == campaign[2:]
        assert restored[1] != campaign[1]
    restored = run(consumer, "history", root, campaigns[2][0], 3, "beta")
    assert restored[0] == campaigns[2][0] and restored[2:] == campaigns[2][2:]
    # Corruption on a later page is returned as a row; other campaigns stay usable.
    damaged_key = keys[100]
    slot = root / "campaigns" / damaged_key[0] / "slots" / damaged_key[1] / f"v{damaged_key[2]}"
    (slot / "COMMITTED").write_bytes(b"corrupt")
    damaged = [row.split() for row in run(consumer, "catalog", root)]
    assert [(r[0], r[8], int(r[7])) for r in damaged] == keys
    row = damaged[100]
    assert row[3] == "18" and row[5] == "0" and row[6] == "3", row
    assert sum(r[5] == "1" for r in damaged) == 144
    # Restore an intact campaign, invalidate cursors with SAVE in the same generation.
    intact = next(c[0] for c in campaigns if c[0] != damaged_key[0])
    run(consumer, "cursor_lifecycle", root, intact)
    empty = base / "empty"
    slots = empty / "campaigns" / ("a" * 32) / "slots"
    slots.mkdir(parents=True, mode=0o700)
    for i in range(4200):
        (slots / f"empty_{i:04d}").mkdir()
    run(consumer, "empty_walk", empty)
    print("C02 paging PASS: 145 H04 versions in four campaigns, deterministic complete order, "
          "historical restores, later-page corruption, cursor replay/discard/expiry and empty traversal")


if __name__ == "__main__":
    main()
