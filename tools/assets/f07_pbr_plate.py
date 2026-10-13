#!/usr/bin/env python3
"""Generate a deterministic UV/PBR armored plate glTF2 GLB for F07.

TECHNICAL SAMPLE, not a Valhalla production asset or proof of UE5 playability.
Python 3.10+ stdlib. Does not read or change original downloaded meshes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import struct
import zlib
from pathlib import Path


def png_rgba(width, height, rgba):
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    scan = b"".join(b"\0" + b"".join(bytes(rgba(x, y)) for x in range(width))
                    for y in range(height))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(scan, 9)) + chunk(b"IEND", b""))


def ring(w, h, c, z):
    return [(-w+c,-h,z),(w-c,-h,z),(w,-h+c,z),(w,h-c,z),
            (w-c,h,z),(-w+c,h,z),(-w,h-c,z),(-w,-h+c,z)]


def model_geometry():
    front = ring(.4, .225, .035, 0)
    shoulder = ring(.372, .197, .032, .018)
    inset = ring(.352, .177, .030, .026)
    back = ring(.4, .225, .035, -.014)
    groups = {0: [], 1: []}

    def triangle(a, b, c, material):
        u = [b[i]-a[i] for i in range(3)]
        v = [c[i]-a[i] for i in range(3)]
        n = (u[1]*v[2]-u[2]*v[1],
             u[2]*v[0]-u[0]*v[2],
             u[0]*v[1]-u[1]*v[0])
        magnitude = math.sqrt(sum(t*t for t in n))
        if magnitude < 1e-12:
            raise ValueError("Degenerate procedural triangle")
        normal = tuple(t/magnitude for t in n)
        for p in (a, b, c):
            groups[material].append((p, normal, ((p[0]+.4)/.8, (p[1]+.225)/.45)))

    for outer, inner in ((front, shoulder), (shoulder, inset)):
        for j in range(8):
            k = (j+1) % 8
            triangle(outer[j], outer[k], inner[k], 0)
            triangle(outer[j], inner[k], inner[j], 0)
    for j in range(8):
        triangle((0., 0., .026), inset[j], inset[(j+1) % 8], 0)
    for j in range(8):
        k = (j+1) % 8
        triangle(front[j], back[j], back[k], 1)
        triangle(front[j], back[k], front[k], 1)
        triangle((0., 0., -.014), back[k], back[j], 1)
    return groups


def build_glb():
    images = [
        png_rgba(64, 64, lambda x, y: (117+(y % 3)*2, 133+(x % 5), 146+(y % 7), 255)),
        png_rgba(64, 64, lambda x, y: (128, 128, 255, 255)),
        png_rgba(64, 64, lambda x, y: (244, 142+(x % 11), 218, 255)),
        png_rgba(16, 16, lambda x, y: (37, 43, 49, 255)),
    ]
    binary = bytearray()
    views, accessors = [], []

    def view(blob, target=None):
        while len(binary) % 4:
            binary.append(0)
        offset = len(binary)
        binary.extend(blob)
        item = {"buffer": 0, "byteOffset": offset, "byteLength": len(blob)}
        if target is not None:
            item["target"] = target
        views.append(item)
        return len(views)-1

    def accessor(values, size, kind, minmax=False):
        index = view(b"".join(struct.pack("<" + "f"*size, *p) for p in values), 34962)
        item = {"bufferView": index, "componentType": 5126,
                "count": len(values), "type": kind}
        if minmax:
            item["min"] = [min(v[i] for v in values) for i in range(size)]
            item["max"] = [max(v[i] for v in values) for i in range(size)]
        accessors.append(item)
        return len(accessors)-1

    groups = model_geometry()
    primitives = []
    for material, vertices in groups.items():
        primitives.append({"attributes": {
            "POSITION": accessor([v[0] for v in vertices], 3, "VEC3", True),
            "NORMAL": accessor([v[1] for v in vertices], 3, "VEC3"),
            "TEXCOORD_0": accessor([v[2] for v in vertices], 2, "VEC2")},
            "material": material, "mode": 4})
    image_names = ("PlateAlbedo", "PlateNormal", "PlateORM", "GasketAlbedo")
    gltf_images = [{"bufferView": view(blob), "mimeType": "image/png", "name": name}
                   for blob, name in zip(images, image_names)]
    while len(binary) % 4:
        binary.append(0)
    doc = {
        "asset": {"version": "2.0", "generator": "Star Trek F07 procedural test v1",
                  "extras": {"kind": "technical_sample", "canonical_asset": False,
                             "units": "metres", "rights": "original procedural geometry"}},
        "scene": 0, "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "F07_ArmorPlate_TechnicalSample"}],
        "meshes": [{"name": "ArmorPlate_UV_PBR_Demo", "primitives": primitives}],
        "buffers": [{"byteLength": len(binary)}],
        "bufferViews": views, "accessors": accessors, "images": gltf_images,
        "samplers": [{"magFilter": 9729, "minFilter": 9987,
                      "wrapS": 10497, "wrapT": 10497}],
        "textures": [{"source": i, "sampler": 0} for i in range(len(images))],
        "materials": [
            {"name": "MI_F07_Armor_Brushed_Demo",
             "pbrMetallicRoughness": {
                 "baseColorTexture": {"index": 0},
                 "metallicRoughnessTexture": {"index": 2},
                 "metallicFactor": 1.0, "roughnessFactor": 1.0},
             "normalTexture": {"index": 1}, "occlusionTexture": {"index": 2}},
            {"name": "MI_F07_Armor_Gasket_Demo",
             "pbrMetallicRoughness": {
                 "baseColorTexture": {"index": 3},
                 "metallicFactor": 0.1, "roughnessFactor": 0.85}}
        ]
    }
    encoded = json.dumps(doc, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")
    encoded += b" " * (-len(encoded) % 4)
    raw = bytes(binary)
    total = 12 + 8 + len(encoded) + 8 + len(raw)
    glb = (struct.pack("<4sII", b"glTF", 2, total) +
           struct.pack("<I4s", len(encoded), b"JSON") + encoded +
           struct.pack("<I4s", len(raw), b"BIN\0") + raw)
    summary = {"kind": "TECHNICAL_SAMPLE_NOT_GAME_ASSET",
               "dimensions_m": [0.8, 0.45, 0.04],
               "triangles": sum(len(g)//3 for g in groups.values()),
               "materials": 2, "embedded_images": 4,
               "uv": "TEXCOORD_0", "pbr": True,
               "blender_tested": False, "ue5_tested": False}
    return glb, summary


def generate(output: Path, force=False):
    output = Path(output)
    if output.exists() and not force:
        raise FileExistsError(f"Output exists: {output}; refuse to overwrite without --force")
    glb, summary = build_glb()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(glb)
    return dict(summary, file=output.name, sha256=hashlib.sha256(glb).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.manifest:
        if args.manifest.resolve() == args.output.resolve():
            parser.error("--manifest and --output must differ")
        if args.manifest.exists() and not args.force:
            parser.error("Manifest exists; refuse to overwrite without --force")
    summary = generate(args.output, args.force)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
