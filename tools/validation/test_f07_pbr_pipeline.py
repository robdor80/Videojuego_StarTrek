#!/usr/bin/env python3
"""Reference-only GLB/UV/PBR quality gates; no Blender/Unreal testing."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plate = load_module("f07_plate", ROOT / "tools/assets/f07_pbr_plate.py")
audit = load_module("f07_audit", ROOT / "tools/assets/f07_gltf_audit.py")


class F07PBRPipeline(unittest.TestCase):
    def test_glb_has_real_geometry_uv_and_lit_materials(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "plate.glb"
            manifest = plate.generate(p)
            observed = audit.inspect(p, require_pbr=True)
            self.assertEqual(observed["sha256"], manifest["sha256"])
            self.assertEqual(observed["meshes"], 1)
            self.assertEqual(observed["triangles_triangle_modes"], 64)
            self.assertEqual(observed["primitives"], 2)
            self.assertEqual(observed["uv_primitives"], 2)
            self.assertEqual(observed["materials"], 2)
            self.assertEqual(observed["unlit_materials"], 0)
            self.assertEqual(observed["images"], 4)
            self.assertEqual(observed["ue5_import"], "NO_EJECUTADO")

    def test_generation_reproducible(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/"first.glb", Path(d)/"second.glb"
            self.assertEqual(plate.generate(a)["sha256"],
                             plate.generate(b)["sha256"])
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_never_overwrites_downloaded_source_by_default(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "original.glb"
            source.write_bytes(b"do not touch")
            with self.assertRaises(FileExistsError):
                plate.generate(source)
            self.assertEqual(source.read_bytes(), b"do not touch")

    def test_corrupted_glb_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"broken.glb"
            plate.generate(p)
            p.write_bytes(p.read_bytes()[:-4])
            with self.assertRaises(ValueError):
                audit.inspect(p)

    def test_pbr_guard_rejects_unlit_material(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"plate.glb"
            plate.generate(p)
            doc, bin_data, data = audit.load_glb(p)
            doc["materials"][0]["extensions"] = {"KHR_materials_unlit": {}}
            with mock.patch.object(audit, "load_glb", return_value=(doc, bin_data, data)):
                with self.assertRaisesRegex(ValueError, "PBR"):
                    audit.inspect(p, require_pbr=True)

    def test_static_evidence_never_implies_runtime(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"plate.glb"
            plate.generate(p)
            report = audit.inspect(p)
            self.assertEqual(report["rights"], "NO_VERIFICADOS")
            self.assertNotIn("fps", report)
            self.assertEqual(report["ue5_import"], "NO_EJECUTADO")


if __name__ == "__main__":
    unittest.main()
