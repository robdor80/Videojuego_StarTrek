#!/usr/bin/env python3
"""F06-P03: build a logical ship visual catalogue from existing asset metadata.

Does NOT import, redistribute or validate the actual 3D objects.
Usage: python3 desarrollo/integration/f06/build_ship_visual_catalog.py
       [--output PATH] [--check PATH]
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
METADATA_ROOT = ROOT / "assets" / "naves"
REGISTRY = ROOT / "sistemas/gameplay/ship_operations/consoles/sensors/ship_class_registry.json"
DEFAULT_OUT = ROOT / "sistemas/gameplay/ship_operations/consoles/sensors/ships_visual_catalog.json"

def build(root: Path = ROOT) -> dict[str, Any]:
    base = root / "assets" / "naves"
    registry_path = root / "sistemas/gameplay/ship_operations/consoles/sensors/ship_class_registry.json"
    classes = json.loads(registry_path.read_text(encoding="utf-8"))["classes"]
    codes = {c["code"]: c["id"] for c in classes}
    assets: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(base.rglob("metadata.json")):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        if metadata.get("category") != "ship":
            continue
        asset_id = metadata.get("asset_id")
        if not isinstance(asset_id, str) or not asset_id or asset_id in seen:
            raise ValueError(f"Invalid or repeated asset_id at {path}")
        seen.add(asset_id)
        taxonomy = metadata.get("taxonomy") or {}
        inferred = taxonomy.get("ship_class_inferred")
        technical = metadata.get("technical") or {}
        raw_files = technical.get("files") or []
        geometry = []
        for f in raw_files:
            ext = str(f.get("extension") or "").lower()
            if ext != ".glb":
                continue
            name = f.get("path")
            if not isinstance(name, str) or not name or Path(name).name != name:
                raise ValueError(f"Unsafe geometry filename in {path}")
            geometry.append({"name": name, "format": ext})
        proven = metadata.get("provenance") or {}
        assets.append({
            "visual_asset_id": asset_id,
            "display_name": metadata.get("display_name"),
            "class_code_candidate": inferred,
            "class_id_candidate": codes.get(inferred),
            "taxonomy_verified": taxonomy.get("taxonomy_verified") is True,
            "metadata_path": path.relative_to(root).as_posix(),
            "local_assets_directory": path.parent.relative_to(root).as_posix(),
            "geometry_inventory": geometry,
            "license_verified": proven.get("license_verified") is True,
            "ue5_imported": technical.get("ue5_imported") is True,
            "ready_for_sensor_viewer": (
                taxonomy.get("taxonomy_verified") is True
                and proven.get("license_verified") is True
                and technical.get("ue5_imported") is True
                and bool(geometry)
            ),
        })
    assets.sort(key=lambda row: row["metadata_path"])
    return {
        "schema_version": "0.1.0",
        "catalog_id": "f06_ship_visual_catalog",
        "source": "assets/naves/**/metadata.json",
        "status": "METADATA_INVENTORY_ONLY",
        "models_count": len(assets),
        "note": ("25 fichas de metadatos ya existentes; los GLB no están en este commit ni su presencia local, licencia, geometría o importación en Unreal se ha validado. Los IDs no conceden conocimiento a Sensores."),
        "reveal_policy": {"unknown":"no exact model","partial":"generic silhouette","class_probable":"unconfirmed label only",
                          "class_confirmed":"only validated class asset in F07","identity_confirmed":"vessel-specific model only with observed identity"},
        "assets": assets,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build()
    text = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if json.loads(args.check.read_text(encoding="utf-8")) != result:
            raise SystemExit(f"Catalog stale: {args.check}")
        print(f"F06 catalog verified: {result['models_count']} models")
    else:
        output = args.output or DEFAULT_OUT
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(f"F06 catalog written: {result['models_count']} models -> {output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
