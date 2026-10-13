#!/usr/bin/env python3
"""F07: catálogo local, SOLO lectura de originales. Python 3.10+."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

EXTENSIONS = {".glb", ".gltf", ".fbx", ".blend", ".obj", ".mtl",
    ".dae", ".stl", ".usd", ".usdz", ".abc", ".3ds", ".ply",
    ".uasset", ".umap", ".png", ".jpeg", ".jpg", ".tga", ".tif",
    ".tiff", ".webp", ".exr", ".hdr", ".dds", ".ktx2", ".bmp",
    ".zip", ".7z", ".rar", ".cr2"}
TEXTURES = {".png", ".jpeg", ".jpg", ".tga", ".tif", ".tiff",
            ".webp", ".exr", ".hdr", ".dds", ".ktx2", ".bmp"}
ARCHIVES = {".zip", ".7z", ".rar"}

def category_for(relative: str, suffix: str) -> str:
    if suffix in ARCHIVES:
        return "archive"
    if suffix in TEXTURES:
        return "texture"
    name = relative.casefold()
    for label, keywords in (
        ("bridge", ("bridge", "puente", "sutherland", "kelvin")),
        ("station", ("station", "estacion", "starbase", "spacedock")),
        ("npc", ("character", "personaje", "npc", "crew", "uniform")),
        ("ship", ("starship", "nave", "ship", "enterprise", "voyager")),
        ("prop", ("prop", "console", "consola", "objeto", "chair")),
    ):
        if any(keyword in name for keyword in keywords):
            return label
    return "unknown"

def friendly_name(stem: str) -> str:
    # Solo etiqueta de interfaz, nunca renombrado en disco.
    stem = re.sub(r"[_\-\s]+Validado[_\-\s]+[a-fA-F0-9]{8,}$",
                  "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[_\-\s]+Rob3D[_\-\s]*\d{6,}$",
                  "", stem, flags=re.IGNORECASE)
    return re.sub(r"[_\s]+", " ", stem).strip() or "(sin nombre)"

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def build_inventory(root: Path, hash_files: bool = False) -> dict:
    root = root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("La ruta raíz debe ser una carpeta.")
    rows = []
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        ext = path.suffix.casefold()
        if ext not in EXTENSIONS:
            continue
        relative = path.relative_to(root).as_posix()
        rows.append({
            "asset_id": "asset-" + hashlib.sha256(
                relative.encode("utf-8")).hexdigest()[:12],
            "ruta_relativa": relative,
            "nombre_original": path.name,
            "nombre_amigable": friendly_name(path.stem),
            "extension": ext,
            "tamano_bytes": path.stat().st_size,
            "categoria_sugerida": category_for(relative, ext),
            "sha256": file_sha256(path) if hash_files else None,
            "procedencia": "PENDIENTE",
            "licencia": "PENDIENTE",
            "validacion_ue5": "NO_EJECUTADO",
        })
    rows.sort(key=lambda row: (row["ruta_relativa"].casefold(),
                               row["ruta_relativa"]))
    return {"schema_version": "1.0.0",
            "kind": "local_inventory_not_runtime_evidence",
            "total": len(rows), "hashes_calculated": hash_files,
            "files": rows}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--hash-files", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve(strict=True)
    output = args.output.expanduser().resolve()
    if output == root or root in output.parents:
        parser.error("--output debe estar fuera de la carpeta de recursos.")
    catalog = build_inventory(root, hash_files=args.hash_files)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"Inventariados {catalog['total']} archivos: {output}")

if __name__ == "__main__":
    main()
