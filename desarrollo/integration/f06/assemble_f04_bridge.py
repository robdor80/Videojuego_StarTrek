#!/usr/bin/env python3
"""Assemble F06 bridge from the *unaltered audited F04 source*.

F04 original source and its historical SHA-256 oracle remain immutable.
F06 extends only a build-local derivative, never a second Core campaign.
Every textual insertion is verified against a unique audited anchor.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATCHES = Path(__file__).with_name("f04_bridge_overlay_patches.json")


def create(source: Path, output: Path) -> None:
    spec = json.loads(PATCHES.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / spec["contract_manifest"]).read_text(encoding="utf-8"))
    expected = manifest["contract_files"][spec["source"]]
    original = source.read_bytes().replace(b"\r\n", b"\n")
    digest = hashlib.sha256(original).hexdigest()
    if digest != expected:
        raise ValueError(
            "F04 historical baseline is not intact. "
            f"Expected {expected}, got {digest}; do NOT regenerate frozen oracles."
        )
    text = original.decode("utf-8")
    if spec["schema"] != 1 or len(spec["patches"]) < 1:
        raise ValueError("Unsupported or empty F06 bridge overlay")
    for number, patch in enumerate(spec["patches"], start=1):
        before, after = patch["old"], patch["new"]
        if not before or text.count(before) != 1:
            raise ValueError(f"F06 overlay patch {number} has missing/ambiguous source anchor")
        text = text.replace(before, after, 1)
    if '#include "f06_runtime.inc"' not in text or "f06_poll(*next" not in text:
        raise ValueError("F06 source guard missing after overlay")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8", newline="\n")
    print(f"F06 overlay built from certified F04 source: {len(spec['patches'])} exact patches")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--source", type=Path, required=True)
    cli.add_argument("--out", type=Path, required=True)
    args = cli.parse_args()
    create(args.source, args.out)
