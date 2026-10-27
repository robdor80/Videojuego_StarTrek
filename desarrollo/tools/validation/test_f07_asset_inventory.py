#!/usr/bin/env python3
"""QA de catálogo y decisiones F07. NO valida Unreal/Blender."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "f07_inventory", ROOT / "desarrollo/tools/assets/f07_inventory.py")
assert spec is not None and spec.loader is not None
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)

class F07InventoryTests(unittest.TestCase):
    def test_read_only_aliases_and_filter(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "Puentes" / "star_trek_sutherland_bridge_Validado_ae9e06f1.glb"
            source.parent.mkdir()
            source.write_bytes(b"model fixture")
            (root / "ignore.txt").write_text("irrelevant", encoding="utf-8")
            before = source.read_bytes()
            data = inv.build_inventory(root)
            self.assertEqual(data["total"], 1)
            item = data["files"][0]
            self.assertEqual(item["nombre_original"], source.name)
            self.assertEqual(item["nombre_amigable"], "star trek sutherland bridge")
            self.assertEqual(item["categoria_sugerida"], "bridge")
            self.assertEqual(item["licencia"], "PENDIENTE")
            self.assertIsNone(item["sha256"])
            self.assertEqual(source.read_bytes(), before)

    def test_stable_ids_optional_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Starship.fbx").write_bytes(b"ship")
            a, b = inv.build_inventory(root, True), inv.build_inventory(root, True)
            self.assertEqual(a, b)
            self.assertEqual(a["files"][0]["categoria_sugerida"], "ship")
            self.assertEqual(len(a["files"][0]["sha256"]), 64)

    def test_selection_registry_and_real_evidence_pending(self):
        registry = json.loads((ROOT / "assets/otros/escenas/bridges/f07_registry.json").read_text(encoding="utf-8"))
        items = {x["asset_id"]: x for x in registry["entries"]}
        self.assertEqual(items["bridge-sutherland-original"]["ue5_status"], "NO_EJECUTADO")
        self.assertFalse(items["bridge-sutherland-original"]["rights_verified"])
        self.assertEqual(items["bridge-kelvin-reserved"]["selection"], "EXCLUIDO_PROTOTIPO")
        record = json.loads((ROOT / "proyecto/docs/roadmap/master/fases/F07/EVIDENCIA_Y_PENDIENTES.json").read_text(encoding="utf-8"))
        self.assertEqual(record["package"]["status"], "NO_EJECUTADO")
        self.assertEqual(len(record["tests_ue5"]), 9)
        self.assertTrue(all(x["status"] == "NO_EJECUTADO" for x in record["tests_ue5"].values()))

if __name__ == "__main__":
    unittest.main()
