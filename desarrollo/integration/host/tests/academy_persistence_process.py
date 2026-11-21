"""Exercise the real TrekHost API in separate processes and build bounded H04 fixtures."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(exe, *args, code=0):
    result = subprocess.run([str(exe), *map(str, args)], capture_output=True,
                            encoding="utf-8", timeout=45, check=False)
    if result.returncode != code:
        raise AssertionError(f"{args}: exit {result.returncode}, expected {code}\n"
                             f"{result.stdout}\n{result.stderr}")
    return result.stdout.splitlines()


def slot(root, campaign, version=1, name="alpha"):
    return root / "campaigns" / campaign / "slots" / name / f"v{version}"


def new_root(base, name):
    root = base / name
    root.mkdir(mode=0o700)
    return root


def committed(path):
    manifest = (path / "manifest").read_bytes()
    assert (path / "COMMITTED").read_bytes() == manifest
    return manifest.decode("ascii").splitlines()


def write_envelope(path, lines):
    data = ("\n".join(lines) + "\n").encode("ascii")
    for filename in ("manifest", "COMMITTED"):
        (path / filename).write_bytes(data)


def restore(exe, root, expected, version=0, mode="read", name="alpha"):
    return run(exe, mode, root, expected[0], name, version, expected[1])


def same_progress(before, after):
    assert before[0] == after[0] and before[1] != after[1]
    assert before[3:] == after[3:], (before, after)


def process(product, base):
    root = new_root(base, "main")
    before = run(product, "write", root)
    campaign = before[0]
    assert committed(slot(root, campaign))[:2] == ["TREKHOST4 2", "ACADEMY"]
    registry = (root / "registry" / campaign).read_bytes()
    resumed = restore(product, root, before, mode="resume")
    same_progress(before, resumed)
    assert before[2] == "0 0" and resumed[2] == "1 0"
    committed(slot(root, campaign, 2))
    assert (root / "registry" / campaign).read_bytes() == registry
    latest = restore(product, root, before)
    assert latest[2] == "2 0"
    same_progress(before, latest)
    retired = restore(product, root, before, version=1)
    same_progress(before, retired)
    assert retired[2] == "1 0"
    print(f"Three independent restores. Campaign {campaign}, candidate {latest[3]}, "
          f"checkpoint SHA-256 {latest[7]}. Tokens {before[1]}, {resumed[1]}, {latest[1]}, {retired[1]}.")

    ship = run(product, "naval", root)[0]
    assert committed(slot(root, ship))[0] == "TREKHOST4 1"
    run(product, "mixed", root, campaign, ship)
    run(product, "inspect", root, campaign, ship)
    run(product, "rebind", new_root(base, "rebind"))


def retarget(path, lines, progress=None):
    current = (path / "history" / "CURRENT").read_bytes()
    lines[10] = hashlib.sha256(current).hexdigest()
    if progress is not None:
        lines[9] = progress
    write_envelope(path, lines)


def negative(product, faults, base):
    root = new_root(base, "seed")
    before = run(product, "write", root)
    campaign = before[0]
    original = slot(root, campaign)
    lines = committed(original)

    def clone(name):
        return shutil.copytree(root, base / name)

    def rejects(where, error="corrupt", version=0):
        run(product, "reject", where, campaign, "alpha", version, error)

    broken = clone("bad-manifest")
    (slot(broken, campaign) / "manifest").write_bytes(b"TREKHOST4 2\nACADEMY\n")
    rejects(broken, "incompatible")

    bad_commit = clone("bad-commit")
    (slot(bad_commit, campaign) / "COMMITTED").write_bytes(b"wrong")
    rejects(bad_commit)

    bad_pointer = clone("bad-pointer")
    current = slot(bad_pointer, campaign) / "history" / "CURRENT"
    pointer = current.read_bytes()
    current.write_bytes(pointer[:-1] + bytes([pointer[-1] ^ 1]))
    rejects(bad_pointer)

    bad_campaign = clone("bad-address")
    altered = lines.copy()
    altered[3] = "ef" * 16
    write_envelope(slot(bad_campaign, campaign), altered)
    rejects(bad_campaign)

    wrong_core = clone("core-pin")
    altered = lines.copy()
    altered[2] = "ef" * 20
    write_envelope(slot(wrong_core, campaign), altered)
    rejects(wrong_core, "incompatible")

    unknown_format = clone("unknown-format")
    altered = lines.copy()
    altered[0] = "TREKHOST4 3"
    write_envelope(slot(unknown_format, campaign), altered)
    rejects(unknown_format, "incompatible")

    bad_clock = clone("clock-mismatch")
    altered = lines.copy()
    altered[9] = lines[9].split()[0] + " 900"
    write_envelope(slot(bad_clock, campaign), altered)
    rejects(bad_clock, "identity")

    for field, index in (("catalog", 6), ("source", 7)):
        altered_root = clone(field)
        altered = lines.copy()
        altered[index] = altered[index][:-64] + "ab" * 32
        write_envelope(slot(altered_root, campaign), altered)
        registry = altered_root / "registry" / campaign
        registry.write_bytes(registry.read_bytes().replace(lines[index].encode(), altered[index].encode()))
        rejects(altered_root, "incompatible")

    imported = new_root(base, "imported")
    shutil.copytree(root / "campaigns", imported / "campaigns")
    rejects(imported, "untrusted")

    profile = clone("profile")
    registry = profile / "registry" / campaign
    changed = registry.read_bytes().splitlines()
    fields = changed[-1].split()
    fields[2] = b"aa" * 16
    changed[-1] = b" ".join(fields)
    registry.write_bytes(b"\n".join(changed) + b"\n")
    rejects(profile, "identity")

    links = clone("linked-file")
    os.link(slot(links, campaign) / "history" / "CURRENT", base / "second-link")
    rejects(links, "path")

    latest_broken = clone("latest-broken")
    restore(product, latest_broken, before, mode="resume")
    latest = slot(latest_broken, campaign, 2)
    active_root = (latest / "history" / "CURRENT").read_bytes()[-32:].hex()
    (latest / "history" / (active_root + ".obj")).write_bytes(b"truncated Core object")
    rejects(latest_broken)
    same_progress(before, restore(product, latest_broken, before, version=1))

    for mode, reason in (("missing-person", "identity"), ("duplicate-person", "identity"),
                         ("wrong-subject", "identity"), ("background", "identity"),
                         ("admitted", "corrupt"), ("legacy", "corrupt")):
        altered = clone(mode)
        target = slot(altered, campaign, 1, "changed")
        target.mkdir(parents=True)
        [progress] = run(faults, mode, root, campaign, "alpha", 1, target / "history")
        envelope = lines.copy()
        envelope[4] = "changed"
        retarget(target, envelope, progress)
        run(product, "reject", altered, campaign, "changed", 1, reason)

    foreign_root = new_root(base, "foreign")
    other = run(product, "write", foreign_root)
    assert other[0] != campaign and other[3].split()[0:2] == before[3].split()[0:2]
    swapped = clone("foreign-core")
    foreign_history = slot(swapped, campaign, 1, "changed")
    foreign_history.mkdir(parents=True)
    shutil.copytree(slot(foreign_root, other[0]) / "history", foreign_history / "history")
    envelope = lines.copy()
    envelope[4] = "changed"
    retarget(foreign_history, envelope)
    run(product, "reject", swapped, campaign, "changed", 1, "identity")
    print("Rejected corrupted, imported, incompatible, linked, foreign and structurally invalid slots.")


def advanced(product, faults, base):
    root = new_root(base, "progress")
    before = run(product, "write", root)
    campaign = before[0]
    target = slot(root, campaign, 1, "advanced")
    target.mkdir(parents=True)
    progress, core_digest = run(faults, "advanced", root, campaign, "alpha", 1, target / "history")
    lines = committed(slot(root, campaign))
    registry_before = (root / "registry" / campaign).read_bytes()
    original_anchor = lines[6:9]
    lines[4] = "advanced"
    retarget(target, lines, progress)
    resumed = restore(product, root, before, name="advanced", mode="resume")
    assert resumed[2] == "2 1" and resumed[7] == core_digest
    assert resumed[3].split()[:2] == before[3].split()[:2]
    assert resumed[3].split()[2] != before[3].split()[2] and resumed[3].split()[4] == "31"
    assert resumed[7] != before[7]
    assert resumed[8:] == before[8:]
    assert committed(slot(root, campaign, 2))[6:9] == original_anchor
    assert (root / "registry" / campaign).read_bytes() == registry_before

    latest = restore(product, root, before)
    same_progress(resumed, latest)
    assert latest[2] == "3 1"
    segments = [p for p in (target / "history").glob("*.obj") if p.read_bytes().startswith(b"CRPGSEG1")]
    assert len(segments) == 1
    assert (slot(root, campaign, 2) / "history" / segments[0].name).read_bytes() == segments[0].read_bytes()
    same_progress(before, restore(product, root, before, version=1))
    damaged = shutil.copytree(root, base / "bad-segment")
    (slot(damaged, campaign, 2) / "history" / segments[0].name).write_bytes(b"truncated segment")
    run(product, "reject", damaged, campaign, "alpha", 0, "corrupt")
    same_progress(before, restore(product, damaged, before, version=1))
    print(f"Preserved Core segment {segments[0].name}, advanced checkpoint {core_digest}, and unchanged H03 anchor.")


def interruptions(product, faults, base):
    root = new_root(base, "interruptions")
    before = run(product, "write", root)
    campaign = before[0]
    count = 1
    for where in ("before_snapshot", "copy_file", "file_sync", "after_snapshot", "partial_write",
                  "after_manifest", "before_publish", "crash", "publish_rename", "after_publish", "before_ack"):
        run(faults, "fault", root, campaign, "alpha", 0, where, code=73 if where == "crash" else 0)
        count += int(where in {"after_publish", "before_ack"})
        assert len(list(slot(root, campaign).parent.glob("v*/COMMITTED"))) == count, where
        same_progress(before, restore(product, root, before))
    run(faults, "close", root, campaign, "alpha")
    same_progress(before, restore(product, root, before, mode="resume"))
    print("Process interruption, publication uncertainty, retry and concurrent CLOSE passed.")


if __name__ == "__main__":
    mode, destination, product_exe, *fault_exe = sys.argv[1:]
    parent = Path(destination).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix=f"{mode}-", dir=parent))
    product_path = Path(product_exe).resolve()
    if mode == "process":
        process(product_path, base)
    else:
        group = {"negative": negative, "advanced": advanced, "interruptions": interruptions}[mode]
        group(product_path, Path(fault_exe[0]).resolve(), base)
