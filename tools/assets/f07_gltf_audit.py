#!/usr/bin/env python3
"""Inspect a glTF 2.0 GLB, read-only. Static metadata, NOT Blender/UE5 proof.

Validates chunk structure, buffer views/accessors, material and UV references.
Python 3.10+ standard library.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path


def load_glb(path: Path):
    data = Path(path).read_bytes()
    if len(data) < 20:
        raise ValueError("GLB too short")
    magic, version, length = struct.unpack_from("<4sII", data)
    if magic != b"glTF" or version != 2 or length != len(data):
        raise ValueError("Invalid glTF 2.0 header or byte length")
    offset, chunks = 12, []
    while offset < len(data):
        if offset+8 > len(data):
            raise ValueError("Truncated chunk header")
        size, tag = struct.unpack_from("<I4s", data, offset)
        offset += 8
        if size % 4 or offset+size > len(data):
            raise ValueError("Unaligned/truncated GLB chunk")
        chunks.append((tag, data[offset:offset+size]))
        offset += size
    if not chunks or chunks[0][0] != b"JSON":
        raise ValueError("Missing first JSON chunk")
    if len(chunks) > 2 or (len(chunks) == 2 and chunks[1][0] != b"BIN\0"):
        raise ValueError("Unsupported GLB chunks")
    try:
        doc = json.loads(chunks[0][1].decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise ValueError("Invalid GLB JSON") from e
    if doc.get("asset", {}).get("version") != "2.0":
        raise ValueError("Wrong glTF version")
    payload = chunks[1][1] if len(chunks) > 1 else b""
    buffers = doc.get("buffers", [])
    if len(buffers) > 1:
        raise ValueError("Multiple/external buffers not supported by this GLB audit")
    if buffers:
        n = buffers[0].get("byteLength")
        if not isinstance(n, int) or n > len(payload) or len(payload)-n > 3:
            raise ValueError("BIN length mismatch")
    return doc, payload, data


def inspect(path: Path, require_pbr=False):
    doc, payload, data = load_glb(path)
    views = doc.get("bufferViews", [])
    accessors = doc.get("accessors", [])
    for i, v in enumerate(views):
        start, size = v.get("byteOffset", 0), v.get("byteLength", -1)
        if (v.get("buffer") != 0 or not isinstance(start, int) or
                not isinstance(size, int) or min(start, size) < 0 or
                start+size > len(payload)):
            raise ValueError(f"Invalid buffer view: {i}")
    components = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4,
                  "MAT2": 4, "MAT3": 9, "MAT4": 16}
    sizes = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
    for i, a in enumerate(accessors):
        view_id = a.get("bufferView")
        if view_id is None:
            continue  # sparse/implicit data not inspected
        if not isinstance(view_id, int) or not 0 <= view_id < len(views):
            raise ValueError(f"Invalid buffer view for accessor {i}")
        width = components.get(a.get("type"), 0) * sizes.get(a.get("componentType"), 0)
        count, offset = a.get("count", -1), a.get("byteOffset", 0)
        view = views[view_id]
        stride = view.get("byteStride", width)
        if (width == 0 or not isinstance(count, int) or count < 0 or
                not isinstance(offset, int) or offset < 0 or
                not isinstance(stride, int) or stride < width):
            raise ValueError(f"Invalid accessor {i}")
        required = (count-1)*stride+width if count else 0
        if offset+required > view["byteLength"]:
            raise ValueError(f"Accessor outside buffer view: {i}")

    materials = doc.get("materials", [])
    meshes = doc.get("meshes", [])
    triangles = primitive_count = uv_primitives = unlit_primitives = 0
    for mesh in meshes:
        for prim in mesh.get("primitives", []):
            primitive_count += 1
            mat_id = prim.get("material")
            if mat_id is not None and (not isinstance(mat_id, int) or
                                       not 0 <= mat_id < len(materials)):
                raise ValueError("Invalid material reference")
            attrs = prim.get("attributes", {})
            pos_id = attrs.get("POSITION")
            if not isinstance(pos_id, int) or not 0 <= pos_id < len(accessors):
                raise ValueError("Missing/invalid position accessor")
            if "TEXCOORD_0" in attrs:
                uv_id = attrs["TEXCOORD_0"]
                if not isinstance(uv_id, int) or not 0 <= uv_id < len(accessors):
                    raise ValueError("Invalid UV accessor")
                uv_primitives += 1
            count = accessors[pos_id]["count"]
            if "indices" in prim:
                idx = prim["indices"]
                if not isinstance(idx, int) or not 0 <= idx < len(accessors):
                    raise ValueError("Invalid index accessor")
                count = accessors[idx]["count"]
            if prim.get("mode", 4) == 4:
                triangles += count // 3
            if mat_id is not None and "KHR_materials_unlit" in materials[mat_id].get("extensions", {}):
                unlit_primitives += 1

    images = doc.get("images", [])
    for image in images:
        i = image.get("bufferView")
        if i is not None and (not isinstance(i, int) or not 0 <= i < len(views)):
            raise ValueError("Invalid image buffer view")
    for texture in doc.get("textures", []):
        i = texture.get("source")
        if i is not None and (not isinstance(i, int) or not 0 <= i < len(images)):
            raise ValueError("Invalid texture/image reference")

    unlit_materials = sum("KHR_materials_unlit" in mat.get("extensions", {}) for mat in materials)
    pbr_textured = sum("baseColorTexture" in mat.get("pbrMetallicRoughness", {})
                       for mat in materials)
    if require_pbr and (not meshes or unlit_materials or
                        uv_primitives != primitive_count or not pbr_textured):
        raise ValueError("PBR technical fixture requirements not satisfied")

    return {
        "kind": "STATIC_ONLY_NOT_UE5_EVIDENCE",
        "filename": Path(path).name, "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data), "meshes": len(meshes),
        "primitives": primitive_count, "triangles_triangle_modes": triangles,
        "uv_primitives": uv_primitives, "materials": len(materials),
        "unlit_materials": unlit_materials,
        "pbr_basecolor_textured_materials": pbr_textured,
        "unlit_primitives": unlit_primitives, "images": len(images),
        "textures": len(doc.get("textures", [])),
        "animations": len(doc.get("animations", [])),
        "license_declared_not_verified": doc.get("asset", {}).get("extras", {}).get("license"),
        "ue5_import": "NO_EJECUTADO", "rights": "NO_VERIFICADOS"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-pbr", action="store_true")
    parser.add_argument("--expect-sha256")
    args = parser.parse_args()
    report = inspect(args.input, args.require_pbr)
    if args.expect_sha256 and args.expect_sha256.lower() != report["sha256"]:
        parser.error("SHA-256 mismatch: not the audited GLB")
    body = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        dest = args.output.resolve()
        if dest == args.input.resolve():
            parser.error("Refusing to overwrite the GLB input")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
    print(body, end="")


if __name__ == "__main__":
    main()
